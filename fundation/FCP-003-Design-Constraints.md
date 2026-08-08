# VIAL Foundation Change Proposal

# FCP-003 — VIAL Design Constraints

**Version:** 1.0.0
**Status:** Draft
**Type:** Foundation Change Proposal
Depends On:
- FCP-002A
**Related:** ADR-0002, TDOC-00 through TDOC-09, VCG-001

---

# 1. Abstract

FCP-003 defines the fundamental design constraints that implementations of VIAL SHALL respect.

The purpose is to prevent the VIAL architecture from gradually becoming another conventional multi-agent framework.

The constraints translate the TDOC theory into engineering boundaries.

---

# 2. Constraint: Organizational Primacy

The Organization SHALL remain the primary cognitive abstraction.

Implementations SHALL NOT define organizational cognition exclusively as the sum of independent agents.

---

# 3. Constraint: State Authority

The Organization SHALL have an authoritative representation of its current cognitive state.

```text
|Authoritative OCS| = 1
```

---

# 4. Constraint: Execution Independence

Organizational continuity SHOULD survive replacement of individual Execution Resources.

---

# 5. Constraint: Role Separation

Roles SHALL be represented independently from their current execution implementation.

```text
Role ≠ Implementation
```

---

# 6. Constraint: Capability Reuse

Capabilities SHOULD be reusable across multiple execution resources.

---

# 7. Constraint: Explicit Governance

Mandatory organizational rules SHALL be represented explicitly.

Governance SHALL NOT depend exclusively on undocumented model behavior.

---

# 8. Constraint: Evidence Provenance

Evidence used for significant organizational Decisions SHOULD remain traceable to its source and lineage.

---

# 9. Constraint: Decision Traceability

A significant Decision SHOULD be associated with:

```text
Context
Evidence
Policy
Decision
Result
```

---

# 10. Constraint: Memory Persistence

Organizational Memory SHALL be independent from temporary execution context.

---

# 11. Constraint: Cognitive Deduplication

Implementations SHOULD avoid transmitting or reconstructing information already available in authoritative organizational state or validated Memory.

---

# 12. Constraint: Bounded Context

Execution Resources SHOULD receive only the organizational information required to perform their assigned responsibility.

This constraint exists to reduce:

* unnecessary context;
* token consumption;
* cognitive noise;
* leakage of irrelevant information.

---

# 13. Constraint: Minimum Necessary Cognition

A VIAL implementation SHOULD perform the minimum amount of reasoning necessary to satisfy the organizational objective while maintaining correctness and governance.

---

# 14. Constraint: Deterministic Where Possible

Deterministic computation SHOULD be preferred over probabilistic reasoning when the task does not require probabilistic cognition.

Example:

```text
Calculation
Validation
Schema Checking
Policy Evaluation
State Verification
```

SHOULD NOT automatically consume an AI reasoning resource.

---

# 15. Constraint: Model Independence

The VIAL specification SHALL remain independent of any particular AI provider or model.

---

# 16. Constraint: Interoperability

Different implementations SHALL be capable of interoperating when they satisfy the same normative VIAL protocol requirements.

---

# 17. Constraint: Auditability

Important organizational transitions SHALL be reconstructable according to defined audit policies.

---

# 18. Constraint: Failure Isolation

Failure of an Execution Resource SHALL NOT automatically invalidate organizational identity, Memory or authoritative state.

---

# 19. Constraint: No Implicit Authority

An Execution Resource SHALL NOT acquire organizational authority merely because it generated a response.

Authority SHALL be explicitly delegated or defined by Policy.

---

# 20. Constraint: No Unbounded Delegation

Delegation SHALL be governed.

A delegated resource SHALL NOT automatically delegate further responsibilities unless explicitly permitted.

---

# 21. Constraint: State Integrity

State transitions SHALL preserve mandatory invariants.

Invalid transitions SHALL NOT become authoritative organizational state.

---

# 22. Constraint: Semantic Stability

Canonical VIAL terminology SHALL remain stable unless changed through formal governance.

---

# 23. Constraint: Economic Efficiency

VIAL SHOULD optimize not only technical performance but also economic cost.

Relevant dimensions include:

```text
Token Cost
Compute Cost
Memory Cost
Network Cost
Latency
Operational Cost
```

---

# 24. Constraint: Scalability

Scaling SHALL be evaluated by organizational capability rather than simply by number of agents.

---

# 25. Constraint: Observable Performance

Performance claims SHALL be supported by measurable benchmarks.

Claims such as:

```text
"uses fewer tokens"
"scales better"
"faster"
"more efficient"
```

SHALL require reproducible measurement.

---

# 26. Constraint: Baseline Comparison

VIAL benchmarks SHOULD compare implementations against meaningful baseline architectures.

The baseline SHALL be documented.

---

# 27. Constraint: No Premature Optimization

Architecture SHALL NOT optimize token consumption by sacrificing:

* correctness;
* safety;
* governance;
* auditability;
* organizational coherence.

---

# 28. Constraint: Protocol Independence

The conceptual VIAL architecture SHALL remain independent from its transport mechanism.

The same organizational semantics MAY be implemented over different transports.

---

# 29. Constraint: Implementation Freedom

The constraints define required properties, not mandatory implementation technologies.

VIAL implementations MAY use:

* Python;
* Rust;
* Go;
* TypeScript;
* Java;
* other languages.

Likewise, they MAY use different storage and infrastructure technologies.

---

# 30. Constraint Hierarchy

When constraints conflict, the following priority applies:

```text
1. Safety
2. Governance
3. Correctness
4. State Integrity
5. Auditability
6. Organizational Coherence
7. Interoperability
8. Efficiency
9. Performance
10. Cost Optimization
```

Optimization SHALL NOT violate a higher-priority constraint.

---

# 31. Compliance

A VIAL implementation SHOULD be evaluated against these constraints before claiming architectural conformance.

---

# 32. Decision

FCP-003 proposes adoption of these constraints as the engineering boundary between VIAL Foundation theory and subsequent protocol specifications.

---

# 33. Next Step

Upon acceptance, the next major artifact SHOULD be the first normative protocol specification.

The recommended sequence is:

```text
FCP-003
   ↓
ADR
   ↓
VIAL Core Specification
   ↓
First RFC
   ↓
Reference Implementation
   ↓
Conformance Tests
   ↓
Benchmark
```

---

# End of FCP-003
