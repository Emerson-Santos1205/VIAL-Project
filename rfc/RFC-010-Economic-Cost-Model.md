# VIAL Platform
# Request for Comments

---

Document ID: RFC-010

Title: Economic Cost Model & Validation Protocol

Version: 1.0.0-draft.1

Status: Draft

Category: Technical Specification

Depends On:
- ADR-0001
- ADR-0002
- RFC-004
- RFC-007
- RFC-008
---

## Abstract

This document converts the VIAL **Economic Objective** (README §7, §27; RFC-004 §21, §22, §23) into a **falsifiable hypothesis** with a **reproducible validation protocol**.

VIAL claims that efficiency is not merely "fewer tokens": the objective is minimum necessary total cognitive cost while preserving correctness. Total cost includes inference, tokens, latency, retrieval, construction, validation, coordination and retries.

RFC-007 measured token cost. RFC-010 extends measurement to total cost and tests the strongest consequence: **token-optimal execution is not always total-cost-optimal**, so optimizing tokens alone can be economically wrong.

The companion artifact is the reference benchmark in `benchmark/economic-cost/`.

---

## 1. Context

README §7 states:

> A system that saves tokens but produces worse organizational outcomes is not necessarily more efficient.

RFC-004 §21 defines Cognitive Cost as a composite of token cost, inference cost, latency, network traffic, memory retrieval, validation cost, coordination cost and retry cost. §22 requires cost-aware resource selection; §23 defines the **Deterministic First** hierarchy: prefer existing validated results, then deterministic rules, then lightweight reasoning, then advanced reasoning.

RFC-004 is normative theory. It does not demonstrate that token-optimal execution can diverge from total-cost-optimal execution, nor that a cost-aware selector captures the divergence.

RFC-010 fills that gap.

---

## 2. Specification

### 2.1 Falsifiable Hypothesis

**H1 (Token vs Total Cost Divergence):**

> There exist economically plausible workloads and price configurations where the token-optimal execution policy is NOT the total-cost-optimal policy. Optimizing tokens alone is therefore insufficient for VIAL's economic objective.

**H2 (Deterministic First Reduces Total Cost):**

> For a workload with a mix of deterministic and reasoning-required operations, a selector following RFC-004 §23 (Deterministic First) achieves equal quality at lower or equal total cost than a policy that reasons about every operation.

**H0 (Null):** no such configuration exists (H1 false), or Deterministic First does not reduce total cost (H2 false).

### 2.2 Operational Definitions

**Token cost:** the token count of the context delivered to the executor (RFC-007 metric).

When cost is evaluated for a consequential Decision or execution boundary, RFC-010 consumes the canonical Context model from RFC-002 through RFC-004: `CREATED → VALID → FROZEN → CONSUMED → ARCHIVED`. Once the relevant Context is FROZEN, its normative content MUST NOT change during that evaluation.

**Inference cost:** the monetary cost of model execution, derived from input/output tokens and per-token prices.

**Latency cost:** elapsed execution time, weighted by a configurable cost-per-unit-time.

**Retrieval cost:** cost per retrieval operation performed by the Context Builder.

**Construction cost:** cost per context assembly (RFC-004 §39: context construction itself has cost).

**Validation cost:** cost per correctness validation performed.

**Total cost:** the weighted sum of token, inference, latency, retrieval, construction and validation costs, using the workload's declared price table. All weights are declared in the workload and fixed before execution.

**Cost-optimal policy:** the execution policy minimizing total cost.

**Token-optimal policy:** the execution policy minimizing token cost.

### 2.3 Price Table

Each workload declares a price table:

```text
tokens:         cost per 1k tokens
inference:      cost per 1k input tokens / per 1k output tokens
latency:        cost per second
retrieval:      cost per retrieval operation
construction:   cost per context assembly
validation:     cost per validation
```

The table is part of the workload (RFC-010 §2.7) and MUST NOT change during a run.

### 2.4 Deterministic First Selector

