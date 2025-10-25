# **Introduction to Software Testing**



We'll provide an overview of software testing concepts.

---

## **Static vs Dynamic Software Analysis**

Software analysis can be categorized into two main approaches based on when and how the analysis is performed:

| **Aspect** | **Static Analysis** | **Dynamic Analysis** |
|------------|-------------------|-------------------|
| **Definition** | Analysis performed **without executing** the software | Analysis performed **by executing** the software with real or simulated inputs |
| **When** | Performed on source code, bytecode, or compiled code | Performed during runtime with actual test cases |
| **Examples** | • Code reviews and inspections (e.g., type, linting, and style checking)<br>• Formal verification (e.g., model checking) | • **Software testing** (unit, integration, system testing)<br>• Runtime monitoring and profiling |
| **Advantages** | • Can analyze all possible execution paths<br>• No need for test data or execution environment<br>• Can find certain types of bugs that testing might miss | • Detects actual runtime behavior<br>• Can find performance and security issues<br>• Provides real-world validation |
| **Limitations** | • May produce false positives<br>• Cannot detect runtime issues<br>• Limited by analysis complexity | • Can only test executed code paths<br>• Requires test data and execution environment<br>• May miss issues in untested scenarios |

### **Software Testing as Dynamic Analysis**
**Software testing** is the most common and important form of **dynamic analysis**. It involves:
- Executing the software with carefully selected test inputs
- Observing the actual behavior and outputs
- Comparing actual results with expected results
- Identifying discrepancies that indicate faults

---

## **What is software testing?**

### **Definitions**

- The act of checking whether software **satisfies expectations** (wikipedia).
- Dynamic verification that a program provides **expected behaviors** on **a finite set of test cases**, suitably selected (IEEE Systems and Software Engineering Vocabulary)
- Software testing is the process of evaluating and verifying that a software product or application **functions correctly**, securely and efficiently according to its specific requirements. (IBM)

### **Purposes**

- Fault detection: Identify bugs, defects, and errors in the software
- Confidence building: Provide assurance that the software works as intended
- Performance validation: Verify software meets performance and efficiency requirements
- Regression prevention: Ensure new changes don't break existing functionality
- Compliance: Ensure software meets regulatory and industry standards
- User satisfaction: Validate that the software meets user needs and expectations

"Program testing can be used to show the presence of bugs, but never to show their absence." (Edsger Dijkstra)

### **Terminology**

- **Test input**: A set of input values and situations provided to the software under test to execute a specific test scenario
- **Test oracle**: A mechanism or procedure used to determine whether a test has passed or failed by comparing actual results with expected results (i.e., expected output)
- **Test case**: A pair of test input and test oracle
- **Test suite**: A collection of test cases gathered for the software under test

---

## **Main Questions of Software Testing**

### **Knowing When to Stop**

**Exhaustive Testing**

**Test Adequacy**

### **Knowing What is Right**

**Implicit vs Explicit Test Oracles**

**Test Oracle Problem**


---


## **Types of Software Testing**

- Test case 정의
- Testing level 종류
    - white-box vs black-box
    - 유닛
    - 시스템
    - 리그레션..
- Testing 행위 종류
- 테스트 생성
    - 테스트 관리, 진화
    - 테스트 자동화
    - 테스트 우선순위화
- Testing 기법 종류
    - random
    - guided random
    - mutation
    - search-based
    - metamorphic
    - model-based