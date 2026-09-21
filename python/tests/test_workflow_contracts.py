import builtins
import importlib
import sys
from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from vidap_workflow import (
    BUILTIN_NODE_REGISTRY,
    NOMINAL_TYPE_TOKENS,
    OMITTED_DEFAULT,
    DisplayMetadata,
    NodeDefinition,
    NodeRegistry,
    ParameterDefinition,
    PortDefinition,
)


def _input_port(key: str = "table") -> PortDefinition:
    return PortDefinition(
        key=key,
        direction="input",
        nominal_type="table",
        display=DisplayMetadata(label="Table"),
        cardinality="one",
        required=True,
    )


def _output_port(key: str = "table") -> PortDefinition:
    return PortDefinition(
        key=key,
        direction="output",
        nominal_type="table",
        display=DisplayMetadata(label="Table"),
    )


def _definition(type_id: str = "synthetic.contract") -> NodeDefinition:
    return NodeDefinition(
        type_id=type_id,
        display=DisplayMetadata(label="Synthetic contract"),
        inputs=(_input_port(),),
        outputs=(_output_port("result"),),
    )


@pytest.mark.unit
def test_contract_values_are_immutable_and_preserve_declared_metadata() -> None:
    parameter = ParameterDefinition(
        key="options",
        value_kind="object",
        required=False,
        display=DisplayMetadata(label="Options", description="Synthetic metadata."),
        default={"enabled": True},
        constraints={"properties": {"enabled": "boolean"}},
    )
    definition = NodeDefinition(
        type_id="synthetic.immutable",
        display=DisplayMetadata(label="Immutable"),
        inputs=(_input_port(),),
        parameters=(parameter,),
    )

    assert definition.inputs[0].required is True
    assert parameter.default == {"enabled": True}
    assert parameter.constraints["properties"] == {"enabled": "boolean"}
    assert isinstance(parameter.constraints, MappingProxyType)
    with pytest.raises(FrozenInstanceError):
        definition.type_id = "synthetic.changed"  # type: ignore[misc]
    with pytest.raises(TypeError):
        parameter.constraints["minimum"] = 1  # type: ignore[index]


@pytest.mark.unit
def test_specimens_cover_each_accepted_nominal_token_with_declared_directions() -> None:
    source = BUILTIN_NODE_REGISTRY.get("vidap.kernel.contract-source")
    sink = BUILTIN_NODE_REGISTRY.get("vidap.kernel.contract-sink")

    assert source is not None
    assert sink is not None
    assert tuple(port.nominal_type for port in source.outputs) == NOMINAL_TYPE_TOKENS
    assert tuple(port.nominal_type for port in sink.inputs) == NOMINAL_TYPE_TOKENS
    assert all(port.direction == "output" for port in source.outputs)
    assert all(port.direction == "input" for port in sink.inputs)
    assert {port.cardinality for port in sink.inputs} == {"one"}
    assert all(port.required is not None for port in sink.inputs)


@pytest.mark.unit
def test_parameter_metadata_distinguishes_omission_from_an_explicit_default() -> None:
    omitted = ParameterDefinition(
        key="optional",
        value_kind="null",
        required=False,
        display=DisplayMetadata(label="Optional"),
    )
    declared = ParameterDefinition(
        key="selection",
        value_kind="array",
        required=True,
        display=DisplayMetadata(label="Selection"),
        default=[],
        constraints={"itemKinds": ["string"], "minItems": 0},
    )

    assert omitted.default is OMITTED_DEFAULT
    assert declared.default == ()
    assert declared.required is True
    assert declared.constraints["itemKinds"] == ("string",)

    many_input = PortDefinition(
        key="tables",
        direction="input",
        nominal_type="table",
        display=DisplayMetadata(label="Tables"),
        cardinality="many",
        required=False,
    )
    assert many_input.cardinality == "many"


@pytest.mark.unit
@pytest.mark.parametrize(
    "type_id",
    ("contract", "Synthetic.contract", "synthetic..contract", "synthetic.contract!"),
)
def test_malformed_node_type_ids_fail_at_definition_time(type_id: str) -> None:
    with pytest.raises(ValueError, match="type_id"):
        _definition(type_id)


@pytest.mark.unit
def test_duplicate_port_and_parameter_keys_fail_at_definition_time() -> None:
    duplicate_parameter = ParameterDefinition(
        key="mode",
        value_kind="string",
        required=False,
        display=DisplayMetadata(label="Mode"),
    )

    with pytest.raises(ValueError, match="port keys"):
        NodeDefinition(
            type_id="synthetic.duplicate-port",
            display=DisplayMetadata(label="Duplicate port"),
            inputs=(_input_port("shared"),),
            outputs=(_output_port("shared"),),
        )
    with pytest.raises(ValueError, match="parameter keys"):
        NodeDefinition(
            type_id="synthetic.duplicate-parameter",
            display=DisplayMetadata(label="Duplicate parameter"),
            parameters=(duplicate_parameter, duplicate_parameter),
        )


@pytest.mark.unit
def test_registry_rejects_duplicate_registration_and_adds_functionally() -> None:
    original = NodeRegistry((_definition(),))
    added = original.with_definition(_definition("synthetic.additional"))

    assert original.get("synthetic.additional") is None
    assert added.get("synthetic.additional") == _definition("synthetic.additional")
    with pytest.raises(ValueError, match="duplicate node type registration"):
        original.with_definition(_definition())


@pytest.mark.unit
def test_built_in_registry_contains_exactly_two_non_operational_definitions() -> None:
    assert tuple(
        definition.type_id for definition in BUILTIN_NODE_REGISTRY.definitions
    ) == (
        "vidap.kernel.contract-source",
        "vidap.kernel.contract-sink",
    )
    assert all(
        definition.operation_key is None
        for definition in BUILTIN_NODE_REGISTRY.definitions
    )


@pytest.mark.unit
def test_public_import_does_not_import_forbidden_consumers_or_discovery_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    forbidden_roots = {
        "fastapi",
        "http",
        "importlib",
        "os",
        "pathlib",
        "pkgutil",
        "socket",
        "subprocess",
        "urllib",
        "uvicorn",
        "vidap_execution",
        "vidap_experiments",
        "vidap_export",
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

    assert imported.NodeRegistry.__name__ == "NodeRegistry"
    assert imported.BUILTIN_NODE_REGISTRY is not None
