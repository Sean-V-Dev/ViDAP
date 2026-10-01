"""Real first-party reference workflow and checked arithmetic proof."""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

from vidap_execution import (
    AttemptRefusal,
    BindingMap,
    run_attempt,
    run_reference_attempt,
)
from vidap_execution.artifacts import remove_attempt
from vidap_execution.dispatch import (
    DispatchRefusal,
    IncomingValue,
    RuntimeRegistration,
    RuntimeTable,
    preflight_dispatch,
)
from vidap_execution.output import ReferenceOutputRefusal
from vidap_execution.planner import plan_execution
from vidap_execution.reference import (
    BINDING_REVISION,
    REFERENCE_BINDINGS,
    REFERENCE_REGISTRY,
    REFERENCE_RUNTIME_TABLE,
    add,
    emit,
    literal,
    multiply,
)
from vidap_workflow import (
    Edge,
    Endpoint,
    LayoutMetadata,
    NodeRegistry,
    Position,
    WorkflowDecodeError,
    WorkflowDocument,
    WorkflowNode,
    deserialize_document,
)

ROOT = Path(__file__).resolve().parents[2]


def _fixture(name: str) -> WorkflowDocument:
    return deserialize_document(
        (ROOT / "fixtures" / "p2-ep05" / name).read_text(encoding="utf-8")
    )


def _owned(result: object) -> str:
    return result.record.data["attemptId"]  # type: ignore[attr-defined, no-any-return]


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
def test_approved_binding_equality_and_real_branch(cleanup: list[str]) -> None:
    doc = _fixture("branched-success-v1.json")
    assert REFERENCE_BINDINGS.revision == BINDING_REVISION
    assert {b.revision for b in REFERENCE_BINDINGS.bindings} == {BINDING_REVISION}
    assert {r.binding_revision for r in REFERENCE_RUNTIME_TABLE.registrations} == {
        BINDING_REVISION
    }
    plan = plan_execution(doc, REFERENCE_REGISTRY, REFERENCE_BINDINGS)
    preflight_dispatch(plan, REFERENCE_RUNTIME_TABLE)
    assert len(plan.schedule) == 5
    bad = BindingMap(BINDING_REVISION + ".bad", REFERENCE_BINDINGS.bindings)
    with pytest.raises(ValueError) as mismatch:
        plan_execution(doc, REFERENCE_REGISTRY, bad)
    assert mismatch.value.code == "binding-revision-mismatch"
    changed_runtime = RuntimeTable(
        REFERENCE_RUNTIME_TABLE.revision,
        (
            RuntimeRegistration(
                "vidap.reference.literal", BINDING_REVISION + ".bad", literal
            ),
            *REFERENCE_RUNTIME_TABLE.registrations[1:],
        ),
    )
    with pytest.raises(DispatchRefusal) as runtime_mismatch:
        preflight_dispatch(plan, changed_runtime)
    assert runtime_mismatch.value.code == "handler-revision-mismatch"
    names = {
        handler.__code__: handler.__name__ for handler in (literal, multiply, add, emit)
    }
    calls: list[str] = []

    def trace(frame: object, event: str, arg: object) -> None:
        if event == "call" and frame.f_code in names:  # type: ignore[attr-defined]
            calls.append(names[frame.f_code])  # type: ignore[attr-defined]

    sys.setprofile(trace)
    try:
        result = run_reference_attempt(doc)
    finally:
        sys.setprofile(None)
    assert calls == ["literal", "multiply", "multiply", "add", "emit"]
    cleanup.append(_owned(result))
    record = result.record.data
    assert record["outcome"] == "succeeded"
    assert record["completedNodeIds"] == plan.schedule
    assert record["contractSnapshotRef"] == plan.representation.contract_snapshot_ref
    assert result.dispatch_result is not None
    assert result.dispatch_result.port_results[(doc.nodes[-1].id, "value")] == 15
    events = record["reuseEvents"]
    assert sum(e["kind"] == "computed" for e in events) == 5
    assert sum(e["kind"] == "reused-within-attempt" for e in events) == 5
    assert (
        sum(
            e["sourceNodeId"] == doc.nodes[0].id and e["kind"] == "computed"
            for e in events
        )
        == 1
    )


def _linear(value: int = 4, factor: int = 5) -> WorkflowDocument:
    ids = [f"35000000-0000-4000-8000-{i:012d}" for i in range(1, 4)]
    nodes = (
        WorkflowNode(ids[0], "vidap.reference.literal", parameters={"value": value}),
        WorkflowNode(ids[1], "vidap.reference.multiply", parameters={"factor": factor}),
        WorkflowNode(ids[2], "vidap.reference.emit"),
    )
    edges = tuple(
        Edge(
            f"36000000-0000-4000-8000-{i:012d}",
            Endpoint(ids[i - 1], "value"),
            Endpoint(ids[i], "input"),
        )
        for i in (1, 2)
    )
    return WorkflowDocument("37000000-0000-4000-8000-000000000001", nodes, edges)


