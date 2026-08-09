# RUNTIME-002 — VIAL Execution Cycle

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Runtime Specification
Depends On:
- RUNTIME-001
- RFC-003
- RFC-004
- RFC-005
- RFC-006

---

# 1. Abstract

This document defines the canonical execution cycle of the VIAL Runtime.

The Execution Cycle describes how an Organization transforms an event or organizational need into:

* Context;
* Cognition;
* Decision;
* Authorization / Approval;
* Invocation / Execution;
* Outcome;
* State transition;
* Organizational learning.

The cycle is designed to preserve three fundamental properties:

```text
Efficiency
Auditability
Organizational Continuity
```

---

# 2. Fundamental Cycle

The canonical VIAL Execution Cycle is:

```text
EVENT
  ↓
STATE
  ↓
CONTEXT
  ↓
COGNITION
  ↓
PROPOSAL
  ↓
DECISION
  ↓
AUTHORITY
  ↓
AUTHORIZATION
  ↓
APPROVAL
  ↓
INVOCATION
  ↓
EXECUTION
  ↓
OUTCOME
  ↓
STATE UPDATE
  ↓
MEMORY UPDATE
  ↓
CYCLE COMPLETE
```

The cycle MAY terminate earlier when no Decision or Execution is required.

---

# 3. Cycle Identity

Every execution cycle SHOULD have a unique identifier.

Example:

```text
Cycle ID: CYCLE-*
```

The Cycle ID SHOULD remain associated with all significant artifacts produced during the cycle.

---

# 4. Cycle Artifacts

A cycle MAY generate:

```text
Event
State Snapshot
Context
Cognition Result
Proposal
Decision
Authority Evaluation
Execution
Result
State Transition
Memory Record
Audit Record
```

These artifacts SHOULD be traceable to the same Cycle ID.

Where entity identifiers are recorded, the Runtime MUST use the canonical
patterns:

```text
Organization ORG-*
Resource     RES-*
Context      CTX-*
Decision     DEC-*
Invocation   INV-*
```

---

# 5. Stage 1 — Event Reception

The cycle begins when the Runtime receives a trigger.

Possible triggers:

* external event;
* State change;
* scheduled task;
* human request;
* sensor observation;
* Tool result;
* another VIAL Organization;
* internal Runtime condition.

---

# 6. Event Normalization

The Runtime SHOULD normalize incoming events before processing.

A normalized Event SHOULD contain:

```text
Event ID
Source
Timestamp
Type
Payload
Scope
Priority
Correlation ID
```

---

# 7. Event Validation

The Runtime SHOULD validate:

* event structure;
* source;
* integrity;
* scope;
* timestamp;
* required metadata.

Invalid events SHOULD NOT silently enter the organizational cycle.

---

# 8. Stage 2 — State Acquisition

After receiving an Event, the Runtime determines the relevant organizational State.

Conceptually:

```text
Event
 ↓
Relevant State
```

The Runtime SHOULD obtain a consistent State snapshot.

---

# 9. State Version

The cycle SHOULD record the State version used.

Example:

```text
State Version: S-1042
```

This allows later reconstruction of the decision context.

---

# 10. State Freshness

The Runtime SHOULD determine whether State freshness is sufficient for the current task.

Low-risk operations MAY tolerate older State.

High-impact operations SHOULD require sufficiently current State.

---

# 11. Stage 3 — Objective Identification

The Runtime determines what organizational objective is associated with the cycle.

The objective MAY originate from:

* Event;
* policy;
* human request;
* active Decision;
* scheduled operation.

The objective should remain explicit.

---

# 12. Stage 4 — Context Construction

The Context Engine creates the minimum sufficient Context.

Conceptually:

```text
State
+
Objective
+
Relevant Memory
+
Policies
+
Evidence
+
Event
      ↓
Context
```

---

# 13. Minimum Sufficient Context

The Runtime SHOULD avoid loading information that does not contribute materially to the current Decision.

This principle exists to reduce:

* computation;
* inference;
* latency;
* memory usage;
* unnecessary data transfer.

---

# 14. Context Validation

Before Cognition begins, the Runtime SHOULD validate:

```text
Context completeness
Context freshness
Context scope
Policy availability
Required evidence
```

If Context is insufficient, the cycle MAY:

* retrieve additional information;
* request clarification;
* escalate;
* terminate.

