# RFC-006 — Decision & Authority Model

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Standards Track
**Depends On:** RFC-002, RFC-003, RFC-004, RFC-005, FCP-002A, FCP-007

---

# 1. Abstract

This document defines the VIAL model for **Organizational Decision and Authority**.

The purpose of this RFC is to establish how an Organization:

* determines who or what may decide;
* evaluates decision proposals;
* separates capability from authority;
* delegates decision rights;
* validates decisions;
* executes authorized decisions;
* records decision provenance;
* resolves authority conflicts;
* escalates decisions when necessary.

The central principle is:

> **The ability to perform an operation does not imply the authority to decide that the Organization should perform it.**

---

# 2. Motivation

Distributed Organizations may contain:

* AI models;
* software agents;
* humans;
* services;
* automated controllers;
* external systems;
* specialized Execution Resources.

Without explicit authority boundaries, any capable resource could potentially become an accidental decision-maker.

VIAL therefore separates:

```text
Capability
=
What a Resource can technically do.
```

```text
Authority
=
What a Resource is permitted to decide.
```

```text
Execution
=
What a Resource is permitted to perform.
```

These three concepts MUST NOT be silently conflated.

---

# 3. Scope

RFC-006 defines:

* Decision;
* Decision Proposal;
* Authority;
* Capability;
* Responsibility;
* Delegation;
* Decision Scope;
* Decision Constraints;
* Approval;
* Escalation;
* Decision Validity;
* Decision Provenance;
* Decision Conflicts.

This RFC does not define:

* authentication protocols;
* cryptographic identity;
* network authorization;
* specific IAM technologies;
* legal authority frameworks.

Those may be defined by implementation-specific or future governance specifications.

---

# 4. Core Principle

A VIAL Organization MUST distinguish:

```text
Can
```

from:

```text
May
```

and:

```text
Should
```

Therefore:

```text
Capability
     ↓
Can perform
```

```text
Authority
     ↓
May decide / act
```

```text
Policy
     ↓
Should / must act according to rules
```

---

# 5. Decision Definition

A Decision is an organizational determination that establishes what should happen, what should be maintained, or what action is authorized.

Conceptually:

```text
Decision =
Objective
+
Choice
+
Authority
+
Constraints
+
Evidence
+
Validity
```

A Decision MAY result in:

* State Transition;
* Execution;
* Delegation;
* Policy application;
* No immediate action.

---

# 6. Decision Proposal

A Decision Proposal is a suggested organizational choice that has not yet become authoritative.

Example:

```text
Proposal:
Reduce pump speed by 10%.
```

A proposal is not automatically a Decision.

The conceptual flow is:

```text
Observation
    ↓
Analysis
    ↓
Proposal
    ↓
Validation
    ↓
Authorization
    ↓
Decision
```

---

# 7. Decision vs Execution

A Decision establishes what should happen.

Execution performs the authorized operation.

```text
Decision
   ↓
Execution
```

An Execution Resource MUST NOT silently convert its own execution behavior into an organizational Decision unless explicitly authorized to do so.

---

# 8. Decision vs State

A Decision and State are distinct.

```text
Decision
=
What the Organization has decided.
```

```text
State
=
What the Organization currently considers to be true.
```

A Decision MAY cause a State Transition.

```text
Decision
   ↓
State Transition
   ↓
New State
```

---

# 9. Authority Definition

Authority is the organizational permission to make or approve a specific class of Decisions within a defined scope.

Authority SHOULD be defined by:

* subject;
* scope;
* operation;
* constraints;
* duration;
* delegation;
* escalation rules.

---

# 10. Authority Is Scoped

Authority SHOULD never be assumed to be unlimited.

Example:

```text
Resource A

May:
Inspect production data.

May:
Recommend maintenance.

May not:
Authorize production shutdown.
```

Authority must therefore be expressed in terms of permitted decision domains.

---

# 11. Capability vs Authority

An Execution Resource may technically possess a capability without possessing authority.

Example:

```text
Resource can:
STOP_MACHINE
```

does not imply:

```text
Resource may:
DECIDE_STOP_MACHINE
```

This distinction is fundamental to safe distributed operation.

---

# 12. Responsibility

Responsibility identifies the organizational role accountable for a Decision or operation.

Responsibility MAY belong to:

* human;
* agent;
* service;
* organizational role;
* governance body.