@pytest.mark.unit
def test_linear_order_repeat_and_changed_semantics(cleanup: list[str]) -> None:
    doc = _linear()
    altered = WorkflowDocument(
        doc.workflow_id,
        tuple(replace(n, label="Shown") for n in reversed(doc.nodes)),
        tuple(reversed(doc.edges)),
        layout=LayoutMetadata({doc.nodes[0].id: Position(2, 4)}),
    )
    results = [
        run_reference_attempt(item)
        for item in (doc, altered, doc, _linear(6), _linear(factor=6))
    ]
    cleanup.extend(_owned(item) for item in results)
    records = [item.record.data for item in results]
    assert len({_owned(item) for item in results}) == 5
    assert [
        item.dispatch_result.port_results[(doc.nodes[-1].id, "value")]
        for item in results
    ] == [20, 20, 20, 30, 24]
    assert len({records[i]["semanticDigest"] for i in range(3)}) == 1
    assert records[3]["semanticDigest"] != records[0]["semanticDigest"]
    assert records[4]["semanticDigest"] != records[0]["semanticDigest"]
    assert [e["compositeKey"] for e in records[0]["reuseEvents"]] == [
        e["compositeKey"] for e in records[1]["reuseEvents"]
    ]
    assert all(
        sum(e["kind"] == "computed" for e in r["reuseEvents"]) == 3 for r in records
    )
    assert (
        plan_execution(doc, REFERENCE_REGISTRY, REFERENCE_BINDINGS).schedule
        == plan_execution(altered, REFERENCE_REGISTRY, REFERENCE_BINDINGS).schedule
    )
    reversed_registry = NodeRegistry(tuple(reversed(REFERENCE_REGISTRY.definitions)))
    reversed_bindings = BindingMap(
        BINDING_REVISION, tuple(reversed(REFERENCE_BINDINGS.bindings))
    )
    reversed_plan = plan_execution(doc, reversed_registry, reversed_bindings)
    preflight_dispatch(
        reversed_plan,
        RuntimeTable(
            REFERENCE_RUNTIME_TABLE.revision,
            tuple(reversed(REFERENCE_RUNTIME_TABLE.registrations)),
        ),
    )
    assert reversed_plan.representation.semantic_digest == records[0]["semanticDigest"]


@pytest.mark.unit
def test_real_overflow_status_and_envelope(cleanup: list[str]) -> None:
    doc = _fixture("checked-overflow-v1.json")
    result = run_reference_attempt(doc)
    cleanup.append(_owned(result))
    record = result.record.data
    assert record["outcome"] == "failed" and record["artifacts"] == ("record.json",)
    assert [n["status"] for n in record["nodes"]] == [
        "completed",
        "completed",
        "failed",
        "blocked",
        "unrelated",
    ]
    assert len(record["attemptedNodeIds"]) == 3
    assert record["diagnostics"][0]["code"] == "handler-failed"
    assert record["diagnostics"][0]["technical"]["type"] == "OverflowError"
    assert result.dispatch_result is not None
    assert (doc.nodes[3].id, "value") not in result.dispatch_result.port_results
    assert (doc.nodes[4].id, "value") not in result.dispatch_result.port_results


def _incoming(key: str, value: object) -> IncomingValue:
    return IncomingValue("edge", "source", "value", "target", key, value)


@pytest.mark.unit
def test_handler_integer_bounds_and_cardinality() -> None:
    assert literal({"value": -(2**63)}, ()) == {"value": -(2**63)}
    assert emit({}, (_incoming("input", 3),)) == {"value": 3}
    assert add({}, (_incoming("left", 2), _incoming("right", 3))) == {"value": 5}
    with pytest.raises(OverflowError):
        multiply({"factor": 2}, (_incoming("input", 2**62),))
    for value in (True, 1.5, "4"):
        with pytest.raises(TypeError):
            literal({"value": value}, ())
        with pytest.raises(TypeError):
            emit({}, (_incoming("input", value),))
    with pytest.raises(ValueError):
        add({}, (_incoming("left", 1), _incoming("left", 2)))
    with pytest.raises(ValueError):
        multiply({"factor": 2}, ())


@pytest.mark.unit
def test_emit_policy_refuses_before_allocation(cleanup: list[str]) -> None:
    doc = _linear()
    for nodes, edges in (
        (doc.nodes[:-1], doc.edges[:-1]),
        (
            (
                *doc.nodes,
                WorkflowNode(
                    "35000000-0000-4000-8000-000000000004", "vidap.reference.emit"
                ),
            ),
            doc.edges,
        ),
        (
            doc.nodes,
            (
                *doc.edges,
                Edge(
                    "36000000-0000-4000-8000-000000000003",
                    Endpoint(doc.nodes[-1].id, "value"),
                    Endpoint(doc.nodes[1].id, "input"),
                ),
            ),
        ),
    ):
        with pytest.raises((ReferenceOutputRefusal, ValueError)):
            run_reference_attempt(WorkflowDocument(doc.workflow_id, nodes, edges))
    with pytest.raises(ValueError):
        run_reference_attempt(
            WorkflowDocument(doc.workflow_id, (*doc.nodes, doc.nodes[0]), doc.edges)
        )
    raw = (ROOT / "fixtures" / "p2-ep05" / "branched-success-v1.json").read_text(
        encoding="utf-8"
    )
    with pytest.raises(WorkflowDecodeError):
        deserialize_document(
            raw.replace('"schemaVersion": "1.0"', '"schemaVersion": "2.0"')
        )
    with pytest.raises(WorkflowDecodeError):
        deserialize_document(
            raw.replace('"workflowId":', '"serializer": "choice", "workflowId":')
        )
    with pytest.raises(AttemptRefusal):
        run_attempt(
            doc,
            NodeRegistry(REFERENCE_REGISTRY.definitions),
            REFERENCE_BINDINGS,
            REFERENCE_RUNTIME_TABLE,
            _reference_output=True,
        )
    assert cleanup == []
