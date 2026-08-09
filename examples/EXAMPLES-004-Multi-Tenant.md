# EXAMPLES-004 — Multi-Tenant

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Example Specification
Depends On:
- EXAMPLES-001
- EXAMPLES-002
- EXAMPLES-003
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

This document demonstrates VIAL operating in a multi-tenant environment.

Domain-specific values in this example are illustrative and MUST NOT be interpreted as introducing new normative states, fields, identifiers or error codes.

The example shows how multiple independent Organizations can share infrastructure while maintaining strict isolation of identity, Resources, Context, authority, Tools and data.

---

# 2. Scenario

A VIAL service provider hosts multiple industrial customers.

```text
VIAL Platform
 ├── Tenant A
 ├── Tenant B
 └── Tenant C
```

Each tenant operates independently.

---

# 3. Tenant Model

Each tenant is represented by an Organization.

```text
Tenant A → ORG-001
Tenant B → ORG-002
Tenant C → ORG-003
```

A tenant MUST have a distinct Organization identity.

---

# 4. Isolation

Tenant isolation MUST apply to:

* Principals;
* Resources;
* Context;
* Decisions;
* Tools;
* Invocations;
* Results;
* Audit records;
* configuration;
* policies.

---

# 5. Principal

A principal belonging to Tenant A:

```text
principal.customer-a.operator
```

MUST NOT automatically obtain access to Tenant B.

---

# 6. Resource Isolation

Tenant A may own:

```text
RES-001
```

Tenant B may own:

```text
RES-002
```

Identical Resource names MUST NOT imply identical Resources.

---

# 7. Context Isolation

Context MUST contain sufficient tenant information to prevent ambiguity.

Example:

```text
organization: ORG-001
resource: RES-001
principal: principal.customer-a.operator
```

---

# 8. Tool Sharing

A Tool implementation MAY be shared across tenants.

Example:

```text
TOOL-001
```

The shared implementation does not imply shared Resource authority.

---

# 9. Tool Contract

The Contract remains identical where the capability is identical.

Tenant-specific authorization remains separate.

---

# 10. Registry

The Registry MAY be:

```text
Shared
Tenant-scoped
Federated
```

Regardless of physical implementation, tenant boundaries MUST remain explicit.

---

# 11. Discovery

A tenant discovery request MUST return only Tools and Resources visible to that tenant.

---

# 12. Invocation

An invocation MUST contain the tenant context.

```text
Invocation:
    tenant: ORG-001
    principal: principal.customer-a.operator
    tool: TOOL-001
    resource: RES-001
```

---

# 13. Cross-Tenant Access

Cross-tenant access MUST NOT occur implicitly.

If supported, it MUST require explicit authority from the relevant Organizations.

---

# 14. Authorization

Authorization MUST evaluate tenant membership before Resource and Tool permissions.

```text
Tenant
 ↓
Principal
 ↓
Resource
 ↓
Tool
 ↓
Operation
```

---

# 15. Data Isolation

A Tool MUST NOT expose data belonging to another tenant.

---

# 16. Audit Isolation

Audit records MUST preserve tenant boundaries.

Tenant A administrators MUST NOT automatically access Tenant B audit data.

---

# 17. Shared Infrastructure

The physical infrastructure MAY be shared.

Logical authority MUST remain isolated.

```text
Shared Runtime
     │
 ┌───┼───┐
 A   B   C
 │   │   │
isolated logical domains
```

---

# 18. Resource Quotas

The platform MAY impose tenant-specific limits:

```text
CPU
Memory
Storage
Tool invocations
Network
Concurrency
```

---

# 19. Rate Limiting

Rate limits MAY be applied independently per tenant.

---

# 20. Tenant Lifecycle

A tenant MAY follow the canonical Organization Lifecycle (SDK-002 §10):

```text
CREATED
   ↓
ACTIVE
   ↓
DEGRADED
   ↓
SUSPENDED
   ↓
ARCHIVED
```

Tenant lifecycle MUST affect access to its Resources and Tools.

---

# 21. Tenant Suspension

Suspending a tenant SHOULD prevent new operations while preserving historical audit information.

---

# 22. Security Boundary

Tenant identity MUST be part of the security context.

A missing or ambiguous tenant identity MUST cause the operation to fail safely.

---

# 23. Example Flow

```text
Tenant A User
      ↓
Tenant A Context
      ↓
Tenant A Authorization
      ↓
Shared Tool
      ↓
Tenant A Resource
      ↓
Tenant A Result
      ↓
Tenant A Audit
```

---

# 24. Failure Example

If Tenant A attempts to access Tenant B:

```text
ACCESS_DENIED
```

The Runtime MUST NOT silently redirect the request to another Resource.

---

# 25. Conformance

A conforming multi-tenant deployment MUST:

1. isolate tenant identity;
2. isolate Resources;
3. isolate Context;
4. enforce tenant-aware authorization;
5. isolate audit data;
6. prevent implicit cross-tenant access;
7. support shared infrastructure without shared authority.

---

# 26. Final Principle

> **Shared infrastructure does not imply shared authority.**

# End of EXAMPLES-004