Responsibility and execution identity do not necessarily have to be identical.

---

# 13. Decision Authority Levels

VIAL MAY represent authority in levels.

A baseline model is:

```text
LEVEL 0
Observation

LEVEL 1
Recommendation

LEVEL 2
Operational Decision

LEVEL 3
Cross-Domain Decision

LEVEL 4
Strategic Decision

LEVEL 5
Exceptional / Human Authority
```

Implementations MAY define different levels.

---

# 14. Observation

Observation does not create authority.

An observer may report:

```text
Temperature = 92°C
```

without deciding:

```text
Stop production.
```

This maintains separation between sensing and deciding.

---

# 15. Recommendation

A Recommendation is a proposed course of action.

Example:

```text
Recommendation:
Inspect cooling system.
```

A recommendation MAY be generated by an Execution Resource without having authority to execute it.

---

# 16. Operational Decision

An Operational Decision authorizes an action within a defined operational domain.

Example:

```text
Decision:
Reduce pump speed to 80%.
```

The decision remains subject to applicable policy and constraints.

---

# 17. Cross-Domain Decision

Some decisions affect multiple organizational domains.

Example:

```text
Production
+
Maintenance
+
Financial
```

Cross-domain decisions SHOULD require authority covering all materially affected domains or explicit escalation.

---

# 18. Strategic Decision

Strategic Decisions affect long-term organizational direction.

Examples:

* organizational goals;
* major resource allocation;
* strategic policies;
* architecture decisions;
* major operational changes.

Such decisions SHOULD have stronger authority requirements.

---

# 19. Exceptional Decisions

Exceptional situations may require special authority.

Examples:

* safety emergency;
* catastrophic failure;
* unavailable decision-maker;
* conflicting authority;
* unknown system state.

Emergency mechanisms SHOULD be explicitly defined rather than inferred.

---

# 20. Decision Scope

Every significant Decision SHOULD define its scope.

Scope may include:

```text
Organization
Domain
Resource
Equipment
Location
Time
Operation
```

This prevents a decision from being interpreted more broadly than intended.

---

# 21. Decision Constraints

A Decision SHOULD include applicable constraints.

Examples:

```text
Maximum cost
Safety limits
Operating limits
Time limit
Resource limit
Policy requirement
```

Constraints are part of the Decision's semantic boundary.

---

# 22. Decision Preconditions

A Decision MAY have preconditions.

Example:

```text
If:
Pressure > 10 bar
AND
Pump = RUNNING
```

then:

```text
Decision:
Reduce pump speed.
```

If the preconditions are no longer satisfied, the Decision SHOULD be revalidated.

---

# 23. Decision Validity

A Decision MAY have:

```text
VALID
PENDING
EXPIRED
REVOKED
SUPERSEDED
INVALID
CONFLICTING
```

status.

Execution SHOULD respect Decision validity.

---

# 24. Decision Expiration

Some Decisions should automatically expire.

Examples:

```text
Temporary operating mode
Emergency authorization
Temporary resource allocation
Time-limited override
```

Expiration prevents stale authority from remaining active indefinitely.

---

# 25. Decision Revocation

An authorized Decision MAY be revoked.

Revocation SHOULD preserve:

* original Decision;
* revocation authority;
* reason;
* timestamp;
* resulting State effect.

---

# 26. Decision Supersession

A newer Decision MAY replace an older Decision.

Example:

```text
Decision D1
   ↓
Decision D2
   ↓
D1 superseded
```

The historical Decision SHOULD remain traceable when auditability requires it.

---

# 27. Delegation

Authority MAY be delegated.

Conceptually:

```text
Authority Holder
       ↓
Delegates
       ↓
Execution Resource
```

Delegation SHOULD specify:

* delegated scope;
* permitted operations;
* constraints;
* duration;
* revocation;
* escalation.

---

# 28. Delegation Cannot Exceed Authority

A Resource MUST NOT delegate authority that it does not itself possess.

```text
Authority(A) = X

Delegation(A → B)
≤ X
```

Delegation cannot expand organizational authority by itself.

---

# 29. Delegation Chain

Authority MAY pass through multiple layers.

Example:

```text
Organization
    ↓
Manager
    ↓
Supervisor
    ↓
Agent
```

The resulting authority SHOULD remain traceable to its original source.

---

