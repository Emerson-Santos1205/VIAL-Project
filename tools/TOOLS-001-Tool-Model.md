# TOOLS-001 — Tool Model

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Tools Specification
Depends On:
- FCP-002A
- RFC-002
- RFC-003
- RFC-004
- RFC-005
- RFC-006
- SDK-001
- SDK-002
- SDK-003
- SDK-004
- SDK-005

---

# 1. Abstract

This document defines the conceptual and structural model of a **Tool** within VIAL.

A Tool is an externally invocable capability that allows an authorized VIAL component to interact with a defined operational, computational, informational or organizational capability.

The fundamental principle is:

> **A Tool is a controlled capability exposed through an explicit contract and executed within organizational authority.**

A Tool is not itself:

* an Agent;
* a Cognition process;
* a Decision;
* a Resource;
* a Context;
* an arbitrary software function.

A Tool provides a controlled interface through which capabilities can be invoked.

---

# 2. Purpose

The Tool Model establishes the common foundation for:

* Tool identification;
* Tool description;
* Tool capabilities;
* Tool inputs;
* Tool outputs;
* Tool invocation;
* Tool authorization;
* Tool execution;
* Tool errors;
* Tool lifecycle;
* Tool provenance;
* Tool observability.

The model provides the conceptual foundation for the remaining Tools specifications.

---

# 3. Tool Definition

A Tool is a formally identifiable capability that can be invoked through a defined interface.

Conceptually:

```text
Caller
   │
   ▼
 Tool Contract
   │
   ▼
 Authorization
   │
   ▼
 Approval (when required)
   │
   ▼
 Invocation
   │
   ▼
  Tool
   │
   ▼
  Execution
   │
   ▼
 Outcome
```

---

# 4. Tool as Capability

A Tool represents a capability rather than an entity that independently reasons.

Examples:

```text
ReadSensor
QueryDatabase
SendNotification
WriteFile
CalculateValue
ControlEquipment
SearchKnowledge
CallExternalAPI
```

The Tool performs an operation when invoked.

---

# 5. Tool vs Resource

A Resource represents an organizational entity or capability managed by VIAL.

A Tool represents an invocable interface to a capability.

Conceptually:

```text
Resource
    │
    └── Capability
             │
             ▼
           Tool
```

A Tool MAY interact with one or more Resources.

---

# 6. Tool vs Agent

An Agent may decide when and why to use a Tool.

```text
Agent
  │
  ├── Cognition
  │
  └── Tool Invocation
          │
          ▼
         Tool
```

The Tool does not inherently possess organizational intent.

---

# 7. Tool vs Decision

A Decision determines an intended course of action.

A Tool provides the capability to perform or retrieve something associated with that Decision.

```text
Decision
   │
   ▼
Authorization
   │
   ▼
Approval (when required)
   │
   ▼
Tool Invocation
   │
   ▼
Execution
```

---

# 8. Tool vs Context

Context provides the information relevant to a purpose.

A Tool may consume Context information as input or contribute information to a Context.

```text
Context
   │
   ▼
 Tool
   │
   ▼
Result
```

---

# 9. Tool Identity

Every Tool MUST have a unique identifier within its organizational namespace.

Conceptually:

```text
ToolID
```

Example:

```text
tool.sensor.read
tool.database.query
tool.notification.send
```

The identifier SHOULD remain stable across Tool versions.

---

# 10. Tool Name

A Tool SHOULD have a human-readable name.

Example:

```text
Read Temperature Sensor
```

The human-readable name MAY change without changing the Tool identity.

---

# 11. Tool Description

Every Tool SHOULD provide a description explaining:

* what it does;
* what it requires;
* what it returns;
* relevant limitations;
* applicable restrictions.

The description SHOULD be understandable by both humans and machine consumers.

---

# 12. Tool Capability

A Tool MUST expose a clearly defined capability.

Example:

```text
Capability:
read_temperature
```

The capability SHOULD be specific enough to determine the intended operation.

---

# 13. Tool Boundary

A Tool MUST have a defined operational boundary.

The boundary determines:

