"""Real first-party slice operations through the accepted attempt layer."""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression as LibraryLogisticRegression
from sklearn.model_selection import train_test_split

from vidap_execution import slice as slice_module
from vidap_execution.artifacts import _directory, remove_attempt
from vidap_execution.dispatch import preflight_dispatch
from vidap_execution.output import ReferenceOutputRefusal
from vidap_execution.planner import plan_execution
from vidap_execution.representation import PreparationFailure
from vidap_execution.slice import (
    BINDING_REVISION,
    SLICE_BINDINGS,
    SLICE_REGISTRY,
    SLICE_RUNTIME_TABLE,
    run_slice_attempt,
)
from vidap_workflow import (
    Edge,
    Endpoint,
    LayoutMetadata,
    Position,
    WorkflowDocument,
    WorkflowNode,
    deserialize_document,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "fixtures" / "p3-ep03b"
DATASET = 1
PREPARE = 2
SPLIT = 3
MODEL = 4
EVALUATE = 5


def node_id(index: int, prefix: str = "41") -> str:
    return f"{prefix}000000-0000-4000-8000-00000000000{index}"


def fixture(name: str) -> WorkflowDocument:
    return deserialize_document((FIXTURES / name).read_text(encoding="utf-8"))


def with_parameter(
    document: WorkflowDocument, index: int, key: str, value: object
) -> WorkflowDocument:
    target = node_id(index)
    nodes = tuple(
        replace(node, parameters={**node.parameters, key: value})
        if node.id == target
        else node
        for node in document.nodes
    )
    return replace(document, nodes=nodes)


def expected_metrics(
    *,
    fill: float = 0.0,
    fraction: float = 0.25,
    seed: int = 0,
    regularization: float = 1.0,
) -> dict[str, object]:
    """Independent calculation straight from the CSV, not through the handlers."""

    text = (FIXTURES / "slice-dataset-v1.csv").read_text(encoding="utf-8")
    rows = list(csv.reader(io.StringIO(text)))[1:]
    x = np.array(
        [
            [float(a), float(b) if b else fill]
            + [1.0 if segment == name else 0.0 for name in ("north", "south", "east")]
            for a, b, segment, _ in rows
        ]
    )
    y = np.array([int(row[3]) for row in rows])
    train, test = train_test_split(
        list(range(len(rows))),
        test_size=fraction,
        random_state=seed,
        stratify=list(y),
    )
    fitted = LibraryLogisticRegression(C=regularization).fit(x[train], y[train])
    correct = int((fitted.predict(x[test]) == y[test]).sum())
    return {
        "accuracy": correct / len(test),
        "correct": correct,
        "format": "vidap.slice-metrics",
        "schemaVersion": "1.0",
        "testRows": len(test),
    }


def recorded_metrics(attempt_id: str) -> dict[str, object]:
    data = (_directory(attempt_id) / "proof-output.bin").read_bytes()
    parsed = json.loads(data)
    assert isinstance(parsed, dict)
    assert data == json.dumps(
        parsed, separators=(",", ":"), sort_keys=True, ensure_ascii=False
    ).encode("utf-8")
    return parsed


def runs() -> set[str]:
    root = ROOT / ".vidap-local" / "runs"
    return {path.name for path in root.iterdir()} if root.is_dir() else set()


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
def test_static_family_prepares_with_one_exact_revision() -> None:
    assert SLICE_BINDINGS.revision == BINDING_REVISION
    assert {b.revision for b in SLICE_BINDINGS.bindings} == {BINDING_REVISION}
    assert {r.binding_revision for r in SLICE_RUNTIME_TABLE.registrations} == {
        BINDING_REVISION
    }
    assert {d.type_id for d in SLICE_REGISTRY.definitions} == {
        "vidap.slice.dataset",
        "vidap.slice.prepare",
        "vidap.slice.split",
        "vidap.slice.model",
        "vidap.slice.evaluate",
    }
    plan = plan_execution(
        fixture("slice-success-v1.json"), SLICE_REGISTRY, SLICE_BINDINGS
    )
    preflight_dispatch(plan, SLICE_RUNTIME_TABLE)
    model = next(
        d for d in SLICE_REGISTRY.definitions if d.type_id == "vidap.slice.model"
    )
    assert "logistic regression" in (model.display.description or "")


@pytest.mark.unit
def test_success_matches_independent_calculation(cleanup: list[str]) -> None:
    result = run_slice_attempt(fixture("slice-success-v1.json"))
    data = result.record.data
    cleanup.append(str(data["attemptId"]))
    assert data["outcome"] == "succeeded"
    assert len(data["completedNodeIds"]) == 5
    assert data["artifacts"] == ("record.json", "proof-output.bin")
    recorded = recorded_metrics(str(data["attemptId"]))
    assert recorded == expected_metrics()
    manifest = json.loads((FIXTURES / "fixture-manifest.json").read_text("utf-8"))
    reviewed = manifest["fixtures"][1]["expectedResult"]["metrics"]
    assert {key: recorded[key] for key in reviewed} == {
        key: reviewed[key] for key in ("accuracy", "correct", "testRows")
    }
    reused = {
        event["consumerNodeId"]
        for event in data["reuseEvents"]
        if event["kind"] == "reused-within-attempt"
        and event["sourceNodeId"] == node_id(SPLIT)
    }
    assert reused == {node_id(MODEL), node_id(EVALUATE)}
    computed = [
        event
        for event in data["reuseEvents"]
        if event["kind"] == "computed" and event["sourceNodeId"] == node_id(SPLIT)
    ]
    assert len(computed) == 1


@pytest.mark.unit
def test_regularization_reaches_the_library_call(
    cleanup: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: list[float] = []

    class Spy(LibraryLogisticRegression):
        def __init__(self, *, C: float) -> None:
            seen.append(C)
            super().__init__(C=C)

    monkeypatch.setattr(slice_module, "LogisticRegression", Spy)
    base = fixture("slice-success-v1.json")
    default = run_slice_attempt(base)
    strong = run_slice_attempt(with_parameter(base, MODEL, "regularization", 0.0001))
    for result in (default, strong):
        cleanup.append(str(result.record.data["attemptId"]))
    assert seen == [1.0, 0.0001]
    default_metrics = recorded_metrics(str(default.record.data["attemptId"]))
    strong_metrics = recorded_metrics(str(strong.record.data["attemptId"]))
    assert strong_metrics == expected_metrics(regularization=0.0001)
    assert strong_metrics["accuracy"] != default_metrics["accuracy"]
    manifest = json.loads((FIXTURES / "fixture-manifest.json").read_text("utf-8"))
    expected = manifest["fixtures"][1]["expectedResult"]
    assert {
        key: strong_metrics[key] for key in ("accuracy", "correct", "testRows")
    } == (expected["metricsWithRegularization0.0001"])


@pytest.mark.unit
def test_repeat_recomputes_and_meaning_changes_change_the_digest(
    cleanup: list[str],
) -> None:
    base = fixture("slice-success-v1.json")
    first = run_slice_attempt(base)
    second = run_slice_attempt(base)
    ids = [str(r.record.data["attemptId"]) for r in (first, second)]
    cleanup.extend(ids)
    assert ids[0] != ids[1]
    assert (_directory(ids[0]) / "proof-output.bin").read_bytes() == (
        _directory(ids[1]) / "proof-output.bin"
    ).read_bytes()
    digest = first.record.data["semanticDigest"]
    assert second.record.data["semanticDigest"] == digest
    for index, key, value in (
        (SPLIT, "seed", 7),
        (SPLIT, "test_fraction", 0.3),
        (PREPARE, "missing_fill", 1.5),
    ):
        changed = plan_execution(
            with_parameter(base, index, key, value), SLICE_REGISTRY, SLICE_BINDINGS
        )
        assert changed.representation.semantic_digest != digest
    relabelled = replace(
        base,
        nodes=tuple(replace(node, label="Renamed") for node in base.nodes),
        layout=LayoutMetadata({node_id(DATASET): Position(10, 20)}),
    )
    unchanged = plan_execution(relabelled, SLICE_REGISTRY, SLICE_BINDINGS)
    assert unchanged.representation.semantic_digest == digest
    other = run_slice_attempt(with_parameter(base, SPLIT, "seed", 7))
    cleanup.append(str(other.record.data["attemptId"]))
    assert recorded_metrics(str(other.record.data["attemptId"])) == expected_metrics(
        seed=7
    )


def _without(document: WorkflowDocument, index: int) -> WorkflowDocument:
    target = node_id(index)
    return replace(
        document,
        nodes=tuple(n for n in document.nodes if n.id != target),
        edges=tuple(
            e
            for e in document.edges
            if target not in (e.source.node_id, e.target.node_id)
        ),
    )


@pytest.mark.unit
def test_refusals_happen_before_any_allocation(cleanup: list[str]) -> None:
    base = fixture("slice-success-v1.json")
    before = runs()
    with pytest.raises(ReferenceOutputRefusal):
        run_slice_attempt(_without(base, EVALUATE))
    duplicate = replace(
        base,
        nodes=(
            *base.nodes,
            WorkflowNode(node_id(6), "vidap.slice.evaluate", parameters={}),
        ),
        edges=(
            *base.edges,
            Edge(
                "42000000-0000-4000-8000-000000000009",
                Endpoint(node_id(MODEL), "model"),
                Endpoint(node_id(6), "model"),
            ),
            Edge(
                "42000000-0000-4000-8000-00000000000a",
                Endpoint(node_id(SPLIT), "split"),
                Endpoint(node_id(6), "split"),
            ),
        ),
    )
    with pytest.raises(ReferenceOutputRefusal):
        run_slice_attempt(duplicate)
    wrong_type = replace(
        _without(base, MODEL),
        edges=(
            *_without(base, MODEL).edges,
            Edge(
                "42000000-0000-4000-8000-00000000000b",
                Endpoint(node_id(SPLIT), "split"),
                Endpoint(node_id(EVALUATE), "model"),
            ),
        ),
    )
    with pytest.raises(PreparationFailure):
        run_slice_attempt(wrong_type)
    for index, key, value in (
        (MODEL, "regularization", 0.0),
        (SPLIT, "test_fraction", 0.9),
        (SPLIT, "seed", -1),
    ):
        with pytest.raises(PreparationFailure):
            run_slice_attempt(with_parameter(base, index, key, value))
    assert runs() == before
