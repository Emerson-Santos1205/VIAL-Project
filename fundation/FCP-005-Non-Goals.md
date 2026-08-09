# FCP-005 — VIAL Efficiency Model
Version: 1.0.0
Status: Draft
Depends On: None

## 13. Non-Goals

FCP-005 deliberately does **not** attempt to:

### 13.1 Minimize Token Consumption at Any Cost

VIAL does not define minimum token consumption as an independent optimization objective.

A reduction in tokens is not considered an improvement if it causes:

* lower decision quality;
* loss of required context;
* weaker governance;
* reduced auditability;
* increased failure rate.

```text
Lower Tokens
≠
Better VIAL
```

---

### 13.2 Minimize the Number of Agents

VIAL does not attempt to create the smallest possible number of agents.

The number of execution resources is an implementation decision.

The objective is:

```text
Optimal Organizational Execution
```

rather than:

```text
Minimum Agent Count
```

---

### 13.3 Replace All AI Reasoning with Deterministic Logic

VIAL does not seek to eliminate AI reasoning.

Deterministic execution SHOULD be preferred when it is sufficient and economically advantageous, but reasoning remains necessary for problems that require:

* interpretation;
* planning;
* ambiguity resolution;
* complex decision-making;
* adaptation.

---

### 13.4 Maximize Model Intelligence

FCP-005 does not define a requirement to use the most capable or largest available model.

The objective is:

```text
Required Capability
/
Minimum Necessary Resource Cost
```

A smaller model may be preferable when it provides sufficient quality.

---

### 13.5 Optimize for a Specific AI Provider

VIAL does not optimize its architecture for a specific:

* model provider;
* model family;
* API;
* inference platform.

The efficiency model SHALL remain provider-independent.

---

### 13.6 Define the VIAL Wire Protocol

FCP-005 does not define:

* network transport;
* API endpoints;
* serialization format;
* message envelopes;
* authentication protocol;
* communication infrastructure.

Those concerns belong to the protocol specifications.

---

### 13.7 Define a Specific Database Architecture

FCP-005 does not require:

* SQL;
* NoSQL;
* graph databases;
* vector databases;
* event stores;
* distributed databases.

The efficiency model SHALL remain independent of storage technology.

---

### 13.8 Define a Universal Benchmark

FCP-005 does not define the complete VIAL benchmark suite.

FCP-004 establishes the success dimensions.

Future benchmark specifications SHALL define:

* workloads;
* datasets;
* procedures;
* baselines;
* scoring;
* statistical methodology.

---

### 13.9 Guarantee Universal Performance Improvements

VIAL does not claim that the architecture will outperform every alternative in every workload.

Efficiency is workload-dependent.

The architecture SHALL be evaluated empirically.

---

### 13.10 Sacrifice Correctness for Performance

FCP-005 explicitly rejects:

```text
Performance
>
Correctness
```

The optimization hierarchy established by FCP-004 remains applicable.

---

### 13.11 Sacrifice Governance for Efficiency

VIAL does not permit optimization mechanisms to bypass required:

* authorization;
* validation;
* policy enforcement;
* audit requirements.

Efficiency SHALL operate within organizational governance.

---

### 13.12 Treat Context Elimination as the Objective

VIAL does not seek to minimize context indiscriminately.

The objective is:

```text
Necessary Context
+
Relevant Context
-
Unnecessary Context
```

Removing information that is necessary for correct reasoning is not an optimization.

---

### 13.13 Treat Caching as Automatically Beneficial

FCP-005 does not assume that caching always improves performance.

Caching may introduce:

* stale information;
* invalid decisions;
* synchronization overhead;
* invalidation complexity.

Cache effectiveness SHALL be measured rather than assumed.

---

### 13.14 Eliminate Organizational Memory

VIAL does not seek to minimize persistent organizational memory simply to reduce storage.

Memory exists to preserve useful organizational knowledge.

The optimization objective is:

```text
Useful Memory
+
Efficient Retrieval
-
Unnecessary Duplication
```

---

### 13.15 Centralize All Cognition

VIAL does not require a central intelligence or central orchestrator.

The architecture SHALL support distributed organizational cognition as established by TDOC.

---

### 13.16 Fully Decentralize All Operations

Conversely, VIAL does not require complete decentralization.

Centralized components MAY be used when they provide measurable benefits without violating the organizational architecture.

---

### 13.17 Define Organizational Governance

FCP-005 does not establish:

* authority models;
* delegation rules;
* organizational hierarchy;
* approval policies;
* human authority;
* escalation rules.

These belong to the governance layer.

---

### 13.18 Define Security Architecture

FCP-005 does not prescribe:

* encryption algorithms;
* identity providers;
* key management;
* network security;
* authentication mechanisms.

Security constraints remain external architectural requirements.

---

### 13.19 Define Legal Compliance

FCP-005 does not establish compliance with any specific:

* jurisdiction;
* regulation;
* industry standard;
* privacy law;
* certification.

Compliance SHALL be addressed by the applicable deployment and governance environment.

---

### 13.20 Optimize Only for Average Performance

VIAL does not define average performance as sufficient.

Efficiency evaluation SHOULD consider:

```text
P50
P95
P99
Failure Cases
Worst-Case Behavior
```

where appropriate.

A system with an excellent average but unacceptable tail behavior may not be suitable for enterprise workloads.

---

### 13.21 Hide Complexity

VIAL does not consider hiding complexity an efficiency improvement.

If an optimization moves complexity from:

```text
Execution
```

to:

```text
Protocol
Governance
Operations
```

the total system cost SHALL be evaluated.

---

### 13.22 Optimize Individual Components in Isolation

FCP-005 does not define component-level optimization as sufficient.

The relevant unit of evaluation is:

```text
Complete Organizational Operation
```

An optimization that improves one component while degrading the overall system SHALL not automatically be accepted.

---

### 13.23 Create a Closed Ecosystem

VIAL does not seek to lock organizations into a proprietary execution environment.

The architecture should remain interoperable across:

* implementations;
* models;
* infrastructure;
* execution resources.

---

### 13.24 Replace Human Organizations

VIAL does not attempt to define a mechanism for eliminating human organizational participation.

Humans remain valid organizational actors and execution resources where appropriate.

---

### 13.25 Define the Final VIAL Architecture

FCP-005 is an efficiency model, not the final implementation architecture.

It establishes principles and measurable relationships that future protocol and implementation specifications SHALL use.

---

## 13.26 Summary

FCP-005 optimizes for:

```text
Useful Organizational Capability
        +
Quality
        +
Reliability
        +
Governance
        +
Auditability
        +
Scalability
        ↓
Minimum Necessary Total Cost
```

It explicitly rejects optimization based solely on:

```text
Minimum Tokens
Minimum Agents
Minimum Latency
Minimum Storage
Minimum Model Size
Minimum Messages
```

when these objectives compromise organizational capability.

---

## 13.27 Governing Principle

> **VIAL does not seek to make cognition smaller. VIAL seeks to eliminate cognition that does not need to happen again.**

This distinction is fundamental to the efficiency strategy of VIAL.

# End of Non-Goals Section
