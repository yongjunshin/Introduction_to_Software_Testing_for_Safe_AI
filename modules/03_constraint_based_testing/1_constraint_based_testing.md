# **Constraint-based testing**


---

## **What is constraint-based testing?**

**Constraint-based testing** refers to methods that **express** intended behavior, reachability goals, or failure scenarios as **logical constraints** over inputs (and sometimes configuration or state), then use **automated solvers** to obtain **concrete test data** or to learn that **no** suitable input exists.

**Typical workflow:**

- **Build a constraint model** from a requirement, a **path condition** (conditions accumulated along a control-flow path), or a **property** you want to refute.
- **Query a solver** for **satisfiability** relative to that model.
- **Use the outcome** to drive testing: **witness inputs** become test cases, or **impossibility** results inform coverage (e.g., infeasible path, inconsistent spec).

This idea aligns with **symbolic execution**, **model checking**-style reasoning, and hybrid setups where **search** proposes candidates and **solvers** refine or discharge feasibility.

---

## **Example SuT (Python)**

The running example is a small function with one **compound decision**. It is intentionally tiny so we can talk about **path conditions** without implementation noise.

```python
def environment_alert(temp_c: float, humidity_pct: float) -> str:
    """Return ALERT when it is hot and humid; otherwise normal."""
    if temp_c > 30.0 and humidity_pct >= 70.0:
        return "ALERT"
    return "normal"
```

**Branches:**

| Outcome | Logical guard (path condition on inputs) |
|---------|-------------------------------------------|
| `"ALERT"` | `temp_c > 30.0` **and** `humidity_pct >= 70.0` |
| `"normal"` | **not** the above—e.g. cooler air, or humidity below the threshold |

Any test input \((t, h)\) you choose either satisfies the **alert guard** or lands in the **normal** side; solvers help you **pick** \((t, h)\) **deliberately** instead of guessing.

---

## **Linking the SuT to solver-backed testing**

**What tools like SMT solvers are for (lab: how to call them)**

**SMT** (*Satisfiability Modulo Theories*) solvers—examples include **Z3**, **cvc5**, and similar—decide whether constraints over variables (arithmetic, arrays, etc.) are **jointly satisfiable**. API usage stays in the **exercise**; here we only connect outcomes to `environment_alert`.

- If the answer is **`sat`**, the tool yields **concrete values** for `temp_c` and `humidity_pct` that **satisfy** the formula you gave—ready to pass into `environment_alert(...)`.
- If **`unsat`**, **no** input satisfies that formula: useful for spotting **impossible** combinations under your model (infeasible path, inconsistent requirements).

---

### **Target the `ALERT` path**

To generate a test that **must** take the first branch and return `"ALERT"`, you would pose constraints equivalent to the guard:

- `temp_c > 30.0`
- `humidity_pct >= 70.0`

A solver that finds any \((t, h)\) satisfying both gives you a **witness**—for example \(t = 35\), \(h = 80\). You then **run** `environment_alert(35.0, 80.0)` and **assert** the result is `"ALERT"`. The values are **guaranteed** to hit that branch by construction, which supports **targeted** branch testing without manual search.

You can **strengthen** the same model to bias toward **boundaries** (e.g. humidity exactly at `70.0`, or temperature just above `30.0`) to stress **comparison-off-by-one** style bugs—still as **extra constraints**, not by resampling at random.

---

### **When the solver says “no such input” (`unsat`)**

Suppose you also model deployment rules, e.g. **sensors never report** `temp_c > 28.0` in a certain product mode. You **conjoin** that envelope with the **alert guard** (`temp_c > 30.0` …). The combined formula may be **`unsat`**: there is **no** witness that is both **operationally allowed** and **raises ALERT**. That is a useful signal for **requirements review** (contradiction) or for concluding that the **ALERT** branch is **unreachable** under those assumptions—distinct from writing a test that **passes** or **fails** at runtime.

---

## **How this supports testing practice (summary)**

| Solver outcome | Testing angle (with `environment_alert`) |
|------------------|-------------------------------------------|
| **`sat` + model** | Evaluate `environment_alert(t, h)` on solver-produced \((t,h)\); assert `"ALERT"` or `"normal"` as intended for that model. |
| **`unsat`** | No input matches the posed constraints—revisit spec vs. envelope or mark infeasibility. |
| **Changing the constraint set** | Move from **alert-region** tests to **normal-region** tests (negation or disjoint cases), or add **boundary** equalities, to build a small but **purposeful** suite. |

---

### **References**

- de Moura, Leonardo, and Nikolaj Bjørner. “Z3: An efficient SMT solver.” *TACAS*. Springer, 2008.
- Barrett, Clark, et al. “cvc5: A Versatile and Industrial-Strength SMT Solver.” *TACAS*. 2022.
- Godefroid, Patrice, Nils Klarlund, and Koushik Sen. “DART: Directed automated random testing.” *ACM SIGPLAN Notices* 40.6 (2005): 213–223.

---

👉 **Move on to next section**: [Search-based Testing](../05_search_based_testing/1_search_based_testing.md)

---

