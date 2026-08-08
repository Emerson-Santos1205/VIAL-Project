# Architecture Decision Record

# ADR-0002 — Adoption of Distributed Organizational Cognition

**Status:** Accepted
**Date:** 2026-08-07
**Decision Type:** Foundation Architecture
**Related:** FCP-002A, TDOC-00 through TDOC-09
Depends On: None

---

# 1. Context

VIAL requires a conceptual model capable of supporting large-scale cognitive systems without making individual AI agents the permanent owners of organizational context.

Traditional multi-agent architectures frequently associate cognition with individual agents.

This creates potential duplication in:

* context;
* memory;
* reasoning;
* communication;
* coordination.

VIAL requires a model in which organizational cognition can persist independently of individual execution resources.

---

# 2. Decision

VIAL SHALL adopt the **Theory of Distributed Organizational Cognition (TDOC)** as a foundational theoretical model.

The Organization becomes the primary cognitive abstraction.

---

# 3. Architectural Principle

The following relationship SHALL be adopted:

```text
Organization
     ↓
Role
     ↓
Capability
     ↓
Execution Resource
```

rather than:

```text
Agent
     ↓
Organization
```

---

# 4. Organizational State

The Organizational Cognitive State (OCS) SHALL be treated as the authoritative representation of current organizational cognition.

---

# 5. Organizational Memory

Persistent organizational Knowledge SHALL remain independent from temporary execution resources.

---

# 6. Governance

Policies SHALL be represented as explicit organizational constraints.

---

# 7. Evidence

Significant Decisions SHOULD maintain traceability to supporting Evidence.

---

# 8. Consequences

## Positive

The decision provides a foundation for:

* reduced context duplication;
* lower communication overhead;
* execution-resource interchangeability;
* organizational continuity;
* auditability;
* scalable specialization;
* vendor neutrality.

## Negative

The architecture introduces additional requirements for:

* state management;
* consistency;
* governance;
* provenance;
* synchronization;
* validation.

---

# 9. Rejected Alternative

### Agent-Centric Cognition

Rejected as the primary VIAL abstraction.

This does not mean VIAL prohibits agent-centric execution.

It means organizational cognition SHALL NOT depend exclusively on individual agent memory or context.

---

# 10. Decision Rule

Future architectural proposals SHALL be evaluated against this ADR.

A proposal that materially contradicts the organizational-cognition model SHALL require explicit architectural review.

---

# 11. Status

Accepted.

The decision is adopted as the foundational architectural model of VIAL: the
entire specification stack (RFC-002 through RFC-010, SDK, RUNTIME, TOOLS) and
the reference implementation are built upon the Theory of Distributed
Organizational Cognition (TDOC), and this ADR is treated as normative by the
dependent RFCs.

---

# End of ADR
