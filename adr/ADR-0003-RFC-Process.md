# Architecture Decision Record

# ADR-0003 - RFC Process

**Status:** Proposed
**Version:** 1.0.0
**Date:** 2026-08-07
**Decision Type:** Governance
**Related:** ADR-0000, FCP-002, VCG-001
Depends On: None

---

## 1. Context

VIAL requires a standardized process for creating, reviewing and accepting technical specifications.

The existing governance model (ADR-0000) defines document hierarchy and change management but does not specify the RFC lifecycle in detail.

Technical specifications require a structured process that ensures:

- architectural consistency
- semantic stability
- technical quality
- reproducibility
- interoperability

---

## 2. Decision

VIAL SHALL use the RFC process for all technical specifications at Level 3 of the normative hierarchy.

RFCs are the mechanism through which architectural decisions become implementable specifications.

---

## 3. RFC Lifecycle

The RFC lifecycle SHALL follow this sequence:

```text
Draft
  ↓
Review
  ↓
Proposed
  ↓
Accepted
  ↓
Stable
  ↓
Deprecated
  ↓
Archived
```

---

## 4. Status Definitions

### Draft

Initial state.

Open for internal development.

Not yet submitted for review.

### Review

Submitted for community review.

Open for comments and feedback.

### Proposed

Review complete.

Awaiting formal acceptance.

### Accepted

Approved for implementation.

Normative for conforming implementations.

### Stable

Mature specification.

No planned changes.

### Deprecated

No longer recommended for new implementations.

Remains available for backward compatibility.

### Archived

Historical reference only.

No longer maintained.

---

## 5. Acceptance Criteria

An RFC SHALL be accepted only if:

- it derives from an approved ADR (when applicable)
- it uses canonical VCG terminology
- it does not contradict higher-level documents
- it includes all required sections
- it addresses security considerations
- it has been reviewed by at least one qualified reviewer
- it includes at least one example

---

## 6. Review Process

Every RFC SHALL undergo the following review process:

1. Author submits Draft
2. Community reviews Draft
3. Author addresses feedback
4. RFC moves to Review
5. Review period (minimum 14 days)
6. Author addresses review feedback
7. RFC moves to Proposed
8. Maintainers evaluate for acceptance
9. RFC moves to Accepted or returns to Review

---

## 7. Breaking Changes

Breaking changes to accepted RFCs MUST:

- be documented in a new RFC
- reference the superseded RFC
- provide migration guidance
- follow the process defined in ADR-0000

---

## 8. Authorship

RFCs MAY be authored by:

- individual contributors
- working groups
- maintainers

All authors MUST be documented.

---

## 9. Conformance

Implementations SHALL conform to accepted RFCs.

Implementations MUST NOT claim VIAL conformance while violating accepted RFCs.

---

## 10. Consequences

### Positive

- structured specification process
- architectural consistency
- technical quality assurance
- reproducibility
- interoperability

### Negative

- additional process overhead
- longer time to specification

---

## 11. Rejected Alternative

### Ad-hoc Specification

Rejected.

Reason: insufficient structure for long-term architectural consistency.

---

## 12. Status

Proposed for approval.

---

## End of ADR
