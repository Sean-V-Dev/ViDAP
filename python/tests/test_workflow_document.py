import builtins
import importlib
import json
import sys

import pytest

from vidap_workflow import (
    Edge,
    Endpoint,
    LayoutMetadata,
    Position,
    Viewport,
    WorkflowDecodeError,
    WorkflowDocument,
    WorkflowNode,
    deserialize_document,
    serialize_document,
    serialize_semantic_document,
)

WORKFLOW_ID = "00000000-0000-4000-8000-000000000001"
SOURCE_ID = "00000000-0000-4000-8000-000000000002"
LEFT_ID = "00000000-0000-4000-8000-000000000003"
RIGHT_ID = "00000000-0000-4000-8000-000000000004"
LEFT_EDGE_ID = "00000000-0000-4000-8000-000000000005"
RIGHT_EDGE_ID = "00000000-0000-4000-8000-000000000006"


def _branched_document(
    *, reverse_collections: bool = False, reverse_construction: bool = False
) -> WorkflowDocument:
    def make_source() -> WorkflowNode:
        return WorkflowNode(
            id=SOURCE_ID,
            type_id="synthetic.source",
            label="Source",
            parameters={"columns": ["age", "score"], "options": {"sample": True}},
        )

    def make_left() -> WorkflowNode:
        return WorkflowNode(
            id=LEFT_ID,
            type_id="synthetic.left",
            label="Left branch",
            parameters={"threshold": 0.5},
        )

    def make_right() -> WorkflowNode:
        return WorkflowNode(
            id=RIGHT_ID,
            type_id="synthetic.right",
            parameters={"enabled": False},
        )

    def make_left_edge() -> Edge:
        return Edge(
            id=LEFT_EDGE_ID,
            source=Endpoint(node_id=SOURCE_ID, port_key="out"),
            target=Endpoint(node_id=LEFT_ID, port_key="in"),
        )

    def make_right_edge() -> Edge:
        return Edge(
            id=RIGHT_EDGE_ID,
            source=Endpoint(node_id=SOURCE_ID, port_key="out"),
            target=Endpoint(node_id=RIGHT_ID, port_key="in"),
        )

    if reverse_construction:
        right = make_right()
        left = make_left()
        source = make_source()
        right_edge = make_right_edge()
        left_edge = make_left_edge()
    else:
        source = make_source()
        left = make_left()
        right = make_right()
        left_edge = make_left_edge()
        right_edge = make_right_edge()
    nodes = (source, left, right)
    edges = (left_edge, right_edge)
    if reverse_collections:
        nodes = tuple(reversed(nodes))
        edges = tuple(reversed(edges))
    return WorkflowDocument(
        workflow_id=WORKFLOW_ID,
        nodes=nodes,
        edges=edges,
        layout=LayoutMetadata(
            node_positions={
                RIGHT_ID: Position(x=400, y=120),
                SOURCE_ID: Position(x=0, y=0),
                LEFT_ID: Position(x=400, y=0),
            },
            viewport=Viewport(x=10, y=20, zoom=1.25),
        ),
    )


@pytest.mark.unit
def test_minimal_document_round_trips_to_identical_full_json() -> None:
    document = WorkflowDocument(workflow_id=WORKFLOW_ID)

    serialized = serialize_document(document)
    decoded = deserialize_document(serialized)

    assert serialized.endswith("\n")
    assert serialized.encode("utf-8")
    assert json.loads(serialized) == document.full_data()
    assert decoded == document
    assert serialize_document(decoded) == serialized


@pytest.mark.unit
def test_branched_document_round_trip_preserves_semantic_fields() -> None:
    document = _branched_document()

    decoded = deserialize_document(serialize_document(document))

    assert decoded == document
    assert tuple(node.id for node in decoded.nodes) == (SOURCE_ID, LEFT_ID, RIGHT_ID)
    assert decoded.nodes[0].type_id == "synthetic.source"
    assert decoded.nodes[1].label == "Left branch"
    assert decoded.nodes[0].parameters["columns"] == ("age", "score")
    assert tuple(edge.id for edge in decoded.edges) == (LEFT_EDGE_ID, RIGHT_EDGE_ID)
    assert decoded.edges[0].source == Endpoint(node_id=SOURCE_ID, port_key="out")
    assert decoded.edges[1].target == Endpoint(node_id=RIGHT_ID, port_key="in")


@pytest.mark.unit
def test_collection_and_construction_order_do_not_change_canonical_json() -> None:
    ordered = _branched_document()
    reverse_constructed = _branched_document(reverse_construction=True)
    reverse_collections = _branched_document(reverse_collections=True)

    assert ordered == reverse_constructed == reverse_collections
    assert serialize_document(ordered) == serialize_document(reverse_constructed)
    assert serialize_document(ordered) == serialize_document(reverse_collections)
    assert serialize_semantic_document(ordered) == serialize_semantic_document(
        reverse_constructed
    )
    assert serialize_semantic_document(ordered) == serialize_semantic_document(
        reverse_collections
    )


