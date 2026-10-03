"""Controlled slice fixture integrity (D0.7) and fail-closed loading."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from slice_fixture_generator import FIXTURE, generate
from test_slice_operations import fixture

from vidap_execution import slice as slice_module
from vidap_execution.artifacts import remove_attempt
from vidap_execution.slice import (
    DATASET_MAX_BYTES,
    DATASET_PATH,
    DATASET_SHA256,
    load_dataset_bytes,
    run_slice_attempt,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "fixtures"
MANIFEST = FIXTURES / "p3-ep03b" / "fixture-manifest.json"


@pytest.fixture
def cleanup() -> Iterator[list[str]]:
    ids: list[str] = []
    root = ROOT / ".vidap-local"
    existed = root.exists()
    yield ids
    for attempt_id in ids:
        remove_attempt(attempt_id)
    if not existed and root.exists():
        (root / "runs").rmdir()
        root.rmdir()


@pytest.mark.unit
def test_generator_reproduces_the_committed_bytes() -> None:
    assert FIXTURE == DATASET_PATH
    data = DATASET_PATH.read_bytes()
    assert generate() == data
    assert hashlib.sha256(data).hexdigest() == DATASET_SHA256
    assert len(data) <= DATASET_MAX_BYTES
    assert b"\r" not in data and data.endswith(b"\n")


@pytest.mark.unit
def test_manifest_matches_every_fixture_and_bounds_hold() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest["fixtures"]
    assert {entry["path"] for entry in entries} == {
        "fixtures/p3-ep03b/slice-dataset-v1.csv",
        "fixtures/p3-ep03b/slice-success-v1.json",
        "fixtures/p3-ep03b/slice-bypass-prepare-v1.json",
    }
    for entry in entries:
        data = (ROOT / entry["path"]).read_bytes()
        assert entry["byteSize"] == len(data) <= 16 * 1024
        assert entry["sha256"] == hashlib.sha256(data).hexdigest().upper()
        assert entry["terms"] == "MIT"
        assert entry["privacyClassification"] == "synthetic non-sensitive"
        assert b"\r" not in data and data.endswith(b"\n")
    table = load_dataset_bytes(DATASET_PATH.read_bytes())
    expected = entries[0]["expectedResult"]
    assert table.row_count == expected["rows"]
    assert sum(1 for v in table.target() if v == 1) == expected["positiveLabels"]
    assert sum(1 for v in table.columns[1] if v is None) == expected["missingFeatureB"]
    labels = list(table.target())
    assert 0.3 <= labels.count(1) / len(labels) <= 0.7
    total = sum(p.stat().st_size for p in FIXTURES.rglob("*") if p.is_file())
    assert total < 64 * 1024
    assert len(MANIFEST.read_bytes()) <= 16 * 1024


@pytest.mark.unit
def test_changed_bytes_fail_closed_before_parsing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data = bytearray(DATASET_PATH.read_bytes())
    data[-3] = ord("1") if data[-3] != ord("1") else ord("0")

    def no_parse(*args: object, **kwargs: object) -> object:
        raise AssertionError("parsed before the integrity check")

    monkeypatch.setattr(slice_module.csv, "reader", no_parse)
    with pytest.raises(ValueError, match="reviewed fixture"):
        load_dataset_bytes(bytes(data))
    with pytest.raises(ValueError, match="size bound"):
        load_dataset_bytes(b"x" * (DATASET_MAX_BYTES + 1))


@pytest.mark.unit
def test_tampered_fixture_fails_the_dataset_node(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    tampered = tmp_path / "slice-dataset-v1.csv"
    tampered.write_bytes(DATASET_PATH.read_bytes().replace(b"north", b"south", 1))
    monkeypatch.setattr(slice_module, "DATASET_PATH", tampered)
    result = run_slice_attempt(fixture("slice-success-v1.json"))
    data = result.record.data
    cleanup.append(str(data["attemptId"]))
    assert data["outcome"] == "failed"
    assert data["failedNodeId"] == "41000000-0000-4000-8000-000000000001"
    assert data["diagnostics"][0]["code"] == "handler-failed"
    assert data["artifacts"] == ("record.json",)
