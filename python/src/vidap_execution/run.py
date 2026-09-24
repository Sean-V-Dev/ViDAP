"""Synchronous, in-process attempt records around accepted planning/dispatch."""

from __future__ import annotations

import hashlib
import platform
import time
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from math import isfinite
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.vidap_workflow import NodeRegistry, WorkflowDocument
else:
    from vidap_workflow import NodeRegistry, WorkflowDocument

from .artifacts import (
    ArtifactRefusal,
    begin_attempt,
    publish_terminal,
    rollback_unpublished,
)
from .bindings import BindingMap
from .diagnostics import RuntimeDiagnostic, diagnostic
from .dispatch import DispatchResult, RuntimeTable, dispatch, preflight_dispatch
from .planner import plan_execution
from .reuse import AttemptLedger, ReuseEvent

RECORD_FORMAT = "vidap.attempt-ownership/1.0"
RECORD_REVISION = "vidap.run-record/1.0"
_CHECKOUT = Path(__file__).resolve().parents[3]


class AttemptRefusal(ValueError):
    """A valid workflow uses values outside this controlled scalar proof."""


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(_freeze(item) for item in value)
    return value


@dataclass(frozen=True, slots=True)
class AttemptRecord:
    data: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "data", _freeze(self.data))


@dataclass(frozen=True, slots=True)
class AttemptResult:
    record: AttemptRecord
    dispatch_result: DispatchResult | None


def _scalar(value: object) -> None:
    if value is None or type(value) is bool:
        return
    if type(value) is int and -(2**63) <= value < 2**63:
        return
    if type(value) is float and isfinite(value):
        return
    raise AttemptRefusal("resolved parameter exceeds controlled scalar policy")


