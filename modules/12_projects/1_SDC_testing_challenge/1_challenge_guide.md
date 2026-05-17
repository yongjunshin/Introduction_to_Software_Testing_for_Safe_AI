# SDC Testing Challenge — Guide

> A test-prioritization competition for self-driving car (SDC) simulator tests.
> Modelled on the **2026 ICST/SBFT SDC Testing Tool Competition**, simplified to run inside this course's JupyterLab environment.

---

## 1. Background — why does this matter?

Self-driving cars (SDCs) are tested in **driving simulators** like BeamNG.tech before ever touching a real road. Each test case asks the simulator: *"Drive along this road shape — can you stay in the lane the whole way, or do you go off the lane?"*

A single test typically takes **tens of seconds to a few minutes** of wall-clock simulation time. A modern SDC project may have **hundreds or thousands of such tests** — running them all on every code change is too expensive. Three classical strategies help:

- **Test selection** — pick only the relevant subset of tests for a change.
- **Test prioritization** — reorder the tests so failures appear early.   ← *this challenge*
- **Test minimization** — discard redundant tests altogether.

If you reorder the tests well, the developer can stop simulation as soon as the first few failures show up, instead of waiting for the whole suite. That's the entire goal of this challenge.

---

## 2. The task

You will write a Python class with two methods:

```python
class MyPrioritizer:
    def initialize(self, oracles: list[OracleEntry]) -> None:
        """(Optional) learn from labelled training data.
        Each OracleEntry = (SDCTestCase, has_failed: bool).
        """

    def prioritize(self, test_suite: list[SDCTestCase]) -> list[str]:
        """Return the test_ids in the order you want them executed.
        Must be a permutation of the input ids.
        """
```

### What an `SDCTestCase` looks like

```python
SDCTestCase(
    test_id     = "65ca1d9f16ba3922d7ad21d5",
    road_points = [(51.97, 10.00), (52.10, 12.09), (52.14, 13.14), ...],  # 197 (x, y) points
)
```

The car starts at the first point and follows the line traced by the rest. Roads with many sharp turns, long stretches, or unusual geometry tend to be harder for the autopilot.

### What the evaluator gives you vs. hides from you

| What | Available in `initialize()` | Available in `prioritize()` | Held only by evaluator |
|---|---|---|---|
| `test_id` & `road_points` | ✅ | ✅ | — |
| `has_failed` label | ✅ (train set) | ❌ | ✅ (test set) |
| `sim_time` (simulator duration) | ❌ | ❌ | ✅ |

You can do whatever you want with the training data — handcraft rules, train a classifier, ignore it entirely. The only contract is: given an unlabelled test suite, return a good order.

---

## 3. How you are scored — APFD

The primary metric is **APFD** (*Average Percentage of Faults Detected*), defined as:

$$\text{APFD} = 1 - \frac{\sum_{i=1}^{m} \text{pos}_i}{n \cdot m} + \frac{1}{2n}$$

where
- *n* = total number of tests in the suite,
- *m* = number of failing tests,
- *posᵢ* = 1-indexed position of the *i*-th failure in your ordering.

Intuition:

- **APFD = 1.0** → all failures are at the very top of your list. Perfect.
- **APFD ≈ 0.5** → failures are scattered uniformly. Same as a random shuffle.
- **APFD = 0.0** → all failures are at the very bottom. Worst possible.

#### Worked mini-example (n = 10, m = 3)
| Ordering of failures | Position sum | APFD |
|---|---|---|
| Failures at positions 1, 2, 3 | 6 | **0.85** (very good) |
| Failures at positions 4, 5, 6 | 15 | **0.55** (slightly better than random) |
| Failures at positions 8, 9, 10 | 27 | **0.15** (worse than random) |

Two secondary metrics are reported but **not used for ranking**:
- **APFDC** — APFD weighted by simulation time per test (catches "you put a failure first, but it was a tiny 1-second test").
- **Time-to-first-fault** — cumulative sim time until the first failure (how quickly the developer sees a problem in real wall-clock terms).

The formulas come straight from the upstream competition evaluator (`tools/prioritizers/evaluator/metrics.py`).

---

## 4. How to run this challenge

The whole challenge lives in this folder:

```
modules/12_projects/1_SDC_testing_challenge/
├── 1_challenge_guide.md                    ← this document
├── exercises/
│   └── sdc_prioritization_challenge.ipynb  ← the notebook you work in
├── data/
│   └── sdc-test-data.json                  ← 956 pre-simulated test cases (PASS=603, FAIL=353)
└── sdc_lib/                                ← helpers — don't edit these
    ├── data_loader.py
    ├── evaluator.py
    ├── baseline.py
    └── visualization.py
```

### Steps

1. From the project root, start JupyterLab:
   ```bash
   ./scripts/run_jupyter.sh
   ```
2. Open `modules/12_projects/1_SDC_testing_challenge/exercises/sdc_prioritization_challenge.ipynb`.
3. Run all cells once with the **default identity prioritizer** to confirm everything works. You should see an APFD around 0.5 from the baselines.
4. Edit only the `MyPrioritizer` class cell (Section 4 of the notebook). Re-run Section 5 to see your new score.
5. Iterate.

> The dataset is loaded once at startup; subsequent runs are sub-second. Feel free to try many ideas quickly.

---

## 5. Ideas to try (low → high effort)

1. **No-op (identity)** — establishes your baseline at ~0.50.
2. **Sort by total road length** — longer roads have more chance to drift off-lane.
3. **Sort by total curvature** — sharper roads stress the autopilot more.
4. **Sort by maximum local turn angle** — even one tight corner can be enough.
5. **Engineered features + a sklearn classifier** — extract a handful of geometric features per road (length, mean curvature, max curvature, number of inflection points, bounding-box area, etc.); train e.g. `RandomForestClassifier` on `train_oracles`; sort the test suite by predicted failure probability.
6. **Ensembles / hybrid** — combine multiple signals (e.g., normalize curvature and length scores and average them).

The official competition includes ML-based tools that achieve `APFD ≈ 0.7–0.8`. With a careful feature set you can get close.

---

## 6. Validity check

The evaluator will refuse your output if any of these are true:
- It contains an ID that is **not** in the test suite.
- The same ID appears more than once.
- Some ID from the test suite is missing.

These rules mirror the official `MetricEvaluator.check_prioritization_validity`. If your output fails the check, the evaluator raises `PrioritizationError` and prints a hint about what's wrong.

---

## 7. Differences vs. the real ICST competition

This local exercise keeps the **algorithm task and metrics exactly the same** as the real competition. What we removed for classroom use:

| Aspect | ICST/SBFT 2026 competition | This exercise |
|---|---|---|
| Interface | gRPC service (`Initialize`, `Prioritize` RPCs) | Plain Python class with the same two methods |
| Packaging | Docker image submitted to evaluator | Run inside the existing course JupyterLab container |
| Data source | MongoDB + PostgreSQL (SensoDat) | Single `sdc-test-data.json` (same upstream tests, no DB) |
| Simulator | BeamNG.tech runs on the eval server | Pre-cached PASS/FAIL outcomes from the upstream dataset |
| Dataset size | thousands of tests sampled per evaluation | 956 tests, fixed split (seed=42), train_ratio=0.2 |
| Submission | Pull request with Docker image link | Save your notebook with the final evaluation report visible |

What stayed **identical**:
- Test case definition (`testId` + sequence of `(x, y)` road points).
- Two-phase interface (`initialize(oracles)` → `prioritize(test_suite)`).
- Pass/fail definition (car stays in-lane / drives off-lane).
- Metrics: APFD, APFDC, time-to-first-fault — same formulas as `tools/prioritizers/evaluator/metrics.py` upstream.
- Validity rules for the prioritization output.

Your `MyPrioritizer.prioritize` method is the same algorithm a real ICST submission would put inside their gRPC server. Only the wrapper differs.

---

## 8. Further reading

- Competition repository: <https://github.com/christianbirchler-org/sdc-testing-competition>
- 2026 competition page: <https://github.com/christianbirchler-org/sdc-testing-competition/blob/main/competitions/2026.md>
- ICST 2025 track page (template for 2026 venue): <https://conf.researchr.org/track/icst-2025/icst-2025-tool-competition--self-driving-car-testing>
- Birchler et al., *Machine learning-based test selection for simulation-based testing of self-driving cars software*, Empirical Software Engineering 28(71), 2023.
- Yoo & Harman, *Regression testing minimization, selection and prioritization: a survey*, STVR 22(2), 2012.

Have fun — and don't be discouraged if your first try is barely above 0.5. That's how every research team also started.
