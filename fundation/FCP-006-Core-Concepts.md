# VIAL Foundation Change Proposal

# FCP-006 — VIAL Core Concepts

**Version:** 1.0.0
**Status:** Draft
**Type:** Foundation Change Proposal
Depends On:
- FCP-002A
- FCP-003
- FCP-004
- FCP-005
**Related:** TDOC-00 through TDOC-09, ADR-0002, VCG-001

---

# 1. Abstract

FCP-006 defines the fundamental concepts required to understand, implement and evaluate VIAL.

The purpose is to establish a common vocabulary across:

* architecture;
* protocol;
* implementation;
* research;
* benchmarking;
* governance;
* documentation.

VIAL SHALL distinguish the organizational system from the execution resources that temporarily operate within it.

The central abstraction is:

```text
Organization
      ↓
Organizational Cognition
      ↓
State
      ↓
Context
      ↓
Execution
      ↓
Observation
      ↓
Decision
      ↓
Organizational Update
```

---

# 2. Organization

An Organization is the persistent logical entity whose goals, policies, knowledge, state and cognition are maintained over time.

An Organization is NOT synonymous with:

* an AI model;
* an agent;
* a process;
* a server;
* a container;
* a database.

Conceptually:

```text
Organization ≠ Agent
Organization ≠ Model
Organization ≠ Process
```

---

# 3. Organizational Cognition

Organizational Cognition is the persistent capability of an Organization to:

* maintain state;
* retain knowledge;
* interpret information;
* establish intent;
* make decisions;
* coordinate execution;
* learn from validated outcomes.

The cognition belongs to the organizational system rather than to a particular model instance.

---

# 4. Distributed Organizational Cognition

VIAL assumes that organizational cognition may be distributed across multiple resources.

```text
                 Organization
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Resource A     Resource B     Resource C
        │              │              │
        └──────────────┼──────────────┘
                       ↓
              Organizational State
```

No individual Execution Resource is required to contain the complete organizational cognition.

---

# 5. Execution Resource

An Execution Resource is a resource temporarily used to perform organizational work.

Examples include:

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

The execution resource is replaceable.

---

# 6. Role

A Role defines an organizational responsibility.

Example:

```text
Role:
    Quality Validator
```

A Role is distinct from the resource performing it.

```text
Role ≠ Execution Resource
```

This allows:

```text
Agent A
   ↓
Quality Validator

Agent A replaced

Agent B
   ↓
Quality Validator
```

without changing the organizational Role.

---

# 7. Capability

A Capability defines an operation an Organization can perform.

Examples:

```text
AnalyzeProductionData
ValidateQualityRecord
PlanMaintenance
EvaluateAlarm
ApproveTransition
```

Capabilities are semantic concepts.

Their implementation may vary.

---

# 8. Goal

A Goal represents a desired organizational outcome.

Examples:

```text
Maintain Production Availability
Reduce Operational Cost
Maintain Product Quality
Resolve Incident
```

Goals provide direction for organizational cognition.

---

# 9. Intent

Intent represents the Organization's current directional focus in relation to its Goals and current State.

Conceptually:

```text
Goals
+
Current State
+
Context
+
Policies
        ↓
      Intent
```

Intent may change over time without changing organizational identity.

---

# 10. Policy

A Policy defines constraints or rules governing organizational behavior.

Policies may define:

* authorization;
* restrictions;
* priorities;
* validation requirements;
* escalation;
* safety constraints.

Policy is a governance mechanism, not merely information.

---

# 11. State

State represents the authoritative current condition of the Organization.

Conceptually:

```text
Organizational State =
What the Organization currently considers authoritative
```

State may contain or reference:

* Goals;
* Intent;
* Policies;
* Roles;
* Capabilities;
* Knowledge;
* Evidence;
* Decisions;
* Metadata.

---

# 12. State Version

Every authoritative state transition SHOULD produce a distinguishable version.

```text
S100
 ↓
S101
 ↓
S102
```

Versioning allows:

* consistency;
* conflict detection;
* auditing;
* reconstruction.

---

# 13. Context

Context is the information selected and provided for a particular operation.

Context is a derived view.

```text
Organizational State
        ↓
Context Selection
        ↓
Execution Context
```

Therefore:

```text
Context ≠ State
```

---

# 14. Context Materialization

Context Materialization is the process of constructing the information required by an Execution Resource.

The objective is to provide:

```text
Necessary Information
+
Relevant Information
-
Unnecessary Information
```

This is one of the primary mechanisms for reducing token and communication waste.

---

# 15. Memory

