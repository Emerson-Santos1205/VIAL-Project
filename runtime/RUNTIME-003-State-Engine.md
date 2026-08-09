# RUNTIME-003 — VIAL State Engine

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Runtime Specification
Depends On:
- RUNTIME-001
- RUNTIME-002
- RFC-003

---

# 1. Abstract

This document defines the **VIAL State Engine**.

The State Engine is responsible for maintaining the authoritative operational State of a VIAL Organization.

It provides:

* State representation;
* State retrieval;
* State validation;
* State versioning;
* State transitions;
* concurrency protection;
* consistency;
* provenance;
* recovery.

The fundamental principle is:

> **State represents what the Organization currently accepts as operational reality.**

---

# 2. Purpose

The State Engine exists to ensure that the Organization does not operate from an undefined or contradictory representation of reality.

It provides the foundation for:

```text
Current Reality
      ↓
State
      ↓
Context
      ↓
Decision
      ↓
Execution
```

Without reliable State, the remaining Runtime components cannot reliably determine what is happening.

---

# 3. State Definition

VIAL State is the current structured representation of relevant organizational conditions.

State MAY include:

* operational conditions;
* resource status;
* active processes;
* equipment conditions;
* organizational variables;
* active objectives;
* current permissions;
* pending operations;
* environmental conditions.

State is not equivalent to Memory.

```text
State
=
What is currently believed to be true.
```

```text
Memory
=
What the Organization has retained from the past.
```

---

# 4. State Characteristics

A valid State SHOULD be:

* explicit;
* versioned;
* attributable;
* time-aware;
* scope-aware;
* internally consistent;
* auditable.

---

# 5. State Authority

The State Engine is the authoritative interface for organizational State.

Other Runtime components SHOULD NOT directly modify the underlying State storage.

```text
Runtime Component
       ↓
State Engine
       ↓
State Store
```

This creates a controlled boundary around organizational State.

---

# 6. State Scope

State SHOULD have an explicit scope.

Examples:

```text
Organization
Site
Department
Production Line
Machine
Process
Task
Resource
```

A State value MUST NOT automatically be assumed to apply outside its defined scope.

---

# 7. State Identity

A State representation SHOULD contain:

```text
State ID
Organization ID
Scope
Version
Timestamp
Source
Status
```

Example:

```text
State ID: ST-10052
Organization: ORG-001
Scope: Production-Line-03
Version: 482
Timestamp: 2026-08-07T10:00:00Z
```

---

# 8. State Versioning

Every meaningful State transition SHOULD produce a new version.

```text
v10
 ↓
v11
 ↓
v12
 ↓
v13
```

Previous versions SHOULD remain reconstructable according to organizational retention policies.

---

# 9. Immutable History

State history SHOULD be append-oriented.

The Runtime SHOULD avoid destructive modification of historical State.

Instead of:

```text
v10 overwritten
```

prefer:

```text
v10
 ↓
v11
```

This is fundamental to auditability.

---

# 10. State Snapshot

The Runtime MAY create a State Snapshot representing the State observed at a particular moment.

A Snapshot SHOULD contain:

```text
Snapshot ID
State Version
Timestamp
Scope
Relevant Values
Source References
```

---

# 11. Snapshot Usage

Snapshots are particularly important for:

* Decision reconstruction;
* auditing;
* debugging;
* replay;
* conflict detection;
* historical analysis.

---

# 12. State Freshness

State is time-sensitive.

The State Engine SHOULD expose sufficient information to determine whether a value is fresh enough for a particular operation.

Example:

```text
Temperature:
Value = 78°C
Observed = 2 seconds ago
```

is different from:

```text
Temperature:
Value = 78°C
Observed = 6 hours ago
```

---

# 13. Freshness Policy

Different operations MAY require different State freshness.

Example:

```text
Low Risk
→ minutes/hours may be acceptable

High Risk
→ seconds or immediate verification may be required
```

Freshness requirements SHOULD be defined by the domain or Decision policy.

---

# 14. State Provenance

Important State values SHOULD preserve provenance.

Possible provenance:

* sensor;
* human;
* Tool;
* database;
* external system;
* computed value;
* previous State;
* verified observation.

Example:

```text
Temperature = 78°C

Source:
Sensor-42

Observed:
10:03:22

Confidence:
Verified
```

---

# 15. State Confidence

Where appropriate, State MAY include confidence or validity metadata.

However, uncertainty MUST NOT be confused with authority.

A highly confident observation does not automatically authorize an action.

---

# 16. State Validation

Before accepting a State transition, the State Engine SHOULD validate:

