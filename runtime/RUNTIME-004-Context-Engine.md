# RUNTIME-004 — VIAL Context Engine

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Runtime Specification
Depends On:
- RUNTIME-001
- RUNTIME-002
- RUNTIME-003
- RFC-003
- RFC-004

---

# 1. Abstract

This document defines the **VIAL Context Engine**.

The Context Engine transforms relevant organizational information into the **minimum sufficient Context** required for Cognition and Decision.

Its primary objectives are:

* reduce unnecessary computation;
* reduce unnecessary data transfer;
* reduce cognitive cost;
* improve decision quality;
* preserve traceability;
* prevent context contamination;
* support scalable execution.

The fundamental principle is:

> **The Runtime should provide enough Context to make a correct Decision, but no more Context than necessary.**

---

# 2. Purpose

The Context Engine connects:

```text
State
+
Memory
+
Event
+
Objective
+
Evidence
+
Policies
      ↓
Context
      ↓
Cognition
```

It does not make the Decision itself.

Its responsibility is to construct the information environment in which the Decision can be made.

---

# 3. Context Definition

Context is a temporary, purpose-specific representation of information assembled for a Runtime cycle.

```text
State
=
Current organizational condition

Memory
=
Retained organizational knowledge

Context
=
Relevant information assembled for the current task
```

Context therefore SHOULD be treated as a derived artifact rather than permanent organizational truth.

---

# 4. Context Characteristics

A valid Context SHOULD be:

* relevant;
* sufficient;
* bounded;
* traceable;
* scoped;
* time-aware;
* policy-aware;
* reproducible where required.

---

# 5. Context Construction

The canonical process is:

```text
EVENT
  ↓
OBJECTIVE
  ↓
STATE
  ↓
MEMORY
  ↓
POLICIES
  ↓
EVIDENCE
  ↓
FILTER
  ↓
CONTEXT
```

---

# 6. Minimum Sufficient Context

The Context Engine SHOULD seek the smallest information set capable of supporting the required operation.

Conceptually:

```text
Too Little Context
        ↓
Poor Decision

Too Much Context
        ↓
Higher Cost
Higher Latency
More Noise

Minimum Sufficient Context
        ↓
Efficient Decision
```

This principle is central to VIAL's goal of reducing consumption.

---

# 7. Context Scope

Every Context SHOULD identify its scope.

Example:

```text
Organization
Site
Production Line
Equipment
Process
Task
```

Context SHOULD NOT contain unrelated organizational information merely because it is available.

---

# 8. Context Identity

A Context MAY contain:

```text
Context ID
Cycle ID
Organization
Scope
Created At
Validity
Source References
Context Version
```

Example:

```text
Context ID: CTX-000482
Cycle ID: C-000921
Scope: Production-Line-03
```

---

# 9. Context Sources

Possible sources include:

* State;
* Memory;
* Events;
* external observations;
* Tools;
* policies;
* procedures;
* human input;
* previous Decisions;
* system configuration.

Each source SHOULD remain identifiable.

---

# 10. Source Provenance

The Context Engine SHOULD preserve provenance.

Example:

```text
Pressure = 5.1 bar

Source:
Sensor-42

Observed:
10:03:22

State:
Version 482
```

This prevents information from becoming detached from its origin.

---

# 11. Context Freshness

Context is time-sensitive.

Each relevant element SHOULD have sufficient information to determine whether it remains valid.

```text
Context
 ↓
Age
 ↓
Validity
```

---

# 12. Context Expiration

Context MAY expire.

Example:

```text
Context created:
10:00

Validity:
5 minutes

Current:
10:07
```

The Runtime SHOULD rebuild or refresh the Context before executing a high-impact Decision.

---

# 13. Context Composition

Context MAY contain:

```text
Facts
State
Observations
Memory
Policies
Constraints
Objectives
Evidence
Prior Decisions
Relevant History
```

The exact composition depends on the task.

---

# 14. Facts

A Context SHOULD distinguish facts from interpretations.

Example:

```text
Fact:
Temperature = 82°C
```

versus:

```text
Interpretation:
Equipment may be overheating.
```

This distinction improves auditability.

---

# 15. Evidence

Evidence supports a claim within Context.

Examples:

```text
Sensor measurement
Document
Database record
Human observation
Tool result
Historical record
```

