"""Deterministic JSON serialization and narrow basic-envelope decoding."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast

from .document import (
    Edge,
    Endpoint,
    JsonValue,
    LayoutMetadata,
    Position,
    Viewport,
    WorkflowDocument,
    WorkflowNode,
    _require_number,
)

type JsonObject = dict[str, object]


class WorkflowDecodeError(ValueError):
    """Signals malformed JSON or a malformed basic workflow-document envelope."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "VIDAP-MALFORMED-ENVELOPE",
        category: str = "structural",
        field: str = "root",
        remedy: str = "Supply a complete workflow document with the required shape.",
        detail: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.category = category
        self.field = field
        self.remedy = remedy
        self.detail = detail


def serialize_document(document: WorkflowDocument) -> str:
    """Encode a full document as UTF-8 JSON text with two-space indent and one newline."""

    return _serialize(document.full_data())


def serialize_semantic_document(document: WorkflowDocument) -> str:
    """Encode only semantic document data with the same deterministic text policy."""

    return _serialize(document.semantic_data())


def deserialize_document(text: str) -> WorkflowDocument:
    """Decode only the supported basic ``vidap.workflow`` / ``1.0`` envelope.

    This boundary intentionally does not validate contracts, registry membership,
    graph structure, or execution behavior.
    """

    if not isinstance(text, str):
        raise WorkflowDecodeError(
            "Workflow JSON must be text.",
            code="VIDAP-MALFORMED-JSON",
            field="text",
            remedy="Supply UTF-8 JSON text for the workflow document.",
        )
    try:
        decoded = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_non_json_constant,
        )
        return _decode_document(_expect_object(decoded, "root"))
    except WorkflowDecodeError:
        raise
    except json.JSONDecodeError, RecursionError, TypeError, ValueError:
        raise WorkflowDecodeError(
            "Workflow JSON is malformed.",
            code="VIDAP-MALFORMED-JSON",
            field="text",
            remedy="Correct the JSON syntax and submit one complete JSON value.",
        ) from None