@pytest.mark.unit
def test_layout_is_not_part_of_semantic_equality_or_serialization() -> None:
    semantic_document = WorkflowDocument(
        workflow_id=WORKFLOW_ID,
        nodes=(WorkflowNode(id=SOURCE_ID, type_id="synthetic.source"),),
    )
    laid_out_document = WorkflowDocument(
        workflow_id=WORKFLOW_ID,
        nodes=(WorkflowNode(id=SOURCE_ID, type_id="synthetic.source"),),
        layout=LayoutMetadata(
            node_positions={SOURCE_ID: Position(x=100, y=200)},
            viewport=Viewport(x=1, y=2, zoom=3),
        ),
    )

    assert semantic_document == laid_out_document
    assert serialize_semantic_document(
        semantic_document
    ) == serialize_semantic_document(laid_out_document)
    assert serialize_document(semantic_document) != serialize_document(
        laid_out_document
    )


@pytest.mark.unit
def test_reordered_json_object_members_decode_to_the_same_document() -> None:
    reordered_json = json.dumps(
        {
            "nodes": [
                {
                    "parameters": {"nested": {"value": 1}},
                    "type": "synthetic.source",
                    "id": SOURCE_ID,
                }
            ],
            "edges": [],
            "workflowId": WORKFLOW_ID,
            "format": "vidap.workflow",
            "schemaVersion": "1.0",
        }
    )
    expected = WorkflowDocument(
        workflow_id=WORKFLOW_ID,
        nodes=(
            WorkflowNode(
                id=SOURCE_ID,
                type_id="synthetic.source",
                parameters={"nested": {"value": 1}},
            ),
        ),
    )

    assert deserialize_document(reordered_json) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "text",
    (
        "{",
        "[]",
        "{}",
        '{"format":"vidap.workflow","schemaVersion":"2.0","workflowId":"bad"}',
        '{"format":"vidap.workflow","schemaVersion":"1.0","workflowId":"bad","nodes":[],"edges":[]}',
    ),
)
def test_bad_json_and_basic_envelopes_raise_the_local_decode_signal(text: str) -> None:
    with pytest.raises(WorkflowDecodeError):
        deserialize_document(text)


@pytest.mark.unit
def test_invalid_utf8_text_and_deeply_nested_input_raise_the_local_decode_signal() -> (
    None
):
    lone_surrogate_label = (
        '{"format":"vidap.workflow","schemaVersion":"1.0","workflowId":"'
        + WORKFLOW_ID
        + '","nodes":[{"id":"'
        + SOURCE_ID
        + '","type":"synthetic.source","label":"\\ud800","parameters":{}}],"edges":[]}'
    )
    deeply_nested_non_object = (
        "[" * (sys.getrecursionlimit() + 10)
        + "0"
        + "]" * (sys.getrecursionlimit() + 10)
    )

    with pytest.raises(WorkflowDecodeError):
        deserialize_document(lone_surrogate_label)
    with pytest.raises(WorkflowDecodeError):
        deserialize_document(deeply_nested_non_object)
    with pytest.raises(ValueError):
        WorkflowNode(id=SOURCE_ID, type_id="synthetic.source", label="\ud800")


@pytest.mark.unit
def test_explicit_null_label_is_rejected_without_silent_content_loss() -> None:
    document_with_null_label = (
        '{"format":"vidap.workflow","schemaVersion":"1.0","workflowId":"'
        + WORKFLOW_ID
        + '","nodes":[{"id":"'
        + SOURCE_ID
        + '","type":"synthetic.source","label":null,"parameters":{}}],"edges":[]}'
    )

    with pytest.raises(WorkflowDecodeError):
        deserialize_document(document_with_null_label)


@pytest.mark.unit
def test_public_import_does_not_import_forbidden_consumer_packages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    forbidden_roots = {
        "vidap_execution",
        "vidap_experiments",
        "vidap_export",
        "fastapi",
        "uvicorn",
    }
    for module_name in tuple(sys.modules):
        if module_name.split(".")[0] in forbidden_roots | {"vidap_workflow"}:
            monkeypatch.delitem(sys.modules, module_name, raising=False)

    original_import = builtins.__import__

    def guarded_import(
        name: str,
        globals: dict[str, object] | None = None,
        locals: dict[str, object] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> object:
        if name.split(".")[0] in forbidden_roots:
            raise AssertionError(f"public workflow import attempted to import {name}")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", guarded_import)

    imported = importlib.import_module("vidap_workflow")

    assert imported.__all__ == (
        "Edge",
        "Endpoint",
        "LayoutMetadata",
        "Position",
        "Viewport",
        "WorkflowDecodeError",
        "WorkflowDocument",
        "WorkflowNode",
        "deserialize_document",
        "serialize_document",
        "serialize_semantic_document",
    )
