# SDK-003 — VIAL Resource API

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** SDK Specification
**Depends On:** SDK-001 — Architecture, SDK-002 — Organization API, FCP-002A — TDOC, RFC-002, RFC-003

---

# 1. Abstract

This document defines the **VIAL Resource API**.

A Resource represents an entity capable of participating in the operation of a VIAL Organization.

Resources may provide:

* information;
* capabilities;
* computation;
* cognition;
* tools;
* execution;
* observations;
* services;
* human interaction.

The fundamental principle is:

> **A Resource is an organizational participant with identity, capabilities, authority and observable behavior.**

---

# 2. Purpose

The Resource API provides a standardized interface for:

* identifying Resources;
* discovering Resources;
* inspecting Resource capabilities;
* observing Resource status;
* managing Resource lifecycle information;
* determining Resource availability;
* associating Resources with an Organization;
* tracking Resource activity.

---

# 3. Resource Model

The fundamental relationship is:

```text
Organization
      │
      ├── Resource
      ├── Resource
      ├── Resource
      └── Resource
```

A Resource exists within an organizational scope.

---

# 4. Resource Identity

Every Resource MUST have a unique identifier.

Conceptually:

```text
ResourceID
```

A Resource ID MUST remain stable for the lifetime of the Resource identity unless explicitly re-identified by the Runtime.

---

# 5. Resource Types

Resources MAY represent different categories of organizational participants.

Examples:

```text
Human
AI Agent
Software Service
Application
Industrial Equipment
Machine
Sensor
Actuator
Database
External System
Network Service
Robot
```

The Resource API MUST NOT require every Resource to behave identically.

---

# 6. Resource Classification

A Resource MAY expose:

```text
resource.type
resource.class
resource.category
```

Classification SHOULD describe what the Resource is, while capabilities describe what it can do.

---

# 7. Identity vs Capability

The SDK MUST distinguish:

```text
Resource Identity
```

from:

```text
Resource Capability
```

Example:

```text
Resource:
PumpController-01

Capabilities:
read_state
report_state
execute_command
```

The existence of a capability does not automatically grant authority to use it.

---

# 8. Resource API

The Resource API SHOULD provide:

```text
resource.get()
resource.info()
resource.status()
resource.health()
resource.capabilities()
resource.events()
resource.operations()
```

---

# 9. Resource Discovery

Organizations SHOULD be able to discover Resources.

Conceptually:

```text
organization.resources()
```

or:

```text
resources.list()
```

Discovery MUST respect authorization.

---

# 10. Resource Retrieval

A specific Resource MAY be retrieved by ID.

```text
resource.get(resource_id)
```

The response SHOULD identify:

```text
ID
Type
Name
Status
Capabilities
Organization
Version
```

---

# 11. Resource Information

Conceptual structure:

```text
Resource {
    id
    organization_id
    name
    type
    status
    capabilities
    version
    created_at
    updated_at
}
```

Additional fields MAY be provided.

---

# 12. Resource Name

A Resource MAY have a human-readable name.

Example:

```text
Pump Controller 01
```

Names SHOULD NOT be used as the primary identity.

The Resource ID remains authoritative.

---

# 13. Resource Description

A Resource MAY provide a description explaining its role within the Organization.

---

# 14. Resource Status

A Resource SHOULD expose operational status.

Possible states:

```text
ACTIVE
INACTIVE
STARTING
STOPPING
DEGRADED
UNAVAILABLE
MAINTENANCE
SUSPENDED
FAILED
```

---

# 15. Resource Lifecycle

A Resource MAY follow:

```text
REGISTERED
    ↓
ACTIVE
    ↓
DEGRADED
    ↓
INACTIVE
    ↓
DECOMMISSIONED
```

The exact lifecycle is Runtime-dependent.

---

# 16. Resource Registration

Resources SHOULD be registered with an Organization before participating in organizational operations.

Conceptually:

```text
resource.register()
```