```text
What the Tool can access
What the Tool can modify
What the Tool cannot access
What operations it can perform
```

A Tool SHOULD NOT implicitly gain capabilities outside its declared boundary.

---

# 14. Tool Contract

Every Tool MUST expose a contract.

The contract defines at minimum:

```text
Identity
Description
Inputs
Outputs
Errors
Invocation semantics
```

Detailed contract requirements are defined in:

**TOOLS-002 — Tool Contract**

---

# 15. Tool Input

Tool inputs MUST be explicitly defined.

Example:

```text
{
    "resource_id": "PUMP-001",
    "parameter": "temperature"
}
```

Undeclared inputs SHOULD be rejected.

---

# 16. Tool Output

Tool outputs MUST have a defined structure.

Example:

```text
{
    "resource_id": "PUMP-001",
    "temperature": 72.4,
    "timestamp": "2026-08-07T14:32:04Z"
}
```

Outputs SHOULD contain sufficient provenance when the information may influence organizational reasoning or Decisions.

---

# 17. Tool Result

A Tool invocation SHOULD produce a structured result.

Conceptually:

```text
ToolResult {
    status
    output
    metadata
    provenance
    error
}
```

---

# 18. Tool Status

Possible execution statuses include:

```text
SUCCESS
FAILED
TIMEOUT
CANCELLED
REJECTED
UNAVAILABLE
PARTIAL
```

The exact status model MAY be extended.

---

# 19. Tool Errors

Tool errors SHOULD be structured.

Example:

```text
{
    "code": "RESOURCE_UNAVAILABLE",
    "message": "Sensor is offline"
}
```

Errors SHOULD be machine-readable.

---

# 20. Tool Invocation

A Tool is activated through an explicit invocation.

Conceptually:

```text
invoke(
    tool_id,
    input
)
```

Invocation MUST be subject to the Tool Contract and authorization rules.

---

# 21. Tool Invocation Identity

Each invocation SHOULD have a unique identifier.

```text
InvocationID
```

Example:

```text
INV-2026-000492
```

This enables traceability.

---

# 22. Tool Caller

Every invocation SHOULD identify the caller.

The caller MAY be:

```text
Human
Agent
Service
Runtime
Organization Process
System
```

---

# 23. Tool Authority

A caller MUST have sufficient authority to invoke the Tool.

Authority MAY depend on:

```text
Organization
Actor
Role
Resource
Purpose
Tool
Operation
Policy
Risk
```

---

# 24. Tool Permissions

Tool permissions SHOULD be explicit.

Example:

```text
Tool:
equipment.control

Permission:
equipment.control.speed

Denied:
equipment.shutdown
```

Permission semantics are further defined in **TOOLS-003 — Tool Security**.

---

# 25. Tool Scope

A Tool invocation MAY be limited by scope.

Example:

```text
Organization:
ORG-001

Resource:
PUMP-001

Operation:
read
```

The Tool MUST NOT exceed the authorized scope.

---

# 26. Read Tools

Read Tools retrieve information without intentionally modifying organizational state.

Examples:

```text
ReadSensor
QueryDatabase
ReadFile
GetResource
```

Read operations SHOULD be distinguished from mutation operations.

---

# 27. Write Tools

Write Tools modify information or organizational state.

Examples:

```text
UpdateDatabase
WriteFile
ChangeConfiguration
```

Write Tools generally require stronger authorization than read Tools.

---

# 28. Action Tools

Action Tools cause or request an operational effect.

Examples:

```text
StartEquipment
StopEquipment
AdjustValve
SendCommand
```

Action Tools SHOULD have explicit risk and authorization requirements.

---

# 29. Destructive Tools

Some Tools can cause irreversible or high-impact effects.

Examples:

```text
DeleteData
ShutdownSystem
DestroyResource
ResetConfiguration
```

Destructive Tools SHOULD require elevated authorization and explicit confirmation where appropriate.

---

# 30. Tool Classification

Tools MAY be classified by operational impact.

Recommended classification:

```text
READ
WRITE
ACTION
DESTRUCTIVE
```

