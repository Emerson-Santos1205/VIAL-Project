# RFC-004 — Context & Cognitive Efficiency

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Standards Track
Depends On:
- RFC-002
- RFC-003
- FCP-002A
- FCP-006
- FCP-007

---

# 1. Abstract

This document defines the VIAL model for **Context Construction and Cognitive Efficiency**.

The objective is to ensure that an execution resource receives the **minimum sufficient context** required to perform an operation correctly.

VIAL treats context as a controlled computational resource rather than as a complete representation of organizational knowledge.

The protocol establishes principles for:

* context selection;
* context projection;
* context references;
* context compression;
* cognitive reuse;
* reasoning escalation;
* redundant-context elimination;
* context freshness;
* context validity;
* cognitive cost measurement.

The central principle is:

> **Provide the smallest sufficient context capable of producing a valid result.**

---

# 2. Motivation

Conventional AI architectures frequently transmit large amounts of information to every execution resource.

Typical patterns include:

```text
Full History
+
Full Memory
+
Full State
+
Full Instructions
+
Current Task
```

This creates unnecessary:

* token consumption;
* latency;
* inference cost;
* network traffic;
* processing;
* repeated reasoning;
* cognitive noise.

VIAL replaces indiscriminate context transmission with **selective contextualization**.

```text
Organization
      ↓
Relevant Information
      ↓
Context Projection
      ↓
execution resource
```

---

# 3. Scope

RFC-004 defines:

* Context;
* Context Projection;
* Context Selection;
* Context References;
* Context Sufficiency;
* Context Minimization;
* Context Freshness;
* Cognitive Cost;
* Cognitive Escalation;
* Reuse;
* caching;
* context invalidation.

It does not define:

* a specific AI model;
* a specific tokenizer;
* a mandatory transport;
* a specific database;
* a specific inference engine;
* a mandatory compression algorithm.

---

# 4. Core Principle

Context MUST be treated as a **derived execution artifact**.

```text
Persistent Organizational Knowledge
             ↓
      Context Selection
             ↓
       Context Projection
             ↓
       execution resource
```

The Organization remains the source of persistent cognition.

The execution resource receives only what is necessary for its assigned operation.

---

# 5. Context Definition

Context is the information made available to an execution resource for a specific operation.

Conceptually:

```text
Context =
Task
+
Relevant State
+
Relevant Knowledge
+
Applicable Policy
+
Required Evidence
+
Constraints
```

Context MAY also contain:

* references;
* execution parameters;
* expected output;
* authorization information;
* temporal constraints.

When Context is material to a consequential evaluation or execution, RFC-004 consumes the canonical Context lifecycle defined by RFC-002 and RFC-003:

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

# 6. Context Is Not Memory

Context and Memory MUST remain conceptually distinct.

```text
Memory
=
Persistent Organizational Knowledge
```

```text
Context
=
Temporary Operational View
```

A memory artifact MAY be included in Context.

However, inclusion does not transform Memory into Context permanently.

---

# 7. Context Is Not State

Similarly:

```text
State
=
Current Organizational Condition
```

```text
Context
=
Selected View Required for Execution
```

A Context Projection MAY contain State information without becoming authoritative State.

---

# 8. Context Selection

Before execution, the Organization SHOULD determine which information is actually relevant.

Selection SHOULD consider:

* operation type;
* objective;
* current State;
* applicable policies;
* required evidence;
* execution capability;
* authorization;
* temporal validity.

---

# 9. Minimum Sufficient Context

The protocol defines the concept of **Minimum Sufficient Context**.

A Context is minimally sufficient when removing relevant information would materially increase the probability of:

* incorrect execution;
* invalid reasoning;
* policy violation;
* unsafe behavior;
* incorrect State Transition.

Adding information beyond that point should require justification.

---

# 10. Context Minimization

The objective is not:

> Send as little information as possible.

The objective is:

> Send as little information as possible **without compromising correctness**.

Therefore:

```text
Minimal Context
        +
Correctness
        =
Efficient Context
```

---

# 11. Context Layers

VIAL Context SHOULD be conceptually divided into layers.

