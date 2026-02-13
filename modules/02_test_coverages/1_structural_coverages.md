# **Structural Coverages**


---

## **What is Structural Test Coverage?**

**Definition**: A metric that quantifies the extent to which the source code of a program has been executed during testing. 

Structural coverage provides insight into which parts of the code have actually been tested and which remain unexplored. 
This approach is crucial for identifying untested code segments, reducing the risk of hidden bugs, and ensuring that critical execution paths are validated. By measuring coverage, developers can make informed decisions about **test suite adequacy** and prioritize additional test cases for poorly covered areas.

**Importance:**

Structural coverage provides a rigorous, measurable approach to ensure software is sufficiently tested. 

More intuitively, testing based on structural coverage is necessary to sell software products in regulated markets. Safety-critical industries often mandate specific coverage levels. 

For example, ISO 26262 (automotive functional safety standard) requires 100% MC/DC coverage for the highest safety integrity levels, making coverage metrics essential for regulatory compliance and commercial viability.

---

Consider the following function as an example under test:

```python
1   def function_under_test(A, B, C):
2       X = 0
3       
4       if A > 5 and B < 10:
5           X = 1
6       else:
7           X = 2
8       
9       if C == 1:
10          Y = 1
11      else:
12          Y = 2
13      
14      return X + Y
```

Five major structural coverages will be introduced with the example.

---

## **Statement Coverage**

**Definition**: The percentage of statements in the code that have been executed by at least one test case.

**Formula**:

$$\text{Statement Coverage} = \frac{\text{Number of Executed Statements}}{\text{Total Number of Executable Statements}} \times 100\%$$

**Example**: Using our `function_under_test` with test input `(A=6, B=5, C=1)`:
- The test executes: lines 2, 5, 10, and 14
- The test does NOT execute: lines 7 and 12 (the else branches)
- **Executed statements**: 4 out of 6 executable statements
- **Statement Coverage**: 4/6 × 100% = **66.67%**
- To achieve **100% statement coverage**, we need additional test cases like:
  - `(A=3, B=15, C=2)` - covers lines 7 and 12

---

## **Branch (Decision) Coverage**

**Definition**: The percentage of branches (decision outcomes) that have been executed. Each decision point (if statement) has two branches: true and false.

**Formula**:

$$\text{Branch Coverage} = \frac{\text{Number of Executed Branches}}{\text{Total Number of Branches}} \times 100\%$$

**Example**: Using our `function_under_test` with test input `(A=6, B=5, C=1)`:
- **Total branches**: 4 branches (2 decisions × 2 outcomes each)
  - Line 4: `if A > 5 and B < 10` → True branch (line 5), False branch (line 7)
  - Line 9: `if C == 1` → True branch (line 10), False branch (line 12)
- The test executes: Line 4 → True (line 5), Line 9 → True (line 10)
- **Branch Coverage**: 2/4 × 100% = **50%**
- To achieve **100% branch coverage**, we need additional test cases like:
  - `(A=3, B=5, C=2)` - covers False/False branches

---

## **Condition Coverage**

**Definition**: The percentage of individual boolean conditions that have been evaluated to both true and false at least once.

**Formula**:

$$\text{Condition Coverage} = \frac{\text{Number of Condition Outcomes Executed}}{\text{Total Number of Condition Outcomes}} \times 100\%$$

**Example**: Using our `function_under_test` with test input `(A=6, B=5, C=1)`:
- **Total conditions**: 3 conditions with 6 possible outcomes (each condition needs True and False)
  - Condition `A > 5`: needs to be True and False
  - Condition `B < 10`: needs to be True and False
  - Condition `C == 1`: needs to be True and False
- The test makes: `A > 5` = True, `B < 10` = True, `C == 1` = True (3 out of 6 outcomes)
- **Condition Coverage**: 3/6 × 100% = **50%**
- To achieve **100% condition coverage**, we need additional test cases like:
  - `(A=3, B=15, C=2)` - covers `A > 5` = False, `B < 10` = False, `C == 1` = False
- **Note**: 100% condition coverage does NOT guarantee 100% branch coverage!

---

## **Path Coverage**

