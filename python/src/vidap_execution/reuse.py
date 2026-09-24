"""Visible sharing within one dispatch, without a persistent cache."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite

from .dispatch import IncomingValue
from .planner import ExecutionPlan

KEY_REVISION = "vidap.attempt-output-key/1.0"
_REFERENCE = re.compile(r"sha256:[0-9a-f]{64}")


class UnreferencedOutput(ValueError):
    """An opaque result has no approved content identity."""


@dataclass(frozen=True, slots=True)
class TrustedValue:
    """First-party handler supplied content digest for an opaque in-memory value."""

    value: object
    content_ref: str

    def __post_init__(self) -> None:
        if not _REFERENCE.fullmatch(self.content_ref):
            raise ValueError("trusted content reference must be a SHA-256 digest")


@dataclass(frozen=True, slots=True)
class ReuseEvent:
    kind: str
    source_node_id: str
    source_port_key: str
    composite_key: str
    content_ref: str
    consumer_node_id: str | None = None
    consumer_port_key: str | None = None


def canonical_json(value: object) -> bytes:
    """Canonical JSON with accepted UTF-16 property ordering."""

    def ordered(item: object) -> object:
        if isinstance(item, Mapping):
            if not all(isinstance(key, str) for key in item):
                raise ValueError("JSON names must be text")
            return {
                key: ordered(item[key])
                for key in sorted(item, key=lambda key: key.encode("utf-16-be"))
            }
        if isinstance(item, (tuple, list)):
            return [ordered(child) for child in item]
        if item is None or type(item) in (bool, str, int):
            return item
        if type(item) is float and isfinite(item):
            return item
        raise ValueError("value has no canonical JSON representation")

    return json.dumps(
        ordered(value), ensure_ascii=False, allow_nan=False, separators=(",", ":")
    ).encode("utf-8")


def scalar_ref(value: object) -> str:
    if value is not None and type(value) not in (bool, int, float):
        raise UnreferencedOutput(
            "only controlled scalar values have derived references"
        )
    if type(value) is int and not -(2**63) <= value < 2**63:
        raise UnreferencedOutput("integer exceeds signed 64-bit boundary")
    try:
        encoded = canonical_json(value)
    except ValueError as error:
        raise UnreferencedOutput("scalar cannot be canonically encoded") from error
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def composite_key(
    operation_key: str,
    binding_revision: str,
    parameters: Mapping[str, object],
    ordered_input_refs: tuple[str, ...],
    semantic_digest: str,
    seed: int | None,
    environment: Mapping[str, object],
) -> str:
    projection = {
        "revision": KEY_REVISION,
        "operationKey": operation_key,
        "bindingRevision": binding_revision,
        "parameters": parameters,
        "orderedInputRefs": ordered_input_refs,
        "semanticDigest": semantic_digest,
        "seed": seed,
        "environment": environment,
    }
    return hashlib.sha256(canonical_json(projection)).hexdigest()


class AttemptLedger:
    """Mutable only during one dispatch; records observed output and consumption."""

    def __init__(
        self, plan: ExecutionPlan, seed: int | None, environment: Mapping[str, object]
    ) -> None:
        self._plan = plan
        self._seed = seed
        self._environment = environment
        self._nodes = {node.node_id: node for node in plan.representation.nodes}
        self._incoming: dict[str, list[str]] = {
            node_id: [] for node_id in plan.schedule
        }
        self._outputs: dict[tuple[str, str], tuple[str, str]] = {}
        self.events: list[ReuseEvent] = []

    def on_consume(self, incoming: IncomingValue) -> None:
        key, reference = self._outputs[
            (incoming.source_node_id, incoming.source_port_key)
        ]
        self._incoming[incoming.target_node_id].append(reference)
        self.events.append(
            ReuseEvent(
                "reused-within-attempt",
                incoming.source_node_id,
                incoming.source_port_key,
                key,
                reference,
                incoming.target_node_id,
                incoming.target_port_key,
            )
        )

    def on_outputs(
        self, node_id: str, staged: Mapping[str, object]
    ) -> dict[str, object]:
        """Validate every output before publishing any output event."""

        references: dict[str, str] = {}
        actual: dict[str, object] = {}
        for port_key, value in staged.items():
            if isinstance(value, TrustedValue):
                references[port_key] = value.content_ref
                actual[port_key] = value.value
            else:
                references[port_key] = scalar_ref(value)
                actual[port_key] = value
        node = self._nodes[node_id]
        key = composite_key(
            node.operation_key,
            node.binding_revision,
            node.parameters,
            tuple(self._incoming[node_id]),
            self._plan.representation.semantic_digest,
            self._seed,
            self._environment,
        )
        for port_key, reference in references.items():
            self._outputs[(node_id, port_key)] = (key, reference)
            self.events.append(
                ReuseEvent("computed", node_id, port_key, key, reference)
            )
        return actual

    def input_refs(self, node_id: str) -> tuple[str, ...]:
        return tuple(self._incoming[node_id])