Additional classifications MAY be introduced.

---

# 31. Tool Risk

Every Tool SHOULD have an associated risk classification.

Example:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Risk MAY influence:

* authorization;
* approval;
* confirmation;
* logging;
* monitoring;
* execution restrictions.

---

# 32. Tool Determinism

A Tool SHOULD declare whether its behavior is deterministic.

Possible values:

```text
DETERMINISTIC
NON_DETERMINISTIC
CONDITIONAL
```

Example:

```text
calculate_sum
```

is normally deterministic.

An external search Tool may be non-deterministic because results can change over time.

---

# 33. Tool Side Effects

A Tool MUST declare whether it produces side effects.

Possible values:

```text
NONE
READ_ONLY
MUTATING
EXTERNAL_ACTION
```

This information is important before invocation.

---

# 34. Tool Idempotency

A Tool SHOULD declare whether repeated invocation produces the same effect.

Possible values:

```text
IDEMPOTENT
NON_IDEMPOTENT
UNKNOWN
```

Example:

```text
set_temperature(70)
```

may be idempotent.

```text
increment_counter()
```

is generally non-idempotent.

---

# 35. Tool Timeout

A Tool SHOULD define an expected execution timeout.

The Runtime MAY terminate invocations exceeding the permitted timeout.

---

# 36. Tool Cancellation

Long-running Tool operations SHOULD support cancellation when technically possible.

```text
invoke
  ↓
running
  ↓
cancel
  ↓
cancelled
```

Cancellation semantics MUST be explicit for Tools with side effects.

---

# 37. Tool Retry

Tools MAY support retry.

Retry behavior MUST consider:

```text
Idempotency
Side Effects
Failure Type
Timeout
External State
```

A non-idempotent Tool SHOULD NOT automatically retry without an appropriate safety mechanism.

---

# 38. Tool Availability

A Tool MAY be:

```text
AVAILABLE
DEGRADED
UNAVAILABLE
DISABLED
```

The Runtime SHOULD expose availability where relevant.

---

# 39. Tool Dependencies

A Tool MAY depend on:

```text
Resource
Service
Database
Network
Credential
Another Tool
External API
```

Dependencies SHOULD be declared where practical.

---

# 40. Tool Environment

A Tool MAY declare environmental requirements.

Examples:

```text
Operating System
Network
Hardware
Runtime
Credential
API
Container
```

---

# 41. Tool Version

Tools SHOULD support explicit versions.

Example:

```text
tool.sensor.read@1.2
```

Versioning MUST preserve compatibility rules defined by the Tool Contract.

---

# 42. Tool Compatibility

A Tool version SHOULD declare compatibility information where required.

Changes to input or output semantics SHOULD produce a new compatible or incompatible version according to the project's versioning rules.

---

# 43. Tool Provenance

Tool results SHOULD identify their origin.

Example:

```text
Tool:
sensor.read

Source:
Sensor Gateway 01

Timestamp:
2026-08-07T14:32:04Z
```

---

# 44. Tool Observability

Tool invocations SHOULD generate sufficient telemetry for operational analysis.

Recommended information:

```text
InvocationID
ToolID
Caller
Timestamp
Duration
Status
Error
Resource
```

---

# 45. Tool Auditability

Security-sensitive or consequential Tool invocations MUST be auditable.

The audit record SHOULD establish:

```text
Who invoked the Tool?
Which Tool?
With what authority?
For what purpose?
Against which scope?
When?
What happened?
```

---

# 46. Tool Isolation

Tools SHOULD execute within an appropriate isolation boundary.

Isolation MAY be provided through:

```text
Process
Container
Sandbox
Service Boundary
Permission Boundary
Network Boundary
```

The required isolation depends on Tool risk.

---

# 47. Tool Least Privilege

Tools MUST follow the principle of least privilege.

A Tool SHOULD receive only the permissions necessary for its declared capability.

---

# 48. Tool Credential Isolation

Credentials required by a Tool SHOULD NOT be exposed unnecessarily to callers.

The Runtime SHOULD provide credentials through controlled mechanisms.

