# VIAL Platform
# Request for Comments

---

Document ID: RFC-007

Title: Selective Context Hypothesis & Validation Protocol

Version: 1.0.0-draft.1

Status: Draft

Category: Technical Specification

Depends On:
- ADR-0001
- ADR-0002
- RFC-003
- RFC-004
---

## Abstract

This document converts the central VIAL efficiency thesis into a **falsifiable hypothesis** with a **reproducible validation protocol**.

VIAL claims that selective contextualization — sending each execution resource only the minimum sufficient projection of persistent State — reduces cognitive cost without materially degrading result quality, when compared to transmitting complete organizational context.

This RFC does NOT assert that the claim is true. It defines exactly what would have to be observed, measured and falsified for the claim to be accepted, and how to reproduce the measurement.

The companion artifact is the reference benchmark in `benchmark/selective-context/`.

---

## 1. Context

RFC-004 establishes the principle:

> Provide the smallest sufficient context capable of producing a valid result.

RFC-003 establishes the State model with selective projection and references.

Both documents are normative theory. They describe how VIAL *should* behave. Neither demonstrates that the behavior *produces the claimed benefit*.

RFC-007 fills that gap by defining:

- the precise claim (Hypothesis H1 and H0);
- the operational definitions of every term in the claim;
- the measurement protocol;
- the acceptance and rejection criteria;
- the required artifacts and reproducibility rules.

This is the minimal RFC required to move VIAL from specification theater to empirical validation.

---

## 2. Specification

### 2.1 Falsifiable Hypothesis

**H1 (Selective Context Hypothesis):**

> For a defined workload W, executing under Selective Context (Sc) produces a result with quality not materially worse than the same workload under Full Context (Fc), while consuming materially less cognitive cost.

**H0 (Null Hypothesis):**

> Selective Context either (a) materially degrades quality, or (b) does not materially reduce cost, for workload W.

The hypothesis is accepted ONLY if both conditions hold simultaneously:

| Condition | Criterion |
|-----------|-----------|
| Cost Reduction | `cost(Fc) / cost(Sc) >= 2.0` on the primary cost metric |
| Quality Parity | `quality(Sc) >= quality(Fc) * (1 - quality_tolerance)` |

where `quality_tolerance` defaults to `0.10` (10% relative degradation is the maximum permitted).

### 2.2 Operational Definitions

**Full Context (Fc):** the complete serialized representation of the Organization's persistent State available for the workload, passed verbatim to the execution resource for every task.

**Selective Context (Sc):** a projection constructed by selecting only the state fields, references and policies that the Context Builder determines relevant to the specific task, per the selection rules in §2.3.

When a workload evaluates a consequential Decision or execution boundary, the benchmark MUST consume the canonical Context model from RFC-002 through RFC-004: `CREATED → VALID → FROZEN → CONSUMED → ARCHIVED`. Once the benchmarked Context is FROZEN, its normative content MUST NOT change during that evaluation.

**Cognitive Cost:** the primary metric is token count of the serialized context delivered to the execution resource. Secondary metrics: bytes, retrieval operations, construction time.

**Quality:** for deterministic tasks, quality = exact-match correctness (0.0 or 1.0). For non-deterministic tasks, quality = an evaluator score in `[0.0, 1.0]` with a documented rubric. The same evaluator MUST be applied to both conditions.

**Materially worse:** quality degradation exceeding `quality_tolerance`.

**Materially reduced:** cost reduction meeting the `cost_ratio_threshold`.

### 2.3 Context Selection Rules (Sc)

The Context Builder MUST select for each task only:

1. the task definition itself;
2. state fields whose relevance descriptor matches the task's required fields;
3. references (not full bodies) to policy and knowledge artifacts, unless the task requires their body;
4. no historical records unless the task's relevance descriptor requests them.

Relevance is determined by a deterministic **relevance descriptor** attached to each state field at model time. This descriptor is part of the workload definition and MUST NOT change between conditions during a single run.

### 2.4 Workload Definition (W)

A workload is defined by:

- task list with relevance descriptors;
- Organization State fixture (a deterministic, versioned State);
- execution mode (deterministic or evaluator-based);
- seed for any randomization.

Workloads MUST be declared before execution and stored with the results.

### 2.5 Metrics

Per condition (Fc and Sc), over all tasks:

| Metric | Definition |
|--------|------------|
| total_cost | sum of per-task token counts |
| mean_cost | total_cost / n_tasks |
| mean_quality | mean per-task quality score |
| median_cost | median per-task token count |
| cost_ratio | cost(Fc) / cost(Sc) |
| quality_delta | quality(Sc) - quality(Fc) |

