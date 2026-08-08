# EXAMPLES-008 — End-to-End

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
- EXAMPLES-007
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

This document demonstrates a complete VIAL workflow from initial intent to final audited result.

It combines the concepts demonstrated by the previous examples.

---

# 2. Scenario

An industrial organization operates multiple plants using a distributed VIAL deployment.

An autonomous monitoring component detects an abnormal condition and requests a controlled operational adjustment.

```text
Organization
    ↓
Distributed Runtime
    ↓
Context
    ↓
Autonomous Agent
    ↓
Decision
    ↓
Tool Discovery
    ↓
Authorization
    ↓
Approval
    ↓
Invocation
    ↓
Execution
    ↓
Verification
    ↓
Audit
```

---

# 3. Organization

```text
Organization:
    org.example.industrial
```

The Organization owns multiple plants.

---

# 4. Tenant / Domain

The target is:

```text
Plant:
    plant-a
```

---

# 5. Resource

The target Resource is:

```text
resource.plant-a.pasteurizer-01
```

Associated Resources include:

```text
temperature-01
pressure-01
pump-01
```

---

# 6. Autonomous Principal

The monitoring agent is:

```text
principal.agent.pasteurizer
```

Its authority is explicitly bounded.

---

# 7. Initial Context

```text
Context:
    organization: org.example.industrial
    plant: plant-a
    equipment: pasteurizer-01
    temperature: 72.5
    pressure: 2.1
    recipe: recipe-A
    production_state: RUNNING
```

---

# 8. Observation

The agent discovers and invokes read-only Tools:

```text
tool.sensor.read_temperature
tool.sensor.read_pressure
```

The results are validated.

---

# 9. Abnormal Condition

The agent determines that pressure is outside the desired operating range.

The observation itself does not authorize an action.

---

# 10. Decision

The agent produces:

```text
Decision:
    intent: stabilize pressure
    target: pump-01
    proposed_action: reduce speed
```

---

# 11. Authority Evaluation

The Runtime evaluates:

```text
Organization
Principal
Context
Decision
Resource
Tool
Policy
```

---

# 12. Tool Discovery

The required capability is:

```text
adjust pump speed
```

Discovery returns:

```text
tool.pump.set_speed
```

---

# 13. Contract

The Tool Contract defines:

```text
Input:
    resource_id
    speed

Side Effects:
    changes pump state

Risk:
    HIGH
```

---

# 14. Authorization

The agent is permitted to request the operation within a bounded range.

Example:

```text
minimum: 30%
maximum: 70%
```

---

# 15. Approval

Because the operation has material side effects, approval is required.

An authorized engineer approves the specific operation.

```text
Approval:
    principal.engineer
    target: pump-01
    operation: set_speed
```

---

# 16. Invocation

The Runtime creates:

```text
Invocation:
    id: inv-000042

Tool:
    tool.pump.set_speed@1.0.0

Resource:
    resource.plant-a.pump-01

Input:
    speed: 55%
```

---

# 17. Invocation Validation

The Runtime validates:

```text
Tool exists
Contract valid
Tool active
Input valid
Principal authorized
Approval valid
Resource authorized
Context valid
```

---

# 18. Execution

The Runtime executes the Tool within the authorized environment.

```text
AUTHORIZED
    ↓
EXECUTING
    ↓
SUCCEEDED
```

---

# 19. Postcondition

The Runtime verifies the Resource state.

```text
pump.speed = 55%
```

It then reads the pressure again.

```text
pressure = 2.0
```

The postcondition is satisfied.

---

# 20. Result

The final result contains:

```text
Invocation:
    inv-000042

Status:
    SUCCESS

Tool:
    tool.pump.set_speed@1.0.0

Resource:
    resource.plant-a.pump-01

Result:
    speed = 55%

Verification:
    pressure = 2.0
```

---

# 21. Provenance

The result is attributable to:

```text
Organization
Plant
Principal
Decision
Tool
Version
Invocation
Runtime
Resource
Timestamp
```

---

# 22. Audit

The complete operation is recorded.

```text
Observation
    ↓
Decision
    ↓
Authorization
    ↓
Approval
    ↓
Invocation
    ↓
Execution
    ↓
Verification
```

---

# 23. Failure Variant

Suppose communication with Plant A fails after the command is sent.

The invocation becomes:

```text
UNKNOWN
```

The system does not automatically repeat the command.

---

# 24. Recovery

The Runtime reconnects and reads the authoritative Resource state.

If:

```text
pump.speed = 55%
```

the operation is confirmed.

If the state is unknown, the system escalates.

---

# 25. Security Variant

Suppose the agent requests:

```text
pump.speed = 90%
```

The request exceeds its authorized range.

The Runtime returns:

```text
AUTHORIZATION_DENIED
```

No execution occurs.

---

# 26. Multi-Tenant Variant

If the agent attempts to access a Resource belonging to another Organization:

```text
ACCESS_DENIED
```

The shared infrastructure does not grant cross-tenant authority.

---

# 27. Lifecycle Variant

If the Tool is suspended during the operation:

```text
Tool:
    SUSPENDED
```

New invocations MUST be rejected according to lifecycle policy.

---

# 28. Complete Architecture

```text
                         VIAL
                          │
                    Organization
                          │
                   Distributed Runtime
                          │
              ┌───────────┴───────────┐
              │                       │
          Context                  Security
              │                       │
              └───────────┬───────────┘
                          │
                    Autonomous Agent
                          │
                       Decision
                          │
                    Tool Discovery
                          │
                    Authorization
                          │
                       Approval
                          │
                      Invocation
                          │
                       Execution
                          │
                     Verification
                          │
                        Audit
```

---

# 29. Concepts Covered

This example combines:

* Organization;
* multi-tenancy;
* Resources;
* Context;
* Decisions;
* authority;
* autonomous operation;
* Tool Registry;
* Tool Discovery;
* Tool Contracts;
* Tool Security;
* Tool Invocation;
* Tool Execution;
* Tool Lifecycle;
* distributed Runtime;
* failure handling;
* recovery;
* audit;
* provenance.

---

# 30. End-to-End Invariant

At every stage:

```text
Identity
+
Context
+
Authority
+
Contract
+
Security
+
Lifecycle
```

remain enforceable.

---

# 31. Conformance

A complete VIAL implementation SHOULD be capable of expressing and executing the complete workflow demonstrated here while preserving the same governance principles at every boundary.

---

# 32. Final Principle

> **VIAL is complete when intent can travel from Organization to Resource through Context, Decision, Tool and Runtime while authority, security, provenance and governance remain intact from beginning to end.**

# End of EXAMPLES-008
