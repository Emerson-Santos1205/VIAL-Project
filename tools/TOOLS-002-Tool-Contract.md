# TOOLS-002 — Tool Contract

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Tools Specification
**Depends On:** TOOLS-001 — Tool Model, TOOLS-003 — Tool Security, SDK-001 — Architecture, SDK-003 — Resource, SDK-004 — Context, SDK-005 — Decision, RFC-002, RFC-003, RFC-004, RFC-005, RFC-006

---

# 1. Abstract

This document defines the formal contract model for Tools within VIAL.

A Tool Contract establishes the machine-readable and human-understandable agreement between a Tool and its callers.

The fundamental principle is:

> **A Tool Contract defines exactly what a Tool accepts, what it may perform, what it returns, and how it fails.**

The contract provides the boundary between:

```text
Caller
   │
   ▼
Tool Contract
   │
   ▼
Tool Implementation
```

The caller SHOULD be able to determine whether a Tool is appropriate without inspecting its internal implementation.

---

# 2. Purpose

The Tool Contract exists to define:

* Tool identity;
* capability;
* inputs;
* outputs;
* schemas;
* validation;
* errors;
* side effects;
* preconditions;
* postconditions;
* execution semantics;
* compatibility;
* versioning;
* provenance requirements.

The contract is the authoritative interface between the Tool and its consumers.

---

# 3. Contract Definition

A Tool Contract is a formal specification describing the externally observable behavior of a Tool.

Conceptually:

```text
Tool Contract
│
├── Identity
├── Capability
├── Input
├── Output
├── Errors
├── Preconditions
├── Postconditions
├── Side Effects
├── Execution Semantics
├── Security Requirements
└── Version
```

---

# 4. Contract Boundary

The Contract defines the public boundary of a Tool.

Internal implementation details SHOULD NOT be part of the Contract unless they affect externally observable behavior.

Example:

```text
Contract:
read_temperature(sensor_id)

Implementation:
Python service
Database query
PLC communication
Cache
```

The implementation MAY change without changing the Contract when observable semantics remain compatible.

---

# 5. Contract Identity

Every Contract MUST identify the Tool to which it belongs.

Conceptually:

```text
ToolContract {
    tool_id
    contract_version
}
```

---

# 6. Tool Identity

The `tool_id` MUST uniquely identify the Tool within its namespace.

Example:

```text
tool.sensor.read_temperature
```

The identifier SHOULD remain stable across compatible Tool versions.

---

# 7. Contract Version

Every Contract SHOULD have an explicit version.

Example:

```text
contract_version:
1.0.0
```

Contract versioning SHOULD follow the project's compatibility policy.

---

# 8. Capability Declaration

The Contract MUST describe the capability exposed by the Tool.

Example:

```text
Capability:
Read the current temperature of a specified sensor.
```

The description SHOULD be precise enough to distinguish the Tool from similar capabilities.

---

# 9. Input Contract

The input contract defines everything the caller is allowed or required to provide.

Example:

```text
Input:
{
    sensor_id: string
}
```

Inputs MUST be explicitly defined.

---

# 10. Required Inputs

The Contract MUST identify required fields.

Example:

```text
sensor_id:
required = true
```

A required input that is absent MUST cause validation failure.

---

# 11. Optional Inputs

The Contract MAY define optional inputs.

Example:

```text
timeout:
required = false
default = 5000
```

Defaults SHOULD be explicitly documented.

---

# 12. Input Types

Each input MUST have a defined type.

Supported conceptual types MAY include:

```text
string
integer
number
boolean
array
object
enum
date
datetime
binary
reference
```

The implementation MAY support additional types.

---

# 13. Input Constraints

Inputs MAY define constraints such as:

```text
minimum
maximum
length
pattern
format
enum
range
```

Example:

```text
speed:
type = number
minimum = 0
maximum = 100
```

Invalid values MUST be rejected before execution.

---

# 14. Input Schema

The Contract SHOULD expose a machine-readable input schema.

Example:

```text
{
    "type": "object",
    "required": ["sensor_id"],
    "properties": {
        "sensor_id": {
            "type": "string"
        }
    }
}
```