Important Decisions SHOULD preserve evidence references.

---

# 16. Evidence Hierarchy

Organizations MAY define evidence priorities.

Example:

```text
Verified Sensor
      ↓
Validated Database
      ↓
Authorized Human Observation
      ↓
Derived Value
      ↓
Unverified Information
```

The exact hierarchy is domain-specific.

---

# 17. Policy Inclusion

Policies relevant to the current task SHOULD be included in Context.

Example:

```text
Objective:
Reduce pressure

Relevant Policy:
Maximum permitted pressure = 5 bar
```

Unrelated policies SHOULD NOT be loaded unnecessarily.

---

# 18. Constraint Inclusion

Context SHOULD include constraints relevant to the proposed operation.

Examples:

* safety limits;
* financial limits;
* operational limits;
* authorization limits;
* resource limits;
* timing constraints.

---

# 19. Objective

The Context Engine SHOULD make the current Objective explicit.

Example:

```text
Objective:
Maintain production while keeping pressure below safety limit.
```

An explicit Objective reduces ambiguity during Cognition.

---

# 20. Context Assembly

A conceptual assembly process is:

```text
Collect
  ↓
Normalize
  ↓
Filter
  ↓
Rank
  ↓
Validate
  ↓
Assemble
  ↓
Compress
  ↓
Publish Context
```

---

# 21. Collection

The Engine identifies candidate information from available sources.

It SHOULD prioritize sources relevant to the current scope.

---

# 22. Filtering

Candidate information SHOULD be filtered according to:

* relevance;
* scope;
* freshness;
* authority;
* objective;
* cost.

---

# 23. Ranking

Where many candidates exist, the Engine MAY rank them.

Possible ranking factors:

```text
Relevance
Freshness
Authority
Reliability
Specificity
Cost
```

---

# 24. Context Compression

Context MAY be compressed when the original information is larger than necessary.

Compression MAY include:

* summarization;
* aggregation;
* deduplication;
* structured representation;
* reference substitution.

Compression MUST preserve information required for the Decision.

---

# 25. Reference Instead of Duplication

Where possible, Context SHOULD reference existing artifacts rather than duplicate them.

Example:

```text
State Version 482
```

instead of copying the entire State representation.

This reduces:

* memory;
* network traffic;
* storage;
* processing.

---

# 26. Context Deduplication

Repeated information SHOULD be removed.

Example:

```text
Temperature = 80°C
Temperature = 80°C
Temperature = 80°C
```

may be represented once with its provenance.

---

# 27. Context Conflict

Sources may disagree.

Example:

```text
Sensor A:
80°C

Sensor B:
86°C
```

The Context Engine MUST NOT silently select one without a defined rule.

Possible outcomes:

```text
Resolve
Flag Conflict
Request Verification
Escalate
```

---

# 28. Unknown Information

Missing information SHOULD remain explicitly unknown.

```text
Pressure = UNKNOWN
```

must not silently become:

```text
Pressure = 0
```

unless the domain explicitly defines the default.

---

# 29. Contradictory Context

If contradictory information materially affects the Decision, the Context SHOULD identify the conflict.

Example:

```text
Context Warning:
Pressure sources disagree.
```

The Cognition layer can then determine the appropriate response.

---

# 30. Context Confidence

Context elements MAY carry confidence or reliability metadata.

Example:

```text
Temperature:
Value = 82°C
Confidence = Verified
```

Confidence SHOULD remain distinguishable from authority.

---

# 31. Context Authority

A source being technically accessible does not make it organizationally authoritative.

```text
Accessible
≠
Authorized
```

The Context Engine SHOULD preserve source authority metadata.

---

# 32. Context Security

Context may contain sensitive information.

The Engine SHOULD enforce:

* scope;
* access control;
* authorization;
* data classification;
* tenant isolation.

---

# 33. Least Context Principle

A Resource SHOULD receive only the Context necessary for its assigned task.

Example:

```text
Temperature Analyzer
```

does not necessarily require:

```text
Entire Organization Financial State
```

This is important for security and efficiency.

---

# 34. Context Isolation

Contexts belonging to different Organizations or security domains MUST remain isolated unless explicitly authorized.

```text
Organization A Context
≠
Organization B Context
```

---

# 35. Multi-Resource Context

Different Resources MAY receive different Context projections.

