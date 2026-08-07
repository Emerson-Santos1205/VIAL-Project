# VIAL

## Organizational Intelligence Infrastructure

**Version:** 1.0
**Status:** Foundation / Draft
**License:** Apache License 2.0

---

## 1. What is VIAL?

VIAL is an architectural foundation for building **persistent, distributed and governable organizational cognition**.

VIAL is designed around a fundamental distinction:

```text
Organization
      ≠
Execution Resource
```

An AI model, agent, human, service or deterministic process may execute organizational work.

But the Organization itself must be able to:

* persist;
* remember;
* reason;
* decide;
* validate;
* delegate;
* learn;
* recover;
* evolve.

The execution resources may change.

The Organization remains.

---

# 2. The Core Idea

Current intelligent systems often concentrate cognition inside temporary execution contexts.

VIAL proposes another model:

```text
                    ORGANIZATION
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
      GOALS           POLICIES          MEMORY
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                ORGANIZATIONAL STATE
                         │
                         ↓
                  SELECTIVE CONTEXT
                         │
                         ↓
                EXECUTION RESOURCE
                         │
                         ↓
                     PROPOSAL
                         │
                         ↓
                    VALIDATION
                         │
                         ↓
                     DECISION
                         │
                         ↓
                  STATE TRANSITION
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
          PROVENANCE             MEMORY
              │                     │
              └──────────┬──────────┘
                         ↓
                ORGANIZATIONAL LEARNING
```

The goal is not simply to create better agents.

The goal is to create organizations that can **use intelligence efficiently and continuously**.

---

# 3. Why VIAL Exists

As intelligent systems scale, several problems become increasingly important:

* repeated reasoning;
* repeated context transmission;
* fragmented memory;
* excessive agent coordination;
* duplicated decisions;
* lack of organizational continuity;
* weak provenance;
* high inference cost;
* vendor dependence;
* difficult auditing;
* poor recovery from execution failure.

VIAL addresses these problems by moving the architectural focus from the individual executor to the persistent Organization.

---

# 4. The VIAL Hypothesis

VIAL is based on the following hypothesis:

> **Intelligence becomes economically scalable when useful cognition can persist, be referenced, reused, governed and transferred independently of the temporary resources that execute it.**

This hypothesis is intended to be measurable and falsifiable.

VIAL does not assume that its architecture is universally superior.

It must demonstrate its value through evidence.

---

# 5. Fundamental Principles

VIAL is guided by several foundational principles.

### Persistent cognition

Organizational cognition should survive the replacement of individual execution resources.

### Selective context

Executors should receive the information they need rather than the complete organizational history.

### Cognitive reuse

Validated cognition should be reused rather than unnecessarily reconstructed.

### Explicit authority

Capability to perform an operation does not automatically imply authority to commit it.

### Evidence before truth

Model output is not automatically organizational truth.

### Auditability

Important organizational decisions and state transitions should remain reconstructable.

### Replaceability

Execution resources should be replaceable without destroying organizational continuity.

### Economic scalability

Efficiency must consider total organizational cost rather than tokens alone.

### Interoperability

Organizational semantics should remain independent of a particular vendor or implementation.

### Falsifiability

Architectural claims must be testable.

---

# 6. The Most Important Distinctions

VIAL intentionally separates several concepts that are frequently conflated.

```text
Organization
    ≠
Execution Resource
```

```text
State
    ≠
Context
```

```text
Capability
    ≠
Authority
```

```text
Information
    ≠
Evidence
```

```text
Model Output
    ≠
Organizational Decision
```

```text
Conversation
    ≠
Organizational Memory
```

These distinctions form part of the conceptual foundation of VIAL.

---

# 7. Efficiency Philosophy

VIAL does not define efficiency as simply using fewer tokens.

The objective is:

```text
Useful Organizational Value
────────────────────────────
Necessary Total Cost
```

Total cost may include:

* inference;
* tokens;
* communication;
* storage;
* synchronization;
* validation;
* infrastructure;
* operations;
* human intervention.