For consequential evaluation or execution, the Runtime SHOULD freeze the Context before proceeding beyond validation. Once FROZEN, the normative content of the Context MUST NOT change; later changes require a new Context.

The Context lifecycle used by this cycle is:

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

The Runtime MUST recognize `FROZEN`. After `FROZEN`, the normative content
MUST NOT be changed. `EXPIRED` MAY be recorded as a validity condition without
creating a competing Context lifecycle.

---

# 15. Stage 5 — Memory Retrieval

The Runtime retrieves relevant Memory.

Memory retrieval SHOULD be:

* relevance-based;
* scope-aware;
* validity-aware;
* cost-aware.

The Runtime SHOULD prefer validated organizational knowledge over repeatedly rediscovering the same information.

---

# 16. Memory Failure

If Memory is unavailable, the Runtime SHOULD explicitly represent the condition.

It MUST NOT silently fabricate Memory.

Possible responses:

```text
Continue without Memory
Retry
Use alternative source
Escalate
Terminate
```

depending on task requirements.

---

# 17. Stage 6 — Cognition Selection

The Runtime determines which Resource should perform Cognition.

The selection MAY consider:

```text
Capability
Cost
Latency
Reliability
Availability
Risk
Authority
Specialization
```

---

# 18. Cognitive Routing

The preferred routing strategy is:

```text
Can a deterministic mechanism solve it?
        │
       YES
        ↓
Deterministic Resource

       NO
        ↓

Can a specialized Resource solve it?
        │
       YES
        ↓
Specialized Resource

       NO
        ↓

General Cognition
```

This prevents unnecessary use of expensive reasoning resources.

---

# 19. Stage 7 — Cognition

The selected Resource analyzes the Context.

The output MAY be:

* answer;
* recommendation;
* plan;
* Decision proposal;
* request for more information;
* escalation.

Cognition does not automatically create authority.

---

# 20. Cognition Result

The Runtime SHOULD record:

```text
Resource
Resource Version
Input Context Reference
Output
Timestamp
Cost
Latency
Confidence, if applicable
```

---

# 21. Stage 8 — Proposal

If Cognition recommends an action, the Runtime creates a Proposal.

Example:

```text
Proposal:
Reduce pump speed to 80%.
```

A Proposal is not yet an authorized organizational Decision.

---

# 22. Proposal Validation

The Runtime SHOULD validate:

* objective alignment;
* scope;
* required parameters;
* preconditions;
* constraints;
* risk.

Invalid Proposals SHOULD be rejected or returned for revision.

---

# 23. Stage 9 — Decision Formation

A validated Proposal MAY become a Decision.

The Decision MUST use the canonical lifecycle:

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

Alternative or terminal states are `CANCELLED`, `REJECTED`, `FAILED` and
`REVOKED`. A Decision in `PENDING` is not authorized and MUST NOT create an
Invocation or produce an external effect.

A Decision SHOULD identify:

```text
DEC-*
Cycle ID
Decision Type
Scope
Action
Constraints
Validity
Authority Requirement
CTX-*
```

---

# 24. Stage 10 — Authority Evaluation

The Authority Engine evaluates the Decision according to RFC-006.

Conceptually:

```text
Decision
   ↓
Identity + Authority + Policy + Context + Scope
   ↓
Authorization Evaluation
   ├── Authorization
   │      ↓
   │   Approval (when required)
   ├── Rejected
   └── ESCALATION event
```

The Authority Engine evaluates the authorization boundary; it does not
replace or mutate the Decision into an authorization object.

---

# 25. Events and States

Decision lifecycle states are persistent conditions:

```text
DRAFT
PENDING
AUTHORIZED
EXECUTING
COMPLETED
CANCELLED
REJECTED
FAILED
REVOKED
```

The following are Runtime events or process transitions, not Decision states:

```text
ESCALATION
AUTHORIZATION_GRANTED
AUTHORIZATION_REVOKED
INVOCATION_CREATED
EXECUTION_STARTED
EXECUTION_COMPLETED
```

An `ESCALATION` event leads to additional authority or review and then to
`AUTHORIZED` or `REJECTED`. It MUST NOT be added to the Decision state set.

---

# 26. Authorized Decision

If authority is sufficient:

```text
Decision
   ↓
AUTHORIZED
```

The Runtime MAY proceed toward Invocation and Execution.

---

# 27. Rejected Decision

If authority is insufficient and no escalation mechanism applies:

```text
Decision
   ↓
REJECTED
   ↓
Cycle Complete
```

No external effect SHOULD occur.

---

# 28. Escalation Event

If additional authority is required, the Runtime SHOULD raise an ESCALATION event:

```text
Decision
   ↓
ESCALATION event
   ↓
Higher Authority
   ↓
AUTHORIZED / REJECTED
```

ESCALATION is an event or transition, not a Decision state. The Decision remains in its current lifecycle state while awaiting the additional authority.

The original analysis SHOULD be preserved.

---

# 29. Stage 11 — Pre-Execution Validation

Immediately before execution, the Runtime SHOULD verify:

```text
Decision validity
Authority
Scope
State
Preconditions
Constraints
Target
Tool existence
Tool lifecycle eligibility
Tool Contract
Invocation identity
```

This is necessary because organizational conditions may have changed after the Decision was created.

The Runtime MUST NOT create an Invocation or execute a Tool whose lifecycle state does not permit normal invocation. In particular, `DRAFT`, `DEFINED`, `DEPRECATED` and `RETIRED` Tools MUST NOT be used for normal execution; only an `ACTIVE` Tool is eligible, subject to Authorization, Approval when required, Contract and scope.

---

# 30. State Revalidation

For high-impact operations:

```text
Decision created
       ↓
State changed
       ↓
Revalidate Decision
```

A stale Decision SHOULD NOT automatically execute.

---

# 31. Decision Validity Expiration

If the Decision validity period has expired:

```text
Decision
   ↓
EXPIRED
```

`EXPIRED` is a validity condition, not a Decision lifecycle state. The Runtime
MUST NOT execute the Decision unless a new valid Decision is created.

---

# 32. Decision Revocation

If a Decision has been revoked:

```text
Decision
   ↓
REVOKED
```

Execution MUST NOT proceed.

---

# 33. Stage 12 — Invocation and Execution

The Runtime creates an Invocation and dispatches the authorized Decision to the
appropriate Resource.

```text
Authorized Decision
       ↓
   Invocation
       ↓
    Resource
       ↓
External Effect
```

---

# 34. Invocation Identity

Each Invocation SHOULD have a unique identifier.

Example:

```text
Invocation ID: INV-92831
```

The Invocation ID SHOULD be associated with:

* Decision;
* Cycle;
* Resource;
* Outcome.

---

# 35. Execution Boundary

Execution is the boundary where VIAL can produce effects outside its internal cognitive process.

Examples:

```text
Write database
Send command
Control machine
Send message
Create document
Call external service
```

This boundary SHOULD receive stronger validation than ordinary internal computation.

---

# 36. Idempotent Execution

Where possible, Execution SHOULD be idempotent.

If a command is retried:

```text
Retry
 ↓
Same intended effect
```

rather than:

```text
Retry
 ↓
Duplicate effect
```

---

# 37. Stage 13 — Result Collection

After Execution, the Runtime records the Result.

Possible Results:

```text
SUCCESS
PARTIAL_SUCCESS
FAILED
TIMEOUT
CANCELLED
REJECTED
UNKNOWN
```

---

# 38. Unknown Result

The Runtime MUST distinguish:

```text
FAILED
```

from:

```text
UNKNOWN
```

Example:

```text
Command sent
Connection lost
No confirmation
```

The correct status is:

```text
UNKNOWN
```

until evidence establishes the actual result.

---

# 39. Stage 14 — State Transition

If Execution changes organizational State, the Runtime applies an authorized State Transition.

```text
Old State
   ↓
Authorized Transition
   ↓
New State
```

The transition SHOULD reference:

```text
Decision ID
Invocation ID
Cycle ID
```

---

# 40. State Conflict

If the State changed unexpectedly before transition:

```text
Expected State
     ≠
Current State
```

the Runtime SHOULD prevent unsafe mutation.

Possible responses:

* retry;
* revalidate;
* recompute;
* escalate;
* reject.

---

# 41. Stage 15 — Memory Update

The Runtime determines whether the cycle produced information worth retaining.

Possible Memory candidates:

* important Decision;
* operational outcome;
* discovered knowledge;
* failure;
* successful procedure;
* organizational learning.

Not every event should become Memory.

---

# 42. Memory Admission

Memory admission SHOULD evaluate:

```text
Relevance
Durability
Reliability
Future Utility
Cost
```

This prevents uncontrolled Memory growth.

