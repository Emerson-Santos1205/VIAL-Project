# TOOLS-003 — Tool Security

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Tools Specification
Depends On:
- TOOLS-001
- TOOLS-002
- SDK-001
- SDK-002
- SDK-003
- SDK-004
- SDK-005
- RFC-002
- RFC-003
- RFC-004
- RFC-005
- RFC-006

---

# 1. Abstract

This document defines the security model governing Tools within VIAL.

A Tool represents a potentially executable capability. Therefore, the existence of a Tool does not imply that any caller is authorized to use it.

The fundamental principle is:

> **Capability does not imply authority.**

Tool Security establishes the mechanisms and principles required to control:

* who may invoke a Tool;
* which operation may be performed;
* against which Resource;
* within which scope;
* under which authority;
* with which data;
* under which conditions;
* with which operational limits.

---

# 2. Purpose

Tool Security provides the security boundary between:

```text
Caller
   │
   ▼
Authority
   │
   ▼
Security Policy
   │
   ▼
Tool
   │
   ▼
Execution
```

The security model protects VIAL Organizations, Resources, Context, Decisions and external systems from unauthorized or unsafe Tool execution.

---

# 3. Security Model

Tool authorization MUST be evaluated independently from Tool availability.

A Tool may be:

```text
AVAILABLE
```

while a particular caller is:

```text
UNAUTHORIZED
```

Therefore:

```text
Tool Available ≠ Tool Authorized
```

---

# 4. Security Boundary

The Tool Security boundary encompasses:

```text
Identity
Authentication
Authorization
Permission
Scope
Policy
Credential
Data Access
Execution
Audit
```

---

# 5. Security Principal

A security principal is an identifiable entity requesting or causing Tool execution.

A principal MAY be:

```text
Human
Agent
Service
Runtime
Organization Process
System
```

Every consequential Tool invocation SHOULD have an identifiable principal.

---

# 6. Identity

The security system MUST establish the identity of the principal whenever authorization depends on identity.

Conceptually:

```text
Principal
    │
    ▼
Identity
    │
    ▼
Authority
```

Identity MUST NOT be inferred solely from untrusted input.

---

# 7. Authentication

Authentication establishes confidence that a principal corresponds to the claimed identity.

Possible mechanisms include:

```text
Credentials
Certificates
Tokens
Service Identity
Device Identity
Cryptographic Identity
```

The mechanism is implementation-dependent.

---

# 8. Authentication vs Authorization

These concerns MUST remain distinct.

```text
Authentication:
Who are you?

Authorization:
What are you allowed to do?
```

Successful authentication does not imply permission to invoke a Tool.

---

# 9. Authorization

Authorization determines whether a principal may perform a specific Tool operation.

Conceptually:

```text
Authorize(
    principal,
    tool,
    operation,
    resource,
    scope,
    context
)
```

The result MUST be explicit.

Possible outcomes:

```text
ALLOW
DENY
REQUIRE_APPROVAL
```

---

# 10. Authorization Decision

An authorization decision SHOULD consider:

```text
Principal
Tool
Operation
Organization
Resource
Scope
Context
Decision
Policy
Risk
Time
Environment
```

Not every authorization system must use every attribute.

---

# 11. Permission

A permission represents an authorized capability.

Example:

```text
equipment.read
equipment.control
database.read
database.write
notification.send
```

Permissions SHOULD be granular enough to prevent unnecessary authority.

---

# 12. Tool Permission

A Tool SHOULD declare the permissions required for its operations.

Example:

```text
Tool:
tool.pump.set_speed

Required Permission:
equipment.control.speed
```

---

# 13. Least Privilege

VIAL MUST follow the principle of least privilege.

A principal MUST receive only the authority necessary for the requested operation.

A Tool MUST receive only the privileges necessary to execute its declared capability.

---

# 14. Deny by Default

When authorization information is absent or insufficient, the default security behavior SHOULD be denial.

```text
No Authority
     │
     ▼
   DENY
```

Exceptions MUST be explicitly defined by policy.

---

# 15. Explicit Authorization

Authorization SHOULD be explicit for consequential operations.

The system SHOULD NOT infer authority from:

* Tool availability;
* network accessibility;
* Resource visibility;
* caller knowledge;
* previous successful invocation.

---

# 16. Resource Scope

Authorization MAY be restricted to specific Resources.