Memory represents persistent organizational information retained for future use.

Memory may contain:

* validated knowledge;
* historical information;
* previous decisions;
* learned patterns;
* organizational experience.

Memory and State are related but distinct.

```text
Memory = Persistent Information
State = Current Authoritative Condition
```

---

# 16. Knowledge

Knowledge is information that has organizational utility.

Knowledge MAY originate from:

* Evidence;
* human input;
* previous Decisions;
* external information;
* validated observations.

Not all available information automatically becomes Knowledge.

---

# 17. Evidence

Evidence is information used to support:

* claims;
* interpretations;
* Decisions;
* State transitions.

Evidence SHOULD maintain provenance.

```text
Evidence
   ↓
Decision
   ↓
State Transition
```

---

# 18. Provenance

Provenance represents the lineage of organizational information.

Conceptually:

```text
Source
 ↓
Observation
 ↓
Evidence
 ↓
Interpretation
 ↓
Decision
 ↓
State Transition
```

Provenance is fundamental to auditability.

---

# 19. Decision

A Decision is an organizationally meaningful determination produced through the VIAL cognitive process.

A model output is not automatically a Decision.

```text
Model Output
      ↓
Evaluation
      ↓
Authorization / Validation
      ↓
Organizational Decision
```

---

# 20. Proposal

A Proposal represents a requested change to organizational state.

Conceptually:

```text
Current State
      ↓
Proposal
      ↓
Validation
      ↓
Commit
      ↓
New State
```

This separation prevents arbitrary Execution Resources from directly changing authoritative state.

---

# 21. State Transition

A State Transition represents an authoritative change in organizational State.

```text
S100
 ↓
Transition
 ↓
S101
```

A transition SHOULD be attributable and auditable.

---

# 22. Organizational Event

An Organizational Event represents something that occurred within the lifecycle of the Organization.

Examples:

```text
Proposal Created
Decision Approved
State Updated
Evidence Invalidated
Role Assigned
Policy Changed
```

Events may be used to reconstruct organizational history.

---

# 23. Audit Record

An Audit Record preserves information required to understand a significant organizational event or transition.

Auditability allows questions such as:

```text
What happened?
Why?
Based on what?
Under which Policy?
By which Role?
Using which Execution Resource?
What State changed?
```

---

# 24. Authority

Authority defines the right to perform a particular organizational operation.

Authority is independent from capability.

A resource may have the capability to perform an operation but lack the authority to commit its result.

```text
Capability ≠ Authority
```

---

# 25. Delegation

Delegation is the controlled transfer of authority from one organizational entity or Role to another.

Delegation SHALL preserve governance constraints.

Delegation does not necessarily transfer organizational ownership.

---

# 26. Validation

Validation determines whether a Proposal, Decision, Evidence item or State Transition satisfies applicable requirements.

Validation may be performed by:

```text
Deterministic Logic
AI Resource
Human
External System
Combination
```

---

# 27. Coordination

Coordination is the mechanism by which multiple Execution Resources contribute to an organizational operation.

VIAL seeks to minimize unnecessary coordination.

```text
Coordination Cost
=
Necessary Coordination
+
Avoidable Coordination
```

The second component is a primary optimization target.

---

# 28. Cognitive Work

Cognitive Work represents reasoning, interpretation, planning and decision-making performed for an organizational purpose.

VIAL distinguishes:

```text
Necessary Cognitive Work
```

from:

```text
Repeated Cognitive Work
```

The latter is a major source of inefficiency.

---

# 29. Cognitive Duplication

Cognitive Duplication occurs when equivalent organizational reasoning is unnecessarily repeated.

Example:

```text
Agent A
   ↓
Analyzes Data

Agent B
   ↓
Analyzes Same Data

Agent C
   ↓
Analyzes Same Data
```

VIAL seeks to replace unnecessary repetition with reusable organizational cognition.

---

# 30. Cognitive Reuse

Cognitive Reuse occurs when previously validated organizational information or reasoning is reused.

```text
Reason Once
    ↓
Validate
    ↓
Store / Reference
    ↓
Reuse
```

This is a central efficiency mechanism.

---

# 31. Organizational Knowledge Reuse

Knowledge Reuse is the ability to apply validated Knowledge across multiple operations without recreating it unnecessarily.

This supports:

* lower token consumption;
* lower latency;
* lower inference cost;
* consistency.

---

# 32. Context Reuse

Context Reuse occurs when previously materialized or validated context can be reused safely.

Reuse SHALL account for freshness and State version.

Stale context SHALL NOT be reused when it could produce incorrect behavior.

---

# 33. Reference

