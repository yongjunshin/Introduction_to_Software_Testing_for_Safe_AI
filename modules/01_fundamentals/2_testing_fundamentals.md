# **Introduction to Software Testing**



We'll learn about an overview of software testing concepts.

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

#### **Exhaustive Testing**

**Definition**: Testing all possible inputs and execution paths of a program

Examples:
- Simple function: `add(a, b)` where a and b are real numbers
- String processing: Testing all possible strings of any length
- User interface: Testing all possible user interactions and sequences
- Database queries: Testing all possible query combinations and data states 


Why it's impossible:
- **Infinite input space**: Most programs accept infinite possible inputs
- **Exponential explosion**: Number of test cases grows exponentially with program complexity
- **Resource constraints**: Limited time, budget, and computational resources
- **Combinatorial explosion**: Testing all combinations of inputs becomes unmanageable

Since exhaustive testing is impossible, we need practical criteria to determine when our testing is "good enough" - this is where test adequacy comes in.

#### **Test Adequacy**

**Definition**: Test adequacy measures how well a test suite covers the software under test, providing criteria for determining when testing is "good enough."

**Example adequacy metrics:**

| **Metric** | **Definition** |
|------------|----------------|
| **Statement Coverage** | Percentage of code statements executed |
| **Branch Coverage** | Percentage of decision branches taken |
| **Path Coverage** | Percentage of execution paths tested |
| **Function Coverage** | Percentage of functions called |
| **Condition Coverage** | Percentage of boolean conditions tested |

Good test adequacy metrics for a software under test can be useful tools that brings us to knowing when to stop testing.


### **Knowing What is Right**

#### **Test Oracle Problem**

**Definition:**
The difficulty of determining the correct expected output for test cases, especially in complex, non-deterministic, or evolving systems.


**Examples in Autonomous Driving Domain:**

| **Software Module** | **Test Oracle Problem Example** |
|---------------------|------------------------|
| **Object Detection** | What's the "correct" detection of a pedestrian in foggy conditions? |
| **Path Planning** | What's the "correct" route in complex traffic scenarios? |
| **Behavior Prediction** | What's the "correct" prediction of other vehicles' behavior? |
| **Emergency Response** | What's the "correct" action in emergency situations? |


#### **Implicit vs Explicit Test Oracles**

| **Aspect** | **Implicit Oracles** | **Explicit Oracles** |
|------------|---------------------|---------------------|
| **Definition** | Things that should not happen regardless of program semantics | Things that should happen due to specific requirements/business logic |
| **Scope** | General correctness properties | Domain-specific correctness criteria |
| **Examples** | • Crash<br>• Null pointer dereference<br>• Infinite loop<br>• Memory leaks<br>• Stack overflow<br>• Vehicle crash | • Assertions<br>• Expected return values<br>• Specific output formats<br>• Business rule compliance<br>• Performance requirements<br>• Safe steering expectation for collision avoidance |
| **Advantages** | • Easy to define<br>• Universal applicability<br>• Clear failure criteria | • Precise validation<br>• Domain-specific accuracy<br>• Business logic verification |
| **Limitations** | • May miss domain-specific bugs<br>• Limited to general properties | • Requires detailed specifications<br>• Domain knowledge needed |

Test oracles are usually derived from the understanding of the requirements of the software under test.
Automated generation of test oracles, especially for explicit oracles, is a challenge (e.g., how do we verify that the test oracle generator's behavior matches the software under test's expected behavior?)


---


## **Types of Software Testing**

### **Testing Based on Software Visibility**

| **Type** | **Definition** |
|----------|---------------|
| **Black-box Testing** | Testing without knowledge of internal structure, focusing on inputs and outputs |
| **White-box Testing** | Testing with full knowledge of internal structure, code, and implementation details |
| **Gray-box Testing** | Testing with partial knowledge of internal structure and implementation |

### **Testing Based on Development Phase**

| **Type** | **Definition** |
|----------|---------------|
| **Unit Testing** | Testing individual components or modules in isolation |
| **Integration Testing** | Testing interactions between integrated components and subsystems |
| **System Testing** | Testing the complete integrated system against requirements |
| **Acceptance Testing** | Testing to verify the system meets user needs and business requirements |
| **Regression Testing** | Testing to ensure new changes don't break existing functionality |

### **Testing Techniques**

| **Type** | **Definition** |
|---------------|---------------|
| **Random Testing** | Generating test cases using random inputs to explore software behavior |
| **Model-based Testing** | Generating tests from formal models of system behavior and specifications |
| **Mutation Testing** | Evaluating test quality by introducing faults and checking if tests detect them |
| **Search-based Testing** | Using optimization algorithms to automatically generate effective test cases |
| **Metamorphic Testing** | Testing relationships between multiple inputs and outputs without explicit oracles


---

👉 **Move on to next section**: [AI Testing Overview](../01_fundamentals/3_ai_testing_overview.md)

---