```text
Layer 0 — Task
Layer 1 — Immediate State
Layer 2 — Constraints
Layer 3 — Relevant Knowledge
Layer 4 — Evidence
Layer 5 — Historical Context
Layer 6 — Extended Organizational Context
```

Execution SHOULD begin with the lowest sufficient layer.

Additional layers SHOULD be introduced only when necessary.

---

# 12. Progressive Context

A resource SHOULD NOT automatically receive all context layers.

Instead:

```text
Task
 ↓
Immediate State
 ↓
Can Execute?
 ├── YES → Execute
 └── NO
       ↓
   Additional Context
       ↓
   Can Execute?
       ├── YES
       └── NO → Escalate
```

This creates **progressive contextualization**.

---

# 13. Context Escalation

If the initial Context is insufficient, additional information MAY be requested.

Example:

```text
Initial Context
      ↓
Insufficient
      ↓
Request Knowledge Reference
      ↓
Expanded Context
      ↓
Retry
```

This is preferable to transmitting the complete organizational knowledge base from the beginning.

---

# 14. Context References

Persistent information SHOULD be referenced rather than duplicated where practical.

Example:

```text
Knowledge Reference: K-482
State Reference: S-901
Policy Reference: P-17
Evidence Reference: E-712
```

The execution resource can retrieve only what is required.

---

# 15. Reference Resolution

A Context Reference SHOULD resolve to a well-defined organizational artifact.

Resolution SHOULD provide:

* identity;
* version;
* validity;
* applicable scope.

A stale or invalid reference MUST NOT silently be treated as current information.

---

# 16. Context Versioning

Context SHOULD be associated with the State and knowledge versions from which it was constructed when such information affects correctness.

Conceptually:

```text
Context
 ├── State v82
 ├── Knowledge v14
 ├── Policy v7
 └── Evidence v91
```

This allows later reconstruction of the execution conditions.

---

# 17. Context Freshness

Context may become stale.

A Context SHOULD be considered stale when relevant underlying information has changed.

Examples:

```text
State changed
Policy changed
Evidence invalidated
Knowledge superseded
Authorization expired
```

Stale Context SHOULD be revalidated before producing a significant organizational mutation.

---

# 18. Context Validity

A Context MAY have a validity status:

```text
VALID
STALE
INVALID
EXPIRED
SUPERSEDED
UNKNOWN
```

The status SHOULD be machine-detectable where necessary.

These validity statuses are conditions, not a competing lifecycle. The canonical lifecycle remains `CREATED → VALID → FROZEN → CONSUMED → ARCHIVED`.

---

# 19. Context Isolation

execution resources SHOULD receive only the information necessary for their assigned authority.

This provides:

* security;
* privacy;
* efficiency;
* reduced cognitive noise.

Context minimization is therefore both a performance and governance mechanism.

---

# 20. Context and Authority

Context SHOULD reflect the authority scope of the execution.

A resource authorized to inspect production State does not automatically require access to:

* financial State;
* personnel information;
* unrelated organizational history.

Context should follow:

```text
Required Information
+
Authorized Scope
```

---

# 21. Cognitive Cost

VIAL defines Cognitive Cost as the total computational and communication burden associated with obtaining an acceptable result.

It may include:

```text
Token Cost
Inference Cost
Latency
Network Traffic
Memory Retrieval
Validation Cost
Coordination Cost
Retry Cost
```

An implementation SHOULD measure these dimensions where practical.

---

# 22. Cost-Aware Execution

The Organization SHOULD consider cognitive cost when selecting an execution resource.

Conceptually:

```text
Task
 ↓
Candidate Resources
 ↓
Capability
+
Cost
+
Reliability
+
Authority
 ↓
Selected Resource
```

The cheapest resource that can safely satisfy the operation SHOULD be preferred.

---

# 23. Deterministic First

Before invoking complex reasoning, the Organization SHOULD determine whether the task can be resolved deterministically.

Preferred hierarchy:

```text
Existing Validated Result
        ↓
Deterministic Rule
        ↓
Calculation
        ↓
Cached Knowledge
        ↓
Lightweight Reasoning
        ↓
Advanced Reasoning
        ↓
Human / Specialized Resource
```

