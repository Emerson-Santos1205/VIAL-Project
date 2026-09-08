# SDK-005 — VIAL Decision API

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** SDK Specification
Depends On:
- FCP-002A
- RFC-002
- RFC-003
- RFC-004
- RFC-005
- RFC-006
- SDK-001
- SDK-002
- SDK-003
- SDK-004

---

# 1. Abstract

This document defines the **VIAL Decision API**.

A Decision represents a formally identifiable organizational conclusion produced from a Context and subject to organizational authority, policies and constraints.

The fundamental principle is:

> **A Decision is an organizational commitment to a selected course of action, recommendation or conclusion under a defined Context.**

A Decision is distinct from:

* an observation;
* a Context;
* a Cognition process;
* an intention;
* an execution;
* an action result.

---

# 2. Purpose

The Decision API provides a standardized interface for:

* creating Decisions;
* retrieving Decisions;
* validating Decisions;
* recording Decision rationale;
* associating Decisions with Context;
* identifying Decision makers;
* recording authority;
* evaluating Decision status;
* approving or rejecting Decisions;
* tracking Decision lifecycle;
* linking Decisions to Execution;
* preserving Decision provenance;
* auditing consequential Decisions.

---

# 3. Decision Position in VIAL

The conceptual flow is:

```text
Organization
      │
      ▼
   Context
      │
      ▼
   Cognition
      │
      ▼
   DECISION
      │
      ▼
 Authorization
      │
      ▼
   Approval
      │
      ▼
  Invocation
      │
      ▼
  Execution
      │
      ▼
    Outcome
```

The Decision is the bridge between organizational reasoning and organizational action.

---

# 4. Decision Definition

A Decision is a structured organizational artifact that records:

```text
Objective
Context
Alternatives
Selected Outcome
Authority
Rationale
Constraints
Actor
Timestamp
Status
```

---

# 5. Decision Is Not Cognition

Cognition is the process of reasoning.

Decision is the resulting organizational conclusion.

```text
Cognition
   ↓
Reasoning
   ↓
Evaluation
   ↓
Decision
```

A Cognition process MAY produce multiple candidate outcomes before one becomes a Decision.

---

# 6. Decision Is Not Execution

A Decision does not automatically execute an action.

```text
Decision
   ↓
Authorization
   ↓
Approval (when required)
   ↓
Invocation
   ↓
Execution
```

Execution requires its own authority and Runtime controls.

---

# 7. Decision Identity

Every Decision MUST have a unique identifier.

Conceptually:

```text
DecisionID
```

Example:

```text
DEC-2026-000184
```

---

# 8. Decision Organization

Every Decision MUST belong to an Organization.

```text
Decision {
    decision_id
    organization_id
}
```

Cross-Organization Decisions MUST be explicitly authorized.

---

# 9. Decision Context

Every consequential Decision SHOULD reference the Context from which it was produced.

```text
Decision
   │
   └── ContextID
```

Where reproducibility is important, the Decision SHOULD reference a frozen Context version.

---

# 10. Decision Objective

A Decision SHOULD explicitly identify its objective.

Examples:

```text
reduce_energy_consumption
maintain_production
respond_to_alarm
select_resource
approve_operation
```

---

# 11. Decision Type

A Decision MAY have a type.

Examples:

```text
RECOMMENDATION
REJECTION
SELECTION
CLASSIFICATION
PRIORITIZATION
ACTION
POLICY
```

The exact taxonomy MAY be extended.

---

# 12. Decision Outcome

A Decision MUST identify its outcome.

Example:

```text
Outcome:
Reduce Pump-01 speed to 70%.
```

The outcome SHOULD be structured whenever possible.

---

# 13. Decision Status

Decision states are divided into lifecycle states and terminal states.

Lifecycle states:

```text
DRAFT
PENDING
AUTHORIZED
EXECUTING
COMPLETED
```

Terminal or alternative states:

```text
CANCELLED
REJECTED
FAILED
REVOKED
```

ESCALATION is not a Decision state.

It is an event or transition that routes a Decision toward additional authority or human review.

---

# 14. Decision Lifecycle

A typical lifecycle is:

```text
DRAFT
  ↓
PENDING
  ↓
AUTHORIZED
  ↓
EXECUTING
  ↓
COMPLETED
```

Alternative outcomes MAY include:

```text
CANCELLED
REJECTED
FAILED
REVOKED
```

A Decision MAY transition to a terminal state from any lifecycle state where the Runtime permits it.

---

# 15. Decision Creation

Conceptual API:

```text
decision.create({
    organization_id,
    context_id,
    objective,
    outcome
})
```

Creation does not imply approval or execution.

---

# 16. Decision Proposal

A Decision MAY initially exist as a proposal.

```text
decision.propose()
```

A proposal represents a candidate organizational conclusion.

---

# 17. Decision Approval

A Decision MAY require explicit approval.

```text
decision.approve()
```

Approval MUST require appropriate authority.

> **Note on Approval semantics:** `decision.approve()` is an internal system
> approval that records acceptance of a proposal. It is part of the standard
> `propose → approve → authorize` flow and does NOT constitute human approval.
> Human approval is a separate, explicit step recorded via
> `approve_decision()` and stored as an `ApprovalRecord`. For medium-risk
> operations, the system approval in `propose_decision()` is sufficient. For
> high/critical risks, an additional `ApprovalRecord` is required (see §67).

---

# 18. Decision Rejection

A Decision MAY be rejected.

```text
decision.reject()
```

A rejection SHOULD preserve:

* rejecting actor;
* timestamp;
* reason;
* authority context.

---

# 19. Decision Authorization

Approval and authorization SHOULD be distinguishable.

```text
APPROVED
```

means the Decision has been accepted by the relevant authority.

```text
AUTHORIZED
```

means the Decision is permitted to proceed under the applicable execution authority.

---

# 20. Decision Rationale

A consequential Decision SHOULD include rationale.

Conceptually:

```text
rationale {
    summary
    evidence
    constraints
    reasoning_reference
}
```

The rationale SHOULD explain why the selected outcome was chosen.

---

# 21. Evidence

Decision evidence SHOULD reference information rather than duplicating authoritative data unnecessarily.

Examples:

```text
State version
Event IDs
Memory references
Resource observations
External sources
```

---

# 22. Evidence Provenance

Evidence SHOULD retain:

```text
Source
Timestamp
Version
Origin
Transformation
```

This enables later reconstruction of the Decision basis.

---

# 23. Alternatives

Where meaningful, a Decision SHOULD identify considered alternatives.

Example:

```text
Alternative A:
Reduce pump speed.

Alternative B:
Stop pump.

Alternative C:
Continue operation.
```

---

# 24. Selected Alternative

The Decision MUST identify the selected outcome.

```text
selected_alternative
```

or an equivalent structured representation.

---

# 25. Rejected Alternatives

Rejected alternatives MAY be recorded.

This is especially useful for:

* audits;
* safety analysis;
* incident investigation;
* organizational learning.

---

# 26. Decision Constraints

A Decision MAY contain explicit constraints.

Examples:

```text
Maximum pressure: 10 bar
Minimum production: 80%
Authority level: Operator
Execution deadline: 15 minutes
```

---

# 27. Decision Preconditions

A Decision MAY define Preconditions.

Example:

```text
Execute only if:
pressure < 8 bar
AND
temperature < 75°C
```

Preconditions SHOULD be evaluated before execution.

---

# 28. Decision Postconditions

A Decision MAY define expected postconditions.

Example:

```text
Expected:
pump_speed = 70%
pressure < 8 bar
```

Postconditions can later be evaluated against actual execution results.

---

# 29. Decision Authority

Every consequential Decision SHOULD identify the authority under which it was created or approved.

Conceptually:

```text
authority {
    actor
    role
    scope
    policy
}
```

---

# 30. Decision Actor

The Decision SHOULD identify its originating actor.

The actor MAY be:

```text
Human
AI Agent
Service
Organization Process
System
```

---

# 31. Human Decision

A human may create or approve a Decision.

Example:

```text
Operator-17
approved:
Shutdown Pump-01
```

---

# 32. AI Decision

An AI Resource MAY produce a Decision when authorized.

