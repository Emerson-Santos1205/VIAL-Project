# TOOLS-004 — Tool Registry

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Tools Specification
**Depends On:** TOOLS-001 — Tool Model, TOOLS-002 — Tool Contract, TOOLS-003 — Tool Security, SDK-001 — Architecture, SDK-002 — Organization API, SDK-003 — Resource API, SDK-004 — Context API, SDK-005 — Decision API, RFC-002, RFC-003, RFC-004, RFC-005, RFC-006

---

# 1. Abstract

This document defines the Tool Registry model within VIAL.

The Tool Registry is the authoritative mechanism for registering, identifying, describing, locating and managing Tools available to the VIAL Runtime.

The fundamental principle is:

> **A Tool cannot be reliably discovered, governed or invoked unless its identity and Contract are registered in an authoritative Registry.**

---

# 2. Purpose

The Registry provides:

* Tool identity;
* Tool metadata;
* Contract association;
* version information;
* lifecycle state;
* ownership;
* security classification;
* availability information;
* implementation references;
* provenance;
* registration history.

---

# 3. Registry Model

Conceptually:

```text
Tool
 │
 ▼
Registry
 │
 ├── Identity
 ├── Contract
 ├── Version
 ├── Owner
 ├── Security
 ├── Lifecycle
 └── Implementation
```

---

# 4. Registry Entry

Every registered Tool MUST have a Registry Entry.

Conceptually:

```text
ToolRegistryEntry {
    tool_id
    name
    version
    contract
    owner
    lifecycle
    security
    implementation
    metadata
}
```

---

# 5. Tool Identity

The `tool_id` MUST uniquely identify the Tool within its namespace.

The identifier SHOULD remain stable across compatible versions.

---

# 6. Tool Name

A human-readable name SHOULD accompany the Tool ID.

The name MUST NOT be used as the sole identity mechanism.

---

# 7. Contract Association

Every active Tool MUST reference a valid Tool Contract.

```text
Registry
   │
   ▼
Tool
   │
   ▼
Contract
```

A Tool without a valid Contract SHOULD NOT be available for normal invocation.

---

# 8. Version

The Registry MUST identify the Tool implementation and Contract versions where they are independently versioned.

Example:

```text
tool_version: 2.1.0
contract_version: 2.0.0
```

---

# 9. Ownership

Every registered Tool SHOULD have an identified owner.

The owner is responsible for:

* maintenance;
* security;
* Contract integrity;
* lifecycle management;
* incident response.

---

# 10. Registration

Tool registration MUST be an authorized operation.

Registration SHOULD validate:

1. identity;
2. Contract;
3. implementation;
4. security requirements;
5. ownership;
6. lifecycle metadata.

---

# 11. Registration Validation

A Tool MUST NOT become active merely because a registration request exists.

Conceptually:

```text
Registration
     ↓
Validation
     ↓
Approval
     ↓
Published
     ↓
Active
```

---

# 12. Duplicate Identity

The Registry MUST prevent conflicting active entries with the same Tool identity and version.

---

# 13. Namespace

Tool IDs SHOULD belong to an explicit namespace.

Example:

```text
tool.sensor.read_temperature
tool.pump.set_speed
```

Namespaces SHOULD support organizational isolation.

---

# 14. Version Resolution

The Registry MAY support multiple versions of the same Tool.

Version resolution MUST be deterministic.

---

# 15. Active Version

The Registry MAY identify an active/default version.

Consumers MUST NOT assume that the latest version is automatically the active version.

---

# 16. Lifecycle State

A Tool Registry Entry SHOULD have a lifecycle state.

Recommended states:

```text
DRAFT
VALIDATING
PUBLISHED
ACTIVE
SUSPENDED
DEPRECATED
RETIRED
```

---

# 17. Suspension

A Tool MAY be suspended without being retired.

Suspension MUST prevent new invocations according to Runtime policy.

---

# 18. Deprecation

A deprecated Tool remains identifiable but SHOULD NOT be selected for new operations unless explicitly requested or required.

---

# 19. Retirement

A retired Tool MUST NOT be presented as an active capability.

Historical information SHOULD remain available for audit.

---

# 20. Implementation Reference

The Registry MAY reference:

```text
Service
Container
Executable
Package
Remote Endpoint
Runtime Module
```

The implementation reference MUST NOT replace the Tool Contract.

---

# 21. Security Metadata

Registry entries SHOULD contain security metadata such as:

```text
required_permissions
risk_level
data_classification
side_effects
isolation_requirement
```

---

# 22. Availability

The Registry MAY record availability information.

Availability metadata MUST NOT be interpreted as authorization.

---

# 23. Health

The Registry MAY maintain Tool health status.

Example:

```text
HEALTHY
DEGRADED
UNAVAILABLE
UNKNOWN
```

Health status SHOULD be distinguishable from lifecycle state.

---

# 24. Registry Integrity

Registry data MUST be protected against unauthorized modification.

Changes SHOULD be attributable and auditable.

---

# 25. Registry Query

Consumers SHOULD be able to query the Registry using:

```text
tool_id
capability
version
organization
lifecycle
security
```

---

# 26. Registry and Discovery

TOOLS-004 establishes authoritative registration.

TOOLS-005 defines how callers discover Tools from that Registry.

---

# 27. Registry and Invocation

TOOLS-006 MUST resolve invocation targets through an authoritative Tool identity and version.

---

# 28. Registry and Execution

TOOLS-007 executes the implementation associated with the resolved Registry Entry.

---

# 29. Registry and Lifecycle

TOOLS-008 governs transitions between lifecycle states.

---

# 30. Audit

Registry operations SHOULD record:

```text
registration
modification
activation
suspension
deprecation
retirement
```

Each event SHOULD contain:

```text
actor
timestamp
Tool ID
version
change
reason
```

---

# 31. Registry Conformance

A conforming Registry MUST:

1. uniquely identify Tools;
2. associate active Tools with Contracts;
3. enforce registration authority;
4. maintain lifecycle state;
5. prevent conflicting identities;
6. preserve version information;
7. support auditability;
8. protect Registry integrity.

---

# 32. Final Principle

> **The Registry is the authoritative identity and governance layer for Tools.**

A Tool becomes a governed VIAL capability only when its identity, Contract, security properties and lifecycle are represented consistently in the Registry.

# End of TOOLS-004
