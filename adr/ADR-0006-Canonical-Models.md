# Architecture Decision Record

# ADR-0006 — Canonical Models (Fase 3A)

**Status:** Accepted
**Date:** 2026-08-08
**Decision Type:** Architecture
**Related:** ADR-0000, ADR-0003, ADR-0005, FCP-002A, RFC-006, SDK-005, RUNTIME-002, RUNTIME-004, TOOLS-001
Depends On: None

---

## 1. Context

The integrity audit (AUDIT-003) and subsequent canonical alignment work
revealed that several normative concepts were defined inconsistently across
layers (RFC, RUNTIME, SDK, TOOLS, EXAMPLES):

- **Decision** conflated with Authorization, Approval, Execution and
  Invocation in different documents.
- **Decision lifecycle** diverged between RUNTIME-002 and SDK-005
  (ESCALATION appeared both as a state and as an event).
- **Context lifecycle** differed between SDK-004 and RUNTIME-004, and the
  Runtime did not recognize the frozen state.
- **Resource vs Execution Resource** were treated inconsistently as separate
  normative types in some documents.
- **Tool lifecycle** was defined twice (TOOLS-001 and TOOLS-008).
- **Identifiers** in EXAMPLES used ad hoc forms (`org.*`, `inv-*`) instead of
  the canonical `ORG-*` / `RES-*` / `CTX-*` / `DEC-*` / `INV-*` patterns used
  by the SDK and Runtime documents.
- **Events** (e.g. ESCALATION) were occasionally modeled as states merely
  because they appear in a flow.
- **Examples** introduced domain-specific codes that were not explicitly
  marked as illustrative.

This ADR records the consolidated canonical model (Fase 3A) so that the
subsequent layer-by-layer application (RFC → RUNTIME → SDK → TOOLS → EXAMPLES)
has traceability.

---

## 2. Analysis

### 2.1 Decision is a Determination, Not an Act

A Decision specifies an intended action or result. It is not the permission
to act, the explicit approval, the invocation, or the result of execution.
Earlier text in RFC-002 and related documents claimed that a Decision is
"always authorized", which is false: a Decision MAY exist without being
authorized. That claim MUST be removed.

### 2.2 Decision Lifecycle and ESCALATION

The canonical Decision lifecycle is
`DRAFT → PENDING → AUTHORIZED → EXECUTING → COMPLETED` with terminal or
alternative states `CANCELLED / REJECTED / FAILED / REVOKED`. ESCALATION is
an event or transition toward additional authority or review; it is not a
Decision state. RUNTIME-002 previously exposed ESCALATION as a state in the
Execution Cycle; under the Events vs States rule it MUST be represented as an
event.

### 2.3 Context Lifecycle and FROZEN

The canonical Context lifecycle is
`CREATED → VALID → FROZEN → CONSUMED → ARCHIVED`. After FROZEN the normative
content of a Context MUST NOT change. The Runtime MUST recognize FROZEN; it
cannot remain an SDK-only abstraction. Additional conditions (e.g. EXPIRED
from temporal validity) MAY exist as terminal conditions without creating a
competing lifecycle.

### 2.4 Resource

`Resource` is the canonical normative term. `Execution Resource` is not a
separate normative type; it is a contextual description of a Resource acting
during execution, unless formally defined in the VCG at a later date.

### 2.5 Tool Lifecycle

The canonical Tool lifecycle is single across the entire Tools layer:
`DRAFT → DEFINED → ACTIVE → DEPRECATED → RETIRED`. TOOLS-008 MUST NOT define a
second lifecycle; it MUST reference the lifecycle defined by TOOLS-001.

### 2.6 Authorization and Approval

Authorization determines whether an operation may proceed under the
applicable authority and policies. Approval is an explicit additional
authorization required by a policy or workflow. Therefore
`Approval ⊂ Authorization workflow`, but `Approval ≠ Authorization`.

### 2.7 Events vs States

A State is a persistent condition. An Event is something that occurred.
ESCALATION, INVOCATION_CREATED, EXECUTION_STARTED and EXECUTION_COMPLETED are
events. Events MUST NOT be converted into states merely because they appear
in a flow.

