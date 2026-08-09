# Architecture Decision Record

# ADR-0005 — Canonical Semantic and Lifecycle Models

**Status:** Proposed
**Version:** 1.0.0
**Date:** 2026-08-08
**Decision Type:** Architecture
**Related:** ADR-0000, ADR-0001, ADR-0003, FCP-002A, SDK-004, SDK-005, RUNTIME-002, RUNTIME-004, TOOLS-001
Depends On: None

---

## 1. Context

The VIAL specification has completed the structural and semantic audits through
AUDIT-003.

The audits identified divergences between the normative model and its Runtime,
SDK, Tools, and Examples representations, particularly around:

- Decision lifecycle;
- Context lifecycle and freezing;
- Resource terminology;
- Tool lifecycle;
- Decision, Authorization, and Approval semantics;
- State versus Event semantics;
- Canonical entity identifiers;
- Domain-specific concepts introduced by Examples.

Phase 3A consolidated the canonical models that must govern subsequent
alignment work.

This ADR records those canonical decisions.

---

## 2. Decisions

### D-008 — Canonical Decision Model

A Decision is a normative or operational determination produced from a Context
that specifies an intended action or outcome.

A Decision is distinct from:

- Authorization;
- Approval;
- Invocation;
- Execution;
- Outcome.

The canonical conceptual flow is:

```text
Context
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
Outcome
```

A Decision MAY exist before authorization.

Therefore, a Decision MUST NOT be defined as inherently authorized.

### D-009 — Canonical Decision Lifecycle

The canonical Decision lifecycle is:

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

The following are terminal or alternative states:

```text
CANCELLED
REJECTED
FAILED
REVOKED
```

ESCALATION is not a Decision state.

Escalation is an event or process that causes additional authority, review, or
intervention.

A Decision MAY enter an escalation flow while remaining in an appropriate
lifecycle state.

Runtime and SDK implementations MUST expose compatible lifecycle semantics.

### D-010 — Canonical Context Lifecycle and Freeze

A Context represents the information associated with a specific evaluation or
execution point.

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

FROZEN is a normative Context state.

After a Context becomes FROZEN, its normative content MUST NOT be modified.

Runtime implementations MUST recognize the frozen state.

Temporal invalidity such as expiration MAY be represented as a terminal
condition where required, but MUST NOT create a competing lifecycle model.

### D-011 — Canonical Resource Terminology

Resource is the canonical normative term.

Execution Resource MUST NOT be treated as a separate normative concept unless a
future specification explicitly defines it as a specialization of Resource.

Documents SHOULD use Resource when referring to the normative entity.

The term `execution resource` MAY be used descriptively when referring to a
Resource in an execution context, but it MUST NOT silently introduce a new
resource type.

### D-012 — Canonical Tool Lifecycle

The canonical Tool lifecycle is:

```text
DRAFT
  ↓
DEFINED
  ↓
ACTIVE
  ↓
DEPRECATED
  ↓
RETIRED
```

Definitions:

- DRAFT — Tool is being designed or specified.
- DEFINED — Tool contract has been formally defined.
- ACTIVE — Tool is available for use.
- DEPRECATED — Tool remains defined but should not be selected for new use.
- RETIRED — Tool is no longer available for operational use.

No Tool specification MAY introduce an independent lifecycle without explicitly
extending or superseding this model.

### D-013 — Decision, Authorization, and Approval Separation

The following concepts are distinct:

Decision

Determines what is intended or should be done.

Authorization

Determines whether the intended operation is permitted under applicable
authority and policy.

Approval

Represents an explicit approval step required by a policy or workflow.

Therefore:

```text
Decision ≠ Authorization
Decision ≠ Approval
Authorization ≠ Approval
```

Approval MAY form part of an authorization workflow, but approval itself does
not replace the authorization model.

Implementations MUST preserve these distinctions.

### D-014 — Events and States Are Distinct

A state represents a condition of an entity.

An event represents an occurrence or transition.

Examples of states include:

```text
DRAFT
PENDING
AUTHORIZED
EXECUTING
COMPLETED
FAILED
REVOKED
```

