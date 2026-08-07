# VIAL Platform
# Benchmark: Cognitive Reuse

Document: benchmark/cognitive-reuse/README.md

Version: 1.0.0

Status: Draft

Type: Normative (reference implementation for RFC-008)

---

## Objective

Validate the **Cognitive Reuse hypotheses (RFC-008)**:

- H1: reusing validated cognition costs materially less than recomputing every operation.
- H2: reuse preserves correctness when relevant State is unchanged.
- H3: State changes invalidate cached results; no stale cognition is served.

---

## Methodology

Per RFC-008:

1. A workload `workloads/reuse.json` declares an **ordered operation stream** over an Organization State, plus a State-change schedule (`transitions`).
2. The same stream is consumed under two conditions:
   - **no_reuse**: every operation invokes the executor.
   - **reuse**: a Reuse Engine checks the cache; hits cost 0 tokens, misses/stale recompute.
3. State changes are applied identically in both conditions.
4. Metrics: cost_ratio, reuse_rate, stale_served, invalidations, mean_quality.
5. Acceptance (RFC-008 §2.5): `cost_ratio >= 2.0` AND quality parity AND `stale_served == 0` AND every transition detected.

---

## Files

| File | Purpose |
|------|---------|
| `generate_workload.py` | Deterministic workload generator (fields + op stream + drift schedule) |
| `workloads/reuse.json` | Declared workload fixture (RFC-008 §2.6) |
| `run_benchmark.py` | Validation harness (deterministic executor) |
| `run_opencode.py` | Real-model validation harness (opencode CLI executor) |
| `results/<run-id>/report.json` | Full artifacts per run |
| `prototype/reuse.py` | Reuse Engine (signature + State compatibility + invalidation) |

---

## How to Reproduce

```text
python benchmark/cognitive-reuse/generate_workload.py --fields 50 --tasks-per-field 4 --drift-fraction 0.5 --out workloads/reuse.json
python benchmark/cognitive-reuse/run_benchmark.py
python benchmark/cognitive-reuse/run_opencode.py --limit 50   # real-model validation
```

---

## Current Results

Run: 20260807-153940 (reproducible; identical metrics on re-run)

Workload: 50 fields, 224 operations, 24 State changes.

| Metric | no_reuse | reuse |
|--------|----------|-------|
| total_cost (tokens) | 13,216 | 4,366 |
| mean_cost | 59.0 | 19.5 |
| mean_quality | 1.0 | 1.0 |
| reuse_rate | — | 0.67 |
| invalidations | — | 24 (all State changes detected) |
| stale_served | — | 0 |

Verdict: **H1 + H2 + H3 supported** — cost_ratio 3.03 >= 2.0, quality_delta 0.0,
stale_served 0, all 24 transitions invalidated.

### Real-model validation (opencode CLI, deepseek-v4-flash-free)

Run: 20260807-164928 (50 tasks = 10 fields, seed 42 workload prefix)

| Metric | no_reuse | reuse |
|--------|----------|-------|
| total_cost (context tokens) | 2,950 | 1,062 |
| mean_cost | 59.0 | 21.24 |
| mean_quality | 1.0 | 1.0 |
| total_model_tokens (opencode) | 411,249 | 148,119 |
| reuse_rate | — | 0.64 |
| invalidations | — | 7 (all 7 exercised State changes) |
| stale_served | — | 0 |

Verdict: **H1 + H2 + H3 supported** — cost_ratio 2.78 >= 2.0, quality 1.0 >= floor 0.90,
7/7 invalidations, 0 stale. The Reuse Engine served 64% of tasks from cache without
executor invocation; model token consumption dropped ~2.8x (411,249 → 148,119) with
identical quality.

---

## Interpretation

- Reuse eliminated ~67% of executor invocations (150/224 hits), cutting token cost ~3x with identical quality.
- **Correctness preserved under State change:** every one of the 24 State changes was detected and invalidated; no stale result was served (H3).
- **Real-model run confirms the same behavior with an actual LLM:** 64% of tasks served from cache, ~2.8x fewer model tokens, quality 1.0, all 7 exercised State changes invalidated. Same-engine behavior holds on real model output, not just the deterministic executor.
- **Scope of validity:** deterministic workload with exact-signature reuse. Semantic similarity reuse (RFC-004 §25) is out of scope for this benchmark. The real-model result is a 50-task prefix on one model and does not establish generalization across models or task types.
- **Negative results are valid** (benchmark/README.md, Principle 2): any run that fails cost, quality or staleness criteria is reported, not discarded.

---

## Related Documents

- RFC-008 Cognitive Reuse Hypothesis & Validation Protocol
- RFC-004 Context & Cognitive Efficiency (§23, §24, §25, §26, §27)
- README §13 Reason Once, Reuse Many Times
- benchmark/README.md Benchmark Principles

---

End of Document
