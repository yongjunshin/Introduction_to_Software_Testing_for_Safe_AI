# **Search-based Testing**
---

## **What is Search-based Testing?**

**Definition**: an approach that **frames test generation and test optimization as a *search problem***. Candidate test cases are treated as points in a search space, and **meta-heuristic** search algorithms are used to automatically find those that best satisfy a given objective (e.g., maximize coverage, reveal faults, or break an AI model).

**Meta-Heuristic**
- High-level, general-purpose search strategy that uses heuristic rules to explore large or complex spaces without exhaustive enumeration.
- Typically stochastic and problem-independent, aiming for good-enough solutions under limited time rather than guaranteed global optima (e.g., GA, PSO, simulated annealing).

**Core Concepts**:
- **Search space**: The set of all possible candidates that the search can explore (e.g., all possible inputs, configurations, or sequences of API calls).
- **Fitness (objective) function**: A numeric function that evaluates how “good” a candidate is with respect to the testing goal (e.g., branch coverage achieved, distance to a target branch).
- **Search algorithm**: The strategy that explores the search space using the fitness signal (e.g., genetic algorithms, hill-climbing, simulated annealing).
- **Stopping criteria**: When to stop the search (e.g., time budget, number of evaluations, convergence of fitness, or reaching a target coverage/failure).


**Search algorithms**:
| **Algorithm**           | **Main feature**                                   | **Example use in testing**                               |
|-------------------------|----------------------------------------------------|----------------------------------------------------------|
| Random search           | Uniformly samples the space; simple baseline      | Baseline fuzzing, quick sanity exploration               |
| Hill-climbing / Local search | Greedily improves candidates via small changes | Targeting specific branches or states                    |
| Simulated annealing     | Probabilistic acceptance of worse moves early on  | Escaping local optima when searching complex inputs      |
| **Genetic algorithm (GA)**  | Evolves a population via crossover and mutation   | Generating high-coverage tests, adversarial ML examples  |
| Particle swarm optimization (PSO) | Swarm of particles guided by global/local bests | Searching large configuration spaces for failures        |
| NSGA-II                 | Multi-objective evolutionary optimization         | Balancing multiple goals (e.g., coverage vs. execution cost) |



---

## **Genetic Algorithm**

**Definition**: a population-based meta-heuristic that evolves candidate solutions (here, test cases) over generations using selection, crossover, and mutation guided by a fitness function.


### **Core concepts**
- **Gene**: the smallest unit in a chromosome, typically encoding one decision variable such as an input parameter, flag, or step in a sequence.
- **Chromosome (individual)**: a full encoding of one candidate test (e.g., a complete input vector or action sequence) composed of multiple genes.
- **Population**: a set of chromosomes that are evaluated and evolved together in each generation.
- **Fitness**: a numeric score measuring how good a chromosome is with respect to the testing goal (e.g., coverage, distance to a target branch, oracles).
- **Selection**: strategy for choosing fitter individuals to act as parents for the next generation.
- **Crossover and mutation**: operators that recombine and randomly perturb chromosomes to explore new candidate tests.


### **Workflow**
1. **Initialization**: randomly (or heuristically) generate an initial population of encoded test cases.
2. **Evaluation**: execute each test, compute its fitness based on the testing objective, and record the scores.
3. **Reproduction**: select parents, apply crossover and mutation to create offspring, and form the next population.
4. **Termination**: repeat evaluation and reproduction until a stopping criterion is satisfied (e.g., time budget, coverage threshold, or max generations).



---


## **Applications for Traditional SW**



---

## **Applications for DL SW**



---

### **References**

---

👉 **Move on to exercises**: 
- [Search-based Testing Exercise](./exercises/search_based_testing_exercise.ipynb)
- [Search-based Testing Challenge](./exercises/search_based_testing_challenge.ipynb)

👉 **Move on to next section**: [Metamorphic Testing](../06_metamorphic_testing/1_metamorphic_testing.md)

---