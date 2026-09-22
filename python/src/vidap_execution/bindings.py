"""Explicit, immutable binding identifiers without executable targets."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from types import MappingProxyType

_KEY = re.compile(r"[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)*")
_REVISION = re.compile(r"[a-z0-9][a-z0-9._-]*")


def _identifier(value: object, name: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise ValueError(f"{name} must be a non-empty static identifier.")
    return value


@dataclass(frozen=True, slots=True)
class StaticBinding:
    """Opaque operation key and revision; neither identifies executable code."""

    operation_key: str
    revision: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "operation_key",
            _identifier(self.operation_key, "operation key", _KEY),
        )
        object.__setattr__(
            self, "revision", _identifier(self.revision, "binding revision", _REVISION)
        )


@dataclass(frozen=True, slots=True)
class BindingMap:
    """A caller-supplied static collection with exact lookup and no discovery."""

    revision: str
    bindings: tuple[StaticBinding, ...] = ()
    _by_key: MappingProxyType[str, StaticBinding] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "revision", _identifier(self.revision, "binding revision", _REVISION)
        )
        bindings = tuple(self.bindings)
        by_key: dict[str, StaticBinding] = {}
        for binding in bindings:
            if not isinstance(binding, StaticBinding):
                raise ValueError("bindings must contain StaticBinding values only.")
            if binding.operation_key in by_key:
                raise ValueError("duplicate operation binding is not allowed.")
            by_key[binding.operation_key] = binding
        object.__setattr__(
            self, "bindings", tuple(sorted(bindings, key=lambda b: b.operation_key))
        )
        object.__setattr__(self, "_by_key", MappingProxyType(by_key))

    def get(self, operation_key: str) -> StaticBinding | None:
        """Return only an explicitly supplied key; never discover a target."""

        return self._by_key.get(operation_key)