The exact schema language is implementation-dependent unless another specification mandates a particular format.

---

# 15. Input Normalization

A Tool MAY normalize valid inputs.

Examples:

```text
"70"
```

to:

```text
70
```

However, normalization MUST NOT silently transform an invalid or unsafe request into a materially different operation.

---

# 16. Input Validation

Input validation MUST occur before Tool execution.

Validation SHOULD include:

```text
Type
Presence
Format
Range
Structure
Allowed Values
Security Constraints
Operational Constraints
```

---

# 17. Input Rejection

Invalid input MUST produce a structured error.

Example:

```text
{
    "code": "INVALID_INPUT",
    "field": "speed",
    "message": "Value must be between 0 and 100."
}
```

---

# 18. Output Contract

The output contract defines the result produced by successful execution.

Example:

```text
Output:
{
    temperature: number,
    timestamp: datetime
}
```

The Tool SHOULD NOT return undocumented fields as part of the normative output unless the contract permits extensibility.

---

# 19. Output Schema

The Contract SHOULD expose a machine-readable output schema.

Example:

```text
{
    "type": "object",
    "required": ["temperature"],
    "properties": {
        "temperature": {
            "type": "number"
        }
    }
}
```

---

# 20. Output Semantics

The Contract MUST define the semantic meaning of important output fields.

For example:

```text
temperature:
Current measured temperature in degrees Celsius.
```

A field name alone is insufficient when its meaning is ambiguous.

---

# 21. Output Provenance

Outputs that may influence Context, Cognition or Decision SHOULD expose provenance.

Recommended information:

```text
source
timestamp
source_version
measurement_id
```

---

# 22. Result Envelope

A Tool MAY use a standardized result envelope.

Example:

```text
{
    "status": "SUCCESS",
    "data": {},
    "metadata": {},
    "provenance": {}
}
```

The envelope SHOULD distinguish operational status from the actual Tool data.

---

# 23. Error Contract

The Tool Contract MUST define expected error classes.

Conceptually:

```text
ToolError {
    code
    message
    category
    retryable
}
```

---

# 24. Error Codes

Error codes MUST be machine-readable and stable within a Contract version.

Examples:

```text
INVALID_INPUT
UNAUTHORIZED
FORBIDDEN
RESOURCE_NOT_FOUND
RESOURCE_UNAVAILABLE
TIMEOUT
RATE_LIMITED
DEPENDENCY_FAILURE
EXECUTION_FAILED
PRECONDITION_FAILED
POSTCONDITION_FAILED
```

---

# 25. Error Categories

Errors MAY be classified as:

```text
VALIDATION
AUTHORIZATION
RESOURCE
EXECUTION
TIMEOUT
DEPENDENCY
POLICY
SYSTEM
```

---

# 26. Retryability

The Contract SHOULD indicate whether an error is retryable.

Example:

```text
{
    "code": "TIMEOUT",
    "retryable": true
}
```

Retryability MUST consider side effects and idempotency.

---

# 27. Error Information

Error messages SHOULD provide enough information to diagnose the problem without exposing secrets or sensitive internal details.

---

# 28. Side Effect Declaration

The Contract MUST declare whether the Tool produces side effects.

Possible values:

```text
NONE
READ_ONLY
MUTATING
EXTERNAL_ACTION
```

This declaration is important for authorization and execution planning.

---

# 29. Side Effect Semantics

The Contract SHOULD describe the nature of side effects.

Example:

```text
Side Effect:
Changes pump operating speed.
```

The description SHOULD identify the affected organizational Resource when applicable.

---

# 30. Idempotency

The Contract SHOULD declare idempotency.

Possible values:

```text
IDEMPOTENT
NON_IDEMPOTENT
CONDITIONAL
UNKNOWN
```

If conditional, the conditions MUST be documented.

---

# 31. Determinism

The Contract SHOULD indicate whether repeated execution with equivalent inputs is expected to produce equivalent results.

Possible values:

```text
DETERMINISTIC
NON_DETERMINISTIC
CONDITIONAL
```

---

# 32. Preconditions

The Contract MAY define conditions that MUST be satisfied before execution.

