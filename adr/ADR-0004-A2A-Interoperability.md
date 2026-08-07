# Architecture Decision Record

# ADR-0004 — Positioning Against External Agent Interoperability Protocols (A2A)

**Status:** Proposed
**Date:** 2026-08-07
**Decision Type:** Architecture
**Related:** ADR-0001, ADR-0002, FCP-001, FCP-002, RFC-007 through RFC-010

---

## 1. Context

VIAL is defined as a distributed cognitive architecture (ADR-0001), not as a communication protocol.

The industry has produced external interoperability standards for agent systems:

- **A2A (Agent2Agent)**: open standard, originated by Google, now governed by the Linux Foundation. Defines communication between independent, opaque agents via Agent Card, Task, Message/Part/Artifact, and protocol bindings (JSON-RPC, gRPC, HTTP).
- **MCP (Model Context Protocol)**: agent-to-tool protocol (context retrieval and tool invocation).

These standards are becoming the de facto transport layer for agent ecosystems.

VIAL must determine how it relates to these standards.

Specifically, VIAL must determine whether:

- external protocols replace VIAL concerns;
- external protocols conflict with VIAL's organizational-cognition model;
- external protocols can be adopted as implementation components without violating VIAL's architectural identity.

---

## 2. Analysis

### 2.1 Scope Comparison

A2A standardizes communication and task delegation between agents.

A2A explicitly does not manage:

- organizational state;
- shared memory;
- context construction;
- cognitive reuse;
- authority or governance;
- cost or provenance across the organization.

VIAL standardizes organizational cognition: persistent state, selective context, cognitive reuse, authority, evidence, provenance, cost.

### 2.2 Unit of Abstraction

A2A treats the agent as the primary opaque unit.

VIAL treats the Organization as the primary cognitive abstraction (ADR-0002), with agents as replaceable execution resources.

### 2.3 State Handling

A2A keeps agent internals opaque and does not define shared organizational state.

VIAL treats the Organizational Cognitive State (OCS) as the authoritative representation of organizational cognition.

### 2.4 The Uncovered Layer

The A2A ecosystem acknowledges that it does not link an agent's internal context, tool state, and task identifiers into a single traceable thread, and that agent memory has no common interface.

This uncovered layer is precisely the layer VIAL defines: organizational memory, persistent state, selective context, reuse, authority, and auditability.

---

## 3. Decision

VIAL SHALL treat external agent interoperability protocols (A2A, MCP, and successors) as **implementation components of the transport layer**, not as competitors to the architectural identity.

VIAL SHALL NOT redefine or reimplement message transport, agent discovery, or tool invocation where an external standard already provides them.

VIAL SHALL NOT adopt external protocols as a replacement for its organizational-cognition model.

A VIAL organization MAY delegate work to external agents through these protocols.

An execution resource SHALL be allowed to expose or consume A2A Agent Cards, MCP servers, or equivalent interfaces.

External protocol constructs (Agent Card, Task, Message, Part, Artifact) SHALL be mapped onto VIAL constructs (Capability, Decision, Evidence, Artifact) when they cross the organizational boundary.

---

## 4. Mapping of External Constructs

| External Construct (A2A/MCP) | VIAL Construct |
|---|---|
| Agent Card | Capability declaration of an Execution Resource |
| AgentSkill | Capability |
| Task | Decision (or sub-decision) under VIAL authority |
| Message / Part | Evidence or Input within a VIAL Decision |
| Artifact | Artifact produced by a Decision |
| Protocol Binding | Transport implementation detail |

---

## 5. Rationale

### 1. Complementary Scope

External protocols solve transport and inter-agent message exchange.

VIAL solves organizational cognition.

They address different layers.

### 2. No Architectural Conflict

Nothing in A2A or MCP contradicts the TDOC model.

Delegating work to an opaque external agent does not require giving that agent ownership of organizational memory.

### 3. Ecosystem Compatibility

Adopting A2A/MCP as transport increases interoperability with third-party agents and tools without changing VIAL's architecture.

### 4. Preserves Organizational Identity

External protocols become interchangeable implementation details.

The Organization remains the primary cognitive abstraction.

---

## 6. Consequences

### Positive

- interoperability with third-party agents and tools;
- reduced implementation burden (transport is not reimplemented);
- vendor neutrality reinforced;
- VIAL positioning as the cognitive substrate beneath the agent-to-agent transport layer;
- clarity for future RFCs deriving implementation bindings.

### Negative

- boundary mapping between external constructs and VIAL constructs must be specified;
- external agents are opaque; their internal cognition is not governed by VIAL;
- protocol evolution (versioning of A2A/MCP) must be tracked.

---

## 7. Rejected Alternative

### A2A/MCP as the Primary Abstraction

Rejected.

Reason:

Adopting an agent-to-agent protocol as the primary abstraction contradicts ADR-0001 and ADR-0002.

It would make communication, not organizational cognition, the central concern.

---

## 8. Compliance

Future specifications SHALL NOT redefine agent-to-agent or agent-to-tool transport when an external standard already provides it.

Future specifications SHALL NOT claim that VIAL conformance depends on any specific transport protocol.

Future RFCs MAY derive from this ADR to specify concrete bindings (for example, exposing a VIAL organization through an A2A Agent Card).

---

## 9. Status

Proposed for approval.

---

## End of ADR
