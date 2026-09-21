"""Pure, deterministic structural and semantic workflow validation."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from typing import cast

from .contracts import (
    OMITTED_DEFAULT,
    PARAMETER_CONSTRAINT_KEYS,
    NodeDefinition,
    ParameterDefinition,
    PortDefinition,
)
from .diagnostics import (
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
    Diagnostic,
)
from .document import Edge, WorkflowDocument, WorkflowNode
from .registry import NodeRegistry
from .serialization import WorkflowDecodeError, deserialize_document


def _finding(
    code: str,
    category: str,
    kind: str,
    reference: str,
    message: str,
    remedy: str,
    *,
    pointer: str | None = None,
    detail: str | None = None,
) -> Diagnostic:
    return Diagnostic(
        code=code,
        severity="error",
        category=category,
        affected_element_kind=kind,
        affected_element_reference=reference,
        message=message,
        remedy=remedy,
        json_pointer=pointer,
        technical_detail=detail,
    )


def _ordered(diagnostics: Iterable[Diagnostic]) -> tuple[Diagnostic, ...]:
    stages = {"structural": 0, "unsupported": 1, "semantic": 2}
    return tuple(
        sorted(
            diagnostics,
            key=lambda finding: (
                stages[finding.category],
                finding.code,
                finding.affected_element_kind,
                finding.affected_element_reference,
                finding.json_pointer or "",
                finding.message,
            ),
        )
    )


def _ports(definition: NodeDefinition) -> dict[str, PortDefinition]:
    return {port.key: port for port in (*definition.inputs, *definition.outputs)}


def _json_sort_key(value: object) -> tuple[object, ...]:
    """Return a recursive, type-explicit key for frozen JSON-compatible values."""

    if value is None:
        return ("null",)
    if isinstance(value, bool):
        return ("boolean", value)
    if isinstance(value, int):
        return ("integer", value)
    if isinstance(value, float):
        return ("number", value)
    if isinstance(value, str):
        return ("string", value)
    if isinstance(value, tuple):
        return ("array", tuple(_json_sort_key(item) for item in value))
    if isinstance(value, Mapping):
        return (
            "object",
            tuple((key, _json_sort_key(item)) for key, item in sorted(value.items())),
        )
    raise TypeError("workflow JSON values must be JSON-compatible.")


def _node_sort_key(node: WorkflowNode) -> tuple[object, ...]:
    """Choose a duplicate-ID representative without consulting source order or label."""

    return (node.id, node.type_id, _json_sort_key(node.parameters))


def _kind_matches(value: object, declared_kind: str) -> bool:
    if declared_kind == "string":
        return isinstance(value, str)
    if declared_kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared_kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if declared_kind == "boolean":
        return isinstance(value, bool)
    if declared_kind == "null":
        return value is None
    if declared_kind == "array":
        return isinstance(value, tuple)
    return isinstance(value, Mapping)


def _unsupported_constraint(
    node: WorkflowNode,
    parameter: ParameterDefinition,
    key: str,
    detail: str,
) -> Diagnostic:
    return _finding(
        UNSUPPORTED_PARAMETER_CONSTRAINT,
        "unsupported",
        "parameter",
        f"{node.id}:{parameter.key}",
        f"Parameter '{parameter.key}' uses unsupported constraint '{key}'.",
        "Use only the documented constraint vocabulary with valid metadata.",
        detail=detail,
    )


def _constraint_findings(
    node: WorkflowNode, parameter: ParameterDefinition, value: object
) -> list[Diagnostic]:
    findings: list[Diagnostic] = []
    constraints = parameter.constraints
    for key in constraints:
        if key not in PARAMETER_CONSTRAINT_KEYS:
            findings.append(
                _unsupported_constraint(node, parameter, key, "unknown constraint key")
            )
    nullable = constraints.get("nullable", False)
    if "nullable" in constraints and not isinstance(nullable, bool):
        findings.append(
            _unsupported_constraint(
                node, parameter, "nullable", "nullable must be boolean"
            )
        )
        return findings
    if value is None:
        if nullable is True:
            return findings
        findings.append(
            _finding(
                PARAMETER_CONSTRAINT_VIOLATION,
                "semantic",
                "parameter",
                f"{node.id}:{parameter.key}",
                f"Parameter '{parameter.key}' cannot be null.",
                "Supply a non-null value or declare nullable metadata.",
            )
        )
        return findings
    relevant = {
        "string": {"allowedValues", "minLength", "maxLength", "pattern"},
        "integer": {"allowedValues", "minimum", "maximum"},
        "number": {"allowedValues", "minimum", "maximum"},
        "boolean": {"allowedValues"},
        "null": set(),
        "array": {"allowedValues", "minItems", "maxItems", "uniqueItems"},
        "object": {"allowedValues", "requiredKeys"},
    }[parameter.value_kind]
    for key in constraints:
        if key in set(PARAMETER_CONSTRAINT_KEYS) - {"nullable"} and key not in relevant:
            findings.append(
                _unsupported_constraint(
                    node, parameter, key, f"not applicable to {parameter.value_kind}"
                )
            )
    if any(finding.category == "unsupported" for finding in findings):
        return findings

    def violated(text: str, remedy: str) -> None:
        findings.append(
            _finding(
                PARAMETER_CONSTRAINT_VIOLATION,
                "semantic",
                "parameter",
                f"{node.id}:{parameter.key}",
                f"Parameter '{parameter.key}' {text}.",
                remedy,
            )
        )

    allowed = constraints.get("allowedValues")
    if allowed is not None:
        if not isinstance(allowed, tuple):
            findings.append(
                _unsupported_constraint(
                    node, parameter, "allowedValues", "must be an array"
                )
            )
        elif value not in allowed:
            violated(
                "is not an allowed value", "Choose one of the declared allowed values."
            )
    if parameter.value_kind in {"integer", "number"}:
        number_value = cast(int | float, value)
        for key, invalid in (("minimum", number_value), ("maximum", number_value)):
            if key not in constraints:
                continue
            bound = constraints[key]
            if isinstance(bound, bool) or not isinstance(bound, (int, float)):
                findings.append(
                    _unsupported_constraint(node, parameter, key, "must be numeric")
                )
            elif key == "minimum" and invalid < bound:
                violated(
                    "is below the minimum",
                    "Use a value within the declared numeric range.",
                )
            elif key == "maximum" and invalid > bound:
                violated(
                    "is above the maximum",
                    "Use a value within the declared numeric range.",
                )
    if parameter.value_kind in {"string", "array"}:
        sized_value = cast(str | tuple[object, ...], value)
        labels = (
            ("minLength", "is shorter than required"),
            ("maxLength", "is longer than allowed"),
            ("minItems", "has too few items"),
            ("maxItems", "has too many items"),
        )
        for key, wording in labels:
            if key not in constraints:
                continue
            bound = constraints[key]
            if isinstance(bound, bool) or not isinstance(bound, int) or bound < 0:
                findings.append(
                    _unsupported_constraint(
                        node, parameter, key, "must be a non-negative integer"
                    )
                )
            elif key.startswith("min") and len(sized_value) < bound:
                violated(wording, "Use a value within the declared size limits.")
            elif key.startswith("max") and len(sized_value) > bound:
                violated(wording, "Use a value within the declared size limits.")
    if "pattern" in constraints:
        pattern = constraints["pattern"]
        if not isinstance(pattern, str):
            findings.append(
                _unsupported_constraint(node, parameter, "pattern", "must be text")
            )
        else:
            try:
                matches = re.search(pattern, cast(str, value)) is not None
            except re.error as error:
                findings.append(
                    _unsupported_constraint(node, parameter, "pattern", str(error))
                )
            else:
                if not matches:
                    violated(
                        "does not match the required pattern",
                        "Use text matching the declared pattern.",
                    )
    if "uniqueItems" in constraints:
        unique = constraints["uniqueItems"]
        if not isinstance(unique, bool):
            findings.append(
                _unsupported_constraint(
                    node, parameter, "uniqueItems", "must be boolean"
                )
            )
        elif unique and _contains_duplicate_items(cast(tuple[object, ...], value)):
            violated("contains duplicate items", "Remove duplicate array items.")
    if "requiredKeys" in constraints:
        required_keys = constraints["requiredKeys"]
        if not isinstance(required_keys, tuple) or not all(
            isinstance(key, str) for key in required_keys
        ):
            findings.append(
                _unsupported_constraint(
                    node, parameter, "requiredKeys", "must be an array of strings"
                )
            )
        else:
            missing = sorted(
                set(cast(tuple[str, ...], required_keys))
                - set(cast(Mapping[str, object], value))
            )
            if missing:
                violated(
                    "is missing required object keys",
                    "Add every declared required key.",
                )
    return findings


def _contains_duplicate_items(items: tuple[object, ...]) -> bool:
    """Compare JSON values without assuming array elements are hashable."""

    return any(
        item == prior for index, item in enumerate(items) for prior in items[:index]
    )


def _parameter_findings(
    node: WorkflowNode, definition: NodeDefinition
) -> list[Diagnostic]:
    findings: list[Diagnostic] = []
    definitions = {parameter.key: parameter for parameter in definition.parameters}
    for key in node.parameters:
        if key not in definitions:
            findings.append(
                _finding(
                    UNKNOWN_PARAMETER,
                    "semantic",
                    "parameter",
                    f"{node.id}:{key}",
                    f"Parameter '{key}' is not declared for this node type.",
                    "Remove the parameter or use a declared parameter key.",
                )
            )
    for parameter in definition.parameters:
        value = node.parameters.get(parameter.key, OMITTED_DEFAULT)
        if value is OMITTED_DEFAULT:
            value = parameter.default
        if value is OMITTED_DEFAULT:
            if parameter.required:
                findings.append(
                    _finding(
                        MISSING_REQUIRED_PARAMETER,
                        "semantic",
                        "parameter",
                        f"{node.id}:{parameter.key}",
                        f"Required parameter '{parameter.key}' is missing.",
                        "Supply a value for the required parameter.",
                    )
                )
            continue
        if not (
            value is None and parameter.constraints.get("nullable") is True
        ) and not _kind_matches(value, parameter.value_kind):
            findings.append(
                _finding(
                    PARAMETER_KIND_MISMATCH,
                    "semantic",
                    "parameter",
                    f"{node.id}:{parameter.key}",
                    f"Parameter '{parameter.key}' has the wrong declared value kind.",
                    f"Supply a {parameter.value_kind} value.",
                )
            )
            continue
        findings.extend(_constraint_findings(node, parameter, value))
    return findings


def _has_cycle(edges: Iterable[tuple[str, str]]) -> bool:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for source, target in edges:
        adjacency[source].add(target)
        adjacency.setdefault(target, set())
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        if any(visit(child) for child in sorted(adjacency[node_id])):
            return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node_id) for node_id in sorted(adjacency))


def validate_workflow(
    document: WorkflowDocument, registry: NodeRegistry
) -> tuple[Diagnostic, ...]:
    """Return stable findings for a workflow without modifying or executing it."""

    if not isinstance(document, WorkflowDocument) or not isinstance(
        registry, NodeRegistry
    ):
        raise TypeError(
            "validate_workflow requires WorkflowDocument and NodeRegistry values."
        )
    findings: list[Diagnostic] = []
    nodes_by_id: dict[str, WorkflowNode] = {}
    for node_id, count in sorted(Counter(node.id for node in document.nodes).items()):
        if count > 1:
            findings.append(
                _finding(
                    DUPLICATE_NODE_ID,
                    "structural",
                    "node",
                    node_id,
                    f"Node ID '{node_id}' is duplicated.",
                    "Give each node a unique ID.",
                )
            )
    for node in sorted(document.nodes, key=_node_sort_key):
        nodes_by_id.setdefault(node.id, node)
    for edge_id, count in sorted(Counter(edge.id for edge in document.edges).items()):
        if count > 1:
            findings.append(
                _finding(
                    DUPLICATE_EDGE_ID,
                    "structural",
                    "edge",
                    edge_id,
                    f"Edge ID '{edge_id}' is duplicated.",
                    "Give each edge a unique ID.",
                )
            )
    edge_shapes = Counter(
        (
            edge.source.node_id,
            edge.source.port_key,
            edge.target.node_id,
            edge.target.port_key,
        )
        for edge in document.edges
    )
    for shape, count in sorted(edge_shapes.items()):
        if count > 1:
            reference = f"{shape[0]}:{shape[1]}->{shape[2]}:{shape[3]}"
            findings.append(
                _finding(
                    DUPLICATE_EXACT_EDGE,
                    "structural",
                    "edge",
                    reference,
                    "The same connection appears more than once.",
                    "Keep only one edge for this connection.",
                )
            )

    definitions: dict[str, NodeDefinition] = {}
    for node_id, node in sorted(nodes_by_id.items()):
        definition = registry.get(node.type_id)
        if definition is None:
            findings.append(
                _finding(
                    UNKNOWN_NODE_TYPE,
                    "unsupported",
                    "node",
                    node_id,
                    f"Node type '{node.type_id}' is not registered.",
                    "Register an approved node type or replace this node.",
                )
            )
        else:
            definitions[node_id] = definition
            findings.extend(_parameter_findings(node, definition))

    valid_edges: list[Edge] = []
    seen_shapes: set[tuple[str, str, str, str]] = set()
    incoming: dict[tuple[str, str], int] = defaultdict(int)
    for edge in document.edges:
        shape = (
            edge.source.node_id,
            edge.source.port_key,
            edge.target.node_id,
            edge.target.port_key,
        )
        if shape in seen_shapes:
            continue
        seen_shapes.add(shape)
        source_node = nodes_by_id.get(edge.source.node_id)
        target_node = nodes_by_id.get(edge.target.node_id)
        edge_reference = edge.id
        if source_node is None:
            findings.append(
                _finding(
                    DANGLING_NODE,
                    "semantic",
                    "edge",
                    edge_reference,
                    "Edge source refers to a missing node.",
                    "Connect the edge to an existing source node.",
                )
            )
        if target_node is None:
            findings.append(
                _finding(
                    DANGLING_NODE,
                    "semantic",
                    "edge",
                    edge_reference,
                    "Edge target refers to a missing node.",
                    "Connect the edge to an existing target node.",
                )
            )
        if source_node is None or target_node is None:
            continue
        source_definition = definitions.get(source_node.id)
        target_definition = definitions.get(target_node.id)
        if source_definition is None or target_definition is None:
            continue
        source_port = _ports(source_definition).get(edge.source.port_key)
        target_port = _ports(target_definition).get(edge.target.port_key)
        if source_port is None:
            findings.append(
                _finding(
                    UNKNOWN_PORT,
                    "semantic",
                    "edge",
                    edge_reference,
                    "Edge source refers to an unknown port.",
                    "Use a declared source port.",
                )
            )
        if target_port is None:
            findings.append(
                _finding(
                    UNKNOWN_PORT,
                    "semantic",
                    "edge",
                    edge_reference,
                    "Edge target refers to an unknown port.",
                    "Use a declared target port.",
                )
            )
        if source_port is None or target_port is None:
            continue
        if source_port.direction != "output" or target_port.direction != "input":
            findings.append(
                _finding(
                    REVERSED_DIRECTION,
                    "semantic",
                    "edge",
                    edge_reference,
                    "Edges must connect an output port to an input port.",
                    "Reverse or replace the connection endpoints.",
                )
            )
            continue
        if source_port.nominal_type != target_port.nominal_type:
            findings.append(
                _finding(
                    NOMINAL_TYPE_MISMATCH,
                    "semantic",
                    "edge",
                    edge_reference,
                    "Connected ports use different nominal types.",
                    "Connect ports with the same declared type.",
                )
            )
            continue
        valid_edges.append(edge)
        incoming[(target_node.id, target_port.key)] += 1
    for node_id, definition in sorted(definitions.items()):
        for port in definition.inputs:
            count = incoming[(node_id, port.key)]
            reference = f"{node_id}:{port.key}"
            if port.cardinality == "one" and count > 1:
                findings.append(
                    _finding(
                        INPUT_CARDINALITY_EXCEEDED,
                        "semantic",
                        "port",
                        reference,
                        f"Input '{port.key}' accepts only one connection.",
                        "Keep one compatible incoming edge.",
                    )
                )
            if port.required and count == 0:
                findings.append(
                    _finding(
                        MISSING_REQUIRED_INPUT,
                        "semantic",
                        "port",
                        reference,
                        f"Required input '{port.key}' is not connected.",
                        "Add one compatible incoming edge.",
                    )
                )
    if _has_cycle((edge.source.node_id, edge.target.node_id) for edge in valid_edges):
        findings.append(
            _finding(
                DIRECTED_CYCLE,
                "semantic",
                "workflow",
                document.workflow_id,
                "Workflow connections contain a directed cycle.",
                "Remove an edge so the workflow is acyclic.",
            )
        )
    return _ordered(findings)


def validate_workflow_text(text: str, registry: NodeRegistry) -> tuple[Diagnostic, ...]:
    """Validate JSON text through the strict, non-mutating workflow boundary."""

    if not isinstance(registry, NodeRegistry):
        raise TypeError("validate_workflow_text requires a NodeRegistry value.")
    try:
        document = deserialize_document(text)
    except WorkflowDecodeError as error:
        return _ordered(
            (
                _finding(
                    error.code,
                    error.category,
                    "document-field",
                    error.field,
                    str(error),
                    error.remedy,
                    pointer=(f"/{error.field}" if error.field != "root" else ""),
                    detail=error.detail,
                ),
            )
        )
    return validate_workflow(document, registry)
