"""Synthetic, non-operational evidence for workflow validation diagnostics."""

from __future__ import annotations

import builtins
import importlib
import sys
from dataclasses import FrozenInstanceError

import pytest

from vidap_workflow import (
    Diagnostic,
    DisplayMetadata,
    Edge,
    Endpoint,
    LayoutMetadata,
    NodeDefinition,
    NodeRegistry,
    ParameterDefinition,
    PortDefinition,
    Position,
    WorkflowDocument,
    WorkflowNode,
    validate_workflow,
)
from vidap_workflow.contracts import PARAMETER_CONSTRAINT_KEYS
from vidap_workflow.diagnostics import (
    DANGLING_NODE,
    DIRECTED_CYCLE,
    DUPLICATE_EDGE_ID,
    DUPLICATE_EXACT_EDGE,
    DUPLICATE_NODE_ID,
    INPUT_CARDINALITY_EXCEEDED,
    MISSING_REQUIRED_INPUT,
    MISSING_REQUIRED_PARAMETER,
    NOMINAL_TYPE_MISMATCH,
    PARAMETER_CONSTRAINT_VIOLATION,
    PARAMETER_KIND_MISMATCH,
    REVERSED_DIRECTION,
    UNKNOWN_NODE_TYPE,
    UNKNOWN_PARAMETER,
    UNKNOWN_PORT,
    UNSUPPORTED_PARAMETER_CONSTRAINT,
)

SOURCE_ID = "11111111-1111-4111-8111-111111111111"
MIDDLE_ID = "22222222-2222-4222-8222-222222222222"
SINK_ID = "33333333-3333-4333-8333-333333333333"
OTHER_ID = "44444444-4444-4444-8444-444444444444"
EDGE_ONE = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
EDGE_TWO = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
EDGE_THREE = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
WORKFLOW_ID = "dddddddd-dddd-4ddd-8ddd-dddddddddddd"


def _input(key: str, kind: str = "table", *, required: bool = True) -> PortDefinition:
    return PortDefinition(
        key=key,
        direction="input",
        nominal_type=kind,
        display=DisplayMetadata(label=key),
        cardinality="one",
        required=required,
    )


def _output(key: str, kind: str = "table") -> PortDefinition:
    return PortDefinition(
        key=key,
        direction="output",
        nominal_type=kind,
        display=DisplayMetadata(label=key),
    )


def _registry(*, sink_parameter: ParameterDefinition | None = None) -> NodeRegistry:
    source = NodeDefinition(
        type_id="synthetic.source",
        display=DisplayMetadata(label="Source"),
        outputs=(_output("out"),),
    )
    middle = NodeDefinition(
        type_id="synthetic.middle",
        display=DisplayMetadata(label="Middle"),
        inputs=(_input("in"),),
        outputs=(_output("out"),),
    )
    sink = NodeDefinition(
        type_id="synthetic.sink",
        display=DisplayMetadata(label="Sink"),
        inputs=(_input("in"),),
        parameters=(() if sink_parameter is None else (sink_parameter,)),
    )
    return NodeRegistry((source, middle, sink))


def _node(
    node_id: str, type_id: str, parameters: dict[str, object] | None = None
) -> WorkflowNode:
    return WorkflowNode(id=node_id, type_id=type_id, parameters=parameters or {})


def _edge(
    edge_id: str, source: str, source_port: str, target: str, target_port: str
) -> Edge:
    return Edge(
        id=edge_id,
        source=Endpoint(node_id=source, port_key=source_port),
        target=Endpoint(node_id=target, port_key=target_port),
    )


def _document(
    nodes: tuple[WorkflowNode, ...], edges: tuple[Edge, ...] = ()
) -> WorkflowDocument:
    return WorkflowDocument(workflow_id=WORKFLOW_ID, nodes=nodes, edges=edges)


def _codes(document: WorkflowDocument, registry: NodeRegistry) -> tuple[str, ...]:
    return tuple(finding.code for finding in validate_workflow(document, registry))


@pytest.mark.unit
def test_valid_source_to_sink_has_no_diagnostics() -> None:
    document = _document(
        (_node(SOURCE_ID, "synthetic.source"), _node(SINK_ID, "synthetic.sink")),
        (_edge(EDGE_ONE, SOURCE_ID, "out", SINK_ID, "in"),),
    )

    assert validate_workflow(document, _registry()) == ()