Registration MUST be authorized.

---

# 17. Resource Deregistration

A Resource MAY be removed from an Organization.

Conceptually:

```text
resource.deregister()
```

Deregistration SHOULD preserve historical records where required.

---

# 18. Resource Decommissioning

Decommissioning SHOULD be distinguished from temporary unavailability.

```text
UNAVAILABLE
```

does not necessarily mean:

```text
DECOMMISSIONED
```

---

# 19. Resource Health

Conceptual API:

```text
resource.health()
```

Health MAY include:

```text
Connectivity
Availability
Latency
Error Rate
Operational State
Dependencies
```

---

# 20. Status vs Health

The SDK SHOULD distinguish:

```text
Status
```

from:

```text
Health
```

Status describes lifecycle or operational state.

Health describes the quality of operation.

---

# 21. Resource Availability

A Resource MAY report availability.

Example:

```text
AVAILABLE
BUSY
UNAVAILABLE
UNKNOWN
```

Availability SHOULD NOT be interpreted as authorization.

---

# 22. Resource Capabilities

Resources MAY expose capabilities.

Conceptually:

```text
resource.capabilities()
```

Example:

```text
read_state
report_state
query_memory
request_cognition
request_decision
execute_action
invoke_tool
```

---

# 23. Capability Description

A capability SHOULD describe:

```text
CapabilityID
Description
Version
Status
Constraints
Required Authority
```

---

# 24. Capability Availability

A capability may be:

```text
AVAILABLE
DISABLED
DEGRADED
UNAVAILABLE
RESTRICTED
```

---

# 25. Capability vs Authority

The distinction is fundamental:

```text
Capability
= what the Resource can do

Authority
= what the Resource is allowed to do
```

A Resource may technically possess a capability without being authorized to exercise it.

---

# 26. Resource Authority

The Runtime determines Resource authority.

The SDK MAY expose effective authority information where authorized.

---

# 27. Delegated Authority

A Resource MAY operate under authority delegated by another Resource.

Example:

```text
Human
   ↓
delegates
   ↓
AI Agent
   ↓
executes within defined scope
```

Delegation SHOULD be explicit and auditable.

---

# 28. Resource Role

A Resource MAY have one or more organizational roles.

Examples:

```text
Operator
Agent
Controller
Observer
Service
Sensor
Executor
```

Roles SHOULD NOT replace capability or authorization models.

---

# 29. Resource Relationships

Resources MAY have relationships with other Resources.

Examples:

```text
Controller
    ↓ controls
Pump

Sensor
    ↓ observes
Tank

Agent
    ↓ operates
System
```

---

# 30. Resource Relationships API

The SDK MAY expose:

```text
resource.relationships()
```

Relationships SHOULD identify their semantic type.

---

# 31. Resource Dependencies

A Resource MAY depend on other Resources.

Example:

```text
AI Agent
   ↓ depends on
Memory Service
```

Dependency information MAY be exposed through health or topology APIs.

---

# 32. Resource Topology

The Runtime MAY expose an organizational Resource topology.

Conceptually:

```text
Organization
     │
     ├── Production
     │      ├── Pump
     │      ├── Valve
     │      └── Sensor
     │
     └── Intelligence
            ├── Agent
            └── Memory
```

---

# 33. Resource Location

A Resource MAY have a logical or physical location.

Examples:

```text
Plant A
Line 2
Server Room
Cloud Region
Edge Node
```

Location information is optional.

---

# 34. Resource Metadata

Resources MAY expose metadata such as:

```text
Manufacturer
Model
Version
Environment
Tags
Location
Owner
```

Sensitive metadata MUST remain protected.

---

# 35. Resource Version

A Resource MAY expose its software, firmware or logical version.

Example:

```text
version = 3.2.1
```

---

# 36. Resource Configuration

Resources MAY expose configuration information where authorized.

The SDK MUST NOT assume that all configuration is publicly readable.

---

# 37. Configuration vs State

