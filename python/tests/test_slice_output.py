"""Slice-metrics bytes (F1) and the P2-EP05 publication challenges."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from test_slice_operations import expected_metrics, fixture

from vidap_execution import run as run_module
from vidap_execution import run_attempt
from vidap_execution.artifacts import (
    ArtifactRefusal,
    _directory,
    read_record,
    remove_attempt,
)
from vidap_execution.output import ReferenceOutputRefusal, SliceMetrics, metrics_bytes
from vidap_execution.reference import (
    REFERENCE_BINDINGS,
    REFERENCE_REGISTRY,
    REFERENCE_RUNTIME_TABLE,
)
from vidap_execution.run import AttemptRefusal, PublicationIndeterminate
from vidap_execution.slice import (
    SLICE_BINDINGS,
    SLICE_REGISTRY,
    SLICE_RUNTIME_TABLE,
    run_slice_attempt,
)

ROOT = Path(__file__).resolve().parents[2]


def expected_bytes() -> bytes:
    return json.dumps(expected_metrics(), separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


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
def test_exact_versioned_bytes() -> None:
    assert metrics_bytes(SliceMetrics(0.9, 36, 40)) == (
        b'{"accuracy":0.9,"correct":36,"format":"vidap.slice-metrics",'
        b'"schemaVersion":"1.0","testRows":40}'
    )
    for bad in (
        (0.5, 36, 40),
        (0.9, 36.0, 40),
        (1, 40, 40),
        (float("nan"), 0, 40),
        (0.0, 0, 0),
        (1.25, 50, 40),
        (True, 1, 1),
    ):
        with pytest.raises(ReferenceOutputRefusal):
            SliceMetrics(*bad)  # type: ignore[arg-type]
    for value in (0.9, {"accuracy": 0.9}, 36):
        with pytest.raises(ReferenceOutputRefusal):
            metrics_bytes(value)


@pytest.mark.unit
def test_output_authority_is_fixed_and_exclusive() -> None:
    doc = fixture("slice-success-v1.json")
    with pytest.raises(AttemptRefusal):
        run_attempt(
            doc,
            REFERENCE_REGISTRY,
            REFERENCE_BINDINGS,
            REFERENCE_RUNTIME_TABLE,
            _slice_output=True,
        )
    with pytest.raises(AttemptRefusal):
        run_attempt(
            doc,
            SLICE_REGISTRY,
            SLICE_BINDINGS,
            SLICE_RUNTIME_TABLE,
            _reference_output=True,
            _slice_output=True,
        )


@pytest.mark.unit
def test_generic_entry_publishes_no_metrics(cleanup: list[str]) -> None:
    result = run_attempt(
        fixture("slice-success-v1.json"),
        SLICE_REGISTRY,
        SLICE_BINDINGS,
        SLICE_RUNTIME_TABLE,
    )
    attempt_id = str(result.record.data["attemptId"])
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "succeeded"
    assert {p.name for p in _directory(attempt_id).iterdir()} == {"record.json"}


@pytest.mark.unit
def test_pre_commit_failures_never_look_successful(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture("slice-success-v1.json")
    keeper = run_slice_attempt(doc)
    keeper_id = str(keeper.record.data["attemptId"])
    cleanup.append(keeper_id)
    original_write = run_module.write_proof_slot

    def fail_write(attempt_id: str, data: bytes) -> None:
        raise OSError("private write failure")

    monkeypatch.setattr(run_module, "write_proof_slot", fail_write)
    failed_write = run_slice_attempt(doc)
    write_id = str(failed_write.record.data["attemptId"])
    cleanup.append(write_id)
    assert failed_write.record.data["outcome"] == "failed"
    assert failed_write.record.data["diagnostics"][0]["code"] == "publication-failed"
    assert {p.name for p in _directory(write_id).iterdir()} == {"record.json"}
    assert b"private" not in (_directory(write_id) / "record.json").read_bytes()
    monkeypatch.setattr(run_module, "write_proof_slot", original_write)

    def fail_terminal(attempt_id: str, record: dict[str, Any]) -> None:
        raise OSError("private terminal failure")

    monkeypatch.setattr(run_module, "publish_terminal", fail_terminal)
    failed_terminal = run_slice_attempt(doc)
    terminal_id = str(failed_terminal.record.data["attemptId"])
    cleanup.append(terminal_id)
    assert failed_terminal.record.data["outcome"] == "failed"
    assert failed_terminal.record.data["publication"] == "failed-pending"
    assert read_record(terminal_id)["state"] == "pending"
    assert {p.name for p in _directory(terminal_id).iterdir()} == {"record.json"}
    assert (_directory(keeper_id) / "proof-output.bin").read_bytes() == expected_bytes()


@pytest.mark.unit
def test_post_commit_error_reports_the_verified_commit(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original = run_module.publish_terminal

    def publish_then_fail(attempt_id: str, record: dict[str, Any]) -> None:
        original(attempt_id, record)
        raise OSError("private post-write failure")

    monkeypatch.setattr(run_module, "publish_terminal", publish_then_fail)
    result = run_slice_attempt(fixture("slice-success-v1.json"))
    attempt_id = str(result.record.data["attemptId"])
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "succeeded"
    assert result.record.data["diagnostics"] == ()
    assert read_record(attempt_id)["state"] == "succeeded"
    assert (
        _directory(attempt_id) / "proof-output.bin"
    ).read_bytes() == expected_bytes()


@pytest.mark.unit
def test_unverifiable_commit_is_indeterminate_and_kept(
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
            run_slice_attempt(fixture("slice-success-v1.json"))
    attempt_id = error.value.attempt_id
    cleanup.append(attempt_id)
    assert "private" not in str(error.value)
    assert read_record(attempt_id)["state"] == "succeeded"
    assert (
        _directory(attempt_id) / "proof-output.bin"
    ).read_bytes() == expected_bytes()


@pytest.mark.unit
def test_failed_slice_publishes_no_metrics(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original = run_module.publish_terminal

    def publish_then_fail(attempt_id: str, record: dict[str, Any]) -> None:
        original(attempt_id, record)
        raise OSError("private post-write failure")

    monkeypatch.setattr(run_module, "publish_terminal", publish_then_fail)
    result = run_slice_attempt(fixture("slice-bypass-prepare-v1.json"))
    attempt_id = str(result.record.data["attemptId"])
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "failed"
    assert read_record(attempt_id)["outcome"] == "failed"
    assert {p.name for p in _directory(attempt_id).iterdir()} == {"record.json"}


@pytest.mark.unit
def test_mismatched_readback_is_indeterminate_and_kept(
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
            run_slice_attempt(fixture("slice-success-v1.json"))
    attempt_id = error.value.attempt_id
    cleanup.append(attempt_id)
    assert "private" not in str(error.value)
    assert read_record(attempt_id)["state"] == "succeeded"
    assert (
        _directory(attempt_id) / "proof-output.bin"
    ).read_bytes() == expected_bytes()


@pytest.mark.unit
def test_rollback_failure_stays_pending_and_reports_it(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_terminal(_attempt_id: str, _record: dict[str, Any]) -> None:
        raise OSError("private pre-commit failure")

    def fail_rollback(_attempt_id: str) -> None:
        raise ArtifactRefusal("private rollback failure")

    with monkeypatch.context() as patcher:
        patcher.setattr(run_module, "publish_terminal", fail_terminal)
        patcher.setattr(run_module, "rollback_unpublished", fail_rollback)
        result = run_slice_attempt(fixture("slice-success-v1.json"))
    attempt_id = str(result.record.data["attemptId"])
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "failed"
    assert result.record.data["publication"] == "failed-cleanup-incomplete"
    assert result.record.data["artifacts"] == ()
    assert read_record(attempt_id)["state"] == "pending"
    assert read_record(attempt_id)["artifacts"] == []


@pytest.mark.unit
def test_partial_proof_write_is_never_success(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original = run_module.write_proof_slot

    def write_then_fail(attempt_id: str, data: bytes) -> None:
        original(attempt_id, data)
        raise OSError("private after-write failure")

    monkeypatch.setattr(run_module, "write_proof_slot", write_then_fail)
    result = run_slice_attempt(fixture("slice-success-v1.json"))
    attempt_id = str(result.record.data["attemptId"])
    cleanup.append(attempt_id)
    assert result.record.data["outcome"] == "failed"
    assert result.record.data["diagnostics"][0]["code"] == "publication-failed"
    assert result.record.data["artifacts"] == ("record.json",)
    assert {p.name for p in _directory(attempt_id).iterdir()} == {"record.json"}
    assert read_record(attempt_id)["state"] == "failed"