This hierarchy is a core VIAL efficiency mechanism.

---

# 24. Cognitive Reuse

Previously validated results SHOULD be reusable when their validity remains applicable.

Instead of:

```text
Same Problem
 ↓
New Reasoning
```

VIAL encourages:

```text
Problem
 ↓
Search Existing Cognition
 ↓
Applicable?
 ├── YES → Reuse
 └── NO  → Reason
```

---

# 25. Reuse Conditions

Cognitive reuse SHOULD consider:

* semantic similarity;
* State compatibility;
* policy compatibility;
* temporal validity;
* evidence validity;
* scope;
* confidence;
* provenance.

Similarity alone MUST NOT be sufficient for reuse when correctness is critical.

---

# 26. Cognitive Cache

An implementation MAY maintain a cognitive cache.

The cache MAY contain:

* validated answers;
* validated decisions;
* computation results;
* common interpretations;
* reusable reasoning artifacts.

Cached cognition MUST have explicit validity semantics where necessary.

---

# 27. Cache Invalidation

Cached cognition SHOULD be invalidated when relevant assumptions change.

Potential invalidation triggers include:

```text
State Change
Policy Change
Evidence Change
Knowledge Update
Time Expiration
Contradictory Evidence
Scope Change
```

The system SHOULD prefer explicit invalidation over silent reuse of known-stale cognition.

---

# 28. Context Deduplication

Repeated information SHOULD be eliminated.

For example:

```text
State:
Pressure = 8.2 bar

History:
Pressure was 8.2 bar yesterday.

Current Task:
Evaluate pressure.
```

The historical value may be unnecessary if only current pressure is relevant.

The Context Builder SHOULD distinguish:

```text
Relevant
```

from:

```text
Available
```

---

# 29. Context Compression

Context MAY be compressed or summarized when semantic integrity is preserved.

Compression MUST NOT remove information necessary for:

* correct execution;
* authorization;
* safety;
* evidence;
* auditability.

Summarization SHOULD preserve references to authoritative sources.

---

# 30. Reference + Summary

A useful VIAL pattern is:

```text
Compact Summary
+
Authoritative Reference
```

Example:

```text
Current production pressure is above normal range.

Evidence: E-482
State: S-91
Policy: P-7
```

This reduces transmission while preserving traceability.

---

# 31. Context Budget

An implementation MAY establish a context budget.

The budget can be expressed in:

* tokens;
* bytes;
* latency;
* retrieval operations;
* monetary cost.

The budget SHOULD NOT override mandatory safety or correctness requirements.

---

# 32. Adaptive Context

Context size SHOULD adapt to task complexity.

```text
Simple Task
    ↓
Small Context

Complex Task
    ↓
Expanded Context
```

The Organization SHOULD avoid a fixed maximum context policy that unnecessarily penalizes simple operations.

---

# 33. Context Quality

Context quality is not proportional to context quantity.

A large Context may reduce performance when it contains:

* irrelevant information;
* contradictions;
* stale facts;
* duplicated information;
* ambiguous instructions.

Therefore:

```text
Context Quality
≠
Context Size
```

---

# 34. Context Noise

Context Noise is information that is available but does not materially contribute to the operation.

Examples:

* unrelated history;
* duplicated facts;
* obsolete policies;
* irrelevant organizational domains;
* redundant instructions.

The Context Builder SHOULD minimize noise.

---

# 35. Contradictory Context

If Context contains contradictory information, the contradiction SHOULD be detectable.

The system SHOULD NOT silently merge contradictory facts.

Example:

```text
Source A: Pump ACTIVE
Source B: Pump STOPPED
```

The execution resource should receive a resolvable conflict state rather than ambiguous data presented as truth.

---

# 36. Context Provenance

Important Context elements SHOULD retain references to their sources.

Conceptually:

```text
Context Element
      ↓
Source Reference
      ↓
Persistent Artifact
```

This allows:

* verification;
* auditing;
* reconstruction;
* invalidation.

---

# 37. Context Construction Pipeline

A VIAL implementation MAY use the following pipeline:

