"""Test-local scalar handlers exercise the actual plan and dispatch path."""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from vidap_execution import BindingMap, StaticBinding, plan_execution
from vidap_execution.dispatch import (
    DispatchRefusal,
    IncomingValue,
    RuntimeRegistration,
    RuntimeTable,
    dispatch,
)
from vidap_execution.planner import RUNTIME_TABLE_REVISION
from vidap_workflow import (
    DisplayMetadata,
    Edge,
    Endpoint,
    NodeDefinition,
    NodeRegistry,
    ParameterDefinition,
    PortDefinition,
    WorkflowDocument,
    WorkflowNode,
)


def _id(number: int) -> str:
    return f"{number:08d}-0000-4000-8000-000000000000"


def _plan(
    connections: tuple[tuple[int, int], ...],
    count: int = 4,
    reverse: bool = False,
    ports: tuple[tuple[str, str], ...] | None = None,
):
    definitions = tuple(
        NodeDefinition(
            f"test.n{number}",
            DisplayMetadata(label=f"Node {number}"),
            inputs=(
                PortDefinition(
                    "a",
                    "input",
                    "table",
                    DisplayMetadata(label="A"),
                    cardinality="many",
                    required=False,
                ),
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
                PortDefinition(
                    "out", "output", "table", DisplayMetadata(label="Output")
                ),
                PortDefinition("z", "output", "table", DisplayMetadata(label="Z")),
            ),
            parameters=(
                ParameterDefinition(
                    "value",
                    "integer",
                    False,
                    DisplayMetadata(label="Value"),
                    default=number,
                ),
            ),
            operation_key=f"test.op{number}",
        )
        for number in range(1, count + 1)
    )
    nodes = tuple(
        WorkflowNode(_id(number), f"test.n{number}") for number in range(1, count + 1)
    )
    edges = tuple(
        Edge(
            _id(100 + index),
            Endpoint(_id(source), ports[index][0] if ports else "out"),
            Endpoint(_id(target), ports[index][1] if ports else "in"),
        )
        for index, (source, target) in enumerate(connections)
    )
    bindings = BindingMap(
        "r1",
        tuple(
            StaticBinding(f"test.op{number}", "r1") for number in range(1, count + 1)
        ),
    )
    if reverse:
        nodes = tuple(reversed(nodes))
        edges = tuple(reversed(edges))
        definitions = tuple(reversed(definitions))
        bindings = BindingMap("r1", tuple(reversed(bindings.bindings)))
    return plan_execution(
        WorkflowDocument(_id(900), nodes, edges), NodeRegistry(definitions), bindings
    )


def _table(
    handlers: Mapping[int, object], revision: str = RUNTIME_TABLE_REVISION
) -> RuntimeTable:
    return RuntimeTable(
        revision,
        tuple(
            RuntimeRegistration(f"test.op{number}", "r1", handler)  # type: ignore[arg-type]
            for number, handler in handlers.items()
        ),
    )


@pytest.mark.unit
def test_branch_join_scalar_flow_and_repeated_call_isolation() -> None:
    plan = _plan(((1, 2), (1, 3), (2, 4), (3, 4)))
    calls: list[tuple[int, tuple[IncomingValue, ...]]] = []

    def handler(number: int):
        def calculate(
            parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
        ):
            calls.append((number, incoming))
            return {
                "out": int(parameters["value"])
                + sum(int(item.value) for item in incoming)
            }

        return calculate

    table = _table({number: handler(number) for number in range(1, 5)})
    first = dispatch(plan, table)
    assert first.stop_reason is None
    assert first.completed_node_ids == tuple(_id(number) for number in range(1, 5))
    assert [number for number, _ in calls] == [1, 2, 3, 4]
    assert [item.value for item in calls[1][1]] == [1]
    assert [item.value for item in calls[2][1]] == [1]
    assert [
        (item.source_node_id, item.target_port_key, item.value) for item in calls[3][1]
    ] == [(_id(2), "in", 3), (_id(3), "in", 4)]
    assert calls[3][1][0].edge_id != calls[3][1][1].edge_id
    assert first.port_results[(_id(4), "out")] == 11
    second = dispatch(plan, table)
    assert [number for number, _ in calls] == [1, 2, 3, 4] * 2
    assert first.port_results is not second.port_results
    assert dict(first.port_results) == dict(second.port_results)


