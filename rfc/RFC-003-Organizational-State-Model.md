# RFC-003 — Organizational State Model

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Standards Track
Depends On:
- RFC-002
- FCP-002A
- FCP-006
- FCP-007

---

# 1. Abstract

This document defines the **Organizational State Model** for VIAL.

Organizational State represents the persistent condition of an Organization at a specific point in its lifecycle.

The model establishes the semantic relationship between:

* Organization;
* State;
* State Version;
* State Transition;
* Event;
* Decision;
* Knowledge;
* Context;
* Provenance.

The objective is to provide a state model that is:

* persistent;
* auditable;
* versionable;
* recoverable;
* efficient;
* implementation-independent;
* suitable for distributed execution.

The protocol intentionally separates **persistent State** from temporary **Context** and from historical **Memory**.

---

# 2. Motivation

Distributed intelligent systems frequently mix:

* current state;
* conversation context;
* historical events;
* memory;
* execution results;
* temporary variables.

This creates ambiguity about what the Organization actually believes to be its current condition.

VIAL establishes a stricter distinction:

```text id="p6kq3d"
STATE
=
Current Organizational Condition
```

```text id="c0j1az"
MEMORY
=
Persistent Organizational Knowledge
```

```text id="w7nq4p"
CONTEXT
=
Temporary Execution View
```

```text id="b4f0xa"
EVENT
=
Occurrence Relevant to Organizational History
```

This separation is fundamental to organizational continuity.

---

# 3. Scope

RFC-003 defines:

* Organizational State;
* State structure;
* State identity;
* State versions;
* State transitions;
* state invariants;
* state history;
* event relationship;
* concurrency;
* consistency;
* snapshots;
* recovery;
* derived state;
* state references.

RFC-003 does not define in detail:

* memory architecture;
* knowledge representation;
* evidence structures;
* authorization mechanisms;
* transport;
* cryptography;
* database technology.

Those concerns belong to other RFCs.

---

# 4. Core Principle

The Organization is the owner of its persistent State.

execution resources may:

```text id="m7g5xq"
Observe State
Request State
Propose State Changes
Execute Authorized Operations
```

but they do not independently redefine organizational State.

The fundamental relationship is:

```text id="2f8m1p"
Organization
      ↓
Persistent State
      ↓
Authorized Transition
      ↓
New State
```

---

# 5. Definition of Organizational State

Organizational State is the set of persistent facts and values required to represent the current operational condition of an Organization.

Conceptually:

```text id="f8qv2k"
State(t) =
{
    Identity,
    Goals,
    Policies,
    Roles,
    Capabilities,
    Operational Facts,
    Active Decisions,
    Relevant Knowledge References,
    Constraints,
    Status
}
```

The exact structure is implementation-dependent.

The semantic meaning MUST remain consistent.

---

# 6. State Is Not Everything the Organization Knows

An Organization may possess a large amount of information.

Only a portion of that information represents its current State.

For example:

```text id="xk4b7v"
Historical Decision
       ↓
Memory / History
```

while:

```text id="2q4x8z"
Current Operating Mode
       ↓
Organizational State
```

State therefore represents **current organizational condition**, not the entire organizational knowledge base.

---

# 7. State and Memory

State and Memory are related but distinct.

```text id="s6h2pm"
STATE
Current condition

MEMORY
Persistent knowledge and experience
```

A memory artifact MAY influence State.

A State Transition MAY create new Memory.

Neither concept should be silently substituted for the other.

---

# 8. State and Context

Context is a temporary representation constructed for execution.

```text id="j8z1qs"
Persistent State
       ↓
Context Selection
       ↓
Execution Context
```

Context MAY contain information derived from State.

Context MUST NOT automatically become persistent State.

When a Context is material to a consequential evaluation or execution, RFC-003 consumes the canonical Context model defined by RFC-002 and RFC-004:

```text
CREATED
   ↓
VALID
   ↓
FROZEN
   ↓
CONSUMED
   ↓
ARCHIVED
```

After FROZEN, the normative content of the Context MUST NOT change.

---

# 9. State Identity

Each Organization MUST have a stable organizational identity.