Example:

```text
Preconditions:
- resource exists
- resource is online
- caller has operation permission
```

Preconditions SHOULD be machine-evaluable whenever possible.

---

# 33. Postconditions

The Contract MAY define expected conditions after successful execution.

Example:

```text
Postcondition:
pump.speed == requested_speed
```

Postconditions MAY be verified by the Runtime.

---

# 34. Execution Semantics

The Contract SHOULD define the general semantics of execution.

For example:

```text
Request
   ↓
Validate
   ↓
Authorize
   ↓
Execute
   ↓
Validate Result
   ↓
Return
```

The Contract describes externally observable semantics rather than implementation internals.

---

# 35. Synchronous Tools

A Tool MAY be synchronous.

Conceptually:

```text
invoke()
   ↓
result
```

The caller waits for the Tool result.

---

# 36. Asynchronous Tools

A Tool MAY be asynchronous.

Conceptually:

```text
invoke()
   ↓
InvocationID
   ↓
running
   ↓
result
```

The Contract MUST define how the caller obtains the final result.

---

# 37. Long-Running Tools

Long-running Tools SHOULD define:

* timeout;
* cancellation;
* progress;
* status;
* result retrieval.

---

# 38. Timeout Contract

The Contract SHOULD define expected timeout behavior.

Example:

```text
default_timeout:
5000 ms

maximum_timeout:
30000 ms
```

A caller MUST NOT assume that an arbitrary timeout is supported.

---

# 39. Cancellation Contract

If cancellation is supported, the Contract SHOULD define:

```text
cancelable:
true
```

and the semantics of cancellation.

For side-effecting operations, the Contract MUST make clear whether cancellation guarantees:

```text
No execution
Partial execution
Best-effort cancellation
Compensation
```

---

# 40. Progress

Asynchronous Tools MAY expose progress.

Example:

```text
progress:
0..100
```

Progress semantics MUST be documented.

---

# 41. Resource References

A Tool Contract MAY accept references to VIAL Resources.

Example:

```text
resource_id:
PUMP-001
```

The Contract SHOULD specify the Resource type expected.

---

# 42. Context References

A Tool MAY accept a Context reference.

Example:

```text
context_id:
CTX-2026-0012
```

The Tool MUST only consume the Context information authorized for its operation.

---

# 43. Decision References

A Tool invocation MAY reference a Decision.

Example:

```text
decision_id:
DEC-2026-000184
```

This is useful when the Tool execution is part of a Decision execution chain.

---

# 44. Authority Requirements

A Contract MAY declare required authority.

Example:

```text
required_permission:
equipment.control.speed
```

Authorization remains a Runtime responsibility.

---

# 45. Security Contract

Security requirements MAY include:

```text
Authentication
Authorization
Permission
Scope
Credential
Network
Data Classification
Audit
```

Detailed security semantics are defined in **TOOLS-003 — Tool Security**.

---

# 46. Data Classification

The Contract SHOULD identify the sensitivity of input and output data where applicable.

