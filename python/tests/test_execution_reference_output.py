"""Versioned bytes and fixed Windows-owned publication challenges."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from vidap_execution import run as run_module
from vidap_execution import run_reference_attempt
from vidap_execution.artifacts import (
    ArtifactRefusal,
    _directory,
    read_record,
    remove_attempt,
    write_proof_slot,
)
from vidap_execution.output import ReferenceOutputRefusal, scalar_bytes
from vidap_execution.run import PublicationIndeterminate
from vidap_workflow import deserialize_document

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = b'{"format":"vidap.reference-scalar","schemaVersion":"1.0","value":15}'


def _fixture(name: str):
    return deserialize_document(
        (ROOT / "fixtures" / "p2-ep05" / name).read_text(encoding="utf-8")
    )


@pytest.fixture
def cleanup() -> list[str]:
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
def test_exact_owned_bytes_and_repeat(cleanup: list[str]) -> None:
    doc = _fixture("branched-success-v1.json")
    first = run_reference_attempt(doc)
    second = run_reference_attempt(doc)
    ids = [first.record.data["attemptId"], second.record.data["attemptId"]]
    cleanup.extend(ids)
    assert ids[0] != ids[1]
    for attempt_id in ids:
        directory = _directory(attempt_id)
        assert {p.name for p in directory.iterdir()} == {
            "record.json",
            "proof-output.bin",
        }
        assert (directory / "proof-output.bin").read_bytes() == EXPECTED
        assert read_record(attempt_id)["artifacts"] == [
            "record.json",
            "proof-output.bin",
        ]
    assert first.record.data["startedAt"] != second.record.data["startedAt"]
    assert first.record.data["semanticDigest"] == second.record.data["semanticDigest"]


@pytest.mark.unit
def test_serializer_refuses_noninteger_and_overflow() -> None:
    assert scalar_bytes(15) == EXPECTED
    assert scalar_bytes(-(2**63)).endswith(b'"value":-9223372036854775808}')
    for value in (True, 1.0, "15", 2**63):
        with pytest.raises(ReferenceOutputRefusal):
            scalar_bytes(value)


@pytest.mark.unit
def test_write_and_terminal_failure_are_bounded(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = _fixture("branched-success-v1.json")
    keeper = run_reference_attempt(doc)
    keeper_id = keeper.record.data["attemptId"]
    cleanup.append(keeper_id)
    original_write = run_module.write_proof_slot

    def fail_write(attempt_id: str, data: bytes) -> None:
        raise OSError("private write failure")

    monkeypatch.setattr(run_module, "write_proof_slot", fail_write)
    failed_write = run_reference_attempt(doc)
    write_id = failed_write.record.data["attemptId"]
    cleanup.append(write_id)
    assert failed_write.record.data["outcome"] == "failed"
    assert failed_write.record.data["diagnostics"][0]["code"] == "publication-failed"
    assert {p.name for p in _directory(write_id).iterdir()} == {"record.json"}
    assert read_record(write_id)["artifacts"] == ["record.json"]
    assert b"private" not in (_directory(write_id) / "record.json").read_bytes()
    monkeypatch.setattr(run_module, "write_proof_slot", original_write)

    def fail_terminal(attempt_id: str, record: dict[str, Any]) -> None:
        raise OSError("private terminal failure")

    monkeypatch.setattr(run_module, "publish_terminal", fail_terminal)
    failed_terminal = run_reference_attempt(doc)
    terminal_id = failed_terminal.record.data["attemptId"]
    cleanup.append(terminal_id)
    assert failed_terminal.record.data["outcome"] == "failed"
    assert failed_terminal.record.data["publication"] == "failed-pending"
    assert {p.name for p in _directory(terminal_id).iterdir()} == {"record.json"}
    assert read_record(terminal_id)["state"] == "pending"
    assert (_directory(keeper_id) / "proof-output.bin").read_bytes() == EXPECTED


@pytest.mark.unit
def test_terminal_write_then_error_reports_immutable_commit(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = _fixture("branched-success-v1.json")
    keeper = run_reference_attempt(doc)
    keeper_id = keeper.record.data["attemptId"]
    cleanup.append(keeper_id)
    original = run_module.publish_terminal

    def publish_then_fail(attempt_id: str, record: dict[str, Any]) -> None:
        original(attempt_id, record)
        assert read_record(attempt_id)["state"] == "succeeded"
        raise OSError("private post-write failure")

    monkeypatch.setattr(run_module, "publish_terminal", publish_then_fail)
    result = run_reference_attempt(doc)
    attempt_id = result.record.data["attemptId"]
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "succeeded"
    assert result.record.data["publication"] == "published"
    assert result.record.data["artifacts"] == ("record.json", "proof-output.bin")
    assert result.record.data["diagnostics"] == ()
    recorded = read_record(attempt_id)
    assert recorded["state"] == "succeeded"
    assert recorded["artifacts"] == ["record.json", "proof-output.bin"]
    assert (_directory(attempt_id) / "proof-output.bin").read_bytes() == EXPECTED
    assert (_directory(keeper_id) / "proof-output.bin").read_bytes() == EXPECTED


@pytest.mark.unit
def test_failed_operation_commit_keeps_immutable_failed_record(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original = run_module.publish_terminal

    def publish_then_fail(attempt_id: str, record: dict[str, Any]) -> None:
        original(attempt_id, record)
        raise OSError("private post-write failure")

    monkeypatch.setattr(run_module, "publish_terminal", publish_then_fail)
    result = run_reference_attempt(_fixture("checked-overflow-v1.json"))
    attempt_id = result.record.data["attemptId"]
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "failed"
    assert result.record.data["diagnostics"][0]["code"] == "handler-failed"
    assert read_record(attempt_id)["outcome"] == "failed"
    assert {path.name for path in _directory(attempt_id).iterdir()} == {"record.json"}


@pytest.mark.unit
def test_post_commit_readback_failure_is_indeterminate_and_non_destructive(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original_publish = run_module.publish_terminal
    original_read = Path.read_bytes
    after_write = False

    def publish_then_fail(attempt_id: str, record: dict[str, Any]) -> None:
        nonlocal after_write
        original_publish(attempt_id, record)
        after_write = True
        raise OSError("private post-write failure")

    def fail_readback(path: Path) -> bytes:
        if after_write and path.name == "record.json":
            raise OSError("private readback failure")
        return original_read(path)

    with monkeypatch.context() as patcher:
        patcher.setattr(run_module, "publish_terminal", publish_then_fail)
        patcher.setattr(Path, "read_bytes", fail_readback)
        with pytest.raises(PublicationIndeterminate) as error:
            run_reference_attempt(_fixture("branched-success-v1.json"))
    attempt_id = error.value.attempt_id
    cleanup.append(attempt_id)
    assert "private" not in str(error.value)
    assert read_record(attempt_id)["state"] == "succeeded"
    assert read_record(attempt_id)["artifacts"] == ["record.json", "proof-output.bin"]
    assert (_directory(attempt_id) / "proof-output.bin").read_bytes() == EXPECTED


@pytest.mark.unit
def test_mismatched_readback_is_indeterminate_without_rewriting_terminal(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original_publish = run_module.publish_terminal
    original_read = Path.read_bytes
    after_write = False

    def publish_then_fail(attempt_id: str, record: dict[str, Any]) -> None:
        nonlocal after_write
        original_publish(attempt_id, record)
        after_write = True
        raise OSError("private post-write failure")

    def mismatch(path: Path) -> bytes:
        if after_write and path.name == "proof-output.bin":
            return b"mismatched readback bytes"
        return original_read(path)

    with monkeypatch.context() as patcher:
        patcher.setattr(run_module, "publish_terminal", publish_then_fail)
        patcher.setattr(Path, "read_bytes", mismatch)
        with pytest.raises(PublicationIndeterminate) as error:
            run_reference_attempt(_fixture("branched-success-v1.json"))
    attempt_id = error.value.attempt_id
    cleanup.append(attempt_id)
    assert read_record(attempt_id)["state"] == "succeeded"
    assert (_directory(attempt_id) / "proof-output.bin").read_bytes() == EXPECTED


@pytest.mark.unit
def test_pre_commit_rollback_failure_stays_pending(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_terminal(_attempt_id: str, _record: dict[str, Any]) -> None:
        raise OSError("private pre-commit failure")

    def fail_rollback(_attempt_id: str) -> None:
        raise ArtifactRefusal("private rollback failure")

    with monkeypatch.context() as patcher:
        patcher.setattr(run_module, "publish_terminal", fail_terminal)
        patcher.setattr(run_module, "rollback_unpublished", fail_rollback)
        result = run_reference_attempt(_fixture("branched-success-v1.json"))
    attempt_id = result.record.data["attemptId"]
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "failed"
    assert result.record.data["publication"] == "failed-cleanup-incomplete"
    assert read_record(attempt_id)["state"] == "pending"
    assert read_record(attempt_id)["artifacts"] == []
    assert (_directory(attempt_id) / "proof-output.bin").read_bytes() == EXPECTED


@pytest.mark.unit
def test_partial_proof_write_is_rolled_back(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original = run_module.write_proof_slot

    def write_then_fail(attempt_id: str, data: bytes) -> None:
        original(attempt_id, data)
        raise OSError("private after-write failure")

    monkeypatch.setattr(run_module, "write_proof_slot", write_then_fail)
    result = run_reference_attempt(_fixture("branched-success-v1.json"))
    attempt_id = result.record.data["attemptId"]
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "failed"
    assert result.record.data["artifacts"] == ("record.json",)
    assert {p.name for p in _directory(attempt_id).iterdir()} == {"record.json"}


@pytest.mark.unit
def test_owned_slot_refuses_overwrite(cleanup: list[str]) -> None:
    doc = _fixture("branched-success-v1.json")
    result = run_reference_attempt(doc)
    attempt_id = result.record.data["attemptId"]
    cleanup.append(attempt_id)
    with pytest.raises(ArtifactRefusal):
        write_proof_slot(attempt_id, b"replacement")
    assert (_directory(attempt_id) / "proof-output.bin").read_bytes() == EXPECTED


@pytest.mark.unit
def test_fixture_integrity_and_policy() -> None:
    manifest_path = ROOT / "fixtures" / "p2-ep05" / "fixture-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_path.read_bytes().endswith(b"\n")
    assert len(manifest["fixtures"]) == 2
    total = len(manifest_path.read_bytes())
    for item in manifest["fixtures"]:
        path = ROOT / item["path"]
        raw = path.read_bytes()
        total += len(raw)
        assert raw.endswith(b"\n") and len(raw) < 16 * 1024
        assert len(raw) == item["byteSize"]
        assert hashlib.sha256(raw).hexdigest().upper() == item["sha256"]
        assert item["terms"] == "MIT" and "Synthetic" in item["provenance"]
        assert item["privacyClassification"] == "synthetic non-sensitive"
        assert item["reviewDate"] == "2026-09-25"
        assert "pending" in item["byteReviewStatus"]
        assert item["permittedConsumers"] == [
            "P2-EP05 tests",
            "later Phase 2 validation and closeout",
        ]
        assert "no personal" in item["privacyAttestation"]
    assert total < 64 * 1024
    assert (
        sum(
            path.stat().st_size
            for path in (ROOT / "fixtures").rglob("*.*")
            if path.is_file()
        )
        < 64 * 1024
    )
