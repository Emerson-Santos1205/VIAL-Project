# EXAMPLES-005 — Autonomous

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Example Specification
Depends On:
- EXAMPLES-001
- EXAMPLES-002
- EXAMPLES-003
- EXAMPLES-004
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

This document demonstrates an autonomous VIAL workflow.

Domain-specific values in this example are illustrative and MUST NOT be interpreted as introducing new normative states, fields, identifiers or error codes.

The example shows how an autonomous component can observe Resources, produce Decisions and invoke Tools while remaining bounded by predefined authority.

---

# 2. Principle

Autonomy does not mean unrestricted authority.

```text
Autonomy
    ≠
Unlimited Authority
```

The autonomous component remains subject to VIAL governance.

---

# 3. Scenario

An autonomous industrial agent monitors a pasteurization system.

```text
Sensors
   ↓
Context
   ↓
Agent
   ↓
Decision
   ↓
Tool
   ↓
Equipment
```

---

# 4. Autonomous Principal

The autonomous agent has an explicit identity:

```text
principal.agent.pasteurizer
```

The identity is subject to authorization.

---

# 5. Scope

The agent is authorized only to perform predefined operations.

Example:

```text
Allowed:
    read temperature
    read pressure
    adjust pump speed within limits

Denied:
    disable safety interlock
    modify security policy
    access unrelated equipment
```

---

# 6. Context

The agent receives operational Context:

```text
equipment
temperature
pressure
recipe
production_state
alarm_state
time
```

---

# 7. Observation

The agent invokes read-only Tools.

Example:

```text
TOOL-001
TOOL-002
```

---

# 8. Decision

The agent evaluates the observed state.

Example:

```text
Decision:
    objective: stabilize pressure
    target: pump-01
    outcome: reduce speed
```

---

# 9. Decision Authority

The Decision does not expand the agent's authority.

The proposed action MUST remain inside the agent's authorization scope.

---

# 10. Policy Boundary

Example policy:

```text
pump_speed:
    minimum: 30%
    maximum: 70%
```

The agent MUST NOT issue a Tool invocation outside that range.

---

# 11. Tool Discovery

The agent may discover the appropriate Tool.

```text
Capability:
    adjust pump speed

Tool:
    TOOL-003
```

---

# 12. Invocation

The agent creates a governed invocation.

```text
principal:
    principal.agent.pasteurizer

tool:
    TOOL-003

resource:
    RES-001

input:
    speed: 55%
```

---

# 13. Authorization

The Runtime independently evaluates the invocation.

The agent cannot authorize itself.

---

# 14. Execution

The Tool executes within the defined scope.

---

# 15. Feedback

The agent may observe the resulting Resource state.

```text
Action
  ↓
Observation
  ↓
Context Update
  ↓
New Decision
```

---

# 16. Bounded Loop

An autonomous loop MUST have explicit limits.

Example:

```text
Maximum iterations: 5
Maximum duration: 60 seconds
Maximum pump adjustment: 10%
```

---

# 17. Escalation

If the agent cannot safely resolve the condition, it SHOULD escalate.

Example:

```text
Agent
  ↓
Unable to resolve
  ↓
Human Approval Required
```

---

# 18. Human Authority

A human operator MAY approve, deny or modify an autonomous operation according to policy.

---

# 19. Autonomous Failure

If the agent produces an invalid or unauthorized action:

```text
AUTHORIZATION_DENIED
```

The Tool MUST NOT execute.

---

# 20. Hallucinated Capability

If the agent proposes a Tool that does not exist or whose Contract does not support the requested operation, execution MUST fail safely.

---

# 21. Audit

Autonomous operations SHOULD record:

```text
agent identity
Context
Decision
Tool
Invocation
Result
```

---

# 22. Provenance

The final result SHOULD identify that the operation originated from an autonomous principal.

---

# 23. Emergency Stop

Critical autonomous systems SHOULD support an independent emergency stop mechanism.

The agent MUST NOT be able to disable its own emergency boundary.

---

# 24. Conformance

A conforming autonomous VIAL implementation MUST:

1. assign explicit identity to autonomous agents;
2. constrain their authority;
3. validate their Tool invocations;
4. enforce Resource scope;
5. bound autonomous loops;
6. support escalation;
7. preserve auditability;
8. prevent self-granted authority.

---

# 25. Final Principle

> **Autonomy is the ability to act within authority, not the ability to define authority.**

# End of EXAMPLES-005
