"""Evaluate a prioritizer's output against the hidden ground-truth.

Metrics follow the official 2026 SDC Testing Competition
(`tools/prioritizers/evaluator/metrics.py` in the upstream repo).

- APFD   : Average Percentage of Faults Detected
- APFDC  : Cost-aware variant (weights faults by cumulative sim time)
- TTFF   : Time-to-First-Fault   (cumulative sim time of the first failing test)
- TTLF   : Time-to-Last-Fault    (cumulative sim time of the last failing test)
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

from sdc_lib.data_loader import OracleEntry, SDCTestCase


class Prioritizer(Protocol):
    """Duck-typed interface that any student solution must satisfy."""

    def initialize(self, oracles: list[OracleEntry]) -> None: ...
    def prioritize(self, test_suite: list[SDCTestCase]) -> list[str]: ...


@dataclass
class EvaluationReport:
    tool_name: str
    n_tests: int
    n_failed: int
    apfd: float
    apfdc: float
    time_to_first_fault: float | None
    time_to_last_fault: float | None
    initialize_seconds: float
    prioritize_seconds: float
    failed_positions: list[int]  # 1-indexed positions of failing tests in the prioritized order
    prioritized: list[str]  # the prioritizer's full output, in order

    def __str__(self) -> str:
        lines = [
            f"=== Evaluation report: {self.tool_name} ===",
            f"  test suite size      : {self.n_tests}",
            f"  failing tests in suite: {self.n_failed}",
            f"  APFD                 : {self.apfd:.4f}   (1.0 = best, 0.0 = worst, ~0.5 = random)",
            f"  APFDC (cost-aware)   : {self.apfdc:.4f}",
            f"  Time-to-first-fault  : {self._fmt_time(self.time_to_first_fault)}",
            f"  Time-to-last-fault   : {self._fmt_time(self.time_to_last_fault)}",
            f"  initialize() runtime : {self.initialize_seconds * 1000:.1f} ms",
            f"  prioritize() runtime : {self.prioritize_seconds * 1000:.1f} ms",
        ]
        return "\n".join(lines)

    @staticmethod
    def _fmt_time(t: float | None) -> str:
        return "n/a (no fault found)" if t is None else f"{t:.1f} s"


class PrioritizationError(Exception):
    pass


def _check_validity(prioritized: list[str], ground_truth: dict[str, dict]) -> None:
    """Mirror the official `check_prioritization_validity`."""
    valid_ids = set(ground_truth.keys())
    seen: set[str] = set()
    for tid in prioritized:
        if tid not in valid_ids:
            raise PrioritizationError(f"Unknown test id in prioritization: {tid!r}")
        if tid in seen:
            raise PrioritizationError(f"Duplicate test id in prioritization: {tid!r}")
        seen.add(tid)
    missing = valid_ids - seen
    if missing:
        raise PrioritizationError(
            f"Prioritization is missing {len(missing)} test id(s); for example: "
            f"{next(iter(missing))!r}"
        )


def _apfd(prioritized: list[str], ground_truth: dict[str, dict]) -> float:
    """Official APFD formula."""
    n = len(prioritized)
    failed_positions = [
        i + 1 for i, tid in enumerate(prioritized) if ground_truth[tid]["has_failed"]
    ]
    m = len(failed_positions)
    if n == 0 or m == 0:
        return 1.0
    return 1.0 - sum(failed_positions) / (n * m) + 1.0 / (2 * n)


def _apfdc(prioritized: list[str], ground_truth: dict[str, dict]) -> float:
    """Official cost-aware APFD (weighted by sim_time)."""
    cumulative_costs_to_faults: list[float] = []
    cumulative_time = 0.0
    total_cost = 0.0
    m = 0
    for tid in prioritized:
        rec = ground_truth[tid]
        cumulative_time += rec["sim_time"]
        total_cost += rec["sim_time"]
        if rec["has_failed"]:
            cumulative_costs_to_faults.append(cumulative_time)
            m += 1
    if m == 0 or total_cost == 0:
        return 1.0
    return 1.0 - sum(cumulative_costs_to_faults) / (total_cost * m) + 1.0 / (2 * m)


def _time_to_first_fault(prioritized: list[str], ground_truth: dict[str, dict]) -> float | None:
    cumulative = 0.0
    for tid in prioritized:
        cumulative += ground_truth[tid]["sim_time"]
        if ground_truth[tid]["has_failed"]:
            return cumulative
    return None


def _time_to_last_fault(prioritized: list[str], ground_truth: dict[str, dict]) -> float | None:
    cumulative = 0.0
    last = None
    for tid in prioritized:
        cumulative += ground_truth[tid]["sim_time"]
        if ground_truth[tid]["has_failed"]:
            last = cumulative
    return last


def evaluate(
    prioritizer: Prioritizer,
    train_oracles: list[OracleEntry],
    test_suite: list[SDCTestCase],
    ground_truth: dict[str, dict],
    tool_name: str | None = None,
) -> EvaluationReport:
    """Run the full pipeline: initialize -> prioritize -> score.

    Raises
    ------
    PrioritizationError
        If the returned order is not a valid permutation of the test suite.
    """
    name = tool_name or type(prioritizer).__name__

    t0 = time.perf_counter()
    prioritizer.initialize(train_oracles)
    t_init = time.perf_counter() - t0

    t0 = time.perf_counter()
    prioritized = list(prioritizer.prioritize(test_suite))
    t_prio = time.perf_counter() - t0

    _check_validity(prioritized, ground_truth)

    failed_positions = [
        i + 1 for i, tid in enumerate(prioritized) if ground_truth[tid]["has_failed"]
    ]

    return EvaluationReport(
        tool_name=name,
        n_tests=len(prioritized),
        n_failed=len(failed_positions),
        apfd=_apfd(prioritized, ground_truth),
        apfdc=_apfdc(prioritized, ground_truth),
        time_to_first_fault=_time_to_first_fault(prioritized, ground_truth),
        time_to_last_fault=_time_to_last_fault(prioritized, ground_truth),
        initialize_seconds=t_init,
        prioritize_seconds=t_prio,
        failed_positions=failed_positions,
        prioritized=prioritized,
    )
