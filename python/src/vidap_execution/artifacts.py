"""Fixed, checkout-owned attempt slots with explicit removal."""

from __future__ import annotations

import ctypes
import json
import os
import stat
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from ctypes import wintypes
from pathlib import Path
from typing import Any

_CHECKOUT = Path(__file__).resolve().parents[3]
_RUNS = _CHECKOUT / ".vidap-local" / "runs"
_SLOTS = frozenset(
    {"record.json", "proof-output.bin", "record.json.tmp", "proof-output.bin.tmp"}
)
_MAX_RECORD = 256 * 1024
_MAX_PROOF = 64 * 1024


class _WindowsFileInfo(ctypes.Structure):
    _fields_ = [
        ("attributes", wintypes.DWORD),
        ("created", wintypes.FILETIME),
        ("accessed", wintypes.FILETIME),
        ("written", wintypes.FILETIME),
        ("volume", wintypes.DWORD),
        ("size_high", wintypes.DWORD),
        ("size_low", wintypes.DWORD),
        ("links", wintypes.DWORD),
        ("index_high", wintypes.DWORD),
        ("index_low", wintypes.DWORD),
    ]


class _WindowsDisposition(ctypes.Structure):
    _fields_ = [("delete", wintypes.BOOLEAN)]


class _UnicodeString(ctypes.Structure):
    _fields_ = [
        ("length", wintypes.USHORT),
        ("maximum_length", wintypes.USHORT),
        ("buffer", wintypes.LPWSTR),
    ]


class _ObjectAttributes(ctypes.Structure):
    _fields_ = [
        ("length", wintypes.ULONG),
        ("root_directory", wintypes.HANDLE),
        ("object_name", ctypes.POINTER(_UnicodeString)),
        ("attributes", wintypes.ULONG),
        ("security_descriptor", wintypes.LPVOID),
        ("security_quality_of_service", wintypes.LPVOID),
    ]


class _IoStatusBlock(ctypes.Structure):
    _fields_ = [("status", wintypes.LPVOID), ("information", ctypes.c_size_t)]


class ArtifactRefusal(ValueError):
    """Unsafe or inconsistent ownership, path, or slot content."""


def _run_id(value: str) -> str:
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError, TypeError) as error:
        raise ArtifactRefusal("attempt ID must be canonical UUIDv4") from error
    if parsed.version != 4 or str(parsed) != value:
        raise ArtifactRefusal("attempt ID must be canonical lowercase UUIDv4")
    return value


