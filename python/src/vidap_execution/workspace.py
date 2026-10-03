"""Backend-owned slice workflow files, sidecars, digests, and change summaries."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import threading
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.vidap_workflow import (
        Diagnostic,
        Edge,
        NodeRegistry,
        WorkflowDocument,
        deserialize_document,
        serialize_document,
        validate_workflow_text,
    )
else:
    from vidap_workflow import (
        Diagnostic,
        Edge,
        NodeRegistry,
        WorkflowDocument,
        deserialize_document,
        serialize_document,
        validate_workflow_text,
    )

_CHECKOUT = Path(__file__).resolve().parents[3]
WORKFLOW_SUFFIX = ".vidap.json"
SIDECAR_SUFFIX = ".vidap-view.json"
MAX_WORKFLOW_BYTES = 256 * 1024
MAX_SIDECAR_BYTES = 64 * 1024
SIDECAR_FORMAT = "vidap.workspace-view"
SIDECAR_SCHEMA_VERSION = "1.0"
_NAME = re.compile(r"[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?")
_REGION = re.compile(r"[A-Za-z0-9_-]{1,40}")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
SAVE_LOCK = threading.Lock()


class StorageRefusal(ValueError):
    """Unsafe storage location or state; carries no path or input text."""


class InvalidName(ValueError):
    """A workflow name outside the fixed naming rule."""


class TooLarge(ValueError):
    """A stored or posted file beyond its fixed size bound."""


class InvalidDigest(ValueError):
    """A base digest that is neither null nor ``sha256:<64 hex>``."""


class InvalidWorkflow(ValueError):
    """A workflow that does not decode or validate; carries Phase 1 findings."""

    def __init__(self, diagnostics: tuple[Diagnostic, ...]) -> None:
        super().__init__("invalid workflow")
        self.diagnostics = diagnostics


class InvalidSidecar(ValueError):
    """A sidecar outside the accepted shape or bounds."""


class UnsupportedSidecar(InvalidSidecar):
    """A sidecar with another format or schema version."""


class Conflict(ValueError):
    """The files on disk differ from the digests the caller based its edit on."""

    def __init__(
        self,
        workflow_digest: str | None,
        sidecar_digest: str | None,
        summary: dict[str, object] | None,
    ) -> None:
        super().__init__("conflict")
        self.workflow_digest = workflow_digest
        self.sidecar_digest = sidecar_digest
        self.summary = summary


_WINDOWS_DEVICES = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{i}" for i in range(1, 10)}
    | {f"lpt{i}" for i in range(1, 10)}
)


def check_name(name: object) -> str:
    if (
        not isinstance(name, str)
        or not _NAME.fullmatch(name)
        or name in _WINDOWS_DEVICES
    ):
        raise InvalidName("invalid workflow name")
    return name


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def check_digest(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        raise InvalidDigest("digest must be null or sha256:<64 hex>")
    return value


def _no_link(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or (
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise StorageRefusal("link or reparse point refused")


def workflows_root(*, create: bool = False) -> Path:
    """The fixed directory, checked segment by segment for links and escape."""

    checkout = _CHECKOUT.resolve(strict=True)
    current = checkout
    for segment in (".vidap-local", "workflows"):
        current = current / segment
        _no_link(current)
        if create:
            current.mkdir(exist_ok=True)
            _no_link(current)
        if current.exists() and not current.is_dir():
            raise StorageRefusal("workflow root is not a directory")
    if current.resolve(strict=False) != checkout / ".vidap-local" / "workflows":
        raise StorageRefusal("workflow root escapes the checkout")
    return current


def _file(name: str, suffix: str) -> Path:
    path = workflows_root() / f"{check_name(name)}{suffix}"
    _no_link(path)
    if path.exists() and not path.is_file():
        raise StorageRefusal("workflow entry is not a regular file")
    return path


def _read(path: Path, maximum: int) -> bytes | None:
    if not path.exists():
        return None
    if path.stat().st_size > maximum:
        raise TooLarge("file exceeds its size bound")
    return path.read_bytes()


def decode_workflow(text: str, registry: NodeRegistry) -> WorkflowDocument:
    """Decode and validate through Phase 1; any finding refuses."""

    findings = validate_workflow_text(text, registry)
    if findings:
        raise InvalidWorkflow(findings)
    return deserialize_document(text)


def _number(value: object, low: float, high: float) -> float:
    if type(value) is int:
        # Compare exactly before converting, so huge integers cannot overflow.
        if not low <= value <= high:
            raise InvalidSidecar("sidecar number is out of range")
        return float(value)
    if type(value) is not float or not isfinite(value) or not low <= value <= high:
        raise InvalidSidecar("sidecar number is out of range")
    return value


def _exact(value: object, keys: set[str]) -> Mapping[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise InvalidSidecar("sidecar object has the wrong fields")
    return value


def check_sidecar(value: object) -> dict[str, object]:
    """Validate the sidecar's shape and bounds; region meaning stays UI-owned."""

    if not isinstance(value, dict):
        raise InvalidSidecar("sidecar must be an object")
    if (
        value.get("format") != SIDECAR_FORMAT
        or value.get("schemaVersion") != SIDECAR_SCHEMA_VERSION
    ):
        raise UnsupportedSidecar("unsupported sidecar format or version")
    data = _exact(value, {"format", "schemaVersion", "regions", "nodes", "viewport"})
    regions = data["regions"]
    if not isinstance(regions, list) or len(regions) > 32:
        raise InvalidSidecar("sidecar regions are invalid")
    keys: set[str] = set()
    for region in regions:
        item = _exact(region, {"key", "width"})
        key = item["key"]
        if not isinstance(key, str) or not _REGION.fullmatch(key) or key in keys:
            raise InvalidSidecar("sidecar region key is invalid")
        keys.add(key)
        _number(item["width"], 120, 4000)
    nodes = data["nodes"]
    if not isinstance(nodes, dict) or len(nodes) > 500:
        raise InvalidSidecar("sidecar nodes are invalid")
    for node_id, entry in nodes.items():
        try:
            parsed = uuid.UUID(node_id)
        except (ValueError, AttributeError, TypeError) as error:
            raise InvalidSidecar("sidecar node ID is invalid") from error
        if str(parsed) != node_id:
            raise InvalidSidecar("sidecar node ID is not canonical")
        item = _exact(entry, {"region", "x", "y"})
        region_key = item["region"]
        if not isinstance(region_key, str) or not _REGION.fullmatch(region_key):
            raise InvalidSidecar("sidecar node region is invalid")
        _number(item["x"], -100000, 100000)
        _number(item["y"], -100000, 100000)
    viewport = _exact(data["viewport"], {"x", "y", "zoom"})
    _number(viewport["x"], -100000, 100000)
    _number(viewport["y"], -100000, 100000)
    _number(viewport["zoom"], 0.1, 4)
    if len(sidecar_bytes(data)) > MAX_SIDECAR_BYTES:
        raise InvalidSidecar("sidecar exceeds its size bound")
    return dict(data)


