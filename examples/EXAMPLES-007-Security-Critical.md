# EXAMPLES-007 — Security-Critical

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
- EXAMPLES-006
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

This document demonstrates VIAL in a security-critical environment.

The example emphasizes strict authorization, least privilege, approval, isolation, audit and emergency control.

---

# 2. Scenario

A Tool controls a safety-relevant industrial actuator.

```text
Safety System
      │
      ▼
Controlled Resource
      ▲
      │
VIAL Tool
```

---

# 3. Risk Classification

The Tool is classified:

```text
Risk:
    CRITICAL
```

Its operations require elevated governance.

---

# 4. Principal

A normal operator may observe the Resource but cannot directly execute the critical operation.

```text
Operator:
    READ

Safety Engineer:
    READ + CONTROL

Administrator:
    POLICY
```

---

# 5. Least Privilege

Each principal receives only the minimum permissions required.

---

# 6. Tool Contract

The Contract defines:

```text
Side Effects:
    critical

Required Approval:
    true

Maximum Operation Scope:
    explicitly defined
```

---

# 7. Security Context

The invocation MUST contain a trusted security context.

---

# 8. Authentication

The Runtime MUST authenticate the principal before authorization.

---

# 9. Authorization

Authorization evaluates:

```text
Identity
Organization
Role
Resource
Tool
Operation
Context
Policy
```

---

# 10. Approval

Critical operations require an explicit approval.

```text
Request
  ↓
Authorization
  ↓
Approval
  ↓
Execution
```

---

# 11. Separation of Duties

Where required, the requester and approver SHOULD be different principals.

---

# 12. Approval Scope

Approval MUST be bound to the specific:

```text
Tool
Resource
Operation
Context
```

---

# 13. Approval Expiration

Approvals SHOULD expire after a defined period.

---

# 14. Replay Protection

Approval credentials SHOULD NOT be reusable for unrelated invocations.

---

# 15. Tool Isolation

Critical Tools SHOULD execute within a hardened environment.

---

# 16. Credential Isolation

Credentials MUST NOT be exposed to unauthorized Tools, Context or callers.

---

# 17. Resource Isolation

A critical Tool MUST NOT access Resources outside its authorized scope.

---

# 18. Emergency Disable

The system SHOULD support emergency Tool suspension.

```text
ACTIVE
   ↓
EMERGENCY SUSPENDED
```

---

# 19. Emergency Authority

Emergency controls SHOULD be independent from the Tool being controlled.

A Tool MUST NOT disable the mechanism that can stop it.

---

# 20. Audit

Every critical invocation MUST be auditable.

Audit SHOULD include:

```text
principal
Tool
Resource
Decision
Approval
Invocation
Result
Timestamp
```

---

# 21. Tamper Resistance

Security-critical audit information SHOULD be protected against unauthorized alteration.

---

# 22. Failure

If any critical security requirement fails:

```text
DENY
```

The system SHOULD fail closed.

---

# 23. Unknown Security State

If the Runtime cannot establish the required security state, the operation MUST NOT proceed.

---

# 24. Security Event

A suspicious invocation MAY generate:

```text
SECURITY_EVENT
```

The event SHOULD be independently recorded.

---

# 25. Rate Limiting

Critical Tools SHOULD have strict rate and concurrency limits.

---

# 26. Monitoring

Critical operations SHOULD be monitored in real time where appropriate.

---

# 27. Recovery

Recovery from a security incident SHOULD include:

```text
Suspend
Investigate
Validate
Authorize
Reactivate
```

---

# 28. Lifecycle Integration

A critical Tool may transition:

```text
ACTIVE
   ↓
SUSPENDED
   ↓
SECURITY REVIEW
   ↓
ACTIVE
```

or:

```text
ACTIVE
   ↓
RETIRED
```

---

# 29. Example Attack

An unauthorized operator attempts:

```text
tool.safety.disable
```

The Runtime evaluates authorization and returns:

```text
ACCESS_DENIED
```

No Tool execution occurs.

---

# 30. Privilege Escalation

A Tool MUST NOT use its execution privileges to grant additional authority to its caller.

---

# 31. Policy Modification

A Tool MUST NOT modify its own security policy unless explicitly authorized and governed as a separate operation.

---

# 32. Conformance

A security-critical implementation MUST:

1. enforce authentication;
2. enforce least privilege;
3. enforce explicit authorization;
4. support approval where required;
5. support separation of duties where required;
6. isolate credentials;
7. isolate Resources;
8. support emergency suspension;
9. fail safely;
10. preserve tamper-resistant auditability.

---

# 33. Final Principle

> **The higher the consequence of an operation, the stronger and more explicit its authority, isolation, verification and audit requirements must be.**

# End of EXAMPLES-007
