# SDK-004 — VIAL Context API

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** SDK Specification
Depends On:
- SDK-001
- SDK-002
- SDK-003
- FCP-002A
- RFC-002
- RFC-003

---

# 1. Abstract

This document defines the **VIAL Context API**.

Context represents the set of organizational information selected and assembled as relevant to a specific objective, operation or cognitive process.

The fundamental principle is:

> **Context is not the entire Organization. Context is the relevant portion of the Organization assembled for a purpose.**

---

# 2. Purpose

The Context API provides a standardized interface for:

* creating Context;
* retrieving Context;
* validating Context;
* updating Context;
* refreshing Context;
* freezing Context;
* versioning Context;
* inspecting Context provenance;
* determining Context validity;
* preparing Context for Cognition and Decision processes.

---

# 3. Context Position in VIAL

The conceptual relationship is:

```text
Organization
      │
      ├── Resources
      ├── State
      ├── Memory
      ├── Policies
      └── Events
             │
             ▼
          CONTEXT
             │
             ▼
         COGNITION
             │
             ▼
          DECISION
```

Context acts as the bridge between organizational information and organizational reasoning.

---

# 4. Context Definition

A Context is a purpose-oriented representation of relevant organizational information.

It may contain:

```text
State
Memory
Events
Policies
Constraints
Objectives
Resources
Evidence
Authority
Capabilities
```

Not every Context contains every category.

---

# 5. Context Is Purpose-Driven

Every meaningful Context SHOULD have an objective.

Example:

```text
Objective:
Determine whether Pump-01 should reduce operating speed.
```

The objective influences what information is relevant.

---

# 6. Context Identity

Every persistent or traceable Context MUST have a unique identifier.

Conceptually:

```text
ContextID
```

Example:

```text
CTX-2026-000184
```

---

# 7. Context Organization

Every Context MUST belong to an Organization.

Conceptually:

```text
Context {
    context_id
    organization_id
}
```

A Context MUST NOT silently cross organizational boundaries.

---

# 8. Context Scope

A Context SHOULD define its scope.

Possible scopes include:

```text
Organization
Plant
Department
Production Line
Process
Equipment
Resource
Operation
Decision
```

---

# 9. Context API

The Context API SHOULD provide:

```text
context.create()
context.get()
context.update()
context.validate()
context.refresh()
context.freeze()
context.version()
context.diff()
context.delete()
```

The exact implementation may vary by language.

---

# 10. Context Creation

Conceptual operation:

```text
context.create({
    organization_id,
    objective,
    scope
})
```

The Runtime is responsible for assembling the resulting Context according to organizational rules.

---

# 11. Context Inputs

Context may be assembled from:

```text
Organization
Resources
State
Memory
Events
Policies
External Information
```

All inputs MUST be subject to authorization.

---

# 12. Context Assembly

The conceptual process is:

```text
Objective
    +
Scope
    +
Relevant State
    +
Relevant Memory
    +
Policies
    +
Events
    +
Constraints
       ↓
    CONTEXT
```

---

# 13. Context Selection

The Runtime SHOULD select information based on relevance to the objective.

The Context API SHOULD NOT require applications to retrieve the entire Organization and construct Context manually.

---

# 14. Minimum Necessary Context

The system SHOULD follow the principle:

> **Retrieve the minimum information necessary to accomplish the objective safely and effectively.**

This reduces:

* unnecessary computation;
* information exposure;
* cognitive noise;
* network traffic;
* storage requirements.

---

# 15. Context Completeness

A Context MAY expose completeness information.

Example:

```text
Context Status:
INCOMPLETE

Missing:
Current flow rate
```

Incomplete Context SHOULD NOT be treated as complete.

---

# 16. Missing Information

The Context API SHOULD allow the Runtime to identify important missing information.

Conceptually:

```text
context.missing()
```

Example:

```text
Required:
temperature
pressure
flow

Available:
temperature
pressure

Missing:
flow
```