A State representation MUST be associated with the Organization to which it belongs.

Conceptually:

```text id="3j2q0w"
Organization ID
      +
State Version
      +
State
```

The identity mechanism itself is implementation-dependent.

---

# 10. State Version

Each meaningful State representation SHOULD have a version identifier.

Conceptually:

```text id="h0m7rw"
State v10
   ↓
Transition
   ↓
State v11
```

The version allows the Organization to distinguish different persistent states.

Version identifiers SHOULD support:

* ordering;
* comparison;
* concurrency detection;
* recovery;
* auditability.

---

# 11. State Transition

A State Transition represents an authorized change from one organizational State to another.

Conceptually:

```text id="k1p8my"
State(n)
   +
Authorized Transition
   ↓
State(n+1)
```

A transition SHOULD identify:

* previous state;
* resulting state;
* triggering operation or decision;
* provenance;
* relevant timestamp;
* transition status.

---

# 12. State Transition Is the Fundamental Mutation

VIAL SHOULD treat significant state changes as transitions rather than unrestricted mutation.

Instead of:

```text id="c9m2y6"
state.value = new_value
```

the semantic model is:

```text id="3v8d2a"
State
   ↓
Transition
   ↓
New State
```

This creates a traceable organizational history.

---

# 13. Transition Sources

A State Transition MAY originate from:

* authorized Decision;
* deterministic operation;
* external event;
* validated observation;
* administrative action;
* recovery procedure.

When a State Transition is Decision-driven, RFC-003 consumes the canonical model defined by RFC-002 and RFC-006: Decision determines the intended change, Authorization determines whether the operation may proceed, and Approval MAY be required as an explicit additional step.

The transition MUST respect applicable authority and policy.

---

# 14. Transition Authorization

A significant State Transition SHOULD be authorized before commitment.

Decision-driven transitions SHOULD conceptually follow:

```text id="4h6m2v"
Proposal
   ↓
Decision
   ↓
Authorization
   ↓
Approval (when required)
   ↓
Invocation
   ↓
Execution
   ↓
State Transition
```

Deterministic transitions that do not require a Decision still require the applicable Authorization model.

The exact authority model is defined in RFC-006.

---

# 15. State Invariants

An invariant is a condition that MUST remain true across valid State Transitions.

Examples:

```text id="q7k2sz"
Safety limits
Required organizational fields
Policy constraints
Resource limits
Identity consistency
Operational constraints
```

A State Transition that violates a mandatory invariant MUST be rejected unless an explicitly authorized exception mechanism exists.

---

# 16. State Validation

Before committing a significant State Transition, the implementation SHOULD validate:

```text id="5z8n2r"
Identity
Authorization
Policy
Current State
Transition Validity
Required Evidence
Invariant Compliance
```

The validation mechanism may be:

* deterministic;
* rule-based;
* model-assisted;
* human;
* hybrid.

---

# 17. Atomic Transition

A State Transition SHOULD be atomic from the perspective of the Organization.

The Organization SHOULD NOT expose an intermediate state that represents an incomplete transition.

Conceptually:

```text id="9v1h3b"
State A
   ↓
[Transition]
   ↓
State B
```

not:

```text id="7r2k6m"
State A
   ↓
Partial State
   ↓
Partial State
   ↓
State B
```

---

# 18. Idempotency

State-changing operations SHOULD support idempotency where practical.

A repeated request should not unintentionally create multiple equivalent transitions.

```text id="0j4s6n"
Request X
   ↓
State A → State B

Retry X
   ↓
No unintended duplicate mutation
```

The implementation MAY use:

* operation identifiers;
* transition identifiers;
* deduplication records;
* transactional mechanisms.

---

# 19. State History

An Organization SHOULD be able to reconstruct relevant historical State.

Conceptually:

```text id="2m8x4q"
State v1
   ↓
State v2
   ↓
State v3
   ↓
State v4
```

Historical state may be represented through:

* full snapshots;
* event history;
* transition logs;
* hybrid mechanisms.

RFC-003 does not mandate one storage strategy.

---

# 20. Snapshot

A Snapshot represents a materialized representation of State at a specific point.

Snapshots MAY be used to improve:

* recovery;
* read performance;
* startup time;
* historical inspection.

Snapshots SHOULD retain sufficient version information to establish their position in organizational history.

---

# 21. Event

An Event represents an occurrence relevant to the Organization.

Examples:

```text id="5d7h9p"
Sensor Reading
External Notification
Completed Operation
Human Input
System Failure
Policy Change
Decision
```

An Event does not necessarily imply a State Transition.

```text id="k4z7qp"
Event
  ≠
State Transition
```

An Event may instead trigger evaluation.

---

# 22. Event-Driven Transition

A common pattern is:

```text id="5u8x1w"
Event
  ↓
Interpretation
  ↓
Validation
  ↓
Decision
  ↓
State Transition
```

The Event is the occurrence.

The Transition is the resulting organizational mutation.

---

# 23. Derived State

Some State may be derived from other persistent information.

For example:

```text id="z7h3p1"
Current Production Status
=
Derived from
Events + Decisions + Operational Data
```

Derived State SHOULD be distinguishable from authoritative persisted State.

An implementation MUST define which source is authoritative when reconstruction is possible.

---

# 24. Authoritative State

Authoritative State is the State recognized by the Organization as the current source of truth for the relevant domain.

There MUST NOT be multiple silently competing authoritative versions of the same State.

If conflicting authoritative candidates exist, the Organization SHOULD enter a detectable conflict condition.

---

# 25. State Conflict

A State Conflict occurs when competing transitions or representations cannot both be accepted as valid.

Example:

```text id="3j9c6q"
State v20
   ├──→ Transition A → State v21A
   │
   └──→ Transition B → State v21B
```

If both modify the same critical state, the Organization MUST detect the conflict.

Resolution MAY require:

* ordering;
* merge;
* rejection;
* revalidation;
* human intervention.

---

# 26. Concurrency

VIAL permits concurrent execution.

However, concurrency MUST NOT silently corrupt organizational State.

Implementations SHOULD detect:

* stale State;
* conflicting transitions;
* duplicate transitions;
* lost updates;
* invalid ordering.

---

# 27. Optimistic Concurrency

An implementation MAY use optimistic concurrency.

Conceptually:

```text id="a7w1q4"
Read State v30
      ↓
Prepare Transition
      ↓
Commit only if State = v30
```

If the Organization is already at v31:

```text id="3f9m8k"
Commit rejected
      ↓
Re-evaluate
```

This avoids unnecessary locking in many distributed scenarios.

---

# 28. Pessimistic Coordination

Some critical operations may require stronger coordination.

An implementation MAY use:

* locks;
* leases;
* serialized execution;
* transactional boundaries.

The choice should depend on the cost and consequences of concurrent mutation.

VIAL does not require a universal concurrency mechanism.

---

# 29. State Freshness

A State representation used for a transition SHOULD have a known freshness relationship with the authoritative State.

An execution resource SHOULD NOT commit a significant mutation based silently on obsolete State.

Conceptually:

```text id="q2r5n7"
State v40
   ↓
Execution
   ↓
Current State = v43
   ↓
Revalidation Required
```

---

# 30. State References

execution resources SHOULD normally receive a reference to relevant State rather than a complete organizational snapshot.

Example:

```text id="8s5m2d"
Organization
+
State Reference
+
Relevant State Fields
+
Task
```

This supports VIAL's selective-context principle.

---

# 31. State Projection

A State Projection is a limited view of State constructed for a particular operation.

Example:

```text id="q4n8s1"
Full Organizational State
          ↓
     State Projection
          ↓
   Production Executor
```

A projection SHOULD contain only information required by the authorized operation.

---

# 32. Projection Is Not State

A State Projection is not authoritative State.

```text id="z6f3v9"
Authoritative State
        ≠
State Projection
```

An execution resource MUST NOT assume that modifying its local projection automatically modifies organizational State.

---

# 33. State Transition Result

A committed transition SHOULD produce an identifiable result.

Conceptually:

```text id="k8d2x5"
Transition ID
Previous State
New State
Decision Reference
Provenance Reference
Timestamp
```

The exact representation belongs to the implementation layer.

---

