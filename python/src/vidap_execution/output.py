"""Fixed reference-scalar selection and deterministic owned-slot bytes."""

from __future__ import annotations

import json

from .dispatch import DispatchResult
from .planner import ExecutionPlan

REFERENCE_FORMAT = "vidap.reference-scalar"
REFERENCE_SCHEMA_VERSION = "1.0"
EMIT_KEY = "vidap.reference.emit"
PROOF_SLOT = "proof-output.bin"


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