The Decision MUST identify the AI Resource.

Example:

```text
Decision Actor:
Agent-07
```

The system SHOULD NOT conceal that the Decision originated from an AI Resource.

---

# 33. Delegated Decision Authority

An Actor MAY make a Decision under delegated authority.

Delegation SHOULD identify:

```text
Delegator
Delegate
Scope
Duration
Policy
```

---

# 34. Decision Authority Validation

The Runtime MUST validate whether the Actor has authority to create, approve or execute the Decision.

---

# 35. Decision Confidence

A Decision MAY contain a confidence or certainty value where appropriate.

Example:

```text
confidence = 0.87
```

Confidence MUST NOT be interpreted as authorization.

---

# 36. Confidence vs Authority

These concepts are independent:

```text
Confidence
= how strongly the system supports the conclusion

Authority
= whether the Actor is permitted to make or execute it
```

A high-confidence Decision can still be unauthorized.

---

# 37. Decision Risk

A Decision MAY contain a risk classification.

Examples:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Risk classification SHOULD influence approval requirements.

---

# 38. Decision Impact

A Decision MAY identify expected impact.

Examples:

```text
Production
Safety
Energy
Financial
Availability
Security
```

---

# 39. Decision Priority

A Decision MAY have a priority.

Example:

```text
LOW
NORMAL
HIGH
URGENT
CRITICAL
```

Priority SHOULD NOT bypass authorization.

---

# 40. Decision Deadline

A Decision MAY have a deadline.

```text
expires_at
```

After expiration, the Decision SHOULD NOT be executed without revalidation.

---

# 41. Decision Revalidation

Before execution, the Runtime MAY revalidate:

```text
Context
State
Policies
Authority
Preconditions
Resource availability
```

---

# 42. Decision Staleness

A Decision may become stale when organizational reality changes.

Example:

```text
Decision based on:
Pressure = 5 bar

Current:
Pressure = 9 bar
```

The Runtime SHOULD detect whether the Decision remains valid.

---

# 43. Decision Supersession

A newer Decision MAY supersede an older Decision.

```text
Decision A
    ↓
SUPERSEDED BY
    ↓
Decision B
```

The historical Decision SHOULD remain traceable.

---

# 44. Decision Cancellation

A Decision MAY be cancelled before execution.

Cancellation SHOULD record:

```text
Actor
Timestamp
Reason
Authority
```

Cancellation is distinct from revocation:

```text
CANCELLED
```

means the Decision was withdrawn before taking effect, while:

```text
REVOKED
```

means an existing Decision was withdrawn after it had been authorized. In both cases execution MUST NOT proceed.

---

# 45. Decision Expiration

A Decision MAY automatically expire.

Expiration SHOULD be distinguishable from rejection.

---

# 46. Decision Conflict

Two Decisions MAY conflict.

The Runtime SHOULD detect conflicts when they affect the same:

```text
Resource
State
Objective
Policy
Execution scope
```

---

# 47. Decision Priority Resolution

When conflicting Decisions exist, resolution MUST follow organizational governance.

The SDK MUST NOT invent priority rules silently.

---

# 48. Decision Dependencies

A Decision MAY depend on another Decision.

Example:

```text
Decision A:
Approve maintenance

Decision B:
Stop equipment

B depends on A
```

---

# 49. Decision Chain

Decisions MAY form a chain:

```text
Observation
    ↓
Decision A
    ↓
Decision B
    ↓
Execution
```

This enables organizational traceability.

---

# 50. Decision Graph

The Runtime MAY represent Decision relationships as a graph.

```text
Context
   ↓
Decision A
   ├── Alternative A
   ├── Alternative B
   └── Selected B
          ↓
      Decision B
          ↓
       Execution
```

---

# 51. Decision API

The SDK SHOULD provide:

```text
decision.create()
decision.get()
decision.list()
decision.propose()
decision.approve()
decision.reject()
decision.authorize()
decision.cancel()
decision.revoke()
decision.escalate()
decision.validate()
decision.revalidate()
decision.supersede()
decision.expire()
decision.history()
```

---

# 52. Decision History

