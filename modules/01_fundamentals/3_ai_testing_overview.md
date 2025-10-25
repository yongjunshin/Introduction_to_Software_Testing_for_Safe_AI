# **AI Testing Overview**

We'll provide an overview of AI testing concepts.

---
## **Testing for AI vs. AI for Testing**
*(Also known as SE4AI vs. AI4SE)*

| **Aspect** | **Testing AI Systems (SE4AI)** | **AI-Augmented Testing (AI4SE)** |
|------------|--------------------------------|----------------------------------|
| **Goal** | Validate AI/ML model correctness, safety, and reliability | Use AI techniques to improve traditional software testing |
| **Approaches** | • Validating autonomous vehicle safety systems<br>• Medical diagnosis model accuracy testing<br>• Fraud detection algorithm verification<br>• Metamorphic testing for model robustness<br>• Differential testing between model versions | • Automated test case generation from requirements<br>• Machine learning identifying buggy code patterns<br>• Smart test prioritization based on risk analysis<br>• Neural networks optimizing test data selection |

This course will focus on testing AI systems (i.e., machine learning-based software).

---

## **Characteristics of Testing ML-based Systems**

### **Traditional Software vs. ML-based Software Testing**

| **Aspect** | **Traditional Software** | **ML-based Software** |
|------------|-------------------------|----------------------|
| **Development** | Written by developers | Trained from data |
| **Core Component** | Code and algorithms | (Deep) neural networks |
| **Behavior** | Deterministic and predictable | Probabilistic and non-deterministic |
| **Testing Goal** | Verify implementation matches specification | Validate model performance and safety |
| **Input Space** | Finite and manageable | Infinite and unmanageable |
| **Oracle** | Explicit (from specifications) | Often implicit or learned from data |



### **Challenges of Software Testing for ML systems**

**Reference**: Marijan, D., & Gotlieb, A. (2020). Software testing for machine learning. In *Proceedings of the AAAI Conference on Artificial Intelligence* (Vol. 34, No. 09).

| **Challenge** | **Summary** |
|---------------|-------------|
| **Missing Test Oracles** | ML systems operate on probabilistic reasoning, producing non-deterministic outputs that can vary even for the same inputs. This makes it hard to define expected outputs (oracles). Techniques such as pseudo-oracles, metamorphic testing, and test data prioritization are explored but remain limited. |
| **Infeasibility of Complete Testing** | The enormous and high-dimensional input space of ML models makes exhaustive testing impossible. Coverage metrics like neuron coverage, DeepCover, and DeepGauge aim to measure adequacy, but they face issues like combinatorial explosion and limited scalability. |
| **Quality of Test Datasets for ML Models** | The correctness of ML models depends heavily on the quality of their training and test data. Approaches such as DeepMutation and MuNN adapt mutation testing to evaluate dataset quality but struggle with realism and domain-specific mutation operators. |
| **Vulnerability to Adversaries** | ML models are easily fooled by adversarial examples—slightly perturbed inputs that cause misclassification. Various generation methods (FGSM, DeepFool, AdvGAN) and defensive measures (distillation, verification) exist, but they remain computationally expensive and incomplete. |
| **Evaluating the Robustness of ML Models** | Robustness testing focuses on measuring and improving a model's resistance to adversarial inputs. Existing robustness metrics and benchmarks (e.g., Cleverhans, Foolbox, Robust Vision Benchmark) help comparison but lack standardization and formal guarantees. |
| **Verifying Ethical Machine Reasoning** | ML systems increasingly act in ethically sensitive domains (e.g., autonomous driving). Verifying that such systems make ethically sound decisions remains largely unsolved—current model-checking approaches face scalability, annotation, and transparency challenges. |



---

## **Evolution of Software Testing for ML Systems**

Current software testing for ML systems is rapidly evolving to address the unique challenges of testing machine learning systems. Some of them are listed below.

### **Test Adequacy**
- Neuron coverage inspired by structural coverage metrics
- Input diversity metrics for comprehensive testing

### **Achieving Test Adequacy**
- Fuzzy testing adapted for high-dimensional input spaces
- Search-based testing for optimizing neuron coverage
- Mutation testing techniques for DNNs

### **Test Oracle Definition**
- Metamorphic testing for defining explicit oracles of black-box DNNs

### **Cost Reduction Strategies**
- Test suite minimization and prioritization while maintaining coverage to minimize high computational cost of DNNs

### **Domain-Specific Testing**
- Test suite reduction for CNN recognition models
- Test driving scenario generations for autonomous driving system testing
- Robustness testing based on metamorphic testing for LLMs


These evolving approaches and techniques will be explored in detail throughout the following sections of this course.

---
👉 **Move on to next section**: [Software structural coverages](../02_test_coverages/1_sw_coverages.md)