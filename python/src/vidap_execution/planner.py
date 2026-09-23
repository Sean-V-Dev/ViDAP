"""Deterministic dependency planning over the validated execution representation."""

from __future__ import annotations

import heapq
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.vidap_workflow import NodeRegistry, WorkflowDocument
else:
    from vidap_workflow import NodeRegistry, WorkflowDocument

from .bindings import BindingMap
from .representation import ExecutionEdge, ExecutionRepresentation, prepare_execution

PLAN_REVISION = "vidap.execution-plan/1.0"
RUNTIME_TABLE_REVISION = "vidap.runtime-table/1.0"


class PlanningFailure(ValueError):
    """A malformed dependency graph in a directly challenged representation."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ExecutionPlan:
    """A fixed schedule and immutable dependency references, without run state."""

    revision: str
    runtime_table_revision: str
    representation: ExecutionRepresentation
    schedule: tuple[str, ...]
    dependencies: Mapping[str, tuple[str, ...]]
    incoming_edges: Mapping[str, tuple[ExecutionEdge, ...]]

    def __post_init__(self) -> None:
        if self.revision != PLAN_REVISION:
            raise ValueError("unsupported plan revision")
        if self.runtime_table_revision != RUNTIME_TABLE_REVISION:
            raise ValueError("unsupported runtime table revision")
        object.__setattr__(self, "schedule", tuple(self.schedule))
        object.__setattr__(
            self,
            "dependencies",
            MappingProxyType(
                {key: tuple(value) for key, value in self.dependencies.items()}
            ),
        )
        object.__setattr__(
            self,
            "incoming_edges",
            MappingProxyType(
                {key: tuple(value) for key, value in self.incoming_edges.items()}
            ),
        )


def _edge_order(edge: ExecutionEdge) -> tuple[str, str, str, str]:
    return (
        edge.target_port_key,
        edge.source_node_id,
        edge.source_port_key,
        edge.edge_id,
    )


def _plan_representation(representation: ExecutionRepresentation) -> ExecutionPlan:
    """Defensively check graph structure; Phase 1 owns port-contract validation."""

    if not isinstance(representation, ExecutionRepresentation):
        raise TypeError("planning requires an ExecutionRepresentation")
    node_ids = {node.node_id for node in representation.nodes}
    dependencies: dict[str, set[str]] = {node_id: set() for node_id in node_ids}
    successors: dict[str, set[str]] = {node_id: set() for node_id in node_ids}
    incoming: dict[str, list[ExecutionEdge]] = {node_id: [] for node_id in node_ids}
    endpoints: set[tuple[str, str, str, str]] = set()
    for edge in representation.edges:
        source = edge.source_node_id
        target = edge.target_node_id
        if source not in node_ids or target not in node_ids:
            raise PlanningFailure("dangling-edge")
        exact = (source, edge.source_port_key, target, edge.target_port_key)
        if exact in endpoints:
            raise PlanningFailure("duplicate-edge")
        endpoints.add(exact)
        if source == target:
            raise PlanningFailure("self-dependency")
        dependencies[target].add(source)
        successors[source].add(target)
        incoming[target].append(edge)

    remaining = {node_id: len(parents) for node_id, parents in dependencies.items()}
    ready = [node_id for node_id, count in remaining.items() if count == 0]
    heapq.heapify(ready)
    schedule: list[str] = []
    while ready:
        node_id = heapq.heappop(ready)
        schedule.append(node_id)
        for successor in successors[node_id]:
            remaining[successor] -= 1
            if remaining[successor] == 0:
                heapq.heappush(ready, successor)
    if len(schedule) != len(node_ids):
        raise PlanningFailure("cycle")
    return ExecutionPlan(
        revision=PLAN_REVISION,
        runtime_table_revision=RUNTIME_TABLE_REVISION,
        representation=representation,
        schedule=tuple(schedule),
        dependencies={
            node_id: tuple(sorted(dependencies[node_id]))
            for node_id in sorted(node_ids)
        },
        incoming_edges={
            node_id: tuple(sorted(incoming[node_id], key=_edge_order))
            for node_id in sorted(node_ids)
        },
    )


def plan_execution(
    document: WorkflowDocument, registry: NodeRegistry, bindings: BindingMap
) -> ExecutionPlan:
    """Prepare exactly once, preserving its original pre-dispatch refusals."""

    return _plan_representation(prepare_execution(document, registry, bindings))