# 30. Delegation Depth

Implementations SHOULD limit unnecessary delegation depth.

Deep chains increase:

* ambiguity;
* validation cost;
* audit complexity;
* revocation complexity.

---

# 31. Delegation Expiration

Delegations SHOULD support expiration.

Example:

```text
Agent authorized:
08:00 → 18:00
```

After expiration, the delegated authority is no longer valid unless renewed.

---

# 32. Decision Provenance

Important Decisions SHOULD preserve provenance.

Conceptually:

```text
Decision
   ↓
Authority
   ↓
Evidence
   ↓
Reasoning
   ↓
Context
   ↓
State
```

This allows the Organization to reconstruct why a Decision was made.

---

# 33. Decision Evidence

A Decision MAY reference Evidence.

For significant decisions, evidence SHOULD be sufficient to explain:

* what was observed;
* when it was observed;
* why it was relevant;
* how it influenced the decision.

Detailed evidence semantics belong to RFC-007.

---

# 34. Decision Context

A Decision SHOULD identify the relevant Context or Context lineage when necessary.

Example:

```text
Decision D42

Based on:
State v82
Policy v17
Evidence E92
Knowledge K44
```

This provides a reproducible decision boundary.

---

# 35. Decision Reasoning

The reasoning behind a Decision MAY be:

* deterministic;
* rule-based;
* model-generated;
* human;
* hybrid.

VIAL does not require AI reasoning for every Decision.

---

# 36. Deterministic Decisions

Where a Decision can be reliably determined by rules or calculations, deterministic mechanisms SHOULD be preferred.

Example:

```text
If pressure > safety_limit:
    initiate emergency procedure
```

No language model is required.

This supports VIAL's efficiency objective.

---

# 37. AI-Assisted Decisions

AI MAY support:

* interpretation;
* planning;
* anomaly analysis;
* recommendation;
* synthesis.

AI-generated reasoning does not automatically confer authority.

The authority remains an organizational property.

---

# 38. Human Decisions

Humans MAY be authoritative decision-makers.

A human Decision SHOULD follow the same organizational concepts:

* scope;
* authority;
* evidence;
* validity;
* provenance.

VIAL is not limited to machine-only organizations.

---

# 39. Hybrid Decisions

A Decision MAY involve multiple participants.

Example:

```text
Sensor
 ↓
AI Analysis
 ↓
Human Approval
 ↓
Execution
```

The final authority should remain identifiable.

---

# 40. Decision Confidence

A Decision MAY have a confidence or support value.

However:

```text
Confidence
≠
Authority
```

A highly confident recommendation does not become authorized merely because confidence is high.

---

# 41. Decision Risk

A Decision SHOULD be evaluated according to potential impact.

A simple conceptual model is:

```text
Decision Risk
=
Impact
×
Uncertainty
```

Implementations MAY use more sophisticated models.

Higher-risk Decisions SHOULD require stronger validation or authority.

---

# 42. Risk-Based Escalation

The Organization SHOULD escalate Decisions when risk exceeds the authority of the current resource.

```text
Low Risk
   ↓
Local Decision

Medium Risk
   ↓
Additional Validation

High Risk
   ↓
Higher Authority

Critical Risk
   ↓
Human / Exceptional Authority
```

---

# 43. Decision Escalation

Escalation MAY occur because:

* authority is insufficient;
* evidence is insufficient;
* confidence is low;
* risk is high;
* State is conflicting;
* policy requires approval;
* required resource is unavailable.

---

# 44. Escalation Should Preserve Work

When escalating, the system SHOULD preserve already completed analysis.

```text
Resource A
   ↓
Analysis
   ↓
Proposal
   ↓
Escalation
   ↓
Resource B
```

Resource B should not necessarily restart the entire reasoning process.

This directly supports cognitive efficiency.

---

# 45. Decision Approval

Some Decisions require explicit approval.

Approval SHOULD identify:

```text
Approver
Decision
Scope
Timestamp
Authority
Conditions
```

---

# 46. Multi-Party Approval

Critical Decisions MAY require multiple approvals.

Example:

```text
Engineering Approval
+
Operations Approval
+
Safety Approval
```

The Decision becomes valid only when the required approval conditions are satisfied.

---

# 47. Quorum

For certain organizational structures, Decisions MAY require a quorum.

The quorum rule SHOULD be explicit.