# 34. State Transition Failure

If a transition cannot be safely committed, the Organization SHOULD preserve the previous valid State.

Conceptually:

```text id="h3v7m2"
State A
   ↓
Attempt Transition
   ↓
Failure
   ↓
State A remains authoritative
```

Partial mutation MUST be avoided.

---

# 35. Recovery

A VIAL implementation SHOULD support recovery from:

* process failure;
* network failure;
* execution resource failure;
* storage failure;
* interrupted transition;
* inconsistent replica;
* invalidated state.

Recovery mechanisms MAY use:

```text id="p7x4q1"
Snapshots
+
Transition History
+
Event History
+
Validation
```

---

# 36. State Replication

An Organization MAY replicate State across infrastructure.

Replication MUST NOT create ambiguous authority.

A system SHOULD clearly distinguish:

```text id="1h6s9k"
Authoritative State
```

from:

```text id="q5w3z8"
Replica
```

Replication consistency requirements depend on the organizational domain.

---

# 37. Consistency Model

VIAL does not mandate a single global consistency model.

Different organizational domains may require different guarantees.

Examples include:

```text id="n4y7p2"
Strong Consistency
Eventual Consistency
Causal Consistency
Domain-Specific Consistency
```

The chosen model MUST be explicit when it affects organizational correctness.

---

# 38. State Partitioning

Large Organizations MAY partition State into domains.

For example:

```text id="z9k4m1"
Organization
 ├── Production State
 ├── Maintenance State
 ├── Inventory State
 ├── Financial State
 └── Personnel State
```

Partitioning SHOULD reduce unnecessary synchronization.

However, cross-domain invariants MUST be explicitly handled.

---

# 39. State Locality

State SHOULD remain close to the operations that require it when doing so improves:

* latency;
* availability;
* cost;
* scalability.

However, locality MUST NOT compromise required organizational consistency.

---

# 40. State Compression

Implementations MAY compress or encode State efficiently.

Compression MUST NOT alter semantic meaning.

VIAL encourages efficient representation because persistent State may be accessed frequently.

---

# 41. State and Token Efficiency

State architecture directly affects cognitive cost.

A poorly structured State can cause:

```text id="f7w3c9"
Large State
   ↓
Large Context
   ↓
High Token Cost
```

A well-structured State enables:

```text id="m9q2v5"
Persistent State
   ↓
Selective Projection
   ↓
Small Context
   ↓
Lower Cognitive Cost
```

Therefore State modeling is part of VIAL's efficiency architecture.

---

# 42. State and Organizational Memory

A State Transition MAY produce a memory artifact.

Example:

```text id="y5p7x2"
State Transition
      ↓
Important Decision
      ↓
Persistent Knowledge
```

However, not every State Transition should become long-term memory.

Memory admission is governed by RFC-005.

---

# 43. State and Evidence

Significant transitions SHOULD reference relevant Evidence where required.

Conceptually:

```text id="r4v8n1"
Evidence
   ↓
Decision
   ↓
State Transition
```

This creates a traceable chain from observation to organizational change.

Detailed evidence semantics belong to RFC-007.

---

# 44. State and Authority

State mutation MUST respect organizational authority.

```text id="j8q3w6"
Capability
      ≠
Authority
      ≠
State Ownership
```

A resource may possess the capability to perform a technical operation without being authorized to commit organizational State.

---

# 45. State Lifecycle

A State artifact may follow:

```text id="s6v9m3"
CREATED
   ↓
ACTIVE
   ↓
UPDATED
   ↓
SUPERSEDED
   ↓
ARCHIVED
```

The exact lifecycle depends on the State domain.

---

# 46. State Validity

A State representation MAY become:

```text id="c7n2x4"
VALID
STALE
INVALID
SUPERSEDED
CONFLICTING
UNKNOWN
```

The status SHOULD be machine-detectable when relevant to safe execution.

---

# 47. State Expiration

Some State has a natural expiration.

Examples:

```text id="m3r8q7"
Temporary Operating Mode
Short-Term Constraint
External Availability
Temporary Authorization
```

Expiration SHOULD be represented explicitly rather than relying on implicit assumptions.

---