def sidecar_bytes(value: Mapping[str, object]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, indent=2)
        + "\n"
    ).encode("utf-8")


def change_summary(
    posted: WorkflowDocument, disk: WorkflowDocument
) -> dict[str, object]:
    """Semantic differences, from the posted (editor) to the disk document."""

    before = {node.id: node for node in posted.nodes}
    after = {node.id: node for node in disk.nodes}
    edges_before = {edge.id: edge for edge in posted.edges}
    edges_after = {edge.id: edge for edge in disk.edges}

    def edge_data(edge_id: str, edges: Mapping[str, Edge]) -> dict[str, object]:
        edge = edges[edge_id]
        return {
            "edgeId": edge_id,
            "source": edge.source.to_data(),
            "target": edge.target.to_data(),
        }

    changed: list[dict[str, object]] = []
    for node_id in sorted(set(before) & set(after)):
        old = dict(before[node_id].parameters)
        new = dict(after[node_id].parameters)
        for key in sorted(set(old) | set(new)):
            if old.get(key, None) != new.get(key, None) or (key in old) != (key in new):
                changed.append(
                    {
                        "nodeId": node_id,
                        "key": key,
                        "before": old.get(key),
                        "after": new.get(key),
                    }
                )
    layout_before = posted.layout.to_data() if posted.layout else None
    layout_after = disk.layout.to_data() if disk.layout else None
    return {
        "nodesAdded": [
            {"nodeId": i, "type": after[i].type_id}
            for i in sorted(set(after) - set(before))
        ],
        "nodesRemoved": [
            {"nodeId": i, "type": before[i].type_id}
            for i in sorted(set(before) - set(after))
        ],
        "edgesAdded": [
            edge_data(i, edges_after)
            for i in sorted(set(edges_after) - set(edges_before))
        ],
        "edgesRemoved": [
            edge_data(i, edges_before)
            for i in sorted(set(edges_before) - set(edges_after))
        ],
        "parametersChanged": changed,
        "labelsChanged": [
            i
            for i in sorted(set(before) & set(after))
            if before[i].label != after[i].label
        ],
        "layoutMetadataChanged": layout_before != layout_after,
    }