```text
Request
   ↓
Identify Operation
   ↓
Determine Decision
   ↓
Determine Authority
   ↓
Approval (when required)
   ↓
Inspect Current State
   ↓
Select Required Knowledge
   ↓
Select Evidence
   ↓
Check Existing Cognition
   ↓
Build Minimum Sufficient Context
   ↓
Validate Context
   ↓
Invocation
   ↓
Execute
```

Within this flow, Decision determines what is intended, Authority determines whether the operation may proceed, and Approval MAY be required as an explicit additional step. RFC-004 does not redefine those concepts; it consumes the canonical model from RFC-002 and RFC-006.

---

# 38. Context Validation

Before execution, Context SHOULD be checked for:

* completeness;
* freshness;
* authorization;
* contradictions;
* required constraints;
* source validity.

If validation fails, execution SHOULD be delayed or escalated.

---

# 39. Context Construction Cost

Context construction itself has a cost.

Therefore:

```text
Context Retrieval Cost
+
Inference Cost
```

should be considered together.

An implementation should avoid retrieving large amounts of information merely to discover that it is unnecessary.

---

# 40. Retrieval Strategy

The preferred retrieval order SHOULD be:

```text
Local / Cached Relevant Data
        ↓
Direct State
        ↓
Indexed Knowledge
        ↓
Referenced Evidence
        ↓
Broader Search
```

This reduces unnecessary retrieval.

---

# 41. Query Minimization

When retrieving organizational knowledge, queries SHOULD be specific enough to avoid unnecessary results.

The objective is:

```text
High Relevance
+
Low Retrieval Volume
```

rather than maximum recall in every operation.

---

# 42. Cognitive Escalation Model

VIAL defines a general escalation path:

```text
LEVEL 0
Direct State / Known Answer

LEVEL 1
Deterministic Processing

LEVEL 2
Lightweight Reasoning

LEVEL 3
Advanced Reasoning

LEVEL 4
Specialized Resource

LEVEL 5
Human Authority
```

Not every implementation must use exactly these levels.

The principle is progressive escalation based on need.

---

# 43. Escalation Criteria

Escalation MAY occur when:

* confidence is insufficient;
* evidence is incomplete;
* ambiguity remains;
* policy complexity exceeds the current resource;
* State conflict exists;
* authority requirements exceed the current resource;
* risk exceeds the acceptable threshold.

---

# 44. No Forced Intelligence

A key VIAL principle is:

> **Do not use intelligence when deterministic computation is sufficient.**

For example:

```text
Temperature > 80°C?
```

may be evaluated deterministically.

It does not require an AI model.

This reduces:

* cost;
* latency;
* token usage;
* unnecessary complexity.

---

# 45. Reasoning Only When Valuable

AI reasoning SHOULD be invoked when it provides meaningful additional value.

Examples include:

* ambiguity;
* interpretation;
* planning;
* anomaly analysis;
* complex decision support;
* synthesis.

The Organization SHOULD NOT invoke reasoning simply because an AI resource is available.

---

# 46. Multi-Resource Efficiency

When multiple execution resources participate, VIAL SHOULD minimize duplicated context.

Instead of:

```text
Context → Agent A
Context → Agent B
Context → Agent C
```

the system MAY use:

```text
Shared References
       ↓
Agent A → Result
Agent B → Result
Agent C → Result
```

Each resource receives only its required projection.

---

# 47. Result Reuse

Execution results MAY be reused when they remain valid.

Example:

```text
Resource A
   ↓
Validated Result
   ↓
Persistent Reference
   ↓
Resource B
```

This prevents repeated computation.

---

# 48. Parallelism

Independent cognitive operations MAY be executed in parallel.

However, parallel execution SHOULD be used only when:

* operations are independent;
* context is sufficient;
* coordination cost does not exceed the benefit.

Parallelism is not inherently more efficient.

---

# 49. Sequential Reasoning

Sequential execution MAY be preferable when:

* operations depend on previous results;
* validation is required between stages;
* state may change;
* evidence must be progressively evaluated.

The protocol does not mandate parallel or sequential cognition.

---

# 50. Context Reuse

A Context MAY be reused for multiple operations when:

* State has not materially changed;
* relevant policies remain valid;
* evidence remains valid;
* authorization remains valid;
* the operation scope remains compatible.

Otherwise, the Context SHOULD be rebuilt or revalidated.

---

# 51. Context Mutation

execution resources SHOULD NOT mutate shared Context in place.

Instead:

```text
Context A
   ↓
Execution
   ↓
Result
```

A new Context MAY be generated for a subsequent operation.

This prevents hidden state coupling.

---

# 52. Context Lineage

Important Context SHOULD be traceable to:

```text
State Version
Knowledge Version
Policy Version
Evidence
Operation
```

This enables reconstruction of the conditions under which a result was produced.

---

# 53. Cognitive Efficiency Metrics

Implementations SHOULD measure at least:

### Context Efficiency

```text
Relevant Context
─────────────────
Total Context
```

### Reuse Rate

```text
Reused Cognition
────────────────
Total Cognitive Operations
```

### Escalation Rate

```text
Escalated Operations
─────────────────────
Total Operations
```

### Redundant Reasoning Rate

```text
Repeated Equivalent Reasoning
──────────────────────────────
Total Reasoning Operations
```

### Cognitive Cost

A composite metric MAY combine:

* tokens;
* latency;
* compute;
* retrieval;
* communication;
* validation.

---

# 54. Efficiency Must Be Measured

VIAL MUST NOT assume that a particular optimization is efficient merely because it appears theoretically efficient.

Implementations SHOULD benchmark:

```text
Before Optimization
        vs.
After Optimization
```

using real workloads.

---

# 55. Safety Over Efficiency

Efficiency MUST NOT override mandatory:

* safety;
* authorization;
* evidence;
* compliance;
* correctness requirements.

The correct hierarchy is:

```text
Safety / Correctness
        ↓
Authority
        ↓
Reliability
        ↓
Efficiency
```

Efficiency optimizes the valid solution space.

It does not redefine it.

---

# 56. Context and Auditability

Reducing Context MUST NOT destroy the ability to reconstruct why a decision was made.

Therefore, compact Context SHOULD preserve references to authoritative sources.

The preferred pattern is:

```text
Small Context
+
Strong References
=
Low Cost + Auditability
```

---

# 57. Example — Industrial Monitoring

Current State:

```text
Pressure = 8.2 bar
Temperature = 72°C
Mode = AUTO
```

Task:

```text
Determine whether pump operation is within configured limits.
```

A complete organizational context is unnecessary.

Minimum Context:

```text
Current Pressure
Current Temperature
Operating Mode
Applicable Limits
```

The operation can be resolved deterministically.

No AI reasoning is required.

---

# 58. Example — Complex Diagnosis

Task:

```text
Determine the probable cause of repeated pressure instability.
```

Initial Context:

```text
Current State
Recent Events
Known Operating Limits
```

If insufficient:

```text
+
Relevant Maintenance History
```

If still insufficient:

```text
+
Historical Failure Patterns
```

Only then should advanced reasoning be invoked.

This is progressive contextualization.

---

# 59. Example — Reusable Cognition

Suppose the Organization previously validated:

```text
Pattern P-17
→
Likely valve obstruction
```

A new event matches the same validated conditions.

Instead of repeating full reasoning:

```text
New Event
   ↓
Pattern Lookup
   ↓
P-17 Applicable?
   ↓
Yes
   ↓
Reuse
```

If the State or evidence differs materially:

```text
P-17
   ↓
Not Applicable
   ↓
New Reasoning
```

---

# 60. Example — Context Conflict

Suppose:

```text
State says:
Pump = RUNNING

Recent event says:
Pump = STOPPED
```

The system should not simply send both facts to an AI and hope it resolves the contradiction.

Instead:

```text
Conflict Detected
       ↓
Determine authoritative source
       ↓
Resolve / Escalate
       ↓
Build valid Context
```

---

# 61. Large-Scale Efficiency

At scale, small inefficiencies become significant.

If an unnecessary 1,000-token context is transmitted 100,000 times:

```text
100,000 × 1,000
=
100,000,000 unnecessary tokens
```

