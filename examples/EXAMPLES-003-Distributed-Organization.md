# EXAMPLES-003 — Distributed

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Example Specification
Depends On:
- EXAMPLES-001
- EXAMPLES-002
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

This document demonstrates VIAL operating across distributed environments.

Domain-specific values in this example are illustrative and MUST NOT be interpreted as introducing new normative states, fields, identifiers or error codes.

The example introduces multiple administrative and execution domains while preserving identity, authority, Context and Tool governance.

---

# 2. Scenario

A company operates multiple industrial facilities.

```text
Organization
 ├── Plant A
 ├── Plant B
 └── Central Operations
```

Each plant has local Resources and Runtime capabilities.

---

# 3. Organization Structure

```text
Organization:
    ORG-001

Units:
    plant-a
    plant-b
    central-operations
```

The Organization remains the top-level authority boundary.

---

# 4. Distributed Resources

Plant A:

```text
RES-001
RES-002
```

Plant B:

```text
RES-003
RES-004
```

---

# 5. Runtime Domains

Each plant may operate a local Runtime:

```text
Central Runtime
       │
 ┌─────┴─────┐
 │           │
Runtime A  Runtime B
 │           │
Plant A    Plant B
```

---

# 6. Local Authority

Each Runtime enforces local operational policies.

A local Runtime MUST NOT assume that a remote caller has unrestricted local authority.

---

# 7. Distributed Principal

A principal may originate from Central Operations:

```text
principal.central.engineer
```

and request access to a Resource in Plant A.

The request crosses an administrative/runtime boundary.

---

# 8. Context Propagation

The relevant Context may include:

```text
organization
plant
principal
resource
operation
decision
security_context
```

Context propagation MUST preserve authority boundaries.

---

# 9. Decision

Central Operations may issue a Decision:

```text
Decision:
    id: DEC-001
    objective: inspect pasteurizer state
    target: plant-a
```

The Decision expresses intent but does not automatically grant local execution authority.

---

# 10. Local Authorization

Plant A evaluates the incoming request.

```text
Central Identity
       +
Organization Policy
       +
Plant Policy
       +
Resource Policy
       +
Tool Policy
       ↓
Authorization
```

---

# 11. Tool Discovery

The central system may discover that Plant A exposes:

```text
TOOL-001
```

The local Registry remains authoritative for the local Tool instance.

---

# 12. Remote Invocation

The request may travel:

```text
Central Runtime
      ↓
Remote Invocation
      ↓
Plant A Runtime
      ↓
Local Tool
      ↓
Resource
```

---

# 13. Invocation Identity

The distributed operation SHOULD maintain correlation between:

```text
Central Invocation ID
Local Invocation ID
```

Example:

```text
central_invocation:
    INV-001

local_invocation:
    INV-002
```

---

# 14. Authority Boundary

The local Runtime MUST independently verify authorization.

A remote invocation MUST NOT bypass local policy.

---

# 15. Network Failure

If Plant A becomes unavailable:

```text
Central Runtime
      ↓
Plant A unavailable
```

The system MUST return an explicit failure.

Example:

```text
RESOURCE_UNAVAILABLE
```

It MUST NOT fabricate the Resource state.

---

# 16. Timeout

Remote invocation SHOULD have bounded timeouts.

---

# 17. Retry

Retries MUST respect:

* idempotency;
* Tool Contract;
* Resource state;
* side effects;
* authorization.

---

# 18. Distributed Side Effects

For consequential Tools, automatic retry MUST NOT create unintended duplicate operations.

---

# 19. Data Locality

A Resource MAY remain entirely inside its local domain.

The central Runtime may receive only the permitted result.

---

# 20. Security

Remote Tools SHOULD use authenticated and authorized communication.

Credentials MUST NOT be exposed through Context or Tool results.

---

# 21. Trust Boundaries

The architecture contains explicit trust boundaries:

```text
Central Domain
      │
      │ trust boundary
      ▼
Plant A Domain
```

Each boundary requires validation.

---

# 22. Tool Registry

The system MAY maintain:

```text
Central Registry
Local Registries
```

Local registries remain authoritative for local Tools.

---

# 23. Discovery Federation

A central Discovery mechanism MAY federate local Tool information.

Federation MUST preserve:

* Tool identity;
* version;
* lifecycle;
* security metadata;
* ownership.

---

# 24. Distributed Lifecycle

A Tool may be:

```text
ACTIVE in Plant A
DEPRECATED in Plant B
```

Lifecycle state is therefore domain-aware when deployments differ.

---

# 25. Distributed Context

Context MUST identify the relevant domain.

Example:

```text
organization: ORG-001
plant: plant-a
resource: pasteurizer-01
```

This prevents ambiguous Resource references.

---

# 26. Distributed Audit

A distributed operation SHOULD produce correlated audit records.

```text
Central Audit
      │
      └── INV-001
              │
              └── INV-002
```

---

# 27. Provenance

The final result SHOULD identify:

```text
Origin
Runtime
Tool
Version
Resource
Invocation
Timestamp
```

---

# 28. Partial Failure

A distributed workflow may partially succeed.

The system MUST distinguish:

```text
SUCCESS
PARTIAL_SUCCESS
FAILED
UNKNOWN
```

---

# 29. Unknown State

If the remote system cannot confirm execution outcome, the result SHOULD be:

```text
UNKNOWN
```

rather than incorrectly reporting failure or success.

---

# 30. Recovery

Recovery mechanisms MAY reconcile state after communication failure.

Reconciliation MUST use authoritative Resource state.

---

# 31. Distributed Tool Chaining

A workflow may involve:

```text
Plant A Sensor
      ↓
Central Decision
      ↓
Plant B Tool
```

Each operation crosses explicit authority boundaries.

---

# 32. Security Principle

Central authority MUST NOT automatically imply local operational authority.

---

# 33. Scalability

The architecture MAY scale to:

```text
1 Organization
    ↓
N Plants
    ↓
N Runtimes
    ↓
N Resources
    ↓
N Tools
```

The governance model remains unchanged.

---

# 34. Example Architecture

```text
                         Organization
                              │
                    Central Operations
                              │
                         Central Runtime
                       ┌──────┴──────┐
                       │             │
                 Plant A Runtime  Plant B Runtime
                       │             │
                  ┌────┴────┐   ┌────┴────┐
                  │         │   │         │
               Tools    Resources      Tools
```

---

# 35. What This Example Demonstrates

This example demonstrates:

* distributed Runtime domains;
* local authority;
* remote invocation;
* federated discovery;
* Context propagation;
* distributed Decisions;
* trust boundaries;
* network failure;
* timeout and retry;
* partial failure;
* correlated audit;
* provenance;
* Resource locality.

---

# 36. Conformance

A distributed VIAL implementation SHOULD be capable of maintaining governance when Tools, Resources and Runtime components are separated across network boundaries.

---

# 37. Final Principle

> **Distribution changes where execution occurs; it must not change the fundamental rules of identity, authority, security, provenance and governance.**

# End of EXAMPLES-003