@dataclass(frozen=True, slots=True)
class Loaded:
    name: str
    workflow: dict[str, object]
    workflow_digest: str
    sidecar: dict[str, object] | None
    sidecar_digest: str | None
    sidecar_notice: str | None


def list_workflows() -> list[dict[str, object]]:
    root = workflows_root()
    if not root.exists():
        return []
    found: list[dict[str, object]] = []
    for entry in sorted(root.iterdir(), key=lambda path: path.name):
        if not entry.name.endswith(WORKFLOW_SUFFIX):
            continue
        name = entry.name[: -len(WORKFLOW_SUFFIX)]
        if not _NAME.fullmatch(name):
            continue
        try:
            path = _file(name, WORKFLOW_SUFFIX)
            data = _read(path, MAX_WORKFLOW_BYTES)
        except StorageRefusal, TooLarge:
            continue
        if data is None:
            continue
        found.append(
            {
                "name": name,
                "workflowDigest": digest(data),
                "hasSidecar": _file(name, SIDECAR_SUFFIX).is_file(),
            }
        )
    return found


def _decode_file(data: bytes, registry: NodeRegistry) -> WorkflowDocument:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        # Undecodable bytes get the Phase 1 malformed-text finding; no repair.
        raise InvalidWorkflow(validate_workflow_text("", registry)) from error
    return decode_workflow(text, registry)


def load(name: str, registry: NodeRegistry) -> Loaded:
    path = _file(name, WORKFLOW_SUFFIX)
    if not path.exists():
        raise FileNotFoundError("workflow not found")
    if path.stat().st_size > MAX_WORKFLOW_BYTES:
        raise TooLarge("workflow exceeds its size bound")
    data = path.read_bytes()
    document = _decode_file(data, registry)
    sidecar: dict[str, object] | None = None
    sidecar_digest: str | None = None
    notice: str | None = None
    side_path = _file(name, SIDECAR_SUFFIX)
    try:
        side_data = _read(side_path, MAX_SIDECAR_BYTES)
    except TooLarge:
        side_data = None
        notice = "unreadable"
    if side_data is not None:
        sidecar_digest = digest(side_data)
        try:
            sidecar = check_sidecar(json.loads(side_data.decode("utf-8")))
        except UnsupportedSidecar:
            notice = "unsupported"
        except InvalidSidecar, ValueError, RecursionError:
            notice = "unreadable"
    elif side_path.exists():
        sidecar_digest = _file_digest(side_path)
    return Loaded(
        name,
        json.loads(serialize_document(document)),
        digest(data),
        sidecar,
        sidecar_digest,
        notice,
    )


