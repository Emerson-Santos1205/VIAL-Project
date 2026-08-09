# Architecture Decision Record

# ADR-0007 — Layer Responsibilities and Application Order

**Status:** Accepted
**Date:** 2026-08-08
**Decision Type:** Architecture
**Related:** ADR-0000, ADR-0003, ADR-0006, FCP-002A, VCG-001
Depends On:
- ADR-0006

---

## 1. Context

ADR-0006 consolidated the canonical models for Decision, Context, Resource,
Authorization, Approval, Tool Lifecycle, Events vs States, identifiers and
Examples boundaries.

The remaining work must be applied consistently across layers without allowing
lower-level artifacts to redefine higher-level concepts.

The repository therefore needs an explicit rule for architectural
responsibility and a deterministic application order for the Phase 3B
alignment work.

---

## 2. Analysis

### 2.1 Layer Responsibility

The same concept appears in multiple layers for different purposes:

- normative documents define the model;
- Runtime realizes the model operationally;
- SDK exposes the model programmatically;
- Tools consume the model in capability/security/invocation surfaces;
- Examples demonstrate the model.

When this distinction is blurred, lower-level artifacts begin redefining
lifecycles, identifiers or semantics that should only come from the normative
layer.

### 2.2 Application Order

Phase 3A established the canonical model. Phase 3B must now propagate it in a
strict order so each downstream layer consumes already-canonical semantics:

`ADR → RFC → RUNTIME → SDK → TOOLS → EXAMPLES → AUDIT-004`

This prevents Examples from inventing concepts before RFC/Runtime/SDK/Tools are
aligned and prevents the SDK or Tools from diverging from Runtime behavior.

---

## 3. Decisions

- **D-001:** Normative documents SHALL define the model. Lower layers MUST NOT
  redefine canonical semantics established by FCP, VCG, ADR and RFC.
- **D-002:** Runtime SHALL implement the model defined by the normative layer.
  Runtime behavior may operationalize the model but MUST NOT contradict or
  replace it.
- **D-003:** SDK SHALL expose the model already defined by the normative layer
  and implemented by Runtime. The SDK MUST NOT introduce competing lifecycles,
  states or semantic categories.
- **D-004:** Tools SHALL consume the canonical model. Tool specifications MUST
  NOT redefine Decision, Authorization, Approval, Resource or lifecycle
  semantics that belong to higher layers.
- **D-005:** Examples SHALL demonstrate canonical concepts only. Examples are
  not a second specification and MUST NOT introduce normative states, fields,
  identifiers, lifecycle values or error codes.
- **D-006:** Phase 3B alignment SHALL be applied in this order:
  `ADR → RFC → RUNTIME → SDK → TOOLS → EXAMPLES → AUDIT-004`.

---

## 4. Consequences

### Positive

- each layer has a clear architectural responsibility;
- semantic authority flows from normative definition to implementation to
  exposure to consumption to demonstration;
- downstream edits become easier to validate because the upstream model is
  already fixed;
- audit work gains a deterministic target order.

### Negative

- changes may need to pause until an upstream layer is corrected first;
- some apparently small downstream edits must wait for normative clarification;
- compliance review becomes stricter across all layers.

---

## 5. Compliance

- Normative documents SHALL define canonical semantics.
- Runtime SHALL implement canonical semantics.
- SDK SHALL expose canonical semantics without redefining them.
- Tools SHALL consume canonical semantics without redefining them.
- Examples SHALL demonstrate canonical semantics without extending them.
- Phase 3B work SHALL proceed in the order `ADR → RFC → RUNTIME → SDK → TOOLS
  → EXAMPLES → AUDIT-004`.

---

## 6. Status

Accepted.

---

## End of ADR
