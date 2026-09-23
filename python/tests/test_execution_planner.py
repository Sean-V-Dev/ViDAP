"""Focused challenges for validated, deterministic dependency planning."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from types import MappingProxyType

import pytest

from vidap_execution import (
    BindingMap,
    PreparationFailure,
    StaticBinding,
    plan_execution,
    prepare_execution,
)
from vidap_execution.planner import (
    PLAN_REVISION,
    RUNTIME_TABLE_REVISION,
    PlanningFailure,
    _plan_representation,
)
from vidap_execution.representation import ExecutionEdge
from vidap_workflow import (
    DisplayMetadata,
    Edge,
    Endpoint,
    LayoutMetadata,
    NodeDefinition,
    NodeRegistry,
    ParameterDefinition,
    PortDefinition,
    Position,
    Viewport,
    WorkflowDocument,
    WorkflowNode,
    validate_workflow,
)


def _id(number: int) -> str:
    return f"{number:08d}-0000-4000-8000-000000000000"


def _inputs(reverse: bool = False) -> tuple[NodeRegistry, BindingMap]:
    definitions = tuple(
        NodeDefinition(
            type_id=f"test.n{number}",
            display=DisplayMetadata(label=f"Node {number}"),
            inputs=(
                PortDefinition(
                    "in",
                    "input",
                    "table",
                    DisplayMetadata(label="Input"),
                    cardinality="many",
                    required=False,
                ),
            ),
            outputs=(
                PortDefinition(
                    "out", "output", "table", DisplayMetadata(label="Output")
                ),
            ),
            parameters=(
                ParameterDefinition(
                    "value",
                    "integer",
                    False,
                    DisplayMetadata(label="Value"),
                    default=number,
                ),
            ),
            operation_key=f"test.op{number}",
        )
        for number in range(1, 5)
    )
    bindings = tuple(StaticBinding(f"test.op{number}", "r1") for number in range(1, 5))
    return (
        NodeRegistry(tuple(reversed(definitions)) if reverse else definitions),
        BindingMap("r1", tuple(reversed(bindings)) if reverse else bindings),
    )


def _document(
    numbers: tuple[int, ...],
    connections: tuple[tuple[int, int], ...],
    *,
    reverse: bool = False,
    display: bool = False,
) -> WorkflowDocument:
    nodes = tuple(
        WorkflowNode(
            _id(number), f"test.n{number}", label="Changed" if display else None
        )
        for number in numbers
    )
    edges = tuple(
        Edge(
            _id(100 + index), Endpoint(_id(source), "out"), Endpoint(_id(target), "in")
        )
        for index, (source, target) in enumerate(connections)
    )
    layout = (
        LayoutMetadata({_id(numbers[0]): Position(80, 20)}, Viewport(5, -4, 2))
        if display and numbers
        else None
    )
    return WorkflowDocument(
        _id(900),
        nodes=tuple(reversed(nodes)) if reverse else nodes,
        edges=tuple(reversed(edges)) if reverse else edges,
        layout=layout,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("numbers", "connections", "expected"),
    [
        ((), (), ()),
        ((1, 2, 3), ((1, 2), (2, 3)), (1, 2, 3)),
        ((1, 2, 3), (), (1, 2, 3)),
        ((1, 2, 3), ((1, 2), (1, 3)), (1, 2, 3)),
        ((1, 2, 3, 4), ((1, 3), (2, 3), (3, 4)), (1, 2, 3, 4)),
        ((1, 2, 3, 4), ((2, 1), (1, 3)), (2, 1, 3, 4)),
    ],
)
def test_sorted_kahn_and_immutable_references(
    numbers: tuple[int, ...],
    connections: tuple[tuple[int, int], ...],
    expected: tuple[int, ...],
) -> None:
    registry, bindings = _inputs()
    plan = plan_execution(_document(numbers, connections), registry, bindings)
    assert plan.revision == PLAN_REVISION
    assert plan.runtime_table_revision == RUNTIME_TABLE_REVISION
    assert plan.schedule == tuple(_id(number) for number in expected)
    assert isinstance(plan.dependencies, MappingProxyType)
    assert isinstance(plan.incoming_edges, MappingProxyType)
    assert plan.representation.semantic_digest
    assert plan.representation.contract_snapshot_ref
    assert plan.representation.binding_revision == "r1"
    with pytest.raises(FrozenInstanceError):
        plan.revision = "changed"  # type: ignore[misc]
    with pytest.raises(TypeError):
        plan.dependencies[_id(1)] = ()  # type: ignore[index]


@pytest.mark.unit
def test_reverse_construction_and_display_leave_plan_unchanged() -> None:
    connections = ((1, 3), (2, 3), (3, 4))
    first_registry, first_bindings = _inputs()
    reverse_registry, reverse_bindings = _inputs(reverse=True)
    first = plan_execution(
        _document((1, 2, 3, 4), connections), first_registry, first_bindings
    )
    second = plan_execution(
        _document((1, 2, 3, 4), connections, reverse=True, display=True),
        reverse_registry,
        reverse_bindings,
    )
    assert first == second
    assert first.representation.semantic_digest == second.representation.semantic_digest
    assert (
        first.representation.contract_snapshot_ref
        == second.representation.contract_snapshot_ref
    )
    assert first.dependencies[_id(3)] == (_id(1), _id(2))
    assert tuple(edge.source_node_id for edge in first.incoming_edges[_id(3)]) == (
        _id(1),
        _id(2),
    )


@pytest.mark.unit
def test_preparation_refusals_are_preserved_before_planning() -> None:
    registry, bindings = _inputs()
    document = _document((1, 2), ((1, 2),))
    invalid = replace(document, nodes=(*document.nodes, document.nodes[0]))
    expected = validate_workflow(invalid, registry)
    assert expected
    with pytest.raises(PreparationFailure) as caught:
        plan_execution(invalid, registry, bindings)
    assert caught.value.code == "invalid-workflow"
    assert caught.value.diagnostics == expected
    with pytest.raises(PreparationFailure) as unbound:
        plan_execution(document, registry, BindingMap("r1"))
    assert unbound.value.code == "unbound-operation"


@pytest.mark.unit
def test_validated_entry_calls_accepted_preparation_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from vidap_execution import planner

    registry, bindings = _inputs()
    document = _document((1, 2), ((1, 2),))
    original = planner.prepare_execution
    calls = 0

    def counted(*args: object):
        nonlocal calls
        calls += 1
        return original(*args)  # type: ignore[arg-type]

    monkeypatch.setattr(planner, "prepare_execution", counted)
    plan = plan_execution(document, registry, bindings)
    assert calls == 1
    assert plan.representation == original(document, registry, bindings)


@pytest.mark.unit
def test_directly_challenged_graph_structure_refuses() -> None:
    registry, bindings = _inputs()
    prepared = prepare_execution(_document((1, 2), ((1, 2),)), registry, bindings)
    original = prepared.edges[0]
    variants = (
        (replace(original, target_node_id=_id(99)), "dangling-edge"),
        (replace(original, edge_id=_id(101)), "duplicate-edge"),
        (replace(original, target_node_id=_id(1)), "self-dependency"),
        (ExecutionEdge(_id(102), _id(2), "out", _id(1), "in"), "cycle"),
    )
    for extra, code in variants:
        edges = (original, extra) if code in ("duplicate-edge", "cycle") else (extra,)
        with pytest.raises(PlanningFailure) as caught:
            _plan_representation(replace(prepared, edges=edges))
        assert caught.value.code == code
