# **Neuron Coverages**

We'll learn neuron coverages of DNN testing inspired by structural coverages.

---

## **DNN Testing Adequacy**

Just as structural coverage metrics help us assess whether traditional software has been adequately tested, we need similar metrics to evaluate the thoroughness of testing for deep neural networks.

**Key Challenges:**
- DNNs lack explicit control flow and conditional statements found in traditional software
- Instead, they consist of layers of interconnected neurons with continuous activation values
- The fundamental question: *How do we know if our test inputs sufficiently exercise the internal behaviors of a neural network?*

**Solution:**
- Software engineering researchers developed DNN-specific coverage criteria inspired by traditional structural testing (statement, branch, MC/DC)
- These metrics measure how thoroughly test inputs:
  - Activate individual neurons
  - Explore neuron activation ranges
  - Exercise relationships between neurons across layers
- They provide quantifiable ways to assess test suite adequacy for deep learning systems

---

## **Neuron Coverage**<sup id="fnref1">[1](#fn1)</sup>

**Definition**: A neuron is covered by a test input if the neuron is activated (produces a positive output) for that input.

Neuron coverage requires that each neuron in the network must be activated at least once by some test input in the test suite. Similar to *statement coverage*, this metric provides a basic measure of how thoroughly the test inputs exercise the different neurons in the neural network, ensuring that every neuron "fires" at least once during testing.

---

## **(K-multisection) Neuron Coverage**<sup id="fnref2a">[2](#fn2)</sup>

**Definition**: For a given neuron, k-multisection neuron coverage measures how thoroughly a test suite covers the neuron's *normal activation value range* (observed during training) by dividing it into k equal sections and computing the ratio of covered sections to total sections.

This metric takes the neuron's activation range observed during training and divides it into k equal sections. A section is covered if at least one test input produces an activation value within that section. The coverage is calculated as the ratio of covered sections to total sections (k). This ensures that test inputs exercise the neuron at different intensity levels across its normal operating range, providing a more fine-grained assessment than basic neuron coverage which only checks if the neuron activates at all.

---

##  **Neuron Boundary Coverage**<sup id="fnref2b">[2](#fn2)</sup>

**Definition**: A neuron is boundary covered by a test input if the activation value produced by that input exceeds the maximum activation value observed for that neuron during training, thus exploring corner-case behaviors.

While k-multisection coverage focuses on the normal operating range, boundary coverage specifically identifies test cases that push neurons *beyond* their typical operating ranges seen in the training data. This metric targets extreme or corner-case scenarios by finding inputs that produce stronger activations than any training example, helping to detect how the network behaves outside its normal training distribution and revealing potential vulnerabilities or unexpected behaviors at the boundaries of the neuron's learned behavior.

---

##  **Top-k Neuron Coverage**<sup id="fnref2c">[2](#fn2)</sup>

**Definition**: Top-k neuron coverage measures how many individual neurons have been among the top k most activated neurons on their layer at least once across all test inputs.

For each test input, we identify the k most activated neurons on each layer. A neuron is covered if it appears in the top-k for its layer for at least one test input. The coverage is the ratio of covered neurons to total neurons in the network. This metric focuses on exercising *individual neurons* with strong activations, ensuring that different dominant neurons are triggered across layers.

---

## **Top-k Neuron Pattern Coverage**<sup id="fnref2d">[2](#fn2)</sup>

**Definition**: Top-k neuron pattern coverage measures the number of unique activation patterns across the network, where each pattern is the combination of top-k neurons from all layers for a given test input.

For each test input, the top-k neurons on each layer together form a pattern. For example, with k=2 and 3 layers, a pattern might be ({n₁, n₃}, {n₅, n₆}, {n₈, n₉}). This metric counts how many distinct patterns appear across all test inputs. While top-k neuron coverage focuses on individual neurons, pattern coverage captures the *combinations* of dominant neurons across layers, revealing diverse decision-making pathways through the network.



---

## **SS/SV/VV Coverage**<sup id="fnref3">[3](#fn3)</sup>

**Definition**: SS (Sign-Sign), SV (Sign-Value), and VV (Value-Value) coverages measure how changes in one neuron's activation independently affect neurons in subsequent layers, inspired by MC/DC coverage.

These criteria evaluate neuron relationships at different granularities. **SS coverage** checks if flipping a neuron's activation state (active/inactive) flips another neuron's state. **SV coverage** checks if changing a neuron's activation state changes another neuron's output magnitude, even if its state remains the same. **VV coverage** checks if continuous changes in one neuron's output value cause continuous changes in another neuron's output value. They form a hierarchy (SS ⊂ SV ⊂ VV) where VV is the most comprehensive, capturing fine-grained continuous dependencies between neurons across layers.

---

## **Surprise Coverage**<sup id="fnref4">[4](#fn4)</sup>

**Definition**: Surprise coverage measures how surprising a test input is to a neural network by comparing its activation pattern to those of the training data.

It evaluates how far a test input’s internal activations deviate from what the model has seen during training, capturing the novelty or out-of-distribution behavior of the input. Test inputs that produce activation patterns unlike any training sample are considered highly surprising. By dividing the surprise scores into intervals and measuring how many are covered by test inputs, this metric ensures that testing explores both familiar and unexpected activation regions of the model.


---

## **Importance-Driven Coverage**<sup id="fnref5">[5](#fn5)</sup>

**Definition**: Importance-driven coverage measures how thoroughly test inputs exercise neurons that are most influential to the model’s output.

Instead of treating all neurons equally, it focuses on *important neurons*—those contributing most to decision-making—and checks whether test inputs cover their major activation behaviors or clusters. This prioritization ensures that testing concentrates on semantically meaningful internal components, improving test efficiency and the likelihood of detecting faults that affect the model’s actual predictive logic.


---



### **References**

- <a id="fn1"></a>**[1]**: Pei, Kexin, et al. "Deepxplore: Automated whitebox testing of deep learning systems." proceedings of the 26th Symposium on Operating Systems Principles (SOSP). 2017.

- <a id="fn2"></a>**[2]**: Ma, Lei, et al. "Deepgauge: Multi-granularity testing criteria for deep learning systems." Proceedings of the 33rd ACM/IEEE international conference on automated software engineering (ASE). 2018.

- <a id="fn3"></a>**[3]**: Sun, Youcheng, et al. "Structural test coverage criteria for deep neural networks." ACM Transactions on Embedded Computing Systems (TECS) 18.5s (2019): 1-23.

- <a id="fn4"></a>**[4]**: Kim, Jinhan, Robert Feldt, and Shin Yoo. "Guiding deep learning system testing using surprise adequacy." 2019 IEEE/ACM 41st International Conference on Software Engineering (ICSE). IEEE, 2019.

- <a id="fn5"></a>**[5]**: Gerasimou, Simos, et al. "Importance-driven deep learning system testing." Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering (ICSE). 2020.


---

👉 **Move on to exercise**: [Neuron Coverage Exercise](./exercises/neuron_coverages_exercise.ipynb)

👉 **Move on to next section**: [Fuzz Testing](../03_fuzz_testing/1_fuzz_testing.md)


---