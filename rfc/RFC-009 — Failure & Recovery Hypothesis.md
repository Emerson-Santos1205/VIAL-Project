# VIAL Platform
# Request for Comments

---

Document ID: RFC-009

Title: Failure & Recovery Hypothesis & Validation Protocol

Version: 1.0.0-draft.1

Status: Draft

Category: Technical Specification

Dependencies:

- ADR-0001 VIAL is a Distributed Cognitive Architecture
- ADR-0002 Adoption of Distributed Organizational Cognition
- RFC-003 Organizational State Model
- RFC-008 Cognitive Reuse Hypothesis & Validation Protocol

---

## Abstract

This document converts the VIAL **Failure & Recovery** principle (README §16; RFC-003 §34, §35, §58) into **falsifiable hypotheses** with a **reproducible validation protocol**, following the discipline of RFC-007 and RFC-008.

VIAL claims that execution resource failure does not become organizational failure: an interrupted operation neither corrupts authoritative State nor causes double execution after recovery.

This RFC defines what would have to be observed to accept these claims, and how to reproduce the measurement.

The companion artifact is the reference benchmark in `benchmark/failure-recovery/`.

---

## 1. Context

README §16 states the principle:

> A resource failure should not automatically become an organizational failure.

RFC-003 establishes the corresponding State properties:

- **Atomic transition (§17):** an incomplete transition must not be observable; State goes from A to B directly.
- **Transition failure (§34):** if a transition cannot be safely committed, the previous valid State remains authoritative.
- **Recovery (§35, §58):** an interrupted operation can be resolved to *committed*, *failed* or *uncertain* using Transition ID, Previous State, and Transition Record; the system MUST avoid executing the operation twice merely because confirmation was lost.

RFC-003 is normative theory. It does not demonstrate that a real coordinator preserves these properties under injected failure.

RFC-009 fills that gap.

---

## 2. Specification

### 2.1 Falsifiable Hypotheses

**H1 (Continuity):**

> An organization that suffers execution resource failures at arbitrary points during an operation stream converges to the SAME authoritative State as the same stream without failures, after recovery.

**H2 (Atomicity):**

> No observable intermediate State exists for a failed or interrupted transition: State either reflects the transition fully or not at all.

**H3 (Recovery Resolution & Idempotency):**

> Every interrupted operation resolves deterministically to exactly one outcome (committed / failed / aborted) using the transition log alone, and a retried operation NEVER produces a duplicate transition (each operation_id commits at most once).

**H0 (Null):** at least one of H1, H2 or H3 fails.

| Hypothesis | Criterion |
|-----------|-----------|
| H1 | `final_state(recovery) == final_state(no_failures)` AND `version(recovery) == version(no_failures)` |
| H2 | `observed_intermediate_states == 0` |
| H3 | `unresolved_operations == 0` AND `duplicate_commits == 0` AND `resolved_committed == committed_operations` |

### 2.2 Operational Definitions

**Operation:** a single intended State Transition, identified by a unique `operation_id`.

**Interrupted operation:** an operation whose executor fails between request and acknowledged completion.

**Recovery:** the process of determining an interrupted operation's outcome from the transition log (`previous_state`, `resulting_state`, `status`) and, where needed, completing or aborting it.

**Duplicate commit:** applying the same `operation_id` as a committed transition more than once.

**Observed intermediate state:** a State read that reflects only part of an intended transition (e.g., a new version recorded but field value not applied, or vice versa).

**Authoritative State:** the State recognized as current truth (RFC-003 §24).

### 2.3 Coordinator Behavior

A conforming coordinator MUST:

1. assign every operation a unique `operation_id`;
2. record operation intent (operation_id, previous_state, expected fields) before mutating State;
3. apply the transition atomically: State version and values change together or not at all;
4. on failure between intent and commit, leave the previous valid State authoritative;
5. on recovery, resolve an interrupted operation from the log:
   - intent recorded, not committed → MAY complete or abort;
   - already committed → return the existing committed outcome, do NOT re-apply;