Example:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
```

---

# 47. Secret Handling

A Contract MUST NOT require callers to expose secrets unnecessarily.

Secrets SHOULD be referenced indirectly.

Example:

```text
credential_ref:
database.production
```

rather than:

```text
password:
"actual-password"
```

---

# 48. External Dependencies

The Contract MAY identify external dependencies.

Examples:

```text
Database
API
Network Service
PLC
Sensor Gateway
Filesystem
```

Dependencies SHOULD be documented when their availability affects Tool behavior.

---

# 49. Availability

The Contract MAY specify availability expectations.

Example:

```text
availability:
99.9%
```

Availability requirements are operational characteristics and SHOULD NOT be confused with execution guarantees.

---

# 50. Rate Limits

The Contract MAY declare invocation limits.

Example:

```text
rate_limit:
100 requests/minute
```

Rate limits SHOULD be explicit when callers need to plan invocation behavior.

---

# 51. Cost Semantics

A Contract MAY describe execution cost.

Cost MAY include:

```text
Compute
Network
External API
Financial
Operational
```

---

# 52. Compatibility

A new Contract version SHOULD preserve compatibility unless a breaking change is explicitly declared.

Compatibility concerns include:

```text
Input changes
Output changes
Error changes
Semantic changes
Side-effect changes
Security changes
```

---

# 53. Breaking Changes

The following SHOULD generally be considered breaking changes:

* removing required inputs;
* changing input semantics;
* removing output fields;
* changing output meaning;
* changing error semantics incompatibly;
* increasing required permissions;
* introducing unexpected side effects;
* changing operation semantics.

---

# 54. Non-Breaking Changes

Depending on the compatibility model, the following MAY be non-breaking:

* adding optional inputs;
* adding optional metadata;
* improving descriptions;
* adding documented error codes;
* improving implementation performance.

Compatibility MUST be evaluated according to actual consumer impact.

---

# 55. Contract Versioning

A Contract SHOULD use semantic versioning or another explicit versioning mechanism.

Example:

```text
1.0.0
1.1.0
2.0.0
```

Major versions SHOULD indicate incompatible changes.

---

# 56. Contract Stability

Once a Tool Contract is published and consumed, its semantics SHOULD be treated as stable.

Changes SHOULD be versioned rather than silently modifying existing behavior.

---

# 57. Contract Deprecation

A Contract MAY be deprecated.

Deprecation SHOULD communicate:

```text
deprecated_at
reason
replacement
removal_target
```

---

# 58. Contract Migration

When a Tool Contract is replaced, consumers SHOULD receive a migration path.

Example:

```text
tool.database.query@1
        ↓
tool.database.query@2
```

---

# 59. Contract Discovery

A caller SHOULD be able to discover the Contract before invoking a Tool.

The discovered Contract SHOULD contain sufficient information to determine:

* capability;
* input requirements;
* output;
* risk;
* side effects;
* authorization requirements.

---

# 60. Contract Machine Readability

Contracts SHOULD be machine-readable.

This enables:

```text
Validation
Discovery
Authorization
Invocation Planning
Documentation
Testing
```

---

# 61. Contract Human Readability

Machine readability MUST NOT eliminate human understandability.

A Tool Contract SHOULD be readable by developers, operators and auditors.

---

# 62. Contract Validation

A Tool implementation SHOULD validate itself against its declared Contract.

Possible validation includes:

```text
Input schema
Output schema
Error schema
Required metadata
Security declaration
Side-effect declaration
Version
```

---

# 63. Contract Testing

A Tool SHOULD have contract tests.

Contract tests SHOULD verify:

```text
Valid Inputs
Invalid Inputs
Expected Outputs
Expected Errors
Authorization Boundaries
Side Effects
Timeout Behavior
```

---

# 64. Contract Conformance

A Tool conforms to its Contract when its externally observable behavior satisfies the declared semantics.

Implementation details do not determine conformance unless they affect those semantics.

---

# 65. Contract Drift

Contract drift occurs when implementation behavior differs from the declared Contract.

Examples:

```text
Contract:
returns temperature in Celsius

Implementation:
returns Fahrenheit
```

or:

```text
Contract:
READ_ONLY

Implementation:
changes Resource state
```

Contract drift MUST be treated as a defect.

---

# 66. Contract Integrity

The published Contract MUST be protected from unauthorized modification.

A caller must be able to trust that the Contract corresponds to the Tool version being invoked.

---

# 67. Contract and Registry

The Tool Registry SHOULD store or reference the authoritative Contract.

```text
Tool Registry
     │
     ▼
Tool Identity
     │
     ▼
Contract
     │
     ▼
Tool Implementation
```

Detailed registry behavior is defined in **TOOLS-004 — Tool Registry**.

---

# 68. Contract and Discovery

Tool Discovery SHOULD expose Contract metadata.

A discovery mechanism SHOULD allow callers to understand whether a Tool can satisfy a requested capability.

Detailed discovery behavior belongs to **TOOLS-005 — Tool Discovery**.

---

# 69. Contract and Invocation

Invocation MUST comply with the Contract.

```text
Caller
   ↓
Contract
   ↓
Validate Input
   ↓
Authorize
   ↓
