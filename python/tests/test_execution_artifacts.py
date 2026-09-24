"""Owned fixed slots, publication, collision, and removal challenges."""

from __future__ import annotations

import json
import os
import stat
import time
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest

from vidap_execution import artifacts


@pytest.fixture
def owned() -> list[str]:
    ids: list[str] = []
    root = Path(__file__).resolve().parents[2] / ".vidap-local"
    existed = root.exists()
    yield ids
    for attempt_id in ids:
        artifacts.remove_attempt(attempt_id)
    if not existed and root.exists():
        # Windows can keep a handle-disposed child visible to the parent briefly.
        for retry in range(50):
            try:
                (root / "runs").rmdir()
                break
            except OSError:
                if retry == 49:
                    raise
                time.sleep(0.02)
        root.rmdir()


def _id() -> str:
    return str(uuid.uuid4())


def _terminal(attempt_id: str, artifacts_list: list[str]) -> dict[str, object]:
    return {
        "format": "vidap.attempt-ownership/1.0",
        "attemptId": attempt_id,
        "state": "succeeded",
        "ownedSlots": sorted(artifacts._SLOTS),
        "artifacts": artifacts_list,
    }


@pytest.mark.unit
def test_pending_proof_terminal_and_recorded_cleanup(owned: list[str]) -> None:
    first, second = _id(), _id()
    for attempt_id in (first, second):
        artifacts.begin_attempt(attempt_id)
        owned.append(attempt_id)
    assert artifacts.read_record(first)["state"] == "pending"
    artifacts.write_proof_slot(first, b"synthetic")
    artifacts.publish_terminal(
        first, _terminal(first, ["record.json", "proof-output.bin"])
    )
    assert artifacts.read_record(first)["state"] == "succeeded"
    directory = artifacts._directory(first)
    assert (directory / "proof-output.bin").read_bytes() == b"synthetic"
    assert not list(directory.glob("*.tmp"))
    (directory / "unexpected").write_text("owned by test", encoding="utf-8")
    with pytest.raises(artifacts.ArtifactRefusal):
        artifacts.remove_attempt(first)
    assert artifacts.read_record(second)["state"] == "pending"
    (directory / "unexpected").unlink()
    artifacts.remove_attempt(first)
    owned.remove(first)
    assert artifacts.read_record(second)["state"] == "pending"


@pytest.mark.unit
def test_collision_bounds_and_format_refusal(owned: list[str]) -> None:
    attempt_id = _id()
    artifacts.begin_attempt(attempt_id)
    owned.append(attempt_id)
    with pytest.raises(FileExistsError):
        artifacts.begin_attempt(attempt_id)
    with pytest.raises(artifacts.ArtifactRefusal):
        artifacts.write_proof_slot(attempt_id, b"x" * (64 * 1024 + 1))
    with pytest.raises(artifacts.ArtifactRefusal):
        artifacts.write_proof_slot(attempt_id, "text")  # type: ignore[arg-type]
    with pytest.raises(artifacts.ArtifactRefusal):
        artifacts.publish_terminal(
            attempt_id, _terminal(attempt_id, ["proof-output.bin"])
        )
    assert artifacts.read_record(attempt_id)["state"] == "pending"
    with pytest.raises(artifacts.ArtifactRefusal):
        artifacts.remove_attempt("../other")


@pytest.mark.unit
@pytest.mark.parametrize("failure_stage", ["creation", "post-creation-check"])
def test_initial_directory_handle_refusal_leaves_no_unowned_attempt(
    owned: list[str], monkeypatch: pytest.MonkeyPatch, failure_stage: str
) -> None:
    other, refused = _id(), _id()
    artifacts.begin_attempt(other)
    owned.append(other)
    refused_path = artifacts._root() / refused
    original_directory = artifacts._directory

    def refuse_creation(parent_handle: int, attempt_id: str) -> int:
        raise artifacts.ArtifactRefusal("synthetic handle acquisition refusal")

    def refuse_post_creation(attempt_id: str, *, require: bool = True) -> Path:
        if attempt_id == refused:
            raise artifacts.ArtifactRefusal("synthetic post-creation check refusal")
        return original_directory(attempt_id, require=require)

    with monkeypatch.context() as patcher:
        if failure_stage == "creation":
            patcher.setattr(artifacts, "_create_pinned_directory", refuse_creation)
        else:
            patcher.setattr(artifacts, "_directory", refuse_post_creation)
        with pytest.raises(artifacts.ArtifactRefusal):
            artifacts.begin_attempt(refused)

    assert not refused_path.exists()
    assert artifacts.read_record(other)["attemptId"] == other
    assert artifacts.read_record(other)["state"] == "pending"


