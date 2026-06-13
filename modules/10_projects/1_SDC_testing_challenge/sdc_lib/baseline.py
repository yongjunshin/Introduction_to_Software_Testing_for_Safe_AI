"""Reference prioritizers — useful as comparison baselines.

Both follow the same `initialize` / `prioritize` interface that students
implement, so you can drop them into the evaluator directly.
"""
from __future__ import annotations

import random

from sdc_lib.data_loader import OracleEntry, SDCTestCase


class RandomPrioritizer:
    """Random shuffling — equivalent to the official `sample_test_prioritizer`.

    Expected APFD ≈ 0.5. Any worthwhile heuristic should beat this.
    """

    def __init__(self, seed: int = 0) -> None:
        self._rng = random.Random(seed)

    def initialize(self, oracles: list[OracleEntry]) -> None:
        # The random baseline ignores training data.
        pass

    def prioritize(self, test_suite: list[SDCTestCase]) -> list[str]:
        ids = [tc.test_id for tc in test_suite]
        self._rng.shuffle(ids)
        return ids


class IdentityPrioritizer:
    """Returns the test suite in its original order (no reordering).

    Equivalent to "no prioritization at all". Useful as a sanity check.
    """

    def initialize(self, oracles: list[OracleEntry]) -> None:
        pass

    def prioritize(self, test_suite: list[SDCTestCase]) -> list[str]:
        return [tc.test_id for tc in test_suite]