### 2.8 Identifiers

Examples and normative documents SHALL use the canonical identifier patterns:

```text
Organization → ORG-*
Resource     → RES-*
Context      → CTX-*
Decision     → DEC-*
Invocation   → INV-*
```

Ad hoc variants such as `org.*` and `inv-*` MUST NOT be used when
representing normative VIAL entities.

### 2.9 Examples Boundary

Examples MAY instantiate normative concepts but MUST NOT create new normative
states, fields, identifiers, lifecycle values or error codes. Domain-specific
values MUST be explicitly marked as illustrative/domain-specific.

---

## 3. Decisions

- **D-001 (Decision Model):** A Decision is a normative/operational
  determination produced from a Context. It is not Authorization, Approval,
  Execution, Invocation or an outcome. Claims that a Decision is always
  authorized SHALL be removed.
- **D-002 (Decision Lifecycle):** Canonical lifecycle
  `DRAFT → PENDING → AUTHORIZED → EXECUTING → COMPLETED`; alternative/terminal
  `CANCELLED / REJECTED / FAILED / REVOKED`; ESCALATION is an event/transition,
  not a state.
- **D-003 (Context Model):** Context is the information bound to an evaluation
  or execution at a point in time; immutable after freezing.
- **D-004 (Context Lifecycle):** `CREATED → VALID → FROZEN → CONSUMED →
  ARCHIVED`. The Runtime MUST recognize FROZEN. EXPIRED MAY exist as a
  terminal condition without a competing lifecycle.
- **D-005 (Resource):** `Resource` is the canonical normative term. Execution
  Resource is a contextual description only.
- **D-006 (Tool Lifecycle):** Single canonical lifecycle
  `DRAFT → DEFINED → ACTIVE → DEPRECATED → RETIRED`; TOOLS-008 references
  TOOLS-001.
- **D-007 (Authorization):** Authorization determines whether an operation
  may proceed under applicable authority and policies.
- **D-008 (Approval):** Approval is an explicit additional authorization
  required by policy/workflow; `Approval ⊂ Authorization workflow`, yet
  `Approval ≠ Authorization`.
- **D-009 (Events vs States):** Events (ESCALATION, INVOCATION_CREATED,
  EXECUTION_STARTED, EXECUTION_COMPLETED) SHALL NOT be represented as states.
- **D-010 (Identifiers):** Canonical identifier patterns
  `ORG-* / RES-* / CTX-* / DEC-* / INV-*`; ad hoc variants SHALL NOT be used
  for normative VIAL entities.
- **D-011 (Examples):** Examples MAY instantiate normative concepts but MUST
  NOT create new normative states, fields, identifiers, lifecycle values or
  error codes; domain-specific values MUST be explicitly marked as
  illustrative.

---

## 4. Consequences

### Positive

- single canonical lifecycle for Decision, Context and Tool;
- Events vs States rule resolves the RUNTIME-002 / SDK-005 divergence;
- Runtime recognizes the frozen Context, aligning SDK-004 and RUNTIME-004;
- `Resource` is a single normative term;
- identifier patterns become testable and consistent with automated tooling;
- examples remain rich while clearly marking illustrative/domain-specific
  content.

### Negative

- several documents require coordinated edits across layers;
- removal of `Decision is always authorized` requires care to avoid
  overcorrecting related claims;
- RUNTIME-002 Cycle model references ESCALATION and MUST be adjusted to the
  Events vs States rule.

---

## 5. Compliance

- Claims equivalent to `Decision is always authorized` SHALL NOT appear.
- ESCALATION SHALL be modeled as an event/transition, not as a state.
- FROZEN SHALL be recognized by the Runtime and immutable after freezing.
- `Resource` SHALL be the canonical normative term; `Execution Resource`
  SHALL only appear as a contextual description.
- TOOLS-008 SHALL reference TOOLS-001 for the canonical Tool lifecycle.
- EXAMPLES SHALL use `ORG-* / RES-* / CTX-* / DEC-* / INV-*` identifier
  patterns and SHALL mark domain-specific values as illustrative.

---

## 6. Status

Accepted.

---

## End of ADR