@pytest.mark.unit
def test_structural_codes_are_actionable_and_stably_ordered() -> None:
    document = _document(
        (
            _node(SOURCE_ID, "synthetic.source"),
            _node(SOURCE_ID, "synthetic.source"),
            _node(SINK_ID, "synthetic.sink"),
        ),
        (
            _edge(EDGE_ONE, SOURCE_ID, "out", SINK_ID, "in"),
            _edge(EDGE_ONE, SOURCE_ID, "out", SINK_ID, "in"),
        ),
    )
    findings = validate_workflow(document, _registry())

    assert {finding.code for finding in findings} >= {
        DUPLICATE_NODE_ID,
        DUPLICATE_EDGE_ID,
        DUPLICATE_EXACT_EDGE,
    }
    assert all(
        finding.severity == "error" and finding.message and finding.remedy
        for finding in findings
    )
    assert tuple(finding.code for finding in findings) == tuple(
        sorted(finding.code for finding in findings)
    )


@pytest.mark.unit
def test_conflicting_duplicate_node_definitions_are_collection_order_invariant() -> (
    None
):
    known = _node(SOURCE_ID, "synthetic.source")
    unknown = _node(SOURCE_ID, "synthetic.unknown")
    ordered = _document((known, unknown))
    reversed_nodes = _document((unknown, known))

    assert validate_workflow(ordered, _registry()) == validate_workflow(
        reversed_nodes, _registry()
    )
    assert _codes(ordered, _registry()) == (DUPLICATE_NODE_ID,)


@pytest.mark.unit
def test_unknown_nodes_and_constraints_are_unsupported() -> None:
    parameter = ParameterDefinition(
        key="choice",
        value_kind="string",
        required=False,
        display=DisplayMetadata(label="Choice"),
        constraints={"notSupported": True},
    )
    document = _document(
        (
            _node(SOURCE_ID, "synthetic.unknown"),
            _node(SINK_ID, "synthetic.sink", {"choice": "x"}),
        )
    )
    findings = validate_workflow(document, _registry(sink_parameter=parameter))

    assert {(finding.code, finding.category) for finding in findings} == {
        (UNKNOWN_NODE_TYPE, "unsupported"),
        (UNSUPPORTED_PARAMETER_CONSTRAINT, "unsupported"),
        (MISSING_REQUIRED_INPUT, "semantic"),
    }


@pytest.mark.unit
@pytest.mark.parametrize(
    ("edge", "expected"),
    (
        (_edge(EDGE_ONE, OTHER_ID, "out", SINK_ID, "in"), DANGLING_NODE),
        (_edge(EDGE_ONE, SOURCE_ID, "missing", SINK_ID, "in"), UNKNOWN_PORT),
        (_edge(EDGE_ONE, SINK_ID, "in", SOURCE_ID, "out"), REVERSED_DIRECTION),
    ),
)
def test_endpoint_failures_are_separate(edge: Edge, expected: str) -> None:
    document = _document(
        (_node(SOURCE_ID, "synthetic.source"), _node(SINK_ID, "synthetic.sink")),
        (edge,),
    )

    assert expected in _codes(document, _registry())


@pytest.mark.unit
def test_type_cardinality_and_required_input_failures_are_separate() -> None:
    mismatch_registry = NodeRegistry(
        (
            NodeDefinition(
                type_id="synthetic.source",
                display=DisplayMetadata(label="Source"),
                outputs=(_output("out", "model"),),
            ),
            NodeDefinition(
                type_id="synthetic.sink",
                display=DisplayMetadata(label="Sink"),
                inputs=(_input("in", "table"),),
            ),
        )
    )
    mismatch = _document(
        (_node(SOURCE_ID, "synthetic.source"), _node(SINK_ID, "synthetic.sink")),
        (_edge(EDGE_ONE, SOURCE_ID, "out", SINK_ID, "in"),),
    )
    cardinality = _document(
        (
            _node(SOURCE_ID, "synthetic.source"),
            _node(MIDDLE_ID, "synthetic.source"),
            _node(SINK_ID, "synthetic.sink"),
        ),
        (
            _edge(EDGE_ONE, SOURCE_ID, "out", SINK_ID, "in"),
            _edge(EDGE_TWO, MIDDLE_ID, "out", SINK_ID, "in"),
        ),
    )

    assert NOMINAL_TYPE_MISMATCH in _codes(mismatch, mismatch_registry)
    assert INPUT_CARDINALITY_EXCEEDED in _codes(cardinality, _registry())
    assert MISSING_REQUIRED_INPUT in _codes(
        _document((_node(SINK_ID, "synthetic.sink"),)), _registry()
    )


