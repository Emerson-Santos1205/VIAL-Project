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

## DEC-001

Name

Decision

Definition

A validated organizational choice capable of modifying the Organizational Cognitive State.

Properties

- auditable
- versioned
- evidence-based

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

# 6. Reserved Terms

The following words possess canonical meaning.

Goal

Organization

Role

Capability

Policy

Decision

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