---

# 49. Tool Secrets

Secrets SHOULD NOT be embedded directly in Tool definitions or invocation payloads.

Examples:

```text
API Keys
Passwords
Private Keys
Tokens
Credentials
```

Secrets SHOULD be resolved through an appropriate secret-management mechanism.

---

# 50. Tool Network Access

Network access SHOULD be explicitly controlled.

A Tool requiring external communication SHOULD declare its permitted destinations or network scope where practical.

---

# 51. Tool Data Access

Data access SHOULD be explicitly scoped.

Example:

```text
Allowed:
Plant-01 / Production / Sensors

Denied:
HR / Payroll
```

---

# 52. Tool Composition

Tools MAY be composed.

```text
Tool A
  ↓
Tool B
  ↓
Tool C
```

Composition SHOULD preserve the authorization and provenance of each invocation.

---

# 53. Tool Chaining

A Tool result MAY become the input of another Tool.

The Runtime SHOULD preserve invocation relationships.

```text
Invocation A
     ↓
Invocation B
     ↓
Invocation C
```

---

# 54. Tool Recursion

Tool recursion SHOULD be explicitly controlled.

Unrestricted recursive Tool invocation MUST NOT be permitted.

---

# 55. Tool Invocation Depth

The Runtime MAY impose a maximum invocation depth.

Example:

```text
max_depth = 10
```

This prevents uncontrolled execution chains.

---

# 56. Tool Resource Limits

The Runtime MAY impose:

```text
CPU limit
Memory limit
Network limit
Execution time
Invocation count
Storage limit
```

Limits SHOULD reflect Tool risk and operational requirements.

---

# 57. Tool Rate Limits

Tools MAY have invocation rate limits.

Example:

```text
100 invocations / minute
```

Rate limits may protect:

* external services;
* organizational Resources;
* infrastructure;
* costs.

---

# 58. Tool Cost

A Tool MAY expose an estimated execution cost.

Cost may represent:

```text
Compute
Network
Financial
Operational
Resource Consumption
```

Cost SHOULD NOT be confused with monetary price alone.

---

# 59. Tool Preconditions

A Tool MAY require Preconditions.

Example:

```text
Resource must be online
Caller must be authorized
Pressure must be below threshold
```

Preconditions SHOULD be validated before execution.

---

# 60. Tool Postconditions

A Tool MAY define expected Postconditions.

Example:

```text
Valve position = 50%
```

The Runtime MAY verify postconditions after execution.

---

# 61. Tool Safety Boundary

A Tool MUST NOT perform operations outside its declared safety boundary.

For high-risk Tools, safety boundaries SHOULD be enforced independently of the caller's requested input.

---

# 62. Tool Input Validation

Tool inputs MUST be validated before execution.

Validation SHOULD include:

```text
Type
Format
Range
Required Fields
Authorization Scope
Safety Constraints
```

---

# 63. Tool Output Validation

Tool outputs SHOULD be validated before being returned to the caller.

This prevents malformed or unexpected results from propagating through the system.

---

# 64. Tool Result Integrity

Where necessary, results SHOULD include integrity information.

Example:

```text
ResultID
Timestamp
Source
Version
Checksum
```

---

# 65. Tool Context Awareness

A Tool MAY receive Context information when required.

However, a Tool SHOULD receive only the portion of Context necessary for its operation.

---

# 66. Tool Decision Awareness

A Tool MAY be invoked as part of a Decision execution chain.

The Tool SHOULD NOT independently reinterpret the Decision unless explicitly designed to do so.

---

# 67. Tool Governance

Tool governance determines:

```text
Who may register a Tool
Who may invoke it
Who may modify it
Who may disable it
Which policies apply
```

Governance SHOULD remain separate from Tool implementation.

---

# 68. Tool Registration

A Tool SHOULD be registered before becoming available for normal invocation.

Registration SHOULD establish:

```text
ToolID
Version
Contract
Security Policy
Owner
Status
```

Detailed registration semantics belong to **TOOLS-004 — Tool Registry**.

---

