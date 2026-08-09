# SDK-001 — VIAL SDK Architecture

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** SDK Specification
Depends On:
- FCP-002A
- RFC-002
- RFC-003
- RUNTIME-001
- RUNTIME-002
- RUNTIME-003
- RUNTIME-004
- RUNTIME-005
- RUNTIME-006

---

# 1. Abstract

This document defines the architecture of the **VIAL Software Development Kit (SDK)**.

The SDK provides the programmatic interface through which applications, Resources, Tools and external systems interact with the VIAL Runtime.

The SDK exists to make the VIAL architecture:

* accessible;
* consistent;
* extensible;
* type-safe where applicable;
* observable;
* governed;
* independent of individual Runtime implementations.

The fundamental principle is:

> **The SDK exposes VIAL capabilities without exposing unnecessary Runtime implementation details.**

---

# 2. Purpose

The SDK provides a stable development boundary between applications and the VIAL Runtime.

Conceptually:

```text
Application
     ↓
VIAL SDK
     ↓
VIAL Runtime
     ↓
Organizational Infrastructure
```

The application SHOULD NOT need to know how the Runtime internally implements:

* State;
* Context;
* Memory;
* Cognition;
* Decision;
* Execution.

---

# 3. Architectural Position

The SDK sits above the Runtime.

```text
┌──────────────────────────────┐
│        Applications          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          VIAL SDK            │
├──────────────────────────────┤
│ Organization                 │
│ State                        │
│ Context                      │
│ Memory                       │
│ Cognition                    │
│ Decision                     │
│ Execution                    │
│ Events                       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        VIAL Runtime          │
└──────────────────────────────┘
```

---

# 4. SDK Responsibilities

The SDK SHOULD provide APIs for:

* connecting to an Organization;
* reading State;
* publishing Events;
* retrieving Context;
* accessing Memory;
* requesting Cognition;
* creating Decision proposals;
* requesting Execution;
* registering Resources;
* invoking Tools;
* observing Runtime Events.

---

# 5. SDK Non-Responsibilities

The SDK SHOULD NOT define:

* internal database implementation;
* Runtime scheduling algorithms;
* specific AI models;
* infrastructure deployment;
* hardware implementation;
* storage engine;
* network topology.

Those concerns belong to the Runtime or infrastructure layers.

---

# 6. Design Principle — Stable Boundary

Applications SHOULD depend on SDK contracts rather than Runtime internals.

```text
Application
     ↓
Stable Contract
     ↓
Runtime Implementation
```

Runtime internals MAY evolve without requiring application changes when the public SDK contract remains compatible.

---

# 7. Design Principle — Capability-Oriented

The SDK exposes capabilities rather than implementation mechanisms.

Example:

```text
memory.search()
```

rather than:

```text
vector_database.query()
```

The first expresses an organizational capability.

The second exposes an implementation detail.

---

# 8. Design Principle — Organization First

The SDK SHOULD treat the Organization as the primary logical boundary.

Conceptually:

```text
Organization
 ├── Resources
 ├── State
 ├── Memory
 ├── Context
 ├── Decisions
 ├── Events
 └── Policies
```

Applications SHOULD operate within an explicit organizational scope.

---

# 9. Design Principle — Explicit Context

Operations that depend on organizational Context SHOULD make that dependency explicit.

The SDK SHOULD avoid hidden global Context.

---

# 10. Design Principle — Explicit Authority

The SDK MUST distinguish:

```text
Capability
```

from:

```text
Authority
```

Having an API available does not imply that the caller is authorized to use it.

---

# 11. Design Principle — Async by Default

Operations that interact with distributed Runtime components SHOULD support asynchronous execution.

Examples:

* cognition;
* execution;
* event processing;
* memory retrieval;
* external Tool calls.

---

# 12. Design Principle — Observable Operations

Important SDK operations SHOULD expose identifiers that allow them to be traced.

Example:

```text
Request ID
Cycle ID
Decision ID
Execution ID
Event ID
```

---

# 13. Core SDK Domains

