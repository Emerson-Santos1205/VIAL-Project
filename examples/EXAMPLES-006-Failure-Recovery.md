# EXAMPLES-006 — Failure & Recovery

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Example Specification
Depends On:
- EXAMPLES-001
- EXAMPLES-002
- EXAMPLES-003
- EXAMPLES-004
- EXAMPLES-005
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

This document demonstrates failure handling and recovery in VIAL.

The objective is to show that failures are explicit states and that recovery does not bypass governance.

---

# 2. Scenario

An industrial Tool is invoked to read equipment state.

During execution, the remote Resource becomes unavailable.

```text
Invocation
    ↓
Tool
    ↓
Resource unavailable
```

---

# 3. Failure Classification

VIAL SHOULD distinguish:

```text
Validation Failure
Authorization Failure
Tool Failure
Resource Failure
Runtime Failure
Network Failure
Timeout
Unknown Outcome
```

---

# 4. Validation Failure

Invalid input MUST prevent execution.

```text
INVALID_INPUT
```

No Tool side effect should occur.

---

# 5. Authorization Failure

If authorization fails:

```text
ACCESS_DENIED
```

The Tool MUST NOT execute.

---

# 6. Tool Failure

If the Tool executes but fails:

```text
TOOL_EXECUTION_FAILED
```

The result MUST explicitly indicate failure.

---

# 7. Resource Failure

If the target Resource is unavailable:

```text
RESOURCE_UNAVAILABLE
```

---

# 8. Network Failure

For distributed operations:

```text
REMOTE_RUNTIME_UNAVAILABLE
```

The Runtime MUST NOT fabricate the Resource state.

---

# 9. Timeout

A bounded operation may reach:

```text
TIMEOUT
```

Timeout MUST be distinguishable from successful completion.

---

# 10. Unknown Outcome

If the system loses communication after the operation may have executed:

```text
UNKNOWN
```

The system MUST NOT blindly retry a non-idempotent operation.

---

# 11. Retry

Retry policy MUST consider:

```text
idempotency
side effects
authorization
timeout
Resource state
```

---

# 12. Idempotent Example

A read-only operation may safely be retried:

```text
read_temperature
```

---

# 13. Non-Idempotent Example

A command such as:

```text
set_pump_speed
```

MUST NOT automatically repeat when execution status is unknown unless the Contract explicitly permits safe retry.

---

# 14. Recovery

Recovery SHOULD follow:

```text
Failure
   ↓
Classify
   ↓
Determine Retryability
   ↓
Recover / Escalate
   ↓
Verify State
   ↓
Resume
```

---

# 15. State Reconciliation

After communication recovery, authoritative Resource state SHOULD be queried.

---

# 16. Compensation

If an operation partially succeeds, a compensating operation MAY be required.

Compensation MUST itself be authorized.

---

# 17. Recovery Authority

Recovery mechanisms MUST NOT create authority that did not exist before the failure.

---

# 18. Audit

Failures SHOULD record:

```text
Invocation
Failure
Timestamp
Tool
Resource
Principal
Recovery Action
Final State
```

---

# 19. Recovery Example

```text
Set pump speed
      ↓
Network failure
      ↓
Outcome UNKNOWN
      ↓
Reconnect
      ↓
Read pump state
      ↓
State = 55%
      ↓
Operation confirmed
```

The system does not repeat the original command unnecessarily.

---

# 20. Recovery Failure

If reconciliation fails:

```text
UNKNOWN
```

The system SHOULD escalate rather than assume success or failure.

---

# 21. Circuit Breaker

Frequently failing Tools MAY be temporarily suspended through operational policy.

---

# 22. Tool Lifecycle

Repeated critical failures MAY cause:

```text
ACTIVE
   ↓
SUSPENDED
```

according to lifecycle policy.

---

# 23. Human Escalation

Critical unresolved failures SHOULD be escalated to an authorized human.

---

# 24. Recovery Limits

Recovery SHOULD have:

```text
maximum retries
maximum duration
maximum compensation attempts
```

---

# 25. Safety

Recovery MUST prioritize preventing unintended side effects over automatic completion.

---

# 26. Conformance

A conforming implementation MUST:

1. classify failures;
2. distinguish unknown outcomes;
3. prevent false success;
4. apply bounded retry;
5. respect idempotency;
6. preserve authorization;
7. reconcile state when required;
8. audit recovery;
9. support escalation.

---

# 27. Final Principle

> **Failure recovery restores a governed system state; it must never use failure as a reason to bypass governance.**

# End of EXAMPLES-006