Invoke
```

Detailed invocation semantics belong to **TOOLS-006 — Tool Invocation**.

---

# 70. Contract and Execution

Execution MUST produce behavior consistent with the Contract.

Detailed execution semantics belong to **TOOLS-007 — Tool Execution**.

---

# 71. Example — Read Temperature

```text
ToolID:
tool.sensor.read_temperature

Version:
1.0.0

Capability:
Read current sensor temperature.

Input:
{
    "sensor_id": "string"
}

Output:
{
    "temperature": "number",
    "unit": "string",
    "timestamp": "datetime"
}

Side Effects:
NONE

Risk:
LOW

Idempotency:
IDEMPOTENT
```

---

# 72. Example — Set Pump Speed

```text
ToolID:
tool.pump.set_speed

Version:
1.0.0

Capability:
Set the operating speed of a pump.

Input:
{
    "pump_id": "string",
    "speed": "number"
}

Constraints:
0 <= speed <= 100

Output:
{
    "pump_id": "string",
    "speed": "number",
    "timestamp": "datetime"
}

Side Effects:
EXTERNAL_ACTION

Risk:
HIGH

Idempotency:
IDEMPOTENT
```

---

# 73. Example — Contract Failure

Request:

```text
{
    "pump_id": "PUMP-001",
    "speed": 150
}
```

Contract:

```text
0 <= speed <= 100
```

Result:

```text
{
    "status": "REJECTED",
    "error": {
        "code": "INVALID_INPUT",
        "field": "speed"
    }
}
```

The Tool MUST NOT execute the operation.

---

# 74. Example — Preconditions

Contract:

```text
Preconditions:
- pump exists
- pump is online
- caller has control permission
```

If the pump is offline:

```text
PRECONDITION_FAILED
```

The Tool SHOULD NOT attempt the action.

---

# 75. Example — Postcondition

Contract:

```text
Requested:
speed = 70
```

Expected:

```text
pump.speed = 70
```

If the resulting state is:

```text
pump.speed = 55
```

the execution MAY be classified as:

```text
POSTCONDITION_FAILED
```

---

# 76. Contract Composition

A Tool Contract MAY reference other contracts when a Tool composes multiple Tools.

Composition SHOULD preserve the individual boundaries and security requirements.

---

# 77. Contract Inheritance

Contracts SHOULD NOT rely heavily on implicit inheritance.

Important operational semantics SHOULD be explicit.

---

# 78. Contract Extensions

A Contract MAY provide extension metadata.

Extensions MUST NOT alter the meaning of mandatory fields without versioning.

---

# 79. Contract Metadata

Recommended metadata:

```text
{
    "tool_id": "...",
    "contract_version": "...",
    "owner": "...",
    "risk": "...",
    "side_effects": "...",
    "idempotency": "...",
    "determinism": "...",
    "created_at": "...",
    "updated_at": "..."
}
```

---

# 80. Canonical Contract Model

Conceptually:

```text
ToolContract {
    identity
    version

    capability

    input {
        schema
        required
        constraints
    }

    output {
        schema
        semantics
        provenance
    }

    errors {
        codes
        categories
        retryability
    }

    execution {
        synchronous
        timeout
        cancellation
        progress
    }

    behavior {
        side_effects
        idempotency
        determinism
    }

    conditions {
        preconditions
        postconditions
    }

    security {
        permissions
        scope
        data_classification
    }

    dependencies

    compatibility

    metadata
}
```

---

# 81. Contract Lifecycle

A Contract MAY follow:

```text
DRAFT
   ↓
VALIDATED
   ↓
PUBLISHED
   ↓
ACTIVE
   ↓
DEPRECATED
   ↓
RETIRED
```

The Tool Lifecycle specification defines the broader relationship between Tool and Contract lifecycle.

---

# 82. Contract Publication

A Contract SHOULD be validated before publication.

Publication means that consumers may rely on the declared interface.

---

# 83. Contract Retirement

A retired Contract MUST NOT be presented as an active interface.

Historical references SHOULD remain resolvable for audit and reproducibility where required.

---

# 84. Contract Auditability

A Contract SHOULD preserve:

```text
Author
Owner
Version
Publication Date
Changes
Approvals
Deprecation
Retirement
```

---

# 85. Contract Change Record

Material Contract changes SHOULD include:

```text
Change
Reason
Impact
Compatibility
Migration
Approver
```

---

# 86. Contract Security Principle

The Contract itself is not an authorization mechanism.

It declares security requirements.

The Runtime and Security layer enforce them.

```text
Contract
   ↓
