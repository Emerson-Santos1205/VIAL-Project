# TOOLS-006 — Tool Invocation

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Tools Specification
**Depends On:** TOOLS-001 — Tool Model, TOOLS-002 — Tool Contract, TOOLS-003 — Tool Security, TOOLS-004 — Tool Registry, TOOLS-005 — Tool Discovery, SDK-001 — Architecture, SDK-002 — Organization API, SDK-003 — Resource API, SDK-004 — Context API, SDK-005 — Decision API, RFC-002, RFC-003, RFC-004, RFC-005, RFC-006

---

# 1. Abstract

This document defines the invocation model for VIAL Tools.

Invocation is the controlled transition from a request for a Tool capability to an authorized Tool execution.

The fundamental principle is:

> **Invocation is a governed operation, not a direct function call.**

---

# 2. Invocation Flow

```text
Request
  ↓
Resolve Tool
  ↓
Resolve Contract
  ↓
Validate Input
  ↓
Authenticate
  ↓
Authorize
  ↓
Check Preconditions
  ↓
Create Invocation
  ↓
Execute
  ↓
Return Result
```

---

# 3. Invocation Identity

Every invocation SHOULD have a unique Invocation ID.

Example:

```text
INV-2026-000001
```

---

# 4. Invocation Request

Conceptually:

```text
InvocationRequest {
    tool_id
    version
    input
    principal
    context
    resource
    decision
}
```

---

# 5. Tool Resolution

The Runtime MUST resolve the requested Tool against the Registry.

An invocation MUST NOT execute an unknown Tool.

---

# 6. Contract Resolution

The Runtime MUST resolve the Contract associated with the selected Tool version.

---

# 7. Input Validation

Input MUST be validated against the Contract before execution.

Invalid input MUST prevent execution.

---

# 8. Authentication

The Runtime MUST establish the identity required for authorization.

---

# 9. Authorization

The Runtime MUST evaluate whether the principal is authorized for the requested operation.

Possible results:

```text
ALLOW
DENY
REQUIRE_APPROVAL
```

---

# 10. Resource Authorization

If the invocation targets a Resource, the Runtime MUST verify that the principal is authorized for that Resource.

---

# 11. Context Validation

Context supplied to an invocation MUST be validated according to its trust and relevance.

---

# 12. Decision Association

An invocation MAY reference a Decision.

The Decision SHOULD provide intent, authority context or justification where applicable.

---

# 13. Invocation Preconditions

The Runtime MUST evaluate required preconditions before execution.

---

# 14. Invocation Record

Before consequential execution, the Runtime SHOULD create an Invocation Record containing:

```text
invocation_id
principal
tool_id
version
contract_version
resource
decision
timestamp
authorization
```

---

# 15. Idempotency

Where supported, the invocation SHOULD accept an idempotency key.

This prevents unintended duplicate execution.

---

# 16. Replay Protection

Security-sensitive invocations SHOULD use replay protection.

---

# 17. Approval

If the Contract or Security Policy requires approval, execution MUST wait for valid approval.

---

# 18. Invocation State

An invocation MAY transition through:

```text
REQUESTED
VALIDATING
AUTHORIZED
APPROVED
EXECUTING
SUCCEEDED
FAILED
CANCELLED
REJECTED
```

---

# 19. Rejection

Rejected invocations MUST NOT execute the Tool operation.

---

# 20. Cancellation

If cancellation is supported, the Runtime MUST apply the Contract's cancellation semantics.

---

# 21. Timeout

Invocation timeout MUST follow the Contract and Runtime limits.

---

# 22. Invocation Result

A successful invocation SHOULD return:

```text
InvocationResult {
    invocation_id
    status
    data
    metadata
    provenance
}
```

---

# 23. Error Result

Failures SHOULD return structured errors.

Example:

```text
{
    "invocation_id": "...",
    "status": "FAILED",
    "error": {
        "code": "TIMEOUT"
    }
}
```

---

# 24. No False Success

The Runtime MUST NOT report successful execution unless the Tool actually reached the declared success condition.

---

# 25. Side Effects

Invocation processing MUST respect the side-effect declaration of the Contract.

---

# 26. Security Context

The security context MUST be bound to the invocation.

---

# 27. Scope

Invocation scope MUST be explicit for consequential operations.

---

# 28. Tool Chaining

When one invocation causes another Tool invocation, the downstream invocation MUST have its own Invocation ID and authorization evaluation.

---

# 29. Recursive Calls

Recursive Tool invocation MUST be bounded.

---

# 30. Observability

Invocation SHOULD expose:

```text
status
duration
Tool
version
result
error
```

without exposing sensitive information.

---

# 31. Audit

Consequential invocations MUST be auditable.

---

# 32. Invocation Integrity

The Invocation Record SHOULD be protected against unauthorized modification.

---

# 33. Invocation Failure

The Runtime SHOULD fail safely when:

* Tool cannot be resolved;
* Contract cannot be resolved;
* authorization cannot be established;
* preconditions fail;
* security context is invalid.

---

# 34. Conformance

A conforming Invocation mechanism MUST:

1. resolve the Tool;
2. resolve its Contract;
3. validate input;
4. establish identity;
5. authorize execution;
6. enforce scope;
7. respect preconditions;
8. create traceable invocation state;
9. return structured results;
10. prevent false success.

---

# 35. Final Principle

> **A Tool invocation is the controlled, attributable and security-validated transition from capability request to execution.**

# End of TOOLS-006