# 69. Tool Discovery

Authorized components MAY discover available Tools.

Discovery SHOULD expose enough metadata to determine whether a Tool is appropriate.

Detailed discovery semantics belong to **TOOLS-005 — Tool Discovery**.

---

# 70. Tool Execution

Execution represents the actual operational invocation of a Tool.

The execution layer SHOULD handle:

```text
Validation
Authorization
Approval (when required)
Invocation
Timeout
Cancellation
Outcome
Error
Audit
```

Detailed execution semantics belong to **TOOLS-007 — Tool Execution**.

---

# 71. Tool Lifecycle

A Tool SHOULD have a defined lifecycle.

The canonical lifecycle is:

```text
DRAFT
   ↓
DEFINED
   ↓
ACTIVE
   ↓
DEPRECATED
   ↓
RETIRED
```

Not every Tool must pass through every state.

SUSPENDED is a transient operational state, not a lifecycle stage. A suspended Tool MAY return to ACTIVE.

DEGRADED reflects health, not lifecycle. EMERGENCY_DISABLED is a security override, not a lifecycle stage.

Detailed lifecycle semantics belong to **TOOLS-008 — Tool Lifecycle**, which references this canonical model.

---

# 72. Tool Ownership

Every Tool SHOULD have an identified owner.

The owner may be:

```text
Organization
Team
Service
Resource
```

Ownership determines responsibility for:

* maintenance;
* security;
* versioning;
* availability;
* retirement.

---

# 73. Tool Responsibility

The Tool owner SHOULD be accountable for ensuring that:

* the contract is accurate;
* permissions are appropriate;
* dependencies are known;
* risks are documented;
* failures are handled;
* lifecycle status is maintained.

---

# 74. Tool Metadata

Recommended Tool metadata:

```text
{
    id,
    name,
    description,
    version,
    owner,
    category,
    risk,
    side_effects,
    determinism,
    idempotency,
    timeout,
    capabilities,
    dependencies,
    status
}
```

---

# 75. Conceptual Tool Model

The complete conceptual model is:

```text
Tool
│
├── Identity
├── Description
├── Capability
├── Contract
│   ├── Inputs
│   ├── Outputs
│   └── Errors
│
├── Security
│   ├── Permissions
│   ├── Scope
│   └── Authority
│
├── Execution
│   ├── Timeout
│   ├── Cancellation
│   ├── Retry
│   └── Limits
│
├── Operational Properties
│   ├── Risk
│   ├── Side Effects
│   ├── Determinism
│   └── Idempotency
│
├── Provenance
├── Observability
├── Ownership
└── Lifecycle
```

---

# 76. Example — Read Tool

```text
ToolID:
tool.sensor.read

Capability:
Read sensor measurement

Type:
READ

Side Effects:
NONE

Input:
sensor_id

Output:
measurement

Risk:
LOW
```

---

# 77. Example — Action Tool

```text
ToolID:
tool.pump.set_speed

Capability:
Set pump operating speed

Type:
ACTION

Side Effects:
EXTERNAL_ACTION

Input:
pump_id
speed

Output:
execution_result

Risk:
HIGH
```

This Tool requires stronger authorization than a simple read operation.

---

# 78. Example — Destructive Tool

```text
ToolID:
tool.database.delete

Capability:
Delete organizational data

Type:
DESTRUCTIVE

Side Effects:
MUTATING

Risk:
CRITICAL
```

Such a Tool SHOULD have strong restrictions and explicit governance.

---

# 79. Tool Invocation Model

The conceptual invocation flow is:

```text
Caller
   │
   ▼
Tool Discovery
   │
   ▼
Tool Contract
   │
   ▼
Input Validation
   │
   ▼
Authorization
   │
   ▼
Approval (when required)
   │
   ▼
Invocation
   │
   ▼
Execution
   │
   ├── Success → Outcome
   │
   └── Failure → Outcome
   │
   ▼
Result
   │
   ▼
Audit / Provenance
```

---

# 80. Failure Principle

A Tool MUST fail explicitly when it cannot safely perform its declared operation.

