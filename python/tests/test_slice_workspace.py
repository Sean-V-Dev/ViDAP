"""Backend-owned workflow and sidecar files through the channel (D3.3, D3.4)."""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import httpx
import pytest
from test_slice_api import fixture_text
from test_slice_operations import fixture

from vidap_execution import workspace
from vidap_execution.app import create_app
from vidap_execution.artifacts import remove_attempt
from vidap_execution.planner import plan_execution
from vidap_execution.slice import SLICE_BINDINGS, SLICE_REGISTRY, run_slice_attempt
from vidap_workflow import deserialize_document, serialize_document

JSON = {"content-type": "application/json"}
SIDE = {
    "format": "vidap.workspace-view",
    "schemaVersion": "1.0",
    "regions": [{"key": "DATA", "width": 280}, {"key": "PREPARE", "width": 320}],
    "nodes": {
        "41000000-0000-4000-8000-000000000001": {"region": "DATA", "x": 24, "y": 40}
    },
    "viewport": {"x": 0, "y": 0, "zoom": 1},
}


ROOT = Path(__file__).resolve().parents[2]


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


def sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def document(**changes: object) -> dict[str, object]:
    data = json.loads(fixture_text("slice-success-v1.json"))
    if "regularization" in changes:
        data["nodes"][3]["parameters"]["regularization"] = changes["regularization"]
    return data


async def put(
    client: httpx.AsyncClient,
    name: str,
    workflow: object,
    sidecar: object = None,
    base: str | None = None,
    side_base: str | None = None,
) -> httpx.Response:
    return await client.put(
        f"/api/slice/workflows/{name}",
        content=json.dumps(
            {
                "workflow": workflow,
                "sidecar": sidecar,
                "baseWorkflowDigest": base,
                "baseSidecarDigest": side_base,
            }
        ),
        headers=JSON,
    )


@pytest.mark.integration
@pytest.mark.anyio
async def test_save_load_and_run_fidelity(
    client: httpx.AsyncClient, isolated_workflows: Path, cleanup: list[str]
) -> None:
    saved = await put(client, "slice-one", document(), SIDE)
    assert saved.status_code == 200
    on_disk = (isolated_workflows / "slice-one.vidap.json").read_bytes()
    assert on_disk == serialize_document(fixture("slice-success-v1.json")).encode()
    assert saved.json()["workflowDigest"] == sha(on_disk)
    side_disk = (isolated_workflows / "slice-one.vidap-view.json").read_bytes()
    assert saved.json()["sidecarDigest"] == sha(side_disk)
    assert not list(isolated_workflows.glob("*.tmp"))

    listed = await client.get("/api/slice/workflows")
    assert listed.json() == {
        "workflows": [
            {"name": "slice-one", "workflowDigest": sha(on_disk), "hasSidecar": True}
        ]
    }
    loaded = (await client.get("/api/slice/workflows/slice-one")).json()
    assert loaded["workflowDigest"] == sha(on_disk)
    assert loaded["sidecar"] == SIDE
    assert loaded["sidecarNotice"] is None

    original = await client.post(
        "/api/slice/run", content=fixture_text("slice-success-v1.json"), headers=JSON
    )
    reloaded = await client.post(
        "/api/slice/run", content=json.dumps(loaded["workflow"]), headers=JSON
    )
    headless = run_slice_attempt(deserialize_document(on_disk.decode()))
    cleanup.extend(
        [
            original.json()["attemptId"],
            reloaded.json()["attemptId"],
            str(headless.record.data["attemptId"]),
        ]
    )
    assert original.json()["semanticDigest"] == reloaded.json()["semanticDigest"]
    assert headless.record.data["semanticDigest"] == original.json()["semanticDigest"]
    assert original.json()["metrics"] == reloaded.json()["metrics"]

    moved = json.loads(json.dumps(SIDE))
    moved["regions"][0]["width"] = 600
    moved["nodes"]["41000000-0000-4000-8000-000000000001"]["x"] = 300
    resaved = await put(
        client,
        "slice-one",
        loaded["workflow"],
        moved,
        loaded["workflowDigest"],
        loaded["sidecarDigest"],
    )
    assert resaved.status_code == 200
    assert resaved.json()["workflowDigest"] == loaded["workflowDigest"]
    assert resaved.json()["sidecarDigest"] != loaded["sidecarDigest"]
    again = (await client.get("/api/slice/workflows/slice-one")).json()
    plan = plan_execution(
        deserialize_document(json.dumps(again["workflow"])),
        SLICE_REGISTRY,
        SLICE_BINDINGS,
    )
    assert plan.representation.semantic_digest == original.json()["semanticDigest"]


