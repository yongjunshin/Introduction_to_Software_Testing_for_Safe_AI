# **Structural Coverages**

We'll learn basic structural coverages of software testing.

## **What is Structural Test Coverage?**

**Definition**: A metric that quantifies the extent to which the source code of a program has been executed during testing. 

Structural coverage provides insight into which parts of the code have actually been tested and which remain unexplored. 
This approach is crucial for identifying untested code segments, reducing the risk of hidden bugs, and ensuring that critical execution paths are validated. By measuring coverage, developers can make informed decisions about **test suite adequacy** and prioritize additional test cases for poorly covered areas.

Consider the following function as an example under test:

```python
def function_under_test(A, B, C):
    X = 0
    
    if A > 5 and B < 10:
        X = 1
    else:
        X = 2
    
    if C == 1:
        Y = 1
    else:
        Y = 2
    
    return X + Y
```

Five major structural coverages will be introduced with the example.

---

## **Statement Coverage**

---

## **Branch (Decision) Coverage**

---

## **Condition Coverage**

---

## **Path Coverage**

---

## **MC/DC Coverage**

---

## **Why is Structural Coverage Important?**

Structural coverage provides a rigorous, measurable approach to ensure software is sufficiently tested. 

More intuitively, testing based on structural coverage is necessary to sell software products in regulated markets. Safety-critical industries often mandate specific coverage levels. 

For example, ISO 26262 (automotive functional safety standard) requires 100% MC/DC coverage for the highest safety integrity levels, making coverage metrics essential for regulatory compliance and commercial viability.

---
👉 **Move on to next section**: [Neuron Coverages](2_neuron_coverages.md)