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

Data layout
-----------
The challenge ships two PUBLIC files (committed) and keeps the answer key
PRIVATE (git-ignored, instructor only):

    PUBLIC   data/sdc-train.json        -> load_train()        -> initialize()
             data/sdc-test-suite.json   -> load_test_suite()   -> prioritize()
    PRIVATE  _grading/sdc-ground-truth.json -> load_ground_truth()  (evaluator)

Students never receive the test-set labels. To get a local APFD estimate
while developing, carve a validation split out of the labelled training set
with `make_local_validation()`. The instructor scores the real submission on
the hidden test set with the private ground-truth.

`load_dataset` / `split_train_test` remain for the (private) `make_split.py`
generator that produces the files above from the full master dataset.
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


def _to_test_case(record: dict) -> SDCTestCase:
    return SDCTestCase(
        test_id=record["test_id"],
        road_points=[(p[0], p[1]) for p in record["road_points"]],
    )


def load_train(path: str | Path) -> list[OracleEntry]:
    """Load the PUBLIC labelled training set (`data/sdc-train.json`).

    Each record carries `has_failed`, so this is what you pass to
    `MyPrioritizer.initialize()`.
    """
    records = json.loads(Path(path).read_text())
    return [
        OracleEntry(test_case=_to_test_case(r), has_failed=r["has_failed"])
        for r in records
    ]


def load_test_suite(path: str | Path) -> list[SDCTestCase]:
    """Load the PUBLIC unlabelled test suite (`data/sdc-test-suite.json`).

    This is the only view your `prioritize()` receives — labels are not present.
    """
    records = json.loads(Path(path).read_text())
    return [_to_test_case(r) for r in records]


def load_ground_truth(path: str | Path) -> dict[str, dict]:
    """Load the PRIVATE answer key (`_grading/sdc-ground-truth.json`).

    Maps test_id -> {"has_failed": bool, "sim_time": float}. Used by the
    evaluator only; this file is git-ignored and not shipped to students.
    """
    return json.loads(Path(path).read_text())


def make_local_validation(
    train_oracles: list[OracleEntry],
    val_ratio: float = 0.3,
    seed: int = 0,
) -> tuple[list[OracleEntry], list[SDCTestCase], dict[str, dict]]:
    """Carve a local validation split out of the labelled training set.

    Because the real test-set labels are held by the instructor, this is how
    you get an APFD *estimate* while developing: train on the larger part,
    measure on the held-out part.

    Returns
    -------
    dev_oracles : list[OracleEntry]
        The training remainder — pass this to `evaluate()` as the train arg.
    val_suite : list[SDCTestCase]
        The held-out cases with labels stripped — what `prioritize()` reorders.
    val_ground_truth : dict[test_id -> {has_failed, sim_time}]
        Local answer key built from the training labels. `sim_time` is unknown
        to students, so it is set to 1.0 — APFD is meaningful here, but APFDC
        and time-to-fault are only meaningful in the instructor's evaluation.
    """
    rng = random.Random(seed)
    shuffled = list(train_oracles)
    rng.shuffle(shuffled)

    n_val = int(round(len(shuffled) * val_ratio))
    val_entries = shuffled[:n_val]
    dev_oracles = shuffled[n_val:]

    val_suite = [e.test_case for e in val_entries]
    val_ground_truth = {
        e.test_case.test_id: {"has_failed": e.has_failed, "sim_time": 1.0}
        for e in val_entries
    }
    return dev_oracles, val_suite, val_ground_truth