* schema;
* type;
* required fields;
* constraints;
* scope;
* version;
* provenance;
* authorization.

---

# 17. State Invariants

An invariant is a condition that must remain true.

Example:

```text
Tank level ≥ 0
```

or:

```text
Valve position ∈ [0,100]
```

The State Engine SHOULD reject transitions that violate mandatory invariants.

---

# 18. Hard and Soft Constraints

VIAL MAY distinguish:

```text
Hard Constraint
→ MUST NOT be violated.
```

```text
Soft Constraint
→ SHOULD normally be respected.
```

The State Engine SHOULD identify the distinction explicitly where relevant.

---

# 19. State Transition

A State Transition represents an authorized change.

```text
Previous State
      ↓
Transition
      ↓
New State
```

A transition SHOULD contain:

```text
Transition ID
Previous Version
New Version
Trigger
Reason
Authority
Timestamp
Source
```

---

# 20. Transition Authorization

State modification SHOULD require a valid authority context.

A Runtime component must not modify critical organizational State merely because it has technical access to storage.

```text
Technical Access
≠
Organizational Authority
```

---

# 21. State Mutation

State mutation SHOULD occur only through controlled transitions.

Conceptually:

```text
Request
 ↓
Validate
 ↓
Authorize
 ↓
Transition
 ↓
Persist
 ↓
Publish Event
```

---

# 22. Atomicity

Where a transition contains multiple dependent State changes, the State Engine SHOULD preserve atomicity.

Example:

```text
Machine = RUNNING
Valve = OPEN
```

Changing the machine to STOPPED may require a coordinated change in valve State.

The transition should not leave an invalid intermediate State visible as the authoritative State.

---

# 23. Consistency

The State Engine SHOULD maintain organizational consistency according to the requirements of the domain.

Not every VIAL implementation requires global strong consistency.

The required consistency model SHOULD be explicitly defined.

---

# 24. Eventual Consistency

Distributed VIAL Organizations MAY use eventual consistency when:

* temporary divergence is acceptable;
* operations are independently safe;
* conflict resolution exists.

Eventual consistency MUST NOT be used blindly for safety-critical State.

---

# 25. Concurrency

Multiple cycles MAY attempt to modify the same State.

Example:

```text
Cycle A → v20 → v21

Cycle B → v20 → v21
```

The State Engine SHOULD detect that both transitions originated from v20.

---

# 26. Optimistic Concurrency

A recommended mechanism is version validation:

```text
Expected Version = 20
Current Version = 21
```

The transition SHOULD fail or require revalidation.

---

# 27. Conflict Resolution

A State conflict MAY result in:

```text
RETRY
REVALIDATE
MERGE
ESCALATE
REJECT
```

The correct behavior depends on domain semantics.

---

# 28. State Ownership

Each State element SHOULD have a defined authority or ownership boundary.

Example:

```text
Production Line State
→ Production System

Equipment State
→ Equipment Controller

Organizational Policy State
→ Governance System
```

Ownership reduces ambiguous mutation.

---

# 29. Derived State

Some State values MAY be calculated from other State.

Example:

```text
Total Production
=
Line A
+
Line B
+
Line C
```

Derived State SHOULD identify its source values or derivation logic.

---

# 30. Derived State Freshness

Derived State MUST NOT appear current if its underlying State is stale.

The Runtime SHOULD be able to determine when recalculation is required.

---

# 31. State vs Observation

An observation is not automatically State.

```text
Observation
    ↓
Validation
    ↓
State Update
```

Example:

```text
Sensor reports 85°C
```

does not necessarily mean:

```text
Organizational State = 85°C
```

until the observation is accepted according to the relevant rules.

---

# 32. State vs Event

An Event represents something that happened or was reported.

State represents the current accepted condition.

```text
Event:
Temperature changed to 85°C

State:
Temperature = 85°C
```

They are related but not identical.

---

# 33. State vs Memory

State:

```text
Machine is STOPPED.
```

Memory:

```text
The machine previously stopped because of excessive pressure.
```

The Runtime MUST preserve this distinction.

---

# 34. State and Context

Context is derived partly from State.

```text
State
+
Memory
+
Objective
+
Evidence
      ↓
Context
```

Context SHOULD NOT modify State directly.

---

# 35. State and Decision

A Decision SHOULD reference the State upon which it was based.

Example:

```text
Decision DEC-100

Based on:
State Version 482
```

This enables later evaluation of whether the Decision was based on valid information.

---

# 36. State Revalidation

Before high-impact Execution, the Runtime SHOULD verify whether the relevant State remains compatible with the Decision.

