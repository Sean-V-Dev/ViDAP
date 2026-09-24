"""Independent component invalidation and technical sanitization checks."""

from __future__ import annotations

import hashlib
import json

import pytest

from vidap_execution.diagnostics import capture_exception, diagnostic
from vidap_execution.reuse import (
    TrustedValue,
    UnreferencedOutput,
    canonical_json,
    composite_key,
    scalar_ref,
)


@pytest.mark.unit
def test_composite_key_components_invalidate_independently() -> None:
    baseline = {
        "operation_key": "test.op",
        "binding_revision": "r1",
        "parameters": {"value": 1},
        "ordered_input_refs": ("sha256:" + "a" * 64, "sha256:" + "b" * 64),
        "semantic_digest": "c" * 64,
        "seed": None,
        "environment": {"pythonVersion": "3.14.7", "lockSha256": {"uv": "d" * 64}},
    }
    expected = composite_key(**baseline)
    variants = (
        ("operation_key", "test.other"),
        ("binding_revision", "r2"),
        ("parameters", {"value": 2}),
        ("ordered_input_refs", tuple(reversed(baseline["ordered_input_refs"]))),
        ("semantic_digest", "e" * 64),
        ("seed", 0),
        ("environment", {"pythonVersion": "3.14.8", "lockSha256": {"uv": "d" * 64}}),
    )
    for field, changed in variants:
        assert composite_key(**(baseline | {field: changed})) != expected
    assert composite_key(**baseline) == expected
    assert (
        expected
        == hashlib.sha256(
            canonical_json(
                {
                    "revision": "vidap.attempt-output-key/1.0",
                    "operationKey": baseline["operation_key"],
                    "bindingRevision": baseline["binding_revision"],
                    "parameters": baseline["parameters"],
                    "orderedInputRefs": baseline["ordered_input_refs"],
                    "semanticDigest": baseline["semantic_digest"],
                    "seed": baseline["seed"],
                    "environment": baseline["environment"],
                }
            )
        ).hexdigest()
    )


@pytest.mark.unit
def test_canonical_utf16_order_and_scalar_boundaries() -> None:
    astral = "\U00010000"
    bmp = "\ue000"
    encoded = canonical_json({bmp: 1, astral: 2})
    assert list(json.loads(encoded)) == [astral, bmp]
    assert scalar_ref(0) != scalar_ref(None)
    assert scalar_ref(False) != scalar_ref(0)
    with pytest.raises(UnreferencedOutput):
        scalar_ref({"private": "value"})
    with pytest.raises(UnreferencedOutput):
        scalar_ref(2**63)
    with pytest.raises(ValueError):
        TrustedValue(object(), "private")


@pytest.mark.unit
def test_malicious_cause_and_path_never_enter_diagnostic() -> None:
    try:
        try:
            raise ValueError("credential=SECRET C:\\Users\\private\\source.py")
        except ValueError as cause:
            raise RuntimeError("token=SECRET /home/private/source.py") from cause
    except RuntimeError as error:
        context = capture_exception(error)
    item = diagnostic(
        "handler-failed",
        "00000000-0000-4000-8000-000000000000",
        "test.op",
        "node",
        technical=context,
    )
    rendered = repr(item)
    assert "SECRET" not in rendered
    assert "Users" not in rendered
    assert "/home" not in rendered
    assert item.technical.type == "RuntimeError"
    assert item.technical.causes == ("ValueError",)
    assert len(item.technical.traceback) <= 8
