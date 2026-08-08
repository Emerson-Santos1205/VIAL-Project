# VIAL Platform

# Contributing Guide

Version: 1.0.0
Status: Draft
Type: Normative

---

## 1. Purpose

This document defines how contributors participate in the development of the VIAL Platform specification, implementations, documentation, tools and ecosystem.

The objective is to maintain:

* architectural consistency;
* semantic stability;
* technical quality;
* auditability;
* reproducibility;
* long-term maintainability.

All contributions SHALL comply with the VIAL Governance Model.

---

## 2. Before Contributing

Contributors SHOULD understand the following documents before proposing architectural changes:

1. `fundation/FP-001-Problem-Statement.md`
2. `fundation/FCP-002-First-Principles.md`
3. `fundation/VCG-001-Canonical-Glossary.md`
4. `fundation/TDC/README.md`
5. `adr/ADR-0000-Governance.md`

Contributors SHALL NOT introduce architectural concepts that contradict these documents.

---

## 3. Contribution Types

Contributions are divided into the following categories:

### 3.1 Foundation

Changes to:

* FCP documents;
* foundational principles;
* canonical terminology;
* TDOC.

### 3.2 Architecture

Changes requiring architectural decisions SHALL be proposed through an ADR.

### 3.3 Specification

Technical behavior SHALL be proposed through an RFC.

### 3.4 Implementation

Changes to:

* Runtime;
* SDK;
* CLI;
* validators;
* tools;
* reference implementations.

### 3.5 Documentation

Improvements to:

* explanations;
* examples;
* tutorials;
* diagrams;
* documentation structure.

### 3.6 Benchmark

Changes to:

* benchmark methodology;
* performance tests;
* conformance tests;
* evaluation metrics.

---

## 4. Architectural Changes

Contributors MUST NOT directly modify architectural behavior without first establishing the required ADR.

The expected process is:

```text
Proposal
   ↓
Discussion
   ↓
ADR
   ↓
Review
   ↓
Acceptance
   ↓
RFC
   ↓
Implementation
```

---

## 5. New Concepts

A new fundamental concept MUST:

1. be identified;
2. receive a canonical identifier;
3. be added to the VCG;
4. be evaluated against the TDOC;
5. receive architectural approval when required.

Concept identifiers MUST NOT be reused.

---

## 6. Terminology

Contributors MUST use canonical VIAL terminology.

If an existing term does not adequately represent a new concept, contributors SHOULD propose a new canonical term instead of redefining an existing one.

---

## 7. Pull Requests

Every pull request SHOULD contain:

* clear title;
* description of the change;
* motivation;
* affected documents;
* compatibility analysis;
* tests, when applicable.

Architectural pull requests MUST reference the corresponding ADR or RFC.

---

## 8. Documentation Standards

Markdown documents SHOULD:

* use clear headings;
* maintain consistent terminology;
* identify document version;
* identify document status;
* identify normative requirements;
* reference related documents.

Documents MUST NOT contain undocumented architectural contradictions.

---

## 9. Tests

Implementations SHALL include appropriate tests.

Depending on the component, these MAY include:

* unit tests;
* integration tests;
* conformance tests;
* interoperability tests;
* performance tests;
* security tests;
* benchmark tests.

A specification change SHOULD include corresponding validation criteria.

---

## 10. Benchmark Contributions

Benchmark contributions MUST clearly identify:

* objective;
* workload;
* environment;
* metrics;
* baseline;
* expected result;
* reproducibility requirements.

Performance improvements SHALL NOT be accepted solely because they reduce execution time.

The effect on:

* correctness;
* cognitive efficiency;
* auditability;
* interoperability;
* resource consumption

SHALL also be considered.

---

## 11. Breaking Changes

Breaking changes MUST NOT be introduced silently.

They require:

* explicit documentation;
* compatibility analysis;
* migration strategy;
* version increment;
* approval according to the governance model.

---

## 12. Deprecated Features

Deprecated features MUST:

* remain documented;
* identify the replacement;
* provide migration guidance when applicable;
* specify the intended removal path.

---

## 13. Quality Requirements

Contributions SHOULD optimize for:

1. correctness;
2. simplicity;
3. efficiency;
4. interoperability;
5. auditability;
6. scalability;
7. maintainability.

Optimization MUST NOT compromise foundational principles.

---

## 14. Security

Security-sensitive contributions MUST explicitly evaluate:

* authorization;
* authentication;
* data integrity;
* confidentiality;
* isolation;
* abuse scenarios;
* auditability.

Security concerns SHALL take precedence over performance optimization.

---

## 15. Vendor Neutrality

Contributions MUST NOT make a specific vendor, model provider, cloud provider or implementation technology a mandatory architectural dependency unless explicitly justified through the governance process.

Reference implementations MAY use specific technologies.

The VIAL architecture SHALL remain vendor-neutral.

---

## 16. Review Principles

Reviewers SHOULD evaluate contributions against:

* TDOC;
* FCP;
* VCG;
* accepted ADRs;
* applicable RFCs;
* compatibility requirements;
* benchmark requirements.

A contribution that violates a higher-level document MUST NOT be accepted without formally changing or superseding that document.

---

## 17. Contribution Lifecycle

```text
Idea
  ↓
Proposal
  ↓
Review
  ↓
Specification
  ↓
Implementation
  ↓
Validation
  ↓
Acceptance
  ↓
Release
```

---

## 18. Contributor Responsibility

Every contributor is responsible for ensuring that their contribution:

* is technically accurate;
* is properly documented;
* does not introduce unnecessary complexity;
* follows canonical terminology;
* preserves architectural consistency;
* includes appropriate validation.

---

## 19. Governance

This document operates under:

`adr/ADR-0000-Governance.md`

If this document conflicts with a higher-level normative document, the higher-level document takes precedence.

---

## 20. Final Principle

VIAL SHALL evolve through explicit knowledge rather than implicit assumptions.

Every important architectural decision SHOULD be documented.

Every new concept SHOULD have a defined semantic origin.

Every implementation SHOULD be traceable to a specification.

Every specification SHOULD be traceable to the foundation.

---

# End of Document