```text
Decision
 ↓
State Version 482

Current State
 ↓
Version 487
```

The Decision may require revalidation.

---

# 37. State Locking

Implementations MAY use locks where required.

However, long-running locks SHOULD be avoided when possible because they reduce scalability.

Prefer:

```text
Short Transaction
+
Version Validation
```

when appropriate.

---

# 38. State Transactions

A State Transaction SHOULD define:

```text
Transaction ID
Initial Version
Operations
Expected Result
Final Version
Status
```

---

# 39. State Event Generation

Meaningful State transitions SHOULD generate Events.

Example:

```text
STATE_CHANGED
```

with references to:

```text
Previous Version
New Version
Transition ID
```

This enables downstream systems to react.

---

# 40. State Subscriptions

Components MAY subscribe to State changes.

Examples:

```text
Monitoring
Analytics
Cognition
Tools
Other Runtime instances
```

Subscriptions SHOULD respect scope and authorization.

---

# 41. State Replication

Distributed implementations MAY replicate State.

Replication SHOULD preserve:

* version;
* provenance;
* scope;
* ordering;
* conflict information.

---

# 42. State Federation

Multiple VIAL Runtime instances MAY maintain partial State.

Example:

```text
                 Organization
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
     Site A         Site B         Site C
      State          State          State
```

Federated State MUST preserve organizational boundaries.

---

# 43. State Partitioning

State MAY be partitioned by:

* organization;
* location;
* domain;
* process;
* resource;
* tenant.

Partitioning SHOULD support scalability without creating ambiguous ownership.

---

# 44. Multi-Tenant State

If a Runtime serves multiple Organizations, State MUST remain isolated between Organizations.

```text
Organization A
≠
Organization B
```

Cross-organization access requires explicit authorization.

---

# 45. State Security

State may contain sensitive organizational information.

The State Engine SHOULD support:

* access control;
* authentication;
* authorization;
* encryption;
* classification;
* audit.

---

# 46. Least Privilege

Components SHOULD receive access only to the State they require.

Example:

```text
Temperature Controller
→ Temperature State

Not:
→ Entire Organization State
```

---

# 47. State Classification

Organizations MAY classify State as:

```text
PUBLIC
INTERNAL
RESTRICTED
CONFIDENTIAL
CRITICAL
```

Classification is domain-defined.

---

# 48. State Retention

State history SHOULD have explicit retention policies.

Retention may depend on:

* legal requirements;
* operational value;
* safety;
* audit requirements;
* storage cost.

---

# 49. State Compaction

Large State histories MAY be compacted.

However, compaction MUST preserve the ability to reconstruct required historical information.

Possible strategy:

```text
Full History
      ↓
Snapshots
+
Transition Log
```

---

# 50. State Recovery

After Runtime failure, the State Engine SHOULD be able to recover from a known valid State version.

Recovery MAY use:

* snapshots;
* transition logs;
* replicated State;
* transactional storage.

---

# 51. State Corruption

If State integrity is uncertain:

```text
STATE_UNTRUSTED
```

SHOULD be represented explicitly.

The Runtime SHOULD avoid making high-impact Decisions from untrusted State.

---

# 52. State Availability

State availability levels MAY include:

```text
AVAILABLE
STALE
PARTIAL
DEGRADED
UNAVAILABLE
UNTRUSTED
```

This allows Cognition and Decision layers to adapt safely.

---

# 53. Partial State

Distributed systems may temporarily have incomplete State.

The Runtime SHOULD identify missing information rather than silently treating it as false.

```text
Unknown
≠
False
```

This is a critical VIAL principle.

---

# 54. State Defaults

Default values SHOULD be used carefully.

A default MUST NOT hide an unknown operational condition.

Example:

```text
Unknown pressure
```

must not automatically become:

```text
Pressure = 0
```

unless the domain explicitly defines that behavior.

---

# 55. State Time

State SHOULD distinguish:

```text
Observed At
Recorded At
Effective At
```

These timestamps may differ.

---

# 56. Temporal State

Some State values are valid only during a specific period.

Example:

```text
Machine maintenance mode:
08:00 → 10:00
```

The State Engine SHOULD support temporal validity where necessary.

---

# 57. State Causality

Where possible, State transitions SHOULD identify their triggering cause.

```text
Transition
   ↓
Triggered By
   ↓
Event / Decision / Execution
```

---

# 58. State Provenance Chain

A critical State value MAY be traceable through:

```text
Observation
 ↓
Validation
 ↓
State Transition
 ↓
Current State
```

