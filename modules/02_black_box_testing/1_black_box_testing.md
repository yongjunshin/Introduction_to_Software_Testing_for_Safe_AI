# **Black-box testing**


---

## **What is black-box testing?**

**Definition**: A family of test design techniques that derive tests from **external descriptions** of the software (requirements, specifications, user-visible behavior) **without using knowledge of the source code or internal structure**.

**Idea:**

- Testers treat the system as a “black box”: inputs are chosen and outputs (or observable behavior) are checked against expected results.
- It complements **white-box (structural)** techniques, which use the program’s internal structure; the same behavior can be exercised from both perspectives for different goals.

**Typical uses:**

- Validate that the implementation matches **agreed behavior** (acceptance, regression on contracts).
- Apply when code is unavailable, immature, or supplied by a third party.

---

## **Equivalence partitioning (EP)**

**Definition**: Divide the **input domain** (or environment conditions) into **equivalence classes** such that every value in a class is assumed to exercise the program “in the same way” with respect to the fault model.

**Idea:**

- Pick **one or few representative tests per class** instead of trying every possible input.
- Classes are often derived from requirements (valid vs. invalid ranges, categories of users, modes).

**Note:** Invalid classes matter for robustness; covering both valid and invalid partitions helps catch handling bugs without exhaustive enumeration.

---

## **Boundary value analysis (BVA)**

**Definition**: A complement to EP that focuses test selection on **values at or near the edges** of equivalence classes (min/max, just inside/outside allowed ranges, empty vs. full lists).

**Idea:**

- Many faults cluster at **off-by-one**, comparison operator mistakes, and boundary rules in specifications.
- BVA systematically stresses those edges rather than only mid-partition samples.

---

## **Combinatorial interaction testing**

**Definition**: A test design approach that covers **combinations of settings** across multiple parameters (factors), often striving for **pairwise (2-way)** or **t-wise** coverage: every pair (or t-tuple) of option values appears in at least one test case.

**Idea:**

- Full Cartesian products of many parameters explode in size; combinatorial designs shrink the suite while retaining interaction coverage.
- Used for configuration testing, GUI option mixes, and multi-field forms.

**Related term:** **Covering arrays** are mathematical objects used to build such efficient combinations.

---

## **Other black-box techniques (overview)**

Brief names only—full detail is left to the full lecture:

- **Decision table testing**: Tabulate combinations of **conditions** and **actions** to ensure each rule is exercised and no contradictory or missing rules remain hidden.
- **State transition / model-based testing**: Use a **model** of states and transitions (e.g., protocol or UI flow) to derive sequences that visit states, events, and guards systematically.
- **Use case / scenario-based testing**: Build tests from **user goals** and end-to-end scenarios (often tied to requirements documents).
- **Classification-tree method**: Hierarchically **structure input aspects** (features, constraints) and combine choices to enumerate structured test cases.
- **Random / stochastic testing**: Sample inputs from a distribution (sometimes guided by operational profiles); useful for stress and diversity, not a substitute for targeted partition design by itself.

---

### **References**

- Myers, Glenford J., Sandler, Corey, and Badgett, Tom. *The Art of Software Testing*. Wiley (classic treatment of EP, BVA, and related ideas).
- Ammann, Paul, and Offutt, Jeff. *Introduction to Software Testing*. Cambridge University Press, 2nd ed., 2016 (includes combinatorial testing and broader test design).

---

👉 **Move on to next section**: [Structural Coverages](../02_test_coverages/1_structural_coverages.md)

---