Example:

```text
3 of 5 authorized participants
```

The protocol does not mandate a particular quorum algorithm.

---

# 48. Conflicting Authority

Conflicting authority occurs when two valid authority sources produce incompatible Decisions.

Example:

```text
Authority A:
Continue operation.

Authority B:
Stop operation.
```

The Organization MUST have a defined conflict-resolution mechanism.

---

# 49. Authority Priority

Priority MAY be determined by:

* organizational hierarchy;
* policy;
* safety;
* domain;
* temporal precedence;
* explicit override.

The mechanism MUST be explicit.

---

# 50. Safety Override

Safety-critical policy MAY override ordinary operational authority.

Example:

```text
Normal operation:
Agent may continue production.

Safety condition:
Emergency shutdown required.
```

The safety mechanism may supersede normal operation when explicitly defined by organizational policy.

---

# 51. No Implicit Override

A Resource MUST NOT assume that it can override another authority merely because it believes its decision is better.

Overrides MUST have an explicit organizational basis.

---

# 52. Decision Conflict Resolution

A conflict MAY follow:

```text
Conflict Detected
       ↓
Identify Authorities
       ↓
Identify Scope
       ↓
Evaluate Policy
       ↓
Evaluate Risk
       ↓
Apply Priority
       ↓
Resolve / Escalate
```

---

# 53. Decision Atomicity

Where a Decision produces a State Transition, the Decision and resulting transition SHOULD have a traceable relationship.

The system should avoid:

```text
Decision exists
but
State change cannot be explained.
```

---

# 54. Decision Idempotency

Repeated processing of the same Decision SHOULD NOT unintentionally create duplicate effects.

Decision identifiers SHOULD be used where necessary.

---

# 55. Decision and Execution

Execution SHOULD verify the Decision before acting.

Conceptually:

```text
Decision
   ↓
Verify:
Authority
Scope
Validity
Constraints
Preconditions
   ↓
Execute
```

---

# 56. Execution Cannot Expand Decision Scope

If a Decision authorizes:

```text
Change pump speed.
```

the Execution Resource MUST NOT interpret it as:

```text
Modify production policy.
```

Execution must remain within Decision scope.

---

# 57. Decision Completion

After execution, the system SHOULD record the outcome.

Example:

```text
Decision:
Reduce pump speed.

Execution:
Completed.

Result:
Speed = 80%.
```

The outcome MAY update State and Memory.

---

# 58. Decision Failure

If execution fails:

```text
Decision
   ↓
Execution
   ↓
Failure
```

the Decision should not automatically be treated as successfully completed.

The system SHOULD record:

* failure;
* reason;
* resulting State;
* retry status;
* escalation if necessary.

---

# 59. Decision Retry

Retries SHOULD respect the original Decision validity.

A Decision that has expired or been superseded MUST NOT be blindly retried.

---

# 60. Decision Cancellation

A pending Decision MAY be cancelled by an authorized authority.

Cancellation SHOULD preserve provenance.

---

# 61. Decision Audit

Significant Decisions SHOULD be auditable.

At minimum:

```text
Decision ID
Authority
Scope
Context Reference
Evidence Reference
Decision Time
Validity
Outcome
```

---

# 62. Decision Reproducibility

A Decision does not necessarily need to produce exactly the same reasoning output again.

However, the Organization SHOULD be able to reconstruct:

* available State;
* relevant Context;
* Evidence;
* Authority;
* Policy;
* Decision;
* resulting action.

---

# 63. Decision Transparency

Transparency should be proportional to decision importance.

Low-risk deterministic Decisions may require minimal records.

High-risk Decisions SHOULD preserve richer provenance.

---

# 64. Decision Cost

Decision-making itself has a cost.

Costs may include:

* inference;
* retrieval;
* human review;
* coordination;
* latency;
* execution;
* opportunity cost.

VIAL encourages proportional decision processes.

---

# 65. Proportionality

The decision mechanism SHOULD match the importance of the Decision.

```text
Simple Decision
→ Simple validation

Complex Decision
→ More context

High-Risk Decision
→ Stronger authority

Critical Decision
→ Strongest governance
```

This avoids unnecessary organizational bureaucracy.

---

# 66. Decision Locality

Decisions SHOULD be made as close as practical to the domain where the required knowledge exists.

However, local autonomy MUST remain within delegated authority.

