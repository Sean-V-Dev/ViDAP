"""The local `/api/slice/` channel: contracts, validation, run, and workflow files."""

from __future__ import annotations

import json
import threading
from collections.abc import Mapping
from math import isfinite
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from src.vidap_workflow import (
        OMITTED_DEFAULT,
        Diagnostic,
        NodeDefinition,
        PortDefinition,
        WorkflowDecodeError,
        WorkflowDocument,
        deserialize_document,
        validate_workflow_text,
    )
else:
    from vidap_workflow import (
        OMITTED_DEFAULT,
        Diagnostic,
        NodeDefinition,
        PortDefinition,
        WorkflowDecodeError,
        WorkflowDocument,
        deserialize_document,
        validate_workflow_text,
    )

from . import workspace
from .artifacts import ArtifactRefusal, _directory
from .dispatch import DispatchRefusal
from .output import (
    METRICS_FORMAT,
    METRICS_SCHEMA_VERSION,
    ReferenceOutputRefusal,
    SliceMetrics,
    metrics_bytes,
)
from .planner import PlanningFailure
from .representation import PreparationFailure
from .run import AttemptRefusal, PublicationIndeterminate
from .slice import SLICE_REGISTRY, run_slice_attempt

MAX_BODY_BYTES = 256 * 1024
MAX_PROOF_BYTES = 64 * 1024
ALLOWED_HOSTS = frozenset({"127.0.0.1", "localhost"})
ALLOWED_ORIGINS = frozenset({"http://127.0.0.1:5173", "http://127.0.0.1:8000"})
RUN_LOCK = threading.Lock()

_ERRORS = {
    "invalid-host": (400, "The request host is not a local loopback name."),
    "origin-refused": (403, "The request origin is not allowed."),
    "unsupported-content-type": (415, "The request body must be application/json."),
    "body-too-large": (413, "The request body exceeds 256 KiB."),
    "malformed-json": (400, "The request body is not valid UTF-8 JSON."),
    "invalid-request": (400, "The request body does not have the required fields."),
    "invalid-name": (400, "The workflow name is not allowed."),
    "invalid-workflow": (422, "The workflow is not valid."),
    "invalid-sidecar": (422, "The workspace view is not valid."),
    "workflow-too-large": (413, "The workflow exceeds its size bound."),
    "run-refused": (422, "This workflow cannot be run as the slice."),
    "busy": (409, "Another run is in progress."),
    "conflict": (409, "The saved files changed since they were loaded."),
    "not-found": (404, "No saved workflow has that name."),
    "storage-refused": (500, "The local workflow storage is not safe to use."),
    "run-storage-failed": (500, "The run could not be recorded safely."),
    "publication-indeterminate": (
        500,
        "The run's recorded state could not be verified; inspect the attempt.",
    ),
    "metrics-readback-failed": (500, "The recorded result could not be read back."),
}


class SliceError(Exception):
    """A fixed, sanitized channel error; carries no exception or input text."""

    def __init__(self, code: str, **extra: object) -> None:
        super().__init__(code)
        self.code = code
        self.extra = extra


def _error_response(_: Request, error: Exception) -> JSONResponse:
    if not isinstance(error, SliceError):
        raise error
    status, message = _ERRORS[error.code]
    body: dict[str, object] = {"error": {"code": error.code, "message": message}}
    body.update(error.extra)
    return JSONResponse(body, status_code=status)


def _host_name(value: str) -> str:
    name, separator, port = value.rpartition(":")
    if separator and port.isdigit():
        return name
    return value


def guard(request: Request) -> None:
    """Host and origin checks for every slice route; no CORS is ever granted."""

    if _host_name(request.headers.get("host", "")) not in ALLOWED_HOSTS:
        raise SliceError("invalid-host")
    origin = request.headers.get("origin")
    if origin is not None and origin not in ALLOWED_ORIGINS:
        raise SliceError("origin-refused")


async def body_text(request: Request) -> str:
    """Content-type, size, and UTF-8 checks before any parsing."""

    media = [
        part.strip().lower()
        for part in request.headers.get("content-type", "").split(";")
    ]
    if media[0] != "application/json" or media[1:] not in ([], ["charset=utf-8"]):
        raise SliceError("unsupported-content-type")
    declared = request.headers.get("content-length")
    if declared is not None and declared.isdigit() and int(declared) > MAX_BODY_BYTES:
        raise SliceError("body-too-large")
    chunks: list[bytes] = []
    size = 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > MAX_BODY_BYTES:
            raise SliceError("body-too-large")
        chunks.append(chunk)
    try:
        return b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as error:
        raise SliceError("malformed-json") from error


Body = Annotated[str, Depends(body_text)]


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate name")
        result[key] = value
    return result


def _reject_constant(_: str) -> object:
    raise ValueError("non-finite number")


