# VIAL Platform
## VIAL Canonical Glossary (VCG)

---

Document ID: VCG-001

Title: Canonical Glossary

Version: 1.0.0-draft.1

Status: Draft

Category: Foundation

Normative: YES

Depends On:
- FP-001
- FCP-002
---

# Abstract

The VIAL Canonical Glossary (VCG) defines the official semantic vocabulary of the VIAL Platform.

Every normative document SHALL reference concepts defined in this glossary.

The purpose of the VCG is to guarantee semantic consistency, interoperability and long-term stability across the VIAL ecosystem.

No normative term may exist outside the VCG.

---

# 1. Purpose

The VCG establishes:

- the official vocabulary;
- concept identifiers;
- semantic relationships;
- naming conventions;
- canonical definitions;
- evolution rules.

The glossary is normative.

---

# 2. Semantic Rules

Every canonical concept SHALL:

- possess a permanent identifier;
- possess exactly one canonical definition;
- define its relationships;
- define its lifecycle;
- define its invariants;
- reference related documents.

Canonical identifiers MUST never be reused.

No normative term may exist outside the VCG.

Examples MAY instantiate normative concepts, but MUST NOT introduce new normative states, fields, lifecycle values, identifiers or error codes unless explicitly marked as illustrative.

---

# 3. Identifier Convention

Every concept receives a permanent semantic identifier.

Examples:

GOAL-001

ORG-001

OCS-001

OC-001

ROL-001

CAP-001

POL-001

DEC-001

EVD-001

MEM-001

Identifiers remain valid forever.

Definitions may evolve.

Identifiers never change.

---

# 4. Canonical Concepts

---

## GOAL-001

Name

Organizational Goal

Definition

A desired organizational outcome that justifies the existence of a Cognitive Organization.

Properties

- unique
- measurable
- persistent
- auditable

Relationships

Creates:

ORG-001

Depends on:

POL-001

Produces:

DEC-001

---

## ORG-001

Name

Cognitive Organization

Definition

A temporary organizational structure created to achieve one or more goals.

Properties

- dynamic
- adaptive
- governed
- auditable

Relationships

Contains:

ROL-001

Maintains:

OCS-001

Uses:

CAP-001

Governed by:

POL-001

---

## OCS-001

Name

Organizational Cognitive State

Definition

The unique shared cognitive state representing the current organizational reality.

Properties

- unique
- authoritative
- synchronized
- versioned

Relationships

Contains:

OC-001

Updated by:

DEC-001

Observed by:

ROL-001

---

## OC-001

Name

Organizational Cognition

Definition

The accumulated organizational understanding composed of knowledge, intent, context, evidence and state.

Model

Organizational Cognition =

Knowledge

+

Intent

+

Context

+

Evidence

+

State

---

## CAP-001

Name

Capability

Definition

A reusable organizational ability required to perform one or more actions.

---

## ROL-001

Name

Role

Definition

A responsibility assumed inside a Cognitive Organization.

Roles define responsibilities.

Agents perform roles.

Roles are organizational.

Agents are implementation resources.

---

## POL-001

Name

Policy

Definition

A normative rule governing organizational behavior.

Policies constrain decisions.

Policies never execute actions.

---

## RES-001

Name

Resource

Definition

Any actor, system or capacity available to the Organization to perform work.

Resources include AI models, agents, humans, functions, services and external systems.

`execution resource` MAY be used as a contextual description of a Resource acting during execution, but it is not a separate normative type (ADR-0006 D-005).

Properties

- temporary
- replaceable
- auditable

Relationships

Performs:

CAP-001

Used by:

ORG-001

---

## DEC-001

Name

Decision

Definition

An operational determination of what the Organization intends to happen.

A Decision is not itself an Authorization, an Approval or an Execution.

Properties

- auditable
- versioned
- evidence-based

Relationships

Determines:

EXE-001

Requires:

AUTH-001

---

## AUTH-001

Name

Authorization

Definition

Permission granted by the authority model that permits an actor, Resource or operation to act.

