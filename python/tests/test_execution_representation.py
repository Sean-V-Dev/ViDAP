"""Only test-local declarative contracts prove the preparation bridge."""

from __future__ import annotations

import hashlib
import json
from dataclasses import FrozenInstanceError, replace
from types import MappingProxyType

import pytest

from vidap_execution import (
    BindingMap,
    PreparationFailure,
    StaticBinding,
    prepare_execution,
    semantic_projection,
)
from vidap_workflow import (
    BUILTIN_NODE_REGISTRY,
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
    deserialize_document,
    validate_workflow,
)

WORKFLOW = "11111111-1111-4111-8111-111111111111"
OTHER_WORKFLOW = "99999999-9999-4999-8999-999999999999"
SOURCE_A = "22222222-2222-4222-8222-222222222222"
SOURCE_B = "33333333-3333-4333-8333-333333333333"
SINK = "44444444-4444-4444-8444-444444444444"
EDGE_A = "55555555-5555-4555-8555-555555555555"
EDGE_B = "66666666-6666-4666-8666-666666666666"


def _registry(
    *, source_key: str | None = "test.source", default: int = 1
) -> NodeRegistry:
    source = NodeDefinition(
        type_id="test.source",
        display=DisplayMetadata(label="Source"),
        outputs=(
            PortDefinition(
                key="out",
                direction="output",
                nominal_type="table",
                display=DisplayMetadata(label="Output"),
            ),
        ),
        parameters=(
            ParameterDefinition(
                key="count",
                value_kind="integer",
                required=False,
                display=DisplayMetadata(label="Count"),
                default=default,
            ),
            ParameterDefinition(
                key="options",
                value_kind="object",
                required=False,
                display=DisplayMetadata(label="Options"),
            ),
        ),
        operation_key=source_key,
    )
    alternate = replace(
        source, type_id="test.alternate", operation_key="test.alternate"
    )
    sink = NodeDefinition(
        type_id="test.sink",
        display=DisplayMetadata(label="Sink"),
        inputs=(
            PortDefinition(
                key="in",
                direction="input",
                nominal_type="table",
                display=DisplayMetadata(label="Input"),
                cardinality="many",
                required=True,
            ),
        ),
        operation_key="test.sink",
    )
    return NodeRegistry((sink, alternate, source))


def _bindings(revision: str = "r1") -> BindingMap:
    return BindingMap(
        revision,
        (
            StaticBinding("test.sink", revision),
            StaticBinding("test.alternate", revision),
            StaticBinding("test.source", revision),
        ),
    )


def _replace_type(
    registry: NodeRegistry, type_id: str, definition: NodeDefinition
) -> NodeRegistry:
    return NodeRegistry(
        tuple(
            definition if existing.type_id == type_id else existing
            for existing in registry.definitions
        )
    )


def _document(
    *,
    label: str = "A",
    options: dict[str, object] | None = None,
    reverse: bool = False,
    layout: LayoutMetadata | None = None,
) -> WorkflowDocument:
    nodes = (
        WorkflowNode(SOURCE_A, "test.source", label=label, parameters=options or {}),
        WorkflowNode(SOURCE_B, "test.source"),
        WorkflowNode(SINK, "test.sink"),
    )
    edges = (
        Edge(EDGE_A, Endpoint(SOURCE_A, "out"), Endpoint(SINK, "in")),
        Edge(EDGE_B, Endpoint(SOURCE_B, "out"), Endpoint(SINK, "in")),
    )
    return WorkflowDocument(
        WORKFLOW,
        nodes=tuple(reversed(nodes)) if reverse else nodes,
        edges=tuple(reversed(edges)) if reverse else edges,
        layout=layout,
    )