---

# 43. Stage 16 — Outcome Evaluation

The Runtime SHOULD determine whether the outcome matched the intended result.

Example:

```text
Expected:
Temperature < 80°C

Actual:
Temperature = 76°C

Outcome:
Successful
```

This provides feedback for future cognition.

---

# 44. Stage 17 — Audit

The Runtime records the cycle's significant events.

A complete trace SHOULD permit reconstruction of:

```text
Trigger
State
Context
Cognition
Decision
Authority
Execution
Result
State Transition
Memory
```

---

# 45. Stage 18 — Cycle Completion

The cycle becomes complete when:

* required execution has finished;
* State transitions are resolved;
* required Memory updates are processed;
* audit information is preserved.

Example:

```text
CYCLE_COMPLETED
```

---

# 46. Cycle Termination Without Execution

Not every cycle requires execution.

Example:

```text
Event
 ↓
Analysis
 ↓
Conclusion:
No action required
 ↓
Memory / Audit
 ↓
Complete
```

This is a valid VIAL cycle.

---

# 47. Cycle Termination Without Decision

Some events may simply update State.

Example:

```text
Sensor Event
 ↓
State Update
 ↓
Cycle Complete
```

No Cognition or Decision is required.

---

# 48. Cycle Escalation

A cycle MAY raise an ESCALATION event when additional authority or review is required.

```text
RUNNING
   ↓
WAITING   (during escalation)
   ↓
RESUMED
```

ESCALATION is an event or transition, not a cycle state (ADR-0006 D-002, D-009).

The original Cycle ID SHOULD remain unchanged.

---

# 49. Cycle Pause

A cycle MAY be paused because:

* external approval is required;
* information is missing;
* resource unavailable;
* external dependency;
* human intervention.

Paused cycles SHOULD preserve their current state.

---

# 50. Cycle Cancellation

A cycle MAY be cancelled.

Cancellation SHOULD preserve:

```text
Reason
Authority
Timestamp
Current Stage
```

---

# 51. Cycle Failure

A cycle SHOULD explicitly identify its failure stage.

Example:

```text
Cycle
 ↓
Context
 ↓
Failure
```

is different from:

```text
Cycle
 ↓
Execution
 ↓
Failure
```

This distinction is important for diagnosis and learning.

---

# 52. Retry

Retries SHOULD resume from the earliest safe stage rather than automatically repeating the entire cycle.

Example:

```text
Memory retrieval failed
        ↓
Retry Memory
```

instead of:

```text
Restart entire organization cycle
```

This reduces resource consumption.

---

# 53. Recovery

A failed cycle MAY enter:

```text
RECOVERY
```

The Recovery Manager SHOULD determine whether to:

* retry;
* compensate;
* resume;
* escalate;
* terminate.

---

# 54. Cycle Cost

The Runtime SHOULD measure cost at each stage.

```text
Event Cost
State Cost
Context Cost
Memory Cost
Cognition Cost
Decision Cost
Execution Cost
```

This enables optimization of the complete organizational process.

---

# 55. Cognitive Cost Optimization

If a cycle repeatedly produces the same result, the Runtime SHOULD consider whether the behavior can be converted into:

* deterministic logic;
* cached knowledge;
* reusable procedure;
* specialized Resource.

This is a key VIAL optimization mechanism.

---

# 56. Context Reuse

When appropriate, Context MAY be reused.

However, reuse MUST verify that:

* State has not invalidated it;
* permissions remain valid;
* evidence remains current;
* assumptions remain valid.

---

# 57. Decision Reuse

A previous Decision MUST NOT automatically be reused simply because a similar Event occurs.

The Runtime SHOULD determine whether the prior Decision is:

* reusable;
* still valid;
* within scope;
* applicable to the current State.

---

# 58. Organizational Learning

The cycle creates a feedback loop:

```text
Execution
   ↓
Result
   ↓
Evaluation
   ↓
Memory
   ↓
Future Context
   ↓
Future Cognition
```

This transforms repeated operation into organizational learning.

---

# 59. Canonical Cycle Example

Consider:

```text
Event:
Pump pressure exceeds limit.
```

Runtime:

```text
1. Receive Event
2. Load current State
3. Retrieve safety policy
4. Retrieve previous incidents
5. Build Context
6. Select deterministic safety rule
7. Generate shutdown proposal
8. Create Decision
9. Validate Authority
10. Execute shutdown
11. Receive result
12. Update equipment State
13. Record incident
14. Store relevant Memory
15. Complete cycle
```

