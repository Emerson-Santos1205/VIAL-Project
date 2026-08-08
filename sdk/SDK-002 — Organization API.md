# SDK-002 — VIAL Organization API

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** SDK Specification
**Depends On:** SDK-001 — Architecture, FCP-002A — TDOC, RFC-002, RFC-003

---

# 1. Abstract

This document defines the **VIAL Organization API**.

The Organization is the fundamental logical boundary of the VIAL architecture.

The Organization API provides the SDK interface for identifying, accessing, observing and interacting with an Organization.

The fundamental principle is:

> **Every meaningful VIAL operation occurs within an explicit organizational context.**

---

# 2. Purpose

The Organization API provides applications and Resources with a consistent interface for:

* identifying an Organization;
* retrieving Organization information;
* accessing organizational configuration;
* discovering organizational Resources;
* accessing organizational capabilities;
* observing organizational status;
* accessing applicable policies;
* maintaining organizational boundaries.

---

# 3. Organizational Model

The fundamental structure is:

```text
Organization
│
├── Resources
├── State
├── Context
├── Memory
├── Cognition
├── Decisions
├── Execution
├── Events
├── Tools
└── Policies
```

The Organization acts as the principal boundary connecting these elements.

---

# 4. Organization Identity

Every Organization MUST have a unique identifier.

Conceptually:

```text
OrganizationID
```

The identifier MUST be stable within its defined scope.

---

# 5. Organization API

The Organization API SHOULD provide:

```text
organization.get()
organization.info()
organization.status()
organization.resources()
organization.capabilities()
organization.policies()
organization.events()
```

---

# 6. Organization Client

The SDK Client SHOULD operate within an explicit Organization.

Conceptually:

```text
client.organization
```

An application SHOULD NOT implicitly operate across Organizations.

---

# 7. Organization Selection

A Client MAY be initialized with an Organization:

```text
VIALClient(
    organization_id = ...
)
```

The Runtime MUST validate whether the authenticated identity is authorized to access that Organization.

---

# 8. Organization Information

Conceptual response:

```text
Organization {
    id
    name
    description
    status
    version
    created_at
    updated_at
}
```

Additional fields MAY be provided by the Runtime.

---

# 9. Organization Status

The Organization SHOULD expose a status.

Possible states include:

```text
ACTIVE
DEGRADED
SUSPENDED
MAINTENANCE
UNAVAILABLE
```

The exact state model MAY be extended by the Runtime.

---

# 10. Organization Lifecycle

An Organization MAY follow:

```text
CREATED
   ↓
ACTIVE
   ↓
DEGRADED
   ↓
SUSPENDED
   ↓
ARCHIVED
```

Not every implementation needs to expose every lifecycle state.

---

# 11. Organization Resources

Resources belong to or operate within an Organization.

Conceptually:

```text
organization.resources()
```

The Resource API is defined separately in:

**SDK-003 — Resource API**

---

# 12. Organization Capabilities

The SDK MAY expose capabilities available to the Organization.

Example:

```text
organization.capabilities()
```

Possible capabilities:

```text
Memory
Cognition
Execution
Tools
Events
State
External Integration
```

Capability discovery MUST NOT bypass authorization.

---

# 13. Organization Policies

An Organization MAY define policies governing its operation.

Conceptually:

```text
organization.policies()
```

Policies MAY define:

* operational limits;
* authority;
* security;
* data access;
* execution constraints;
* Resource behavior;
* governance requirements.

---

# 14. Policy Authority

The SDK provides access to organizational policy information where authorized.

The SDK MUST NOT independently override organizational policies.

---

# 15. Organization Configuration

The API MAY expose organizational configuration.

Examples:

```text
Timezone
Locale
Operational Mode
Feature Flags
Limits
Integration Settings
```

Sensitive configuration SHOULD NOT be exposed unless authorized.

---

# 16. Organization Boundaries

Organization boundaries MUST be enforced by the Runtime.

An authenticated identity associated with:

```text
Organization A
```

MUST NOT automatically access:

```text
Organization B
```

---

# 17. Cross-Organization Access

Cross-Organization access MAY exist where explicitly authorized.

Such access SHOULD be:

* explicit;
* limited;
* auditable;
* policy-controlled.

---

# 18. Organization Context

The Organization provides the root context for SDK operations.

Conceptually:

```text
Organization
     ↓
Resource
     ↓
Operation
```

and:

```text
Organization
     ↓
State
     ↓
Context
     ↓
Decision
```

---

# 19. Organization and Resources

Resources operate on behalf of or within an Organization.

Examples:

```text
Human Operator
AI Agent
Software Service
Industrial Equipment
Sensor
External System
```

The detailed Resource model belongs to SDK-003.

---

# 20. Organization and State

The Organization contains the logical State of the organizational system.

```text
Organization
      ↓
State
```

State is not necessarily stored physically inside one system.

The Runtime provides the authoritative organizational view.

---

# 21. Organization and Memory

Memory belongs to the organizational cognitive architecture.

```text
Organization
      ↓
Memory
```

Memory access MUST remain subject to organizational policies.

---

# 22. Organization and Context

Context is created within an organizational scope.

```text
Organization
      ↓
Context
```

A Context MUST identify the Organization to which it belongs.

---

# 23. Organization and Cognition

Cognition operates within organizational Context.

```text
Organization
      ↓
Context
      ↓
Cognition
```

The Organization defines the authority and constraints under which Cognition operates.

---

# 24. Organization and Decision

Decisions are organizational artifacts.

```text
Organization
      ↓
Decision
```

A Decision SHOULD be traceable to:

* Organization;
* Context;
* authority;
* evidence;
* responsible Resource.

---

# 25. Organization and Execution

Execution occurs within organizational authority.

```text
Organization
      ↓
Decision
      ↓
Execution
```

The Organization determines whether the relevant Resource has authority to execute the requested action.

---

# 26. Organization and Events

Events SHOULD identify the Organization in which they occurred.

Conceptually:

```text
Event {
    id
    organization_id
    source
    type
    timestamp
}
```

---

# 27. Organization Event Stream

Applications MAY subscribe to organizational Events.

Conceptually:

```text
organization.events.subscribe()
```

Access MUST be authorized.

---

# 28. Organization Membership

An Organization MAY contain multiple identities.

Examples:

```text
Human
Service
Agent
Resource
Application
```

Membership and roles are governed by the Runtime.

---

# 29. Organization Roles

The Organization MAY define roles.

Examples:

```text
Administrator
Operator
Observer
Developer
Agent
Service
```

Roles are organizational concepts and SHOULD NOT be hard-coded into the Core SDK.

---

# 30. Organization Authority

Authority determines what an identity or Resource is permitted to do.

The SDK MAY expose authority information.

However:

> **The Runtime remains the authoritative source for authorization.**

---

# 31. Organization Identity vs User Identity

The SDK MUST distinguish:

```text
Organization Identity
```

from:

```text
Actor Identity
```

For example:

```text
Organization:
Factory-A

Actor:
Operator-17
```

---

# 32. Acting on Behalf Of

A Resource MAY act on behalf of another identity.

Example:

```text
Human
   ↓ authorizes
AI Agent
   ↓ acts within
Organization
```

Delegation MUST be explicit.

---

# 33. Organization Metadata

The SDK MAY expose organizational metadata.

Examples:

```text
Name
Description
Industry
Location
Timezone
Version
Tags
```

Sensitive information MUST remain protected.

---

# 34. Organization Version

The Organization MAY have a configuration or structural version.

This allows applications to detect significant organizational changes.

---

# 35. Organization Health

Conceptual API:

```text
organization.health()
```

Health information MAY include:

```text
Runtime
Resources
Connectivity
State
Memory
Execution
Integrations
```

---

# 36. Health vs Status

The SDK SHOULD distinguish:

```text
Organization Status
```

from:

```text
Organization Health
```

Status represents the organizational lifecycle.

Health represents operational condition.

---

# 37. Organization Discovery

The SDK MAY support discovery of Organizations available to the authenticated identity.

Conceptually:

```text
client.organizations()
```

The result MUST contain only Organizations the identity is authorized to discover.

---

# 38. Organization Selection After Discovery

An application MAY select an Organization after discovery.

```text
Organizations
      ↓
Select Organization
      ↓
Create Organization Context
```

---

# 39. Organization Session

A Client MAY establish an Organization-scoped session.

Conceptually:

```text
OrganizationSession
```

The session SHOULD preserve:

* Organization ID;
* identity;
* authorization context;
* Runtime connection;
* correlation metadata.

---

# 40. Session Expiration

Organization sessions MAY expire.

The SDK SHOULD expose expiration rather than silently continuing with invalid credentials.