---

# 17. Context Validity

A Context SHOULD have a validity state.

Possible states:

```text
VALID
INCOMPLETE
STALE
INVALID
EXPIRED
REVOKED
```

---

# 18. Context Validation

Conceptual:

```text
context.validate(context_id)
```

Validation MAY check:

* required information;
* freshness;
* authorization;
* policy applicability;
* provenance;
* consistency;
* integrity;
* scope.

---

# 19. Context Freshness

Context MAY become stale as the Organization changes.

Example:

```text
Context created:
14:30:00

Current time:
14:45:00

State changed:
14:43:21
```

The Context may no longer represent current organizational conditions.

---

# 20. Context Refresh

Conceptual:

```text
context.refresh(context_id)
```

Refreshing Context MAY:

* retrieve new State;
* retrieve new Events;
* update Memory references;
* re-evaluate policies;
* remove obsolete information;
* add newly relevant information.

---

# 21. Refresh vs New Context

A Runtime MAY either:

```text
Refresh existing Context
```

or:

```text
Create a new Context version
```

depending on the significance of the change.

Important Decision processes SHOULD preferably preserve the original Context snapshot.

---

# 22. Context Version

Contexts SHOULD support versioning.

Example:

```text
CTX-001 v1
CTX-001 v2
CTX-001 v3
```

Each version represents a distinct Context state.

---

# 23. Context Immutability

A Context used as evidence for a consequential Decision SHOULD be immutable.

Changes SHOULD produce a new version.

---

# 24. Context Freeze

Conceptual:

```text
context.freeze(context_id)
```

Freezing creates a stable Context snapshot.

```text
LIVE CONTEXT
     ↓
   FREEZE
     ↓
IMMUTABLE CONTEXT
```

---

# 25. Frozen Context

A frozen Context SHOULD NOT change.

If additional information is required, a new Context SHOULD be created.

---

# 26. Context Provenance

Important Context elements SHOULD retain provenance.

Example:

```text
Temperature:
72.4 °C

Source:
Sensor-17

Observed:
2026-08-07T14:32:04Z
```

---

# 27. Provenance Requirements

Provenance SHOULD identify, where applicable:

```text
Source
Timestamp
Version
Transformation
Origin
```

---

# 28. Derived Information

Context may contain information derived from other information.

Derived values SHOULD be identifiable.

Example:

```text
Temperature Trend:
Increasing

Derived from:
Temperature observations
```

---

# 29. Evidence

Context MAY contain evidence relevant to its objective.

Example:

```text
Evidence:
Pump vibration increased 18%
during the last 10 minutes.
```

Evidence SHOULD retain provenance.

---

# 30. Policies in Context

Policies relevant to the objective SHOULD be included.

Example:

```text
Production Rate:
Must remain above 80%

Safety:
Maximum pressure = 10 bar
```

---

# 31. Constraints

Context MAY contain explicit constraints.

Examples:

```text
Minimum production
Maximum pressure
Maximum temperature
Available Resources
Authority limits
Time constraints
```

---

# 32. Authority Context

Where Cognition or Decision is involved, Context MAY include the authority of the requesting actor.

Example:

```text
Actor:
Operator-17

Authority:
May request recommendation
May not directly authorize shutdown
```

---

# 33. Capability Context

Context MAY include capabilities relevant to the objective.

Example:

```text
Available Resource:
PumpController-01

Capability:
Adjust speed
```

---

# 34. Resource References

Context SHOULD preferably reference Resources rather than duplicate their complete representation.

Example:

```text
resource_id:
PUMP-001
```

---

# 35. State References

Context SHOULD reference the State version used where possible.

Example:

```text
state_version:
18492
```

This improves reproducibility.

---

# 36. Memory References

Context MAY reference relevant Memory.

Example:

```text
memory_refs:
MEM-182
MEM-441
```

The Context SHOULD NOT automatically expose the entire Memory system.

---

# 37. Event References