Conceptual:

```text
decision.history(decision_id)
```

History SHOULD include:

```text
Created
Proposed
Modified
Approved
Rejected
Authorized
Cancelled
Executed
Superseded
```

---

# 53. Decision Immutability

Once a Decision has materially influenced execution, its historical record SHOULD be immutable.

Changes SHOULD create a new Decision or version.

---

# 54. Decision Versioning

A Decision MAY support versions.

```text
DEC-001 v1
DEC-001 v2
```

Each version SHOULD remain traceable.

---

# 55. Decision Snapshot

A consequential Decision SHOULD preserve a snapshot containing:

```text
Decision
Context reference
Context version
Evidence
Authority
Policy
Timestamp
```

---

# 56. Decision Reproducibility

The system SHOULD allow an authorized investigator to reconstruct the basis of a Decision.

---

# 57. Decision Explainability

Where a Decision originates from Cognition, the system SHOULD provide an appropriate explanation or rationale.

The explanation SHOULD identify evidence and relevant factors without exposing restricted internal information.

---

# 58. Decision Traceability

The Decision SHOULD be traceable to:

```text
Organization
Context
Resources
State
Memory
Events
Cognition
Actor
Authority
Execution
Result
```

---

# 59. Decision and Context

The Decision depends on Context.

```text
Context
   ↓
Decision
```

A Decision SHOULD NOT claim to be based on information absent from its Context unless that information is separately recorded.

---

# 60. Decision and Cognition

Cognition MAY produce:

```text
Candidate Decisions
```

The Decision API records the organizationally relevant result.

---

# 61. Decision and Execution

The relationship is:

```text
Decision
   ↓
Execution Request
   ↓
Execution
```

Execution is not guaranteed merely because a Decision exists.

---

# 62. Decision and Resource

A Decision MAY target one or more Resources.

Example:

```text
Decision:
Reduce speed

Target:
Pump-01
```

---

# 63. Decision and State

Decision evaluation may depend on State.

State references SHOULD identify the relevant version or observation time.

---

# 64. Decision and Memory

Historical Memory MAY influence a Decision.

Memory references SHOULD preserve provenance.

---

# 65. Decision and Policy

Policies constrain Decisions.

Example:

```text
Policy:
Pressure > 10 bar requires emergency shutdown.
```

A Decision violating mandatory policy SHOULD be rejected by the Runtime.

---

# 66. Decision and Governance

Governance determines:

* who may decide;
* which Decisions require approval;
* which Decisions require multiple approvals;
* which Decisions require human intervention.

---

# 67. Human-in-the-Loop

Some Decision classes MAY require human approval.

Conceptually:

```text
AI Cognition
     ↓
Decision Proposal
     ↓
System Approval (internal)
     ↓
Authorization
     ↓
Human Approval (explicit, if required)
     ↓
Invocation
     ↓
Execution
```

> **Important:** The standard `propose → approve → authorize` flow in
> `propose_decision()` includes only *system approval* (internal acceptance).
> *Human approval* is a separate, explicit step recorded via
> `approve_decision()` and stored as an `ApprovalRecord`. For medium-risk
> operations, system approval is sufficient. For high/critical risks, an
> additional `ApprovalRecord` is required before invocation.

---

# 68. Multi-Approval Decisions

Critical Decisions MAY require multiple approvals.

Example:

```text
Operator Approval
        +
Supervisor Approval
        ↓
Authorized
```

---

# 69. Approval Records

Each approval SHOULD record:

```text
Actor
Role
Timestamp
Authority
Decision Version
```

---

# 70. Decision Quorum

Organizations MAY define quorum requirements.

The Decision API SHOULD support such requirements without hard-coding a universal quorum model.

---

# 71. Decision Voting

Some organizational processes MAY use voting.

Voting SHOULD remain a governance-level mechanism.

The resulting Decision SHOULD identify the applicable process.

---

# 72. Decision Safety

Safety-critical Decisions SHOULD have stronger validation.

Possible requirements:

```text
Context freshness
Policy validation
Human approval
Resource availability
Precondition verification
Execution confirmation
```

---

# 73. Decision Simulation