A Reference identifies an existing organizational artifact without duplicating its contents.

Examples:

```text
Knowledge ID
Evidence ID
Decision ID
State Version
Policy ID
Context ID
```

References are fundamental to VIAL's efficiency model.

---

# 34. Materialization

Materialization converts references and relevant organizational information into an execution-ready representation.

```text
References
    ↓
Resolution
    ↓
Selection
    ↓
Materialization
    ↓
Execution Context
```

Materialization SHOULD occur as late as practical.

---

# 35. Canonical Representation

A Canonical Representation defines the semantic meaning of an organizational concept independently from its implementation format.

The same concept may be represented using:

```text
JSON
Database
Binary Protocol
Graph
Memory Store
```

without changing its semantic identity.

---

# 36. Protocol

A Protocol defines how VIAL entities and operations are represented and exchanged.

The protocol SHALL be distinguished from:

```text
Organization
State
Execution
Implementation
```

The protocol exists to enable interoperable implementation.

---

# 37. Conformance

Conformance means that an implementation satisfies the normative requirements defined by VIAL specifications.

A system may be:

```text
Fast but Non-Conformant
```

or:

```text
Conformant but Poorly Optimized
```

Performance and conformance are separate properties.

---

# 38. Efficiency

VIAL Efficiency represents the amount of useful organizational capability produced relative to the resources consumed.

Conceptually:

```text
Efficiency =
Organizational Value
/
Total Necessary Cost
```

Total cost may include:

* tokens;
* inference;
* communication;
* storage;
* synchronization;
* validation;
* infrastructure.

---

# 39. Organizational Value

Organizational Value represents the useful outcome produced by the Organization.

It may include:

```text
Goal Achievement
Decision Quality
Task Completion
Constraint Compliance
Operational Improvement
```

Value is workload-dependent.

---

# 40. Cognitive Waste

Cognitive Waste is organizational effort that does not contribute sufficient additional value.

Examples:

```text
Repeated Context
Repeated Reasoning
Unnecessary Agent Calls
Duplicate Validation
Unnecessary Communication
Unnecessary Synchronization
```

Reducing Cognitive Waste is a primary VIAL objective.

---

# 41. Organizational Continuity

Organizational Continuity is the ability of the Organization to preserve its identity, Goals, State, Knowledge and Policies across changes in Execution Resources.

Example:

```text
Agent A
   ↓
Replacement
   ↓
Agent B

Organization continues
```

This is a fundamental property of VIAL.

---

# 42. Persistence

Persistence means that organizational information survives beyond the lifecycle of an individual execution.

```text
Execution Ends
      ↓
Organization Continues
```

Persistence enables long-running organizational cognition.

---

# 43. Temporal Separation

VIAL distinguishes:

```text
Persistent Organizational State
```

from:

```text
Temporary Execution Context
```

This separation allows the execution layer to remain lightweight while organizational cognition persists.

---

# 44. Organizational Boundary

The Organizational Boundary defines what belongs to an Organization.

Within the boundary:

* State;
* Goals;
* Policies;
* Knowledge;
* Roles;
* Decisions

are organizational resources.

External systems may interact with the Organization without becoming part of it.

---

# 45. Identity

Organizational Identity provides stable reference to the Organization across time.

Identity SHOULD remain independent of:

* model replacement;
* agent replacement;
* infrastructure migration;
* protocol implementation.

---

# 46. Lifecycle

A VIAL Organization may conceptually progress through:

```text
Create
  ↓
Initialize
  ↓
Operate
  ↓
Learn
  ↓
Adapt
  ↓
Recover
  ↓
Archive / Terminate
```

The exact lifecycle protocol is defined separately.

---

# 47. Failure

Failure is an execution condition that prevents an intended operation from completing correctly.

VIAL distinguishes:

```text
Execution Failure
Protocol Failure
Validation Failure
Policy Failure
State Conflict
Infrastructure Failure
```

Failure SHALL NOT automatically imply organizational corruption.

---

# 48. Recovery

Recovery is the process of restoring valid organizational operation after failure.

A successful recovery SHOULD preserve:

* Organizational Identity;
* authoritative State;
* Goals;
* Policies;
* critical Knowledge;
* auditability.

---

# 49. Simulation

Simulation is execution against a non-authoritative organizational representation.

```text
Production State
      ↓
Simulation
      ↓
Hypothetical Result
```

Simulation SHALL NOT silently modify authoritative organizational State.

---

# 50. Baseline

A Baseline is a reference implementation or architecture used to evaluate VIAL.

Examples may include:

```text
Single-Agent Architecture
Conventional Multi-Agent Architecture
Centralized Orchestration
VIAL Architecture
```

Baselines are necessary for empirical evaluation.

---

# 51. Benchmark

A Benchmark is a controlled workload used to measure VIAL properties.

Benchmarks SHALL evaluate multiple dimensions rather than relying exclusively on token or latency measurements.

---

# 52. Primary Architectural Relationship

The core VIAL model can be summarized as:

```text
                    ORGANIZATION
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
      GOALS          POLICIES          MEMORY
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                  ORGANIZATIONAL STATE
                         │
                         ↓
                     CONTEXT
                         │
                         ↓
                EXECUTION RESOURCE
                         │
                         ↓
                    OBSERVATION
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
                         ↓
                  AUDIT / PROVENANCE
```

---

# 53. Core Separation Principle

The most important conceptual separation in VIAL is:

```text
Organization
      ≠
Execution Resource
```

and:

```text
Organizational State
      ≠
Execution Context
```

and:

```text
Capability
      ≠
Authority
```

and:

```text
Information
      ≠
Evidence
```

and:

```text
Model Output
      ≠
Organizational Decision
```

These distinctions SHALL be preserved throughout subsequent specifications.

---

# 54. Efficiency Principle

The efficiency model can be summarized as:

```text
Persistent Cognition
        ↓
Selective Context
        ↓
Minimal Necessary Execution
        ↓
Reusable Results
        ↓
Reduced Repetition
```

The objective is not to eliminate cognition.

The objective is to avoid performing the same organizational cognition unnecessarily.

---

# 55. Core VIAL Invariant

A central invariant is:

> **Execution Resources are replaceable; Organizational Cognition is persistent.**

This invariant distinguishes VIAL from architectures where organizational intelligence is primarily located inside individual agents.

---

# 56. Core Efficiency Invariant

A second invariant is:

> **Information that has already been validated SHOULD be referenced and reused rather than repeatedly reconstructed when reuse is safe.**

---

# 57. Core Governance Invariant

A third invariant is:

> **Capability to perform an operation does not automatically imply authority to commit its result to organizational State.**

---

# 58. Core Audit Invariant

A fourth invariant is:

> **Significant organizational changes SHALL remain attributable and reconstructable according to applicable governance requirements.**

---

# 59. Core Interoperability Invariant

A fifth invariant is:

> **Semantic identity SHALL remain independent from implementation technology.**

Therefore VIAL concepts SHALL not depend on:

* a specific AI provider;
* a specific programming language;
* a specific database;
* a specific infrastructure provider.

---

# 60. Core Scalability Principle

VIAL SHOULD allow organizational complexity to increase without requiring every Execution Resource to receive the complete organizational state.

Conceptually:

```text
Organization Complexity ↑
          │
          ↓
Selective Context
          │
          ↓
Bounded Execution Context
```

where the workload permits.

---

# 61. Core Economic Principle

VIAL SHALL optimize total organizational cost rather than isolated infrastructure metrics.

```text
Total Cost =
Inference
+
Tokens
+
Communication
+
Storage
+
Synchronization
+
Validation
+
Operations
```

An optimization is valuable only when evaluated against the complete system.

---

# 62. Core Scientific Principle

VIAL architectural claims SHALL be falsifiable.

If benchmark evidence demonstrates that a proposed mechanism:

* does not improve efficiency;
* reduces quality;
* increases total cost;
* damages reliability;

the mechanism SHALL be reconsidered.

---

# 63. Relationship to Previous FCPs

The foundation now follows:

```text
FCP-002A
Theory of Distributed Organizational Cognition
        ↓
FCP-003
Design Constraints
        ↓
FCP-004
Success Metrics
        ↓
FCP-005
Efficiency Model
        ↓
FCP-006
Core Concepts
```

The progression establishes:

```text
Theory
   ↓
Constraints
   ↓
Measurement
   ↓
Optimization Model
   ↓
Common Vocabulary
```

---

# 64. Acceptance Criteria

FCP-006 may be accepted when:

* terminology is reviewed;
* concepts do not conflict with TDOC;
* concepts are compatible with FCP-003;
* metrics from FCP-004 can be applied to the concepts;
* efficiency principles from FCP-005 are preserved;
* the vocabulary is sufficient for subsequent protocol specifications.

---

# 65. Next Step

The next recommended document is:

```text
FCP-007 — VIAL Architectural Invariants
```

Its purpose will be to transform the concepts established here into explicit properties that implementations **must preserve**, regardless of technology or implementation strategy.

---

# End of FCP-006