Example:

```text
Principal:
operator-01

Permission:
equipment.control

Scope:
PUMP-001
```

The same principal may be denied access to:

```text
PUMP-002
```

---

# 17. Organizational Scope

Authority MAY be limited to an Organization.

Example:

```text
Organization:
ORG-001

Permission:
database.read
```

A principal authorized in one Organization MUST NOT automatically gain equivalent authority in another Organization.

---

# 18. Namespace Isolation

VIAL SHOULD maintain isolation between organizational namespaces.

A Tool operating within one namespace SHOULD NOT automatically access another namespace.

---

# 19. Operation Scope

A permission SHOULD be associated with a specific operation whenever practical.

Example:

```text
equipment.read
equipment.start
equipment.stop
equipment.configure
```

This is preferable to a broad:

```text
equipment.*
```

for high-risk environments.

---

# 20. Role-Based Authority

A principal MAY receive permissions through a role.

Example:

```text
Role:
MaintenanceOperator

Permissions:
equipment.read
equipment.start
equipment.stop
```

Role assignment MUST itself be authorized.

---

# 21. Attribute-Based Authority

Authorization MAY depend on attributes.

Examples:

```text
Department
Organization
Resource
Time
Location
Risk
Purpose
Environment
```

Example:

```text
Allow:
equipment.control

When:
organization == ORG-001
AND
resource.sector == PRODUCTION
```

---

# 22. Contextual Authorization

Authorization MAY depend on Context.

Example:

```text
Allow shutdown only when:
maintenance_mode == true
```

Context used for authorization MUST have an appropriate trust level.

---

# 23. Decision-Based Authorization

A Tool invocation MAY be authorized as part of a Decision.

Example:

```text
Decision
   │
   ├── Authority
   │
   └── Tool Invocation
```

The existence of a Decision does not automatically authorize every Tool operation.

The Decision's authority and scope MUST be compatible with the requested operation.

---

# 24. Delegated Authority

A principal MAY delegate limited authority to another principal.

Delegation SHOULD specify:

```text
Delegator
Delegate
Permission
Scope
Purpose
Validity
Restrictions
```

Delegation MUST NOT silently expand the authority of the delegating principal.

---

# 25. Authority Chain

Where delegation exists, the Runtime SHOULD preserve the authority chain.

Example:

```text
Organization
    │
    ▼
Human
    │
    ▼
Agent
    │
    ▼
Tool
```

The final Tool invocation SHOULD remain attributable to the originating authority.

---

# 26. Authority Propagation

Authority propagated through an execution chain MUST NOT exceed the authority of the originating principal.

```text
A
│
▼
B
│
▼
Tool
```

The authority available to the Tool MUST be bounded by the authority legitimately propagated from A.

---

# 27. Credential Isolation

Credentials MUST be isolated from callers whenever possible.

A Tool MAY receive a credential reference rather than the secret itself.

Example:

```text
credential_ref:
production.database
```

---

# 28. Secret Protection

Secrets MUST NOT be:

* embedded in Tool definitions;
* exposed in logs;
* returned in normal Tool results;
* unnecessarily passed between Tools.

Examples include:

```text
Passwords
API Keys
Private Keys
Access Tokens
Certificates
```

---

# 29. Credential Scope

Credentials SHOULD be scoped to the minimum required capability.

Example:

```text
Database credential:
READ ONLY
```

rather than:

```text
Database credential:
FULL ADMIN
```

---

# 30. Credential Rotation

Credentials SHOULD support rotation without requiring changes to Tool Contracts where possible.

---

# 31. Credential Revocation

The system MUST support revocation of credentials used by Tools.

Revocation SHOULD take effect within an operationally appropriate period.

---

# 32. Data Access Control

Tool access to data MUST be subject to authorization.

The Tool MUST NOT assume that because a caller can invoke it, the caller can access every dataset available to the Tool.

---

# 33. Data Minimization

A Tool SHOULD receive only the data necessary to perform its operation.

Example:

```text
Required:
temperature

Not Required:
employee records
financial data
unrelated production records
```

---

# 34. Context Minimization

When Context is supplied to a Tool, only the relevant authorized portion SHOULD be exposed.

This reduces:

* data leakage;
* accidental disclosure;
* unnecessary processing;
* security risk.

---

# 35. Sensitive Data

