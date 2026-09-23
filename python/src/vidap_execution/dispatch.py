"""Invocation-local sequential control for explicit first-party handlers."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from .bindings import StaticBinding
from .planner import ExecutionPlan
from .representation import ExecutionNode


@dataclass(frozen=True, slots=True)
class IncomingValue:
    edge_id: str
    source_node_id: str
    source_port_key: str
    target_node_id: str
    target_port_key: str
    value: object


type Handler = Callable[
    [Mapping[str, object], tuple[IncomingValue, ...]], Mapping[str, object]
]


@dataclass(frozen=True, slots=True)
class RuntimeRegistration:
    operation_key: str
    binding_revision: str
    handler: Handler = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        StaticBinding(self.operation_key, self.binding_revision)
        if not callable(self.handler):
            raise ValueError("runtime registration requires a handler")


@dataclass(frozen=True, slots=True)
class RuntimeTable:
    """Code-constructed handler authority; no document-driven discovery."""

    revision: str
    registrations: tuple[RuntimeRegistration, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "registrations", tuple(self.registrations))
        if not all(
            isinstance(item, RuntimeRegistration) for item in self.registrations
        ):
            raise ValueError("runtime table requires registrations")


class DispatchRefusal(ValueError):
    """Whole-table preflight refusal before any handler invocation."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class StopReason:
    category: str
    code: str
    node_id: str
    operation_key: str
    technical_type: str | None = None


@dataclass(frozen=True, slots=True)
class DispatchResult:
    """Observations and port values owned by one dispatch call only."""

    attempted_node_ids: tuple[str, ...]
    completed_node_ids: tuple[str, ...]
    failed_node_id: str | None
    blocked_node_ids: tuple[str, ...]
    unrelated_unstarted_node_ids: tuple[str, ...]
    stop_reason: StopReason | None
    port_results: Mapping[tuple[str, str], object]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "port_results", MappingProxyType(dict(self.port_results))
        )


def _handlers(
    plan: ExecutionPlan, table: RuntimeTable
) -> dict[tuple[str, str], Handler]:
    if table.revision != plan.runtime_table_revision:
        raise DispatchRefusal("table-revision-mismatch")
    found: dict[tuple[str, str], Handler] = {}
    for registration in table.registrations:
        pair = (registration.operation_key, registration.binding_revision)
        if pair in found:
            raise DispatchRefusal("duplicate-handler")
        found[pair] = registration.handler
    for node in plan.representation.nodes:
        pair = (node.operation_key, node.binding_revision)
        if pair not in found:
            if any(key == node.operation_key for key, _ in found):
                raise DispatchRefusal("handler-revision-mismatch")
            raise DispatchRefusal("missing-handler")
    return found


def _failure(
    plan: ExecutionPlan,
    completed: list[str],
    failed: ExecutionNode,
    code: str,
    results: dict[tuple[str, str], object],
    technical_type: str | None = None,
) -> DispatchResult:
    successors: dict[str, set[str]] = {
        node.node_id: set() for node in plan.representation.nodes
    }
    for edge in plan.representation.edges:
        successors[edge.source_node_id].add(edge.target_node_id)
    descendants: set[str] = set()
    pending = list(successors[failed.node_id])
    while pending:
        node_id = pending.pop()
        if node_id not in descendants:
            descendants.add(node_id)
            pending.extend(successors[node_id])
    unstarted = set(plan.schedule) - set(completed) - {failed.node_id}
    blocked = descendants & unstarted
    return DispatchResult(
        attempted_node_ids=(*completed, failed.node_id),
        completed_node_ids=tuple(completed),
        failed_node_id=failed.node_id,
        blocked_node_ids=tuple(sorted(blocked)),
        unrelated_unstarted_node_ids=tuple(sorted(unstarted - blocked)),
        stop_reason=StopReason(
            "execution", code, failed.node_id, failed.operation_key, technical_type
        ),
        port_results=results,
    )


def dispatch(plan: ExecutionPlan, table: RuntimeTable) -> DispatchResult:
    """Preflight all handlers, then run each scheduled node at most once."""

    handlers = _handlers(plan, table)
    nodes = {node.node_id: node for node in plan.representation.nodes}
    outgoing: dict[str, set[str]] = {node_id: set() for node_id in nodes}
    for edge in plan.representation.edges:
        outgoing[edge.source_node_id].add(edge.source_port_key)
    results: dict[tuple[str, str], object] = {}
    completed: list[str] = []
    for node_id in plan.schedule:
        node = nodes[node_id]
        incoming = tuple(
            IncomingValue(
                edge.edge_id,
                edge.source_node_id,
                edge.source_port_key,
                edge.target_node_id,
                edge.target_port_key,
                results[(edge.source_node_id, edge.source_port_key)],
            )
            for edge in plan.incoming_edges[node_id]
        )
        try:
            output = handlers[(node.operation_key, node.binding_revision)](
                node.parameters, incoming
            )
        except Exception as error:  # noqa: BLE001 - handlers are the failure boundary
            return _failure(
                plan, completed, node, "handler-failed", results, type(error).__name__
            )
        try:
            if not isinstance(output, Mapping):
                raise TypeError("handler output is not a mapping")
            staged = dict(output.items())
            if not all(isinstance(key, str) and key for key in staged):
                raise TypeError("handler output keys must be non-empty text")
        except Exception as error:  # noqa: BLE001 - output mappings are untrusted
            return _failure(
                plan,
                completed,
                node,
                "invalid-handler-output",
                results,
                type(error).__name__,
            )
        if any(port not in staged for port in outgoing[node_id]):
            return _failure(plan, completed, node, "missing-output", results)
        for port, value in staged.items():
            results[(node_id, port)] = value
        completed.append(node_id)
    return DispatchResult(
        attempted_node_ids=tuple(completed),
        completed_node_ids=tuple(completed),
        failed_node_id=None,
        blocked_node_ids=(),
        unrelated_unstarted_node_ids=(),
        stop_reason=None,
        port_results=results,
    )