It MUST NOT:

* silently fabricate results;
* silently expand permissions;
* silently change scope;
* silently ignore safety constraints.

---

# 81. Unknown Result

Unknown or unavailable information MUST remain distinguishable from a valid negative result.

Example:

```text
UNKNOWN
```

is not equivalent to:

```text
FALSE
```

and:

```text
UNAVAILABLE
```

is not equivalent to:

```text
EMPTY
```

---

# 82. Tool Trust

A Tool SHOULD NOT be trusted merely because it is registered.

Trust SHOULD depend on:

```text
Identity
Owner
Contract
Security
Provenance
Execution Integrity
Operational History
```

---

# 83. Tool Integrity

The Runtime SHOULD protect Tool definitions and execution mechanisms from unauthorized modification.

---

# 84. Tool Observability Requirements

For consequential Tools, the Runtime SHOULD capture:

```text
ToolID
Version
InvocationID
Caller
Organization
Scope
Timestamp
Duration
Input Reference
Output Reference
Status
Error
```

Sensitive input/output data SHOULD be protected according to security policy.

---

# 85. Tool Conformance

A Tool implementation conforms to this model when it:

1. has a unique identity;
2. exposes a defined capability;
3. has a contract;
4. defines inputs and outputs;
5. supports explicit invocation;
6. declares operational characteristics;
7. is subject to authorization;
8. respects its operational boundary;
9. produces structured results;
10. exposes sufficient provenance;
11. supports appropriate observability;
12. follows lifecycle governance.

---

# 86. Mandatory Properties

At minimum, a Tool SHOULD define:

```text
ToolID
Name
Description
Version
Capability
Contract
Input Schema
Output Schema
Security Policy
Risk Classification
Side Effect Classification
Status
Owner
```

---

# 87. Recommended Properties

A mature Tool SHOULD additionally define:

```text
Timeout
Cancellation
Retry Policy
Idempotency
Determinism
Dependencies
Rate Limits
Resource Limits
Preconditions
Postconditions
Cost
Health
Availability
```

---

# 88. Design Principles

### Principle 1 — Explicit Capability

> A Tool must clearly define what capability it provides.

### Principle 2 — Explicit Contract

> Inputs, outputs and failure behavior must be defined.

### Principle 3 — Least Privilege

> A Tool must have only the permissions required for its purpose.

### Principle 4 — Explicit Side Effects

> Callers must be able to determine whether a Tool can change organizational state.

### Principle 5 — Traceability

> Consequential Tool usage must be traceable.

### Principle 6 — Fail Safely

> A Tool must not silently produce false or fabricated results.

### Principle 7 — Organizational Authority

> Tool capability does not imply authorization to use that capability.

### Principle 8 — Separation of Concerns

> Tool definition, authorization, invocation and execution are distinct concerns.

---

# 89. Relationship With Other Tool Specifications

```text
TOOLS-001
Tool Model
   │
   ├── TOOLS-002
   │   Tool Contract
   │
   ├── TOOLS-003
   │   Tool Security
   │
   ├── TOOLS-004
   │   Tool Registry
   │
   ├── TOOLS-005
   │   Tool Discovery
   │
   ├── TOOLS-006
   │   Tool Invocation
   │
   ├── TOOLS-007
   │   Tool Execution
   │
   └── TOOLS-008
       Tool Lifecycle
```

TOOLS-001 is therefore the conceptual foundation for the entire Tools layer.

---

# 90. Final Statement

The VIAL Tool Model defines Tools as controlled, identifiable and authorized capabilities.

```text
CAPABILITY
     │
     ▼
    TOOL
     │
 ┌───┴────┐
 ▼        ▼
CONTRACT SECURITY
 │        │
 └───┬────┘
     ▼
 INVOCATION
     │
     ▼
 EXECUTION
     │
     ▼
  RESULT
```

The Tool layer transforms abstract organizational intent into controlled interaction with operational capabilities.

> **A Tool is not merely something that can be called. It is a governed capability whose identity, contract, authority, execution and consequences must remain explicit.**

# End of TOOLS-001