Tools processing sensitive data SHOULD declare the applicable data classification.

Possible classes:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
```

---

# 36. Output Security

Tool outputs MUST respect the authorization boundary of the caller.

A Tool MUST NOT return information simply because the underlying system can access it.

---

# 37. Information Disclosure

Error messages, metadata and outputs MUST NOT unnecessarily reveal:

```text
Credentials
Internal Network Details
Security Policies
Private Data
System Secrets
```

---

# 38. Tool Isolation

High-risk Tools SHOULD execute inside an appropriate isolation boundary.

Possible mechanisms:

```text
Process Isolation
Container
Sandbox
VM
Service Boundary
Network Policy
Operating System Permissions
```

---

# 39. Filesystem Security

Tools accessing files SHOULD operate within explicitly authorized filesystem boundaries.

A Tool MUST NOT assume unrestricted filesystem access.

---

# 40. Network Security

Tools requiring network access SHOULD have explicitly controlled network permissions.

Example:

```text
Allowed:
api.example.internal

Denied:
arbitrary external hosts
```

---

# 41. External Service Security

When a Tool invokes an external service, security controls SHOULD cover:

```text
Destination
Authentication
Authorization
TLS
Credentials
Timeout
Rate Limit
Response Validation
```

---

# 42. Tool-to-Tool Security

When one Tool invokes another Tool, the downstream Tool MUST evaluate the authority available to the caller.

Tool chaining MUST NOT create an implicit privilege escalation.

---

# 43. Privilege Escalation

A Tool MUST NOT be used to obtain authority greater than that possessed by the invoking principal.

Example:

```text
Caller
  │
  └── read permission
          │
          ▼
       Tool A
          │
          ▼
       Tool B
          │
          X
       admin operation
```

Tool A MUST NOT transform read authority into administrator authority.

---

# 44. Confused Deputy Prevention

A Tool MUST NOT use its own authority to perform an operation that the caller is not authorized to request.

This is especially important for Tools with elevated privileges.

---

# 45. Ambient Authority

Tools SHOULD avoid relying on implicit ambient privileges.

Permissions SHOULD be explicitly associated with the invocation or execution context.

---

# 46. Execution Identity

The identity under which a Tool executes SHOULD be distinguishable from the identity that requested the Tool.

Example:

```text
Requested by:
agent-42

Executed by:
tool-runtime-07
```

Both identities SHOULD remain traceable.

---

# 47. Invocation Identity

Every consequential invocation SHOULD have a unique Invocation ID.

Example:

```text
INV-2026-000492
```

The Invocation ID SHOULD connect:

```text
Caller
Authorization
Tool
Execution
Result
Audit
```

---

# 48. Security Context

The Runtime SHOULD establish a security context before execution.

Conceptually:

```text
SecurityContext {
    principal
    organization
    permissions
    scope
    credentials
    policies
    invocation_id
}
```

---

# 49. Security Context Integrity

The security context MUST NOT be modifiable by the Tool caller through ordinary Tool input.

---

# 50. Policy Evaluation

Security policies SHOULD be evaluated before consequential execution.

Example:

```text
Request
   ↓
Policy Evaluation
   ↓
ALLOW / DENY
   ↓
Execution
```

---

# 51. Policy Precedence

Where multiple policies apply, the system MUST define deterministic precedence.

A restrictive policy SHOULD NOT be silently overridden by a less restrictive policy.

---

# 52. Explicit Denial

Authorization denial SHOULD produce a structured result.

Example:

```text
{
    "status": "DENIED",
    "error": {
        "code": "FORBIDDEN"
    }
}
```

---

# 53. Denial Information

Denial responses SHOULD provide enough information to diagnose authorization problems without revealing sensitive policy information.

---

# 54. Approval

High-risk operations MAY require explicit approval.

Example:

```text
Tool Invocation
       │
       ▼
Risk Evaluation
       │
       ▼
Approval Required
       │
       ▼
Authorized Execution
```

Approval SHOULD be attributable to an identifiable authority.

---

# 55. Human Approval

A Tool MAY require human approval for high-impact operations.

The approval record SHOULD include:

```text
Approver
Time
Operation
Scope
Reason
Invocation ID
```

---

# 56. Multi-Party Approval

Critical operations MAY require more than one authorized approver.

Example:

```text
Approver A
     +
