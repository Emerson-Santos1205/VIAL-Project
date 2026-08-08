# Architecture Decision Record

# ADR-0005 — Document Identity and Reference Normalization

**Status:** Proposed
**Date:** 2026-08-08
**Decision Type:** Governance
**Related:** ADR-0000, ADR-0003, FCP-002A, RFC-0001
Depends On: None

---

## 1. Context

An audit of repository references found broken cross-references between documents:

- Several documents reference `RFC-001` (RFC-002 through RFC-006, RUNTIME-001, FCP-004), but no `RFC-001` exists.
- The repository contains `RFC-0001-Template.md`, a template whose internal document ID is `RFC-0001`.
- The SDK numbering previously debated creating an `SDK-005 — State API`; this was not created.
- `TOOLS-002` through `TOOLS-008` exist as empty, planned files.

The repository must resolve these inconsistencies without inventing documents and without renumbering valid documents.

---

## 2. Analysis

### 2.1 Template vs. Effective Document

`RFC-0001-Template.md` has document ID `RFC-0001` but is explicitly a template (`Title: Template`, `Version: 1.0.0-draft.1`).

It defines the structure for future RFCs; it does not define a conceptual specification.

A reference to `RFC-001` must not be automatically rewritten to `RFC-0001`, because the template is not necessarily the intended dependency.

### 2.2 Renumbering vs. Identity

Renumbering `SDK-005 — Decision API` to a different identifier would break existing references and create churn without justification.

No `SDK-005 — State API` was ever created; therefore no empty slot needs to be filled.

### 2.3 Empty Documents

Empty files are valid placeholders for planned specifications.

They must not be treated as completed documents, and they must not be referenced as dependencies until they have content.

---

## 3. Decisions

- **D-001:** `RFC-0001` is the correct identifier of the existing template. `RFC-001` will not be created automatically.
- **D-002:** `SDK-005` remains the Decision API. No `SDK-005 — State API` will be created.
- **D-003:** `RFC-006` remains a direct dependency of `SDK-005`.
- **D-004:** `TOOLS-002` through `TOOLS-008` are planned/empty documents, not completed documents.
- **D-005:** Existing `RFC-001` references must be audited and corrected individually.
- **D-006:** References within the body of a document carry the same weight as `Depends On` declarations.
- **D-007:** Files will not be renamed solely for style correction until a formal naming convention is established.

---

## 4. Consequences

### Positive

- broken references are resolved without fabricating documents;
- valid identifiers are preserved, avoiding churn;
- empty placeholders remain honest about their state;
- body references are treated with the same rigor as header declarations.

### Negative

- each `RFC-001` reference requires individual judgment (template vs. other intent);
- correctness of the fix depends on manual audit.

---

## 5. Compliance

- `RFC-001` SHALL NOT be introduced as a document identifier.
- References to `RFC-0001` SHALL denote the template `RFC-0001-Template.md` or a future effective RFC-0001, and the intended target SHALL be confirmed per reference.
- Empty documents SHALL NOT be listed as dependencies.
- Body references SHALL be corrected with the same rigor as `Depends On` declarations.

---

## 6. Status

Proposed for approval.

---

## End of ADR