@pytest.mark.unit
def test_partial_write_leaves_pending_ownership_and_no_stage(
    owned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    attempt_id = _id()
    artifacts.begin_attempt(attempt_id)
    owned.append(attempt_id)
    original_replace = os.replace

    def fail_terminal(
        source: str | os.PathLike[str], target: str | os.PathLike[str]
    ) -> None:
        if Path(target).name == "record.json":
            raise OSError("synthetic publication failure")
        original_replace(source, target)

    monkeypatch.setattr(os, "replace", fail_terminal)
    with pytest.raises(OSError):
        artifacts.publish_terminal(attempt_id, _terminal(attempt_id, ["record.json"]))
    assert artifacts.read_record(attempt_id)["state"] == "pending"
    assert not (artifacts._directory(attempt_id) / "record.json.tmp").exists()


@pytest.mark.unit
def test_reparse_attempt_directory_refuses(owned: list[str], tmp_path: Path) -> None:
    attempt_id = _id()
    root = artifacts._root(create=True)
    link = root / attempt_id
    try:
        os.symlink(tmp_path, link, target_is_directory=True)
    except OSError, NotImplementedError:
        pytest.skip("directory symlink creation is unavailable on this Windows host")
    try:
        with pytest.raises(artifacts.ArtifactRefusal):
            artifacts.read_record(attempt_id)
        with pytest.raises(artifacts.ArtifactRefusal):
            artifacts.remove_attempt(attempt_id)
    finally:
        link.unlink()


@pytest.mark.unit
def test_reparse_attribute_refuses_even_without_symlink_privilege(
    owned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    attempt_id = _id()
    artifacts.begin_attempt(attempt_id)
    owned.append(attempt_id)
    original = Path.lstat
    directory = artifacts._directory(attempt_id)

    def reparse_lstat(path: Path):
        info = original(path)
        if path == directory:
            return SimpleNamespace(
                st_mode=info.st_mode,
                st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT,
            )
        return info

    with monkeypatch.context() as patcher:
        patcher.setattr(Path, "lstat", reparse_lstat)
        with pytest.raises(artifacts.ArtifactRefusal):
            artifacts.read_record(attempt_id)
        with pytest.raises(artifacts.ArtifactRefusal):
            artifacts.remove_attempt(attempt_id)


@pytest.mark.unit
def test_record_size_and_invalid_json_are_refused(owned: list[str]) -> None:
    attempt_id = _id()
    artifacts.begin_attempt(attempt_id)
    owned.append(attempt_id)
    record = _terminal(attempt_id, ["record.json"])
    record["padding"] = "x" * (256 * 1024)
    with pytest.raises(artifacts.ArtifactRefusal):
        artifacts.publish_terminal(attempt_id, record)
    assert (
        json.loads(
            (artifacts._directory(attempt_id) / "record.json").read_text(
                encoding="utf-8"
            )
        )["state"]
        == "pending"
    )


@pytest.mark.unit
def test_directory_swap_after_ownership_read_cannot_delete_another_run(
    owned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    first, second, spare = _id(), _id(), _id()
    artifacts.begin_attempt(first)
    artifacts.begin_attempt(second)
    owned.extend((first, second))
    first_path = artifacts._directory(first)
    second_path = artifacts._directory(second)
    spare_path = first_path.parent / spare
    original_read = artifacts.read_record
    swap_attempted = False

    def read_then_swap(attempt_id: str):
        nonlocal swap_attempted
        record = original_read(attempt_id)
        if attempt_id == first:
            swap_attempted = True
            os.rename(first_path, spare_path)
            os.rename(second_path, first_path)
            os.rename(spare_path, second_path)
        return record

    with monkeypatch.context() as patcher:
        patcher.setattr(artifacts, "read_record", read_then_swap)
        with pytest.raises(OSError):
            artifacts.remove_attempt(first)
    assert swap_attempted
    assert not spare_path.exists()
    assert original_read(first)["attemptId"] == first
    assert original_read(second)["attemptId"] == second


@pytest.mark.unit
@pytest.mark.parametrize("operation", ["publish", "rollback", "proof"])
def test_directory_swap_after_ownership_read_cannot_mutate_another_run(
    owned: list[str], monkeypatch: pytest.MonkeyPatch, operation: str
) -> None:
    first, second, spare = _id(), _id(), _id()
    artifacts.begin_attempt(first)
    artifacts.begin_attempt(second)
    owned.extend((first, second))
    artifacts.write_proof_slot(second, b"other-attempt-proof")
    first_path = artifacts._directory(first)
    second_path = artifacts._directory(second)
    spare_path = first_path.parent / spare
    original_read = artifacts.read_record
    swap_attempted = False

    def read_then_swap(attempt_id: str):
        nonlocal swap_attempted
        record = original_read(attempt_id)
        if attempt_id == first:
            swap_attempted = True
            os.rename(first_path, spare_path)
            os.rename(second_path, first_path)
            os.rename(spare_path, second_path)
        return record

    with monkeypatch.context() as patcher:
        patcher.setattr(artifacts, "read_record", read_then_swap)
        with pytest.raises(OSError):
            if operation == "publish":
                artifacts.publish_terminal(first, _terminal(first, ["record.json"]))
            elif operation == "rollback":
                artifacts.rollback_unpublished(first)
            else:
                artifacts.write_proof_slot(first, b"first-attempt-proof")

    assert swap_attempted
    assert not spare_path.exists()
    assert original_read(first)["attemptId"] == first
    assert original_read(first)["state"] == "pending"
    assert original_read(second)["attemptId"] == second
    assert original_read(second)["state"] == "pending"
    assert not (first_path / "proof-output.bin").exists()
    assert (second_path / "proof-output.bin").read_bytes() == b"other-attempt-proof"