Authorization is not a Decision and not an Approval.

Properties

- permission-based
- revocable
- scope-bound
- auditable

Relationships

Granted by:

POL-001

Permits:

EXE-001

---

## APV-001

Name

Approval

Definition

An explicit, attributable act of approval required before an operation may proceed.

Approval is not a Decision and not an Authorization.

Properties

- explicit
- attributable
- auditable
- condition-bound

Relationships

Precedes:

EXE-001

---

## EXE-001

Name

Execution

Definition

The effective realization of an authorized and, where required, approved operation.

Properties

- observable
- attributable
- auditable

Relationships

Follows:

AUTH-001

Follows:

APV-001

---

## INV-001

Name

Invocation

Definition

A request to perform an operation, submitted by an authorized principal through the authority model.

An Invocation is not a Decision, not an Authorization, not an Approval and not Execution.

Properties

- attributable
- auditable
- traceable

Relationships

Follows:

AUTH-001

Follows:

APV-001

Triggers:

EXE-001

---

## OTC-001

Name

Outcome

Definition

The result produced by Execution.

An Outcome is not a Decision, not an Authorization and not the Invocation itself.

Properties

- observable
- attributable
- auditable

Relationships

Follows:

EXE-001

---

## EVD-001

Name

Evidence

Definition

Observable information supporting or rejecting organizational decisions.

Evidence increases organizational confidence.

Evidence never replaces decisions.

---

## MEM-001

Name

Organizational Memory

Definition

Persistent organizational knowledge surviving individual organizations and execution resources.

---

# 5. Semantic Relationships

Goal

↓

creates

↓

Organization

↓

contains

↓

Roles

↓

perform

↓

Capabilities

↓

generate

↓

Decisions

↓

update

↓

Organizational Cognitive State

↓

evolves

↓

Organizational Cognition

↓

stored in

↓

Organizational Memory

---

Decision ≠ Authorization ≠ Approval ≠ Execution

The canonical operational flow is:

```text
Context
   ↓
Decision
   ↓
Authorization
   ↓
Approval (if required)
   ↓
Invocation
   ↓
Execution
   ↓
Outcome
```

Decision determines what must be done. Authorization determines whether it may be done. Approval is an explicit additional authorization required by policy or workflow (Approval ⊂ Authorization workflow, yet Approval ≠ Authorization). Invocation requests the operation. Execution realizes the operation. Outcome is the result of execution.

A Decision MAY exist without being authorized (ADR-0006 D-001).

---

# 6. Reserved Terms

The following words possess canonical meaning.

Goal

Organization

Role

Capability

Policy

Resource

Decision

Authorization

Approval

Invocation

Execution

Outcome

Evidence

Trust

Knowledge

Memory

Intent

Context

State

Organization

Organizational Cognition

Organizational Cognitive State

Organizational Memory

These terms SHALL NOT receive alternative definitions.

---

# 7. Evolution Rules

Definitions MAY evolve.

Identifiers SHALL NOT.

Relationships MAY expand.

Canonical meaning SHALL remain compatible.

Breaking semantic changes require a new identifier.

---

# 8. Semantic Invariants

Every Organization possesses exactly one OCS.

Every Goal creates at least one Organization.

Every Decision updates an OCS.

Every Decision requires Evidence.

Every Capability belongs to at least one Role.

Every Organization follows one or more Policies.

Every OCS belongs to exactly one Organization.

Knowledge survives Organizations.

Agents do not own organizational knowledge.

---

# 9. Graph Representation

The VCG SHALL be representable as a directed semantic graph.

Every concept becomes a graph node.

Every relationship becomes a graph edge.

Future tooling MAY automatically generate:

- documentation;
- diagrams;
- validators;
- SDKs;
- code generators;
- benchmark mappings.

---

# 10. Future Evolution

Future versions of the VCG may introduce additional concepts.

Existing canonical identifiers SHALL remain valid indefinitely.

The VCG is intended to become the semantic registry of the VIAL Platform.

---

End of Document