### 2.6 Acceptance Criteria

H1 is supported when, on the reported run:

- `cost_ratio >= cost_ratio_threshold` (default 2.0); AND
- `mean_quality(Sc) >= mean_quality(Fc) * (1 - quality_tolerance)`.

H0 is supported (hypothesis falsified) when EITHER:

- `cost_ratio < cost_ratio_threshold`; OR
- `mean_quality(Sc) < mean_quality(Fc) * (1 - quality_tolerance)`.

A run that falsifies H1 is a **valid negative result** and MUST be reported. Negative results are valid artifacts (benchmark/README.md, Principle 2).

### 2.7 Required Artifacts

Every validation run MUST produce:

1. workload declaration (immutable);
2. raw per-task results (cost + quality for both conditions);
3. summary metrics;
4. environment description (executor, tokenizer, Python version);
5. the exact command used to reproduce.

### 2.8 Reproducibility Rules

- Deterministic workloads MUST produce identical results across runs with the same seed.
- Randomness MUST be seeded.
- The workload fixture MUST be versioned.
- Results MUST be stored under `benchmark/selective-context/results/<run-id>/`.
- A run without its workload declaration is invalid.

---

## 3. Conformance Requirements

- [ ] MUST define a workload W before execution (RFC-007 §2.4).
- [ ] MUST execute each task under both Fc and Sc conditions (RFC-007 §2.2).
- [ ] MUST use the same evaluator for both conditions (RFC-007 §2.2).
- [ ] MUST compute cost_ratio and quality_delta (RFC-007 §2.5).
- [ ] MUST apply acceptance criteria from §2.6.
- [ ] MUST store workload, results, environment and command (RFC-007 §2.7).
- [ ] MUST report negative results without omission (RFC-007 §2.6).
- [ ] MUST seed all randomization (RFC-007 §2.8).

---

## 4. Examples

### 4.1 Minimal Deterministic Workload

Organization State fixture:

```text
{
  "identity": {"org": "ORG-007"},
  "pressure": 8.2,        // relevance: [control, safety]
  "temperature": 72.0,    // relevance: [control, safety]
  "mode": "AUTO",         // relevance: [control]
  "ledger_balance": 999,  // relevance: [finance]
  "hr_headcount": 42      // relevance: [hr]
}
```

Task T1: "Is pressure within limit 4.0–10.0?" — required fields: `[pressure]`.

- Fc: full State serialized → 5 fields.
- Sc: only `pressure` → 1 field.

Per RFC-004 the operation is deterministic (RFC-004 §44): no reasoning required.

### 4.2 Expected Observable (illustrative, not a claim)

```text
condition    total_cost   mean_quality
Fc           5000         1.0
Sc           1000         1.0

cost_ratio = 5.0 >= 2.0
quality_delta = 0.0 >= -0.10
→ H1 supported for this workload
```

This illustration is NOT a result. Results come only from actual runs.

---

## 5. Security Considerations

- Selection MUST NOT leak state outside the authority scope of the task (RFC-004 §19).
- Results and workloads MAY contain organizational fixtures; sensitive fixtures MUST be synthetic.
- The benchmark executor MUST NOT have access to the Full Context when evaluating Selective Context quality, and vice versa.
- This RFC consumes the canonical authority model from RFC-006. Authorization remains distinct from Decision, Approval, Invocation and Execution; benchmark governance MUST NOT redefine those concepts.
- If review or escalation is required during a benchmark workflow, it MUST be treated as a governance event or process, not as a Decision lifecycle state.

---

## 6. Alternatives

| Alternative | Considered because | Rejected because |
|-------------|-------------------|------------------|
| Accept RFC-004 as self-evident | Simpler | Assertion without measurement is not evidence (RFC-004 §54) |
| Define cost only in tokens | Simple | Ignores latency, retrieval, construction cost |
| Single fixed workload | Faster | Not representative; no generalization signal |
| Require LLM execution | Realistic | Not reproducible without external dependency; deterministic mode is baseline |

---

## 7. References

- ADR-0000 Governance
- ADR-0001 VIAL is a Distributed Cognitive Architecture
- RFC-003 Organizational State Model (§30, §31, §41)
- RFC-004 Context & Cognitive Efficiency (§9, §10, §44, §54)
- benchmark/README.md Benchmark Principles
- FCP-004 Success Metrics

---

## 8. Backward Compatibility

This RFC introduces no changes to existing specifications. It defines a validation protocol and a new reference artifact. It does not modify normative language of prior RFCs.

---

End of Document
