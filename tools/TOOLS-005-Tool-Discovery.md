# TOOLS-005 — Tool Discovery

**Project:** VIAL
**Version:** 1.0.0
**Status:** Draft
**Category:** Tools Specification
Depends On:
- TOOLS-001
- TOOLS-002
- TOOLS-003
- TOOLS-004
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

This document defines how Tools are discovered within VIAL.

Discovery allows a caller to identify available capabilities without relying on implementation-specific knowledge.

The fundamental principle is:

> **Discovery exposes capabilities; it does not grant authority to execute them.**

---

# 2. Purpose

Tool Discovery provides:

* capability search;
* Tool identification;
* Contract retrieval;
* version information;
* security metadata;
* lifecycle visibility;
* compatibility information.

---

# 3. Discovery Model

```text
Caller
  │
  ▼
Discovery
  │
  ▼
Registry
  │
  ▼
Tool Metadata
  │
  ▼
Contract
```

---

# 4. Discovery Request

A discovery request MAY specify:

```text
capability
tool_id
version
organization
resource_type
risk_level
status
```

---

# 5. Discovery Result

A discovery result SHOULD include:

```text
tool_id
name
description
version
contract_version
capability
side_effects
risk
lifecycle
required_permissions
```

---

# 6. Capability-Based Discovery

Callers SHOULD be able to search by capability rather than knowing the Tool ID beforehand.

Example:

```text
"read current equipment temperature"
```

may resolve to:

```text
tool.sensor.read_temperature
```

---

# 7. Semantic Discovery

A discovery mechanism MAY support semantic matching.

Semantic matching MUST NOT be treated as proof of capability equivalence.

The final Contract remains authoritative.

---

# 8. Exact Discovery

Exact Tool ID and version lookup SHOULD be supported.

Example:

```text
tool.pump.set_speed@1.0.0
```

---

# 9. Security-Aware Discovery

Discovery SHOULD respect the caller's visibility permissions.

A caller MAY be prevented from discovering restricted Tools.

---

# 10. Discovery vs Authorization

Discovery does not authorize invocation.

```text
DISCOVERED ≠ AUTHORIZED
```

A discovered Tool MUST still pass authorization during invocation.

---

# 11. Contract Retrieval

Discovery SHOULD provide access to the authoritative Tool Contract.

---

# 12. Version Discovery

Discovery SHOULD identify compatible versions.

The caller SHOULD be able to distinguish:

```text
ACTIVE
DEPRECATED
RETIRED
```

versions.

---

# 13. Compatibility

Discovery MAY filter Tools according to Contract compatibility.

---

# 14. Resource-Aware Discovery

Discovery MAY consider Resource type.

Example:

```text
Resource:
Pump

Capability:
Set speed
```

Only Tools compatible with the Resource SHOULD be returned as preferred candidates.

---

# 15. Context-Aware Discovery

Discovery MAY use Context to refine candidate selection.

Context MUST NOT override authorization.

---

# 16. Decision-Aware Discovery

A Decision MAY provide the intended capability or operation.

Discovery can use this information to identify candidate Tools.

---

# 17. Ranking

Discovery MAY rank candidates.

Ranking MAY consider:

```text
Capability match
Contract compatibility
Version
Availability
Risk
Latency
Cost
Organization
Resource compatibility
```

Ranking MUST NOT change security requirements.

---

# 18. Discovery Result Confidence

Semantic discovery MAY provide a confidence or relevance score.

The score MUST NOT be interpreted as authorization or execution permission.

---

# 19. Hidden Tools

Tools MAY be intentionally undiscoverable.

An undiscoverable Tool remains subject to the same security requirements.

---

# 20. Discovery Metadata

Recommended metadata:

```text
tool_id
description
capability
version
contract
risk
side_effects
owner
status
```

---

# 21. Discovery Freshness

Discovery results SHOULD identify freshness where Tool state changes frequently.

---

# 22. Stale Discovery

A caller MUST revalidate critical Tool information before consequential execution when discovery data may be stale.

---

# 23. Discovery Cache

Discovery results MAY be cached.

Caches MUST respect lifecycle and authorization changes.

---

# 24. Registry Dependency

Discovery SHOULD use the authoritative Registry rather than independently maintained Tool lists.

---

# 25. Discovery Audit

Security-sensitive discovery MAY be audited.

Audit information SHOULD include:

```text
caller
query
timestamp
result
```

---

# 26. Discovery Security

Discovery MUST NOT reveal:

* credentials;
* private configuration;
* secrets;
* restricted implementation details.

---

# 27. Discovery Failure

Discovery failures MUST be explicit.

Examples:

```text
REGISTRY_UNAVAILABLE
INVALID_QUERY
NOT_FOUND
ACCESS_DENIED
```

---

# 28. No Capability Fabrication

Discovery MUST NOT claim that a Tool supports a capability not declared by its Contract.

---

# 29. Contract Authority

When metadata conflicts with the Contract, the Contract is authoritative for Tool behavior.

---

# 30. Conformance

A conforming Discovery mechanism MUST:

1. identify Tools accurately;
2. expose authoritative Contracts;
3. respect lifecycle state;
4. respect discovery security;
5. distinguish discovery from authorization;
6. support deterministic identification;
7. avoid capability fabrication.

---

# 31. Final Principle

> **Discovery answers "what capabilities are available?" It does not answer "what am I authorized to execute?"**

# End of TOOLS-005
