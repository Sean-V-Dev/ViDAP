"""Immutable declarative node-contract values.

These values describe node metadata only.  They do not inspect workflow
instances, validate connections or overrides, or select any runtime behavior.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType

NOMINAL_TYPE_TOKENS = (
    "table",
    "target",
    "split",
    "model",
    "predictions",
    "metrics",
    "artifact",
)
"""The complete initial vocabulary for nominal workflow artifact types."""

INPUT_CARDINALITIES = ("one", "many")
"""The supported declarative cardinalities for input ports."""

PARAMETER_VALUE_KINDS = (
    "string",
    "integer",
    "number",
    "boolean",
    "null",
    "array",
    "object",
)
"""The JSON-compatible declared value kinds for parameter metadata."""

PARAMETER_CONSTRAINT_KEYS = (
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
"""The complete initial declarative parameter-constraint vocabulary."""

_TYPE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | tuple[JsonValue, ...] | Mapping[str, JsonValue]


class _OmittedDefault:
    """Identity sentinel for a parameter definition without a declared default."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "OMITTED_DEFAULT"


OMITTED_DEFAULT = _OmittedDefault()
"""An explicit immutable marker distinguishing an omitted default from ``None``."""


def _require_text(value: object, field_name: str, *, non_empty: bool = True) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text.")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError(f"{field_name} must be valid UTF-8 text.") from error
    if non_empty and not value:
        raise ValueError(f"{field_name} must not be empty.")
    return value


def _freeze_json_value(value: object, field_name: str) -> JsonValue:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, str):
        return _require_text(value, field_name, non_empty=False)
    if isinstance(value, float):
        if not isfinite(value):
            raise ValueError(f"{field_name} must not contain a non-finite number.")
        return value
    if isinstance(value, Mapping):
        return _freeze_metadata_mapping(value, field_name)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json_value(item, field_name) for item in value)
    raise ValueError(f"{field_name} must contain JSON-compatible metadata only.")


def _freeze_metadata_mapping(value: object, field_name: str) -> Mapping[str, JsonValue]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping.")
    frozen: dict[str, JsonValue] = {}
    for key, item in value.items():
        frozen_key = _require_text(key, f"{field_name} key")
        frozen[frozen_key] = _freeze_json_value(item, f"{field_name}.{frozen_key}")
    return MappingProxyType(dict(sorted(frozen.items())))


@dataclass(frozen=True, slots=True)
class DisplayMetadata:
    """Human-readable, non-semantic contract display metadata."""

    label: str
    description: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "label", _require_text(self.label, "display label"))
        if self.description is not None:
            object.__setattr__(
                self,
                "description",
                _require_text(self.description, "display description", non_empty=False),
            )


@dataclass(frozen=True, slots=True)
class PortDefinition:
    """A declared node port with no connection-validation behavior."""

    key: str
    direction: str
    nominal_type: str
    display: DisplayMetadata
    cardinality: str | None = None
    required: bool | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "key", _require_text(self.key, "port key"))
        if self.direction not in {"input", "output"}:
            raise ValueError("port direction must be 'input' or 'output'.")
        if self.nominal_type not in NOMINAL_TYPE_TOKENS:
            raise ValueError(
                "port nominal_type must be an accepted nominal type token."
            )
        if not isinstance(self.display, DisplayMetadata):
            raise ValueError("port display must be DisplayMetadata.")
        if self.direction == "input":
            if self.cardinality not in INPUT_CARDINALITIES:
                raise ValueError("input port cardinality must be 'one' or 'many'.")
            if not isinstance(self.required, bool):
                raise ValueError("input port required must be a boolean.")
        elif self.cardinality is not None or self.required is not None:
            raise ValueError("output ports do not declare cardinality or requiredness.")


@dataclass(frozen=True, slots=True)
class ParameterDefinition:
    """A declared parameter contract, including metadata but no value validation."""

    key: str
    value_kind: str
    required: bool
    display: DisplayMetadata
    default: JsonValue | _OmittedDefault = OMITTED_DEFAULT
    constraints: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "key", _require_text(self.key, "parameter key"))
        if self.value_kind not in PARAMETER_VALUE_KINDS:
            raise ValueError(
                "parameter value_kind must be an accepted JSON value kind."
            )
        if not isinstance(self.required, bool):
            raise ValueError("parameter required must be a boolean.")
        if not isinstance(self.display, DisplayMetadata):
            raise ValueError("parameter display must be DisplayMetadata.")
        if self.default is not OMITTED_DEFAULT:
            object.__setattr__(
                self, "default", _freeze_json_value(self.default, "parameter default")
            )
        object.__setattr__(
            self,
            "constraints",
            _freeze_metadata_mapping(self.constraints, "parameter constraints"),
        )


@dataclass(frozen=True, slots=True)
class NodeDefinition:
    """An immutable node type declaration without a runtime implementation."""

    type_id: str
    display: DisplayMetadata
    inputs: tuple[PortDefinition, ...] = ()
    outputs: tuple[PortDefinition, ...] = ()
    parameters: tuple[ParameterDefinition, ...] = ()
    operation_key: str | None = None

    def __post_init__(self) -> None:
        type_id = _require_text(self.type_id, "node type_id")
        if not _TYPE_ID_PATTERN.fullmatch(type_id):
            raise ValueError("node type_id must be a lowercase namespaced identifier.")
        object.__setattr__(self, "type_id", type_id)
        if not isinstance(self.display, DisplayMetadata):
            raise ValueError("node display must be DisplayMetadata.")

        inputs = tuple(self.inputs)
        outputs = tuple(self.outputs)
        parameters = tuple(self.parameters)
        if not all(isinstance(port, PortDefinition) for port in inputs):
            raise ValueError("node inputs must contain PortDefinition values only.")
        if not all(isinstance(port, PortDefinition) for port in outputs):
            raise ValueError("node outputs must contain PortDefinition values only.")
        if not all(
            isinstance(parameter, ParameterDefinition) for parameter in parameters
        ):
            raise ValueError(
                "node parameters must contain ParameterDefinition values only."
            )
        if any(port.direction != "input" for port in inputs):
            raise ValueError("node inputs must contain input ports only.")
        if any(port.direction != "output" for port in outputs):
            raise ValueError("node outputs must contain output ports only.")
        _require_unique_keys(
            (port.key for port in (*inputs, *outputs)), "node port keys"
        )
        _require_unique_keys(
            (parameter.key for parameter in parameters), "node parameter keys"
        )
        object.__setattr__(self, "inputs", inputs)
        object.__setattr__(self, "outputs", outputs)
        object.__setattr__(self, "parameters", parameters)

        if self.operation_key is not None:
            object.__setattr__(
                self,
                "operation_key",
                _require_text(self.operation_key, "operation_key"),
            )


def _require_unique_keys(keys: Iterable[str], field_name: str) -> None:
    seen: set[str] = set()
    for key in keys:
        if key in seen:
            raise ValueError(f"{field_name} must be unique within a node definition.")
        seen.add(key)