The SDK MUST distinguish:

```text
Configuration
```

from:

```text
Current State
```

Example:

```text
Configuration:
Maximum temperature = 80°C

State:
Current temperature = 72°C
```

---

# 38. Resource State

A Resource may have its own State.

However:

```text
Resource State
```

is distinct from:

```text
Organizational State
```

The Resource API provides access to Resource identity and operational information, while detailed State semantics belong to **SDK-001 §15 (State API)**.

---

# 39. Resource Observations

Resources MAY report observations.

Example:

```text
Sensor-17
reports:
temperature = 72.4°C
```

Reported observations become organizational information only according to Runtime rules.

---

# 40. Resource Provenance

Information originating from a Resource SHOULD identify that Resource as its source.

---

# 41. Resource Events

Resources MAY emit Events.

Examples:

```text
resource.started
resource.stopped
resource.failed
resource.connected
resource.disconnected
resource.capability.changed
```

---

# 42. Resource Event Stream

Applications MAY subscribe to Resource Events.

Conceptually:

```text
resource.events.subscribe(resource_id)
```

---

# 43. Resource Operations

A Resource MAY participate in operations.

Examples:

```text
Observe
Compute
Reason
Decide
Execute
Report
Communicate
```

The SDK SHOULD distinguish requesting an operation from the Resource actually performing it.

---

# 44. Resource Invocation

Where appropriate:

```text
resource.invoke()
```

MAY request an operation from a Resource.

Invocation MUST be authorized.

---

# 45. Resource Execution

Execution semantics belong primarily to the Execution API.

The Resource API identifies the Resource capable of performing the execution.

---

# 46. Resource Availability Before Execution

Before high-impact operations, the Runtime MAY verify:

```text
Resource Status
Resource Health
Capability
Authority
Dependencies
```

---

# 47. Resource Concurrency

A Resource MAY have limits on concurrent operations.

Example:

```text
maximum_concurrent_operations = 4
```

The Runtime SHOULD enforce such limits.

---

# 48. Resource Capacity

Resources MAY expose capacity information.

Examples:

```text
CPU
Memory
Concurrent Operations
Storage
Throughput
Production Capacity
```

---

# 49. Capacity vs Availability

Capacity describes potential capability.

Availability describes whether the Resource can currently provide it.

---

# 50. Resource Load

A Resource MAY expose operational load.

Example:

```text
load = 82%
```

Load information can be used by scheduling or orchestration systems.

---

# 51. Resource Scheduling

Scheduling is primarily a Runtime responsibility.

The SDK MAY expose scheduling information without implementing the scheduler itself.

---

# 52. Resource Selection

Applications MAY request Resources based on criteria.

Example:

```text
resources.find({
    capability: "image_analysis",
    status: "ACTIVE"
})
```

The Runtime remains responsible for authoritative selection and authorization.

---

# 53. Resource Allocation

Resource allocation MAY be performed by the Runtime.

The SDK SHOULD expose allocation results and status.

---

# 54. Resource Reservation

A Resource MAY support reservation.

Example:

```text
resource.reserve()
```

Reservations SHOULD have:

```text
ResourceID
Requester
Purpose
Expiration
Scope
```

---

# 55. Resource Lease

Long-running reservations MAY use leases.

Example:

```text
Lease {
    id
    resource_id
    holder
    expires_at
}
```

Expired leases SHOULD be automatically invalidated by the Runtime.

---

# 56. Resource Ownership

A Resource MAY have an owner or organizational responsibility.

Ownership MUST NOT automatically imply unrestricted authority.

---

# 57. Resource Identity Lifecycle

Resource identity SHOULD remain distinguishable from the physical or software instance.

For example:

```text
Resource Identity
      ↓
Physical Instance
```

A replacement physical device may represent:

```text
New Resource
```

or:

```text
Continuation of existing Resource identity
```

depending on organizational policy.

---

# 58. Resource Registration Metadata