Example:

```text
Full Context
     │
 ┌───┼────┐
 ↓   ↓    ↓
AI  Rule Human
```

Each Resource receives only the information appropriate to its role.

---

# 36. Context Projection

A Context Projection is a subset or transformed representation of the canonical Context.

Example:

```text
Canonical Context
      ↓
AI Projection
      ↓
Rule Projection
      ↓
Human Projection
```

All projections SHOULD remain traceable to the originating Context.

---

# 37. Context and AI

When AI is used, the Context Engine SHOULD provide structured information whenever possible.

Prefer:

```text
State:
Temperature = 82°C
Pressure = 5.1 bar
```

over unnecessary unstructured repetition.

This reduces token consumption and ambiguity.

---

# 38. Context and Deterministic Resources

Deterministic Resources MAY require very little Context.

Example:

```text
Pressure > 5 bar
```

may be sufficient for a rule engine.

The Runtime SHOULD not send unnecessary information to deterministic components.

---

# 39. Context and Human Resources

Human Resources MAY require a richer presentation.

The underlying Context remains the same, but the presentation MAY differ.

```text
Machine Data
      ↓
Human-readable Context
```

---

# 40. Context and Memory

Memory retrieval SHOULD be selective.

The Runtime SHOULD prefer:

```text
Relevant Memory
```

rather than:

```text
All Historical Memory
```

---

# 41. Memory Retrieval Strategy

Memory MAY be retrieved using:

* semantic relevance;
* exact references;
* temporal relevance;
* organizational scope;
* causal relationships;
* previous Decisions.

---

# 42. Historical Depth

The Engine SHOULD determine how much history is required.

Example:

```text
Routine operation
→ Recent State

Failure investigation
→ Extended history
```

Historical depth should be task-dependent.

---

# 43. Context Cost

The Runtime SHOULD measure Context cost.

Possible metrics:

```text
Bytes
Tokens
Queries
Retrieval Latency
Memory Consumption
Network Transfer
Processing Time
```

---

# 44. Context Budget

A cycle MAY define a Context budget.

Example:

```text
Maximum retrieval cost
Maximum token budget
Maximum latency
Maximum number of sources
```

The Engine SHOULD optimize within the budget.

---

# 45. Cost-Aware Retrieval

If two sources provide equivalent information:

```text
Source A:
100 ms

Source B:
2 seconds
```

the Runtime SHOULD prefer the lower-cost source when quality and authority are equivalent.

---

# 46. Context Cache

Frequently reused Context components MAY be cached.

Cache entries MUST preserve:

```text
Version
Timestamp
Scope
Validity
Provenance
```

---

# 47. Context Reuse

Context reuse is allowed only when the underlying information remains valid.

```text
Cached Context
 ↓
Validate Freshness
 ↓
Reuse
```

or:

```text
Cached Context
 ↓
Invalid
 ↓
Rebuild
```

---

# 48. Context Invalidation

A Context MAY become invalid because:

* State changed;
* policy changed;
* authorization changed;
* evidence expired;
* external condition changed;
* objective changed.

---

# 49. Context Dependencies

The Engine SHOULD be able to identify dependencies.

Example:

```text
Context
 ├── State v482
 ├── Policy P12 v3
 ├── Memory M42
 └── Sensor S17
```

This makes invalidation possible.

---

# 50. Context Rebuild

When a critical dependency changes:

```text
Dependency Changed
       ↓
Context Invalidated
       ↓
Context Rebuilt
```

---

# 51. Context Snapshot

For important Decisions, the Runtime SHOULD preserve the Context Snapshot used.

This enables:

```text
Decision
 ↓
Context Snapshot
 ↓
State
 ↓
Evidence
```

and therefore historical reconstruction.

---

# 52. Context Determinism

The same Context inputs SHOULD produce the same Context representation when deterministic processing is required.

Where dynamic retrieval occurs, the Runtime SHOULD record the actual sources used.

---

# 53. Context Reproducibility

A Context SHOULD be reproducible enough to support:

* audit;
* debugging;
* evaluation;
* simulation;
* incident investigation.

Perfect reproduction is not required where external information is inherently dynamic, but the Runtime SHOULD preserve the relevant references.

---

# 54. Context Lifecycle

The canonical Context lifecycle is:

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

