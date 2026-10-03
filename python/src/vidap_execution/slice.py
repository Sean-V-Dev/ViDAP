"""Five first-party operations for the bounded Phase 3 vertical slice."""

from __future__ import annotations

import csv
import hashlib
import io
from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import sklearn
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

if TYPE_CHECKING:
    from src.vidap_workflow import (
        DisplayMetadata,
        NodeDefinition,
        NodeRegistry,
        ParameterDefinition,
        PortDefinition,
        WorkflowDocument,
    )
else:
    from vidap_workflow import (
        DisplayMetadata,
        NodeDefinition,
        NodeRegistry,
        ParameterDefinition,
        PortDefinition,
        WorkflowDocument,
    )

from .bindings import BindingMap, StaticBinding
from .diagnostics import DeclaredFailure
from .dispatch import IncomingValue, RuntimeRegistration, RuntimeTable
from .output import SliceMetrics
from .planner import RUNTIME_TABLE_REVISION
from .reuse import TrustedValue, canonical_json
from .run import AttemptResult, run_attempt

BINDING_REVISION = "vidap.slice.bindings.v1"
DATASET_KEY = "vidap.slice.dataset"
PREPARE_KEY = "vidap.slice.prepare"
SPLIT_KEY = "vidap.slice.split"
MODEL_KEY = "vidap.slice.model"
EVALUATE_KEY = "vidap.slice.evaluate"
MODEL_IMPLEMENTATION = "sklearn.linear_model.LogisticRegression"

_CHECKOUT = Path(__file__).resolve().parents[3]
DATASET_PATH = _CHECKOUT / "fixtures" / "p3-ep03b" / "slice-dataset-v1.csv"
DATASET_SHA256 = "30ef03b9a552af2482a87d087b170c777629d72ee4247c3a4f1822570a0fc5ff"
DATASET_MAX_BYTES = 16 * 1024

NUMERIC = "numeric"
CATEGORY = "category"
TARGET = "target"


@dataclass(frozen=True, slots=True)
class ColumnSpec:
    """One declared column; nothing about it is inferred from data."""

    name: str
    kind: str
    nullable: bool = False
    categories: tuple[str, ...] = ()


DECLARED_SCHEMA = (
    ColumnSpec("feature_a", NUMERIC),
    ColumnSpec("feature_b", NUMERIC, nullable=True),
    ColumnSpec("segment", CATEGORY, categories=("north", "south", "east")),
    ColumnSpec("label", TARGET, categories=("0", "1")),
)


@dataclass(frozen=True, slots=True)
class SliceTable:
    """An immutable column-oriented table that carries its declared schema."""

    schema: tuple[ColumnSpec, ...]
    columns: tuple[tuple[object, ...], ...]

    def __post_init__(self) -> None:
        if len(self.schema) != len(self.columns):
            raise ValueError("table schema and columns differ")
        if len({len(column) for column in self.columns}) > 1:
            raise ValueError("table columns differ in length")
        if [spec.kind for spec in self.schema].count(TARGET) != 1:
            raise ValueError("table requires exactly one target column")

    @property
    def row_count(self) -> int:
        return len(self.columns[0]) if self.columns else 0

    def rows(self, indices: tuple[int, ...]) -> SliceTable:
        return SliceTable(
            self.schema,
            tuple(tuple(column[i] for i in indices) for column in self.columns),
        )

    def target(self) -> tuple[object, ...]:
        return next(
            column
            for spec, column in zip(self.schema, self.columns, strict=True)
            if spec.kind == TARGET
        )

    def features(self) -> tuple[tuple[ColumnSpec, tuple[object, ...]], ...]:
        return tuple(
            (spec, column)
            for spec, column in zip(self.schema, self.columns, strict=True)
            if spec.kind != TARGET
        )

    def payload(self) -> dict[str, object]:
        return {
            "schema": [
                {
                    "name": spec.name,
                    "kind": spec.kind,
                    "nullable": spec.nullable,
                    "categories": list(spec.categories),
                }
                for spec in self.schema
            ],
            "columns": [list(column) for column in self.columns],
        }


@dataclass(frozen=True, slots=True)
class SliceSplit:
    train: SliceTable
    test: SliceTable

    def __post_init__(self) -> None:
        if self.train.schema != self.test.schema:
            raise ValueError("split parts must share one schema")