Relevant Events MAY be included or referenced.

Example:

```text
event_refs:
EVT-9981
EVT-9984
```

---

# 38. Context Structure

Conceptual structure:

```text
Context {
    id
    organization_id
    objective
    scope
    resources
    state_refs
    memory_refs
    event_refs
    policies
    constraints
    evidence
    authority
    capabilities
    provenance
    status
    version
    created_at
    updated_at
}
```

---

# 39. Context Objective

The objective SHOULD be explicit and machine-readable where possible.

Examples:

```text
diagnose_equipment
evaluate_efficiency
recommend_action
validate_operation
analyze_failure
```

---

# 40. Context Scope

Scope SHOULD prevent unnecessary information retrieval.

Example:

```text
scope:
Production Line 2
```

rather than:

```text
scope:
Entire Organization
```

when the objective concerns only one production line.

---

# 41. Context Filtering

The SDK MAY support filtering.

Conceptual:

```text
context.filter({
    include: [
        "temperature",
        "pressure",
        "flow"
    ]
})
```

Filtering MUST NOT remove mandatory policy or safety information.

---

# 42. Context Expansion

Context MAY be expanded when additional information is required.

```text
Context
   ↓
Missing Information
   ↓
Retrieve
   ↓
Expanded Context
```

---

# 43. Context Reduction

Context MAY also be reduced to remove irrelevant information.

This can improve:

* performance;
* privacy;
* cognitive efficiency;
* processing cost.

---

# 44. Context Budget

A Context MAY have a budget.

Possible limits:

```text
Maximum Items
Maximum Size
Maximum Tokens
Maximum Retrieval Cost
Maximum Processing Time
```

---

# 45. Context Relevance

Information included in Context SHOULD have a reason for inclusion.

A Context SHOULD avoid becoming an uncontrolled information dump.

---

# 46. Context Consistency

The Runtime SHOULD prevent incompatible information versions from being silently combined.

Example:

```text
State v18492
+
Policy v21
+
Memory v8
```

The versions should remain identifiable.

---

# 47. Context Reproducibility

A Context used for important reasoning SHOULD be reproducible where practical.

The Runtime SHOULD retain enough information to determine how it was constructed.

---

# 48. Context Diff

Conceptual:

```text
context.diff(version_a, version_b)
```

A diff MAY show:

```text
Added
Removed
Changed
Expired
Updated
```

---

# 49. Context Lifecycle

A Context MAY follow:

```text
CREATED
   ↓
VALID
   ↓
REFRESHED
   ↓
STALE
   ↓
EXPIRED
```

A Decision-related Context MAY instead follow:

```text
CREATED
   ↓
VALIDATED
   ↓
FROZEN
   ↓
USED
   ↓
ARCHIVED
```

---

# 50. Context Expiration

A Context MAY have an expiration time.

Example:

```text
expires_at:
2026-08-07T15:00:00Z
```

Expiration SHOULD prevent the Context from being treated as current.

---

# 51. Context Revocation

A Context MAY be revoked if:

* its authorization becomes invalid;
* source information is withdrawn;
* organizational policy changes;
* security requirements require invalidation.

---

# 52. Context Deletion

Context deletion SHOULD respect organizational retention policies.

For auditable operations, deletion may mean logical deletion rather than physical destruction.

---

# 53. Context Security

Context can contain highly sensitive organizational information.

The API MUST enforce:

* authentication;
* authorization;
* Organization boundaries;
* Resource access policies;
* data classification;
* retention policies.

---

# 54. Context Isolation

A Context from Organization A MUST NOT be passed to a process operating in Organization B unless explicitly authorized.

---

# 55. Context Access Control

Access MAY be controlled by:

```text
Actor
Role
Resource
Organization
Purpose
Data Classification
Policy
```

---

# 56. Context and Privacy

The Context API SHOULD minimize unnecessary personal or sensitive information.

Information irrelevant to the objective SHOULD NOT be included merely because it is available.