@pytest.mark.unit
def test_preparation_is_frozen_and_uses_resolved_defaults() -> None:
    original: dict[str, object] = {"options": {"levels": [1], "flag": True}}
    document = _document(options=original)
    prepared = prepare_execution(document, _registry(), _bindings())
    original["options"]["levels"].append(2)  # type: ignore[index,union-attr]
    assert prepared.format == "vidap.workflow"
    assert prepared.schema_version == "1.0"
    assert prepared.workflow_id == WORKFLOW
    assert len(prepared.contract_snapshot_ref) == 64
    assert [node.node_id for node in prepared.nodes] == sorted(
        (SOURCE_A, SOURCE_B, SINK)
    )
    assert [edge.edge_id for edge in prepared.edges] == sorted((EDGE_A, EDGE_B))
    assert prepared.nodes[0].parameters["count"] == 1
    assert prepared.nodes[0].parameters["options"]["levels"] == (1,)  # type: ignore[index]
    assert isinstance(prepared.nodes[0].parameters, MappingProxyType)
    with pytest.raises(FrozenInstanceError):
        prepared.binding_revision = "r2"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        prepared.contract_snapshot_ref = "0" * 64  # type: ignore[misc]
    with pytest.raises(TypeError):
        prepared.nodes[0].parameters["count"] = 2  # type: ignore[index]
    with pytest.raises(TypeError):
        prepared.nodes[0].parameters["options"]["levels"] = (2,)  # type: ignore[index]


