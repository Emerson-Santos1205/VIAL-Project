# VIAL Platform
# Benchmark: Economic Cost

Document: benchmark/economic-cost/README.md

Version: 1.0.0

Status: Draft

Type: Normative (reference implementation for RFC-010)

---

## Objective

Validate the **Economic Cost hypotheses (RFC-010)**:

- H1: divergence exists between the policy that minimizes TOKEN consumption and the policy that minimizes TOTAL cost (inference + latency + retrieval + construction + validation, not just tokens).
- H2: the Deterministic First policy (RFC-004 §23, RFC-010 §2.4) produces total cost less than or equal to the reason-everything policy, with no loss of correctness.

---

## Methodology

Per RFC-010:

1. A workload declares a stream of operations plus a price table (tokens_per_1k, inference_input/output_per_1k, latency, retrieval, construction, validation) and a tier order.
2. Each reasoning operation declares per-tier token volumes: `flash` is verbose but cheap per token; `advanced` is terse but expensive per token.
3. The same stream is evaluated under four policies:
   - **token_optimal**: chooses the tier minimizing token count per operation.
   - **total_cost_optimal**: chooses the tier minimizing total cost per operation.
   - **deterministic_first**: deterministic-solvable ops go to the deterministic tier; others use the cheapest capable tier.
   - **reason_everything**: always uses the most expensive capable tier.
4. Metrics: per-policy cost components, token_cheapest_policy vs total_cheapest_policy, det_first_total vs reason_total.
5. Acceptance (RFC-010 §2.6): divergence_exists (H1) AND det_first_total <= reason_total (H2).

---

## Files

| File | Purpose |
|------|---------|
| `generate_workload.py` | Deterministic workload generator (operations + price table) |
| `workloads/economic.json` | Declared workload fixture |
| `run_benchmark.py` | Validation harness |
| `run_opencode.py` | Supplemental two-model validation harness |
| `workloads/economic-real.json` | Small real-model workload with expected answers |
| `results/<run-id>/report.json` | Full artifacts per run |
| `prototype/cost.py` | CostModel / CostComponents / ResourceSelector |

---

## How to Reproduce

```text
python benchmark/economic-cost/generate_workload.py --operations 80 --deterministic-fraction 0.5 --out workloads/economic.json
python benchmark/economic-cost/run_benchmark.py
```

### Real-model validation

The real-model harness performs calibration first, freezes policy choices, and
then evaluates the four policies on a fresh pass. It requires exactly two
models and records actual model tokens, latency, inference cost and quality.
For this supplemental real-model extension, `token_cost` is based on
`input_tokens + output_tokens` from the model event stream; `context_tokens`
remains a separate diagnostic metric. This avoids treating identical VIAL
contexts as different token policies solely because different models were
selected.

```text
python benchmark/economic-cost/run_opencode.py --models openai/gpt-5.4 openai/gpt-5.6-luna --limit 8 --timeout 60
```

This is supplemental evidence. The declared price table is still part of the
experiment, and results must not be generalized beyond the tested models,
workload and configuration.

---

## Current Results

Run: 20260807-155118 (deterministic; identical metrics on re-run)

Workload: 80 operations (34 deterministic, 46 reasoning), seed 42.

| Policy | tokens | inference | latency | total |
|--------|--------|-----------|---------|-------|
| token_optimal | 0.002533 | 0.092997 | 0.012665 | 0.154995 |
| total_cost_optimal | 0.005258 | 0.035940 | 0.026292 | 0.114290 |
| deterministic_first | 0.005258 | 0.035940 | 0.026292 | 0.114290 |
| reason_everything | 0.002533 | 0.092997 | 0.012665 | 0.154995 |

| Hypothesis | Result |
|------------|--------|
| H1 Divergence (token_cheapest != total_cheapest) | **supported** |
| H2 Deterministic First (det_first_total <= reason_total) | **supported** |

Verdict: **H1 + H2 supported** — the token-minimal policy is NOT the total-cost-minimal policy; deterministic_first reproduces the total-cost optimum (0.114290) and beats reason_everything (0.154995).

---

## Interpretation

- **Divergence exists:** token_optimal picks the terse `advanced` tier (fewest tokens) but this is the most expensive tier per token; the cost-optimal choice is the verbose `flash` tier. In this price table, token-minimization and reason-everything coincide — the terse model is the premium model.
- **Deterministic First is cost-optimal here:** deterministic_first and total_cost_optimal produce identical cost (0.114290). RFC-010 §2.4's cheapest-capable-tier rule reproduces the total-cost optimum on this workload; it is not merely a heuristic.
- **Deterministic First saves ~26%** over reason_everything (0.114290 vs 0.154995).
- **Scope of validity:** cost model is workload-declared and uses synthetic token volumes; real-model quality parity is not asserted here (RFC-010 treats correctness as preserved by all policies; divergence is about cost, not correctness). Real API pricing and latency are out of scope for this benchmark.
- Real-model results, when available, are reported separately from this deterministic baseline and do not replace it.
- **Negative results are valid** (benchmark/README.md, Principle 2).

---

## Related Documents

- RFC-010 Economic Cost Model
- RFC-004 Organizational Design (§21-23)
- README §5 Economic Objective, §7 Economic Constraints
- benchmark/README.md Benchmark Principles

---

End of Document
