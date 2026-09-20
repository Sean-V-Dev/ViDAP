"""Immutable workflow values with deterministic, JSON-compatible projections.

This module preserves document shape and stable identifiers only.  It does not
validate node contracts, graph semantics, or execution behavior.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from uuid import UUID

WORKFLOW_FORMAT = "vidap.workflow"
WORKFLOW_SCHEMA_VERSION = "1.0"

type Number = int | float
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | tuple[JsonValue, ...] | Mapping[str, JsonValue]


def _require_non_empty_string(value: object, field_name: str) -> str:
    text = _require_utf8_string(value, field_name)
    if not text:
        raise ValueError(f"{field_name} must be a non-empty string.")
    return text


def _require_utf8_string(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError(f"{field_name} must be valid UTF-8 text.") from error
    return value


def _require_uuid4(value: object, field_name: str) -> str:
    text = _require_non_empty_string(value, field_name)
    try:
        parsed = UUID(text)
    except ValueError as error:
        raise ValueError(f"{field_name} must be lowercase UUIDv4 text.") from error
    if parsed.version != 4 or str(parsed) != text:
        raise ValueError(f"{field_name} must be lowercase UUIDv4 text.")
    return text


def _require_number(value: object, field_name: str) -> Number:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a JSON number.")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError(f"{field_name} must be a finite JSON number.")
    return value


def _freeze_json_value(value: object, field_name: str) -> JsonValue:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, str):
        return _require_utf8_string(value, field_name)
    if isinstance(value, float):
        if not isfinite(value):
            raise ValueError(f"{field_name} must not contain a non-finite number.")
        return value
    if isinstance(value, Mapping):
        return _freeze_json_mapping(value, field_name)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json_value(item, field_name) for item in value)
    raise ValueError(f"{field_name} must contain JSON-compatible values only.")


def _freeze_json_mapping(value: object, field_name: str) -> Mapping[str, JsonValue]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping.")

    frozen: dict[str, JsonValue] = {}
    for key, item in value.items():
        frozen_key = _require_non_empty_string(key, f"{field_name} key")
        frozen[frozen_key] = _freeze_json_value(item, f"{field_name}.{frozen_key}")
    return MappingProxyType(dict(sorted(frozen.items())))


def _thaw_json_value(value: JsonValue) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw_json_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json_value(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class Endpoint:
    """A reference to one immutable contract port on one workflow node."""

    node_id: str
    port_key: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "node_id", _require_uuid4(self.node_id, "node_id"))
        object.__setattr__(
            self, "port_key", _require_non_empty_string(self.port_key, "port_key")
        )

    def to_data(self) -> dict[str, str]:
        return {"nodeId": self.node_id, "portKey": self.port_key}


@dataclass(frozen=True, slots=True)
class Edge:
    """A directed edge with explicit source and target endpoint references."""

    id: str
    source: Endpoint
    target: Endpoint

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _require_uuid4(self.id, "edge id"))
        if not isinstance(self.source, Endpoint) or not isinstance(
            self.target, Endpoint
        ):
            raise ValueError("edge endpoints must be Endpoint values.")

    def to_data(self) -> dict[str, object]:
        return {
            "id": self.id,
            "source": self.source.to_data(),
            "target": self.target.to_data(),
        }


@dataclass(frozen=True, slots=True)
class WorkflowNode:
    """A node instance without registry, parameter, or port-contract validation."""

    id: str
    type_id: str
    label: str | None = None
    parameters: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _require_uuid4(self.id, "node id"))
        object.__setattr__(
            self, "type_id", _require_non_empty_string(self.type_id, "node type")
        )
        if self.label is not None:
            object.__setattr__(
                self, "label", _require_utf8_string(self.label, "node label")
            )
        object.__setattr__(
            self, "parameters", _freeze_json_mapping(self.parameters, "parameters")
        )

    def to_data(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "parameters": _thaw_json_value(self.parameters),
            "type": self.type_id,
        }
        if self.label is not None:
            data["label"] = self.label
        return data


@dataclass(frozen=True, slots=True)
class Position:
    """A non-semantic two-dimensional layout position."""

    x: Number
    y: Number

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _require_number(self.x, "position x"))
        object.__setattr__(self, "y", _require_number(self.y, "position y"))

    def to_data(self) -> dict[str, Number]:
        return {"x": self.x, "y": self.y}


@dataclass(frozen=True, slots=True)
class Viewport:
    """Non-semantic viewport coordinates retained only in full-document output."""

    x: Number
    y: Number
    zoom: Number

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _require_number(self.x, "viewport x"))
        object.__setattr__(self, "y", _require_number(self.y, "viewport y"))
        object.__setattr__(self, "zoom", _require_number(self.zoom, "viewport zoom"))

    def to_data(self) -> dict[str, Number]:
        return {"x": self.x, "y": self.y, "zoom": self.zoom}


@dataclass(frozen=True, slots=True)
class LayoutMetadata:
    """Optional presentation metadata isolated from workflow semantics."""

    node_positions: Mapping[str, Position] = field(default_factory=dict)
    viewport: Viewport | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.node_positions, Mapping):
            raise ValueError("node_positions must be a mapping.")
        positions: dict[str, Position] = {}
        for node_id, position in self.node_positions.items():
            positions[_require_uuid4(node_id, "layout node id")] = position
            if not isinstance(position, Position):
                raise ValueError("layout node positions must be Position values.")
        if self.viewport is not None and not isinstance(self.viewport, Viewport):
            raise ValueError("layout viewport must be a Viewport value when supplied.")
        object.__setattr__(
            self, "node_positions", MappingProxyType(dict(sorted(positions.items())))
        )

    def to_data(self) -> dict[str, object]:
        data: dict[str, object] = {
            "nodePositions": {
                node_id: position.to_data()
                for node_id, position in self.node_positions.items()
            }
        }
        if self.viewport is not None:
            data["viewport"] = self.viewport.to_data()
        return data


@dataclass(frozen=True, slots=True, eq=False)
class WorkflowDocument:
    """The canonical workflow document, excluding any execution interpretation."""

    workflow_id: str
    nodes: tuple[WorkflowNode, ...] = ()
    edges: tuple[Edge, ...] = ()
    layout: LayoutMetadata | None = None
    format: str = WORKFLOW_FORMAT
    schema_version: str = WORKFLOW_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "workflow_id", _require_uuid4(self.workflow_id, "workflow id")
        )
        if self.format != WORKFLOW_FORMAT:
            raise ValueError(f"format must be {WORKFLOW_FORMAT!r}.")
        if self.schema_version != WORKFLOW_SCHEMA_VERSION:
            raise ValueError(f"schema_version must be {WORKFLOW_SCHEMA_VERSION!r}.")

        nodes = tuple(self.nodes)
        edges = tuple(self.edges)
        if not all(isinstance(node, WorkflowNode) for node in nodes):
            raise ValueError("nodes must contain WorkflowNode values only.")
        if not all(isinstance(edge, Edge) for edge in edges):
            raise ValueError("edges must contain Edge values only.")
        if self.layout is not None and not isinstance(self.layout, LayoutMetadata):
            raise ValueError("layout must be LayoutMetadata when supplied.")

        object.__setattr__(
            self, "nodes", tuple(sorted(nodes, key=lambda node: node.id))
        )
        object.__setattr__(
            self, "edges", tuple(sorted(edges, key=lambda edge: edge.id))
        )

    def __hash__(self) -> int:
        raise TypeError("unhashable type: 'WorkflowDocument'")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WorkflowDocument):
            return NotImplemented
        return self.semantic_data() == other.semantic_data()

    def semantic_data(self) -> dict[str, object]:
        """Return the canonical semantic data projection without layout metadata."""

        return {
            "edges": [edge.to_data() for edge in self.edges],
            "format": self.format,
            "nodes": [node.to_data() for node in self.nodes],
            "schemaVersion": self.schema_version,
            "workflowId": self.workflow_id,
        }

    def full_data(self) -> dict[str, object]:
        """Return the canonical full-document projection, including optional layout."""

        data = self.semantic_data()
        if self.layout is not None:
            data["layout"] = self.layout.to_data()
        return data