def _fingerprint() -> dict[str, object]:
    locks: dict[str, str] = {}
    for name, path in (
        ("package-lock.json", _CHECKOUT / "package-lock.json"),
        ("python/uv.lock", _CHECKOUT / "python" / "uv.lock"),
    ):
        if not path.is_file() or path.is_symlink():
            raise AttemptRefusal("required lock authority is missing or unsafe")
        try:
            locks[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as error:
            raise AttemptRefusal("required lock authority is unreadable") from error
    return {
        "pythonImplementation": platform.python_implementation(),
        "pythonVersion": platform.python_version(),
        "osFamily": platform.system(),
        "architecture": platform.machine(),
        "lockSha256": locks,
    }


def _utc() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds")


def _event(event: ReuseEvent) -> dict[str, object]:
    return {
        "kind": event.kind,
        "sourceNodeId": event.source_node_id,
        "sourcePortKey": event.source_port_key,
        "compositeKey": event.composite_key,
        "contentRef": event.content_ref,
        "consumerNodeId": event.consumer_node_id,
        "consumerPortKey": event.consumer_port_key,
    }


def _diagnostic(item: RuntimeDiagnostic) -> dict[str, object]:
    return {
        "category": item.category,
        "code": item.code,
        "attemptId": item.attempt_id,
        "operationKey": item.operation_key,
        "nodeId": item.node_id,
        "portKey": item.port_key,
        "outcome": item.outcome,
        "explanation": item.explanation,
        "remedy": item.remedy,
        "technical": {
            "type": item.technical.type,
            "message": item.technical.message,
            "traceback": list(item.technical.traceback),
            "causes": list(item.technical.causes),
        },
    }


def run_attempt(
    document: WorkflowDocument,
    registry: NodeRegistry,
    bindings: BindingMap,
    table: RuntimeTable,
    *,
    seed: int | None = None,
) -> AttemptResult:
    """Refuse before allocation; dispatch once after publishing pending ownership."""

    plan = plan_execution(document, registry, bindings)
    preflight_dispatch(plan, table)
    if seed is not None and (type(seed) is not int or not -(2**63) <= seed < 2**63):
        raise AttemptRefusal("seed must be an optional signed 64-bit integer")
    for node in plan.representation.nodes:
        for value in node.parameters.values():
            _scalar(value)
    environment = _fingerprint()
    attempt_id = str(uuid.uuid4())
    started_at = _utc()
    started_clock = time.perf_counter()
    allocation_failed = False
    try:
        begin_attempt(attempt_id)
    except FileExistsError as error:
        raise ArtifactRefusal("attempt UUID collision") from error
    except ArtifactRefusal, OSError:
        allocation_failed = True
    ledger = AttemptLedger(plan, seed, environment)
    result = None if allocation_failed else dispatch(plan, table, observer=ledger)
    reason = result.stop_reason if result is not None else None
    diagnostics: list[RuntimeDiagnostic] = []
    if allocation_failed:
        diagnostics.append(diagnostic("publication-failed", attempt_id))
    if reason is not None:
        diagnostics.append(
            diagnostic(
                reason.code,
                attempt_id,
                reason.operation_key,
                reason.node_id,
                reason.port_key,
                reason.technical,
            )
        )
    completed = set(result.completed_node_ids) if result is not None else set()
    blocked = set(result.blocked_node_ids) if result is not None else set()
    unrelated = (
        set(result.unrelated_unstarted_node_ids)
        if result is not None
        else set(plan.schedule)
    )
    nodes: list[dict[str, object]] = []
    for node_id in plan.schedule:
        node = next(
            item for item in plan.representation.nodes if item.node_id == node_id
        )
        status = (
            "completed"
            if node_id in completed
            else "failed"
            if result is not None and node_id == result.failed_node_id
            else "blocked"
            if node_id in blocked
            else "unrelated"
            if node_id in unrelated
            else "unrelated"
        )
        nodes.append(
            {
                "nodeId": node_id,
                "operationKey": node.operation_key,
                "bindingRevision": node.binding_revision,
                "parameters": dict(node.parameters),
                "orderedInputRefs": list(ledger.input_refs(node_id)),
                "status": status,
            }
        )
    outcome = "failed" if reason is not None or allocation_failed else "succeeded"
    record: dict[str, Any] = {
        "format": RECORD_FORMAT,
        "revision": RECORD_REVISION,
        "state": outcome,
        "attemptId": attempt_id,
        "workflowId": plan.representation.workflow_id,
        "semanticDigest": plan.representation.semantic_digest,
        "contractSnapshotRef": plan.representation.contract_snapshot_ref,
        "planRevision": plan.revision,
        "bindingRevision": plan.representation.binding_revision,
        "runtimeTableRevision": plan.runtime_table_revision,
        "nodes": nodes,
        "seed": seed,
        "environment": environment,
        "startedAt": started_at,
        "endedAt": _utc(),
        "elapsedMs": max(0.0, (time.perf_counter() - started_clock) * 1000),
        "attemptedNodeIds": list(result.attempted_node_ids) if result else [],
        "completedNodeIds": list(result.completed_node_ids) if result else [],
        "failedNodeId": result.failed_node_id if result else None,
        "blockedNodeIds": list(result.blocked_node_ids) if result else [],
        "unrelatedNodeIds": list(result.unrelated_unstarted_node_ids)
        if result
        else list(plan.schedule),
        "outcome": outcome,
        "reuseEvents": [_event(item) for item in ledger.events],
        "diagnostics": [_diagnostic(item) for item in diagnostics],
        "publication": "failed-before-dispatch" if allocation_failed else "published",
        "ownedSlots": sorted(
            (
                "record.json",
                "proof-output.bin",
                "record.json.tmp",
                "proof-output.bin.tmp",
            )
        ),
        "artifacts": [] if allocation_failed else ["record.json"],
    }
    if not allocation_failed:
        try:
            publish_terminal(attempt_id, record)
        except ArtifactRefusal, OSError:
            record["state"] = "failed"
            record["outcome"] = "failed"
            record["publication"] = "failed-pending"
            record["diagnostics"].append(
                _diagnostic(diagnostic("publication-failed", attempt_id))
            )
            try:
                rollback_unpublished(attempt_id)
            except ArtifactRefusal, OSError:
                record["publication"] = "failed-cleanup-incomplete"
            record["artifacts"] = []
    return AttemptResult(AttemptRecord(record), result)
