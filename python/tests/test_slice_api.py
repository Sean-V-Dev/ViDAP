"""The `/api/slice/` channel: contracts, validation, run, guards, concurrency."""

from __future__ import annotations

import json
import uuid
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import httpx
import pytest
from test_slice_operations import FIXTURES, expected_metrics, fixture, runs

from vidap_execution import run as run_module
from vidap_execution import slice_api, workspace
from vidap_execution.app import create_app
from vidap_execution.artifacts import _directory, remove_attempt
from vidap_execution.planner import plan_execution
from vidap_execution.run import PublicationIndeterminate
from vidap_execution.slice import SLICE_BINDINGS, SLICE_REGISTRY

ROOT = Path(__file__).resolve().parents[2]
JSON = {"content-type": "application/json"}


def fixture_text(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


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


@pytest.fixture
def isolated_workflows(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Never touch the real checkout's saved workflows from tests."""

    monkeypatch.setattr(workspace, "_CHECKOUT", tmp_path)
    return tmp_path / ".vidap-local" / "workflows"


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(
        transport=transport, base_url="http://127.0.0.1:8000"
    ) as session:
        yield session


def code(response: httpx.Response) -> str:
    return str(response.json()["error"]["code"])


@pytest.mark.integration
@pytest.mark.anyio
async def test_contracts_are_the_registry_projection(
    client: httpx.AsyncClient,
) -> None:
    response = await client.get("/api/slice/contracts")
    assert response.status_code == 200
    contracts = response.json()["contracts"]
    assert [c["type"] for c in contracts] == [
        d.type_id for d in SLICE_REGISTRY.definitions
    ]
    for contract, definition in zip(contracts, SLICE_REGISTRY.definitions, strict=True):
        assert contract["label"] == definition.display.label
        assert contract["description"] == definition.display.description
        for side in ("inputs", "outputs"):
            assert contract[side] == [
                {
                    "key": port.key,
                    "nominalType": port.nominal_type,
                    "label": port.display.label,
                    "cardinality": port.cardinality,
                    "required": port.required,
                }
                for port in getattr(definition, side)
            ]
        assert [p["key"] for p in contract["parameters"]] == [
            p.key for p in definition.parameters
        ]
        for data, parameter in zip(
            contract["parameters"], definition.parameters, strict=True
        ):
            assert data["kind"] == parameter.value_kind
            assert data["required"] == parameter.required
            assert data["label"] == parameter.display.label
            assert data["default"] == parameter.default
            assert data["constraints"] == dict(parameter.constraints)
    assert "region" not in response.text.lower()


@pytest.mark.integration
@pytest.mark.anyio
async def test_validate_returns_phase_one_findings_and_allocates_nothing(
    client: httpx.AsyncClient,
) -> None:
    before = runs()
    ok = await client.post(
        "/api/slice/validate",
        content=fixture_text("slice-success-v1.json"),
        headers=JSON,
    )
    assert ok.status_code == 200
    assert ok.json() == {"valid": True, "diagnostics": []}
    document = json.loads(fixture_text("slice-success-v1.json"))
    document["nodes"][3]["parameters"]["regularization"] = 0.0
    document["edges"][3]["target"]["portKey"] = "split"
    bad = await client.post(
        "/api/slice/validate", content=json.dumps(document), headers=JSON
    )
    assert bad.status_code == 200
    assert bad.json()["valid"] is False
    codes = {item["code"] for item in bad.json()["diagnostics"]}
    assert "VIDAP-PARAMETER-CONSTRAINT-VIOLATION" in codes
    assert len(codes) >= 2 and all(c.startswith("VIDAP-") for c in codes)
    item = bad.json()["diagnostics"][0]
    assert set(item) == {
        "code",
        "severity",
        "category",
        "elementKind",
        "elementReference",
        "message",
        "remedy",
        "jsonPointer",
    }
    undecodable = await client.post(
        "/api/slice/validate", content='{"format": "other"}', headers=JSON
    )
    assert undecodable.status_code == 422
    assert code(undecodable) == "invalid-workflow"
    assert undecodable.json()["diagnostics"][0]["code"].startswith("VIDAP-")
    assert runs() == before


@pytest.mark.integration
@pytest.mark.anyio
async def test_run_returns_only_the_recorded_metrics(
    client: httpx.AsyncClient, cleanup: list[str]
) -> None:
    response = await client.post(
        "/api/slice/run",
        content=fixture_text("slice-success-v1.json"),
        headers=JSON,
    )
    assert response.status_code == 200
    body = response.json()
    cleanup.append(body["attemptId"])
    assert body["outcome"] == "succeeded"
    assert body["metrics"] == expected_metrics()
    slot = (_directory(body["attemptId"]) / "proof-output.bin").read_bytes()
    assert json.loads(slot) == body["metrics"]
    assert [node["status"] for node in body["nodes"]] == ["completed"] * 5
    assert body["diagnostics"] == []
    plan = plan_execution(
        fixture("slice-success-v1.json"), SLICE_REGISTRY, SLICE_BINDINGS
    )
    assert body["semanticDigest"] == plan.representation.semantic_digest


@pytest.mark.integration
@pytest.mark.anyio
async def test_failed_run_reports_its_cause_and_no_metrics(
    client: httpx.AsyncClient, cleanup: list[str]
) -> None:
    response = await client.post(
        "/api/slice/run",
        content=fixture_text("slice-bypass-prepare-v1.json"),
        headers=JSON,
    )
    body = response.json()
    cleanup.append(body["attemptId"])
    assert response.status_code == 200
    assert body["outcome"] == "failed"
    assert body["metrics"] is None
    (diagnostic,) = body["diagnostics"]
    assert diagnostic["code"] == "unencoded-category-input"
    assert diagnostic["nodeId"] == "43000000-0000-4000-8000-000000000004"
    assert "Prepare Data" in diagnostic["remedy"]


@pytest.mark.integration
@pytest.mark.anyio
async def test_publication_problems_never_return_metrics(
    client: httpx.AsyncClient, cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    text = fixture_text("slice-success-v1.json")

    def fail_write(attempt_id: str, data: bytes) -> None:
        raise OSError("private write failure")

    with monkeypatch.context() as patch:
        patch.setattr(run_module, "write_proof_slot", fail_write)
        failed = await client.post("/api/slice/run", content=text, headers=JSON)
    cleanup.append(failed.json()["attemptId"])
    assert failed.json()["outcome"] == "failed"
    assert failed.json()["metrics"] is None
    assert "private" not in failed.text

    original = run_module.write_proof_slot

    def write_noncanonical(attempt_id: str, data: bytes) -> None:
        original(attempt_id, data.replace(b",", b", ", 1))

    with monkeypatch.context() as patch:
        patch.setattr(run_module, "write_proof_slot", write_noncanonical)
        tampered = await client.post("/api/slice/run", content=text, headers=JSON)
    assert tampered.status_code == 500
    assert code(tampered) == "metrics-readback-failed"
    assert "metrics" not in tampered.json()
    cleanup.append(tampered.json()["attemptId"])

    attempt = str(uuid.uuid4())

    def indeterminate(document: object) -> object:
        raise PublicationIndeterminate(attempt)

    with monkeypatch.context() as patch:
        patch.setattr(slice_api, "run_slice_attempt", indeterminate)
        unknown = await client.post("/api/slice/run", content=text, headers=JSON)
    assert unknown.status_code == 500
    assert unknown.json() == {
        "error": {
            "code": "publication-indeterminate",
            "message": slice_api._ERRORS["publication-indeterminate"][1],
        },
        "attemptId": attempt,
    }


@pytest.mark.integration
@pytest.mark.anyio
async def test_invalid_and_refused_runs_allocate_nothing(
    client: httpx.AsyncClient,
) -> None:
    before = runs()
    document = json.loads(fixture_text("slice-success-v1.json"))
    document["nodes"][3]["parameters"]["regularization"] = 0.0
    invalid = await client.post(
        "/api/slice/run", content=json.dumps(document), headers=JSON
    )
    assert invalid.status_code == 422
    assert code(invalid) == "invalid-workflow"
    assert invalid.json()["diagnostics"]
    no_evaluate = json.loads(fixture_text("slice-success-v1.json"))
    no_evaluate["nodes"] = no_evaluate["nodes"][:4]
    no_evaluate["edges"] = [
        e
        for e in no_evaluate["edges"]
        if e["target"]["nodeId"] != "41000000-0000-4000-8000-000000000005"
    ]
    refused = await client.post(
        "/api/slice/run", content=json.dumps(no_evaluate), headers=JSON
    )
    assert refused.status_code == 422
    assert code(refused) == "run-refused"
    assert runs() == before


@pytest.mark.integration
@pytest.mark.anyio
async def test_a_second_run_is_refused_not_queued(
    client: httpx.AsyncClient,
) -> None:
    before = runs()
    assert slice_api.RUN_LOCK.acquire(blocking=False)
    try:
        busy = await client.post(
            "/api/slice/run",
            content=fixture_text("slice-success-v1.json"),
            headers=JSON,
        )
    finally:
        slice_api.RUN_LOCK.release()
    assert busy.status_code == 409
    assert code(busy) == "busy"
    assert runs() == before


@pytest.mark.integration
@pytest.mark.anyio
@pytest.mark.parametrize(
    "host", ["testserver", "evil.example", "127.0.0.2", "localhost.evil"]
)
async def test_foreign_hosts_are_refused(host: str) -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(
        transport=transport, base_url=f"http://{host}:8000"
    ) as session:
        response = await session.get("/api/slice/contracts")
        status = await session.get("/api/status")
    assert response.status_code == 400
    assert code(response) == "invalid-host"
    assert status.status_code == 200


@pytest.mark.integration
@pytest.mark.anyio
async def test_localhost_name_and_allowed_origins_are_accepted(
    isolated_workflows: Path,
) -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(
        transport=transport, base_url="http://localhost:5173"
    ) as session:
        for origin in ("http://127.0.0.1:5173", "http://127.0.0.1:8000"):
            response = await session.get(
                "/api/slice/workflows", headers={"origin": origin}
            )
            assert response.status_code == 200
            assert "access-control-allow-origin" not in response.headers


@pytest.mark.integration
@pytest.mark.anyio
@pytest.mark.parametrize(
    "origin",
    [
        "http://evil.example",
        "null",
        "http://localhost:5173",
        "http://127.0.0.1:5174",
        "",
    ],
)
async def test_foreign_origins_are_refused(
    client: httpx.AsyncClient, origin: str
) -> None:
    before = runs()
    response = await client.post(
        "/api/slice/run",
        content=fixture_text("slice-success-v1.json"),
        headers={**JSON, "origin": origin},
    )
    assert response.status_code == 403
    assert code(response) == "origin-refused"
    assert "access-control-allow-origin" not in response.headers
    assert runs() == before


@pytest.mark.integration
@pytest.mark.anyio
@pytest.mark.parametrize(
    "content_type",
    [None, "text/plain", "application/json; charset=latin-1", "application/jsonx"],
)
async def test_only_json_bodies_are_read(
    client: httpx.AsyncClient, content_type: str | None
) -> None:
    headers = {} if content_type is None else {"content-type": content_type}
    response = await client.post(
        "/api/slice/validate",
        content=fixture_text("slice-success-v1.json"),
        headers=headers,
    )
    assert response.status_code == 415
    assert code(response) == "unsupported-content-type"
    charset = await client.post(
        "/api/slice/validate",
        content=fixture_text("slice-success-v1.json"),
        headers={"content-type": "Application/JSON; Charset=UTF-8"},
    )
    assert charset.status_code == 200


@pytest.mark.integration
@pytest.mark.anyio
async def test_size_and_encoding_limits(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    before = runs()
    large = await client.post(
        "/api/slice/run", content=b" " * (256 * 1024 + 1), headers=JSON
    )
    assert large.status_code == 413
    assert code(large) == "body-too-large"

    async def chunks() -> AsyncIterator[bytes]:
        for _ in range(5):
            yield b" " * (64 * 1024)

    streamed = await client.post("/api/slice/run", content=chunks(), headers=JSON)
    assert streamed.status_code == 413
    bad_utf8 = await client.post("/api/slice/run", content=b"\xff\xfe", headers=JSON)
    assert bad_utf8.status_code == 400
    assert code(bad_utf8) == "malformed-json"
    for body in (b"{", b'{"a": NaN}', b'{"a": 1, "a": 2}'):
        response = await client.put(
            "/api/slice/workflows/example", content=body, headers=JSON
        )
        assert response.status_code == 400
        assert code(response) == "malformed-json"
    assert runs() == before
    assert not isolated_workflows.exists()


@pytest.mark.integration
@pytest.mark.anyio
async def test_errors_never_echo_input_or_documentation(
    client: httpx.AsyncClient,
) -> None:
    response = await client.post(
        "/api/slice/validate",
        content=b'{"format": "secret-value-123"}',
        headers=JSON,
    )
    assert "secret-value-123" not in response.text
    for path in ("/docs", "/openapi.json", "/redoc"):
        assert (await client.get(path)).status_code == 404
    preflight = await client.options(
        "/api/slice/run",
        headers={
            "origin": "http://127.0.0.1:5173",
            "access-control-request-method": "POST",
        },
    )
    assert "access-control-allow-origin" not in preflight.headers
