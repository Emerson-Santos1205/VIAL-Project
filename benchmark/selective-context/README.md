# VIAL Platform
# Benchmark: Selective Context

Document: benchmark/selective-context/README.md

Version: 1.0.0

Status: Draft

Type: Normative (reference implementation for RFC-007)

---

## Objective

Validate the **Selective Context Hypothesis (RFC-007)**:

> Executing a workload under Selective Context consumes materially less cognitive cost without materially degrading result quality, compared to Full Context.

---

## Methodology

Per RFC-007:

1. A workload `workload.json` is declared (immutable fixture: Organization State with relevance descriptors + task list).
2. Each task is executed under **Full Context** (complete serialized State) and **Selective Context** (projection by relevance descriptor, with references).
3. Cost is measured in tokens (`tiktoken` cl100k_base).
4. Quality is scored by a deterministic evaluator (0.0/1.0 exact match).
5. Acceptance criteria (RFC-007 §2.6):
   - `cost_ratio >= 2.0`
   - `mean_quality(Sc) >= mean_quality(Fc) * 0.90`

---

## Files

| File | Purpose |
|------|---------|
| `workload.json` | Declared workload fixture (RFC-007 §2.4) |
| `run_benchmark.py` | Validation harness (RFC-007 §2.7) |
| `results/<run-id>/report.json` | Full artifacts per run |
| `prototype/` (repo root) | Minimal OCS + Context Builder + executor |

---

## How to Reproduce

```text
python benchmark/selective-context/run_benchmark.py
```

Optional:

```text
python benchmark/selective-context/run_benchmark.py --workload workload.json --out results
```

---

## Current Results

Run: 20260807-144626 (reproducible; identical metrics on re-run)

| Metric | Full Context | Selective Context |
|--------|--------------|-------------------|
| total_cost | 738 | 269 |
| mean_cost | 147.6 | 53.8 |
| mean_quality | 1.0 | 1.0 |

Verdict: **H1 supported** — cost_ratio 2.74 >= 2.0, quality_delta 0.0.

---

## Interpretation

- The selective projection reduced token cost by ~64% with identical quality on this deterministic workload.
- **Scope of validity:** this is a baseline (deterministic, 5 tasks, single Organization). It validates the mechanism, not generalization. Larger and non-deterministic workloads are required before accepting RFC-007 beyond this workload.
- **Negative results are valid** (benchmark/README.md, Principle 2): any run that fails `cost_ratio` or `quality_floor` is reported and must not be discarded.

---

## Related Documents

- RFC-007 Selective Context Hypothesis & Validation Protocol
- RFC-003 Organizational State Model (§30, §31, §41)
- RFC-004 Context & Cognitive Efficiency (§9, §10, §44, §54)
- benchmark/README.md Benchmark Principles

---

End of Document