@dataclass(frozen=True, slots=True)
class SliceModel:
    """A fitted fixed implementation and the feature order it was fitted on."""

    feature_names: tuple[str, ...]
    estimator: LogisticRegression
    content_ref: str


def _digest(payload: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(payload)).hexdigest()


def _trusted_table(table: SliceTable) -> TrustedValue:
    return TrustedValue(table, _digest({"table": table.payload()}))


def _incoming(
    incoming: tuple[IncomingValue, ...], keys: tuple[str, ...]
) -> dict[str, object]:
    if len(incoming) != len(keys) or {item.target_port_key for item in incoming} != set(
        keys
    ):
        raise ValueError("slice input cardinality is invalid")
    return {item.target_port_key: item.value for item in incoming}


def _keys(parameters: Mapping[str, object], keys: tuple[str, ...]) -> None:
    if set(parameters) != set(keys):
        raise ValueError("slice parameters are invalid")


def _number(value: object, minimum: float, maximum: float) -> float:
    if type(value) not in (int, float):
        raise TypeError("slice number parameter must be numeric")
    number = float(value)  # type: ignore[arg-type]
    if not isfinite(number) or not minimum <= number <= maximum:
        raise ValueError("slice number parameter is out of range")
    return number


def _integer(value: object, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError("slice integer parameter is out of range")
    return value


def _table(value: object) -> SliceTable:
    if not isinstance(value, SliceTable):
        raise TypeError("slice input must be a slice table")
    return value


def _split_value(value: object) -> SliceSplit:
    if not isinstance(value, SliceSplit):
        raise TypeError("slice input must be a slice split")
    return value


def _parse_numeric(text: str, spec: ColumnSpec) -> float | None:
    if text == "":
        if not spec.nullable:
            raise ValueError("declared column does not allow missing values")
        return None
    number = float(text)
    if not isfinite(number):
        raise ValueError("numeric field must be finite")
    return number


def load_dataset_bytes(data: bytes) -> SliceTable:
    """Parse the fixed fixture by its declared schema; refuse any mismatch."""

    if len(data) > DATASET_MAX_BYTES:
        raise ValueError("dataset exceeds its size bound")
    if hashlib.sha256(data).hexdigest() != DATASET_SHA256:
        raise ValueError("dataset bytes do not match the reviewed fixture")
    reader = csv.reader(io.StringIO(data.decode("utf-8"), newline=""))
    rows = list(reader)
    if not rows or tuple(rows[0]) != tuple(spec.name for spec in DECLARED_SCHEMA):
        raise ValueError("dataset header does not match the declared schema")
    columns: list[list[object]] = [[] for _ in DECLARED_SCHEMA]
    for row in rows[1:]:
        if len(row) != len(DECLARED_SCHEMA):
            raise ValueError("dataset row does not match the declared schema")
        for index, (spec, text) in enumerate(zip(DECLARED_SCHEMA, row, strict=True)):
            if spec.kind == NUMERIC:
                columns[index].append(_parse_numeric(text, spec))
            elif spec.kind == CATEGORY:
                if text not in spec.categories:
                    raise ValueError("category value is not declared")
                columns[index].append(text)
            else:
                if text not in spec.categories:
                    raise ValueError("target value is not declared")
                columns[index].append(int(text))
    return SliceTable(DECLARED_SCHEMA, tuple(tuple(column) for column in columns))


def dataset(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    _incoming(incoming, ())
    _keys(parameters, ())
    if DATASET_PATH.is_symlink() or not DATASET_PATH.is_file():
        raise ValueError("dataset fixture is missing")
    if DATASET_PATH.stat().st_size > DATASET_MAX_BYTES:
        raise ValueError("dataset exceeds its size bound")
    return {"table": _trusted_table(load_dataset_bytes(DATASET_PATH.read_bytes()))}


def prepare(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    table = _table(_incoming(incoming, ("table",))["table"])
    _keys(parameters, ("missing_fill",))
    fill = _number(parameters["missing_fill"], -1e6, 1e6)
    schema: list[ColumnSpec] = []
    columns: list[tuple[object, ...]] = []
    numeric = [(s, c) for s, c in table.features() if s.kind == NUMERIC]
    category = [(s, c) for s, c in table.features() if s.kind == CATEGORY]
    if numeric:
        raw = np.array(
            [[np.nan if v is None else v for v in c] for _, c in numeric],
            dtype=float,
        ).T
        filled = SimpleImputer(strategy="constant", fill_value=fill).fit_transform(raw)
        for index, (spec, _) in enumerate(numeric):
            schema.append(ColumnSpec(spec.name, NUMERIC))
            columns.append(tuple(float(v) for v in filled[:, index]))
    for spec, column in category:
        encoder = OneHotEncoder(
            categories=[list(spec.categories)],
            sparse_output=False,
            handle_unknown="error",
        )
        encoded = encoder.fit_transform(np.array(column, dtype=object).reshape(-1, 1))
        for index, name in enumerate(spec.categories):
            schema.append(ColumnSpec(f"{spec.name}={name}", NUMERIC))
            columns.append(tuple(float(v) for v in encoded[:, index]))
    target_spec = next(s for s in table.schema if s.kind == TARGET)
    schema.append(target_spec)
    columns.append(table.target())
    return {"prepared": _trusted_table(SliceTable(tuple(schema), tuple(columns)))}


def split(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    table = _table(_incoming(incoming, ("table",))["table"])
    _keys(parameters, ("test_fraction", "seed"))
    fraction = _number(parameters["test_fraction"], 0.1, 0.5)
    seed = _integer(parameters["seed"], 0, 2**32 - 1)
    indices = list(range(table.row_count))
    train_indices, test_indices = train_test_split(
        indices,
        test_size=fraction,
        random_state=seed,
        stratify=list(table.target()),
    )
    value = SliceSplit(
        table.rows(tuple(int(i) for i in train_indices)),
        table.rows(tuple(int(i) for i in test_indices)),
    )
    reference = _digest(
        {"split": {"train": value.train.payload(), "test": value.test.payload()}}
    )
    return {"split": TrustedValue(value, reference)}


def _matrix(table: SliceTable) -> tuple[np.ndarray, np.ndarray]:
    features = table.features()
    if any(spec.kind == CATEGORY for spec, _ in features):
        raise DeclaredFailure("unencoded-category-input")
    if any(value is None for _, column in features for value in column):
        raise DeclaredFailure("missing-value-input")
    x = np.array([column for _, column in features], dtype=float).T
    y = np.array(table.target(), dtype=int)
    return x, y


def model(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    parts = _split_value(_incoming(incoming, ("split",))["split"])
    _keys(parameters, ("regularization",))
    regularization = _number(parameters["regularization"], 0.0001, 10000.0)
    x, y = _matrix(parts.train)
    estimator = LogisticRegression(C=regularization)
    estimator.fit(x, y)
    names = tuple(spec.name for spec, _ in parts.train.features())
    reference = _digest(
        {
            "model": {
                "implementation": MODEL_IMPLEMENTATION,
                "sklearnVersion": sklearn.__version__,
                "regularization": regularization,
                "features": list(names),
                "classes": [int(v) for v in estimator.classes_],
                "coefficients": [[float(v) for v in row] for row in estimator.coef_],
                "intercept": [float(v) for v in estimator.intercept_],
            }
        }
    )
    value = SliceModel(names, estimator, reference)
    return {"model": TrustedValue(value, reference)}


def evaluate(
    parameters: Mapping[str, object], incoming: tuple[IncomingValue, ...]
) -> Mapping[str, object]:
    values = _incoming(incoming, ("model", "split"))
    fitted = values["model"]
    if not isinstance(fitted, SliceModel):
        raise TypeError("slice input must be a fitted slice model")
    parts = _split_value(values["split"])
    _keys(parameters, ())
    names = tuple(spec.name for spec, _ in parts.test.features())
    if names != fitted.feature_names:
        raise ValueError("evaluation features differ from the fitted model")
    x, y = _matrix(parts.test)
    predicted = fitted.estimator.predict(x)
    accuracy = float(accuracy_score(y, predicted))
    correct = int(np.sum(predicted == y))
    rows = int(y.shape[0])
    if accuracy != correct / rows:
        raise ValueError("accuracy disagrees with the counted result")
    metrics = SliceMetrics(accuracy, correct, rows)
    return {"metrics": TrustedValue(metrics, _digest({"metrics": metrics.payload()}))}


def _input(key: str, nominal: str, label: str) -> PortDefinition:
    return PortDefinition(
        key, "input", nominal, DisplayMetadata(label), cardinality="one", required=True
    )


def _output(key: str, nominal: str, label: str) -> PortDefinition:
    return PortDefinition(key, "output", nominal, DisplayMetadata(label))


def _number_parameter(
    key: str,
    label: str,
    description: str,
    minimum: float,
    maximum: float,
    default: float,
) -> ParameterDefinition:
    return ParameterDefinition(
        key,
        "number",
        False,
        DisplayMetadata(label, description),
        default=default,
        constraints={"minimum": minimum, "maximum": maximum},
    )


SLICE_REGISTRY = NodeRegistry(
    (
        NodeDefinition(
            type_id=DATASET_KEY,
            operation_key=DATASET_KEY,
            display=DisplayMetadata(
                "Dataset",
                "Loads the controlled synthetic slice dataset by its declared schema.",
            ),
            outputs=(_output("table", "table", "Table"),),
        ),
        NodeDefinition(
            type_id=PREPARE_KEY,
            operation_key=PREPARE_KEY,
            display=DisplayMetadata(
                "Prepare Data",
                "Fills missing numbers with a constant and encodes the declared "
                "categories as numbers. Learns nothing from the rows.",
            ),
            inputs=(_input("table", "table", "Table"),),
            outputs=(_output("prepared", "table", "Prepared table"),),
            parameters=(
                _number_parameter(
                    "missing_fill",
                    "Missing value fill",
                    "The number used in place of a missing value.",
                    -1e6,
                    1e6,
                    0.0,
                ),
            ),
        ),
        NodeDefinition(
            type_id=SPLIT_KEY,
            operation_key=SPLIT_KEY,
            display=DisplayMetadata(
                "Train/Test Split",
                "Splits rows into training and test parts, keeping the label "
                "balance in both.",
            ),
            inputs=(_input("table", "table", "Table"),),
            outputs=(_output("split", "split", "Split"),),
            parameters=(
                _number_parameter(
                    "test_fraction",
                    "Test fraction",
                    "The share of rows held out for testing.",
                    0.1,
                    0.5,
                    0.25,
                ),
                ParameterDefinition(
                    "seed",
                    "integer",
                    False,
                    DisplayMetadata("Split seed", "Controls which rows are held out."),
                    default=0,
                    constraints={"minimum": 0, "maximum": 2**32 - 1},
                ),
            ),
        ),
        NodeDefinition(
            type_id=MODEL_KEY,
            operation_key=MODEL_KEY,
            display=DisplayMetadata(
                "Model",
                "Trains the slice's fixed model implementation, logistic "
                "regression, on the training part.",
            ),
            inputs=(_input("split", "split", "Split"),),
            outputs=(_output("model", "model", "Trained model"),),
            parameters=(
                _number_parameter(
                    "regularization",
                    "Regularization",
                    "Smaller values constrain the model more strongly.",
                    0.0001,
                    10000.0,
                    1.0,
                ),
            ),
        ),
        NodeDefinition(
            type_id=EVALUATE_KEY,
            operation_key=EVALUATE_KEY,
            display=DisplayMetadata(
                "Evaluate",
                "Measures the trained model's accuracy on the test part.",
            ),
            inputs=(
                _input("model", "model", "Trained model"),
                _input("split", "split", "Split"),
            ),
            outputs=(_output("metrics", "metrics", "Metrics"),),
        ),
    )
)
_HANDLERS = (
    (DATASET_KEY, dataset),
    (PREPARE_KEY, prepare),
    (SPLIT_KEY, split),
    (MODEL_KEY, model),
    (EVALUATE_KEY, evaluate),
)
SLICE_BINDINGS = BindingMap(
    BINDING_REVISION,
    tuple(StaticBinding(key, BINDING_REVISION) for key, _ in _HANDLERS),
)
SLICE_RUNTIME_TABLE = RuntimeTable(
    RUNTIME_TABLE_REVISION,
    tuple(
        RuntimeRegistration(key, BINDING_REVISION, handler)
        for key, handler in _HANDLERS
    ),
)


def run_slice_attempt(
    document: WorkflowDocument, *, seed: int | None = None
) -> AttemptResult:
    """Run the fixed slice family once through the accepted attempt layer."""

    return run_attempt(
        document,
        SLICE_REGISTRY,
        SLICE_BINDINGS,
        SLICE_RUNTIME_TABLE,
        seed=seed,
        _slice_output=True,
    )