# 48. State Mutation Cost

Implementations SHOULD avoid creating State Transitions for information that does not materially change organizational State.

For example:

```text id="v8q2m4"
Repeated identical observation
```

should not necessarily produce:

```text
New Organizational State Version
```

unless organizational policy requires it.

This prevents unnecessary state churn.

---

# 49. No Unnecessary Version Inflation

Version numbers SHOULD represent meaningful state changes.

Implementations SHOULD avoid generating excessive versions merely because:

* an executor accessed State;
* context was generated;
* a temporary calculation occurred;
* an unchanged value was rewritten.

This improves storage, auditability and performance.

---

# 50. State Normalization

Implementations SHOULD avoid storing the same authoritative fact redundantly in multiple independent State locations unless required.

Redundant state increases the risk of:

* inconsistency;
* synchronization;
* storage;
* cognitive ambiguity.

---

# 51. State References Over Duplication

When an authoritative object already exists, State SHOULD reference it instead of duplicating the complete object when appropriate.

This follows the VIAL principle:

> **Reference persistent cognition; do not repeatedly replicate it.**

---

# 52. State Transition Contract

Conceptually, a transition can be represented as:

```text id="p1w7r3"
Transition {
    organization
    previous_state
    operation
    decision
    authority
    resulting_state
    provenance
}
```

This is a semantic model.

It is not a mandatory wire format.

---

# 53. Minimal State Contract

At minimum, a VIAL implementation needs to establish:

```text id="q8m2v6"
Organization Identity
Current State
State Version
Transition Mechanism
Authority Boundary
State Validity
```

Everything beyond this should be justified by requirements.

---

# 54. State Efficiency Principle

The State Model SHOULD optimize for:

```text id="t4x9n2"
Minimal Persistent Representation
+
Fast Relevant Retrieval
+
Reliable Transition
+
Traceable History
```

The objective is not maximum state detail.

The objective is sufficient state for organizational continuity and correct decisions.

---

# 55. State as Organizational Memory Boundary

The State Model creates a boundary between:

```text id="f2m7k5"
What is true now
```

and:

```text id="r9x3w1"
What the Organization knows
```

This distinction allows VIAL to maintain large organizational memory without forcing the complete memory into every execution context.

---

# 56. Example — Industrial Organization

Consider a production organization.

Current State:

```text id="d6q8w2"
Production Line: ACTIVE
Pump: RUNNING
Pressure: 8.2 bar
Temperature: 72°C
Operating Mode: AUTO
```

A sensor generates an Observation.

An execution resource evaluates it.

A Proposal is generated:

```text id="y3n7p4"
Reduce pump speed by 10%.
```

The Proposal is validated.

A Decision is created.

The Organization authorizes execution of the proposed transition.

The State Transition becomes:

```text id="b8m2x6"
Pump: RUNNING
        ↓
Pump: REDUCED_SPEED
```

The resulting State receives a new version.

The transition references:

* Decision;
* Evidence;
* execution resource;
* timestamp;
* previous State.

The Organization can therefore reconstruct why its current State exists.

---

# 57. Example — Concurrent Operations

Suppose:

```text id="n5q8r2"
State v100
```

Two resources read it simultaneously.

Resource A proposes:

```text
State v101A
```

Resource B proposes:

```text
State v101B
```

If the operations conflict, the Organization MUST detect that both were based on State v100.

Possible result:

```text id="j7x4m9"
A commits
B rejected as stale
```

B may then retrieve the new State and re-evaluate.

---

# 58. Example — Recovery

Suppose an execution resource fails after a State Transition request but before confirmation.

The Organization can use:

```text id="p3k7w5"
Transition ID
+
Previous State
+
Transition Record
+
Current State
```

to determine whether the transition:

* committed;
* failed;
* remains uncertain.

The system SHOULD avoid executing the operation twice merely because confirmation was lost.

---

# 59. State Model and Large-Scale Deployment

For large Organizations, State MAY be distributed.

However:

```text id="k6m2q9"
Distributed Storage
      ≠
Distributed Authority
```

The system must preserve clear ownership and consistency semantics.

Large-scale implementations SHOULD favor:

* partitioning;
* selective retrieval;
* state projections;
* event-driven updates;
* efficient snapshots;
* explicit consistency boundaries.

---

# 60. Conformance Requirements

A VIAL implementation conforming to RFC-003 MUST:

1. represent persistent Organizational State;
2. associate State with an Organization;
3. distinguish State from temporary Context;
4. support meaningful State versioning;
5. represent significant State Transitions;
6. enforce applicable authorization boundaries;
7. prevent silent conflicting state mutations;
8. provide a mechanism for recovery;
9. distinguish authoritative State from derived or projected State;
10. maintain sufficient information to reconstruct significant transitions.

---

# 61. Recommended Requirements

A conforming implementation SHOULD additionally support:

* optimistic concurrency;
* idempotent state-changing operations;
* snapshots;
* state projections;
* conflict detection;
* state freshness;
* transition provenance;
* efficient state references;
* selective retrieval;
* state expiration.

---

# 62. Non-Goals

RFC-003 does not attempt to define:

* a universal database schema;
* a universal distributed database;
* a mandatory event-sourcing architecture;
* a mandatory CQRS architecture;
* a specific serialization format;
* a specific cloud platform;
* a specific consistency algorithm;
* a specific consensus protocol.

These remain implementation choices unless future RFCs explicitly standardize them.

---

# 63. Design Invariants

The following principles should remain stable.

### State Invariant

> Organizational State represents the current persistent condition of the Organization.

### Transition Invariant

> Significant state changes occur through controlled State Transitions.

### Authority Invariant

> Only authorized operations may commit significant organizational State changes.

### Continuity Invariant

> execution resource failure must not inherently destroy organizational State.

### Consistency Invariant

> Conflicting State mutations must be detectable.

### Efficiency Invariant

> State should be selectively projected rather than unnecessarily replicated into execution contexts.

### Provenance Invariant

> Significant State Transitions should remain reconstructable.

---

# 64. Relationship With RFC-002

RFC-002 defines how Organizational Cognition operates.

RFC-003 defines what persistent organizational State means.

The relationship is:

```text id="v2x7m4"
RFC-002
Organizational Cognition
        ↓
Produces / Evaluates
        ↓
RFC-003
Organizational State
        ↓
Provides Persistent Basis
        ↓
RFC-002
Future Cognition
```

This creates the fundamental organizational loop.

---

# 65. Relationship With Future RFCs

RFC-003 provides the state foundation for:

```text id="s9m3q1"
RFC-004 — Context & Cognitive Efficiency
        ↓
State Projection

RFC-005 — Memory & Knowledge
        ↓
State / Memory Relationship

RFC-006 — Decision & Authority
        ↓
Authorized State Transition

RFC-007 — Selective Context
        ↓
Relevant State Selection

RFC-008 — Cognitive Reuse
        ↓
State-Based Reuse

RFC-009 — Failure & Recovery
        ↓
State Recovery

RFC-010 — Economic Cost
        ↓
State Cost Accounting

RFC-011 — Security & Governance (planned)
        ↓
State Protection
```

---

# 66. Final Model

The VIAL State Model can be summarized as:

```text id="n8q4w2"
                    ORGANIZATION
                         │
                         ↓
                AUTHORITATIVE STATE
                         │
                         ↓
                  STATE VERSION
                         │
                         ↓
                  AUTHORIZED CHANGE
                         │
                         ↓
                 STATE TRANSITION
                         │
                         ↓
                 NEW STATE VERSION
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
         PROVENANCE              MEMORY
              │                     │
              └──────────┬──────────┘
                         ↓
                 FUTURE CONTEXT
                         ↓
                  FUTURE COGNITION
```

---

# 67. Final Principle

VIAL does not treat State as a passive data structure.

State is the persistent representation of the Organization's current condition.

Therefore:

```text id="c4m8x2"
Context is temporary.
Memory is persistent knowledge.
Events are occurrences.
Decisions determine change.
Authorization grants permission for change.
Transitions modify State.
State preserves organizational continuity.
```

The central principle is:

> **An Organization should never need to reconstruct its current condition merely because the resource executing its next operation has changed.**

# End of RFC-003
