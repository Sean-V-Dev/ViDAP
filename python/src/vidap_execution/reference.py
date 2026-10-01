"""Four first-party checked-integer operations for the bounded Phase 2 proof."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.vidap_workflow import (
        DisplayMetadata,
        NodeDefinition,
        NodeRegistry,
        ParameterDefinition,
        PortDefinition,
        WorkflowDocument,
    )
else:
    from vidap_workflow import (
        DisplayMetadata,
        NodeDefinition,
        NodeRegistry,
        ParameterDefinition,
        PortDefinition,
        WorkflowDocument,
    )

from .bindings import BindingMap, StaticBinding
from .dispatch import IncomingValue, RuntimeRegistration, RuntimeTable
from .planner import RUNTIME_TABLE_REVISION
from .run import AttemptResult, run_attempt

BINDING_REVISION = "vidap.reference.bindings.v1"
MINIMUM = -(2**63)
MAXIMUM = 2**63 - 1
_KEYS = (
    "vidap.reference.literal",
    "vidap.reference.multiply",
    "vidap.reference.add",
    "vidap.reference.emit",
)


def _checked(value: object) -> int:
    if type(value) is not int:
        raise TypeError("reference value must be an integer")
    if not MINIMUM <= value <= MAXIMUM:
        raise OverflowError("reference integer exceeds signed 64-bit range")
    return value


def _incoming(
    incoming: tuple[IncomingValue, ...], keys: tuple[str, ...]
) -> dict[str, int]:
    if len(incoming) != len(keys) or {item.target_port_key for item in incoming} != set(
        keys
    ):
        raise ValueError("reference input cardinality is invalid")
    return {item.target_port_key: _checked(item.value) for item in incoming}


def _parameters(
    parameters: Mapping[str, object], keys: tuple[str, ...]
) -> dict[str, int]:
    if set(parameters) != set(keys):
        raise ValueError("reference parameters are invalid")
    return {key: _checked(parameters[key]) for key in keys}


def literal(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    _incoming(incoming, ())
    return {"value": _parameters(parameters, ("value",))["value"]}


def multiply(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    value = _incoming(incoming, ("input",))["input"]
    factor = _parameters(parameters, ("factor",))["factor"]
    return {"value": _checked(value * factor)}


def add(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    values = _incoming(incoming, ("left", "right"))
    _parameters(parameters, ())
    return {"value": _checked(values["left"] + values["right"])}


def emit(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    value = _incoming(incoming, ("input",))["input"]
    _parameters(parameters, ())
    return {"value": value}


def _port(key: str, direction: str) -> PortDefinition:
    return PortDefinition(
        key,
        direction,
        "artifact",
        DisplayMetadata(key.title()),
        cardinality="one" if direction == "input" else None,
        required=True if direction == "input" else None,
    )


def _definition(
    key: str, inputs: tuple[str, ...], parameter: str | None
) -> NodeDefinition:
    return NodeDefinition(
        type_id=key,
        operation_key=key,
        display=DisplayMetadata(key.rsplit(".", 1)[-1].title()),
        inputs=tuple(_port(name, "input") for name in inputs),
        outputs=(_port("value", "output"),),
        parameters=(
            ParameterDefinition(
                parameter,
                "integer",
                True,
                DisplayMetadata(parameter.title()),
                constraints={"minimum": MINIMUM, "maximum": MAXIMUM},
            ),
        )
        if parameter
        else (),
    )


REFERENCE_REGISTRY = NodeRegistry(
    (
        _definition(_KEYS[0], (), "value"),
        _definition(_KEYS[1], ("input",), "factor"),
        _definition(_KEYS[2], ("left", "right"), None),
        _definition(_KEYS[3], ("input",), None),
    )
)
REFERENCE_BINDINGS = BindingMap(
    BINDING_REVISION, tuple(StaticBinding(key, BINDING_REVISION) for key in _KEYS)
)
REFERENCE_RUNTIME_TABLE = RuntimeTable(
    RUNTIME_TABLE_REVISION,
    tuple(
        RuntimeRegistration(key, BINDING_REVISION, handler)
        for key, handler in zip(_KEYS, (literal, multiply, add, emit), strict=True)
    ),
)


def run_reference_attempt(
    document: WorkflowDocument, *, seed: int | None = None
) -> AttemptResult:
    """Run the fixed reference family once through the accepted attempt layer."""

    return run_attempt(
        document,
        REFERENCE_REGISTRY,
        REFERENCE_BINDINGS,
        REFERENCE_RUNTIME_TABLE,
        seed=seed,
        _reference_output=True,
    )
