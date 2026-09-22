"""Validated workflow semantics frozen for a future execution consumer."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from src.vidap_workflow import (
        OMITTED_DEFAULT,
        Diagnostic,
        NodeRegistry,
        WorkflowDocument,
        validate_workflow,
    )
    from src.vidap_workflow.document import JsonValue
else:
    from vidap_workflow import (
        OMITTED_DEFAULT,
        Diagnostic,
        NodeRegistry,
        WorkflowDocument,
        validate_workflow,
    )
    from vidap_workflow.document import JsonValue

from .bindings import BindingMap, StaticBinding

_VALIDATION_POLICY = "vidap.workflow-validation/1.0"


class PreparationFailure(ValueError):
    """Pre-dispatch refusal, preserving Phase 1 findings when invalid."""

    def __init__(
        self, code: str, message: str, diagnostics: tuple[Diagnostic, ...] = ()
    ) -> None:
        super().__init__(message)
        self.code = code
        self.diagnostics = diagnostics


def _freeze(value: object) -> JsonValue:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, str):
        value.encode("utf-8")
        return value
    if isinstance(value, float) and isfinite(value):
        return value
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("parameter names must be text.")
        return MappingProxyType(
            {key: _freeze(item) for key, item in sorted(value.items())}
        )
    if isinstance(value, (tuple, list)):
        return tuple(_freeze(item) for item in value)
    raise ValueError("parameters must contain finite JSON values only.")


def _ordered_json(value: object) -> object:
    """Recursively order object names by RFC 8785 UTF-16 code units only."""

    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("JSON object names must be text.")
        return {
            key: _ordered_json(value[key])
            for key in sorted(value, key=lambda name: name.encode("utf-16-be"))
        }
    if isinstance(value, (list, tuple)):
        return [_ordered_json(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class ExecutionNode:
    """Identity, static binding reference, and resolved canonical parameters."""

    node_id: str
    type_id: str
    operation_key: str
    binding_revision: str
    parameters: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.node_id, str) or not self.node_id:
            raise ValueError("node ID must be non-empty text.")
        if not isinstance(self.type_id, str) or not self.type_id:
            raise ValueError("node type must be non-empty text.")
        StaticBinding(self.operation_key, self.binding_revision)
        frozen = _freeze(self.parameters)
        if not isinstance(frozen, Mapping):
            raise ValueError("node parameters must be a mapping.")
        object.__setattr__(self, "parameters", frozen)


@dataclass(frozen=True, slots=True)
class ExecutionEdge:
    """One directed pair of canonical port endpoints."""

    edge_id: str
    source_node_id: str
    source_port_key: str
    target_node_id: str
    target_port_key: str

    def __post_init__(self) -> None:
        for name in (
            "edge_id",
            "source_node_id",
            "source_port_key",
            "target_node_id",
            "target_port_key",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{name} must be non-empty text.")


@dataclass(frozen=True, slots=True)
class ExecutionRepresentation:
    """ID-stable collections; their order is not an execution schedule."""

    format: str
    schema_version: str
    workflow_id: str
    semantic_digest: str
    contract_snapshot_ref: str
    binding_revision: str
    nodes: tuple[ExecutionNode, ...]
    edges: tuple[ExecutionEdge, ...]

    def __post_init__(self) -> None:
        if self.format != "vidap.workflow" or self.schema_version != "1.0":
            raise ValueError("representation must use the supported workflow envelope.")
        if not isinstance(self.workflow_id, str) or not self.workflow_id:
            raise ValueError("workflow ID must be non-empty text.")
        if not isinstance(self.semantic_digest, str) or not re.fullmatch(
            r"[0-9a-f]{64}", self.semantic_digest
        ):
            raise ValueError("semantic digest must be lowercase SHA-256 hex.")
        if not isinstance(self.contract_snapshot_ref, str) or not re.fullmatch(
            r"[0-9a-f]{64}", self.contract_snapshot_ref
        ):
            raise ValueError(
                "contract snapshot reference must be lowercase SHA-256 hex."
            )
        BindingMap(self.binding_revision)
        nodes = tuple(self.nodes)
        edges = tuple(self.edges)
        if not all(isinstance(node, ExecutionNode) for node in nodes):
            raise ValueError("representation nodes must be ExecutionNode values.")
        if not all(isinstance(edge, ExecutionEdge) for edge in edges):
            raise ValueError("representation edges must be ExecutionEdge values.")
        if len({node.node_id for node in nodes}) != len(nodes):
            raise ValueError("representation node IDs must be unique.")
        if len({edge.edge_id for edge in edges}) != len(edges):
            raise ValueError("representation edge IDs must be unique.")
        if any(node.binding_revision != self.binding_revision for node in nodes):
            raise ValueError("node binding revision must match the representation.")
        object.__setattr__(
            self, "nodes", tuple(sorted(nodes, key=lambda node: node.node_id))
        )
        object.__setattr__(
            self, "edges", tuple(sorted(edges, key=lambda edge: edge.edge_id))
        )


def _validated(document: WorkflowDocument, registry: NodeRegistry) -> None:
    diagnostics = validate_workflow(document, registry)
    if diagnostics:
        raise PreparationFailure(
            "invalid-workflow", "Phase 1 workflow validation failed.", diagnostics
        )


def _resolved_parameters(
    document: WorkflowDocument, registry: NodeRegistry
) -> dict[str, Mapping[str, JsonValue]]:
    resolved: dict[str, Mapping[str, JsonValue]] = {}
    for node in document.nodes:
        definition = registry.get(node.type_id)
        if definition is None:
            raise PreparationFailure(
                "invalid-workflow", "Registered node type is missing."
            )
        values: dict[str, JsonValue] = dict(node.parameters)
        for parameter in definition.parameters:
            if parameter.key not in values and parameter.default is not OMITTED_DEFAULT:
                values[parameter.key] = cast(JsonValue, parameter.default)
        frozen = _freeze(values)
        resolved[node.id] = cast(Mapping[str, JsonValue], frozen)
    return resolved


def _projection(
    document: WorkflowDocument, resolved: Mapping[str, Mapping[str, JsonValue]]
) -> dict[str, object]:
    data = {
        "format": document.format,
        "schemaVersion": document.schema_version,
        "workflowId": document.workflow_id,
        "nodes": [
            {
                "id": node.id,
                "type": node.type_id,
                "parameters": resolved[node.id],
            }
            for node in sorted(document.nodes, key=lambda node: node.id)
        ],
        "edges": [
            {
                "id": edge.id,
                "source": edge.source.to_data(),
                "target": edge.target.to_data(),
            }
            for edge in sorted(document.edges, key=lambda edge: edge.id)
        ],
    }
    return cast(dict[str, object], _ordered_json(data))


def _contract_projection(
    document: WorkflowDocument, registry: NodeRegistry
) -> Mapping[str, JsonValue]:
    """Freeze only the declarative contracts used by a validated document."""

    node_types: list[dict[str, object]] = []
    for type_id in sorted({node.type_id for node in document.nodes}):
        definition = registry.get(type_id)
        if definition is None:
            raise PreparationFailure(
                "invalid-workflow", "Registered node type is missing."
            )
        inputs = [
            {
                "key": port.key,
                "direction": port.direction,
                "nominalType": port.nominal_type,
                "cardinality": port.cardinality,
                "required": port.required,
            }
            for port in sorted(definition.inputs, key=lambda port: port.key)
        ]
        outputs = [
            {
                "key": port.key,
                "direction": port.direction,
                "nominalType": port.nominal_type,
            }
            for port in sorted(definition.outputs, key=lambda port: port.key)
        ]
        parameters: list[dict[str, object]] = []
        for parameter in sorted(definition.parameters, key=lambda item: item.key):
            has_default = parameter.default is not OMITTED_DEFAULT
            parameter_data: dict[str, object] = {
                "key": parameter.key,
                "valueKind": parameter.value_kind,
                "required": parameter.required,
                "defaultPresent": has_default,
                "constraints": parameter.constraints,
            }
            if has_default:
                parameter_data["default"] = parameter.default
            parameters.append(parameter_data)
        node_types.append(
            {
                "typeId": definition.type_id,
                "operationKey": definition.operation_key,
                "inputs": inputs,
                "outputs": outputs,
                "parameters": parameters,
            }
        )
    data = {
        "validationPolicy": _VALIDATION_POLICY,
        "format": document.format,
        "schemaVersion": document.schema_version,
        "nodeTypes": node_types,
    }
    return cast(Mapping[str, JsonValue], _freeze(data))


def _sha256_json(data: object) -> str:
    encoded = json.dumps(
        _ordered_json(data),
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def semantic_projection(
    document: WorkflowDocument, registry: NodeRegistry
) -> dict[str, object]:
    """Inspect the deterministic validated meaning, excluding display fields."""

    _validated(document, registry)
    return _projection(document, _resolved_parameters(document, registry))


def prepare_execution(
    document: WorkflowDocument, registry: NodeRegistry, bindings: BindingMap
) -> ExecutionRepresentation:
    """Validate first, then freeze one static, layout-free handoff value."""

    _validated(document, registry)
    if not isinstance(bindings, BindingMap):
        raise TypeError("prepare_execution requires a BindingMap value.")
    resolved = _resolved_parameters(document, registry)
    nodes: list[ExecutionNode] = []
    for node in document.nodes:
        definition = registry.get(node.type_id)
        if definition is None:
            raise PreparationFailure(
                "invalid-workflow", "Registered node type is missing."
            )
        key = definition.operation_key
        if not key:
            raise PreparationFailure(
                "missing-operation-key",
                f"Node type {node.type_id!r} has no operation key.",
            )
        binding = bindings.get(key)
        if binding is None:
            raise PreparationFailure(
                "unbound-operation", f"Operation key {key!r} has no static binding."
            )
        if binding.revision != bindings.revision:
            raise PreparationFailure(
                "binding-revision-mismatch",
                f"Operation key {key!r} does not match the binding-map revision.",
            )
        nodes.append(
            ExecutionNode(
                node_id=node.id,
                type_id=node.type_id,
                operation_key=key,
                binding_revision=binding.revision,
                parameters=resolved[node.id],
            )
        )
    return ExecutionRepresentation(
        format=document.format,
        schema_version=document.schema_version,
        workflow_id=document.workflow_id,
        semantic_digest=_sha256_json(_projection(document, resolved)),
        contract_snapshot_ref=_sha256_json(_contract_projection(document, registry)),
        binding_revision=bindings.revision,
        nodes=tuple(nodes),
        edges=tuple(
            ExecutionEdge(
                edge_id=edge.id,
                source_node_id=edge.source.node_id,
                source_port_key=edge.source.port_key,
                target_node_id=edge.target.node_id,
                target_port_key=edge.target.port_key,
            )
            for edge in document.edges
        ),
    )
