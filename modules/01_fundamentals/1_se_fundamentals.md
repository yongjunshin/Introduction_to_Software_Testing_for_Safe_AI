# **Introduction to Software Engineering**

We'll provide an overview of software engineering concepts.

---

## **What is software engineering?**

* "Software engineering is a discipline that is concerned with all aspects of software production from the early stages of system specification to maintaining the system after it has gone into use." (Software engineering, Ian Sommerville)
* "The application of a systematic, disciplined, quantifiable approach to development, operation and maintenance of software" (IEEE Systems and Software Engineering Vocabulary)

---

## **Why it matters?**

### **Software engineering vs. Programming**

**Programming** is the act of writing code to solve a specific problem, while **software engineering** encompasses the entire process of creating, maintaining, and evolving software systems.

| Programming | Software Engineering |
|-------------|---------------------|
| Writing code | System design and architecture |
| Solving problems with code | Long-term activities from defining the problem to maintainability |
| Immediate results | Sustainable and reproducible development |
| A genius can do well | Make ordinary people (like us) do well |

### **Software crisis**

The **software crisis** refers to the difficulties in writing correct, understandable, and verifiable computer programs, despite advances in hardware and programming languages.

"... now we have gigantic computers, programming has become an equally gigantic problem." (Edsger Dijkstra, 1972)

**Key characteristics**:
- Cost overruns (50-100% budget excess)
- Schedule delays (months to years late)
- Quality issues (bugs and security vulnerabilities)
- Maintenance problems (legacy system difficulties)
- Fatal accidents (property damage and loss of life due to software failures)

**Known crisis cases**:
- Tesla Autopilot Accidents (2016-2023): Multiple fatalities due to autonomous driving software failures, regulatory investigations, \$2B+ in settlements and recalls
- Boeing 737 MAX (2018-2019): MCAS software bug, 346 deaths, \$18.7B cost, 20-month grounding
- Equifax Data Breach (2017): 147M people affected, \$1.4B settlements, Apache Struts vulnerability
- Healthcare.gov (2013): \$2.1B cost overrun, launch day crashes, poor load testing
- Knight Capital (2012): Trading algorithm bug, \$440M loss in 45 minutes, company nearly bankrupt
- Therac-25 (1985-1987): Radiation therapy machine software bug, 3 deaths, 3 serious injuries
- Ariane 5 Flight 501 (1996): Software overflow error, $370M rocket destroyed, 4 satellites lost


### **Technical debt**

**Technical debt** is the implied cost of additional rework caused by choosing an easy solution now instead of using a better approach that would take longer.

**Types of technical debt:**
- Code debt: Poor code quality, lack of documentation
- Design debt: Architectural shortcuts, tight coupling
- Testing debt: Insufficient test coverage, manual testing
- Documentation debt: Missing or outdated documentation
- Infrastructure debt: Outdated tools, dependencies, and environments

**Why technical debt accumulates:**
- Time pressure: "We'll fix it later" mentality
- Lack of expertise: Developers choosing familiar but suboptimal solutions
- Changing requirements: Quick fixes that don't align with long-term goals
- Resource constraints: Limited time and budget for proper implementation

**Impact of technical debt:**
- Reduced velocity: Development becomes slower over time
- Increased bugs: Poor code quality leads to more defects
- Higher maintenance costs: More time spent fixing issues than adding features
- Team morale: Developers frustrated with poor codebase quality
- Business risk: System failures and security vulnerabilities

---

## **Software lifecycle**

### **V model**

The V model emphasizes verification and validation at each stage, with testing activities corresponding to each development phase.

- **Requirement gathering**: Collect and document user needs and system requirements
- **System analysis**: Analyze requirements and define system architecture
- **Software design**: Create high-level and detailed design specifications
- **Module design**: Design individual components and their interfaces
- **Coding**: Implement the software according to design specifications
- **Unit testing**: Test individual modules against their specifications
- **Integration testing**: Test integrated components and interfaces
- **System testing**: Test the complete system against requirements
- **Acceptance testing**: Validate the system meets user needs

### **Software development process models**

- **Waterfall model**: Sequential phases (requirements → design → implementation → testing → maintenance) with minimal overlap
- **Spiral model**: Iterative approach combining design and prototyping with risk assessment and mitigation
- **Agile model**: Iterative development with short sprints, continuous collaboration, and adaptive planning 

---

## **Core activities in software engineering**

### **Requirements engineering**
- Gathering and analyzing user needs
- Functional and non-functional requirements
- Requirements validation and verification
- Stakeholder management

### **System design and architecture**
- High-level system design
- Architectural patterns and styles
- Component design and interfaces
- Verification of the design

### **Implementation and coding**
- Code development and programming
- Code review and quality assurance
- Version control and collaboration
- Documentation and commenting

### **Testing and quality assurance**
- Unit testing and component testing
- System testing and acceptance testing
- Performance testing and security testing
- Test automation and continuous integration

### **System integration and validation**
- Integration testing and system validation
- End-to-end testing and user acceptance testing
- Performance validation and load testing
- Security validation and compliance checking

### **Deployment and operations**
- Release management and deployment
- Monitoring and logging
- Maintenance and support
- Incident response and troubleshooting

### **Project management**
- Planning and scheduling
- Resource allocation and team coordination
- Risk management and mitigation
- Communication and stakeholder management

### **Beyond technology, understanding humans**
- Code Today, Deadline Tomorrow: Procrastination Among Software Developers (ICSE 2025)  
    - Shows how **last-minute coding often leads to more bugs and poor-quality code**—like students rushing work the night before a deadline.  
- Time Warp: The Gap Between Developers’ Ideal vs Actual Workweeks in an AI-Driven Era (ICSE 2025)  
    - Explains **how developers plan focused, productive days, but end up stuck in meetings and endless notifications** instead.  
- How Much Does AI Impact Development Speed? An Enterprise Randomized Controlled Trial (ICSE 2025)  
    - Finds that using **AI tools can slow teams down at first**, as developers learn to trust and adapt before real speed benefits appear.  
- Emoji in Software Development (ICSE 2020)  
    - Shows that a simple **🙂 or 😕 emoji in team chats can reveal a lot** about team mood and collaboration quality.  
- Social Debt: How Developer Stress Spreads in Teams (ICSE 2019)  
    - Finds that **stress is contagious**—when one developer burns out, the whole team feels the pressure.  
- The Effect of Time of Day and Day of Week on Commit Quality (ICSE 2017)  
    - Confirms that **Friday-night commits are risky**, with a higher chance of bugs just before the weekend.  

---

👉 **Move on to next section**: [Software Testing Fundamentals](../01_fundamentals/2_testing_fundamentals.md)

---




