# VIAL Platform
# Benchmark: Failure & Recovery

Document: benchmark/failure-recovery/README.md

Version: 1.0.0

Status: Draft

Type: Normative (reference implementation for RFC-009)

---

## Objective

Validate the **Failure & Recovery hypotheses (RFC-009)**:

- H1: an organization with injected executor failures converges to the SAME authoritative State as a no-failure run.
- H2: no observable intermediate State exists for an interrupted transition (atomicity).
- H3: every interrupted operation resolves from the log, and no operation is ever committed twice (idempotency).

---

## Methodology

Per RFC-009:

1. A workload declares an ordered operation stream (State transitions) plus a deterministic failure schedule.
2. The same stream is run twice:
   - **no_failures**: every operation commits cleanly.
   - **with_failures**: operations fail at deterministic points (`before_commit` = intent recorded but interrupted; `after_commit` = committed but ack lost).
3. Recovery is deterministic: `before_commit` → abort + retry with a fresh operation_id; `after_commit` → resolve as committed, block the misinformed retry.
4. Metrics: final_state_equal, version_equal, observed_intermediate_states, unresolved_operations, duplicate_commits.
5. Acceptance (RFC-009 §2.5): H1 AND H2 AND H3.

---

## Files

| File | Purpose |
|------|---------|
| `generate_workload.py` | Deterministic operation-stream + failure-schedule generator |
| `workloads/failure.json` | Declared workload fixture |
| `run_benchmark.py` | Validation harness (deterministic stream) |
| `run_opencode.py` | Real-model validation harness (model proposes transitions) |
| `results/<run-id>/report.json` | Full artifacts per run |
| `prototype/coordinator.py` | StateCoordinator (intent log, atomic commit, recovery, idempotency) |

---

## How to Reproduce

```text
python benchmark/failure-recovery/generate_workload.py --fields 20 --operations 60 --fail-fraction 0.4 --out workloads/failure.json
python benchmark/failure-recovery/run_benchmark.py
python benchmark/failure-recovery/run_opencode.py --limit 40   # real-model validation
```

---

## Current Results

Run: 20260807-154621 (reproducible; identical metrics on re-run)

Workload: 20 fields, 60 operations, 23 injected failures (13 before_commit, 10 after_commit).

| Metric | no_failures | with_failures |
|--------|-------------|---------------|
| State version | 80 | 80 |
| Committed transitions | 80 | 80 |
| Interruptions | 0 | 23 |

| Hypothesis | Result |
|------------|--------|
| H1 Continuity (final_state_equal + version_equal) | **supported** |
| H2 Atomicity (observed_intermediate_states == 0) | **supported** |
| H3 Recovery (unresolved == 0, duplicate_commits == 0) | **supported** |

Verdict: **H1 + H2 + H3 supported** — 23/23 interruptions resolved, 0 duplicate commits, 0 intermediate states observed, final State identical to no-failure run.

### Real-model validation (opencode CLI, deepseek-v4-flash-free)

Run: 20260807-170233 (40 operations, model-proposed transitions)

| Metric | Result |
|--------|--------|
| proposal_quality (exact key+value match) | 1.0 (40/40) |
| pipeline_ops | 40 |
| Interruptions (injected) | 15 |
| final_state_equal + version_equal | true / true |
| observed_intermediate_states | 0 |
| unresolved_operations | 0 |
| duplicate_commits | 0 |

Verdict: **H1 + H2 + H3 supported** — a real model proposed every transition correctly
(40/40), and the StateCoordinator preserved continuity, atomicity, idempotency and
recovery through 15 injected interruptions on the model-proposed stream.

---

## Interpretation

- **Continuity holds:** after 23 interruptions at two different failure points, the organization converges to exactly the same State (values and version) as a failure-free run.
- **Atomicity holds:** a pending (intent-recorded, uncommitted) transition never exposed a partial State — version and values changed together on commit.
- **Idempotency holds:** misinformed retries of already-committed operations were blocked (10 cases); no operation_id was committed twice.
- **Real-model run confirms the same guarantees with model-proposed transitions:** the deepseek proposer produced the correct key/value 40/40 times, and the coordinator still converged identically (clean vs failure), with zero intermediate states and zero duplicates across 15 injected interruptions. The guarantees live in the coordinator, not in the executor.
- **Scope of validity:** single-coordinator, single-organization model. Distributed consensus, network partitions and replica recovery (RFC-003 §36) are out of scope for this benchmark.
- **Negative results are valid** (benchmark/README.md, Principle 2).

---

## Related Documents

- RFC-009 Failure & Recovery Hypothesis & Validation Protocol
- RFC-003 Organizational State Model (§17, §18, §26, §33, §34, §35, §58)
- README §16 Failure and Recovery
- benchmark/README.md Benchmark Principles

---

End of Document