A conforming selector MUST:

1. determine whether the operation can be satisfied deterministically (RFC-004 §23);
2. if yes, use the deterministic path (no reasoning, no inference cost);
3. if no, use the cheapest reasoning tier capable of the operation;
4. never choose a more expensive capable tier when a cheaper capable tier exists.

### 2.5 Metrics

| Metric | Definition |
|--------|------------|
| total_cost(policy) | weighted total cost of the policy over the workload |
| token_cost(policy) | token component of cost |
| inference_cost(policy) | inference component of cost |
| divergence_exists | argmin over policies of total_cost differs from argmin over policies of token_cost |
| mean_quality(policy) | quality under the policy |

### 2.6 Acceptance Criteria

H1 supported when `divergence_exists == True`.
H2 supported when `total_cost(deterministic_first) <= total_cost(reason_everything)` AND `mean_quality(deterministic_first) >= mean_quality(reason_everything) * (1 - quality_tolerance)`.

Both MUST hold for RFC-010 to be supported. Any failure is a valid negative result and MUST be reported.

### 2.7 Required Artifacts

Every validation run MUST produce:

1. workload declaration (operation stream + price table);
2. per-policy cost breakdown;
3. summary metrics;
4. environment description;
5. the exact reproduction command.

### 2.8 Reproducibility Rules

- Price tables MUST be declared in the workload, not inferred.
- Policy evaluation MUST consume the same operation stream.
- Randomness MUST be seeded.

---

## 3. Conformance Requirements

- [ ] MUST declare a price table before execution (RFC-010 §2.7).
- [ ] MUST evaluate every policy on the same operation stream (RFC-010 §2.8).
- [ ] MUST compute total_cost and token_cost per policy (RFC-010 §2.5).
- [ ] MUST determine divergence_exists (RFC-010 §2.5).
- [ ] MUST apply acceptance criteria from §2.6.
- [ ] MUST report negative results without omission (RFC-010 §2.6).

---

## 4. Examples

### 4.1 Illustrative Divergence

```text
Tier A: token cost 100, inference cost 2 (cheap model, verbose)
Tier B: token cost 60,  inference cost 9 (expensive model, terse)

token-optimal  → B (60 < 100)
total-cost-optimal → A (2 < 9, assuming same latency/retrieval)
→ divergence_exists = True
```

This illustration is NOT a result. Results come only from actual runs.

---

## 5. Security Considerations

- The price table is configuration; a tampered table invalidates results and MUST be versioned with the workload.
- Cost optimization MUST NOT override mandatory safety, authorization or correctness requirements (RFC-004 §55: Safety > Authority > Reliability > Efficiency).
- Divergence findings MUST NOT be used to justify skipping validation.
- This RFC consumes the canonical authority model from RFC-006. Authorization remains distinct from Decision, Approval, Invocation and Execution; economic selection logic MUST NOT redefine those concepts.
- Review, escalation or revocation triggered by economic policy MUST be treated as events or governance processes, not as Decision lifecycle states.

---

## 6. Alternatives

| Alternative | Considered because | Rejected because |
|-------------|-------------------|------------------|
| Tokens as the only cost | Simple | README §7 explicitly rejects token-only efficiency |
| Monetary cost only | Realistic | Ignores latency/retrieval/construction; VIAL defines total cost broadly |
| Fixed global weights | Deterministic | A single weight set cannot demonstrate divergence honestly |

---

## 7. References

- ADR-0000 Governance
- ADR-0001 VIAL is a Distributed Cognitive Architecture
- README §7 Efficiency Philosophy, §27 Economic Objective
- RFC-004 Context & Cognitive Efficiency (§21, §22, §23, §55)
- RFC-007 Selective Context Hypothesis & Validation Protocol
- benchmark/README.md Benchmark Principles

---

## 8. Backward Compatibility

This RFC introduces no changes to existing specifications. It defines a cost model and validation protocol layered on RFC-004, RFC-007 and RFC-008.

---

End of Document