This provides strong auditability.

---

# 59. State Audit

Important transitions SHOULD preserve:

```text
Who / What
When
Why
Previous State
New State
Authority
Source
```

---

# 60. State Replay

A Runtime MAY support replaying historical State transitions.

Replay SHOULD be read-only unless explicitly authorized.

This enables:

* incident analysis;
* testing;
* simulation;
* auditing;
* debugging.

---

# 61. State Simulation

A copy or virtual State MAY be used for simulation.

```text
Current State
     ↓
Simulation
     ↓
Possible Future State
```

Simulation MUST NOT automatically alter production State.

---

# 62. State Prediction

Predicted State is not authoritative State.

```text
Predicted State
≠
Current State
```

Predictions SHOULD remain explicitly classified as predictions.

---

# 63. State Confidence and Prediction

A prediction MAY include:

```text
Value
Probability
Model
Timestamp
Validity Window
```

But it MUST remain distinguishable from observed State.

---

# 64. State Transition Lifecycle

This lifecycle applies to the State Transition record managed by the State Engine. It is distinct from the canonical Decision lifecycle defined by RFC-006.

```text
PROPOSED
   ↓
VALIDATED
   ↓
AUTHORIZED
   ↓
APPLIED
   ↓
CONFIRMED
```

Possible terminal states:

```text
REJECTED
FAILED
CANCELLED
CONFLICTED
```

---

# 65. State Engine Failure

If the State Engine is unavailable, the Runtime SHOULD determine whether the operation can safely continue.

For operations requiring current State:

```text
State unavailable
   ↓
DO NOT EXECUTE
```

For low-risk operations, alternative behavior MAY be permitted.

---

# 66. State Engine Efficiency

The State Engine SHOULD optimize:

* read latency;
* write latency;
* storage;
* replication;
* synchronization;
* serialization;
* network traffic.

However, optimization MUST NOT compromise required consistency or auditability.

---

# 67. State Access Economy

The Runtime SHOULD retrieve only the State required by the current cycle.

```text
Required State
≠
Entire State Database
```

This reduces:

* bandwidth;
* memory;
* processing;
* context size.

---

# 68. State Caching

State MAY be cached.

Cached State MUST expose enough metadata to determine:

```text
Age
Version
Scope
Validity
```

A cache MUST NOT silently appear to be authoritative current State when it is stale.

---

# 69. State Synchronization

When State is replicated, synchronization SHOULD preserve version and conflict information.

A synchronized value without provenance SHOULD NOT automatically be considered authoritative.

---

# 70. State API Boundary

A conceptual State Engine interface MAY provide:

```text
getState()
getSnapshot()
getVersion()
validateState()
proposeTransition()
validateTransition()
authorizeTransition()
applyTransition()
getHistory()
restoreSnapshot()
```

These names are conceptual and do not define a programming language.

---

# 71. State Contract

A conceptual State contract is:

```text
State {
    organization
    scope
    version
    timestamp
    values
    provenance
    validity
}
```

A conceptual Transition contract is:

```text
Transition {
    id
    cycle
    previous_version
    operations
    authority
    reason
    result
}
```

---

# 72. State Engine and Runtime

The relationship is:

```text
Runtime
   ↓
State Engine
   ↓
State
```

The Runtime orchestrates.

The State Engine governs State.

---

# 73. State Engine and Context Engine

```text
State Engine
      ↓
Current State
      ↓
Context Engine
      ↓
Context
```

The Context Engine consumes State.

It should not directly mutate it.

---

# 74. State Engine and Memory Engine

State and Memory cooperate but remain separate:

```text
State
=
Current condition

Memory
=
Retained knowledge
```

A Memory entry MAY reference State versions.

---

# 75. State Engine and Decision Engine

The Decision Engine uses State as evidence.

A Decision SHOULD identify the relevant State version when traceability matters.

---

# 76. State Engine and Execution Engine

Execution may produce State changes.

```text
Decision
 ↓
Execution
 ↓
Result
 ↓
State Transition
```

The Execution Engine should not bypass the State Engine when updating organizational State.

---

# 77. State Engine and Tools

Tools MAY observe or affect external systems.

However:

```text
Tool Result
      ↓
Validation
      ↓
State Engine
      ↓
Organizational State
```

External Tool output does not automatically become authoritative State.

---

# 78. State Engine and Audit

Every significant State transition SHOULD be auditable.

The audit trail SHOULD connect:

```text
Event
→ Decision
→ Execution
→ State Transition
```

---

# 79. State Engine and Efficiency

A reliable State Engine reduces repeated cognition.