The SDK SHOULD be organized into logical domains.

```text
vial
├── organization
├── state
├── context
├── memory
├── cognition
├── decision
├── execution
├── events
├── resources
├── tools
└── governance
```

The exact package structure is implementation-dependent.

---

# 14. Organization API

The Organization API provides access to organizational scope.

Conceptual operations:

```text
organization.get()
organization.info()
organization.resources()
organization.policies()
```

---

# 15. State API

The State API provides controlled access to organizational State.

Conceptual operations:

```text
state.get()
state.query()
state.observe()
state.subscribe()
```

State mutation SHOULD occur through governed Runtime mechanisms.

---

# 16. Context API

The Context API provides task-relevant Context.

Conceptual operations:

```text
context.create()
context.get()
context.refresh()
context.validate()
```

Context SHOULD be constructed according to Runtime rules rather than assembled arbitrarily by applications.

---

# 17. Memory API

The Memory API exposes organizational Memory.

Conceptual operations:

```text
memory.get()
memory.search()
memory.create()
memory.validate()
memory.update()
memory.supersede()
```

Memory authority and lifecycle rules MUST remain enforced by the Runtime.

---

# 18. Cognition API

The Cognition API allows an application or Resource to request organizational Cognition.

Conceptual operation:

```text
cognition.evaluate()
```

The request SHOULD contain:

```text
Objective
Context
Constraints
Authority
```

---

# 19. Decision API

The Decision API represents organizational Decisions.

Conceptual operations:

```text
decision.propose()
decision.validate()
decision.approve()
decision.reject()
decision.get()
```

Approval MUST remain subject to organizational authority.

---

# 20. Execution API

The Execution API requests actions from authorized Resources.

Conceptual operations:

```text
execution.request()
execution.status()
execution.cancel()
execution.result()
```

Execution MUST NOT bypass authorization.

---

# 21. Events API

The Events API provides communication with the VIAL Event system.

Conceptual operations:

```text
events.publish()
events.subscribe()
events.get()
events.history()
```

Events SHOULD be immutable once published where architectural requirements demand event integrity.

---

# 22. Resource API

The Resource API allows Resources to register and expose capabilities.

Conceptual operations:

```text
resource.register()
resource.get()
resource.capabilities()
resource.status()
```

---

# 23. Tool API

The Tool API provides governed Tool access.

Conceptual operations:

```text
tools.list()
tools.describe()
tools.invoke()
tools.status()
```

Tool invocation MUST respect authorization and governance rules.

For a consequential operation, `tools.invoke()` SHOULD expose or preserve the
following correlation fields:

```text
tool_id
resource_id: RES-*
context_id: CTX-*
decision_id: DEC-*
invocation_id: INV-*
authorization
approval (when required)
outcome
```

The SDK MUST NOT treat a Decision as Authorization or Approval. Invocation is
the governed request that connects an authorized Decision to Tool Execution.

`tools.status()` SHOULD expose the canonical Tool lifecycle state defined by
TOOLS-001 §71 so callers can distinguish an `ACTIVE` Tool from a Tool that is
not eligible for normal invocation.

---

# 24. Governance API

Governance APIs provide access to organizational constraints.

Conceptual operations:

```text
governance.policies()
governance.authority()
governance.permissions()
governance.audit()
```

The SDK audit surface SHOULD support a minimum auditable record for
consequential operations:

```text
organization_id: ORG-*
resource_id: RES-*
context_id: CTX-*
decision_id: DEC-*
invocation_id: INV-*
tool_id
approval (when required)
execution
outcome
timestamp
provenance
correlation_id
```

The record MUST preserve enough correlation to reconstruct the relationship
between Context, Decision, Authorization, Approval, Invocation, Execution and
Outcome. Implementations MAY add fields, but MUST NOT collapse these concepts
into one field or status.

---

# 25. SDK Client

Applications SHOULD interact with VIAL through an SDK Client.

Conceptually:

```text
client = VIALClient(...)
```

The Client provides access to the organization's APIs.

---