@pytest.mark.unit
def test_parameter_presence_kind_default_and_constraint_behavior_is_non_mutating() -> (
    None
):
    required = ParameterDefinition(
        key="name",
        value_kind="string",
        required=True,
        display=DisplayMetadata(label="Name"),
    )
    typed = ParameterDefinition(
        key="count",
        value_kind="integer",
        required=False,
        display=DisplayMetadata(label="Count"),
    )
    defaulted = ParameterDefinition(
        key="mode",
        value_kind="string",
        required=False,
        display=DisplayMetadata(label="Mode"),
        default="bad",
        constraints={"allowedValues": ("good",)},
    )
    constrained = ParameterDefinition(
        key="tags",
        value_kind="array",
        required=False,
        display=DisplayMetadata(label="Tags"),
        constraints={"minItems": 2, "uniqueItems": True},
    )
    definition = NodeDefinition(
        type_id="synthetic.sink",
        display=DisplayMetadata(label="Sink"),
        parameters=(required, typed, defaulted, constrained),
    )
    registry = NodeRegistry((_registry().get("synthetic.source"), definition))
    original = {"count": "one", "unknown": True, "tags": ["x", "x"]}
    document = _document((_node(SINK_ID, "synthetic.sink", original),))
    codes = _codes(document, registry)

    assert {
        MISSING_REQUIRED_PARAMETER,
        UNKNOWN_PARAMETER,
        PARAMETER_KIND_MISMATCH,
        PARAMETER_CONSTRAINT_VIOLATION,
    } <= set(codes)
    assert document.nodes[0].parameters == {
        "count": "one",
        "tags": ("x", "x"),
        "unknown": True,
    }


@pytest.mark.unit
def test_supported_constraint_vocabulary_including_nullable_and_invalid_pattern_metadata() -> (
    None
):
    nullable = ParameterDefinition(
        key="value",
        value_kind="string",
        required=False,
        display=DisplayMetadata(label="Value"),
        constraints={"nullable": True},
    )
    broken_pattern = ParameterDefinition(
        key="pattern",
        value_kind="string",
        required=False,
        display=DisplayMetadata(label="Pattern"),
        constraints={"pattern": "["},
    )
    definition = NodeDefinition(
        type_id="synthetic.sink",
        display=DisplayMetadata(label="Sink"),
        parameters=(nullable, broken_pattern),
    )
    registry = NodeRegistry((_registry().get("synthetic.source"), definition))
    document = _document(
        (_node(SINK_ID, "synthetic.sink", {"value": None, "pattern": "test"}),)
    )

    assert _codes(document, registry) == (UNSUPPORTED_PARAMETER_CONSTRAINT,)