6. never commit the same `operation_id` twice.

### 2.4 Metrics

| Metric | Definition |
|--------|------------|
| final_state_equal | authoritative State after recovery equals no-failure run |
| version_equal | State version after recovery equals no-failure run |
| observed_intermediate_states | number of reads exposing a partial transition |
| unresolved_operations | interrupted operations left without a resolved outcome |
| duplicate_commits | operation_ids committed more than once |
| resolved_committed | interrupted operations resolved to committed |
| total_committed | number of committed transitions |

### 2.5 Acceptance Criteria

H1 supported when `final_state_equal == True` AND `version_equal == True`.
H2 supported when `observed_intermediate_states == 0`.
H3 supported when `unresolved_operations == 0` AND `duplicate_commits == 0`.

All three MUST hold. Any failure is a valid negative result and MUST be reported.

### 2.6 Required Artifacts

Every validation run MUST produce:

1. workload declaration (operation stream + deterministic failure schedule);
2. per-operation outcomes and resolutions;
3. summary metrics;
4. environment description;
5. the exact reproduction command.

### 2.7 Reproducibility Rules

- The failure schedule (which operations fail and at what point) MUST be deterministic and identical across runs.
- The no-failure and failure-injected runs MUST consume the same operation stream.
- Randomness MUST be seeded.

---

## 3. Conformance Requirements

- [ ] MUST assign a unique operation_id per operation (RFC-009 §2.3.1).
- [ ] MUST record intent before mutation (RFC-009 §2.3.2).
- [ ] MUST apply transitions atomically (RFC-009 §2.3.3).
- [ ] MUST resolve every interrupted operation from the log (RFC-009 §2.3.5).
- [ ] MUST NOT commit the same operation_id twice (RFC-009 §2.3.6).
- [ ] MUST compare against a no-failure run (RFC-009 §2.1 H1).
- [ ] MUST report negative results without omission (RFC-009 §2.5).

---

## 4. Examples

### 4.1 Interrupted Commit

```text
operation_id: O-42, field: pressure, new value: 12.0
intent recorded  (previous_state: v10, status: PENDING)
[ executor fails here ]
State remains at v10, pressure unchanged   → atomicity holds
recovery(O-42): intent recorded, not committed → re-drive or abort
```

### 4.2 Ack Lost After Commit

```text
operation_id: O-43, committed → State v11, status: COMMITTED
[ ack lost; caller retries ]
recovery(O-43): already committed → return v11 result, do NOT re-apply
→ no duplicate commit
```

---

## 5. Security Considerations

- Recovery MUST respect authority: only authorized actors may complete or abort an interrupted operation.
- The transition log is a trust boundary; tampering with it breaks recovery correctness and auditability (RFC-003 §33, §34).
- Idempotency keys (operation_id) MUST be unforgeable where the operation is consequential.

---

## 6. Alternatives

| Alternative | Considered because | Rejected because |
|-------------|-------------------|------------------|
| No intent log; retry freely | Simpler | Cannot distinguish committed-from-lost-ack vs never-committed; risks double execution |
| Lock everything during execution | Simple correctness | Kills concurrency; RFC-003 §26 permits concurrent execution |
| Assume failures are rare, ignore | Pragmatic | README §16 assumes failure; recovery must be tested, not assumed |

---

## 7. References

- ADR-0000 Governance
- ADR-0001 VIAL is a Distributed Cognitive Architecture
- RFC-003 Organizational State Model (§17, §18, §26, §33, §34, §35, §58)
- README §16 Failure and Recovery
- benchmark/README.md Benchmark Principles

---

## 8. Backward Compatibility

This RFC introduces no changes to existing specifications. It defines a validation protocol consistent with RFC-003 and RFC-008.

---

End of Document
