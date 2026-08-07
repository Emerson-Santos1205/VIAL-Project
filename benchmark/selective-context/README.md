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

Generate a scaled workload:

```text
python benchmark/selective-context/generate_workload.py --fields 1000 --tasks 300 --out workloads/w1000.json
```

Run the scaling sweep:

```text
python benchmark/selective-context/run_scaling.py --sizes 100,1000,10000,100000 --tasks 200
```

### Real-model (LLM) validation

Costs real API tokens. Set environment variables first:

```text
set VIAL_LLM_API_KEY=your-key
set VIAL_LLM_BASE_URL=https://api.openai.com/v1   (optional, OpenAI-compatible)
set VIAL_LLM_MODEL=gpt-4o-mini                    (optional)
```

Generate a reasoning workload and run:

```text
python benchmark/selective-context/generate_llm_workload.py --entries 200 --tasks 100 --out workloads/reasoning.json
python benchmark/selective-context/run_llm.py --workload workloads/reasoning.json --limit 20
```

The reasoning workload uses non-deterministic tasks (True/False over text entries), which is the setting where quality parity is actually meaningful. `--limit` caps the number of tasks to control cost on the first run.

---

## Current Results

### Baseline (workload.json, 5 fields / 5 tasks)

Run: 20260807-144626 (reproducible; identical metrics on re-run)

| Metric | Full Context | Selective Context |
|--------|--------------|-------------------|
| total_cost | 738 | 269 |
| mean_cost | 147.6 | 53.8 |
| mean_quality | 1.0 | 1.0 |

Verdict: **H1 supported** — cost_ratio 2.74 >= 2.0, quality_delta 0.0.

### Scaling sweep (seed 42, 200 tasks/size)

Run: 20260807 (artifacts: results/scaling.json)

| State fields | Full total_cost | Selective total_cost | cost_ratio | qFc | qSc | H1 |
|--------------|-----------------|----------------------|------------|-----|-----|----|
| 100 | 549,976 | 20,991 | 26.2 | 1.0 | 1.0 | yes |
| 1,000 | 5,423,393 | 22,137 | 245.0 | 1.0 | 1.0 | yes |
| 10,000 | 54,149,943 | 20,838 | 2,598.6 | 1.0 | 1.0 | yes |
| 100,000 | 541,367,586 | 21,288 | 25,430.6 | 1.0 | 1.0 | yes |

Key observation: **Selective Context cost is ~constant (~105 tokens/task) regardless of state size**, while Full Context grows linearly with state size. Cost ratio scales with organization size, matching the RFC-003 §41 prediction (`Large State → Large Context → High Token Cost`).

---

## Interpretation

- The selective projection reduced token cost by ~64% on the baseline workload and by up to 4 orders of magnitude at 100,000 fields, with identical quality.
- **Scope of validity:** results so far are deterministic (rule-based executor, no LLM). They validate the mechanism and the scaling prediction, not real-model generalization.
- **Next step:** an LLM executor (real model) is required to validate quality parity on non-deterministic reasoning tasks.
- **Negative results are valid** (benchmark/README.md, Principle 2): any run that fails `cost_ratio` or `quality_floor` is reported and must not be discarded.

---

## Related Documents

- RFC-007 Selective Context Hypothesis & Validation Protocol
- RFC-003 Organizational State Model (§30, §31, §41)
- RFC-004 Context & Cognitive Efficiency (§9, §10, §44, §54)
- benchmark/README.md Benchmark Principles

---

End of Document
