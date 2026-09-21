"""Immutable, actionable validation diagnostics for workflow instances."""

from __future__ import annotations

from dataclasses import dataclass

DIAGNOSTIC_SEVERITIES = ("error", "warning")
DIAGNOSTIC_CATEGORIES = ("structural", "semantic", "unsupported")

DUPLICATE_NODE_ID = "VIDAP-DUPLICATE-NODE-ID"
DUPLICATE_EDGE_ID = "VIDAP-DUPLICATE-EDGE-ID"
DUPLICATE_EXACT_EDGE = "VIDAP-DUPLICATE-EXACT-EDGE"
UNKNOWN_NODE_TYPE = "VIDAP-UNKNOWN-NODE-TYPE"
UNSUPPORTED_PARAMETER_CONSTRAINT = "VIDAP-UNSUPPORTED-PARAMETER-CONSTRAINT"
DANGLING_NODE = "VIDAP-DANGLING-NODE"
UNKNOWN_PORT = "VIDAP-UNKNOWN-PORT"
REVERSED_DIRECTION = "VIDAP-REVERSED-DIRECTION"
NOMINAL_TYPE_MISMATCH = "VIDAP-NOMINAL-TYPE-MISMATCH"
INPUT_CARDINALITY_EXCEEDED = "VIDAP-INPUT-CARDINALITY-EXCEEDED"
MISSING_REQUIRED_INPUT = "VIDAP-MISSING-REQUIRED-INPUT"
UNKNOWN_PARAMETER = "VIDAP-UNKNOWN-PARAMETER"
MISSING_REQUIRED_PARAMETER = "VIDAP-MISSING-REQUIRED-PARAMETER"
PARAMETER_KIND_MISMATCH = "VIDAP-PARAMETER-KIND-MISMATCH"
PARAMETER_CONSTRAINT_VIOLATION = "VIDAP-PARAMETER-CONSTRAINT-VIOLATION"
DIRECTED_CYCLE = "VIDAP-DIRECTED-CYCLE"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """One stable, user-actionable finding; optional detail is non-contract aid."""

    code: str
    severity: str
    category: str
    affected_element_kind: str
    affected_element_reference: str
    message: str
    remedy: str
    json_pointer: str | None = None
    technical_detail: str | None = None

    def __post_init__(self) -> None:
        if not self.code.startswith("VIDAP-"):
            raise ValueError("diagnostic codes must start with 'VIDAP-'.")
        if self.severity not in DIAGNOSTIC_SEVERITIES:
            raise ValueError("diagnostic severity is not supported.")
        if self.category not in DIAGNOSTIC_CATEGORIES:
            raise ValueError("diagnostic category is not supported.")
        for name in (
            "affected_element_kind",
            "affected_element_reference",
            "message",
            "remedy",
        ):
            if not getattr(self, name):
                raise ValueError(f"diagnostic {name} must not be empty.")
