# **Metamorphic Testing**
---

## **What is Metamorphic Testing?**

**Motivation**: addresses the **oracle problem**—situations where it is hard or impossible to know the exact correct output for a test case (e.g., complex numerical software or ML models)—by checking whether results obey necessary relational properties instead of exact values, effectively using these relations as a **pseudo oracle**.

**Definition**: a property-based software testing technique that addresses the test oracle problem by deriving new test cases and expected outputs from existing ones using *metamorphic relations*—necessary properties that the program’s outputs must satisfy when inputs are changed in specific ways.

**Core Concepts**:
- **Metamorphic relation (MR)**: a specified relationship between multiple input–output pairs (e.g., “scaling all inputs by 2 should double the sum”) used to generate follow-up tests and check correctness without knowing absolute expected outputs.
- **Source and follow-up test cases**: a source test is an original input with a known (or observed) output, and follow-up tests are systematically derived inputs whose outputs must satisfy the MR with the source output.
- **Oracle problem mitigation**: metamorphic testing provides a **pseudo oracle** based on MRs and is particularly useful when a reliable test oracle (exact expected output) is hard or impossible to obtain.
- **MR design and selection**: choosing meaningful, non-trivial, and domain-relevant MRs is critical to the fault-detection effectiveness of metamorphic testing.

**Domain-specific testing**: MRs are often tightly coupled to domain knowledge (e.g., numerical analysis, vision, NLP), so metamorphic testing naturally formalize and exploit such domain properties.

**Workflow**
1. **Identify suitable MRs**: use domain knowledge to define properties that must relate outputs under specific input transformations.
2. **Generate source test cases**: create initial inputs (manually or automatically) and record their observed outputs.
3. **Derive follow-up test cases**: systematically transform each source input according to an MR to obtain one or more follow-up inputs.
4. **Execute and compare**: run the program on follow-up inputs and check whether the relation between source and follow-up outputs satisfies the MR.
5 **Detect violations**: treat any MR violation as a potential fault.
---

## **Metamorphic Testing for Traditional SW**


### **Example 1: Testing mathematical functions**

**Oracle problem**: for many mathematical and numerical functions (including `sin(x)`), computing a highly accurate “ground-truth” value for arbitrary real inputs may require special tools or very high precision, so using a traditional oracle for every test case is impractical.

**Metamorphic relations for testing `sin(x)`**

| **MR description** | **Example** |
|--------------------|-------------|
| Odd symmetry: `sin(-x) = -sin(x)` (within a small numerical tolerance). | Check that `sin(-1.2) ≈ -sin(1.2)`. |
| Periodicity: `sin(x + 2π) = sin(x)`. | Check that `sin(0.7 + 2π) ≈ sin(0.7)`. |
| Pythagorean identity with cosine: `sin²(x) + cos²(x) = 1`. | For a random `x`, check that `sin(x)**2 + cos(x)**2 ≈ 1`. |
| Range constraint: outputs must stay in `[-1, 1]`. | For many random `x`, verify that `-1 - ε ≤ sin(x) ≤ 1 + ε` for a small tolerance `ε`. |
| Monotonicity on restricted intervals: on `[-π/2, π/2]`, `sin(x)` is strictly increasing. | Sample `x1 < x2` in `[-π/2, π/2]` and check that `sin(x1) < sin(x2)` up to numerical noise. |


### **Example 2: Testing Search Engine [1]**

**Oracle problem**: for commercial search engines there is no clear ground-truth ranked list, specifications are largely hidden, and relevance is subjective and changes over time—so most queries have no precise oracle.

**Metamorphic relations**

| **MR description** | **Example** |
|------------------------------|-------------|
| A page that appears in the results for an exact keyword/phrase query should not “disappear” if we repeat the same query but restrict it to that page’s domain. | If the top result for `["open source search engine"]` is from domain `example.com`, then restricting the query to `site:example.com "open source search engine"` should still retrieve that page. |
| If we take the title of a result and use it as a new query, the original page should show up near the top of the results. | Given a result whose title contains “introduction to metamorphic testing”, using that title as a new query should return the original page within the top results. |
| Reversing the order of several quoted names combined with AND should still return very similar result sets. | Queries like `["Vincent Van Gogh" AND "Albert Einstein"]` and `["Albert Einstein" AND "Vincent Van Gogh"]` should return highly overlapping result sets. |
| Swapping the order of two ordinary query words should not drastically change the top‑k results. | `["software testing"]` and `["testing software"]` should yield similar top‑k results. |
| If we take the top result of a query and then search again using the same query but restricted to that site, that page should still be found. | If the top result for `["metamorphic testing"]` is from `example.org`, then querying `"metamorphic testing" site:example.org` should still list that page among the results. |


---

## **Metamorphic Testing for DL SW**

**Fitness of metamorphic testing to DL testing**: DL models often lack clear ground-truth oracles, but we can still test them by checking whether their outputs respect well-chosen metamorphic relations (e.g., invariance to small noise or consistency under simple input changes).


The SE community has been steadily developing metamorphic testing as a mature methodology **since 1998**, building a solid foundation of theory, tools, and case studies that can now be effectively applied to testing DL systems. Many approaches proposed in the AI/ML field (e.g., invariance testing, perturbation-based testing, input transformation tests) are conceptually similar to metamorphic testing and can be viewed as instances of it, further improved by leveraging the rich foundations the SE community has developed over decades.  

### **Example 1: Testing CNN**


### **Example 2: Testing LLM**


---

### **References**

- [1] Zhou, Zhi Quan, Shaowen Xiang, and Tsong Yueh Chen. "Metamorphic testing for software quality assessment: A study of search engines." IEEE Transactions on Software Engineering (TSE) 42.3 (2015): 264-284.

---

👉 **Move on to exercises**: 
- [CNN Metamorphic Testing Exercise](./exercises/cnn_metamorphic_testing_exercise.ipynb)
- [LLM Metamorphic Testing Exercise](./exercises/llm_metamorphic_testing_exercise.ipynb)

👉 **Move on to next section**: [Input Diversity](../07_input_diversity/1_input_diversities.md)

---