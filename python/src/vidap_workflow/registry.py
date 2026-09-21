"""Explicit static first-party node-contract registry values."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType

from .contracts import (
    NOMINAL_TYPE_TOKENS,
    DisplayMetadata,
    NodeDefinition,
    ParameterDefinition,
    PortDefinition,
)


@dataclass(frozen=True, slots=True)
class NodeRegistry:
    """An immutable registry supplied by explicit first-party definitions only."""

    definitions: tuple[NodeDefinition, ...] = ()
    _by_type_id: MappingProxyType[str, NodeDefinition] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        definitions = tuple(self.definitions)
        by_type_id: dict[str, NodeDefinition] = {}
        for definition in definitions:
            if not isinstance(definition, NodeDefinition):
                raise ValueError(
                    "registry definitions must be NodeDefinition values only."
                )
            if definition.type_id in by_type_id:
                raise ValueError("duplicate node type registration is not allowed.")
            by_type_id[definition.type_id] = definition
        object.__setattr__(self, "definitions", definitions)
        object.__setattr__(self, "_by_type_id", MappingProxyType(by_type_id))

    def get(self, type_id: str) -> NodeDefinition | None:
        """Return the declarative definition for an explicit registered type, if any."""

        return self._by_type_id.get(type_id)

    def with_definition(self, definition: NodeDefinition) -> NodeRegistry:
        """Return a new registry after one explicit first-party registration."""

        return NodeRegistry((*self.definitions, definition))


CONTRACT_SOURCE = NodeDefinition(
    type_id="vidap.kernel.contract-source",
    display=DisplayMetadata(
        label="Contract source",
        description="Non-operational specimen for declared output contracts.",
    ),
    outputs=tuple(
        PortDefinition(
            key=token,
            direction="output",
            nominal_type=token,
            display=DisplayMetadata(label=f"{token.title()} output"),
        )
        for token in NOMINAL_TYPE_TOKENS
    ),
)

CONTRACT_SINK = NodeDefinition(
    type_id="vidap.kernel.contract-sink",
    display=DisplayMetadata(
        label="Contract sink",
        description="Non-operational specimen for declared input contracts.",
    ),
    inputs=tuple(
        PortDefinition(
            key=token,
            direction="input",
            nominal_type=token,
            display=DisplayMetadata(label=f"{token.title()} input"),
            cardinality="one",
            required=True,
        )
        for token in NOMINAL_TYPE_TOKENS
    ),
    parameters=(
        ParameterDefinition(
            key="display-mode",
            value_kind="string",
            required=False,
            display=DisplayMetadata(label="Display mode"),
            default="summary",
            constraints={"allowedValues": ("summary", "detail")},
        ),
    ),
)

BUILTIN_NODE_REGISTRY = NodeRegistry((CONTRACT_SOURCE, CONTRACT_SINK))
"""The complete immutable built-in registry: two non-operational specimens."""