A system that saves tokens but produces worse organizational outcomes is not necessarily more efficient.

---

# 8. Cognitive Waste

VIAL identifies several forms of cognitive waste.

### Repeated context

Sending the same information repeatedly when a reference would be sufficient.

### Repeated reasoning

Reconstructing reasoning that has already been validated.

### Unnecessary execution

Invoking an intelligent resource when deterministic execution would be sufficient.

### Excessive coordination

Using multiple resources when one resource could complete the operation.

### Redundant validation

Repeating validation without meaningful additional value.

### Unnecessary synchronization

Creating coordination overhead without sufficient organizational benefit.

The objective is not to eliminate intelligence.

It is to eliminate **unnecessary intelligence expenditure**.

---

# 9. Organizational Cognition

VIAL treats cognition as an organizational capability.

An Organization may maintain:

```text
Goals
Policies
Roles
Capabilities
State
Knowledge
Memory
Evidence
Decisions
Provenance
```

Execution Resources interact with this organizational substrate.

---

# 10. Execution Resources

An Execution Resource may be:

```text
AI Model
AI Agent
Human
Function
Service
Database Operation
External System
Deterministic Process
```

VIAL does not require cognition to be implemented entirely by AI.

The important property is that execution remains subordinate to the Organization's state, policies and authority model.

---

# 11. Organizational Continuity

A VIAL Organization should survive changes in its execution infrastructure.

For example:

```text
Model A
   ↓
Replacement
   ↓
Model B
```

The Organization should preserve, where applicable:

```text
Identity
Goals
Policies
State
Knowledge
Decisions
Provenance
```

This creates continuity beyond individual sessions and models.

---

# 12. Selective Context

VIAL separates persistent organizational knowledge from temporary execution context.

```text
Large Organizational Knowledge
            ↓
       Retrieval
            ↓
      Context Selection
            ↓
     Minimal Relevant Context
            ↓
          Execution
```

The objective is to reduce:

* unnecessary tokens;
* latency;
* cognitive noise;
* communication overhead.

---

# 13. Reason Once, Reuse Many Times

One of the central VIAL ideas is:

```text
Reason
  ↓
Validate
  ↓
Persist
  ↓
Reference
  ↓
Reuse
```

The same organizational cognition should not need to be reconstructed simply because a different executor is performing the next operation.

---

# 14. Governance

VIAL separates:

```text
Capability
Authority
Validation
Decision
State Transition
```

A resource may recommend an action without having authority to commit it.

This enables powerful execution resources while maintaining organizational control.

---

# 15. Auditability

Important decisions should be reconstructable.

A mature VIAL implementation should be able to answer questions such as:

```text
What happened?

Why?

Based on what evidence?

Under which policy?

Which role was involved?

Which execution resource participated?

Which state changed?

When did the change occur?
```

Auditability is therefore part of the architecture rather than an afterthought.

---

# 16. Failure and Recovery

VIAL assumes execution failure.

Models fail.

Agents fail.

Services fail.

Networks fail.

Infrastructure fails.

The architectural question is:

> Can the Organization continue?

Therefore:

```text
Execution Failure
       ↓
Recovery
       ↓
Organizational Continuity
```

A resource failure should not automatically become an organizational failure.

---

# 17. Interoperability

VIAL is designed to remain independent of:

* AI provider;
* model family;
* programming language;
* database;
* cloud provider;
* infrastructure platform.

The semantic Organization should survive implementation changes.

---

# 18. What VIAL Is Not

VIAL is not fundamentally:

* another agent framework;
* another prompt framework;
* another model wrapper;
* another workflow engine;
* another orchestration library;
* a claim of artificial consciousness;
* a replacement for every AI architecture.

VIAL is an architectural foundation for **organizational cognition**.

---

# 19. Project Philosophy

VIAL follows several engineering principles:

```text
Evidence over authority
Measurement over assumption
Simplicity over unnecessary complexity
Persistence over repetition
Selective context over universal context
Reuse over reconstruction
Interoperability over lock-in
Governance over uncontrolled execution
Long-term integrity over short-term convenience
```

---

# 20. Foundation Documents

The conceptual foundation is organized into the following documents.

| Document        | Purpose                                        |
| --------------- | ---------------------------------------------- |
| FCP-002A        | Theory of Distributed Organizational Cognition |
| FCP-003         | Design Constraints                             |
| FCP-004         | Success Metrics                                |
| FCP-005         | Efficiency Model                               |
| FCP-006         | Core Concepts                                  |
| FCP-007         | Philosophical Principles                       |
| FCP-008         | VIAL Manifesto                                 |
| Code of Conduct | Community and contributor standards            |
| LICENSE         | Legal licensing terms                          |

---

# 21. TDOC

The **Theory of Distributed Organizational Cognition (TDOC)** provides the theoretical foundation for VIAL.

TDOC establishes the idea that organizational cognition can be distributed across multiple execution resources while remaining coherent through persistent organizational state.

The central relationship is:

```text
Organization
      ↓
Distributed Cognition
      ↓
Multiple Execution Resources
      ↓
Persistent Organizational State
```

---

# 22. Foundation Change Proposals

FCPs define the evolving conceptual foundation of VIAL.

They are intended to answer questions such as:

```text
Why does VIAL exist?

What problem is it solving?

What principles govern it?

What does success mean?

What should not be optimized?

What concepts must remain stable?
```

Technical protocol specifications will build upon this foundation.

---

# 23. ADRs

Architectural Decision Records preserve important decisions made during the development of VIAL.

ADRs should capture:

* context;
* problem;
* alternatives;
* decision;
* consequences;
* status.

The objective is to prevent architectural knowledge from being lost.

---

# 24. Repository Philosophy

The repository should maintain a clear distinction between:

```text
Foundation
    ↓
Theory
    ↓
Architecture
    ↓
Protocol
    ↓
Implementation
    ↓
Experiments
    ↓
Benchmarks
```

Experimental implementations should not silently become normative requirements.

---

# 25. Expected Evolution

VIAL is expected to evolve through evidence.

A simplified lifecycle is:

```text
Hypothesis
    ↓
Proposal
    ↓
Discussion
    ↓
ADR
    ↓
Specification
    ↓
Implementation
    ↓
Benchmark
    ↓
Evaluation
    ↓
Revision
```

This process allows VIAL to evolve without losing architectural history.

---

# 26. Performance Evaluation

VIAL should be evaluated against meaningful baselines.

Relevant dimensions may include:

```text
Quality
Efficiency
Latency
Token Consumption
Communication
Reliability
Auditability
Scalability
Operational Cost
```

No single metric should define success.

---

# 27. The Economic Objective

VIAL ultimately seeks:

```text
More Useful Organizational Capability
                  ↓
        Less Unnecessary Work
                  ↓
       Lower Total Cognitive Cost
```

The objective is not simply to build a more complex intelligent system.

It is to make organizational intelligence economically sustainable.

---

# 28. Long-Term Vision

VIAL aims to enable organizations capable of:

```text
Remembering
Understanding
Planning
Delegating
Executing
Validating
Learning
Adapting
Recovering
Explaining
```

while remaining independent of temporary execution resources.

---

# 29. The Central Invariant

The most important VIAL invariant is:

> **Execution Resources are replaceable; Organizational Cognition is persistent.**

This principle should guide future architecture and protocol decisions.

---

# 30. The Efficiency Invariant

A second fundamental invariant is:

> **Validated organizational information should be referenced and reused rather than unnecessarily reconstructed when safe to do so.**

---

# 31. The Governance Invariant

A third invariant is:

> **Capability to perform an operation does not automatically grant authority to commit its result to organizational State.**

---

# 32. The Audit Invariant

A fourth invariant is:

> **Significant organizational changes should remain attributable and reconstructable according to applicable governance requirements.**

---