Therefore, Context Architecture is an economic architecture.

VIAL treats context minimization as a first-class system design concern.

---

# 62. Economic Objective

The VIAL objective is not simply:

> Use fewer tokens.

It is:

> Produce the required organizational outcome with the minimum sufficient cognitive and computational expenditure.

This includes:

* token cost;
* model cost;
* infrastructure cost;
* communication;
* latency;
* human intervention;
* repeated work.

---

# 63. Context Efficiency Principle

The fundamental optimization loop is:

```text
Observe Cost
      ↓
Identify Waste
      ↓
Reduce Context
      ↓
Measure Result
      ↓
Validate Correctness
      ↓
Adopt Optimization
```

Optimization MUST remain empirical.

---

# 64. Conformance Requirements

An implementation conforming to RFC-004 MUST:

1. distinguish Context from persistent State;
2. distinguish Context from persistent Memory;
3. support selective context construction;
4. avoid requiring complete organizational history for every operation;
5. preserve required authorization and correctness information;
6. support detection of stale Context for significant operations;
7. preserve references to authoritative information where required;
8. provide a mechanism for progressive context expansion or equivalent behavior;
9. avoid unnecessary repeated cognition where validated reuse is possible.

---

# 65. Recommended Capabilities

A conforming implementation SHOULD additionally support:

* context budgets;
* cognitive caching;
* context projections;
* reference-based retrieval;
* progressive escalation;
* context quality metrics;
* reuse metrics;
* redundant reasoning detection;
* context lineage;
* adaptive context construction.

---

# 66. Non-Goals

RFC-004 does not define:

* a universal prompt format;
* a universal tokenization strategy;
* a mandatory LLM;
* a mandatory context-window size;
* a specific retrieval-augmented generation framework;
* a specific vector database;
* a mandatory caching technology.

---

# 67. Relationship With RFC-002

RFC-002 defines the Organizational Cognition Protocol.

RFC-004 defines how the information required by that protocol is efficiently provided to execution resources.

```text
RFC-002
Cognition
   ↓
RFC-004
Context Efficiency
   ↓
Execution
```

The two together establish:

```text
Persistent Cognition
+
Selective Context
```

---

# 68. Relationship With RFC-003

RFC-003 defines persistent State.

RFC-004 defines how relevant State becomes temporary execution Context.

```text
RFC-003
Persistent State
       ↓
RFC-004
State Projection
       ↓
Execution Context
```

This prevents the complete organizational State from being unnecessarily transmitted.

---

# 69. Relationship With RFC-005

RFC-005 will define Memory & Knowledge.

RFC-004 will determine how relevant portions of that persistent cognition are selected for execution.

```text
Memory / Knowledge
       ↓
Relevance
       ↓
Context Projection
       ↓
Execution
```

---

# 70. Architectural Principle

VIAL's efficiency architecture can therefore be summarized as:

```text
        PERSIST
           ↓
        REFERENCE
           ↓
        SELECT
           ↓
        PROJECT
           ↓
        EXECUTE
           ↓
        VALIDATE
           ↓
         REUSE
```

The system should not repeatedly reconstruct information that already exists.

---

# 71. Final Model

The VIAL Context Model is:

```text
                 ORGANIZATION
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
        STATE                  MEMORY
          │                       │
          └───────────┬───────────┘
                      ↓
              CONTEXT SELECTION
                      ↓
             MINIMUM SUFFICIENT
                   CONTEXT
                      ↓
              EXECUTION RESOURCE
                      ↓
                  RESULT
                      ↓
                 VALIDATION
                      ↓
                STATE / MEMORY
                      ↓
                FUTURE REUSE
```

---

# 72. Final Principle

The fundamental VIAL context principle is:

> **Do not send the Organization to the Executor. Send the Executor only what it needs from the Organization.**

Therefore:

```text
Context is temporary.
State is persistent.
Memory is reusable.
References reduce duplication.
Reasoning is escalated when necessary.
Deterministic operations are preferred when sufficient.
Efficiency is measured, not assumed.
```

The ultimate objective is:

> **Maximum organizational capability with minimum unnecessary cognitive expenditure.**

# End of RFC-004
