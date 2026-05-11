# **Regression testing**


---

## **Regression fault and regression testing**

**Regression fault**: A **new or re-emerged defect** in software that previously worked correctly for some behavior—often introduced by a **change** (patch, refactor, configuration, dependency update) that unintentionally breaks existing functionality elsewhere.

**Regression testing** (retesting for regressions): Re-executing tests after changes to **verify that existing, previously passing behavior still holds**. The goal is to detect regression faults **as early and cheaply** as possible within project constraints.

**Typical triggers:**

- Code merges, feature work, bug fixes, refactors, library or model updates, environment or data pipeline changes.

---

## **Retest-all vs. regression testing techniques**

**Retest all**: Run **every** test in the suite after each change. 

- **Pros**: Conceptually simple; **high confidence** if the suite is strong and environments are stable.
- **Cons**: Does **not scale**—run time, machine cost, and feedback delay grow with suite size and CI frequency.

**Selective regression testing**: Apply **techniques** (selection, prioritization, minimization) to run a **subset or order** of tests that still aims to expose regressions while controlling cost.

- Research and practice distinguish **safe** approaches (under stated assumptions, missing a fault is unlikely) from **risk–benefit** heuristics when budgets are tight.

---

## **Test suite minimization**

**Definition**: Given a test suite \(T\), produce a **smaller** subset \(T' \subseteq T\) that **still satisfies a criterion**—for example, preserving **structural coverage**, covering a set of **requirements**, or killing a set of **mutants**.

**Idea:**

- Remove **redundant** tests that do not add value under the chosen sufficiency model.
- Often framed as an optimization problem; exact minimization can be **hard** (set-cover–like structures), so **greedy heuristics** are common in toolchains.

**Note:** Minimization targets **size** of the retained set; it does not by itself define **execution order** (that is prioritization).

---

## **Test suite prioritization**

**Definition**: Assign an **order** to tests (or test chunks) so that **more important** tests run **earlier**—for example, to **fail fast** in CI, surface faults relevant to the **latest change**, or maximize **estimated fault detection** per unit time.

**Idea:**

- The **full** suite may still run eventually; prioritization improves **feedback latency** and resource use on **partial** runs.
- Order can depend on **historical failure rates**, **code churn**, **coverage overlap with changed files**, **requirement criticality**, or **machine-learning predictors**.

---

## **Test case selection**

**Definition**: Choose a **subset** of tests to run for a **given build or change**—without necessarily minimizing the whole suite globally.

**Idea:**

- Map **changes** (diffs, affected modules, data contracts) to **tests that might be behaviorally relevant**.
- Contrasts with **minimization** (smallest suite meeting a global constraint) and overlaps with **prioritization** when selection **orders** the chosen subset for execution.

**Common families (names only for this summary):**

- **Change-impact** or **coverage-based** selection (tests exercising changed entities).
- **History-based** selection (tests that failed or touched volatile areas recently).
- **Policy-based** gates (must-run smoke sets alongside selective expansion).

---

### **References**

- Rothermel, Gregg, and Mary Jean Harrold. “A safe, efficient algorithm for regression test selection.” *Software Engineering* (ICSE). 1994.
- Yoo, Shin, and Mark Harman. “Regression testing minimization, selection and prioritization: a survey.” *Software Testing, Verification and Reliability* 22.2 (2012): 67–120.

---

👉 **Move on to next section**: [Interactive Testing](../09_interactive_testing/1_interactive_testing.md)

---