Registration SHOULD capture enough information to establish:

```text
Identity
Organization
Type
Capabilities
Owner
Version
Security Identity
```

---

# 59. Resource Authentication

Resources SHOULD authenticate before joining an Organization.

Authentication MAY use:

* certificates;
* credentials;
* tokens;
* hardware identity;
* platform identity.

---

# 60. Resource Identity Security

Resource credentials SHOULD be protected independently from Resource metadata.

---

# 61. Resource Trust

The Runtime MAY maintain a trust state for a Resource.

Example:

```text
TRUSTED
UNTRUSTED
PENDING
REVOKED
```

Trust MUST NOT replace authorization.

---

# 62. Resource Revocation

A Resource MAY have its organizational access revoked.

After revocation, Runtime access SHOULD be denied even if the Resource retains technical capabilities.

---

# 63. Resource Isolation

Resources SHOULD only access organizational information necessary for their authorized role.

---

# 64. Resource-to-Resource Interaction

Resources MAY communicate through the Runtime.

Conceptually:

```text
Resource A
    ↓
VIAL Runtime
    ↓
Resource B
```

Direct communication MAY exist where explicitly supported and governed.

---

# 65. Resource-to-Resource Authority

Communication between Resources does not automatically grant authority.

---

# 66. Resource and Organization

The fundamental relationship is:

```text
Organization
      ↓
Resource
```

A Resource MUST have an organizational scope when participating in VIAL operations.

---

# 67. Resource and Context

A Resource MAY create, consume or contribute to Context.

```text
Resource
   ↓
Observation
   ↓
Context
```

---

# 68. Resource and State

A Resource may provide State observations.

```text
Resource
   ↓
Observation
   ↓
State
```

**SDK-001 §15 (State API)** defines the resulting State model.

---

# 69. Resource and Memory

A Resource MAY contribute information to Memory when authorized.

---

# 70. Resource and Cognition

A Resource MAY provide Cognition capabilities.

Example:

```text
AI Agent
    ↓
Cognition capability
```

The Cognition API defines the cognitive interaction.

---

# 71. Resource and Decision

A Resource MAY request or produce Decisions according to its authority.

---

# 72. Resource and Execution

A Resource MAY be an execution target.

Example:

```text
Decision
   ↓
Execution Request
   ↓
Resource
```

---

# 73. Resource and Tools

A Resource MAY provide or consume Tools.

---

# 74. Resource and Governance

Resource behavior is constrained by organizational governance.

```text
Organization Policy
       ↓
Resource Authority
       ↓
Resource Action
```

---

# 75. Resource Observability

Resource operations SHOULD expose:

```text
RequestID
ResourceID
OrganizationID
Timestamp
Status
Latency
```

---

# 76. Resource Auditability

Important Resource operations SHOULD be auditable.

The system SHOULD be able to determine:

```text
Which Resource?
Which Organization?
Which Actor?
Which Operation?
When?
Under Which Authority?
What Result?
```

---

# 77. Resource Errors

Possible errors include:

```text
RESOURCE_NOT_FOUND
RESOURCE_UNAVAILABLE
RESOURCE_UNAUTHORIZED
RESOURCE_REVOKED
RESOURCE_BUSY
RESOURCE_CAPABILITY_UNAVAILABLE
RESOURCE_CONFLICT
RESOURCE_TIMEOUT
RESOURCE_FAILED
```

---

# 78. Resource Health Errors

Health failures SHOULD be distinguished from authorization failures.

For example:

```text
RESOURCE_UNAVAILABLE
```

is different from:

```text
RESOURCE_ACCESS_DENIED
```

---

# 79. Resource Caching

Resource metadata MAY be cached.

Cached information SHOULD include freshness information.

---

# 80. Resource Consistency

Applications SHOULD know whether Resource information is:

```text
AUTHORITATIVE
CACHED
HISTORICAL
EVENTUALLY_CONSISTENT
```

---

