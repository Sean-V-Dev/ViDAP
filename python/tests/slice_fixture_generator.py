"""Deterministic generator for the P3-EP03B synthetic slice dataset.

Run from the repository root to rewrite the fixture:
``python python/tests/slice_fixture_generator.py``. The committed bytes must
equal ``generate()``; a test checks this. Changing the generator requires a
new fixture version and a manifest update.
"""

from __future__ import annotations

import random
from pathlib import Path

GENERATOR_VERSION = "1.0"
SEED = 20261002
ROWS = 160
MISSING_RATE = 0.08
_SEGMENT_EFFECT = {"north": 0.9, "south": -0.9, "east": 0.0}
FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "fixtures"
    / "p3-ep03b"
    / "slice-dataset-v1.csv"
)


def generate() -> bytes:
    """Return the exact CSV bytes: UTF-8, LF line endings, final newline."""

    rng = random.Random(SEED)  # noqa: S311 - synthetic data, not security
    lines = ["feature_a,feature_b,segment,label"]
    for _ in range(ROWS):
        feature_a = round(rng.gauss(0.0, 1.0), 3)
        feature_b = round(rng.gauss(0.0, 1.0), 3)
        segment = rng.choice(("north", "south", "east"))
        noise = rng.gauss(0.0, 0.7)
        score = 1.6 * feature_a - 1.1 * feature_b + _SEGMENT_EFFECT[segment] + noise
        label = 1 if score > 0.3 else 0
        missing = rng.random() < MISSING_RATE
        b_text = "" if missing else f"{feature_b:.3f}"
        lines.append(f"{feature_a:.3f},{b_text},{segment},{label}")
    return ("\n".join(lines) + "\n").encode("utf-8")


if __name__ == "__main__":
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_bytes(generate())