---

# 57. Context and Cognition

Context is the primary input to Cognition.

```text
Context
   ↓
Cognition
```

The Cognition API SHOULD identify the Context used for a cognitive operation.

---

# 58. Context and Decision

A Decision SHOULD reference the Context from which it was produced.

```text
Context
   ↓
Cognition
   ↓
Decision
```

This creates traceability.

---

# 59. Context and Execution

Execution SHOULD NOT rely on an ambiguous or untraceable Context when the Context materially influenced the Decision.

---

# 60. Context and State

State is one of the primary sources of Context.

```text
State
  ↓
Relevant State
  ↓
Context
```

Detailed State semantics belong to **SDK-001 §15 (State API)**.

---

# 61. Context and Memory

Memory provides historical and organizational knowledge relevant to Context.

```text
Memory
   ↓
Relevant Memory
   ↓
Context
```

Detailed Memory semantics belong to the Memory SDK.

---

# 62. Context and Resources

Resources contribute observations, capabilities and operational information.

```text
Resource
   ↓
Information
   ↓
Context
```

Resource semantics are defined by **SDK-003 — Resource API**.

---

# 63. Context and Events

Events may provide recent organizational changes.

```text
Events
   ↓
Relevant Events
   ↓
Context
```

---

# 64. Context and External Information

External information MAY be incorporated where authorized.

External sources SHOULD be explicitly identified.

---

# 65. Context Creation Example

Conceptual:

```text
context = client.context.create({
    organization_id: "ORG-001",
    objective: "evaluate_pump_efficiency",
    scope: "PUMP-001"
})
```

The Runtime assembles relevant information.

---

# 66. Context Validation Example

```text
validation = client.context.validate(
    context.id
)
```

Possible result:

```text
VALID
```

or:

```text
INCOMPLETE
Missing:
flow_rate
```

---

# 67. Context Freeze Example

```text
frozen = client.context.freeze(
    context.id
)
```

The resulting Context becomes a stable snapshot.

---

# 68. Context Refresh Example

```text
context = client.context.refresh(
    context.id
)
```

The refreshed Context SHOULD receive a new version when required.

---

# 69. Context Diff Example

```text
diff = client.context.diff(
    context_v1,
    context_v2
)
```

Possible result:

```text
Changed:
pressure: 4.8 → 5.2 bar

Added:
vibration = HIGH
```

---

# 70. Context Streaming

The SDK MAY support dynamic Context updates.

Streaming SHOULD define:

* ordering;
* reconnection;
* cancellation;
* backpressure;
* versioning.

---

# 71. Context Snapshot

A Context snapshot SHOULD represent a coherent information set.

Snapshots are particularly important for:

* Cognition;
* Decisions;
* audits;
* incident analysis.

---

# 72. Context Freeze Before Decision

For consequential Decisions, the recommended pattern is:

```text
Create Context
      ↓
Validate
      ↓
Freeze
      ↓
Cognition
      ↓
Decision
```

---

# 73. Context Failure

The Runtime SHOULD fail explicitly when safe Context construction is impossible.

It SHOULD NOT silently invent missing information.

---

# 74. Unknown Information

Unknown information MUST remain distinguishable from known negative information.

Example:

```text
temperature = UNKNOWN
```

is not equivalent to:

```text
temperature = 0
```

---

# 75. Context Confidence

A Context MAY include confidence or quality information.

This describes the quality of the assembled information.

It SHOULD NOT be confused with confidence in a Decision.

---

# 76. Context Quality

A Context quality model MAY include:

```text
Completeness
Freshness
Consistency
Provenance
Reliability
Authorization
```

---

# 77. Context Metrics

The Runtime MAY expose:

```text
Context Creation Time
Context Size
Retrieval Cost
Validation Time
Refresh Count
Staleness
```

---

# 78. Context Observability

Important operations SHOULD expose:

```text
ContextID
OrganizationID
RequestID
Version
Timestamp
Actor
Status
```