# 33. The Interoperability Invariant

A fifth invariant is:

> **Semantic identity should remain independent from implementation technology.**

---

# 34. Why This Matters

The fundamental challenge is no longer simply:

> How do we make an AI model more capable?

The next challenge is:

> How do we make intelligence persistent, coordinated, reusable, governable and economically scalable?

VIAL is an attempt to provide an architectural answer.

---

# 35. Manifesto

We believe intelligence should not disappear when its executor disappears.

We believe organizational knowledge should not remain trapped inside conversations.

We believe validated cognition should be reusable.

We believe context should be selective.

We believe unnecessary reasoning is waste.

We believe capability must be separated from authority.

We believe important decisions must be attributable.

We believe organizations must survive execution failures.

We believe interoperability is essential.

We believe economic efficiency is an architectural requirement.

We believe complexity must earn its place.

We believe humans and machines can participate in organizational cognition.

We believe architectural claims must be measurable.

We believe VIAL must remain falsifiable.

Above all:

> **We believe the next generation of intelligent systems will be defined not only by how intelligent their individual agents are, but by how effectively intelligence can persist, coordinate, compound and scale as an Organization.**

---

# 36. Getting Started

VIAL is currently being developed from the Foundation upward.

The recommended order for understanding the project is:

```text
README
  ↓
Manifesto
  ↓
Philosophical Principles
  ↓
Core Concepts
  ↓
Efficiency Model
  ↓
Success Metrics
  ↓
TDOC
  ↓
Architecture
  ↓
Protocol
  ↓
RFC Hypotheses
  ↓
Prototype
  ↓
Benchmark
```

Minimal prototypes and reference implementations live under `prototype/`, hypothesis validation benchmarks under `benchmark/`.

---

# 37. Contributing

Contributions should follow the principles defined in:

```text
CONTRIBUTING.md
CODE_OF_CONDUCT.md
```

Architectural changes should be documented through the appropriate FCP and ADR mechanisms.

Contributors are encouraged to challenge assumptions with evidence.

---

# 38. Project Status

VIAL is currently in the **Foundation, Architecture and Early Validation phase**.

The conceptual model is established. Hypothesis-driven RFCs are now validated through minimal prototypes and reproducible benchmarks before any implementation is treated as normative.

Current priority:

```text
Foundation
    ↓
Architecture
    ↓
Protocol
    ↓
Hypothesis → RFC
    ↓
Minimal Prototype
    ↓
Benchmark
    ↓
Validation
    ↓
Revision
```

Validated hypotheses (each with a reproducible benchmark under `benchmark/`):

| RFC | Claim | Status |
|-----|-------|--------|
| RFC-007 | Selective context vs Full context | Hypothesis supported (token cost ratio 2.74x deterministic baseline; 17.85x with a real model) |
| RFC-008 | Cognitive reuse with stale invalidation | Hypothesis supported (cost ratio 3.03x, reuse rate 0.67) |
| RFC-009 | Atomicity, idempotency and recovery from failure | Hypothesis supported (23/23 interruptions resolved, 0 duplicates) |
| RFC-010 | Token-minimal policy diverges from total-cost-minimal; Deterministic First | Hypothesis supported (Deterministic First reproduces the cost optimum, ~26% below reason-everything) |

Workloads and harnesses are versioned for reproducibility; run artifacts are kept locally under `benchmark/<name>/results/` and excluded from version control. Results for RFC-007 were also validated with a real model (`opencode/deepseek-v4-flash-free`).

---

# 39. Final Principle

VIAL is not an attempt to create one perfect intelligent executor.

It is an attempt to create an environment in which many different forms of intelligence can contribute to a persistent Organization without forcing the Organization to repeatedly reconstruct itself.

```text
Temporary Intelligence
        ↓
Persistent Organization
        ↓
Reusable Cognition
        ↓
Compounding Capability
        ↓
Scalable Intelligence
```

> **Build organizations that can use intelligence intelligently.**

---

# End of README
