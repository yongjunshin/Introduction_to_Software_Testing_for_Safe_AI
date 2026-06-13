"""Helper library for the SDC Testing Challenge.

Modules:
    data_loader   — load the dataset and split it into train / test
    evaluator     — compute APFD / APFDC / Time-to-first-fault (= the official
                    competition metrics) given a prioritizer's output
    visualization — plot road shapes and fault-detection curves
    baseline      — reference prioritizers (random, identity) for comparison

Students only need to import these helpers — the actual challenge work is
implementing the `prioritize()` method of their own class.
"""

from sdc_lib.data_loader import SDCTestCase, OracleEntry, load_dataset, split_train_test
from sdc_lib.evaluator import EvaluationReport, evaluate
from sdc_lib.baseline import RandomPrioritizer, IdentityPrioritizer
from sdc_lib.visualization import (
    plot_road,
    plot_roads_grid,
    plot_fault_detection_curve,
    plot_top_picks,
)

__all__ = [
    "SDCTestCase",
    "OracleEntry",
    "load_dataset",
    "split_train_test",
    "EvaluationReport",
    "evaluate",
    "RandomPrioritizer",
    "IdentityPrioritizer",
    "plot_road",
    "plot_roads_grid",
    "plot_fault_detection_curve",
    "plot_top_picks",
]