Approver B
     ↓
Execution
```

---

# 57. Risk-Based Security

Security controls SHOULD correspond to Tool risk.

Example:

```text
LOW
  → standard authorization

MEDIUM
  → stronger policy evaluation

HIGH
  → elevated authority / audit

CRITICAL
  → explicit approval / stronger isolation
```

---

# 58. Side-Effect Security

Tools with side effects SHOULD have stronger controls than read-only Tools.

```text
READ
  < WRITE
  < ACTION
  < DESTRUCTIVE
```

This is a conceptual risk ordering, not an absolute rule.

---

# 59. Destructive Operations

Destructive Tools SHOULD require:

* explicit authorization;
* narrow scope;
* strong auditability;
* appropriate confirmation;
* appropriate isolation.

---

# 60. Safety Constraints

Security authorization MUST NOT override independent safety constraints.

A caller may be authorized to perform an operation that is nevertheless unsafe under current operating conditions.

Therefore:

```text
Authorization ≠ Safety Approval
```

Both controls may be required.

---

# 61. Preconditions

Security-sensitive preconditions SHOULD be validated before execution.

Example:

```text
maintenance_mode == true
```

---

# 62. Race Conditions

Authorization and safety checks SHOULD occur sufficiently close to execution to reduce the possibility that conditions change between validation and execution.

---

# 63. Time-Bounded Authority

Permissions MAY expire.

Example:

```text
valid_from
valid_until
```

Expired authority MUST NOT authorize new execution.

---

# 64. One-Time Authority

Critical operations MAY use one-time authorization.

Example:

```text
approval_token:
single_use
```

After successful execution, the authority is invalidated.

---

# 65. Rate Limiting

Security policies MAY limit Tool invocation frequency.

Rate limits SHOULD protect against:

* abuse;
* accidental loops;
* denial of service;
* excessive cost;
* Resource exhaustion.

---

# 66. Invocation Limits

The Runtime MAY limit:

```text
Calls per minute
Concurrent executions
Execution duration
Data volume
Network bandwidth
```

---

# 67. Replay Protection

Security-sensitive Tool invocations SHOULD prevent unauthorized replay.

Possible mechanisms include:

```text
Invocation ID
Nonce
Timestamp
Expiration
Signature
One-Time Token
```

---

# 68. Idempotency and Security

Idempotent Tools are generally safer to retry than non-idempotent Tools.

Security policy SHOULD consider this distinction.

---

# 69. Audit

Security-relevant Tool invocations MUST be auditable.

At minimum:

```text
Invocation ID
Principal
Tool
Operation
Resource
Authorization Result
Timestamp
Execution Result
```

---

# 70. Audit Integrity

Audit records SHOULD be protected against unauthorized modification.

---

# 71. Audit Privacy

Audit records MUST themselves respect data protection requirements.

Sensitive input and output SHOULD be referenced or redacted rather than unnecessarily copied into logs.

---

# 72. Security Events

Security-relevant events SHOULD be identifiable.

Examples:

```text
AUTHENTICATION_FAILED
AUTHORIZATION_DENIED
TOOL_BLOCKED
POLICY_VIOLATION
CREDENTIAL_FAILURE
SECURITY_CONTEXT_INVALID
```

---

# 73. Monitoring

High-risk Tools SHOULD be monitored for abnormal behavior.

Indicators MAY include:

```text
Unexpected frequency
Unexpected Resource access
Repeated failures
Permission violations
Unexpected destinations
Abnormal execution time
```

---

# 74. Anomaly Detection

The Runtime MAY detect anomalous Tool behavior.

Anomaly detection SHOULD NOT silently alter Tool semantics.

Security responses SHOULD be explicit and auditable.

---

# 75. Tool Integrity

The Tool implementation SHOULD be protected from unauthorized modification.

Integrity mechanisms MAY include:

```text
Signed Artifacts
Checksums
Trusted Deployment
Immutable Images
Version Verification
```

---

# 76. Contract Integrity

The security system SHOULD ensure that the Contract associated with a Tool corresponds to the actual Tool implementation/version.

A malicious or accidental mismatch MUST NOT silently bypass security assumptions.

---

# 77. Registry Security

Tool registration SHOULD require authorization.

Only authorized entities SHOULD be able to:

```text
Register
Modify
Enable
Disable
Retire
```

a Tool.

---

# 78. Discovery Security

Tool Discovery SHOULD respect authorization.

A caller MAY be prevented from discovering Tools that it is not permitted to use.

---

# 79. Hidden Capabilities

A Tool MUST NOT expose undocumented privileged capabilities through hidden parameters or undocumented operations.

---

# 80. Input Security

Tool inputs MUST be treated as untrusted unless explicitly established otherwise.

Validation MUST occur before sensitive operations.

---

# 81. Injection Protection

Tools processing structured or interpreted input SHOULD protect against injection attacks.

Examples include:

```text
SQL Injection
Command Injection
Script Injection
Template Injection
Path Traversal
Prompt Injection
```

The exact controls depend on the Tool implementation.

---

# 82. Command Execution

Tools capable of executing operating-system commands MUST have strict command and argument boundaries.

Arbitrary command execution SHOULD NOT be permitted unless explicitly required and appropriately isolated.

---

# 83. Path Security

Filesystem Tools MUST prevent unauthorized path traversal.

Examples:

```text
../
../../
absolute paths
symbolic-link escapes
```

must be controlled according to the Tool's security boundary.

---

# 84. External Input

Data obtained from external systems MUST be treated as untrusted until validated.

A Tool MUST NOT assume that external responses are safe merely because the external service is trusted.

---

# 85. Output Injection

Tool outputs consumed by other systems SHOULD be safely encoded or structured to prevent interpretation as executable content.

---

# 86. Prompt Injection

When a Tool processes natural-language or untrusted content that may influence an AI system, the content MUST be treated as data rather than authority.

External content MUST NOT automatically modify:

```text
Permissions
Policies
System Instructions
Security Context
Authority
```

---

# 87. Trust Boundaries

VIAL SHOULD explicitly distinguish trust boundaries.

Example:

```text
Trusted Runtime
       │
       ▼
