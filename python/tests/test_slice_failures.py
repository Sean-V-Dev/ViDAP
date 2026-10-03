"""Declared slice failures (F6) and the generic handler-failure fallback."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from pathlib import Path

import pytest
from test_slice_operations import fixture, node_id

from vidap_execution import BindingMap, StaticBinding, run_attempt
from vidap_execution.artifacts import _directory, read_record, remove_attempt
from vidap_execution.diagnostics import (
    DECLARED_FAILURES,
    DeclaredFailure,
    declared_code,
)
from vidap_execution.dispatch import IncomingValue, RuntimeRegistration, RuntimeTable
from vidap_execution.planner import RUNTIME_TABLE_REVISION
from vidap_execution.reuse import TrustedValue
from vidap_execution.slice import (
    CATEGORY,
    NUMERIC,
    TARGET,
    ColumnSpec,
    SliceSplit,
    SliceTable,
    model,
    run_slice_attempt,
)
from vidap_workflow import (
    DisplayMetadata,
    NodeDefinition,
    NodeRegistry,
    WorkflowDocument,
    WorkflowNode,
)

ROOT = Path(__file__).resolve().parents[2]
CATEGORY_TEXT = DECLARED_FAILURES["unencoded-category-input"]


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


def _split(schema: tuple[ColumnSpec, ...], columns: tuple[tuple[object, ...], ...]):
    table = SliceTable(schema, columns)
    return TrustedValue(SliceSplit(table, table), "sha256:" + "0" * 64)


def _incoming(value: object) -> tuple[IncomingValue, ...]:
    return (
        IncomingValue(
            "42000000-0000-4000-8000-000000000001",
            node_id(3),
            "split",
            node_id(4),
            "split",
            value,
        ),
    )


@pytest.mark.unit
def test_bypassing_prepare_fails_on_model_with_its_real_cause(
    cleanup: list[str],
) -> None:
    result = run_slice_attempt(fixture("slice-bypass-prepare-v1.json"))
    data = result.record.data
    attempt_id = str(data["attemptId"])
    cleanup.append(attempt_id)
    assert data["outcome"] == "failed"
    statuses = {node["nodeId"]: node["status"] for node in data["nodes"]}
    assert statuses == {
        node_id(1, "43"): "completed",
        node_id(3, "43"): "completed",
        node_id(4, "43"): "failed",
        node_id(5, "43"): "blocked",
    }
    (diagnostic,) = data["diagnostics"]
    assert diagnostic["code"] == "unencoded-category-input"
    assert diagnostic["category"] == "execution"
    assert diagnostic["nodeId"] == node_id(4, "43")
    assert (diagnostic["explanation"], diagnostic["remedy"]) == CATEGORY_TEXT
    assert diagnostic["technical"]["type"] == "DeclaredFailure"
    assert data["artifacts"] == ("record.json",)
    assert {p.name for p in _directory(attempt_id).iterdir()} == {"record.json"}
    assert read_record(attempt_id)["state"] == "failed"


@pytest.mark.unit
def test_model_checks_category_before_missing_values() -> None:
    target = ColumnSpec("label", TARGET, categories=("0", "1"))
    numeric = ColumnSpec("x", NUMERIC, nullable=True)
    category = ColumnSpec("segment", CATEGORY, categories=("north",))
    missing = _split((numeric, target), ((None, 1.0), (0, 1)))
    with pytest.raises(DeclaredFailure) as error:
        model({"regularization": 1.0}, _incoming(missing.value))
    assert error.value.code == "missing-value-input"
    both = _split(
        (numeric, category, target), ((None, 1.0), ("north", "north"), (0, 1))
    )
    with pytest.raises(DeclaredFailure) as error:
        model({"regularization": 1.0}, _incoming(both.value))
    assert error.value.code == "unencoded-category-input"


def _single(handler) -> tuple[WorkflowDocument, NodeRegistry, BindingMap, RuntimeTable]:
    key = "vidap.test.declared"
    revision = "vidap.test.bindings.v1"
    registry = NodeRegistry(
        (NodeDefinition(key, DisplayMetadata("Declared"), operation_key=key),)
    )
    bindings = BindingMap(revision, (StaticBinding(key, revision),))
    table = RuntimeTable(
        RUNTIME_TABLE_REVISION, (RuntimeRegistration(key, revision, handler),)
    )
    document = WorkflowDocument(
        "45000000-0000-4000-8000-000000000001",
        (WorkflowNode("46000000-0000-4000-8000-000000000001", key, parameters={}),),
    )
    return document, registry, bindings, table


class _Forged(DeclaredFailure):
    pass


@pytest.mark.unit
@pytest.mark.parametrize(
    ("raised", "code"),
    [
        (lambda: DeclaredFailure("missing-value-input"), "missing-value-input"),
        (
            lambda: DeclaredFailure("unencoded-category-input"),
            "unencoded-category-input",
        ),
        (lambda: RuntimeError("private detail"), "handler-failed"),
        (lambda: DeclaredFailure("not-in-the-list"), "handler-failed"),
    ],
)
def test_dispatch_maps_only_closed_list_codes(
    cleanup: list[str], raised, code: str
) -> None:
    def handler(
        parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
    ) -> Mapping[str, object]:
        raise raised()

    result = run_attempt(*_single(handler))
    data = result.record.data
    cleanup.append(str(data["attemptId"]))
    (diagnostic,) = data["diagnostics"]
    assert diagnostic["code"] == code
    assert diagnostic["category"] == "execution"
    assert "private" not in str(data)
    if code in DECLARED_FAILURES:
        assert (diagnostic["explanation"], diagnostic["remedy"]) == DECLARED_FAILURES[
            code
        ]


@pytest.mark.unit
def test_codes_never_come_from_text_or_subclasses() -> None:
    forged = _Forged("missing-value-input")
    assert declared_code(forged) == "handler-failed"
    tampered = DeclaredFailure("missing-value-input")
    tampered.code = "something-else"
    assert declared_code(tampered) == "handler-failed"
    assert declared_code(ValueError("missing-value-input")) == "handler-failed"
    with pytest.raises(ValueError):
        DeclaredFailure("unknown")
