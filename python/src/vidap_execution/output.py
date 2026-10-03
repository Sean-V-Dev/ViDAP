"""Fixed first-party output selection and deterministic owned-slot bytes."""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import isfinite

from .dispatch import DispatchResult
from .planner import ExecutionPlan

REFERENCE_FORMAT = "vidap.reference-scalar"
REFERENCE_SCHEMA_VERSION = "1.0"
EMIT_KEY = "vidap.reference.emit"
PROOF_SLOT = "proof-output.bin"
METRICS_FORMAT = "vidap.slice-metrics"
METRICS_SCHEMA_VERSION = "1.0"
EVALUATE_KEY = "vidap.slice.evaluate"


class ReferenceOutputRefusal(ValueError):
    """The fixed reference result cannot be published."""


def emit_node_id(plan: ExecutionPlan) -> str:
    """Require one terminal emit in the already validated plan."""

    emits = [
        node.node_id
        for node in plan.representation.nodes
        if node.operation_key == EMIT_KEY
    ]
    if len(emits) != 1:
        raise ReferenceOutputRefusal("reference workflow requires exactly one emit")
    if any(edge.source_node_id == emits[0] for edge in plan.representation.edges):
        raise ReferenceOutputRefusal("reference emit must be terminal")
    return emits[0]


def scalar_bytes(value: object) -> bytes:
    """Serialize only a checked signed integer with UTF-16 key ordering."""

    if type(value) is not int or not -(2**63) <= value < 2**63:
        raise ReferenceOutputRefusal(
            "reference emit value is not a signed 64-bit integer"
        )
    payload = {
        "format": REFERENCE_FORMAT,
        "schemaVersion": REFERENCE_SCHEMA_VERSION,
        "value": value,
    }
    # These fixed ASCII keys are already in UTF-16 code-unit order.
    return json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def selected_bytes(plan: ExecutionPlan, result: DispatchResult, node_id: str) -> bytes:
    if result.stop_reason is not None or node_id != emit_node_id(plan):
        raise ReferenceOutputRefusal(
            "reference output requires successful terminal emit"
        )
    try:
        value = result.port_results[(node_id, "value")]
    except KeyError as error:
        raise ReferenceOutputRefusal("reference emit output is missing") from error
    return scalar_bytes(value)


@dataclass(frozen=True, slots=True)
class SliceMetrics:
    """The slice's recorded evaluation result; the accuracy follows the counts."""

    accuracy: float
    correct: int
    test_rows: int

    def __post_init__(self) -> None:
        if (
            type(self.correct) is not int
            or type(self.test_rows) is not int
            or not 0 < self.test_rows < 2**63
            or not 0 <= self.correct <= self.test_rows
        ):
            raise ReferenceOutputRefusal("slice metrics counts are invalid")
        if (
            type(self.accuracy) is not float
            or not isfinite(self.accuracy)
            or self.accuracy != self.correct / self.test_rows
        ):
            raise ReferenceOutputRefusal("slice accuracy disagrees with its counts")

    def payload(self) -> dict[str, object]:
        return {
            "accuracy": self.accuracy,
            "correct": self.correct,
            "testRows": self.test_rows,
        }


def evaluate_node_id(plan: ExecutionPlan) -> str:
    """Require one terminal Evaluate node in the already validated plan."""

    nodes = [
        node.node_id
        for node in plan.representation.nodes
        if node.operation_key == EVALUATE_KEY
    ]
    if len(nodes) != 1:
        raise ReferenceOutputRefusal("slice workflow requires exactly one evaluate")
    if any(edge.source_node_id == nodes[0] for edge in plan.representation.edges):
        raise ReferenceOutputRefusal("slice evaluate must be terminal")
    return nodes[0]


def metrics_bytes(value: object) -> bytes:
    """Serialize only checked slice metrics with UTF-16 key ordering."""

    if not isinstance(value, SliceMetrics):
        raise ReferenceOutputRefusal("slice evaluate value is not slice metrics")
    payload = {
        "format": METRICS_FORMAT,
        "schemaVersion": METRICS_SCHEMA_VERSION,
        **value.payload(),
    }
    # These fixed ASCII keys are already in UTF-16 code-unit order.
    return json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def selected_metrics_bytes(
    plan: ExecutionPlan, result: DispatchResult, node_id: str
) -> bytes:
    if result.stop_reason is not None or node_id != evaluate_node_id(plan):
        raise ReferenceOutputRefusal("slice output requires successful evaluate")
    try:
        value = result.port_results[(node_id, "metrics")]
    except KeyError as error:
        raise ReferenceOutputRefusal("slice evaluate output is missing") from error
    return metrics_bytes(value)
