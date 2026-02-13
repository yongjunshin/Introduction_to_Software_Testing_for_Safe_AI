# **Random and Fuzz Testing**



---

## **What is Random & Fuzz Testing?**

**Random Testing**: A testing technique that generates random inputs from the entire input space to test software behavior and discover unexpected failures.

**Fuzz Testing (Fuzzing)**: A specialized form of random testing that generates *malformed, unexpected, or invalid* inputs to find security vulnerabilities, crashes, and edge-case failures in software systems.

**Key Distinction:**
- **Random testing** uses random inputs from the valid input space to explore diverse behaviors
- **Fuzz testing** deliberately generates invalid, malformed, or boundary-breaking inputs to stress-test the system's robustness and security

Fuzz testing is based on random testing but specialized for finding vulnerabilities by intentionally violating input specifications, boundaries, and assumptions. While random testing explores normal behavior variations, fuzzing actively tries to break the system by feeding it unexpected or malicious inputs.

**Random is Strong!**

Despite its simplicity, random and fuzz testing have proven remarkably effective at finding critical bugs in production software. The success of fuzzing lies in its ability to explore unexpected edge cases that human testers rarely consider.
- **Google OSS-Fuzz (2016-present)**: Discovered over 10,000 vulnerabilities in 1,000+ open-source projects, including critical security flaws in Chrome, OpenSSL, and FFmpeg
- **Microsoft Security Risk Detection**: Found thousands of previously unknown bugs in Windows and Office through automated fuzzing
- **Heartbleed Bug (OpenSSL)**: Could have been discovered earlier through systematic fuzzing, leading to widespread adoption of fuzzing in cryptographic libraries
- **AFL (American Fuzzy Lop)**: Discovered hundreds of zero-day vulnerabilities in widely-used software including Adobe Flash, PHP, and various Linux utilities
- **Miller et al. Study (1990)**: Simple random input testing crashed 25-33% of UNIX utilities, revealing fundamental robustness issues that had gone undetected for years

Because of its effectiveness, randomness has become a fundamental component throughout software testing—not just in this dedicated discipline, but also in mutation testing, search-based testing, metamorphic testing, and many other approaches covered in later sections. 
In this section, we focus on the core concepts and foundational works of random and fuzz testing.

---

## **Random and Fuzz Testing for Traditional Software**

### **Types of Fuzzing**
Classification of fuzzing techniques based on how much knowledge about the program is used (black-box, white-box, grey-box).

### **Input Generation Strategies**
Different approaches to generating test inputs including mutation-based, generation-based, and grammar-based fuzzing.

### **Coverage-Guided Fuzzing**
How fuzzing tools use code coverage feedback to guide input generation toward unexplored program paths.

### **Popular Fuzzing Tools**
Overview of widely-used fuzzing frameworks like AFL, LibFuzzer, and their applications in finding real-world vulnerabilities.

### **Success Stories**
Notable vulnerabilities and bugs discovered through fuzzing in production software systems.

---

## **Random and Fuzz Testing for DL Software**

### **Challenges in Testing DL Systems**
Why traditional fuzzing techniques don't directly apply to neural networks and what makes DL testing unique.

### **Input Mutation for DL**
Techniques for generating test inputs by perturbing images, text, or other data while maintaining semantic validity.

### **Adversarial Examples**
How small, imperceptible perturbations can cause neural networks to make incorrect predictions.

### **Coverage-Guided DL Fuzzing**
Using neuron coverage and other DL-specific coverage metrics to guide test input generation.

### **DL Fuzzing Tools and Frameworks**
Overview of tools like DeepXplore, TensorFuzz, and DeepTest for automated DL system testing.

---

### **References**

- [1] Zhu, Xiaogang, et al. "Fuzzing: a survey for roadmap." ACM Computing Surveys (CSUR) 54.11s (2022): 1-36.
- [2] Mallissery, Sanoop, and Yu-Sung Wu. "Demystify the fuzzing methods: A comprehensive survey." ACM Computing Surveys (CSUR) 56.3 (2023): 1-38.
- [3] Guo, Jianmin, et al. "Dlfuzz: Differential fuzzing testing of deep learning systems." Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering (FSE). 2018.
- [4] Xie, Xiaofei, et al. "Deephunter: a coverage-guided fuzz testing framework for deep neural networks." Proceedings of the 28th ACM SIGSOFT international symposium on software testing and analysis (ISSTA). 2019.
- [5] Odena, Augustus, et al. "Tensorfuzz: Debugging neural networks with coverage-guided fuzzing." International conference on machine learning (PMLR), 2019.
- [6] Gao, Xiang, et al. "Fuzz testing based data augmentation to improve robustness of deep neural networks." Proceedings of the acm/ieee 42nd international conference on software engineering (ICSE). 2020.

---

👉 **Move on to exercise**: [Fuzz Testing Exercise](./exercises/fuzz_testing_exercise.ipynb)
1. [Traditional Coverage-Guided Fuzzing](./exercises/01_traditional_coverage_guided_fuzzing.ipynb)
2. [MNIST Random & Mutation Testing](./exercises/02_mnist_random_mutation_testing.ipynb)
3. [MNIST Coverage-Guided Fuzzing](./exercises/03_mnist_coverage_guided_fuzzing.ipynb)
4. [MNIST FGSM Adversarial Testing](./exercises/04_mnist_fgsm_adversarial_testing.ipynb)

👉 **Move on to next section**: [Mutation Testing](../04_mutation_testing/1_mutation_testing.md)


---