```text
Local Knowledge
+
Local Authority
=
Efficient Local Decision
```

---

# 67. Centralization vs Distribution

VIAL does not require centralized decision-making.

An Organization MAY distribute authority.

The important requirement is:

> Distributed authority must remain explicit and auditable.

---

# 68. Decision Independence

Independent Decisions MAY be made concurrently.

The Organization SHOULD detect when apparently independent Decisions affect the same State domain.

---

# 69. Decision Dependency

Some Decisions depend on previous Decisions.

Example:

```text
Decision A
   ↓
Decision B
   ↓
Decision C
```

Dependencies SHOULD be represented when they affect validity.

---

# 70. Decision Preconditions and State

A Decision may depend on a particular State version.

Example:

```text
Decision D1
Based on State v50
```

If State becomes v54 before execution, the Decision MAY require revalidation.

---

# 71. Stale Decisions

A Decision becomes stale when its assumptions no longer represent the organizational reality required for execution.

Possible causes:

* State change;
* policy change;
* evidence invalidation;
* authority expiration;
* environmental change.

---

# 72. Decision Revalidation

Before executing a high-impact Decision, the system SHOULD verify:

```text
Authority
State
Policy
Preconditions
Evidence
Validity
```

---

# 73. Decision Memory

Important Decisions SHOULD be persisted according to RFC-005.

This creates organizational continuity:

```text
Decision
   ↓
Memory
   ↓
Future Context
   ↓
Future Decision
```

---

# 74. Decision and Organizational Learning

The Organization SHOULD evaluate significant Decisions after execution.

Questions may include:

```text
Was the decision correct?
Was the outcome expected?
Was the evidence sufficient?
Should the procedure change?
Should new knowledge be stored?
```

This creates feedback into Memory.

---

# 75. Decision Lifecycle

A Decision MAY follow:

```text
PROPOSED
   ↓
VALIDATING
   ↓
AUTHORIZED
   ↓
ACTIVE
   ↓
EXECUTED
   ↓
COMPLETED
```

Alternative paths include:

```text
REJECTED
EXPIRED
REVOKED
SUPERSEDED
CANCELLED
FAILED
ESCALATED
```

---

# 76. Decision State Machine

Conceptually:

```text
                 ┌──────────────┐
                 │   PROPOSED   │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │  VALIDATING  │
                 └──────┬───────┘
                        ↓
              ┌─────────┴─────────┐
              ↓                   ↓
        ┌───────────┐       ┌──────────┐
        │ AUTHORIZED│       │ REJECTED │
        └─────┬─────┘       └──────────┘
              ↓
        ┌───────────┐
        │  ACTIVE   │
        └─────┬─────┘
              ↓
        ┌───────────┐
        │ EXECUTED  │
        └─────┬─────┘
              ↓
        ┌───────────┐
        │ COMPLETED │
        └───────────┘
```

---

# 77. Minimal Decision Contract

At minimum, a significant Decision SHOULD identify:

```text
Decision ID
Organization
Decision
Authority
Scope
Validity
```

Where applicable:

```text
Evidence
Context
Preconditions
Constraints
Outcome
```

---

# 78. Authority Contract

A minimal Authority representation SHOULD identify:

```text
Authority Holder
Scope
Permitted Decision Type
Constraints
Validity
Delegation Source
```

---

# 79. Delegation Contract

A delegation SHOULD identify:

```text
Delegator
Delegate
Scope
Permissions
Constraints
Start
Expiration
Revocation
```

---

# 80. Conformance Requirements

A VIAL implementation conforming to RFC-006 MUST:

1. distinguish Capability from Authority;
2. distinguish Decision from Execution;
3. distinguish Decision from State;
4. represent authority scope;
5. prevent unauthorized significant Decisions;
6. support Decision validity;
7. preserve provenance for significant Decisions;
8. prevent execution outside Decision scope;
9. detect or prevent conflicting authority where required;
10. support escalation when authority is insufficient.

---

# 81. Recommended Capabilities

A conforming implementation SHOULD additionally support:

* delegation;
* expiration;
* revocation;
* decision versioning;
* risk-based escalation;
* multi-party approval;
* decision dependencies;
* decision replay;
* decision audit;
* outcome evaluation;
* decision memory;
* authority conflict resolution.

---

# 82. Non-Goals