If the Organization knows:

```text
Machine = STOPPED
```

the Runtime does not need to repeatedly infer this fact from multiple sources unless freshness requirements demand verification.

Thus:

```text
Reliable State
→ Less Cognition
→ Less Cost
→ Less Latency
```

---

# 80. State Engine and Organizational Cognition

The State Engine provides the temporal foundation for Distributed Organizational Cognition.

Different Resources may participate in cognition, but they must be able to reference a common organizational reality.

```text
Human
AI
Rule Engine
Sensor
Service
   ↓
Shared Organizational State
```

This is essential for organizational coherence.

---

# 81. Example — Industrial System

Consider a production line.

Current State:

```text
Line = RUNNING
Pump = ON
Valve = 72%
Pressure = 4.2 bar
Temperature = 76°C
```

A sensor reports:

```text
Pressure = 5.1 bar
```

The State Engine:

```text
Receive Observation
       ↓
Validate
       ↓
Update State
       ↓
Version +1
       ↓
Publish State Event
```

The new State becomes authoritative only after the transition is accepted.

---

# 82. Example — Concurrent Changes

Initial:

```text
State v100
```

Cycle A:

```text
v100 → v101
```

Cycle B attempts:

```text
v100 → v101
```

The State Engine detects that:

```text
Current = v101
Expected = v100
```

Cycle B must revalidate.

This prevents silent lost updates.

---

# 83. Example — Unknown Observation

Sensor becomes unavailable.

The Runtime should represent:

```text
Pressure = UNKNOWN
```

rather than:

```text
Pressure = 0
```

unless the domain explicitly defines zero as the correct fail-safe value.

---

# 84. Example — State-Based Efficiency

Suppose a Decision repeatedly requires:

```text
Current machine status
```

Without State:

```text
Query
→ Analyze
→ Infer
```

With reliable State:

```text
Read State
→ Continue
```

The second path is cheaper and faster.

---

# 85. Conformance Requirements

A State Engine conforming to RUNTIME-003 MUST:

1. maintain explicit State;
2. provide State versioning;
3. support controlled transitions;
4. distinguish State from Event;
5. distinguish State from Memory;
6. preserve required provenance;
7. protect against unsafe concurrent modification;
8. represent unknown State explicitly;
9. prevent unauthorized critical State mutation;
10. support reconstruction of required State history.

---

# 86. Recommended Capabilities

A mature State Engine SHOULD support:

* snapshots;
* optimistic concurrency;
* State subscriptions;
* distributed replication;
* State classification;
* temporal validity;
* simulation;
* replay;
* caching;
* conflict resolution;
* State health;
* State lineage.

---

# 87. Non-Goals

RUNTIME-003 does not define:

* a specific database;
* SQL schemas;
* REST endpoints;
* message brokers;
* programming language;
* cloud infrastructure;
* UI;
* specific industrial protocols.

Those belong to implementation-specific specifications.

---

# 88. Relationship With Future Runtime Documents

RUNTIME-003 establishes the State foundation for:

```text
RUNTIME-004
Context Engine

RUNTIME-005
Memory Engine

RUNTIME-006
Cognition / Decision components
```

The State Engine therefore precedes the higher-level engines.

---

# 89. Final Principles

### Principle 1 — State Is Explicit

> What the Organization believes to be true must be represented explicitly.

### Principle 2 — State Is Versioned

> Meaningful changes must be distinguishable over time.

### Principle 3 — State Is Governed

> Technical access does not equal authority to change organizational reality.

### Principle 4 — Unknown Is Not False

> Missing information must remain distinguishable from a known negative condition.

### Principle 5 — State Is Traceable

> Important State transitions must be reconstructable.

### Principle 6 — State Is Economical

> Reliable State reduces unnecessary cognition and repeated discovery.

### Principle 7 — State Is Organizational

> State belongs to the Organization, not to an individual AI, Tool or Resource.

---

# 90. Final Statement

The VIAL State Engine establishes the operational foundation upon which organizational cognition can occur.

Its purpose is not merely to store variables.

It maintains a **versioned, governed and auditable representation of organizational reality**.

The fundamental relationship is:

```text
OBSERVATION
     ↓
VALIDATION
     ↓
STATE
     ↓
VERSION
     ↓
CONTEXT
     ↓
DECISION
     ↓
EXECUTION
     ↓
STATE TRANSITION
     ↺
```

A VIAL Organization becomes progressively more efficient when it does not repeatedly rediscover what it already knows about its current condition.

> **Reliable State is the first economy of cognition.**

# End of RUNTIME-003