Tool
       │
       ▼
External System
       │
       ▼
Untrusted Data
```

Crossing a trust boundary requires appropriate validation.

---

# 88. External Tool Trust

External Tools SHOULD NOT automatically receive the same trust level as internal Tools.

Trust SHOULD depend on:

```text
Origin
Identity
Integrity
Contract
Security
History
```

---

# 89. Sandbox Requirement

Untrusted or high-risk Tools SHOULD execute in a sandbox or equivalent isolation mechanism.

---

# 90. Network Egress Control

High-risk Tools SHOULD have restricted network egress.

The Tool SHOULD only communicate with destinations necessary for its capability.

---

# 91. Resource Limits

Security isolation SHOULD include resource limits where appropriate.

Examples:

```text
CPU
Memory
Storage
Network
Execution Time
Processes
```

---

# 92. Denial of Service Protection

The Tool layer SHOULD protect against excessive Tool execution caused by:

* malicious callers;
* accidental loops;
* recursive Tool chains;
* compromised Agents;
* external events.

---

# 93. Recursive Invocation Security

Tool recursion MUST be bounded.

Example:

```text
Tool A
 ↓
Tool B
 ↓
Tool A
 ↓
Tool B
```

The Runtime SHOULD detect and limit such cycles.

---

# 94. Security Across Tool Chains

Every Tool in a chain MUST maintain its own security boundary.

A previously authorized Tool invocation MUST NOT automatically authorize unrelated downstream operations.

---

# 95. Delegation Across Tool Chains

Delegated authority SHOULD preserve:

```text
Original Principal
Original Scope
Original Purpose
Expiration
Restrictions
```

---

# 96. Security Context Propagation

Security context MAY propagate through Tool chains, but only authorized attributes SHOULD be propagated.

Secrets SHOULD NOT automatically propagate.

---

# 97. Revocation

Permissions MUST be revocable.

Revocation SHOULD prevent new unauthorized invocations.

The handling of already-running operations MUST be explicitly defined according to risk.

---

# 98. Emergency Disablement

The system SHOULD support emergency Tool disablement.

Example:

```text
ACTIVE
   ↓
EMERGENCY_DISABLED
```

Emergency disablement SHOULD prevent new invocations.

---

# 99. Emergency Operations

Emergency operations MUST themselves be controlled and audited.

Emergency authority SHOULD NOT become a permanent privilege.

---

# 100. Security Failure Principle

When security cannot be established reliably, the default behavior SHOULD be:

```text
FAIL CLOSED
```

The system SHOULD NOT execute a consequential Tool operation when authorization state is unknown.

---

# 101. Availability vs Security

Security controls SHOULD consider availability, but availability MUST NOT silently override authorization.

```text
Service Available
        ≠