RFC-006 does not define:

* a specific authentication mechanism;
* a specific IAM system;
* a specific cryptographic protocol;
* legal authority;
* employment hierarchy;
* a mandatory governance structure.

It defines the semantic model required for VIAL organizational decision-making.

---

# 83. Relationship With RFC-003

RFC-003 defines how State changes.

RFC-006 defines who or what may authorize those changes.

```text
RFC-006
Decision + Authority
       ↓
RFC-003
Authorized State Transition
       ↓
New State
```

---

# 84. Relationship With RFC-004

RFC-004 determines how much Context is required for cognition.

RFC-006 determines what authority is required for the resulting Decision.

```text
Context
   ↓
Reasoning
   ↓
Proposal
   ↓
Authority Validation
   ↓
Decision
```

---

# 85. Relationship With RFC-005

RFC-005 preserves important organizational knowledge.

RFC-006 creates Decision Memory for significant organizational choices.

```text
Decision
   ↓
Outcome
   ↓
Memory
   ↓
Future Decision
```

---

# 86. Relationship With FCP-002A

FCP-002A defines the organizational cognition model.

RFC-006 establishes the authority boundary within which distributed cognition may produce organizational Decisions.

The Organization can therefore distribute cognition without distributing authority indiscriminately.

---

# 87. Distributed Authority Model

The VIAL model can be summarized as:

```text
                  ORGANIZATION
                       │
                AUTHORITY MODEL
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       HUMAN         AGENT       SERVICE
          │            │            │
          └────────────┼────────────┘
                       ↓
                  DECISION
                       ↓
                  VALIDATION
                       ↓
                   EXECUTION
                       ↓
                 STATE CHANGE
                       ↓
                    MEMORY
```

---

# 88. Fundamental Safety Boundary

The most important boundary in RFC-006 is:

```text
CAPABILITY
    ≠
AUTHORITY
```

A system may be technically capable of doing something without being organizationally permitted to do it.

---

# 89. Fundamental Efficiency Boundary

The second important boundary is:

```text
ANALYSIS
    ≠
DECISION
```

Not every analysis needs to become an organizational decision.

Likewise:

```text
DECISION
    ≠
EXECUTION
```

Separating these stages allows VIAL to use the least expensive appropriate resource at each stage.

---

# 90. Fundamental Governance Boundary

The Organization should know:

```text
Who decided?
Why?
Based on what?
With what authority?
Within what scope?
What happened afterward?
```

This is the minimum foundation for auditable distributed cognition.

---

# 91. Final Decision Architecture

```text
                 OBSERVATION
                      ↓
                  ANALYSIS
                      ↓
                RECOMMENDATION
                      ↓
             AUTHORITY EVALUATION
                      ↓
              DECISION PROPOSAL
                      ↓
               VALIDATION
                      ↓
             AUTHORIZED DECISION
                      ↓
                  EXECUTION
                      ↓
                STATE CHANGE
                      ↓
                 OUTCOME
                      ↓
              MEMORY / LEARNING
```

---

# 92. Final Principles

### Principle 1 — Authority

> Capability does not create authority.

### Principle 2 — Scope

> Every significant Decision must have a defined scope.

### Principle 3 — Proportionality

> Decision complexity should match Decision importance.

### Principle 4 — Escalation

> Uncertainty or insufficient authority should trigger escalation rather than unauthorized action.

### Principle 5 — Continuity

> Important Decisions should survive the replacement of individual Execution Resources.

### Principle 6 — Auditability

> Significant Decisions should be reconstructable.

### Principle 7 — Efficiency

> Decisions should use the least expensive mechanism capable of producing a sufficiently reliable result.

### Principle 8 — Separation

> Observation, analysis, decision and execution are distinct organizational functions.

---

# 93. Final Statement

VIAL does not attempt to create an Organization in which every intelligent resource can decide everything.

It creates an Organization in which intelligence can be distributed while authority remains controlled.

The fundamental principle is:

> **Distribute cognition without losing governance.**

Therefore:

```text
Many Resources
      ↓
Distributed Cognition
      ↓
Explicit Authority
      ↓
Controlled Decisions
      ↓
Traceable Execution
      ↓
Persistent Organizational Learning
```

The objective is:

> **Maximum organizational autonomy with minimum ambiguity about who or what is authorized to decide.**

# End of RFC-006
