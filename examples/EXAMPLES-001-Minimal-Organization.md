# EXAMPLES-001 — Minimal Organization

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Example Specification
Depends On:
- FCP-002A
- RFC-002
- RFC-003
- RFC-004
- RFC-005
- RFC-006
- RUNTIME-001
- RUNTIME-002
- RUNTIME-003
- RUNTIME-004
- RUNTIME-005
- RUNTIME-006
- SDK-001
- SDK-002
- SDK-003
- SDK-004
- SDK-005
- TOOLS-001
- TOOLS-002
- TOOLS-003
- TOOLS-004
- TOOLS-005
- TOOLS-006
- TOOLS-007
- TOOLS-008

---

# 1. Purpose

This document presents the smallest meaningful VIAL deployment.

The example demonstrates how the fundamental VIAL concepts operate together:

Domain-specific values in this example are illustrative and MUST NOT be interpreted as introducing new normative states, fields, identifiers or error codes.

```text
Organization
Resource
Context
Decision
Tool
Runtime
```

The objective is to demonstrate the minimum complete system rather than a production-scale deployment.

---

# 2. Scenario

A small organization manages a single industrial resource.

The organization has one authorized operator and one Tool capable of reading the state of the Resource.

```text
Organization
    │
    └── Resource
          │
          └── Tool
```

---

# 3. Organization

```text
Organization:
    id: ORG-001
    name: Minimal Organization
```

The Organization represents the administrative and authority boundary.

---

# 4. Principal

The example contains one principal:

```text
Principal:
    id: user.operator
    role: operator
```

The principal is authorized to interact with the Resource according to the applicable policy.

---

# 5. Resource

The Organization contains one Resource:

```text
Resource:
    id: RES-001
    type: temperature_sensor
```

The Resource represents the entity whose state may be observed.

---

# 6. Tool

The Tool provides the capability:

```text
Tool:
    id: TOOL-001
    version: 1.0.0
```

Capability:

```text
read_temperature
```

The Tool is registered according to the Tool Registry model.

---

# 7. Contract

The Tool Contract defines:

```text
Input:
    resource_id

Output:
    temperature

Side Effects:
    none
```

The Tool is therefore a read-only capability.

---

# 8. Context

The Runtime creates Context for the operation.

Example:

```text
Context:
    organization: ORG-001
    principal: user.operator
    resource: RES-001
    operation: read_temperature
```

---

# 9. Decision

The Decision establishes the intended operation.

```text
Decision:
    id: DEC-001
    objective: obtain current temperature
    resource: RES-001
    tool: TOOL-001
```

---

# 10. Authorization

The Runtime evaluates:

```text
Principal
    ↓
Organization
    ↓
Resource
    ↓
Tool
    ↓
Operation
```

The operation is authorized.

---

# 11. Discovery

The Tool may be discovered through the Registry.

The caller does not need to know the implementation details.

Conceptually:

```text
"Read the current temperature"
        ↓
Tool Discovery
        ↓
TOOL-001
```

---

# 12. Invocation

The Runtime creates an Invocation:

```text
Invocation:
    id: INV-001
    tool: TOOL-001
    resource: RES-001
```

The Contract is validated before execution.

---

# 13. Execution

The Tool reads the Resource.

Example result:

```text
{
    "resource_id": "RES-001",
    "temperature": 72.4,
    "unit": "C"
}
```

---

# 14. Result

The Runtime returns the validated result to the caller.

The result remains associated with the Invocation ID.

---

# 15. Audit

The operation produces an auditable event:

```text
Invocation:
    INV-001

Principal:
    user.operator

Tool:
    TOOL-001@1.0.0

Resource:
    RES-001

Result:
    SUCCESS
```

---

# 16. Complete Flow

```text
User
 │
 ▼
Organization
 │
 ▼
Context
 │
 ▼
Decision
 │
 ▼
Tool Discovery
 │
 ▼
Authorization
 │
 ▼
Invocation
 │
 ▼
Execution
 │
 ▼
Result
 │
 ▼
Audit
```

---

# 17. What This Example Demonstrates

This example demonstrates the minimum relationship between:

* Organization;
* Principal;
* Resource;
* Context;
* Decision;
* Tool;
* Contract;
* Authorization;
* Invocation;
* Execution;
* Audit.

---

# 18. What It Does Not Demonstrate

This example intentionally excludes:

* multiple Organizations;
* distributed execution;
* complex Resource relationships;
* high-risk operations;
* multi-party authorization;
* Tool chaining;
* failure recovery.

Those concerns are demonstrated by later examples.

---

# 19. Conformance

A minimal VIAL implementation SHOULD be capable of reproducing this scenario.

---

# 20. Final Principle

> **The Minimal Organization example demonstrates the smallest complete governed VIAL operation.**

# End of EXAMPLES-001