Examples of events include:

```text
ESCALATION
INVOCATION_CREATED
EXECUTION_STARTED
EXECUTION_COMPLETED
```

An event MUST NOT be introduced as a lifecycle state merely because it appears
in an operational flow.

Runtime, SDK, Tools, and Examples MUST preserve this distinction.

### D-015 — Canonical Entity Identifiers

Normative entity identifiers use the following canonical prefixes:

```text
ORG-*   Organization
RES-*   Resource
CTX-*   Context
DEC-*   Decision
INV-*   Invocation
```

Implementations and Examples SHOULD use these canonical forms.

Alternative identifiers such as `org.*` or `inv-*` MUST NOT be used when
representing canonical VIAL entities.

Domain-specific identifiers MAY exist for external systems, but MUST remain
distinguishable from canonical VIAL identifiers.

### D-016 — Non-Normative Boundary of Examples

Examples exist to demonstrate the normative system.

Examples MAY instantiate domain-specific values and scenarios.

Examples MUST NOT silently introduce new normative:

- lifecycle states;
- entity types;
- required fields;
- error codes;
- event types;
- identifiers;
- authorization semantics.

A domain-specific value that is not part of the normative model MUST be
explicitly presented as illustrative or domain-specific.

Examples therefore MUST conform to the canonical models defined by the FCP,
RFC, Runtime, SDK, and Tools layers.

---

## 3. Consequences

These decisions establish a single semantic model across the VIAL
specification.

The following alignment is required:

```text
RFC
 ↓
RUNTIME
 ↓
SDK
 ↓
TOOLS
 ↓
EXAMPLES
```

The normative layers define the model, Runtime implements the model, SDK
exposes the model, Tools consume the model, and Examples demonstrate the
model.

Existing documents that contradict these decisions MUST be updated during Phase
3B.

---

## 4. Required Alignment

The following known divergences are specifically covered by this ADR:

- RUNTIME-006 MUST remain the Cognition Engine and MUST NOT introduce a second
  Decision Engine.
- RUNTIME-006 MUST align with RFC-006.
- Runtime and SDK Decision lifecycles MUST converge on D-009.
- Context freeze MUST be implemented consistently between SDK and Runtime.
- Tenant lifecycle examples MUST use the canonical Organization lifecycle.
- Execution Resource terminology MUST converge on Resource.
- TOOLS-001 and TOOLS-008 MUST use D-012.
- Decision, Authorization, and Approval MUST be separated.
- Example-specific error codes and fields MUST NOT become implicit normative
  concepts.
- Example identifiers MUST use the canonical identifier model.

---

## 5. Implementation Order

The decisions in this ADR MUST be applied in the following order:

1. RFC
2. RUNTIME
3. SDK
4. TOOLS
5. EXAMPLES

After implementation, AUDIT-004 MUST verify normative coverage and semantic
consistency.

---

## 6. Related Audits

- AUDIT-001 — Repository Integrity Report
- AUDIT-002 — Dependency & Reference Integrity
- AUDIT-003 — Semantic & Architectural Audit
- Phase 3A — Canonical Models

---

## 7. Decision History

| ID | Decision |
|---|---|
| D-001 | Existing ADR-0005 decision |
| D-002 | Existing ADR-0005 decision |
| D-003 | Existing ADR-0005 decision |
| D-004 | Existing ADR-0005 decision |
| D-005 | Existing ADR-0005 decision |
| D-006 | Existing ADR-0005 decision |
| D-007 | Existing ADR-0005 decision |
| D-008 | Canonical Decision Model |
| D-009 | Canonical Decision Lifecycle |
| D-010 | Canonical Context Lifecycle and Freeze |
| D-011 | Canonical Resource Terminology |
| D-012 | Canonical Tool Lifecycle |
| D-013 | Decision / Authorization / Approval Separation |
| D-014 | Events vs States |
| D-015 | Canonical Entity Identifiers |
| D-016 | Non-Normative Boundary of Examples |

---

## 8. Status

Proposed for approval.

---

## End of ADR
