# VIAL Platform
# Request for Comments

---

Document ID: RFC-008

Title: Cognitive Reuse Hypothesis & Validation Protocol

Version: 1.0.0-draft.1

Status: Draft

Category: Technical Specification

Dependencies:

- ADR-0001 VIAL is a Distributed Cognitive Architecture
- ADR-0002 Adoption of Distributed Organizational Cognition
- RFC-003 Organizational State Model
- RFC-004 Context & Cognitive Efficiency
- RFC-007 Selective Context Hypothesis & Validation Protocol

---

## Abstract

This document converts the VIAL **Cognitive Reuse** principle (README §13; RFC-004 §23–27) into a **falsifiable hypothesis** with a **reproducible validation protocol**, following the same discipline established by RFC-007.

VIAL claims that previously validated cognition can be reused for equivalent future operations — instead of being reconstructed — without degrading correctness, provided the relevant underlying State has not changed.

This RFC does NOT assert that the claim is true. It defines what would have to be observed to accept it, and how to reproduce the measurement.

The companion artifact is the reference benchmark in `benchmark/cognitive-reuse/`.

---

## 1. Context

RFC-004 establishes the reuse model:

> Previously validated results SHOULD be reusable when their validity remains applicable.

It also defines the **Deterministic First** hierarchy (§23): reuse an existing validated result before performing any reasoning. And it defines **cache invalidation** (§27): cached cognition must be invalidated when relevant State, Policy, Evidence or Knowledge changes.

RFC-004 is normative theory. It does not demonstrate that reuse produces the claimed benefit, nor that invalidation protects correctness.

RFC-008 fills that gap by defining:

- the precise claims (H1, H2, H3);
- operational definitions;
- the measurement protocol;
- acceptance and rejection criteria;
- required artifacts.

---

## 2. Specification

### 2.1 Falsifiable Hypotheses

**H1 (Reuse Reduces Cost):**

> For a workload W containing repeated equivalent operations, executing under a Reuse Engine consumes materially less cognitive cost than executing every operation from scratch, with equal correctness.

**H2 (Reuse Preserves Correctness):**

> Reusing a cached result is no less correct than recomputing it, for operations whose relevant State is unchanged.

**H3 (Invalidation Protects Correctness):**

> When relevant State changes, the Reuse Engine invalidates the affected cached results and does NOT reuse stale cognition, so correctness is preserved.

**H0 (Null):** at least one of H1, H2 or H3 fails for workload W.

The hypotheses are accepted ONLY if all three hold simultaneously:

| Hypothesis | Criterion |
|-----------|-----------|
| H1 | `cost(no_reuse) / cost(reuse) >= 2.0` |
| H2 | `quality(reuse) >= quality(no_reuse) * (1 - quality_tolerance)` |
| H3 | `stale_reuse_count == 0` |

where `quality_tolerance` defaults to `0.10`.

### 2.2 Operational Definitions

**Equivalent operations:** two operations whose Reuse Signature (§2.3) is identical.

**Reuse Signature:** a deterministic key derived from the operation semantics — the operation type plus its parameters, excluding state values. Two operations with the same signature ask the same question; whether the answer is reusable depends on State compatibility.

**State compatibility:** an operation is reusable iff the State fields referenced by its original projection have the same values now as when the result was validated. Fields NOT referenced by the operation MAY change without invalidating its result (RFC-004 §25 "State compatibility").

**Stale reuse:** serving a cached result whose referenced State fields have changed since validation. Stale reuse is a correctness violation.

**Cognitive cost:** the primary metric is token count of the context delivered to the executor, summed over all operations. A cache hit is a deterministic lookup with no executor invocation and counts as 0 tokens.

**Quality:** same evaluator as RFC-007 §2.2, applied to both conditions.

### 2.3 Reuse Engine Behavior

A conforming Reuse Engine MUST:

1. compute the Reuse Signature of each operation;
2. on an operation, check for a cached result with matching signature;
3. verify State compatibility (§2.2) before serving the cached result;
4. if compatible, serve the cached result WITHOUT invoking the executor;
5. if incompatible, invalidate the cached entry and recompute;
6. store newly validated results with their State references and State version.

### 2.4 Metrics

Per condition (no_reuse vs reuse), over all operations:

| Metric | Definition |
|--------|------------|
| total_cost | sum of executor-invocation context tokens |
| reuse_hits | operations served from cache |
| recomputes | operations that invoked the executor |
| stale_reuse | cache hits served despite incompatible State (MUST be 0) |
| reuse_rate | reuse_hits / total_operations |
| mean_quality | mean per-operation quality |