# 26. Client Lifecycle

A Client MAY have the following lifecycle:

```text
Initialize
   ↓
Authenticate
   ↓
Authorize
   ↓
Connect
   ↓
Operate
   ↓
Close
```

---

# 27. Authentication

The SDK SHOULD support Runtime-defined authentication mechanisms.

Examples MAY include:

* tokens;
* certificates;
* service identities;
* workload identities.

The SDK MUST NOT assume one authentication technology.

---

# 28. Authorization

Authorization SHOULD be evaluated by the Runtime.

The SDK MAY provide local convenience checks, but local checks MUST NOT replace authoritative Runtime authorization.

---

# 29. Tenant and Organization Isolation

A Client SHOULD operate within an explicit Organization boundary.

Cross-organization access MUST require explicit authorization.

---

# 30. Error Model

The SDK SHOULD expose structured errors.

Conceptually:

```text
VIALError {
    code
    message
    request_id
    details
}
```

Errors SHOULD distinguish between:

```text
Authentication
Authorization
Validation
Runtime
Network
Timeout
Conflict
Unavailable
```

---

# 31. Error Transparency

The SDK SHOULD NOT hide meaningful Runtime failures behind generic errors.

Applications need enough information to decide whether to:

* retry;
* escalate;
* request authorization;
* modify the request;
* stop.

---

# 32. Retry Semantics

The SDK MAY automatically retry operations that are safe to retry.

Retries SHOULD consider:

* idempotency;
* operation type;
* failure type;
* timeout;
* Runtime policy.

---

# 33. Idempotency

Consequential operations SHOULD support idempotency where technically possible.

Example:

```text
execution.request(
    idempotency_key="..."
)
```

This reduces duplicate execution risk.

---

# 34. Timeouts

Distributed SDK operations SHOULD support explicit timeouts.

Applications SHOULD NOT depend exclusively on infinite waits.

---

# 35. Cancellation

Long-running operations SHOULD support cancellation where the underlying Runtime permits it.

Cancellation MUST preserve the actual execution state.

---

# 36. Versioning

The SDK MUST use explicit versioning.

Conceptually:

```text
SDK v1
SDK v2
SDK v3
```

Breaking changes SHOULD require a major version transition.

---

# 37. Backward Compatibility

Minor SDK releases SHOULD preserve compatibility whenever possible.

Deprecated APIs SHOULD have a documented migration path.

---

# 38. API Stability

The SDK SHOULD distinguish:

```text
Stable
Experimental
Deprecated
Internal
```

Applications SHOULD depend primarily on Stable APIs.

---

# 39. Type Safety

Where the implementation language permits, SDK types SHOULD explicitly represent important VIAL concepts.

Examples:

```text
OrganizationID
ResourceID
EventID
MemoryID
DecisionID
ExecutionID
```

This reduces accidental identifier mixing.

---

# 40. Structured Data

SDK objects SHOULD prefer structured representations over unstructured strings for important Runtime concepts.

Example:

```text
Decision
{
    id,
    status,
    authority,
    rationale,
    evidence
}
```

---

# 41. Serialization

SDK objects MAY be serialized for:

* network transport;
* persistence;
* logging;
* auditing;
* caching.

Serialization formats are implementation-dependent.

---

# 42. Event Compatibility

SDK Event structures SHOULD remain compatible with the VIAL Event model defined by the Runtime.

---

# 43. Streaming

The SDK MAY support streaming for:

* Events;
* Cognition progress;
* Execution status;
* State changes.

Streaming SHOULD preserve event ordering where required.

---

# 44. Observability

SDK operations SHOULD expose:

```text
Request ID
Timestamp
Latency
Status
Resource
Operation
```

Applications MAY integrate these with their observability systems.

---

# 45. Logging

The SDK MAY provide structured logging hooks.

Sensitive organizational data SHOULD NOT automatically appear in logs.

---

# 46. Metrics

The SDK MAY expose:

```text
Requests
Errors
Latency
Retries
Timeouts
Throughput
```

