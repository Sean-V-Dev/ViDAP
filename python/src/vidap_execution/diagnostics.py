"""Bounded, non-secret runtime diagnostics for the attempt boundary."""

from __future__ import annotations

import re
import traceback
from dataclasses import dataclass

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z_0-9]{0,79}")


@dataclass(frozen=True, slots=True)
class TechnicalContext:
    type: str | None
    message: str
    traceback: tuple[str, ...]
    causes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RuntimeDiagnostic:
    category: str
    code: str
    attempt_id: str
    operation_key: str | None
    node_id: str | None
    port_key: str | None
    outcome: str
    explanation: str
    remedy: str
    technical: TechnicalContext


def _safe_identifier(value: str) -> str:
    return value if _IDENTIFIER.fullmatch(value) else "UnidentifiedError"


def capture_exception(error: BaseException) -> TechnicalContext:
    """Capture identifiers only; raw exception messages and file paths are untrusted."""

    frames = traceback.extract_tb(error.__traceback__)[-8:]
    safe_frames = tuple(_safe_identifier(frame.name) for frame in frames)
    causes: list[str] = []
    seen: set[int] = {id(error)}
    current = error.__cause__ or error.__context__
    while current is not None and len(causes) < 4 and id(current) not in seen:
        seen.add(id(current))
        causes.append(_safe_identifier(type(current).__name__))
        current = current.__cause__ or current.__context__
    return TechnicalContext(
        _safe_identifier(type(error).__name__),
        "Exception text withheld because it may contain sensitive values.",
        safe_frames,
        tuple(causes),
    )


def diagnostic(
    code: str,
    attempt_id: str,
    operation_key: str | None = None,
    node_id: str | None = None,
    port_key: str | None = None,
    technical: TechnicalContext | None = None,
) -> RuntimeDiagnostic:
    explanations = {
        "handler-failed": (
            "The operation stopped while calculating its result.",
            "Inspect the operation inputs and configuration, then retry a new attempt.",
        ),
        "invalid-handler-output": (
            "The operation returned an invalid output shape.",
            "Correct the first-party handler to return a mapping with text port keys.",
        ),
        "missing-output": (
            "The operation did not return a required connected output.",
            "Correct the first-party handler to return the connected port.",
        ),
        "unreferenced-output": (
            "A result cannot be safely referenced for this attempt.",
            "Return a bounded scalar or an explicitly trusted content reference.",
        ),
        "publication-failed": (
            "The attempt record could not be published safely.",
            "Inspect and explicitly remove the owned pending attempt before retrying.",
        ),
    }
    explanation, remedy = explanations[code]
    return RuntimeDiagnostic(
        "artifact" if code == "publication-failed" else "execution",
        code,
        attempt_id,
        operation_key,
        node_id,
        port_key,
        "failed",
        explanation,
        remedy,
        technical
        or TechnicalContext(None, "No exception context was captured.", (), ()),
    )