@pytest.mark.unit
def test_projection_is_order_and_display_independent() -> None:
    layout = LayoutMetadata({SOURCE_A: Position(10, 20)}, Viewport(50, -30, 2))
    a = _document()
    b = _document(label="Changed", reverse=True, layout=layout)
    first = prepare_execution(a, _registry(), _bindings())
    second = prepare_execution(b, _registry(), _bindings())
    assert first == second
    assert first.contract_snapshot_ref == second.contract_snapshot_ref
    assert semantic_projection(a, _registry()) == semantic_projection(b, _registry())
    projection = semantic_projection(a, _registry())
    assert "layout" not in projection
    assert "label" not in projection["nodes"][0]  # type: ignore[index]
    encoded = json.dumps(
        projection, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    assert first.semantic_digest == hashlib.sha256(encoded).hexdigest()
    # JSON member order is immaterial at the canonical document boundary.
    data = b.full_data()
    reversed_members = dict(reversed(tuple(data.items())))
    decoded = deserialize_document(json.dumps(reversed_members))
    assert prepare_execution(decoded, _registry(), _bindings()) == first


@pytest.mark.unit
def test_digest_uses_rfc_8785_property_order_for_non_ascii_names() -> None:
    first = _document(options={"options": {"\ue000": 1, "😀": 2}})
    second = _document(options={"options": {"😀": 2, "\ue000": 1}}, reverse=True)
    projection = semantic_projection(first, _registry())
    prepared = prepare_execution(first, _registry(), _bindings())
    assert (
        prepare_execution(second, _registry(), _bindings()).semantic_digest
        == prepared.semantic_digest
    )
    assert list(projection["nodes"][0]["parameters"]["options"]) == ["😀", "\ue000"]  # type: ignore[index]
    # The independent expected object places the supplementary character before
    # the private-use BMP character, the opposite of Python code-point order.
    expected = {
        "edges": projection["edges"],
        "format": "vidap.workflow",
        "nodes": [
            {
                "id": SOURCE_A,
                "parameters": {"count": 1, "options": {"😀": 2, "\ue000": 1}},
                "type": "test.source",
            },
            {"id": SOURCE_B, "parameters": {"count": 1}, "type": "test.source"},
            {"id": SINK, "parameters": {}, "type": "test.sink"},
        ],
        "schemaVersion": "1.0",
        "workflowId": WORKFLOW,
    }
    encoded = json.dumps(expected, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    assert prepared.semantic_digest == hashlib.sha256(encoded).hexdigest()
    wrong_order = json.dumps(
        expected, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    assert (
        prepared.semantic_digest
        != hashlib.sha256(wrong_order.encode("utf-8")).hexdigest()
    )


@pytest.mark.unit
def test_semantic_changes_affect_digest_and_binding_changes_affect_handoff() -> None:
    baseline = _document()
    registry = _registry()
    bindings = _bindings()
    initial = prepare_execution(baseline, registry, bindings)
    variants = (
        replace(baseline, workflow_id=OTHER_WORKFLOW),
        replace(
            baseline,
            nodes=(
                replace(baseline.nodes[0], type_id="test.alternate"),
                *baseline.nodes[1:],
            ),
        ),
        replace(
            baseline,
            nodes=(
                replace(baseline.nodes[0], parameters={"count": 3}),
                *baseline.nodes[1:],
            ),
        ),
        replace(
            baseline,
            edges=(
                replace(baseline.edges[0], source=Endpoint(SOURCE_B, "out")),
                baseline.edges[1],
            ),
        ),
        replace(
            baseline,
            edges=(replace(baseline.edges[0], id=OTHER_WORKFLOW), baseline.edges[1]),
        ),
    )
    for variant in variants:
        # A duplicate exact endpoint is invalid and must refuse instead of hashing.
        if validate_workflow(variant, registry):
            with pytest.raises(PreparationFailure):
                prepare_execution(variant, registry, bindings)
        else:
            assert (
                prepare_execution(variant, registry, bindings).semantic_digest
                != initial.semantic_digest
            )
    assert (
        prepare_execution(baseline, _registry(default=2), bindings).semantic_digest
        != initial.semantic_digest
    )
    new_key = _registry(source_key="test.changed")
    changed_key_bindings = BindingMap(
        "r1", (*bindings.bindings, StaticBinding("test.changed", "r1"))
    )
    changed_key = prepare_execution(baseline, new_key, changed_key_bindings)
    assert changed_key != initial
    assert changed_key.semantic_digest == initial.semantic_digest
    assert changed_key.contract_snapshot_ref != initial.contract_snapshot_ref
    changed_revision = prepare_execution(baseline, registry, _bindings("r2"))
    assert changed_revision != initial
    assert changed_revision.semantic_digest == initial.semantic_digest
    assert changed_revision.contract_snapshot_ref == initial.contract_snapshot_ref


@pytest.mark.unit
def test_snapshot_is_used_contract_fingerprint_not_workflow_digest() -> None:
    document = WorkflowDocument(
        WORKFLOW, nodes=(WorkflowNode(SOURCE_A, "test.source"),)
    )
    registry = _registry()
    baseline = prepare_execution(document, registry, _bindings())
    source = registry.get("test.source")
    assert source is not None
    changed_source = replace(
        source,
        outputs=(replace(source.outputs[0], nominal_type="target"),),
    )
    changed_registry = _replace_type(registry, source.type_id, changed_source)
    assert validate_workflow(document, changed_registry) == ()
    changed = prepare_execution(document, changed_registry, _bindings())
    assert changed.semantic_digest == baseline.semantic_digest
    assert changed.contract_snapshot_ref != baseline.contract_snapshot_ref
    assert changed != baseline


@pytest.mark.unit
def test_snapshot_covers_ports_parameters_defaults_and_constraints() -> None:
    full = _document()
    document = replace(
        full,
        nodes=(full.nodes[0], full.nodes[2]),
        edges=(full.edges[0],),
    )
    registry = _registry()
    initial = prepare_execution(document, registry, _bindings())
    source = registry.get("test.source")
    sink = registry.get("test.sink")
    assert source is not None and sink is not None
    input_port = sink.inputs[0]
    for changed_input in (
        replace(input_port, cardinality="one"),
        replace(input_port, required=False),
    ):
        changed = _replace_type(
            registry, sink.type_id, replace(sink, inputs=(changed_input,))
        )
        assert validate_workflow(document, changed) == ()
        prepared = prepare_execution(document, changed, _bindings())
        assert prepared.semantic_digest == initial.semantic_digest
        assert prepared.contract_snapshot_ref != initial.contract_snapshot_ref
    count = source.parameters[0]
    for changed_count in (
        replace(count, value_kind="number"),
        replace(count, default=2),
        replace(count, constraints={"minimum": 0}),
    ):
        changed = _replace_type(
            registry,
            source.type_id,
            replace(source, parameters=(changed_count, source.parameters[1])),
        )
        assert validate_workflow(document, changed) == ()
        assert (
            prepare_execution(document, changed, _bindings()).contract_snapshot_ref
            != initial.contract_snapshot_ref
        )
    options = source.parameters[1]
    absent = replace(options, constraints={"nullable": True})
    explicit_null = replace(absent, default=None)
    omitted_registry = _replace_type(
        registry, source.type_id, replace(source, parameters=(count, absent))
    )
    null_registry = _replace_type(
        registry, source.type_id, replace(source, parameters=(count, explicit_null))
    )
    assert validate_workflow(document, omitted_registry) == ()
    assert validate_workflow(document, null_registry) == ()
    assert (
        prepare_execution(document, omitted_registry, _bindings()).contract_snapshot_ref
        != prepare_execution(document, null_registry, _bindings()).contract_snapshot_ref
    )
    forward_values = replace(
        options, constraints={"allowedValues": ({"x": 1}, {"x": 2})}
    )
    reverse_values = replace(
        options, constraints={"allowedValues": ({"x": 2}, {"x": 1})}
    )
    forward_registry = _replace_type(
        registry, source.type_id, replace(source, parameters=(count, forward_values))
    )
    reverse_registry = _replace_type(
        registry, source.type_id, replace(source, parameters=(count, reverse_values))
    )
    assert validate_workflow(document, forward_registry) == ()
    assert validate_workflow(document, reverse_registry) == ()
    forward = prepare_execution(document, forward_registry, _bindings())
    reverse = prepare_execution(document, reverse_registry, _bindings())
    assert forward.semantic_digest == reverse.semantic_digest
    assert forward.contract_snapshot_ref != reverse.contract_snapshot_ref


@pytest.mark.unit
def test_snapshot_excludes_display_registry_order_and_unused_types() -> None:
    document = _document()
    registry = _registry()
    initial = prepare_execution(document, registry, _bindings())
    source = registry.get("test.source")
    alternate = registry.get("test.alternate")
    assert source is not None and alternate is not None
    displayed = replace(
        source,
        display=DisplayMetadata(label="Changed", description="Visible only"),
        outputs=(replace(source.outputs[0], display=DisplayMetadata(label="Renamed")),),
        parameters=(
            replace(source.parameters[0], display=DisplayMetadata(label="Changed")),
            source.parameters[1],
        ),
    )
    display_registry = _replace_type(registry, source.type_id, displayed)
    assert prepare_execution(document, display_registry, _bindings()) == initial
    unused = _replace_type(
        registry, alternate.type_id, replace(alternate, operation_key="test.unused")
    )
    assert prepare_execution(document, unused, _bindings()) == initial
    assert (
        prepare_execution(
            document, NodeRegistry(tuple(reversed(registry.definitions))), _bindings()
        )
        == initial
    )
    other_output = replace(source.outputs[0], key="other", nominal_type="target")
    expanded_source = replace(source, outputs=(source.outputs[0], other_output))
    forward = _replace_type(registry, source.type_id, expanded_source)
    reversed_declarations = _replace_type(
        registry,
        source.type_id,
        replace(
            expanded_source,
            outputs=tuple(reversed(expanded_source.outputs)),
            parameters=tuple(reversed(expanded_source.parameters)),
        ),
    )
    assert prepare_execution(document, forward, _bindings()) == prepare_execution(
        document, reversed_declarations, _bindings()
    )


@pytest.mark.unit
def test_snapshot_expected_hash_and_non_ascii_property_order() -> None:
    document = WorkflowDocument(
        WORKFLOW, nodes=(WorkflowNode(SOURCE_A, "test.source"),)
    )
    registry = _registry()
    prepared = prepare_execution(document, registry, _bindings())
    expected = {
        "format": "vidap.workflow",
        "nodeTypes": [
            {
                "inputs": [],
                "operationKey": "test.source",
                "outputs": [
                    {"direction": "output", "key": "out", "nominalType": "table"}
                ],
                "parameters": [
                    {
                        "constraints": {},
                        "default": 1,
                        "defaultPresent": True,
                        "key": "count",
                        "required": False,
                        "valueKind": "integer",
                    },
                    {
                        "constraints": {},
                        "defaultPresent": False,
                        "key": "options",
                        "required": False,
                        "valueKind": "object",
                    },
                ],
                "typeId": "test.source",
            }
        ],
        "schemaVersion": "1.0",
        "validationPolicy": "vidap.workflow-validation/1.0",
    }
    encoded = json.dumps(expected, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )
    assert prepared.contract_snapshot_ref == hashlib.sha256(encoded).hexdigest()
    source = registry.get("test.source")
    assert source is not None
    nested_default = {"\ue000": 1, "😀": 2}
    options = replace(source.parameters[1], default=nested_default)
    changed_registry = _replace_type(
        registry,
        source.type_id,
        replace(source, parameters=(source.parameters[0], options)),
    )
    nested_default["😀"] = 99
    changed = prepare_execution(document, changed_registry, _bindings())
    expected["nodeTypes"][0]["parameters"][1] = {  # type: ignore[index]
        "constraints": {},
        "default": {"😀": 2, "\ue000": 1},
        "defaultPresent": True,
        "key": "options",
        "required": False,
        "valueKind": "object",
    }
    encoded_non_ascii = json.dumps(
        expected, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    assert (
        changed.contract_snapshot_ref == hashlib.sha256(encoded_non_ascii).hexdigest()
    )
    wrong_order = json.dumps(
        expected, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    assert changed.contract_snapshot_ref != hashlib.sha256(wrong_order).hexdigest()


@pytest.mark.unit
def test_phase_one_diagnostics_precede_binding_refusal() -> None:
    valid = _document()
    invalid = replace(valid, nodes=(*valid.nodes, valid.nodes[0]))
    expected = validate_workflow(invalid, _registry())
    assert expected
    with pytest.raises(PreparationFailure) as caught:
        prepare_execution(invalid, _registry(), BindingMap("r1"))
    assert caught.value.code == "invalid-workflow"
    assert caught.value.diagnostics == expected
    assert caught.value.diagnostics[0].code == "VIDAP-DUPLICATE-NODE-ID"


@pytest.mark.unit
def test_missing_unbound_duplicate_and_mismatched_bindings_refuse() -> None:
    with pytest.raises(PreparationFailure, match="no operation key") as missing:
        prepare_execution(_document(), _registry(source_key=None), _bindings())
    assert missing.value.code == "missing-operation-key"
    with pytest.raises(PreparationFailure) as unbound:
        prepare_execution(_document(), _registry(), BindingMap("r1"))
    assert unbound.value.code == "unbound-operation"
    with pytest.raises(ValueError, match="duplicate operation binding"):
        BindingMap(
            "r1",
            (StaticBinding("test.source", "r1"), StaticBinding("test.source", "r1")),
        )
    mismatched = BindingMap(
        "r1", (StaticBinding("test.source", "r2"), StaticBinding("test.sink", "r1"))
    )
    with pytest.raises(PreparationFailure) as mismatch:
        prepare_execution(_document(), _registry(), mismatched)
    assert mismatch.value.code == "binding-revision-mismatch"
    with pytest.raises(PreparationFailure) as builtin:
        prepare_execution(
            WorkflowDocument(
                WORKFLOW,
                nodes=(WorkflowNode(SOURCE_A, "vidap.kernel.contract-source"),),
            ),
            BUILTIN_NODE_REGISTRY,
            _bindings(),
        )
    assert builtin.value.code == "missing-operation-key"


@pytest.mark.unit
def test_binding_metadata_is_static_and_immutable() -> None:
    source = [StaticBinding("test.source", "r1")]
    bindings = BindingMap("r1", source)  # type: ignore[arg-type]
    source.clear()
    assert bindings.get("test.source") == StaticBinding("test.source", "r1")
    assert bindings.get("unknown") is None
    with pytest.raises(FrozenInstanceError):
        bindings.revision = "r2"  # type: ignore[misc]
    with pytest.raises(TypeError):
        bindings._by_key["other"] = StaticBinding("other", "r1")  # type: ignore[index]
    for forbidden in ("https://example.com", "pkg/module", "x;run", "  "):
        with pytest.raises(ValueError):
            StaticBinding(forbidden, "r1")
