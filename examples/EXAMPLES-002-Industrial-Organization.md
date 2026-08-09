# EXAMPLES-002 — Industrial

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Example Specification
Depends On:
- EXAMPLES-001
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

This document demonstrates VIAL in an industrial environment.

Domain-specific values in this example are illustrative and MUST NOT be interpreted as introducing new normative states, fields, identifiers or error codes.

The example expands the Minimal Organization scenario to include multiple Resources, Tools, operational Context and consequential Decisions.

---

# 2. Scenario

A manufacturing plant operates a pasteurization system.

The system contains:

```text
Pasteurizer
 ├── Temperature Sensor
 ├── Pressure Sensor
 ├── Pump
 ├── Valve
 └── Water Circuit
```

VIAL provides governed access to these Resources.

---

# 3. Organization

```text
Organization:
    id: ORG-001
    name: Example Industrial Plant
```

The Organization represents the operational authority boundary.

---

# 4. Resources

Resources include:

```text
RES-001
RES-002
RES-003
RES-004
RES-005
```

Resources may have relationships.

Example:

```text
Pasteurizer
    ├── Temperature Sensor
    ├── Pressure Sensor
    ├── Pump
    └── Valve
```

---

# 5. Principals

The plant contains multiple principals:

```text
operator
maintenance
engineer
administrator
```

Their permissions are not equivalent.

---

# 6. Tools

Example Tools:

```text
TOOL-001
TOOL-002
TOOL-003
TOOL-004
TOOL-005
TOOL-006
```

Read-only Tools generally have lower operational risk than control Tools.

---

# 7. Tool Security

A Tool such as:

```text
TOOL-004
```

has side effects.

Its Contract therefore defines stricter requirements.

Example:

```text
Risk:
    HIGH

Side Effects:
    changes pump operating state

Required Authority:
    maintenance or authorized operator
```

---

# 8. Context

An industrial operation may require additional Context:

```text
plant
line
equipment
recipe
production_order
current_state
operator
maintenance_state
```

Example:

```text
Context:
    plant: plant-01
    line: line-02
    equipment: pasteurizer-01
    recipe: recipe-A
    production_order: order-2026-001
```

---

# 9. Decision

Suppose the pasteurizer pressure is outside the operational range.

A Decision may determine that pump speed must be adjusted.

```text
Decision:
    id: DEC-001
    objective: restore operating pressure
    resource: RES-004
```

The Decision expresses intent; it does not by itself grant permission to act.

---

# 10. Authority

The Decision does not itself bypass authorization.

The Runtime verifies:

```text
Principal
+
Organization
+
Resource
+
Tool
+
Decision
+
Policy
```

---

# 11. Discovery

The Runtime can discover suitable Tools.

Example:

```text
Required capability:
    adjust pump speed

Discovery:
    TOOL-004
```

---

# 12. Invocation

The invocation specifies:

```text
Tool:
    TOOL-004

Resource:
    RES-004

Input:
    speed = 65%
```

---

# 13. Preconditions

Before execution, the Runtime may verify:

```text
Pump available
Emergency stop inactive
Operator authorized
Pressure within safe transition range
Tool active
Required approval present
```

---

# 14. Execution

The Tool executes the requested operation.

The Runtime maintains the Invocation state.

```text
REQUESTED
    ↓
VALIDATING
    ↓
AUTHORIZED
    ↓
EXECUTING
    ↓
SUCCEEDED
```

---

# 15. Postcondition

The system may verify:

```text
pump.speed == 65%
```

and:

```text
pressure within expected operating range
```

---

# 16. Audit

The complete operation is recorded:

```text
Decision
Invocation
Principal
Tool
Resource
Input
Result
Timestamp
```

---

# 17. Failure Scenario

If the pump refuses the command:

```text
Execution
    ↓
FAILED
```

The Runtime MUST NOT report success.

The failure may be:

```text
RESOURCE_UNAVAILABLE
```

or:

```text
EXECUTION_FAILURE
```

---

# 18. Safety Boundary

A Tool MUST NOT use a general authorization to bypass equipment-specific safety constraints.

For example:

```text
Operator authorized
```

does not imply:

```text
Operator authorized to ignore safety interlocks
```

---

# 19. Multiple Tools

A more complex operation may involve:

```text
Read pressure
      ↓
Read temperature
      ↓
Decision
      ↓
Adjust pump
      ↓
Read pressure again
```

Each consequential Tool operation remains independently governed.

---

# 20. Tool Chaining

If Tool A invokes Tool B, Tool B receives its own Invocation identity and authorization evaluation.

---

# 21. Industrial Observability

The system SHOULD expose:

```text
equipment state
tool status
invocation state
execution latency
failure state
decision history
```

---

# 22. Industrial Security

High-risk operations SHOULD use stronger:

* authorization;
* approval;
* audit;
* isolation;
* monitoring.

---

# 23. Example Architecture

```text
                    Organization
                         │
              ┌──────────┴──────────┐
              │                     │
          Principals            Policies
              │
              ▼
           Runtime
              │
        ┌─────┴─────┐
        │           │
     Context     Decision
        │           │
        └─────┬─────┘
              │
           Discovery
              │
            Tools
              │
        ┌─────┼─────┐
        │     │     │
      Pump  Valve  Sensors
        │     │     │
        └─────┴─────┘
            Resources
```

---

# 24. What This Example Demonstrates

This scenario demonstrates:

* multiple Resources;
* multiple Tools;
* operational Context;
* consequential Decisions;
* Tool security;
* preconditions;
* postconditions;
* Tool chaining;
* audit;
* industrial safety boundaries.

---

# 25. Final Principle

> **Industrial VIAL deployments demonstrate that capability, authority, safety and execution must remain separate but coordinated.**

# End of EXAMPLES-002