def _finite_float(text: str) -> float:
    number = float(text)
    if not isfinite(number):
        raise ValueError("number overflows to infinity")
    return number


def _parse(text: str) -> object:
    """Strict JSON: no duplicate names, no non-finite numbers, bounded depth."""

    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
        )
    except ValueError, RecursionError:
        raise SliceError("malformed-json") from None


def _diagnostics(items: tuple[Diagnostic, ...]) -> list[dict[str, object]]:
    return [
        {
            "code": item.code,
            "severity": item.severity,
            "category": item.category,
            "elementKind": item.affected_element_kind,
            "elementReference": item.affected_element_reference,
            "message": item.message,
            "remedy": item.remedy,
            "jsonPointer": item.json_pointer,
        }
        for item in items
    ]


def _document(text: str) -> WorkflowDocument:
    try:
        return workspace.decode_workflow(text, SLICE_REGISTRY)
    except workspace.InvalidWorkflow as error:
        raise SliceError(
            "invalid-workflow", diagnostics=_diagnostics(error.diagnostics)
        ) from None


def _nested_document(value: object) -> WorkflowDocument:
    if not isinstance(value, dict):
        raise SliceError("invalid-request")
    try:
        text = json.dumps(value, ensure_ascii=False, allow_nan=False)
    except ValueError, RecursionError:
        raise SliceError("malformed-json") from None
    return _document(text)


def _fields(value: object, required: set[str]) -> Mapping[str, object]:
    if not isinstance(value, dict) or set(value) != required:
        raise SliceError("invalid-request")
    return value


def _digest_field(value: object) -> str | None:
    try:
        return workspace.check_digest(value)
    except workspace.InvalidDigest:
        raise SliceError("invalid-request") from None


def _name(name: str) -> str:
    try:
        return workspace.check_name(name)
    except workspace.InvalidName:
        raise SliceError("invalid-name") from None


def _contract(definition: NodeDefinition) -> dict[str, object]:
    def port(item: PortDefinition) -> dict[str, object]:
        return {
            "key": item.key,
            "nominalType": item.nominal_type,
            "label": item.display.label,
            "cardinality": item.cardinality,
            "required": item.required,
        }

    parameters: list[dict[str, object]] = []
    for parameter in definition.parameters:
        data: dict[str, object] = {
            "key": parameter.key,
            "kind": parameter.value_kind,
            "required": parameter.required,
            "label": parameter.display.label,
            "description": parameter.display.description,
            "constraints": dict(parameter.constraints),
        }
        if parameter.default is not OMITTED_DEFAULT:
            data["default"] = parameter.default
        parameters.append(data)
    return {
        "type": definition.type_id,
        "label": definition.display.label,
        "description": definition.display.description,
        "inputs": [port(item) for item in definition.inputs],
        "outputs": [port(item) for item in definition.outputs],
        "parameters": parameters,
    }


def _plain(value: object) -> object:
    """Convert the frozen record values back into plain JSON values."""

    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _read_metrics(attempt_id: str) -> dict[str, object]:
    """Only the owned slot's exact bytes may become a displayed result."""

    try:
        path = _directory(attempt_id) / "proof-output.bin"
        if not path.is_file() or path.stat().st_size > MAX_PROOF_BYTES:
            raise ValueError("slot missing or oversized")
        data = path.read_bytes()
        parsed = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
        if not isinstance(parsed, dict) or set(parsed) != {
            "accuracy",
            "correct",
            "format",
            "schemaVersion",
            "testRows",
        }:
            raise ValueError("slot shape")
        if (
            parsed["format"] != METRICS_FORMAT
            or parsed["schemaVersion"] != METRICS_SCHEMA_VERSION
        ):
            raise ValueError("slot format")
        metrics = SliceMetrics(
            parsed["accuracy"],
            parsed["correct"],
            parsed["testRows"],
        )
        if metrics_bytes(metrics) != data:
            raise ValueError("slot bytes are not canonical")
    except (ArtifactRefusal, OSError, ValueError, TypeError) as error:
        raise SliceError("metrics-readback-failed", attemptId=attempt_id) from error
    return parsed


router = APIRouter(prefix="/api/slice", dependencies=[Depends(guard)])


@router.get("/contracts")
def contracts() -> dict[str, object]:
    return {"contracts": [_contract(item) for item in SLICE_REGISTRY.definitions]}


@router.post("/validate")
def validate(text: Body) -> dict[str, object]:
    findings = validate_workflow_text(text, SLICE_REGISTRY)
    try:
        deserialize_document(text)
    except WorkflowDecodeError:
        raise SliceError(
            "invalid-workflow", diagnostics=_diagnostics(findings)
        ) from None
    return {"valid": not findings, "diagnostics": _diagnostics(findings)}