A Decision MAY be evaluated through simulation before authorization.

Conceptually:

```text
Decision
   ↓
Simulation
   ↓
Expected Outcome
```

Simulation results SHOULD be distinguishable from real-world results.

---

# 74. Decision Dry Run

The SDK MAY support dry-run evaluation.

```text
decision.evaluate(dry_run=true)
```

No real-world action should occur during a true dry run.

---

# 75. Decision Validation

Conceptual:

```text
decision.validate(decision_id)
```

Validation MAY check:

```text
Context validity
Authority
Policy
Constraints
Preconditions
Resource availability
Conflicts
Expiration
```

---

# 76. Decision Revalidation Before Execution

For consequential actions:

```text
Decision
   ↓
Revalidate
   ↓
Execute
```

This protects against stale organizational conditions.

---

# 77. Decision Execution Reference

After execution, the Decision SHOULD reference the resulting Invocation and resulting Execution.

```text
Decision
   ↓
INV-*
```

---

# 78. Decision Result

The Decision itself should not be confused with its result.

```text
Decision:
Reduce pump speed to 70%

Execution:
Command sent

Result:
Pump reached 70%
```

---

# 79. Decision Outcome Evaluation

After execution, the system MAY compare:

```text
Expected Outcome
vs
Actual Outcome
```

This supports organizational learning.

---

# 80. Decision Feedback

Execution results MAY become feedback for future Context and Cognition.

```text
Decision
   ↓
Execution
   ↓
Result
   ↓
Memory / State
   ↓
Future Context
```

---

# 81. Decision Learning

The Decision API SHOULD preserve sufficient provenance to allow later learning systems to evaluate Decision quality.

---

# 82. Decision Quality

Decision quality MAY be evaluated using:

```text
Correctness
Outcome
Risk
Policy Compliance
Efficiency
Timeliness
Robustness
```

---

# 83. Decision Metrics

The Runtime MAY expose:

```text
Decision Count
Approval Rate
Rejection Rate
Execution Success Rate
Decision Latency
Decision Failure Rate
Policy Violation Rate
Outcome Quality
```

---

# 84. Decision Audit

Consequential Decisions SHOULD be auditable.

The audit record SHOULD answer:

```text
What was decided?
Who decided?
For which Organization?
Using which Context?
Based on which evidence?
Under which authority?
When?
Was it approved?
Was it executed?
What happened?
```

The SDK SHOULD use the cross-API audit correlation defined by SDK-001 §24,
including `ORG-*`, `CTX-*`, `DEC-*` and `INV-*` identifiers and distinct
Authorization, Approval, Execution and Outcome records.

---

# 85. Decision Security

The Decision API MUST:

1. enforce Organization boundaries;
2. authenticate actors;
3. validate authority;
4. protect Decision information;
5. preserve Decision provenance;
6. preserve historical versions;
7. prevent unauthorized modification;
8. maintain auditability.

---

# 86. Decision Errors

Possible errors include:

```text
DECISION_NOT_FOUND
DECISION_UNAUTHORIZED
DECISION_INVALID
DECISION_EXPIRED
DECISION_STALE
DECISION_CONFLICT
DECISION_REQUIRES_APPROVAL
DECISION_POLICY_VIOLATION
DECISION_PRECONDITION_FAILED
DECISION_RESOURCE_UNAVAILABLE
DECISION_ALREADY_EXECUTED
```

---

# 87. Decision Concurrency

Concurrent Decision creation or modification SHOULD support conflict detection.

---

# 88. Optimistic Concurrency

Conceptual:

```text
decision.update(
    expected_version = 3
)
```

If the current version is 4, the Runtime MAY reject the update.

---

# 89. Decision Event Stream

Decision lifecycle changes MAY generate Events.

Examples:

```text
decision.created
decision.drafted
decision.pending
decision.authorized
decision.executing
decision.completed
decision.cancelled
decision.rejected
decision.failed
decision.revoked
```

ESCALATION is an event, not a Decision state:

```text
Decision
   ↓
ESCALATION event
   ↓
new authority / human review
```

An ESCALATION event routes the Decision toward additional authority or human review without changing the Decision's state to a distinct escalation state.

