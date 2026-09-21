"""Controlled-fixture proof for strict 1.0 workflow compatibility."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import pytest

from vidap_workflow import (
    BUILTIN_NODE_REGISTRY,
    deserialize_document,
    serialize_document,
    serialize_semantic_document,
    validate_workflow_text,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIRECTORY = ROOT / "fixtures" / "p1-ep05"
MANIFEST_PATH = FIXTURE_DIRECTORY / "fixture-manifest.json"
PRIVACY_ATTESTATION = (
    "Contains no personal, sensitive, credential, path, network, telemetry, "
    "proprietary, or dataset content."
)
PERMITTED_CONSUMERS = ["P1-EP05 tests", "Phase 1 validation and closeout evidence"]


def _fixture_bytes(name: str) -> bytes:
    return (FIXTURE_DIRECTORY / name).read_bytes()


def _fixture_text(name: str) -> str:
    return _fixture_bytes(name).decode("utf-8")


def _fixture_payload(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads(_fixture_text(name)))


def _codes(text: str) -> tuple[str, ...]:
    return tuple(
        diagnostic.code
        for diagnostic in validate_workflow_text(text, BUILTIN_NODE_REGISTRY)
    )


def _reverse_member_order(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: _reverse_member_order(value[key]) for key in reversed(tuple(value))
        }
    if isinstance(value, list):
        return [_reverse_member_order(item) for item in value]
    return value


@pytest.mark.unit
def test_fixture_manifest_matches_exact_controlled_fixture_bytes() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = manifest["fixtures"]
    assert manifest["fixtureManifestVersion"] == "1.0"
    assert isinstance(entries, list) and len(entries) == 4
    expected_names = {
        "valid-branched-v1.json",
        "invalid-unknown-node-v1.json",
        "invalid-unknown-core-field-v1.json",
        "unsupported-schema-version-v2.json",
    }
    assert {Path(entry["path"]).name for entry in entries} == expected_names

    for entry in entries:
        path = ROOT / entry["path"]
        raw = path.read_bytes()
        assert path.parent == FIXTURE_DIRECTORY
        assert raw.decode("utf-8").encode("utf-8") == raw
        assert entry["byteSize"] == len(raw) < 16 * 1024
        assert entry["sha256"] == hashlib.sha256(raw).hexdigest().upper()
        assert entry["provenance"].startswith("Synthetic workflow text")
        assert entry["terms"] == "MIT"
        assert entry["creationMethod"]
        assert entry["permittedConsumers"] == PERMITTED_CONSUMERS
        assert entry["privacyAttestation"] == PRIVACY_ATTESTATION
        assert entry["centralReviewer"] == "Central"
        assert entry["reviewDate"] == "2026-09-21"
        assert entry["id"].startswith("p1-ep05-")
        assert entry["schemaVersion"] in {"1.0", "2.0"}
        assert isinstance(entry["expectedResult"]["diagnosticCodes"], list)

    aggregate = sum(
        path.stat().st_size for path in ROOT.joinpath("fixtures").rglob("*")
    )
    assert aggregate < 64 * 1024


@pytest.mark.unit
def test_valid_branched_fixture_is_deterministic_and_member_order_invariant() -> None:
    text = _fixture_text("valid-branched-v1.json")
    document = deserialize_document(text)
    member_reordered = json.dumps(_reverse_member_order(json.loads(text)))
    reordered_document = deserialize_document(member_reordered)

    assert validate_workflow_text(text, BUILTIN_NODE_REGISTRY) == ()
    assert validate_workflow_text(member_reordered, BUILTIN_NODE_REGISTRY) == ()
    assert serialize_document(deserialize_document(serialize_document(document))) == (
        serialize_document(document)
    )
    assert serialize_semantic_document(document) == serialize_semantic_document(
        reordered_document
    )
    assert len(document.nodes) == 3
    assert len(document.edges) == 14
    assert sum(edge.source.port_key == "table" for edge in document.edges) == 2


@pytest.mark.unit
@pytest.mark.parametrize(
    ("name", "expected_code", "expected_category"),
    (
        (
            "invalid-unknown-node-v1.json",
            "VIDAP-UNKNOWN-NODE-TYPE",
            "unsupported",
        ),
        (
            "invalid-unknown-core-field-v1.json",
            "VIDAP-UNKNOWN-CORE-FIELD",
            "structural",
        ),
        (
            "unsupported-schema-version-v2.json",
            "VIDAP-UNSUPPORTED-VERSION",
            "unsupported",
        ),
    ),
)
def test_invalid_fixture_results_are_stable_and_actionable(
    name: str, expected_code: str, expected_category: str
) -> None:
    diagnostics = validate_workflow_text(_fixture_text(name), BUILTIN_NODE_REGISTRY)

    assert tuple(diagnostic.code for diagnostic in diagnostics) == (expected_code,)
    assert diagnostics[0].category == expected_category
    assert diagnostics[0].affected_element_reference
    assert diagnostics[0].message and diagnostics[0].remedy
    assert diagnostics[0].technical_detail is None or isinstance(
        diagnostics[0].technical_detail, str
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("mutator", "expected_code"),
    (
        (lambda payload: payload.pop("schemaVersion"), "VIDAP-UNSUPPORTED-VERSION"),
        (
            lambda payload: payload.__setitem__("schemaVersion", 1),
            "VIDAP-UNSUPPORTED-VERSION",
        ),
        (
            lambda payload: payload.__setitem__("schemaVersion", "0.9"),
            "VIDAP-UNSUPPORTED-VERSION",
        ),
        (
            lambda payload: payload.__setitem__("schemaVersion", "2.0"),
            "VIDAP-UNSUPPORTED-VERSION",
        ),
        (
            lambda payload: payload.__setitem__(
                "extensions", {"namespace": "future", "version": "1"}
            ),
            "VIDAP-UNSUPPORTED-EXTENSION",
        ),
    ),
)
def test_missing_malformed_older_future_and_extension_content_fail_visibly(
    mutator: object, expected_code: str
) -> None:
    payload = _fixture_payload("valid-branched-v1.json")
    cast(object, mutator)
    mutator(payload)  # type: ignore[operator]
    diagnostics = validate_workflow_text(json.dumps(payload), BUILTIN_NODE_REGISTRY)

    assert tuple(diagnostic.code for diagnostic in diagnostics) == (expected_code,)
    assert diagnostics[0].category == "unsupported"


@pytest.mark.unit
def test_malformed_json_nonobject_root_and_duplicate_names_are_structural() -> None:
    cases = (
        ("{", "VIDAP-MALFORMED-JSON"),
        ("[]", "VIDAP-NONOBJECT-ROOT"),
        (
            '{"format":"vidap.workflow","format":"vidap.workflow"}',
            "VIDAP-DUPLICATE-OBJECT-NAME",
        ),
    )

    for text, expected_code in cases:
        diagnostics = validate_workflow_text(text, BUILTIN_NODE_REGISTRY)
        assert tuple(diagnostic.code for diagnostic in diagnostics) == (expected_code,)
        assert diagnostics[0].category == "structural"


@pytest.mark.unit
def test_text_boundary_has_no_migration_unknown_preservation_or_io_side_effect() -> (
    None
):
    original = _fixture_text("invalid-unknown-core-field-v1.json")
    registry_before = BUILTIN_NODE_REGISTRY.definitions
    diagnostics = validate_workflow_text(original, BUILTIN_NODE_REGISTRY)
    serialization_source = (
        ROOT / "python/src/vidap_workflow/serialization.py"
    ).read_text(encoding="utf-8")
    validation_source = (ROOT / "python/src/vidap_workflow/validation.py").read_text(
        encoding="utf-8"
    )

    assert original == _fixture_text("invalid-unknown-core-field-v1.json")
    assert BUILTIN_NODE_REGISTRY.definitions == registry_before
    assert tuple(diagnostic.code for diagnostic in diagnostics) == (
        "VIDAP-UNKNOWN-CORE-FIELD",
    )
    source = serialization_source + validation_source
    assert "migration" not in source.lower()
    assert all(
        token not in source
        for token in ("pathlib", "open(", "subprocess", "socket", "urllib", "fastapi")
    )
