# TOOLS-007 — Tool Execution

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Tools Specification
Depends On:
- TOOLS-001
- TOOLS-002
- TOOLS-003
- TOOLS-004
- TOOLS-005
- TOOLS-006
- SDK-001
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

This document defines the execution semantics of Tools within VIAL.

Invocation determines whether an operation may occur. Execution performs the operation according to the Tool Contract.

The fundamental principle is:

> **Execution MUST remain within the authority, Contract and scope established by invocation.**

---

# 2. Execution Model

```text
Authorized Invocation
        ↓
Execution Environment
        ↓
Tool Implementation
        ↓
Outcome
        ↓
Postcondition Validation
        ↓
Audit
```

---

# 3. Execution Boundary

Execution MUST occur within the security and operational boundaries established by the Runtime.

---

# 4. Execution Identity

Execution MUST remain attributable to its Invocation ID.

---

# 5. Implementation Resolution

The Runtime MUST execute the implementation associated with the resolved Registry Entry.

---

# 6. Contract Compliance

The implementation MUST conform to its Contract.

---

# 7. Input

Execution MUST receive only validated input.

The implementation MUST NOT bypass Contract validation.

---

# 8. Security Context

Execution MUST operate under the authorized Security Context.

---

# 9. Resource Scope

Execution MUST NOT access Resources outside the authorized scope.

---

# 10. Environment Isolation

Tools SHOULD execute in an environment appropriate to their risk.

Possible boundaries include:

```text
Process
Container
Sandbox
VM
Service
```

---

# 11. Resource Limits

The Runtime MAY enforce:

```text
CPU
Memory
Storage
Network
Execution Time
Concurrency
```

---

# 12. Timeout

Execution MUST respect applicable timeout limits.

---

# 13. Cancellation

If cancellation is requested, execution MUST follow the Contract's cancellation semantics.

---

# 14. Side Effects

Execution MUST perform only side effects declared or explicitly permitted by the Contract.

---

# 15. External Systems

External system interactions MUST remain within authorized destinations and credentials.

---

# 16. Result Validation

The Runtime SHOULD validate the Tool outcome against the Contract output schema.

---

# 17. Postconditions

Where defined, postconditions SHOULD be evaluated after execution.

---

# 18. Execution Success

Execution SHOULD be considered successful only when:

```text
Tool completed
AND
output is valid
AND
required postconditions are satisfied
```

---

# 19. Partial Execution

If an operation partially executes, the result MUST explicitly indicate partial completion.

The system MUST NOT represent partial execution as complete success.

---

# 20. Failure

Execution failures SHOULD identify:

```text
failure_code
message
retryability
invocation_id
```

---

# 21. Retry

Retries MUST respect:

* idempotency;
* authorization;
* timeout;
* rate limits;
* side effects.

---

# 22. Non-Idempotent Execution

Non-idempotent Tools SHOULD NOT be automatically retried unless the Contract explicitly permits it.

---

# 23. Compensation

A Tool MAY define compensation behavior for partial or failed execution.

Compensation is not equivalent to guaranteed rollback.

---

# 24. Transaction Semantics

If transactional behavior is supported, the Contract MUST define its guarantees.

---

# 25. Concurrency

Concurrent execution MUST respect Tool and Resource concurrency constraints.

---

# 26. Race Prevention

Where Resource state affects execution, the Runtime SHOULD validate relevant state close to execution.

---

# 27. Tool Chaining

Execution of downstream Tools MUST create separate governed invocations.

---

# 28. Recursive Execution

Recursive execution MUST be bounded to prevent uncontrolled loops.

---

# 29. Provenance

Results SHOULD contain sufficient provenance to identify:

```text
Tool
Version
Invocation
Execution Time
Source
```

---

# 30. Observability

Execution SHOULD expose operational telemetry without leaking sensitive data.

---

# 31. Audit

Consequential execution MUST be recorded in the audit trail.

---

# 32. Execution Integrity

The Runtime SHOULD verify that the executed implementation corresponds to the expected Tool version.

---

# 33. Artifact Integrity

Where applicable, Tool artifacts SHOULD be verified using:

```text
signature
checksum
trusted source
version
```

---

# 34. Runtime Failure

Runtime infrastructure failure MUST be distinguishable from Tool-level failure.

Example:

```text
RUNTIME_FAILURE
```

versus:

```text
TOOL_EXECUTION_FAILED
```

---

# 35. Dependency Failure

External dependency failures SHOULD be explicitly represented.

Example:

```text
DEPENDENCY_UNAVAILABLE
```

---

# 36. Security Failure

Security failures MUST remain distinguishable from normal Tool execution failures.

---

# 37. Execution State

Execution MAY use:

```text
CREATED
STARTING
RUNNING
COMPLETING
SUCCEEDED
FAILED
CANCELLED
TIMED_OUT
```

---

# 38. State Integrity

Execution state transitions MUST be controlled by the Runtime.

---

# 39. Execution Isolation

High-risk Tools SHOULD have stronger isolation than low-risk read-only Tools.

---

# 40. Output Handling

Tool results MUST be returned through the controlled Runtime path.

The implementation SHOULD NOT directly bypass Runtime governance.

---

# 41. Logging

Logs SHOULD include:

```text
invocation_id
tool_id
version
state
duration
result_status
```

Sensitive values SHOULD be redacted.

---

# 42. Security Principle

Execution MUST NOT:

* elevate privileges;
* expand Resource scope;
* access unauthorized data;
* modify Contract semantics;
* bypass audit;
* fabricate results.

---

# 43. Conformance

A conforming execution layer MUST:

1. execute only authorized invocations;
2. enforce Contract semantics;
3. preserve security context;
4. respect Resource scope;
5. enforce operational limits;
6. validate results;
7. distinguish failure types;
8. preserve provenance;
9. maintain auditability;
10. prevent unauthorized side effects.

---

# 44. Final Principle

> **Execution is the realization of an already authorized capability, not a mechanism for obtaining additional authority.**

# End of TOOLS-007