---

# 90. Decision Notifications

Applications MAY subscribe to Decision events.

Critical Decisions MAY require immediate notification according to organizational policy.

---

# 91. Decision Search

The SDK MAY support authorized Decision search.

Filters MAY include:

```text
organization
actor
resource
type
status
risk
date
objective
```

---

# 92. Decision Retention

Decision retention MUST follow organizational governance and applicable policies.

Consequential Decisions SHOULD normally remain traceable for the required retention period.

---

# 93. Decision Privacy

Decision records may contain sensitive organizational information.

Access MUST be limited according to authorization and data classification.

---

# 94. Decision Export

Authorized systems MAY export Decision records for:

* audits;
* reports;
* incident investigations;
* compliance;
* organizational learning.

---

# 95. Decision Interoperability

Decision representations SHOULD be serializable and transport-independent.

Possible formats include:

```text
JSON
MessagePack
Protocol Buffers
```

The conceptual model remains independent of transport.

---

# 96. Recommended Decision Object

Conceptually:

```text
Decision {
    id
    organization_id
    context_id
    context_version

    type
    objective
    outcome

    alternatives
    rationale
    evidence
    constraints
    preconditions
    postconditions

    actor
    authority

    confidence
    risk
    priority

    status
    version

    execution_refs
    supersedes
    superseded_by

    created_at
    updated_at
    expires_at
}
```

---

# 97. Recommended Operational Pattern

The preferred pattern is:

```text
1. Create Context
        ↓
2. Validate Context
        ↓
3. Cognition
        ↓
4. Create Decision Proposal
        ↓
5. Validate Authority
        ↓
6. Approve if required
        ↓
7. Revalidate
        ↓
8. Authorize
        ↓
9. Execute
        ↓
10. Evaluate Result
```

---

# 98. Conformance Requirements

An implementation conforming to SDK-005 MUST:

1. provide Decision identity;
2. associate Decisions with an Organization;
3. support Context references;
4. represent Decision outcomes;
5. represent Decision status;
6. support authority information;
7. preserve Decision provenance;
8. support validation;
9. distinguish Decision from Execution;
10. enforce organizational authorization;
11. preserve consequential Decision history;
12. support auditability.

---

# 99. Recommended Capabilities

A mature implementation SHOULD additionally provide:

* Decision versioning;
* approval workflows;
* multi-approval;
* quorum;
* Decision conflict detection;
* Decision simulation;
* dry runs;
* precondition evaluation;
* revalidation;
* Decision graphs;
* outcome evaluation;
* Decision quality metrics;
* event streaming.

---

# 100. Final Principles

### Principle 1 — Decision Is an Organizational Artifact

> A Decision is not merely a model output; it is a traceable organizational conclusion.

### Principle 2 — Decision Requires Context

> A consequential Decision must be grounded in an identifiable Context.

### Principle 3 — Decision Requires Authority

> The ability to reason does not imply the authority to decide or act.

### Principle 4 — Decision Is Not Execution

> A Decision defines what should happen; Execution defines what actually happens.

### Principle 5 — Decisions Must Be Traceable

> Important Decisions must preserve their origin, evidence, authority and outcome.

### Principle 6 — Decisions Can Become Stale

> A Decision remains valid only while its Context, authority and constraints remain applicable.

### Principle 7 — Governance Controls Consequential Decisions

> High-impact Decisions must follow organizational approval, safety and policy requirements.

---

# 101. Final Statement

The Decision API establishes the formal bridge between VIAL cognition and organizational action:

```text
             ORGANIZATION
                   │
                   ▼
                CONTEXT
                   │
                   ▼
              COGNITION
                   │
                   ▼
              ┌─────────┐
              │ DECISION│
              └────┬────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
      APPROVAL          REJECTION
          │
          ▼
     AUTHORIZATION
          │
          ▼
      EXECUTION
          │
          ▼
        RESULT
```

The Decision is therefore the point where organizational reasoning becomes an explicit commitment to a possible course of action.

> **A Decision is meaningful only when its Context, authority, constraints and consequences remain traceable.**

# End of SDK-005