---

# 41. Organization Configuration Changes

Changes to organizational configuration SHOULD be auditable.

Examples:

```text
Policy Changed
Resource Added
Capability Enabled
Authority Changed
Integration Added
```

---

# 42. Organization Events

Such changes MAY generate Events.

Example:

```text
organization.policy.changed
organization.resource.added
organization.capability.enabled
```

---

# 43. Organization Snapshot

The Runtime MAY provide an organizational snapshot.

Conceptually:

```text
organization.snapshot()
```

A snapshot MAY include:

```text
Resources
Capabilities
Policies
Configuration
Status
Version
```

---

# 44. Snapshot Consistency

Snapshots SHOULD identify their version or timestamp.

Applications SHOULD NOT assume that a snapshot remains current indefinitely.

---

# 45. Organization Queries

The SDK MAY support structured Organization queries.

Queries SHOULD be limited to information authorized for the caller.

---

# 46. Organization Search

Where multiple Organizations are available, the SDK MAY provide search.

Example:

```text
organizations.search(...)
```

Search results MUST respect access controls.

---

# 47. Organization Isolation

The SDK MUST prevent accidental mixing of organizational data.

For example, an application SHOULD NOT be able to submit:

```text
Organization A Context
```

to:

```text
Organization B Cognition
```

without explicit authorization.

---

# 48. Organization-Scoped Identifiers

Where practical, SDK identifiers SHOULD carry enough context to prevent accidental cross-Organization operations.

---

# 49. Organization-Aware Requests

Requests SHOULD contain organizational identity when required.

Conceptually:

```text
RequestContext {
    organization_id
    request_id
    correlation_id
}
```

---

# 50. Organization Authorization

Every sensitive Organization operation MUST be authorized.

Examples:

```text
Read Policy
Modify Configuration
Register Resource
Request Execution
Access Memory
```

---

# 51. Organization Auditability

Important organizational operations SHOULD produce audit information.

The system SHOULD be able to answer:

```text
Who?
What?
When?
Which Organization?
Which Resource?
Which Policy?
What Result?
```

---

# 52. Organization Security

The Organization API MUST:

1. enforce organizational boundaries;
2. respect authentication;
3. respect authorization;
4. protect sensitive configuration;
5. preserve auditability;
6. prevent accidental cross-Organization access.

---

# 53. Organization API Errors

Possible errors include:

```text
ORGANIZATION_NOT_FOUND
ORGANIZATION_UNAVAILABLE
ORGANIZATION_SUSPENDED
ORGANIZATION_UNAUTHORIZED
ORGANIZATION_ACCESS_DENIED
ORGANIZATION_INVALID
```

---

# 54. Organization Operations

Conceptual operations:

```text
organization.get()
organization.status()
organization.health()
organization.resources()
organization.capabilities()
organization.policies()
organization.snapshot()
organization.events()
```

---

# 55. Read Operations

Read operations SHOULD be safe and preferably idempotent.

Examples:

```text
organization.get()
organization.status()
organization.health()
```

---

# 56. Mutating Operations

Where supported, organizational mutation operations MUST require explicit authority.

Examples:

```text
organization.update()
organization.configure()
organization.suspend()
organization.archive()
```

These operations are not automatically part of every SDK implementation.

---

# 57. Dangerous Operations

High-impact organizational operations SHOULD require stronger authorization.

Examples:

```text
Suspend Organization
Change Authority
Change Critical Policy
Archive Organization
```

The SDK SHOULD make such operations explicit.

---

# 58. Organization Lifecycle Management

Lifecycle management SHOULD remain under Runtime governance.

The SDK provides the interface, not independent lifecycle authority.

---

# 59. Multi-Organization Applications

Applications MAY operate with multiple Organizations.

However, each operation MUST maintain explicit organizational context.

Example:

```text
Organization A
    ↓
Context A

Organization B
    ↓
Context B
```

---

# 60. Multi-Organization Isolation

Applications MUST NOT accidentally reuse:

* Context;
* Memory references;
* State;
* authorization;
* Resource identifiers

between Organizations.

---

# 61. Organization Switching

If the SDK supports switching Organizations, the transition SHOULD explicitly reset or replace organization-scoped context.

---

# 62. Organization Cache

Organization information MAY be cached.

Cached information SHOULD include freshness metadata.

---

# 63. Organization Consistency

The SDK SHOULD clearly indicate whether organizational information is:

```text
Authoritative
Cached
Historical
Eventually Consistent
```

---

# 64. Organization Observability

Organization operations SHOULD expose:

```text
RequestID
OrganizationID
Timestamp
SDK Version
Runtime Version
Latency
Status
```

---

# 65. Organization Metrics

The SDK MAY expose:

```text
Organization Requests
Organization Errors
Organization Latency
Organization Availability
```

---

# 66. Organization Extensions

Organizations MAY define domain-specific metadata or capabilities.

The SDK SHOULD permit extensions without compromising the Core Organization contract.

---

# 67. Domain Extensions

Examples:

```text
Industrial Organization
Healthcare Organization
Financial Organization
Research Organization
Enterprise Organization
```

The core Organization model remains consistent.

---

# 68. Organization API and Resource API

The Organization API identifies and scopes Resources.

```text
Organization
      ↓
Resource
```

Resource-specific behavior belongs to **SDK-003 — Resource API**.

---

# 69. Organization API and Context API

The Organization provides the scope in which Context is created.

```text
Organization
      ↓
Context
```

Context-specific behavior belongs to **SDK-004 — Context API**.

---

# 70. Organization API and State API

State is organizational information.

```text
Organization
      ↓
State
```

State-specific behavior belongs to **SDK-001 §15 (State API)**.

---

# 71. Organization API and Memory

Memory is organizational Memory.

The Organization determines the boundary under which Memory exists.

---

# 72. Organization API and Cognition

Cognition operates under organizational constraints and authority.

---

# 73. Organization API and Decision

Decisions belong to the organizational decision process.

---

# 74. Organization API and Execution

Execution must occur within organizational authority.

---

# 75. Organization API and Tools

Tools are exposed to an Organization according to capability and authorization.

---

# 76. Organization API and Governance

Governance determines organizational authority, policies and constraints.

---

# 77. Recommended Usage Pattern

A typical application flow is:

```text
Authenticate
    ↓
Discover Organization
    ↓
Select Organization
    ↓
Establish Organization Context
    ↓
Discover Resources
    ↓
Observe State
    ↓
Create Context
    ↓
Cognition
    ↓
Decision
    ↓
Execution
```

---

# 78. Conceptual Example

```text
organization = client.organization.get()

if organization.status == ACTIVE:

    resources = client.organization.resources()

    capabilities = client.organization.capabilities()
```

The exact syntax is implementation-dependent.

---

# 79. Conformance Requirements

An implementation conforming to SDK-002 MUST:

1. represent Organization identity;
2. support Organization-scoped operations;
3. enforce organizational boundaries;
4. expose Organization status;
5. provide authorized Organization information;
6. support Resource discovery;
7. expose applicable organizational capabilities;
8. respect organizational policies;
9. preserve organizational auditability;
10. prevent unauthorized cross-Organization access.

---

# 80. Recommended Capabilities

A mature implementation SHOULD additionally provide:

* Organization discovery;
* Organization sessions;
* Organization snapshots;
* health checks;
* configuration metadata;
* event subscriptions;
* capability discovery;
* multi-Organization support;
* organizational lifecycle information.

---

# 81. Final Principles

### Principle 1 — Organization Is the Root

> Every VIAL operation exists within an organizational boundary.

### Principle 2 — Identity Is Explicit

> Organization identity must never be implicit when it affects authorization or data access.

### Principle 3 — Isolation Is Mandatory

> Organizational data and authority must remain isolated.

### Principle 4 — Authority Is Runtime-Controlled

> The SDK exposes organizational capabilities but never replaces Runtime authorization.

### Principle 5 — Organization Is More Than a Container

> The Organization defines the scope in which Resources, State, Memory, Cognition, Decisions and Execution become meaningful.

---

# 82. Final Statement

The Organization API establishes the first concrete interface of the VIAL SDK.

It provides the root from which the remaining SDK architecture can be understood:

```text
                 ORGANIZATION
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    RESOURCES       STATE        CONTEXT
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                   MEMORY
                      │
                      ▼
                  COGNITION
                      │
                      ▼
                   DECISION
                      │
                      ▼
                  EXECUTION
```

The Organization is therefore not merely an administrative object.

It is the **fundamental boundary of identity, authority, knowledge and action in VIAL**.

> **The Organization defines where VIAL exists, who participates, what is known, what may be decided, and what may be executed.**

# End of SDK-002