def _no_reparse(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or (
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise ArtifactRefusal("reparse traversal is forbidden")


def _root(create: bool = False) -> Path:
    checkout = _CHECKOUT.resolve(strict=True)
    if not checkout.is_dir():
        raise ArtifactRefusal("checkout root is unavailable")
    current = checkout
    for segment in (".vidap-local", "runs"):
        current = current / segment
        _no_reparse(current)
        if create:
            current.mkdir(exist_ok=True)
            _no_reparse(current)
        if current.exists() and not current.is_dir():
            raise ArtifactRefusal("managed root is not a directory")
    if current.resolve(strict=False) != checkout / ".vidap-local" / "runs":
        raise ArtifactRefusal("managed root escapes checkout")
    return current


def _directory(attempt_id: str, *, require: bool = True) -> Path:
    path = _root() / _run_id(attempt_id)
    _no_reparse(path)
    if require and not path.is_dir():
        raise ArtifactRefusal("attempt directory is missing")
    if path.exists() and path.resolve(strict=True).parent != _root().resolve(
        strict=True
    ):
        raise ArtifactRefusal("attempt directory escapes managed root")
    return path


def _encoded_record(record: dict[str, Any]) -> bytes:
    try:
        data = json.dumps(
            record,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
        parsed = json.loads(data.decode("utf-8"))
    except (TypeError, ValueError, UnicodeError) as error:
        raise ArtifactRefusal("record is not valid UTF-8 JSON") from error
    if parsed != record or len(data) > _MAX_RECORD:
        raise ArtifactRefusal("record is inconsistent or exceeds 256 KiB")
    return data


def _atomic_slot(
    directory: Path, slot: str, data: bytes, maximum: int, *, replace: bool = False
) -> None:
    if slot not in ("record.json", "proof-output.bin") or len(data) > maximum:
        raise ArtifactRefusal("slot is unknown or exceeds its size bound")
    _no_reparse(directory)
    target = directory / slot
    temporary = directory / f"{slot}.tmp"
    _no_reparse(target)
    _no_reparse(temporary)
    if temporary.exists():
        raise ArtifactRefusal("fixed temporary slot already exists")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    descriptor = os.open(temporary, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.stat().st_size != len(data):
            raise ArtifactRefusal("incomplete slot write")
        _no_reparse(target)
        if replace:
            os.replace(temporary, target)
        else:
            # Initial publication must refuse a slot created since the check.
            os.rename(temporary, target)
    finally:
        if temporary.exists() and not temporary.is_symlink():
            temporary.unlink()


def begin_attempt(attempt_id: str) -> None:
    _root(create=True)
    pending = {
        "format": "vidap.attempt-ownership/1.0",
        "attemptId": attempt_id,
        "state": "pending",
        "ownedSlots": sorted(_SLOTS),
        "artifacts": [],
    }
    with _pinned_attempt(attempt_id, create=True) as (directory, kernel, handle):
        try:
            _atomic_slot(
                directory, "record.json", _encoded_record(pending), _MAX_RECORD
            )
        except ArtifactRefusal, OSError:
            # The handle disposition refuses if a slot remains in the directory.
            _mark_directory_deleted(kernel, handle)
            raise


def write_proof_slot(attempt_id: str, data: bytes) -> None:
    """Synthetic evidence slot; no product output format is implied."""

    if not isinstance(data, bytes):
        raise ArtifactRefusal("proof slot requires opaque bytes")
    with _pinned_attempt(attempt_id) as (directory, _, _):
        ownership = read_record(attempt_id)
        if ownership.get("state") != "pending":
            raise ArtifactRefusal("proof slot requires pending ownership")
        if (directory / "proof-output.bin").exists():
            raise ArtifactRefusal("proof slot already published")
        _atomic_slot(directory, "proof-output.bin", data, _MAX_PROOF)


def publish_terminal(attempt_id: str, record: dict[str, Any]) -> None:
    with _pinned_attempt(attempt_id) as (directory, _, _):
        if read_record(attempt_id).get("state") != "pending":
            raise ArtifactRefusal("only pending ownership may become terminal")
        if record.get("attemptId") != attempt_id or record.get("state") not in (
            "succeeded",
            "failed",
        ):
            raise ArtifactRefusal("terminal ownership is inconsistent")
        if record.get("ownedSlots") != sorted(_SLOTS):
            raise ArtifactRefusal("terminal ownership slots are inconsistent")
        artifacts = record.get("artifacts")
        if not isinstance(artifacts, list) or not set(artifacts) <= {
            "record.json",
            "proof-output.bin",
        }:
            raise ArtifactRefusal("terminal artifact references are invalid")
        if "record.json" not in artifacts:
            raise ArtifactRefusal("terminal record must reference itself")
        if (
            "proof-output.bin" in artifacts
            and not (directory / "proof-output.bin").is_file()
        ):
            raise ArtifactRefusal("referenced proof slot is absent")
        _atomic_slot(
            directory, "record.json", _encoded_record(record), _MAX_RECORD, replace=True
        )


def read_record(attempt_id: str) -> dict[str, Any]:
    path = _directory(attempt_id) / "record.json"
    _no_reparse(path)
    if not path.is_file() or path.stat().st_size > _MAX_RECORD:
        raise ArtifactRefusal("ownership record missing or oversized")
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, ValueError) as error:
        raise ArtifactRefusal("ownership record is invalid") from error
    if not isinstance(record, dict) or record.get("attemptId") != attempt_id:
        raise ArtifactRefusal("ownership record identifies another attempt")
    return record


def rollback_unpublished(attempt_id: str) -> None:
    """Leave pending ownership, remove only unpublished same-attempt slots."""

    with _pinned_attempt(attempt_id) as (directory, _, _):
        if read_record(attempt_id).get("state") != "pending":
            raise ArtifactRefusal("rollback requires pending ownership")
        for name in ("record.json.tmp", "proof-output.bin.tmp", "proof-output.bin"):
            path = directory / name
            _no_reparse(path)
            if path.exists():
                path.unlink()


def _windows_api() -> Any:
    if os.name != "nt":
        raise ArtifactRefusal("safe removal requires the supported Windows runtime")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.GetFileInformationByHandle.argtypes = (
        wintypes.HANDLE,
        ctypes.POINTER(_WindowsFileInfo),
    )
    kernel.GetFileInformationByHandle.restype = wintypes.BOOL
    kernel.SetFileInformationByHandle.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    kernel.SetFileInformationByHandle.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.CloseHandle.restype = wintypes.BOOL
    return kernel


def _create_pinned_directory(parent_handle: int, attempt_id: str) -> int:
    """Create a new directory and receive its handle in one Windows operation."""

    native = ctypes.WinDLL("ntdll")
    native.NtCreateFile.argtypes = (
        ctypes.POINTER(wintypes.HANDLE),
        wintypes.DWORD,
        ctypes.POINTER(_ObjectAttributes),
        ctypes.POINTER(_IoStatusBlock),
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    native.NtCreateFile.restype = wintypes.LONG
    name_buffer = ctypes.create_unicode_buffer(attempt_id)
    name = _UnicodeString(
        len(attempt_id.encode("utf-16-le")),
        len(name_buffer) * ctypes.sizeof(ctypes.c_wchar),
        ctypes.cast(name_buffer, wintypes.LPWSTR),
    )
    attributes = _ObjectAttributes(
        ctypes.sizeof(_ObjectAttributes),
        parent_handle,
        ctypes.pointer(name),
        0x0000_0040,  # OBJ_CASE_INSENSITIVE
        None,
        None,
    )
    status_block = _IoStatusBlock()
    handle = wintypes.HANDLE()
    status = native.NtCreateFile(
        ctypes.byref(handle),
        0x0000_0080 | 0x0001_0000,  # FILE_READ_ATTRIBUTES | DELETE
        ctypes.byref(attributes),
        ctypes.byref(status_block),
        None,
        stat.FILE_ATTRIBUTE_NORMAL,
        0x0000_0001 | 0x0000_0002,  # SHARE_READ | SHARE_WRITE; no SHARE_DELETE
        2,  # FILE_CREATE: refuse an existing UUID directory
        1,  # FILE_DIRECTORY_FILE
        None,
        0,
    )
    if status != 0:
        if status & 0xFFFF_FFFF == 0xC000_0035:  # STATUS_OBJECT_NAME_COLLISION
            raise FileExistsError("attempt UUID directory already exists")
        raise ArtifactRefusal(
            f"attempt directory cannot be created with a pinned handle "
            f"(Windows NTSTATUS {status & 0xFFFF_FFFF:#010x})"
        )
    if handle.value is None:
        raise ArtifactRefusal("attempt directory creation returned no handle")
    return handle.value


@contextmanager
def _pinned_attempt(
    attempt_id: str, *, create: bool = False
) -> Iterator[tuple[Path, Any, int]]:
    """Pin managed directories and deny rename/delete sharing during an operation."""

    kernel = _windows_api()
    run = _RUNS / _run_id(attempt_id)
    paths = (_CHECKOUT, _CHECKOUT / ".vidap-local", _RUNS, run)
    handles: list[int] = []
    created = False
    yielded = False
    try:
        for index, path in enumerate(paths):
            if index and not (create and index == 3):
                _no_reparse(path)
            if create and index == 3:
                handle = _create_pinned_directory(handles[-1], attempt_id)
                created = True
            else:
                handle = kernel.CreateFileW(
                    str(path),
                    0x0000_0080 | (0x0001_0000 if index == 3 else 0),
                    # FILE_READ_ATTRIBUTES; DELETE only for the owned run
                    0x0000_0001 | 0x0000_0002,
                    # SHARE_READ | SHARE_WRITE; no SHARE_DELETE
                    None,
                    3,  # OPEN_EXISTING
                    0x0200_0000 | (0x0020_0000 if index else 0),
                    None,  # BACKUP_SEMANTICS; OPEN_REPARSE_POINT below checkout
                )
            if handle == ctypes.c_void_p(-1).value or handle is None:
                raise ArtifactRefusal(
                    f"managed directory cannot be pinned safely at level {index} "
                    f"(Windows error {ctypes.get_last_error()})"
                )
            handles.append(handle)
            info = _WindowsFileInfo()
            if not kernel.GetFileInformationByHandle(handle, ctypes.byref(info)):
                raise ArtifactRefusal("managed directory identity is unavailable")
            if not info.attributes & stat.FILE_ATTRIBUTE_DIRECTORY:
                raise ArtifactRefusal("managed path is not a directory")
            if index and info.attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ArtifactRefusal("managed directory is a reparse point")
        directory = _directory(attempt_id)
        yielded = True
        yield directory, kernel, handles[-1]
    finally:
        try:
            if created and not yielded and handles:
                # Only this newly created handle can be marked; Windows refuses
                # a nonempty directory without following a later path lookup.
                _mark_directory_deleted(kernel, handles[-1])
        finally:
            for handle in reversed(handles):
                kernel.CloseHandle(handle)


def _mark_directory_deleted(kernel: Any, handle: int) -> None:
    disposition = _WindowsDisposition(1)
    if not kernel.SetFileInformationByHandle(
        handle, 4, ctypes.byref(disposition), ctypes.sizeof(disposition)
    ):
        raise ArtifactRefusal("verified directory could not be marked for removal")


def remove_attempt(attempt_id: str) -> None:
    """Refuse any ambiguous state before removing fixed recorded slots."""

    with _pinned_attempt(attempt_id) as (directory, kernel, handle):
        record = read_record(attempt_id)
        if record.get("format") != "vidap.attempt-ownership/1.0" or record.get(
            "ownedSlots"
        ) != sorted(_SLOTS):
            raise ArtifactRefusal("ownership metadata is inconsistent")
        if record.get("state") not in ("pending", "succeeded", "failed"):
            raise ArtifactRefusal("ownership state is inconsistent")
        references = record.get("artifacts")
        if not isinstance(references, list) or not set(references) <= {
            "record.json",
            "proof-output.bin",
        }:
            raise ArtifactRefusal("artifact references are inconsistent")
        if record["state"] == "pending" and references:
            raise ArtifactRefusal("pending ownership cannot publish artifacts")
        if record["state"] != "pending" and "record.json" not in references:
            raise ArtifactRefusal("terminal record reference is missing")
        proof = directory / "proof-output.bin"
        if record["state"] != "pending" and proof.exists() != (
            "proof-output.bin" in references
        ):
            raise ArtifactRefusal("terminal proof reference is inconsistent")
        for entry in directory.iterdir():
            if entry.name not in _SLOTS:
                raise ArtifactRefusal("attempt contains an unexpected entry")
            _no_reparse(entry)
            if not entry.is_file():
                raise ArtifactRefusal("attempt contains a non-file slot")
        for name in sorted(_SLOTS - {"record.json"}):
            path = directory / name
            if path.exists():
                path.unlink()
        (directory / "record.json").unlink()
        _mark_directory_deleted(kernel, handle)