Operation Authorized
```

---

# 102. Security Testing

Security testing SHOULD include:

```text
Unauthorized Invocation
Privilege Escalation
Scope Violation
Credential Leakage
Input Injection
Replay
Rate Limit Bypass
Tool Chain Abuse
Contract Mismatch
Sandbox Escape
```

---

# 103. Security Conformance

A Tool Security implementation conforms to this specification when it:

1. identifies the invoking principal;
2. authenticates where required;
3. evaluates authorization;
4. enforces scope;
5. follows least privilege;
6. protects credentials;
7. protects sensitive data;
8. prevents unauthorized privilege escalation;
9. provides appropriate isolation;
10. maintains auditability;
11. supports revocation;
12. fails safely when authority cannot be established.

---

# 104. Recommended Security Properties

A mature implementation SHOULD additionally provide:

```text
Policy Engine
Role-Based Access
Attribute-Based Access
Delegation
Approval Workflows
Sandboxing
Network Controls
Credential Rotation
Replay Protection
Anomaly Detection
Signed Tool Artifacts
Security Monitoring
```

---

# 105. Security Architecture

The conceptual security architecture is:

```text
                    ┌──────────────┐
                    │   Principal  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Authentication│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Authorization│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Policy    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Tool Security│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Execution  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Audit/Result │
                    └──────────────┘
```

---

# 106. Relationship With TOOLS-001

`TOOLS-001 — Tool Model` defines what a Tool is.

`TOOLS-003 — Tool Security` defines how access to that Tool is controlled.

```text
Tool Model
    │
    ▼
Capability
    │
    ▼
Security Boundary
    │
    ▼
Authorized Invocation
```

---

# 107. Relationship With TOOLS-002

`TOOLS-002 — Tool Contract` defines the externally observable interface.

`TOOLS-003` establishes the security requirements governing access to that interface.

```text
Contract
    │
    ├── What can be requested
    │
    └── Security
          │
          └── Who may request it
```

---

# 108. Relationship With SDK

Tool Security relies on organizational concepts defined by the SDK:

```text
Organization
Resource
Context
Decision
Authority
```

Security therefore remains integrated with the VIAL organizational model rather than being an isolated authentication subsystem.

---

# 109. Relationship With Decision

A Decision may provide intent and authority context.

However:

> **A Decision does not bypass Tool Security.**

The Tool invocation remains subject to authorization, scope, policy and safety constraints.

---

# 110. Relationship With Runtime

The Runtime is responsible for enforcing Tool Security during invocation and execution.

Conceptually:

```text
Caller
  │
  ▼
Runtime
  │
  ├── Identity
  ├── Authorization
  ├── Policy
  ├── Scope
  ├── Limits
  │
  ▼
Tool
```

---

# 111. Security Invariants

The following invariants MUST hold:

### Invariant 1

A Tool MUST NOT execute a consequential operation without sufficient authority.

### Invariant 2

A Tool MUST NOT exceed its authorized Resource scope.

### Invariant 3

A Tool MUST NOT elevate caller privileges.

### Invariant 4

Secrets MUST NOT be unnecessarily exposed.

### Invariant 5

Security failure MUST NOT silently become successful execution.

### Invariant 6

Every consequential operation MUST remain attributable.

### Invariant 7

Tool chaining MUST NOT create implicit privilege escalation.

### Invariant 8

A Decision MUST NOT bypass independent Tool Security controls.

---

# 112. Final Statement

VIAL treats Tool Security as a fundamental organizational control rather than an implementation detail.

```text
CAPABILITY
     │
     ▼
   TOOL
     │
     ▼
 CONTRACT
     │
     ▼
AUTHORITY
     │
     ▼
 SECURITY
     │
     ▼
 EXECUTION
     │
     ▼
  RESULT
     │
     ▼
  AUDIT
```

The central security principle is:

> **A Tool may possess a capability without possessing authority, and a caller may possess authority without being granted access to every capability.**

Tool Security exists to ensure that capability, authority, scope and execution remain explicitly separated and independently enforceable.

# End of TOOLS-003