After FROZEN, the normative content of a Context MUST NOT change. A new Context SHALL be created when additional information is required.

The Runtime SHALL recognize FROZEN (ADR-0006 D-004).

Additional conditions MAY exist without creating a competing lifecycle. For example, temporal validity MAY produce:

```text
EXPIRED
```

as a terminal condition. A Context that is EXPIRED is no longer valid for a new Decision but remains a stable record once FROZEN.

---

# 55. Context Status

Possible statuses:

```text
CREATED
VALIDATING
VALID
FROZEN
PARTIAL
CONFLICTED
STALE
INVALID
EXPIRED
CONSUMED
ARCHIVED
```

FROZEN and ARCHIVED are lifecycle states (see §54). The other statuses are conditions that MAY apply without defining a competing lifecycle.

---

# 56. Partial Context

If sufficient information is unavailable, the Engine MAY produce a Partial Context.

Example:

```text
Context:
State = Complete
Memory = Partial
External Evidence = Missing
```

The Runtime SHOULD clearly identify the limitation.

---

# 57. Context Completeness

Completeness is task-dependent.

A Context is not incomplete merely because it does not contain every available piece of information.

The correct question is:

> **Does the Context contain what is required for this operation?**

---

# 58. Context Validation Contract

Before Cognition, the Context Engine SHOULD verify:

```text
Scope
Objective
State
Evidence
Policies
Constraints
Freshness
Conflicts
Authority requirements
```

---

# 59. Context Failure

If required Context cannot be constructed, the Runtime MAY:

```text
Retry
Retrieve additional information
Request clarification
Escalate
Use a safer fallback
Terminate
```

The Runtime SHOULD record the reason.

---

# 60. Context and Auditability

The audit trail SHOULD identify:

```text
What information was used
Where it came from
When it was retrieved
Which version was used
Why it was included
```

This enables later examination of the Decision process.

---

# 61. Context and Organizational Learning

Context itself may reveal recurring information requirements.

For example:

```text
Every maintenance Decision
requires:
Temperature
Pressure
Operating Hours
```

The Runtime may eventually optimize this retrieval pattern.

---

# 62. Context Templates

Organizations MAY define Context Templates.

Example:

```text
Maintenance Context:

Equipment
Operating Hours
Temperature
Pressure
Last Maintenance
Current Alarms
Relevant Procedure
```

Templates reduce repeated discovery.

---

# 63. Context Template Versioning

Templates SHOULD be versioned.

Example:

```text
Maintenance Context v3
```

Decisions SHOULD identify the template version when relevant.

---

# 64. Context Policy

Organizations MAY define policies controlling:

* mandatory fields;
* prohibited data;
* retention;
* maximum size;
* source priority;
* security classification.

---

# 65. Context Governance

The Context Engine SHOULD provide governance mechanisms to prevent:

* unnecessary data exposure;
* uncontrolled context growth;
* stale information;
* undocumented source substitution;
* cross-tenant contamination.

---

# 66. Context Economy

Context efficiency is a major VIAL design objective.

The Runtime SHOULD favor:

```text
Reuse
+
Reference
+
Compression
+
Filtering
+
Caching
+
Deterministic Processing
```

over:

```text
Repeated Retrieval
+
Repeated Inference
+
Repeated Transmission
```

---

# 67. Context and Scalability

Large-scale VIAL Organizations may execute thousands or millions of cycles.

Therefore Context construction MUST be economical.

A small saving per cycle can become significant at scale.

```text
1 KB saved × 1,000,000 cycles
=
~1 GB less data movement
```

The same principle applies to:

* tokens;
* database queries;
* CPU;
* network;
* storage;
* latency.

---

# 68. Context Reuse Across Cycles

Some Context components MAY be reused across cycles.

Example:

```text
Organization Policy
```

may remain valid for many cycles.

Dynamic information such as:

```text
Current Pressure
```

may require frequent refresh.

The Engine SHOULD distinguish stable and dynamic information.

---

# 69. Stable Context

Examples:

```text
Policy
Procedure
Equipment Specification
Organizational Structure
```

These MAY be cached aggressively.

---

# 70. Dynamic Context

Examples:

```text
Sensor Values
Current State
Current Load
Active Alarms
External Conditions
```

These SHOULD have stricter freshness rules.

---

# 71. Context Layering

A useful implementation model is:

```text
┌─────────────────────────────┐
│ Dynamic Context             │
├─────────────────────────────┤
│ Operational State           │
├─────────────────────────────┤
│ Relevant Memory             │
├─────────────────────────────┤
│ Policies / Constraints      │
├─────────────────────────────┤
│ Stable Knowledge            │
└─────────────────────────────┘
```

Only layers required for the current operation should be loaded.

---

# 72. Context and Distributed Cognition

Different organizational Resources may consume the same canonical Context.

```text
             Context
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
     Human      AI      Rule
       │        │        │
       └────────┼────────┘
                ↓
             Decision
```

This supports the TDOC principle of distributed organizational cognition.

---

# 73. Context and Organizational Coherence

Without a common Context foundation:

```text
Human sees X
AI sees Y
Rule Engine sees Z
```

The Organization may behave inconsistently.

The Context Engine reduces this risk by establishing a controlled information boundary.

---

# 74. Context API Boundary

A conceptual Context interface MAY provide:

```text
createContext()
getContext()
validateContext()
refreshContext()
invalidateContext()
projectContext()
snapshotContext()
estimateCost()
```

These names are conceptual.

---

# 75. Context Contract

A conceptual Context contract is:

```text
Context {
    id
    cycle
    objective
    scope
    state_reference
    memory_references
    evidence
    policies
    constraints
    freshness
    provenance
    validity
}
```

---

# 76. Relationship With RUNTIME-003

RUNTIME-003 provides:

```text
State
```

RUNTIME-004 transforms State and other sources into:

```text
Context
```

The relationship is:

```text
RUNTIME-003
State Engine
     ↓
RUNTIME-004
Context Engine
     ↓
Cognition
```

---

# 77. Relationship With RUNTIME-002

The Execution Cycle invokes the Context Engine during:

```text
Event
 ↓
State
 ↓
Context
 ↓
Cognition
```

The Context Engine therefore operates as a core Runtime component.

---

# 78. Non-Goals

RUNTIME-004 does not define:

* a specific vector database;
* a specific LLM;
* a specific prompt format;
* a specific database;
* a UI;
* a programming language;
* a cloud provider;
* a specific retrieval algorithm.

These belong to implementation or SDK specifications.

---

# 79. Conformance Requirements

A Context Engine conforming to RUNTIME-004 MUST:

1. construct task-specific Context;
2. preserve source provenance;
3. respect organizational scope;
4. distinguish State, Memory, Event and Context;
5. support freshness evaluation;
6. identify critical conflicts;
7. avoid silently converting unknown information into known values;
8. support Context validation;
9. preserve sufficient traceability for important Decisions;
10. minimize unnecessary Context consumption.

---

# 80. Recommended Capabilities

A mature implementation SHOULD support:

* Context templates;
* Context caching;
* Context projections;
* cost-aware retrieval;
* conflict detection;
* context snapshots;
* invalidation;
* compression;
* deduplication;
* dependency tracking;
* context budgets;
* distributed Context construction.

---

# 81. Final Principles

### Principle 1 — Minimum Sufficient Context

> Use what is necessary, not everything that is available.

### Principle 2 — Context Is Derived

> Context is constructed for a task and does not replace organizational State.

### Principle 3 — Provenance Matters

> Information without origin loses organizational traceability.

### Principle 4 — Unknown Is Explicit

> Missing information must remain distinguishable from known information.

### Principle 5 — Freshness Matters

> Old Context must not silently become current Context.

### Principle 6 — Context Is Economical

> Every unnecessary byte, query, token and computation has a cost at scale.

### Principle 7 — Context Is Shared Carefully

> Distributed cognition requires coherent information without unnecessary data exposure.

---

# 82. Final Statement

The VIAL Context Engine is the mechanism that converts organizational information into usable organizational understanding.

Its central optimization is:

```text
More Data
      ≠
Better Cognition
```

Instead:

```text
Relevant Data
+
Correct State
+
Reliable Evidence
+
Applicable Policy
+
Clear Objective
      ↓
Minimum Sufficient Context
      ↓
Efficient Cognition
```

The objective is not to maximize the amount of information provided to a Resource.

The objective is to maximize **decision value per unit of information and computation**.

> **Good Context is not more information. Good Context is the right information at the right time, for the right Decision.**

# End of RUNTIME-004
