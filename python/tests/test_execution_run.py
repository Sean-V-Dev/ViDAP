"""Synthetic evidence through accepted preparation, planning, and dispatch."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import pytest

from vidap_execution import (
    AttemptRefusal,
    BindingMap,
    PreparationFailure,
    StaticBinding,
    run_attempt,
)
from vidap_execution.artifacts import _directory, remove_attempt
from vidap_execution.dispatch import (
    DispatchRefusal,
    IncomingValue,
    RuntimeRegistration,
    RuntimeTable,
)
from vidap_execution.planner import RUNTIME_TABLE_REVISION
from vidap_execution.reuse import TrustedValue
from vidap_workflow import (
    DisplayMetadata,
    Edge,
    Endpoint,
    LayoutMetadata,
    NodeDefinition,
    NodeRegistry,
    ParameterDefinition,
    PortDefinition,
    Position,
    WorkflowDocument,
    WorkflowNode,
)


def _id(number: int) -> str:
    return f"{number:08d}-0000-4000-8000-000000000000"


def _inputs(
    connections: tuple[tuple[int, int], ...],
    *,
    reverse: bool = False,
    display: bool = False,
    parameter: object = 1,
) -> tuple[WorkflowDocument, NodeRegistry, BindingMap]:
    definitions = tuple(
        NodeDefinition(
            f"test.n{number}",
            DisplayMetadata(label=f"Node {number}"),
            inputs=(
                PortDefinition(
                    "in",
                    "input",
                    "table",
                    DisplayMetadata(label="Input"),
                    cardinality="many",
                    required=False,
                ),
            ),
            outputs=(
                PortDefinition("out", "output", "table", DisplayMetadata(label="Out")),
            ),
            parameters=(
                ParameterDefinition(
                    "value",
                    "integer" if type(parameter) is int else "string",
                    False,
                    DisplayMetadata(label="Value"),
                    default=parameter,
                ),
            ),
            operation_key=f"test.op{number}",
        )
        for number in range(1, 5)
    )
    nodes = tuple(
        WorkflowNode(_id(number), f"test.n{number}") for number in range(1, 5)
    )
    edges = tuple(
        Edge(
            _id(100 + index), Endpoint(_id(source), "out"), Endpoint(_id(target), "in")
        )
        for index, (source, target) in enumerate(connections)
    )
    if reverse:
        definitions, nodes, edges = (
            tuple(reversed(definitions)),
            tuple(reversed(nodes)),
            tuple(reversed(edges)),
        )
    document = WorkflowDocument(
        _id(900),
        nodes,
        edges,
        layout=LayoutMetadata({_id(1): Position(10, 20)}) if display else None,
    )
    return (
        document,
        NodeRegistry(definitions),
        BindingMap(
            "r1",
            tuple(StaticBinding(f"test.op{number}", "r1") for number in range(1, 5)),
        ),
    )


def _table(handler: Any) -> RuntimeTable:
    return RuntimeTable(
        RUNTIME_TABLE_REVISION,
        tuple(
            RuntimeRegistration(f"test.op{number}", "r1", handler(number))
            for number in range(1, 5)
        ),
    )


@pytest.fixture
def owned() -> list[str]:
    ids: list[str] = []
    root = Path(__file__).resolve().parents[2] / ".vidap-local"
    existed = root.exists()
    yield ids
    for attempt_id in ids:
        remove_attempt(attempt_id)
    if not existed and root.exists():
        (root / "runs").rmdir()
        root.rmdir()


@pytest.mark.unit
@pytest.mark.parametrize(
    "connections", [((1, 2), (2, 3)), ((1, 2), (1, 3), (2, 4), (3, 4))]
)
def test_attempt_success_truthful_sharing_and_deep_immutability(
    owned: list[str], connections: tuple[tuple[int, int], ...]
) -> None:
    calls: list[int] = []

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            calls.append(number)
            return {
                "out": int(parameters["value"])
                + sum(int(item.value) for item in incoming)
            }

        return calculate

    document, registry, bindings = _inputs(connections)
    result = run_attempt(document, registry, bindings, _table(handler), seed=0)
    record = result.record.data
    owned.append(record["attemptId"])
    assert record["outcome"] == "succeeded"
    assert record["publication"] == "published"
    assert record["workflowId"] == document.workflow_id
    assert record["contractSnapshotRef"] and record["semanticDigest"]
    assert record["seed"] == 0
    assert set(record["environment"]["lockSha256"]) == {
        "package-lock.json",
        "python/uv.lock",
    }
    assert calls == [1, 2, 3, 4]
    assert result.dispatch_result is not None
    assert result.dispatch_result.port_results[(_id(4), "out")] >= 1
    events = record["reuseEvents"]
    assert sum(event["kind"] == "computed" for event in events) == 4
    assert sum(event["kind"] == "reused-within-attempt" for event in events) == len(
        connections
    )
    assert (
        len(
            [
                event
                for event in events
                if event["sourceNodeId"] == _id(1) and event["kind"] == "computed"
            ]
        )
        == 1
    )
    with pytest.raises(TypeError):
        record["nodes"][0]["parameters"]["value"] = 9
    with pytest.raises(FrozenInstanceError):
        result.record.data = {}  # type: ignore[misc]


@pytest.mark.unit
def test_visual_construction_and_new_attempt_do_not_reuse_across_runs(
    owned: list[str],
) -> None:
    calls: list[int] = []

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            calls.append(number)
            return {
                "out": int(parameters["value"])
                + sum(int(item.value) for item in incoming)
            }

        return calculate

    a = _inputs(((1, 2), (1, 3)), reverse=False)
    b = _inputs(((1, 2), (1, 3)), reverse=True, display=True)
    first = run_attempt(*a, _table(handler))
    second = run_attempt(*b, _table(handler))
    owned.extend((first.record.data["attemptId"], second.record.data["attemptId"]))
    assert first.record.data["semanticDigest"] == second.record.data["semanticDigest"]
    assert first.record.data["attemptId"] != second.record.data["attemptId"]
    assert [event["compositeKey"] for event in first.record.data["reuseEvents"]] == [
        event["compositeKey"] for event in second.record.data["reuseEvents"]
    ]
    assert calls == [1, 2, 3, 4] * 2


@pytest.mark.unit
def test_pre_dispatch_refusals_create_no_owned_run(owned: list[str]) -> None:
    calls: list[int] = []

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            calls.append(number)
            return {"out": number}

        return calculate

    document, registry, bindings = _inputs(((1, 2),))
    invalid = WorkflowDocument(
        _id(900), (*document.nodes, document.nodes[0]), document.edges
    )
    with pytest.raises(PreparationFailure) as caught:
        run_attempt(invalid, registry, bindings, _table(handler))
    assert caught.value.code == "invalid-workflow" and caught.value.diagnostics
    with pytest.raises(PreparationFailure):
        run_attempt(document, registry, BindingMap("r1"), _table(handler))
    with pytest.raises(DispatchRefusal):
        run_attempt(document, registry, bindings, RuntimeTable(RUNTIME_TABLE_REVISION))
    string_inputs = _inputs((), parameter="private")
    with pytest.raises(AttemptRefusal):
        run_attempt(*string_inputs, _table(handler))
    assert calls == [] and owned == []


@pytest.mark.unit
@pytest.mark.parametrize("failure", ["raise", "malformed", "missing"])
def test_failure_is_terminal_and_sanitized(owned: list[str], failure: str) -> None:
    calls: list[int] = []

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            calls.append(number)
            if number == 2:
                if failure == "raise":
                    try:
                        raise ValueError("secret C:\\Users\\private\\token")
                    except ValueError as cause:
                        raise RuntimeError("credential=private") from cause
                if failure == "malformed":
                    return 3
                return {"other": 3}
            return {"out": number}

        return calculate

    inputs = _inputs(((1, 2), (2, 3)))
    result = run_attempt(*inputs, _table(handler))
    record = result.record.data
    owned.append(record["attemptId"])
    assert record["outcome"] == "failed" and record["publication"] == "published"
    assert calls == [1, 2]
    assert record["completedNodeIds"] == (_id(1),)
    assert record["blockedNodeIds"] == (_id(3),)
    assert record["unrelatedNodeIds"] == (_id(4),)
    assert len(record["diagnostics"]) == 1
    assert (
        record["diagnostics"][0]["explanation"] and record["diagnostics"][0]["remedy"]
    )
    assert all(event["sourceNodeId"] != _id(2) for event in record["reuseEvents"])
    assert "private" not in repr(record) and "Users" not in repr(record)
    stored = (_directory(record["attemptId"]) / "record.json").read_text(
        encoding="utf-8"
    )
    assert "credential=private" not in stored and "Users" not in stored


@pytest.mark.unit
@pytest.mark.parametrize("trusted", [False, True])
def test_opaque_result_needs_explicit_trusted_reference(
    owned: list[str], trusted: bool
) -> None:
    opaque = object()
    calls: list[int] = []

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            calls.append(number)
            if number == 1:
                return {
                    "out": TrustedValue(opaque, "sha256:" + "a" * 64)
                    if trusted
                    else opaque
                }
            if number == 2:
                assert incoming[0].value is opaque
            return {"out": 2}

        return calculate

    result = run_attempt(*_inputs(((1, 2),)), _table(handler))
    record = result.record.data
    owned.append(record["attemptId"])
    if trusted:
        assert record["outcome"] == "succeeded"
        assert result.dispatch_result is not None
        assert result.dispatch_result.port_results[(_id(1), "out")] is opaque
        assert calls == [1, 2, 3, 4]
    else:
        assert record["outcome"] == "failed"
        assert record["diagnostics"][0]["code"] == "unreferenced-output"
        assert calls == [1]
        assert all(event["sourceNodeId"] != _id(1) for event in record["reuseEvents"])


@pytest.mark.unit
def test_publication_failure_returns_failed_pending_state(
    owned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    from vidap_execution import run as run_module

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            return {"out": number}

        return calculate

    def fail_publish(attempt_id: str, record: dict[str, Any]) -> None:
        raise OSError("secret C:\\Users\\private\\record.json")

    monkeypatch.setattr(run_module, "publish_terminal", fail_publish)
    result = run_attempt(*_inputs(()), _table(handler))
    record = result.record.data
    owned.append(record["attemptId"])
    assert record["outcome"] == "failed"
    assert record["publication"] == "failed-pending"
    assert record["artifacts"] == ()
    assert record["diagnostics"][0]["category"] == "artifact"
    assert "private" not in repr(record)


@pytest.mark.unit
def test_pending_publication_failure_is_in_memory_failure_before_dispatch(
    owned: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    from vidap_execution import artifacts

    calls: list[int] = []

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            calls.append(number)
            return {"out": number}

        return calculate

    def fail_initial_publish(source: object, target: object) -> None:
        raise OSError("secret initial publication error")

    monkeypatch.setattr(artifacts.os, "rename", fail_initial_publish)
    result = run_attempt(*_inputs(()), _table(handler))
    record = result.record.data
    assert result.dispatch_result is None
    assert calls == []
    assert record["outcome"] == "failed"
    assert record["publication"] == "failed-before-dispatch"
    assert record["artifacts"] == ()
    assert record["diagnostics"][0]["code"] == "publication-failed"
    assert "secret" not in repr(record)
    assert not any(artifacts._root().iterdir())


@pytest.mark.unit
def test_missing_lock_refuses_before_durable_write(
    owned: list[str], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from vidap_execution import run as run_module

    def handler(number: int):
        def calculate(parameters: Any, incoming: tuple[IncomingValue, ...]):
            return {"out": number}

        return calculate

    monkeypatch.setattr(run_module, "_CHECKOUT", tmp_path)
    with pytest.raises(AttemptRefusal):
        run_attempt(*_inputs(()), _table(handler))
    assert owned == []