@pytest.mark.unit
def test_reversed_construction_keeps_dispatch_trace() -> None:
    connections = ((1, 2), (1, 3), (2, 4), (3, 4))

    def observed(reverse: bool) -> list[tuple[int, tuple[str, ...]]]:
        trace: list[tuple[int, tuple[str, ...]]] = []

        def handler(number: int):
            def calculate(
                parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
            ):
                trace.append((number, tuple(item.edge_id for item in incoming)))
                return {
                    "out": int(parameters["value"])
                    + sum(int(item.value) for item in incoming)
                }

            return calculate

        plan = _plan(connections, reverse=reverse)
        result = dispatch(
            plan, _table({number: handler(number) for number in range(1, 5)})
        )
        assert result.stop_reason is None
        return trace

    assert observed(False) == observed(True)


@pytest.mark.unit
def test_incoming_order_keeps_target_and_source_port_identity() -> None:
    plan = _plan(
        ((1, 3), (2, 3), (1, 3)),
        count=3,
        ports=(("z", "in"), ("out", "a"), ("out", "in")),
    )
    received: list[tuple[str, str, str, object]] = []

    def root(parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]):
        value = int(parameters["value"])
        return {"out": value, "z": value * 10}

    def join(parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]):
        received.extend(
            (
                item.target_port_key,
                item.source_node_id,
                item.source_port_key,
                item.value,
            )
            for item in incoming
        )
        return {"out": sum(int(item.value) for item in incoming)}

    result = dispatch(plan, _table({1: root, 2: root, 3: join}))
    assert result.stop_reason is None
    assert received == [
        ("a", _id(2), "out", 2),
        ("in", _id(1), "out", 1),
        ("in", _id(1), "z", 10),
    ]


@pytest.mark.unit
@pytest.mark.parametrize(
    "kind", ["missing", "duplicate", "handler-revision", "table-revision"]
)
def test_preflight_refuses_before_any_handler(kind: str) -> None:
    plan = _plan(((1, 2),), count=2)
    calls: list[int] = []

    def handler(parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]):
        calls.append(1)
        return {"out": 1}

    registrations = [RuntimeRegistration("test.op1", "r1", handler)]
    revision = RUNTIME_TABLE_REVISION
    if kind == "duplicate":
        registrations.extend(
            (registrations[0], RuntimeRegistration("test.op2", "r1", handler))
        )
    elif kind == "handler-revision":
        registrations.append(RuntimeRegistration("test.op2", "r2", handler))
    elif kind == "table-revision":
        revision = "other-plan-revision"
        registrations.append(RuntimeRegistration("test.op2", "r1", handler))
    with pytest.raises(DispatchRefusal) as caught:
        dispatch(plan, RuntimeTable(revision, tuple(registrations)))
    assert (
        caught.value.code
        == {
            "missing": "missing-handler",
            "duplicate": "duplicate-handler",
            "handler-revision": "handler-revision-mismatch",
            "table-revision": "table-revision-mismatch",
        }[kind]
    )
    assert calls == []


@pytest.mark.unit
def test_first_handler_failure_distinguishes_all_unstarted_states() -> None:
    plan = _plan(((1, 2), (2, 3)))
    calls: list[int] = []

    def handler(number: int):
        def calculate(
            parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
        ):
            calls.append(number)
            if number == 2:
                raise RuntimeError("secret raw error text")
            return {"out": number}

        return calculate

    result = dispatch(plan, _table({number: handler(number) for number in range(1, 5)}))
    assert calls == [1, 2]
    assert result.completed_node_ids == (_id(1),)
    assert result.failed_node_id == _id(2)
    assert result.blocked_node_ids == (_id(3),)
    assert result.unrelated_unstarted_node_ids == (_id(4),)
    assert result.attempted_node_ids == (_id(1), _id(2))
    assert result.stop_reason is not None
    assert (result.stop_reason.category, result.stop_reason.code) == (
        "execution",
        "handler-failed",
    )
    assert result.stop_reason.technical_type == "RuntimeError"
    assert "secret" not in repr(result)
    assert dict(result.port_results) == {(_id(1), "out"): 1}


@pytest.mark.unit
@pytest.mark.parametrize(
    ("output", "code"),
    [
        ({"other": 2}, "missing-output"),
        (7, "invalid-handler-output"),
        ({1: 2}, "invalid-handler-output"),
    ],
)
def test_bad_output_never_publishes_partial_results(output: object, code: str) -> None:
    plan = _plan(((1, 2), (2, 3)), count=3)
    calls: list[int] = []

    def first(parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]):
        calls.append(1)
        return {"out": 1}

    def bad(parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]):
        calls.append(2)
        return output

    def later(parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]):
        calls.append(3)
        return {"out": 3}

    result = dispatch(plan, _table({1: first, 2: bad, 3: later}))
    assert calls == [1, 2]
    assert result.stop_reason is not None and result.stop_reason.code == code
    assert result.completed_node_ids == (_id(1),)
    assert result.blocked_node_ids == (_id(3),)
    assert dict(result.port_results) == {(_id(1), "out"): 1}