---

# 60. Example Without AI

The entire cycle MAY be deterministic:

```text
Sensor
 ↓
Rule
 ↓
Decision
 ↓
Authority
 ↓
Command
 ↓
Result
```

No AI model is necessary.

This is intentional.

---

# 61. Example With AI

A more complex situation MAY use AI:

```text
Event
 ↓
State
 ↓
Memory
 ↓
Context
 ↓
AI Analysis
 ↓
Proposal
 ↓
Authority
 ↓
Human Approval
 ↓
Execution
 ↓
Result
```

The Runtime remains the same.

Only the Cognition Resource changes.

---

# 62. Example With Human Cognition

A human may be the Cognition Resource:

```text
Event
 ↓
Context
 ↓
Human Analysis
 ↓
Decision
 ↓
Authority
 ↓
Execution
```

The Runtime does not require artificial cognition.

---

# 63. Multi-Resource Cognition

Multiple Resources MAY participate:

```text
Sensor
   ↓
Analyzer
   ↓
AI
   ↓
Human
   ↓
Decision
```

The Runtime SHOULD preserve the provenance of each contribution.

---

# 64. Parallel Cognition

Independent analyses MAY run in parallel.

```text
          Context
             │
       ┌─────┼─────┐
       ↓     ↓     ↓
      AI    Rule  Expert
       └─────┼─────┘
             ↓
          Synthesis
```

The synthesis stage SHOULD preserve the sources.

---

# 65. Parallel Execution

Independent authorized executions MAY run concurrently.

The Runtime MUST verify that concurrent effects do not violate State or authority constraints.

---

# 66. Cycle Determinism

The Runtime SHOULD keep deterministic orchestration wherever possible.

Probabilistic behavior should remain localized to Cognition Resources rather than becoming implicit Runtime behavior.

---

# 67. Cycle Contract

A conceptual Cycle Contract is:

```text
Cycle {
    id
    trigger
    state
    context
    cognition
    proposal
    decision
    authority
    execution
    result
    state_transition
    memory
    audit
    status
}
```

This is a semantic model, not a required programming-language structure.

---

# 68. Cycle Status

A Cycle MAY have:

```text
CREATED
RUNNING
WAITING
COMPLETED
FAILED
CANCELLED
RECOVERING
```

ESCALATION is an event or transition, not a Cycle status (ADR-0006 D-009).

---

# 69. Conformance

A Runtime conforming to RUNTIME-002 MUST:

1. provide a traceable execution cycle;
2. separate Context from State;
3. separate Cognition from Decision;
4. validate Authority before external Execution;
5. validate Decision validity before execution;
6. represent Execution Results explicitly;
7. handle unknown outcomes;
8. protect State transitions;
9. preserve cycle provenance;
10. support explicit cycle completion or failure.

---

# 70. Recommended Capabilities

A mature implementation SHOULD support:

* cycle pause/resume;
* partial retry;
* recovery;
* compensation;
* parallel cognition;
* parallel execution;
* cost tracking;
* context reuse;
* decision reuse;
* human approval;
* cycle replay;
* distributed tracing.

---

# 71. Relationship With RUNTIME-001

RUNTIME-001 defines the architecture.

RUNTIME-002 defines the operational sequence executed by that architecture.

```text
RUNTIME-001
Architecture
      ↓
RUNTIME-002
Execution Cycle
      ↓
RUNTIME-003+
Individual Runtime Engines
```

---

# 72. Final Principle

The VIAL Execution Cycle is designed around one central idea:

> **Every organizational effect should have a traceable path from observation to authorized action and measurable outcome.**

Therefore:

```text
EVENT
  ↓
UNDERSTAND
  ↓
DECIDE
  ↓
AUTHORIZE
  ↓
ACT
  ↓
OBSERVE
  ↓
LEARN
  ↺
```

The cycle should become progressively more efficient over time because previous outcomes become organizational knowledge.

---

# 72. Final Statement

VIAL does not define intelligence as the ability to generate an answer.

It defines organizational intelligence as the ability to:

```text
Observe
→ Understand
→ Decide
→ Act
→ Evaluate
→ Remember
→ Improve
```

The Runtime Execution Cycle is the mechanism that makes this continuous process operational.

# End of RUNTIME-002