def _serialize(data: Mapping[str, object]) -> str:
    return (
        json.dumps(
            data,
            allow_nan=False,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def _unique_object(pairs: list[tuple[str, object]]) -> JsonObject:
    result: JsonObject = {}
    for key, value in pairs:
        if key in result:
            raise WorkflowDecodeError(
                "Workflow JSON must not contain duplicate object names.",
                code="VIDAP-DUPLICATE-OBJECT-NAME",
                field="root",
                remedy="Keep one value for each object name.",
            )
        result[key] = value
    return result


def _reject_non_json_constant(value: str) -> None:
    raise ValueError(f"{value} is not valid JSON.")


def _expect_object(value: object, name: str) -> JsonObject:
    if not isinstance(value, dict):
        raise WorkflowDecodeError(
            f"{name} must be an object.",
            code=(
                "VIDAP-NONOBJECT-ROOT" if name == "root" else "VIDAP-MALFORMED-ENVELOPE"
            ),
            field=name,
            remedy=(
                "Supply one JSON object as the workflow root."
                if name == "root"
                else "Supply the required object value for this workflow field."
            ),
        )
    return value


def _expect_list(value: object, name: str) -> list[object]:
    if not isinstance(value, list):
        raise WorkflowDecodeError(f"{name} must be an array.")
    return value


def _expect_exact_keys(
    value: JsonObject,
    *,
    name: str,
    required: set[str],
    optional: set[str] | None = None,
) -> None:
    allowed = required | (optional or set())
    if not required.issubset(value) or not set(value).issubset(allowed):
        raise WorkflowDecodeError(f"{name} has unsupported or missing fields.")


def _expect_string(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise WorkflowDecodeError(f"{name} must be a string.")
    return value


def _decode_document(value: JsonObject) -> WorkflowDocument:
    for field, expected in (("format", "vidap.workflow"), ("schemaVersion", "1.0")):
        if field not in value or value[field] != expected:
            raise WorkflowDecodeError(
                f"Workflow {field} is not supported.",
                code="VIDAP-UNSUPPORTED-VERSION",
                category="unsupported",
                field=field,
                remedy="Use format 'vidap.workflow' with schemaVersion '1.0'.",
                detail=f"Expected {field}={expected!r}.",
            )
    allowed = {"format", "schemaVersion", "workflowId", "nodes", "edges", "layout"}
    unknown = set(value) - allowed
    if "extensions" in unknown:
        raise WorkflowDecodeError(
            "Workflow extensions are not supported by schemaVersion '1.0'.",
            code="VIDAP-UNSUPPORTED-EXTENSION",
            category="unsupported",
            field="extensions",
            remedy="Remove extension content or use a future reader that explicitly supports it.",
        )
    if unknown:
        fields = ", ".join(sorted(unknown))
        raise WorkflowDecodeError(
            f"Workflow JSON has unknown core field(s): {fields}.",
            code="VIDAP-UNKNOWN-CORE-FIELD",
            field=fields,
            remedy="Remove fields that are not part of the supported 1.0 envelope.",
        )
    required = {"format", "schemaVersion", "workflowId", "nodes", "edges"}
    if not required.issubset(value):
        raise WorkflowDecodeError(
            "Workflow JSON is missing required envelope fields.",
            code="VIDAP-MALFORMED-ENVELOPE",
            field="root",
            remedy="Supply format, schemaVersion, workflowId, nodes, and edges.",
        )
    try:
        layout = _decode_layout(value["layout"]) if "layout" in value else None
        return WorkflowDocument(
            workflow_id=_expect_string(value["workflowId"], "workflowId"),
            nodes=tuple(
                _decode_node(item) for item in _expect_list(value["nodes"], "nodes")
            ),
            edges=tuple(
                _decode_edge(item) for item in _expect_list(value["edges"], "edges")
            ),
            layout=layout,
        )
    except WorkflowDecodeError:
        raise
    except ValueError:
        raise WorkflowDecodeError(
            "Workflow JSON has malformed basic values.",
            code="VIDAP-MALFORMED-ENVELOPE",
            field="root",
            remedy="Correct the affected envelope value and use the supported 1.0 shape.",
        ) from None


def _decode_node(value: object) -> WorkflowNode:
    node = _expect_object(value, "node")
    _expect_exact_keys(
        node,
        name="node",
        required={"id", "type", "parameters"},
        optional={"label"},
    )
    parameters = _expect_object(node["parameters"], "node parameters")
    label: str | None = None
    if "label" in node:
        label = _expect_string(node["label"], "node label")
    return WorkflowNode(
        id=_expect_string(node["id"], "node id"),
        type_id=_expect_string(node["type"], "node type"),
        label=label,
        parameters=cast(Mapping[str, JsonValue], parameters),
    )


def _decode_edge(value: object) -> Edge:
    edge = _expect_object(value, "edge")
    _expect_exact_keys(edge, name="edge", required={"id", "source", "target"})
    return Edge(
        id=_expect_string(edge["id"], "edge id"),
        source=_decode_endpoint(edge["source"], "edge source"),
        target=_decode_endpoint(edge["target"], "edge target"),
    )


def _decode_endpoint(value: object, name: str) -> Endpoint:
    endpoint = _expect_object(value, name)
    _expect_exact_keys(endpoint, name=name, required={"nodeId", "portKey"})
    return Endpoint(
        node_id=_expect_string(endpoint["nodeId"], f"{name} nodeId"),
        port_key=_expect_string(endpoint["portKey"], f"{name} portKey"),
    )


def _decode_layout(value: object) -> LayoutMetadata:
    layout = _expect_object(value, "layout")
    _expect_exact_keys(
        layout,
        name="layout",
        required={"nodePositions"},
        optional={"viewport"},
    )
    positions = _expect_object(layout["nodePositions"], "layout nodePositions")
    return LayoutMetadata(
        node_positions={
            node_id: _decode_position(position)
            for node_id, position in positions.items()
        },
        viewport=_decode_viewport(layout["viewport"]) if "viewport" in layout else None,
    )


def _decode_position(value: object) -> Position:
    position = _expect_object(value, "layout position")
    _expect_exact_keys(position, name="layout position", required={"x", "y"})
    return Position(
        x=_decode_number(position["x"], "layout position x"),
        y=_decode_number(position["y"], "layout position y"),
    )


def _decode_viewport(value: object) -> Viewport:
    viewport = _expect_object(value, "layout viewport")
    _expect_exact_keys(viewport, name="layout viewport", required={"x", "y", "zoom"})
    return Viewport(
        x=_decode_number(viewport["x"], "layout viewport x"),
        y=_decode_number(viewport["y"], "layout viewport y"),
        zoom=_decode_number(viewport["zoom"], "layout viewport zoom"),
    )


def _decode_number(value: object, name: str) -> int | float:
    try:
        return _require_number(value, name)
    except ValueError:
        raise WorkflowDecodeError(f"{name} must be a finite JSON number.") from None