Domain-specific metrics remain Runtime responsibilities.

---

# 47. Tracing

Distributed SDK calls SHOULD support trace propagation.

Conceptually:

```text
Application
   ↓ trace_id
SDK
   ↓ trace_id
Runtime
   ↓ trace_id
Resource
```

---

# 48. Security Boundary

The SDK is part of the VIAL security boundary.

It MUST NOT:

* bypass authorization;
* expose secrets unnecessarily;
* disable Runtime governance;
* permit unauthorized cross-organization access.

---

# 49. Secrets

Secrets SHOULD NOT be hard-coded into SDK applications.

The SDK SHOULD support secure credential providers where appropriate.

---

# 50. Local vs Remote Runtime

The SDK SHOULD be capable of interacting with:

```text
Local Runtime
```

and:

```text
Remote Runtime
```

without requiring application-level architectural changes.

---

# 51. Transport Independence

The SDK SHOULD avoid exposing transport-specific concepts in its core API.

The Runtime MAY use:

* HTTP;
* gRPC;
* messaging;
* local IPC;
* other mechanisms.

The application should depend on the SDK contract.

---

# 52. Offline Operation

Where appropriate, SDK modules MAY support limited offline operation.

Offline behavior MUST clearly distinguish:

```text
Local State
```

from:

```text
Authoritative Organizational State
```

---

# 53. Caching

The SDK MAY cache safe read operations.

Caching MUST respect:

* State freshness;
* authorization;
* version;
* invalidation;
* organizational policy.

---

# 54. SDK Extensions

The SDK SHOULD support extensions without modifying its core.

Possible extensions:

```text
Domain SDK
Industry SDK
Equipment SDK
AI SDK
Analytics SDK
```

---

# 55. Domain SDKs

A domain-specific SDK MAY build on top of the Core SDK.

Example:

```text
Industrial SDK
      ↓
VIAL Core SDK
      ↓
VIAL Runtime
```

---

# 56. SDK Plugins

Plugins MAY provide additional capabilities.

Plugins MUST operate within the VIAL security and governance model.

---

# 57. SDK and Tools

Tools are capabilities exposed to the Organization.

The SDK provides the programmatic mechanism for accessing them.

```text
Application
    ↓
SDK
    ↓
Tool API
    ↓
Tool
```

---

# 58. SDK and Resources

Resources may expose capabilities through the SDK.

```text
Resource
    ↓
Capability
    ↓
SDK Interface
```

---

# 59. SDK and Cognition

The SDK MAY allow applications to request Cognition.

However, the SDK does not become the Cognition Engine.

```text
SDK
 ↓ request
Cognition Engine
```

---

# 60. SDK and Memory

The SDK exposes Memory operations but does not own organizational Memory.

Memory remains a Runtime responsibility.

---

# 61. SDK and Execution

The SDK can request Execution.

It does not independently execute organizational actions unless explicitly operating as an authorized local Resource.

---

# 62. Local Resource SDK

A Resource implementation MAY use the SDK to communicate with the Runtime.

Example:

```text
Resource
   ↓
SDK
   ↓
Runtime
```

This enables Resources to participate in the same organizational architecture as external applications.

---

# 63. SDK as Organizational Interface

The SDK should make the VIAL organizational model visible to developers.

Developers should be able to understand:

```text
Organization
 → State
 → Context
 → Memory
 → Cognition
 → Decision
 → Execution
```

without needing to understand internal infrastructure.

---

# 64. Minimal Core

The Core SDK SHOULD remain small.

Features should be added only when they represent stable organizational capabilities.

This prevents the SDK from becoming a mirror of every Runtime implementation detail.

---

# 65. SDK Complexity

SDK complexity SHOULD grow more slowly than Runtime complexity.

```text
Runtime Complexity
        ↑
        │
        │
SDK Complexity
        ↑
```

The SDK abstracts complexity rather than reproducing it.

---

# 66. Testing

SDK implementations SHOULD provide:

* unit tests;
* integration tests;
* compatibility tests;
* contract tests;
* security tests.