# 81. Resource Streaming

The SDK MAY support streaming Resource events and operational updates.

Streaming SHOULD support appropriate:

* backpressure;
* reconnection;
* cursors;
* cancellation.

---

# 82. Resource Discovery Performance

Resource discovery SHOULD support filtering.

Examples:

```text
type
status
capability
location
tag
availability
```

---

# 83. Resource Query Example

Conceptual:

```text
resources.find({
    type: "sensor",
    status: "ACTIVE",
    capability: "temperature"
})
```

---

# 84. Resource Selection Example

```text
resources.find({
    capability: "cognition",
    availability: "AVAILABLE"
})
```

The returned Resources are candidates; the Runtime remains authoritative for final authorization and allocation.

---

# 85. Resource Lifecycle Events

Lifecycle transitions SHOULD generate Events where auditing is required.

Example:

```text
resource.registered
resource.activated
resource.suspended
resource.revoked
resource.decommissioned
```

---

# 86. Resource Degradation

A Resource MAY remain operational while degraded.

Example:

```text
Status:
DEGRADED

Reason:
High latency
```

Applications SHOULD not interpret DEGRADED as equivalent to FAILED.

---

# 87. Resource Maintenance

Maintenance MAY temporarily change availability.

Example:

```text
Status:
MAINTENANCE
```

Maintenance SHOULD be distinguishable from failure.

---

# 88. Resource Dependency Health

A Resource's health MAY depend on other Resources.

Example:

```text
AI Agent
   ↓ depends on
Memory Service
```

If the Memory Service fails, the Agent MAY become DEGRADED.

---

# 89. Resource Capability Versioning

Capabilities MAY evolve independently of Resource identity.

Example:

```text
Resource:
Agent-01

Capability:
cognition.v2
```

---

# 90. Resource API Security Requirements

The Resource API MUST:

1. enforce Organization boundaries;
2. authenticate Resources;
3. respect authorization;
4. protect Resource credentials;
5. distinguish capability from authority;
6. preserve Resource provenance;
7. support revocation;
8. maintain auditability.

---

# 91. Conformance Requirements

An implementation conforming to SDK-003 MUST:

1. represent Resource identity;
2. associate Resources with Organizations;
3. support Resource discovery;
4. expose Resource status;
5. expose Resource capabilities;
6. distinguish capability from authority;
7. support Resource health information;
8. support Resource lifecycle information;
9. preserve Resource provenance;
10. enforce organizational security boundaries.

---

# 92. Recommended Capabilities

A mature implementation SHOULD additionally provide:

* Resource relationships;
* topology;
* capacity;
* load;
* reservations;
* leases;
* event streaming;
* capability versioning;
* trust state;
* revocation;
* Resource selection;
* simulation.

---

# 93. Final Principles

### Principle 1 — Resource Is an Actor

> A Resource is an organizational participant, not merely a technical endpoint.

### Principle 2 — Identity Comes First

> Every Resource must have an explicit identity.

### Principle 3 — Capability Is Not Authority

> What a Resource can do is different from what it is allowed to do.

### Principle 4 — Resources Are Governed

> Resource behavior exists within organizational policy and authority.

### Principle 5 — Resources Are Observable

> Important Resource behavior must remain traceable.

### Principle 6 — Resource Independence

> A Resource may be replaced or upgraded without necessarily changing the conceptual organizational architecture.

---

# 94. Final Statement

The Resource API establishes the second major boundary of the VIAL SDK:

```text
ORGANIZATION
      │
      ▼
   RESOURCE
      │
 ┌────┼────┐
 ▼    ▼    ▼
State Context Capability
```

Resources are the participants through which the Organization observes, reasons and acts.

They may be human, digital, physical or hybrid.

Their technical capability does not determine their organizational authority.

Their authority is established by the VIAL Runtime and organizational governance.

> **Resources provide capability to the Organization; governance determines how that capability may be used.**

# End of SDK-003