Cross-condition:

| Metric | Definition |
|--------|------------|
| cost_ratio | total_cost(no_reuse) / total_cost(reuse) |
| quality_delta | mean_quality(reuse) - mean_quality(no_reuse) |

### 2.5 Acceptance Criteria

H1 supported when `cost_ratio >= cost_ratio_threshold` (default 2.0).
H2 supported when `mean_quality(reuse) >= mean_quality(no_reuse) * (1 - quality_tolerance)`.
H3 supported when `stale_reuse == 0`.

All three MUST hold for the RFC-008 hypotheses to be supported. Any failure is a valid negative result and MUST be reported.

### 2.6 Required Artifacts

Every validation run MUST produce:

1. workload declaration (immutable, including the State-change schedule);
2. per-operation results for both conditions;
3. summary metrics;
4. environment description;
5. the exact reproduction command.

### 2.7 Reproducibility Rules

- Workloads MUST be deterministic (seeded).
- The State-change schedule is part of the workload and MUST be identical across conditions.
- Both conditions MUST consume the same ordered operation stream.

---

## 3. Conformance Requirements

- [ ] MUST define workload W before execution (RFC-008 §2.6).
- [ ] MUST consume the same ordered operation stream in both conditions (RFC-008 §2.7).
- [ ] MUST verify State compatibility before serving cached results (RFC-008 §2.3).
- [ ] MUST count stale_reuse and report it (RFC-008 §2.4).
- [ ] MUST compute cost_ratio, reuse_rate and quality_delta (RFC-008 §2.4).
- [ ] MUST apply acceptance criteria from §2.5.
- [ ] MUST report negative results without omission (RFC-008 §2.5).
- [ ] MUST seed all randomization (RFC-008 §2.7).

---

## 4. Examples

### 4.1 Minimal Reuse Sequence

State: `pressure = 8.2` (relevance: `[pressure, control]`).

Operation stream:

```text
1. T1 "Is pressure within [4,10]?"  → execute, store, answer TRUE
2. T2 "Is pressure within [4,10]?"  → cache hit (State unchanged), answer TRUE
3. State transition: pressure = 12.0
4. T3 "Is pressure within [4,10]?"  → invalidated (State changed), execute, answer FALSE
```

- reuse_hits = 1, recomputes = 2, stale_reuse = 0
- total_cost(reuse) = cost(T1) + cost(T3) = cost(T2 excluded)
- total_cost(no_reuse) = cost(T1) + cost(T2) + cost(T3)

### 4.2 Expected Observable (illustrative, not a claim)

```text
condition   total_cost   mean_quality   stale_reuse
no_reuse    3000         1.0            -
reuse       2000         1.0            0

cost_ratio = 1.5 < 2.0 → H1 NOT supported (illustration only)
```

This illustration is NOT a result. Results come only from actual runs.

---

## 5. Security Considerations

- Cache hits bypass the executor; therefore State compatibility MUST be verified (RFC-004 §27). A buggy compatibility check is a correctness and security risk.
- Cached results MUST retain provenance references to the validated State version.
- Cache admission MUST respect authorization: an operation must not serve a result beyond the caller's authority scope.

---

## 6. Alternatives

| Alternative | Considered because | Rejected because |
|-------------|-------------------|------------------|
| Reuse without State check | Simpler, faster | Violates RFC-004 §27; stale results are correctness failures |
| Reuse by semantic similarity only | More general | RFC-004 §25: similarity alone MUST NOT be sufficient |
| No reuse at all | Simplest | Ignores RFC-004 §23; leaves repeated reasoning on the table |
| Key by prompt hash | Simple | Fragile; equivalent ops with different wording would miss |

---

## 7. References

- ADR-0000 Governance
- ADR-0001 VIAL is a Distributed Cognitive Architecture
- RFC-003 Organizational State Model (§23, §24, §25)
- RFC-004 Context & Cognitive Efficiency (§23, §24, §25, §26, §27, §54)
- RFC-007 Selective Context Hypothesis & Validation Protocol
- README §13 Reason Once, Reuse Many Times
- benchmark/README.md Benchmark Principles

---

## 8. Backward Compatibility

This RFC introduces no changes to existing specifications. It defines a validation protocol and a reference artifact, consistent with RFC-007.

---

End of Document