---

# 79. Context Auditability

The system SHOULD be able to answer:

```text
Which Context was used?
Who created it?
When?
For what objective?
Which State was used?
Which Memory was used?
Which policies applied?
Which Resources contributed?
```

---

# 80. Context Performance

The Context API SHOULD minimize unnecessary retrieval and serialization.

Selective retrieval SHOULD be preferred over retrieving the entire Organization.

---

# 81. Context Caching

Contexts MAY be cached when safe.

Cached Contexts MUST retain freshness and authorization information.

---

# 82. Context Concurrency

When multiple processes modify or refresh Context, version control SHOULD prevent silent overwrites.

---

# 83. Optimistic Concurrency

Conceptually:

```text
context.update(
    expected_version = 4
)
```

If the current version is 5, the Runtime MAY reject the operation.

---

# 84. Context API Errors

Possible errors include:

```text
CONTEXT_NOT_FOUND
CONTEXT_INVALID
CONTEXT_INCOMPLETE
CONTEXT_STALE
CONTEXT_EXPIRED
CONTEXT_REVOKED
CONTEXT_UNAUTHORIZED
CONTEXT_CONFLICT
CONTEXT_SOURCE_UNAVAILABLE
```

---

# 85. Context Security Requirements

The Context API MUST:

1. enforce Organization boundaries;
2. enforce authorization;
3. preserve provenance;
4. protect sensitive information;
5. distinguish current and stale Context;
6. preserve version information;
7. prevent unauthorized Context reuse;
8. prevent silent fabrication of missing information.

---

# 86. Conformance Requirements

An implementation conforming to SDK-004 MUST:

1. provide Context identity;
2. associate Context with an Organization;
3. support objective and scope;
4. support Context creation;
5. support Context retrieval;
6. support Context validation;
7. represent Context status;
8. preserve relevant provenance;
9. support Context versioning where required;
10. preserve organizational security boundaries.

---

# 87. Recommended Capabilities

A mature implementation SHOULD additionally provide:

* Context refresh;
* Context freeze;
* Context diff;
* Context snapshots;
* selective retrieval;
* Context budgets;
* streaming;
* caching;
* optimistic concurrency;
* completeness analysis;
* freshness analysis;
* simulation.

---

# 88. Recommended Operational Pattern

The preferred VIAL pattern is:

```text
1. Define Objective
        ↓
2. Define Scope
        ↓
3. Assemble Context
        ↓
4. Validate Context
        ↓
5. Freeze if consequential
        ↓
6. Pass Context to Cognition
        ↓
7. Produce Decision
```

---

# 89. Final Principles

### Principle 1 — Context Is Purpose

> Context exists because something needs to be understood, evaluated or decided.

### Principle 2 — Context Is Selective

> Context should contain relevant information, not everything that exists.

### Principle 3 — Context Is Traceable

> Important information must retain its provenance.

### Principle 4 — Context Is Time-Bound

> A Context can become stale as organizational reality changes.

### Principle 5 — Context Must Be Validated

> Cognition should not blindly operate on incomplete or invalid Context.

### Principle 6 — Context Must Respect Authority

> Context access is governed by organizational authorization.

### Principle 7 — Context Enables Cognition

> Cognition should receive a meaningful representation of organizational reality rather than an uncontrolled data dump.

---

# 90. Final Statement

The Context API establishes the bridge between the Organization and VIAL's cognitive processes:

```text
ORGANIZATION
      │
      ├── Resources
      ├── State
      ├── Memory
      ├── Events
      └── Policies
             │
             ▼
          CONTEXT
             │
             ▼
         COGNITION
             │
             ▼
          DECISION
             │
             ▼
         EXECUTION
```

Context is therefore not merely a data structure.

It is a **purposeful representation of organizational reality** prepared for understanding, reasoning and action.

> **The quality of Cognition is constrained by the quality of the Context from which it reasons.**

# End of SDK-004