@pytest.mark.unit
def test_each_supported_constraint_has_deterministic_validation_coverage() -> None:
    parameters = (
        ParameterDefinition(
            key="minimum",
            value_kind="number",
            required=False,
            display=DisplayMetadata(label="Minimum"),
            constraints={"minimum": 1},
        ),
        ParameterDefinition(
            key="maximum",
            value_kind="integer",
            required=False,
            display=DisplayMetadata(label="Maximum"),
            constraints={"maximum": 5},
        ),
        ParameterDefinition(
            key="min-length",
            value_kind="string",
            required=False,
            display=DisplayMetadata(label="Minimum length"),
            constraints={"minLength": 2},
        ),
        ParameterDefinition(
            key="max-length",
            value_kind="string",
            required=False,
            display=DisplayMetadata(label="Maximum length"),
            constraints={"maxLength": 2},
        ),
        ParameterDefinition(
            key="pattern",
            value_kind="string",
            required=False,
            display=DisplayMetadata(label="Pattern"),
            constraints={"pattern": "^yes$"},
        ),
        ParameterDefinition(
            key="min-items",
            value_kind="array",
            required=False,
            display=DisplayMetadata(label="Minimum items"),
            constraints={"minItems": 2},
        ),
        ParameterDefinition(
            key="max-items",
            value_kind="array",
            required=False,
            display=DisplayMetadata(label="Maximum items"),
            constraints={"maxItems": 1},
        ),
        ParameterDefinition(
            key="unique-items",
            value_kind="array",
            required=False,
            display=DisplayMetadata(label="Unique items"),
            constraints={"uniqueItems": True},
        ),
        ParameterDefinition(
            key="required-keys",
            value_kind="object",
            required=False,
            display=DisplayMetadata(label="Required keys"),
            constraints={"requiredKeys": ("name",)},
        ),
    )
    registry = NodeRegistry(
        (
            NodeDefinition(
                type_id="synthetic.sink",
                display=DisplayMetadata(label="Sink"),
                parameters=parameters,
            ),
        )
    )
    document = _document(
        (
            _node(
                SINK_ID,
                "synthetic.sink",
                {
                    "minimum": 0,
                    "maximum": 6,
                    "min-length": "x",
                    "max-length": "long",
                    "pattern": "no",
                    "min-items": ["one"],
                    "max-items": ["one", "two"],
                    "unique-items": [{"name": "one"}, {"name": "one"}],
                    "required-keys": {},
                },
            ),
        )
    )

    assert PARAMETER_CONSTRAINT_KEYS == (
        "allowedValues",
        "minimum",
        "maximum",
        "minLength",
        "maxLength",
        "pattern",
        "minItems",
        "maxItems",
        "uniqueItems",
        "requiredKeys",
        "nullable",
    )
    assert _codes(document, registry).count(PARAMETER_CONSTRAINT_VIOLATION) == 9


@pytest.mark.unit
def test_directed_cycle_is_reported_without_an_execution_order_claim() -> None:
    document = _document(
        (_node(SOURCE_ID, "synthetic.middle"), _node(MIDDLE_ID, "synthetic.middle")),
        (
            _edge(EDGE_ONE, SOURCE_ID, "out", MIDDLE_ID, "in"),
            _edge(EDGE_TWO, MIDDLE_ID, "out", SOURCE_ID, "in"),
        ),
    )
    findings = validate_workflow(document, _registry())

    assert DIRECTED_CYCLE in tuple(finding.code for finding in findings)
    assert all("order" not in finding.message.lower() for finding in findings)


@pytest.mark.unit
def test_layout_construction_collection_and_member_order_do_not_change_findings() -> (
    None
):
    nodes = (_node(SOURCE_ID, "synthetic.source"), _node(SINK_ID, "synthetic.sink"))
    edges = (_edge(EDGE_ONE, SOURCE_ID, "out", SINK_ID, "missing"),)
    first = _document(nodes, edges)
    second = WorkflowDocument(
        workflow_id=WORKFLOW_ID,
        nodes=tuple(reversed(nodes)),
        edges=tuple(reversed(edges)),
        layout=LayoutMetadata(node_positions={SOURCE_ID: Position(x=100, y=200)}),
    )

    assert validate_workflow(first, _registry()) == validate_workflow(
        second, _registry()
    )


@pytest.mark.unit
def test_diagnostics_and_results_are_immutable_and_public_import_is_consumer_free(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finding = Diagnostic(
        "VIDAP-EXAMPLE", "error", "semantic", "node", "node", "Message", "Remedy"
    )
    with pytest.raises(FrozenInstanceError):
        finding.code = "VIDAP-CHANGED"  # type: ignore[misc]
    result = validate_workflow(
        _document((_node(SINK_ID, "synthetic.sink"),)), _registry()
    )
    assert isinstance(result, tuple)
    forbidden = {
        "fastapi",
        "uvicorn",
        "vidap_execution",
        "vidap_experiments",
        "vidap_export",
        "socket",
        "subprocess",
        "urllib",
    }
    for module_name in tuple(sys.modules):
        if module_name.split(".")[0] in forbidden | {"vidap_workflow"}:
            monkeypatch.delitem(sys.modules, module_name, raising=False)
    original_import = builtins.__import__

    def guarded_import(
        name: str,
        globals: dict[str, object] | None = None,
        locals: dict[str, object] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> object:
        if name.split(".")[0] in forbidden:
            raise AssertionError(f"workflow import attempted to import {name}")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    imported = importlib.import_module("vidap_workflow")
    assert imported.validate_workflow.__name__ == "validate_workflow"