**Definition**: The percentage of all possible execution paths through the code that have been executed. A path is a unique sequence of statements from entry to exit.

**Formula**:

$$\text{Path Coverage} = \frac{\text{Number of Executed Paths}}{\text{Total Number of Paths}} \times 100\%$$

**Example**: Using our `function_under_test` with test input `(A=6, B=5, C=1)`:
- **Total paths**: 4 paths (2 decisions with 2 branches each = 2² = 4 paths)
  1. Path 1: Line 2 → Line 5 (True) → Line 10 (True) → Line 14
  2. Path 2: Line 2 → Line 5 (True) → Line 12 (False) → Line 14
  3. Path 3: Line 2 → Line 7 (False) → Line 10 (True) → Line 14
  4. Path 4: Line 2 → Line 7 (False) → Line 12 (False) → Line 14
- The test executes Path 1: True/True → returns 1+1=2
- **Path Coverage**: 1/4 × 100% = **25%**
- To achieve **100% path coverage**, we need additional test cases like:
  - `(A=6, B=5, C=2)` - covers Path 2 (True/False → returns 3)
  - `(A=3, B=5, C=1)` - covers Path 3 (False/True → returns 3)
  - `(A=3, B=5, C=2)` - covers Path 4 (False/False → returns 4)
- **Challenge**: Path coverage is the most comprehensive but can be **infeasible to achieve** for complex code due to:
  - Exponential growth (loops and nested conditions create millions of paths)
  - Some paths may be logically unreachable due to dependencies between conditions

---

## **MC/DC Coverage**

**Definition**: Modified Condition/Decision Coverage ensures that each condition independently affects the decision outcome. Each condition must be shown to independently change the decision result while holding other conditions constant.

**Formula**:

$$\text{MC/DC Coverage} = \frac{\text{Number of Conditions with Independence Proven}}{\text{Total Number of Conditions}} \times 100\%$$

Note: Each condition must be proven to independently affect its decision outcome.

**Example**: Using our `function_under_test` with test inputs `(A=6, B=5, C=1)` and `(A=3, B=5, C=1)`:
- **Requirements**: Each condition must independently affect the decision outcome. This means:

| Condition to Test | Must Find Test Pair Where... | Corresponding Decision Must Change |
|-------------------|------------------------------|-----------------------------------|
| **A** (`A > 5`) | Only A changes (B, C stay same) | Decision 1: True↔False |
| **B** (`B < 10`) | Only B changes (A, C stay same) | Decision 1: True↔False |
| **C** (`C == 1`) | Only C changes (A, B stay same) | Decision 2: True↔False |

- Two tests `(A=6, B=5, C=1)` and `(A=3, B=5, C=1)` prove **A** independence (only A changes, Decision 1 changes)
- **MC/DC Coverage**: 1/3 × 100% = **33.33%** (only 1 out of 3 conditions proven independent)
- To achieve **100% MC/DC coverage**, we need four test cases that prove independence:

| Test Case | A>5 | B<10 | Decision 1 | C==1 | Decision 2 | MC/DC Test Case? |
|-----------|-----|------|------------|------|------------|------------------|
| `(A=6, B=5, C=1)` | T | T | **True** | T | **True** | **O** (Baseline) |
| `(A=3, B=5, C=1)` | F | T | **False** | T | **True** | **O** (Proves A) |
| `(A=6, B=15, C=1)` | T | F | **False** | T | **True** | **O** (Proves B) |
| `(A=6, B=5, C=2)` | T | T | **True** | F | **False** | **O** (Proves C) |


- **Why MC/DC?** Required by safety-critical standards (ISO 26262, DO-178C) because:
  - Provides strong decision-level coverage with linear test growth (O(#condition)), unlike the exponential growth of full path coverage.
  - MC/DC offers a practical balance between thoroughness and feasibility for safety-critical systems

---

👉 **Move on to exercises**: 
1. [Structural Coverage Exercise](./exercises/01_structural_coverages_exercise.ipynb)
2. [Pytest Exercise](./exercises/02_pytest_exercise.ipynb)

👉 **Move on to next section**: [Neuron Coverages](2_neuron_coverages.md)