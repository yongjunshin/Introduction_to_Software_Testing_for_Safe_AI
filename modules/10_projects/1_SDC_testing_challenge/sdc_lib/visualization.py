"""Matplotlib helpers for inspecting roads and prioritization results."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Sequence

import matplotlib.pyplot as plt

from sdc_lib.data_loader import OracleEntry, SDCTestCase

if TYPE_CHECKING:
    from sdc_lib.evaluator import EvaluationReport


def plot_road(
    test_case: SDCTestCase,
    has_failed: bool | None = None,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot a single road as a 2D line.

    If `has_failed` is given, color the line red for failing roads and
    green for passing ones.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(4, 4))
    xs = [p[0] for p in test_case.road_points]
    ys = [p[1] for p in test_case.road_points]

    if has_failed is None:
        color, label = "tab:blue", "road"
    elif has_failed:
        color, label = "tab:red", "FAIL (off-lane)"
    else:
        color, label = "tab:green", "PASS (in-lane)"

    ax.plot(xs, ys, color=color, linewidth=2, label=label)
    ax.scatter(xs[0], ys[0], marker="o", color="black", s=40, zorder=3, label="start")
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(f"test_id={test_case.test_id[:8]}…")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="best", fontsize=8)
    return ax


def plot_roads_grid(
    oracles: Sequence[OracleEntry],
    n_cols: int = 4,
    figsize_per_plot: tuple[float, float] = (3.0, 3.0),
) -> plt.Figure:
    """Plot a grid of roads with their pass/fail outcome (uses OracleEntry).

    Handy at the start of the challenge to build intuition about what
    kinds of roads tend to fail.
    """
    n = len(oracles)
    n_rows = math.ceil(n / n_cols)
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(figsize_per_plot[0] * n_cols, figsize_per_plot[1] * n_rows),
    )
    axes_flat = axes.flatten() if n > 1 else [axes]
    for ax, entry in zip(axes_flat, oracles):
        plot_road(entry.test_case, has_failed=entry.has_failed, ax=ax)
    for ax in axes_flat[len(oracles):]:
        ax.set_axis_off()
    fig.tight_layout()
    return fig


def plot_fault_detection_curve(
    failed_positions: list[int],
    n_tests: int,
    title: str = "Fault detection curve",
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot cumulative fraction of faults found vs. fraction of tests executed.

    A perfect prioritizer's curve reaches 1.0 instantly; random sits near
    the diagonal; a bad prioritizer stays flat for a long time.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 4))

    m = len(failed_positions)
    xs = [0.0]
    ys = [0.0]
    for k, pos in enumerate(sorted(failed_positions), start=1):
        xs.append(pos / n_tests)
        ys.append(k / m if m else 0)
    xs.append(1.0)
    ys.append(1.0 if m else 0.0)

    ax.plot(xs, ys, drawstyle="steps-post", linewidth=2, label="your prioritizer")
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.6, label="random expectation")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("fraction of test suite executed")
    ax.set_ylabel("fraction of faults detected")
    ax.set_title(title)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)
    return ax


def plot_top_picks(
    report: "EvaluationReport",
    test_suite: list[SDCTestCase],
    ground_truth: dict[str, dict],
    k: int = 4,
    title: str | None = None,
) -> plt.Figure:
    """Visualize the top-k roads ranked by a prioritizer.

    Each subplot shows one road colored by its true outcome — FAIL (red) means
    the prioritizer made a good catch by putting a real failure at the top;
    PASS (green) means the simulation budget would be wasted on that test.
    """
    test_by_id = {tc.test_id: tc for tc in test_suite}
    top_k_ids = report.prioritized[:k]

    fig, axes = plt.subplots(1, k, figsize=(3.2 * k, 3.2))
    axes_list = list(axes) if k > 1 else [axes]
    for ax, tid in zip(axes_list, top_k_ids):
        plot_road(test_by_id[tid], has_failed=ground_truth[tid]["has_failed"], ax=ax)

    suptitle = title or f"{report.tool_name} top-{k} picks"
    fig.suptitle(f"{suptitle}  (FAIL = good catch, PASS = wasted simulation)", y=1.02)
    fig.tight_layout()
    return fig