Requirement
   ↓
Security Enforcement
```

---

# 87. Contract and Organizational Authority

A Tool Contract MAY specify that an operation requires authority associated with a Resource, Organization or Decision.

The actual authority validation remains outside the Contract implementation.

---

# 88. Contract and Decision

When a Tool executes as part of a Decision:

```text
Decision
   ↓
Tool Contract
   ↓
Authorization
   ↓
Execution
```

The Contract defines what the Tool can do; the Decision defines why the operation is being performed.

---

# 89. Contract and Context

A Tool may consume Context, but the Contract MUST identify the expected structure and semantics of Context inputs.

---

# 90. Contract and Resource

When operating on Resources, the Contract SHOULD identify:

```text
Resource Type
Required Resource State
Permitted Operations
Expected Result
```

---

# 91. Contract and Provenance

For information-producing Tools, the Contract SHOULD define provenance requirements.

This is particularly important when results can become part of organizational Context or Decision evidence.

---

# 92. Contract and Audit

For consequential Tools, the Contract SHOULD define the minimum information required for auditability.

---

# 93. Contract Failure Principle

If the Tool cannot satisfy its Contract safely, it MUST fail explicitly.

It MUST NOT:

* fabricate outputs;
* silently change semantics;
* silently expand permissions;
* silently ignore constraints;
* report success when the declared operation did not occur.

---

# 94. Conformance Requirements

A conforming Tool Contract MUST:

1. identify the Tool;
2. identify its version;
3. define its capability;
4. define its inputs;
5. define its outputs;
6. define expected errors;
7. declare side effects;
8. define relevant constraints;
9. define applicable security requirements;
10. define compatibility expectations;
11. remain consistent with actual Tool behavior.

---

# 95. Recommended Requirements

A mature Contract SHOULD additionally provide:

* machine-readable schemas;
* preconditions;
* postconditions;
* idempotency;
* determinism;
* timeout;
* cancellation;
* progress;
* provenance;
* dependencies;
* rate limits;
* cost;
* data classification;
* migration information.

---

# 96. Design Principles

### Principle 1 — Explicit Interface

> The Tool Contract defines the public interface of the Tool.

### Principle 2 — No Hidden Semantics

> Important externally observable behavior must be declared.

### Principle 3 — Contract Before Invocation

> A caller should understand the Contract before invoking the Tool.

### Principle 4 — Security Is Explicit

> Required authority and security characteristics must be identifiable.

### Principle 5 — Side Effects Are Explicit

> Callers must know whether an operation can modify organizational state.

### Principle 6 — Versioned Semantics

> Material changes to behavior require Contract versioning.

### Principle 7 — Implementation Independence

> Internal implementation may evolve without changing the Contract when observable behavior remains compatible.

### Principle 8 — Fail Explicitly

> Contract violations must result in explicit failure rather than silent deviation.

---

# 97. Relationship With Tools Layer

```text
TOOLS-001
Tool Model
    │
    ▼
TOOLS-002
Tool Contract
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

TOOLS-002 therefore establishes the formal interface on which the remaining Tools specifications depend.

---

# 98. Final Statement

The Tool Contract transforms a Tool from an opaque callable capability into an explicit, inspectable and governable interface.

```text
CAPABILITY
    │
    ▼
TOOL
    │
    ▼
CONTRACT
    │
 ┌──┼───────────┐
 ▼  ▼           ▼
INPUT OUTPUT   ERRORS
 │
 ▼
VALIDATION
 │
 ▼
AUTHORIZATION
 │
 ▼
EXECUTION
```

The Contract establishes the boundary of trust between a caller and a Tool.

> **A Tool may implement any internal mechanism it requires, but its externally observable capability, inputs, outputs, constraints, side effects and failure semantics must remain explicit.**

# End of TOOLS-002