---

# 67. Contract Testing

SDK contracts SHOULD be testable independently from specific Runtime implementations.

---

# 68. Mocking

The SDK SHOULD provide mechanisms that allow developers to test applications without requiring a production Runtime.

Examples:

```text
Mock State
Mock Memory
Mock Cognition
Mock Decision
Mock Execution
```

---

# 69. Simulation

SDK test environments MAY provide simulated Organizations.

This enables development without affecting production organizational State.

---

# 70. Developer Experience

The SDK SHOULD provide:

* clear documentation;
* predictable APIs;
* examples;
* typed models where possible;
* useful errors;
* migration guides;
* test utilities.

---

# 71. SDK Documentation

Every stable API SHOULD document:

* purpose;
* inputs;
* outputs;
* authorization requirements;
* errors;
* side effects;
* idempotency;
* version compatibility.

---

# 72. SDK Examples

Examples SHOULD demonstrate complete organizational flows.

Example:

```text
Observe State
    ↓
Create Context
    ↓
Retrieve Memory
    ↓
Request Cognition
    ↓
Create Decision
    ↓
Request Execution
    ↓
Observe Outcome
```

These examples will be defined in the **Examples** documentation phase.

---

# 73. SDK Governance

Changes to stable SDK APIs SHOULD follow the VIAL governance process.

Breaking changes SHOULD require explicit architectural review.

---

# 74. SDK Evolution

The SDK SHOULD evolve according to:

```text
Runtime Capability
       ↓
Stable Contract
       ↓
SDK API
       ↓
Developer Adoption
       ↓
Feedback
       ↓
Evolution
```

---

# 75. Non-Goals

SDK-001 does not define:

* concrete programming language;
* concrete package manager;
* concrete transport;
* concrete authentication provider;
* concrete database;
* concrete AI provider;
* concrete cloud infrastructure;
* detailed API signatures.

Those belong to subsequent SDK specifications and implementation documentation.

---

# 76. Conformance Requirements

A VIAL SDK conforming to SDK-001 MUST:

1. expose stable organizational capabilities;
2. preserve Organization boundaries;
3. respect Runtime authorization;
4. distinguish capability from authority;
5. provide structured error handling;
6. support explicit versioning;
7. preserve traceability for consequential operations;
8. avoid exposing unnecessary Runtime implementation details;
9. support the fundamental VIAL organizational model;
10. remain compatible with the defined Runtime contracts.

---

# 77. Recommended Capabilities

A mature SDK SHOULD provide:

* typed identifiers;
* asynchronous APIs;
* streaming;
* retries;
* idempotency;
* cancellation;
* tracing;
* metrics;
* structured logging;
* testing utilities;
* simulation;
* extension mechanisms.

---

# 78. Final Principles

### Principle 1 — SDK Is a Boundary

> The SDK separates application development from Runtime implementation.

### Principle 2 — Capabilities Over Internals

> Developers consume organizational capabilities, not infrastructure mechanisms.

### Principle 3 — Organization Is the Boundary

> SDK operations occur within explicit organizational scope.

### Principle 4 — Authority Is Explicit

> Access to an API does not imply permission to perform an operation.

### Principle 5 — Stable Contracts

> Runtime evolution should not unnecessarily break applications.

### Principle 6 — Observable by Design

> Important operations must remain traceable.

### Principle 7 — Small Core

> The SDK should expose what is architecturally stable, not everything the Runtime can do.

---

# 79. Final Statement

The VIAL SDK is the primary developer-facing interface to the VIAL organizational architecture.

It translates the concepts defined by the Foundation, RFCs and Runtime into usable software interfaces.

Its purpose can be summarized as:

```text
VIAL Architecture
       ↓
Stable Contracts
       ↓
SDK
       ↓
Applications & Resources
```

The SDK therefore becomes the bridge between **VIAL as an organizational architecture** and **VIAL as a software ecosystem**.

> **The SDK should make VIAL easy to use without making VIAL's architecture invisible.**

# End of SDK-001