@pytest.mark.integration
@pytest.mark.anyio
async def test_conflicts_refuse_the_whole_save_and_explain_why(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    first = (await put(client, "shared", document(), SIDE)).json()
    workflow_path = isolated_workflows / "shared.vidap.json"
    sidecar_path = isolated_workflows / "shared.vidap-view.json"

    no_base = await put(client, "shared", document())
    assert no_base.status_code == 409
    assert no_base.json()["error"]["code"] == "conflict"

    outside = deserialize_document(fixture_text("slice-success-v1.json"))
    outside_text = json.loads(serialize_document(outside))
    outside_text["nodes"][3]["parameters"]["regularization"] = 0.5
    outside_text["nodes"] = outside_text["nodes"][:4]
    outside_text["edges"] = [
        e
        for e in outside_text["edges"]
        if e["target"]["nodeId"] != "41000000-0000-4000-8000-000000000005"
    ]
    workflow_path.write_text(json.dumps(outside_text), encoding="utf-8")
    before = (workflow_path.read_bytes(), sidecar_path.read_bytes())

    stale = await put(
        client,
        "shared",
        document(regularization=2.0),
        SIDE,
        first["workflowDigest"],
        first["sidecarDigest"],
    )
    assert stale.status_code == 409
    body = stale.json()
    assert body["workflowDigest"] == sha(before[0])
    summary = body["summary"]
    assert summary["nodesRemoved"] == [
        {
            "nodeId": "41000000-0000-4000-8000-000000000005",
            "type": "vidap.slice.evaluate",
        }
    ]
    assert {
        "nodeId": "41000000-0000-4000-8000-000000000004",
        "key": "regularization",
        "before": 2.0,
        "after": 0.5,
    } in summary["parametersChanged"]
    assert len(summary["edgesRemoved"]) == 2
    assert (workflow_path.read_bytes(), sidecar_path.read_bytes()) == before

    compared = await client.post(
        "/api/slice/workflows/shared/compare",
        content=json.dumps(
            {
                "workflow": document(regularization=2.0),
                "baseWorkflowDigest": first["workflowDigest"],
                "baseSidecarDigest": first["sidecarDigest"],
            }
        ),
        headers=JSON,
    )
    assert compared.json()["changed"] is True
    assert compared.json()["summary"] == summary

    current = sha(before[0])
    sidecar_path.write_text(json.dumps(SIDE) + " ", encoding="utf-8")
    side_stale = await put(
        client, "shared", document(), SIDE, current, first["sidecarDigest"]
    )
    assert side_stale.status_code == 409
    assert workflow_path.read_bytes() == before[0]

    unchanged = await client.post(
        "/api/slice/workflows/shared/compare",
        content=json.dumps(
            {
                "workflow": document(),
                "baseWorkflowDigest": current,
                "baseSidecarDigest": sha(sidecar_path.read_bytes()),
            }
        ),
        headers=JSON,
    )
    assert unchanged.json()["changed"] is False
    assert unchanged.json()["summary"] is None

    workflow_path.unlink()
    removed = await put(
        client, "shared", document(), None, current, sha(sidecar_path.read_bytes())
    )
    assert removed.status_code == 409
    assert removed.json()["missing"] is True
    assert removed.json()["summary"] is None
    assert not workflow_path.exists()


@pytest.mark.integration
@pytest.mark.anyio
async def test_load_refuses_bad_files_without_repair(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    isolated_workflows.mkdir(parents=True)
    unsupported = json.loads(fixture_text("slice-success-v1.json"))
    unsupported["schemaVersion"] = "2.0"
    unknown = json.loads(fixture_text("slice-success-v1.json"))
    unknown["nodes"][0]["type"] = "vidap.slice.unknown"
    files = {
        "malformed": b"{ not json",
        "unsupported": json.dumps(unsupported).encode(),
        "invalid": json.dumps(unknown).encode(),
        "undecodable": b"\xff\xfe\x00",
    }
    for name, data in files.items():
        (isolated_workflows / f"{name}.vidap.json").write_bytes(data)
        response = await client.get(f"/api/slice/workflows/{name}")
        assert response.status_code == 422, name
        assert response.json()["error"]["code"] == "invalid-workflow"
        assert response.json()["diagnostics"][0]["code"].startswith("VIDAP-")
        assert (isolated_workflows / f"{name}.vidap.json").read_bytes() == data
    large = isolated_workflows / "large.vidap.json"
    large.write_bytes(b" " * (256 * 1024 + 1))
    too_large = await client.get("/api/slice/workflows/large")
    assert too_large.status_code == 413
    assert too_large.json()["error"]["code"] == "workflow-too-large"
    missing = await client.get("/api/slice/workflows/absent")
    assert missing.status_code == 404


@pytest.mark.integration
@pytest.mark.anyio
async def test_bad_sidecars_degrade_and_layout_round_trips(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    with_layout = document()
    with_layout["layout"] = {
        "nodePositions": {"41000000-0000-4000-8000-000000000001": {"x": 5, "y": 7.5}}
    }
    saved = await put(client, "laid-out", with_layout)
    assert saved.status_code == 200
    loaded = (await client.get("/api/slice/workflows/laid-out")).json()
    assert loaded["workflow"]["layout"] == with_layout["layout"]
    side = isolated_workflows / "laid-out.vidap-view.json"
    for content, notice in (
        (b"{ broken", "unreadable"),
        (json.dumps({**SIDE, "schemaVersion": "2.0"}).encode(), "unsupported"),
        (json.dumps({**SIDE, "extra": 1}).encode(), "unreadable"),
        (b" " * (64 * 1024 + 1), "unreadable"),
    ):
        side.write_bytes(content)
        response = (await client.get("/api/slice/workflows/laid-out")).json()
        assert response["sidecar"] is None
        assert response["sidecarNotice"] == notice
        assert response["sidecarDigest"] == sha(content)
        assert response["workflowDigest"] == loaded["workflowDigest"]


@pytest.mark.integration
@pytest.mark.anyio
@pytest.mark.parametrize(
    "sidecar",
    [
        {**SIDE, "extra": True},
        {**SIDE, "regions": [{"key": "bad key", "width": 300}]},
        {**SIDE, "regions": [{"key": "A", "width": 10}]},
        {**SIDE, "regions": [{"key": "A", "width": 300}, {"key": "A", "width": 300}]},
        {**SIDE, "nodes": {"not-a-uuid": {"region": "A", "x": 0, "y": 0}}},
        {
            **SIDE,
            "nodes": {
                "41000000-0000-4000-8000-000000000001": {
                    "region": "A",
                    "x": 1e9,
                    "y": 0,
                }
            },
        },
        {**SIDE, "viewport": {"x": 0, "y": 0, "zoom": 9}},
        {**SIDE, "viewport": {"x": 0, "y": 0, "zoom": True}},
        {**SIDE, "format": "other"},
        [],
    ],
)
async def test_sidecar_shape_is_enforced(
    client: httpx.AsyncClient, isolated_workflows: Path, sidecar: object
) -> None:
    response = await put(client, "shape", document(), sidecar)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid-sidecar"
    assert not (isolated_workflows / "shape.vidap.json").exists()


@pytest.mark.integration
@pytest.mark.anyio
@pytest.mark.parametrize(
    ("name", "status"),
    [
        ("UPPER", 400),
        ("a_b", 400),
        ("-a", 400),
        ("a-", 400),
        ("x" * 65, 400),
        ("%2e%2e", 400),
        ("a.b", 400),
        # Windows reserved device names are refused on every platform.
        ("con", 400),
        ("nul", 400),
        ("com1", 400),
        ("lpt9", 400),
        # An encoded separator never matches a slice route at all.
        ("con%2Fx", 404),
    ],
)
async def test_invalid_names_are_refused(
    client: httpx.AsyncClient, isolated_workflows: Path, name: str, status: int
) -> None:
    for response in (
        await client.get(f"/api/slice/workflows/{name}"),
        await put(client, name, document()),
    ):
        assert response.status_code == status
        if status == 400:
            assert response.json()["error"]["code"] == "invalid-name"
    assert not isolated_workflows.exists() or not any(isolated_workflows.iterdir())
    assert workspace.check_name("a") == "a"
    assert workspace.check_name("a" * 64) == "a" * 64


@pytest.mark.integration
@pytest.mark.anyio
async def test_requests_need_exact_fields_and_digests(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    for body in (
        {"workflow": document()},
        {
            "workflow": document(),
            "sidecar": None,
            "baseWorkflowDigest": "md5:abc",
            "baseSidecarDigest": None,
        },
        {
            "workflow": [],
            "sidecar": None,
            "baseWorkflowDigest": None,
            "baseSidecarDigest": None,
        },
    ):
        response = await client.put(
            "/api/slice/workflows/fields", content=json.dumps(body), headers=JSON
        )
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "invalid-request"
    invalid = await put(client, "fields", document(regularization=0.0))
    assert invalid.status_code == 422
    assert invalid.json()["error"]["code"] == "invalid-workflow"
    assert not isolated_workflows.exists() or not any(isolated_workflows.iterdir())


@pytest.mark.integration
@pytest.mark.anyio
async def test_storage_refuses_links_leftovers_and_stray_names(
    client: httpx.AsyncClient, isolated_workflows: Path, tmp_path: Path
) -> None:
    saved = await put(client, "safe", document())
    assert saved.status_code == 200
    (isolated_workflows / "Stray_Name.vidap.json").write_text("{}", encoding="utf-8")
    (isolated_workflows / "notes.txt").write_text("x", encoding="utf-8")
    listed = (await client.get("/api/slice/workflows")).json()["workflows"]
    assert [item["name"] for item in listed] == ["safe"]

    leftover = isolated_workflows / "safe.vidap.json.tmp"
    leftover.write_bytes(b"other")
    blocked = await put(
        client,
        "safe",
        document(regularization=3.0),
        None,
        saved.json()["workflowDigest"],
    )
    assert blocked.status_code == 500
    assert blocked.json()["error"]["code"] == "storage-refused"
    assert leftover.read_bytes() == b"other"
    assert (isolated_workflows / "safe.vidap.json").read_bytes() == serialize_document(
        fixture("slice-success-v1.json")
    ).encode()
    leftover.unlink()

    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        os.symlink(outside / "x.vidap.json", isolated_workflows / "linked.vidap.json")
    except OSError:
        pytest.skip("symlinks are not permitted on this host")
    linked = await client.get("/api/slice/workflows/linked")
    assert linked.status_code == 500
    assert linked.json()["error"]["code"] == "storage-refused"
    target = tmp_path / "elsewhere"
    target.mkdir()
    for entry in isolated_workflows.iterdir():
        entry.unlink()
    isolated_workflows.rmdir()
    os.symlink(target, isolated_workflows, target_is_directory=True)
    escaped = await put(client, "escape", document())
    assert escaped.status_code == 500
    assert escaped.json()["error"]["code"] == "storage-refused"
    assert not any(target.iterdir())


DEEP = "[" * 50000 + "]" * 50000


@pytest.mark.integration
@pytest.mark.anyio
async def test_crafted_bodies_keep_the_error_envelope(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    """R1: recursion, overflowing floats, and huge integers never escape."""

    bodies = {
        "deep wrapper": '{"workflow": ' + DEEP + "}",
        "overflowing float in workflow": json.dumps(
            {
                "workflow": document(),
                "sidecar": None,
                "baseWorkflowDigest": None,
                "baseSidecarDigest": None,
            }
        ).replace('"regularization": 1.0', '"regularization": 1e400'),
        "deep sidecar": json.dumps(
            {
                "workflow": document(),
                "sidecar": None,
                "baseWorkflowDigest": None,
                "baseSidecarDigest": None,
            }
        ).replace('"sidecar": null', '"sidecar": ' + DEEP),
    }
    assert "1e400" in bodies["overflowing float in workflow"]
    for label, body in bodies.items():
        for response in (
            await client.put(
                "/api/slice/workflows/crafted", content=body, headers=JSON
            ),
            await client.post(
                "/api/slice/workflows/crafted/compare", content=body, headers=JSON
            ),
        ):
            assert response.status_code == 400, label
            assert response.json()["error"]["code"] == "malformed-json", label
    huge = json.loads(json.dumps(SIDE))
    huge["nodes"]["41000000-0000-4000-8000-000000000001"]["x"] = 10**400
    response = await put(client, "crafted", document(), huge)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid-sidecar"
    for value in (10**400, -(10**400), 2**63, 100001, -100001):
        huge["nodes"]["41000000-0000-4000-8000-000000000001"]["x"] = value
        response = await put(client, "crafted", document(), huge)
        assert response.json()["error"]["code"] == "invalid-sidecar"
    assert not isolated_workflows.exists() or not any(isolated_workflows.iterdir())


@pytest.mark.integration
@pytest.mark.anyio
async def test_crafted_files_on_disk_still_load_or_refuse_cleanly(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    """R1 / AC10: a hostile sidecar degrades; a hostile workflow is refused."""

    saved = await put(client, "on-disk", document())
    assert saved.status_code == 200
    side = isolated_workflows / "on-disk.vidap-view.json"
    huge_side = json.dumps(SIDE).replace('"x": 24', '"x": ' + "9" * 400)
    assert "9" * 400 in huge_side
    for content in (huge_side, DEEP, '{"a": ' + DEEP + "}"):
        side.write_text(content, encoding="utf-8")
        response = await client.get("/api/slice/workflows/on-disk")
        assert response.status_code == 200
        assert response.json()["sidecar"] is None
        assert response.json()["sidecarNotice"] == "unreadable"
    side.unlink()
    workflow = isolated_workflows / "on-disk.vidap.json"
    for content in (DEEP, '{"format": ' + DEEP + "}"):
        workflow.write_text(content, encoding="utf-8")
        response = await client.get("/api/slice/workflows/on-disk")
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "invalid-workflow"
        assert workflow.read_text(encoding="utf-8") == content
    workflow.write_bytes(b" " * (256 * 1024 + 1))
    compared = await client.post(
        "/api/slice/workflows/on-disk/compare",
        content=json.dumps(
            {
                "workflow": document(),
                "baseWorkflowDigest": None,
                "baseSidecarDigest": None,
            }
        ),
        headers=JSON,
    )
    assert compared.status_code == 413
    assert compared.json()["error"]["code"] == "workflow-too-large"
    oversized_digest = "sha256:" + hashlib.sha256(workflow.read_bytes()).hexdigest()
    resave = await put(client, "on-disk", document(), None, oversized_digest)
    assert resave.status_code == 413
    assert resave.json()["error"]["code"] == "workflow-too-large"
    assert workflow.stat().st_size == 256 * 1024 + 1


@pytest.mark.integration
@pytest.mark.anyio
async def test_a_stale_sidecar_temporary_refuses_the_whole_save(
    client: httpx.AsyncClient, isolated_workflows: Path
) -> None:
    """R2: no write happens unless both files can be written."""

    saved = (await put(client, "pair", document(), SIDE)).json()
    workflow = isolated_workflows / "pair.vidap.json"
    sidecar = isolated_workflows / "pair.vidap-view.json"
    before = (workflow.read_bytes(), sidecar.read_bytes())
    leftover = isolated_workflows / "pair.vidap-view.json.tmp"
    leftover.write_bytes(b"other")
    moved = json.loads(json.dumps(SIDE))
    moved["regions"][0]["width"] = 500
    response = await put(
        client,
        "pair",
        document(regularization=3.0),
        moved,
        saved["workflowDigest"],
        saved["sidecarDigest"],
    )
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "storage-refused"
    assert (workflow.read_bytes(), sidecar.read_bytes()) == before
    assert leftover.read_bytes() == b"other"
    leftover.unlink()
    retried = await put(
        client,
        "pair",
        document(regularization=3.0),
        moved,
        saved["workflowDigest"],
        saved["sidecarDigest"],
    )
    assert retried.status_code == 200
