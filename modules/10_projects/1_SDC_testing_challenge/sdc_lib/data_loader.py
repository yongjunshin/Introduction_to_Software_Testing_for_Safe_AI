"""Load the SDC dataset and split it into train (with oracle) / test (oracle hidden).

Design notes
------------
- `SDCTestCase` intentionally does NOT carry `has_failed`. Students
  receive only this view in `prioritize()`, so they cannot accidentally
  peek at the ground-truth label.
- `OracleEntry` pairs a test case with its label. Students receive a
  list of these in `initialize()` so they can learn a model if they wish.
- The evaluator keeps its own ground-truth dict, built from the full
  records before they are stripped.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SDCTestCase:
    """A single SDC test case = an ordered sequence of 2D road points."""

    test_id: str
    road_points: list[tuple[float, float]] = field(default_factory=list)


@dataclass(frozen=True)
class OracleEntry:
    """A test case paired with its ground-truth label (failed or not)."""

    test_case: SDCTestCase
    has_failed: bool


def load_dataset(path: str | Path) -> list[dict]:
    """Load the raw normalized dataset (list of dicts with test_id, road_points,
    has_failed, sim_time). Used internally by `split_train_test`.
    """
    with Path(path).open() as f:
        return json.load(f)


def split_train_test(
    raw_records: list[dict],
    train_ratio: float = 0.2,
    seed: int = 42,
) -> tuple[list[OracleEntry], list[SDCTestCase], dict[str, dict]]:
    """Shuffle the records and split into train and test.

    Returns
    -------
    train_oracles : list[OracleEntry]
        Passed to `MyPrioritizer.initialize()`. Includes ground-truth labels.
    test_suite : list[SDCTestCase]
        Passed to `MyPrioritizer.prioritize()`. Ground-truth labels are
        intentionally stripped so the student cannot peek.
    ground_truth : dict[test_id -> {has_failed, sim_time}]
        Held by the evaluator only. Used to score the student's output.
    """
    rng = random.Random(seed)
    shuffled = list(raw_records)
    rng.shuffle(shuffled)

    n_train = int(round(len(shuffled) * train_ratio))
    train_raw = shuffled[:n_train]
    test_raw = shuffled[n_train:]

    train_oracles = [
        OracleEntry(
            test_case=SDCTestCase(
                test_id=r["test_id"],
                road_points=[(p[0], p[1]) for p in r["road_points"]],
            ),
            has_failed=r["has_failed"],
        )
        for r in train_raw
    ]
    test_suite = [
        SDCTestCase(
            test_id=r["test_id"],
            road_points=[(p[0], p[1]) for p in r["road_points"]],
        )
        for r in test_raw
    ]
    ground_truth = {
        r["test_id"]: {"has_failed": r["has_failed"], "sim_time": r["sim_time"]}
        for r in test_raw
    }
    return train_oracles, test_suite, ground_truth