@router.post("/run")
def run(text: Body) -> dict[str, object]:
    document = _document(text)
    if not RUN_LOCK.acquire(blocking=False):
        raise SliceError("busy")
    try:
        result = run_slice_attempt(document)
    except PublicationIndeterminate as error:
        raise SliceError(
            "publication-indeterminate", attemptId=error.attempt_id
        ) from None
    except (
        ReferenceOutputRefusal,
        AttemptRefusal,
        DispatchRefusal,
        PlanningFailure,
        PreparationFailure,
    ):
        raise SliceError("run-refused") from None
    except ArtifactRefusal:
        raise SliceError("run-storage-failed") from None
    finally:
        RUN_LOCK.release()
    data = _plain(result.record.data)
    if not isinstance(data, dict):
        raise SliceError("run-storage-failed")
    attempt_id = str(data["attemptId"])
    artifacts = data["artifacts"]
    nodes = data["nodes"]
    if not isinstance(artifacts, list) or not isinstance(nodes, list):
        raise SliceError("run-storage-failed")
    published = data["outcome"] == "succeeded" and "proof-output.bin" in artifacts
    return {
        "attemptId": attempt_id,
        "outcome": data["outcome"],
        "semanticDigest": data["semanticDigest"],
        "nodes": [
            {
                "nodeId": node["nodeId"],
                "operationKey": node["operationKey"],
                "status": node["status"],
            }
            for node in nodes
        ],
        "diagnostics": data["diagnostics"],
        "metrics": _read_metrics(attempt_id) if published else None,
    }


@router.get("/workflows")
def workflows() -> dict[str, object]:
    try:
        return {"workflows": workspace.list_workflows()}
    except workspace.StorageRefusal:
        raise SliceError("storage-refused") from None


@router.get("/workflows/{name}")
def load(name: str) -> dict[str, object]:
    name = _name(name)
    try:
        loaded = workspace.load(name, SLICE_REGISTRY)
    except FileNotFoundError:
        raise SliceError("not-found") from None
    except workspace.TooLarge:
        raise SliceError("workflow-too-large") from None
    except workspace.InvalidWorkflow as error:
        raise SliceError(
            "invalid-workflow", diagnostics=_diagnostics(error.diagnostics)
        ) from None
    except workspace.StorageRefusal, OSError:
        raise SliceError("storage-refused") from None
    return {
        "name": loaded.name,
        "workflow": loaded.workflow,
        "workflowDigest": loaded.workflow_digest,
        "sidecar": loaded.sidecar,
        "sidecarDigest": loaded.sidecar_digest,
        "sidecarNotice": loaded.sidecar_notice,
    }


@router.put("/workflows/{name}")
def save(name: str, text: Body) -> dict[str, object]:
    name = _name(name)
    request = _fields(
        _parse(text), {"workflow", "sidecar", "baseWorkflowDigest", "baseSidecarDigest"}
    )
    base_workflow = _digest_field(request["baseWorkflowDigest"])
    base_sidecar = _digest_field(request["baseSidecarDigest"])
    document = _nested_document(request["workflow"])
    sidecar: dict[str, object] | None = None
    if request["sidecar"] is not None:
        try:
            sidecar = workspace.check_sidecar(request["sidecar"])
        except workspace.InvalidSidecar:
            raise SliceError("invalid-sidecar") from None
    try:
        workflow_digest, sidecar_digest = workspace.save(
            name, document, sidecar, base_workflow, base_sidecar, SLICE_REGISTRY
        )
    except workspace.Conflict as conflict:
        raise SliceError(
            "conflict",
            workflowDigest=conflict.workflow_digest,
            sidecarDigest=conflict.sidecar_digest,
            missing=conflict.workflow_digest is None,
            summary=conflict.summary,
        ) from None
    except workspace.TooLarge:
        raise SliceError("workflow-too-large") from None
    except workspace.StorageRefusal, OSError:
        raise SliceError("storage-refused") from None
    return {
        "name": name,
        "workflowDigest": workflow_digest,
        "sidecarDigest": sidecar_digest,
    }


@router.post("/workflows/{name}/compare")
def compare(name: str, text: Body) -> dict[str, object]:
    name = _name(name)
    request = _fields(
        _parse(text), {"workflow", "baseWorkflowDigest", "baseSidecarDigest"}
    )
    base_workflow = _digest_field(request["baseWorkflowDigest"])
    base_sidecar = _digest_field(request["baseSidecarDigest"])
    document = _nested_document(request["workflow"])
    try:
        return workspace.compare(
            name, document, base_workflow, base_sidecar, SLICE_REGISTRY
        )
    except workspace.TooLarge:
        raise SliceError("workflow-too-large") from None
    except workspace.StorageRefusal, OSError:
        raise SliceError("storage-refused") from None


def install(app: FastAPI) -> None:
    """Add only the slice routes and their error envelope to the shell."""

    app.include_router(router)
    app.add_exception_handler(SliceError, _error_response)