def _file_digest(path: Path) -> str | None:
    """Digest of any existing file, read in bounded chunks."""

    if not path.exists():
        return None
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            hasher.update(chunk)
    return "sha256:" + hasher.hexdigest()


def _current(path: Path, maximum: int) -> tuple[bytes | None, str | None]:
    """Current bytes and digest, refusing a file beyond its size bound."""

    if not path.exists():
        return None, None
    if path.stat().st_size > maximum:
        raise TooLarge("file exceeds its size bound")
    data = path.read_bytes()
    return data, digest(data)


def _summary(
    posted: WorkflowDocument, disk_data: bytes | None, registry: NodeRegistry
) -> dict[str, object] | None:
    if disk_data is None:
        return None
    try:
        disk = _decode_file(disk_data, registry)
    except InvalidWorkflow:
        return {"diskUnreadable": True}
    return change_summary(posted, disk)


def compare(
    name: str,
    posted: WorkflowDocument,
    base_workflow: str | None,
    base_sidecar: str | None,
    registry: NodeRegistry,
) -> dict[str, object]:
    workflow_data, workflow_digest = _current(
        _file(name, WORKFLOW_SUFFIX), MAX_WORKFLOW_BYTES
    )
    sidecar_digest = _file_digest(_file(name, SIDECAR_SUFFIX))
    changed = workflow_digest != base_workflow or sidecar_digest != base_sidecar
    return {
        "changed": changed,
        "missing": workflow_data is None,
        "workflowDigest": workflow_digest,
        "sidecarDigest": sidecar_digest,
        "summary": _summary(posted, workflow_data, registry) if changed else None,
    }


def _temporary(path: Path) -> Path:
    temporary = path.with_name(path.name + ".tmp")
    _no_link(temporary)
    if temporary.exists():
        raise StorageRefusal("a temporary file already exists")
    return temporary


def _write(path: Path, data: bytes) -> None:
    temporary = _temporary(path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    try:
        descriptor = os.open(temporary, flags, 0o600)
    except FileExistsError as error:
        raise StorageRefusal("a temporary file already exists") from error
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        _no_link(path)
        os.replace(temporary, path)
    finally:
        if temporary.exists() and not temporary.is_symlink():
            temporary.unlink()


def save(
    name: str,
    document: WorkflowDocument,
    sidecar: dict[str, object] | None,
    base_workflow: str | None,
    base_sidecar: str | None,
    registry: NodeRegistry,
) -> tuple[str, str | None]:
    """Refuse the whole save on any digest mismatch; never silently overwrite."""

    check_name(name)
    workflow_bytes = serialize_document(document).encode("utf-8")
    if len(workflow_bytes) > MAX_WORKFLOW_BYTES:
        raise TooLarge("workflow exceeds its size bound")
    side_bytes = sidecar_bytes(sidecar) if sidecar is not None else None
    with SAVE_LOCK:
        workflows_root(create=True)
        workflow_path = _file(name, WORKFLOW_SUFFIX)
        sidecar_path = _file(name, SIDECAR_SUFFIX)
        disk_data, current_workflow = _current(workflow_path, MAX_WORKFLOW_BYTES)
        current_sidecar = _file_digest(sidecar_path)
        if current_workflow != base_workflow or current_sidecar != base_sidecar:
            raise Conflict(
                current_workflow,
                current_sidecar,
                _summary(document, disk_data, registry),
            )
        # Refuse before writing anything, so a refusal never leaves one file new.
        _temporary(workflow_path)
        if side_bytes is not None:
            _temporary(sidecar_path)
        _write(workflow_path, workflow_bytes)
        if side_bytes is not None:
            _write(sidecar_path, side_bytes)
            return digest(workflow_bytes), digest(side_bytes)
        return digest(workflow_bytes), current_sidecar
