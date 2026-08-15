# VIAL Platform
# Benchmark

Document: benchmark/README.md

Version: 1.0.0

Status: Draft

Type: Normative

---

## Purpose

The benchmark directory contains evaluation methodology, performance tests, conformance tests and benchmarks for the VIAL Platform.

Benchmarks enable reproducible comparison of VIAL implementations against architectural requirements.

---

## Benchmark Categories

### 1. Conformance Benchmarks

Verify that implementations comply with VIAL specifications.

- TDOC compliance
- FCP compliance
- VCG compliance
- ADR compliance
- RFC compliance

### 2. Performance Benchmarks

Measure cognitive efficiency, token consumption, latency and throughput.

- Token Efficiency
- Cognitive Cost
- Communication Overhead
- State Synchronization
- Decision Latency

### 3. Scalability Benchmarks

Evaluate behavior under increasing organizational complexity.

- Agent Count Scaling
- Goal Count Scaling
- Knowledge Volume Scaling
- Memory Persistence
- Concurrent Organizations

### 4. Resilience Benchmarks

Test behavior under failure conditions.

- Agent Failure Recovery
- State Corruption Recovery
- Network Partition
- Knowledge Loss Recovery

---

## Benchmark Structure

Every benchmark SHOULD include:

- Objective
- Workload Definition
- Environment Description
- Configuration
- Metrics
- Baseline
- Expected Results
- Reproducibility Instructions

---

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Token Efficiency | Tokens per unit of organizational cognition |
| Cognitive Cost | Total cognitive cost per decision cycle |
| Communication Overhead | Messages per unit of knowledge transfer |
| Decision Latency | Time from proposal to validated decision |
| Knowledge Reuse Rate | Percentage of knowledge accessed vs transmitted |
| Audit Completeness | Percentage of decisions with full provenance |
| Recovery Time | Time to restore organizational state after failure |

---

## Benchmark Principles

1. Reproducibility is mandatory
2. Negative results are valid
3. Methodology changes must be documented
4. Cherry-picking is prohibited
5. Baselines must be included

---

## Relationship with FCP-004

Benchmarks SHALL measure success according to the dimensions defined in FCP-004 Success Metrics.

---

## Current Benchmarks

| Benchmark | Description | Status |
|-----------|-------------|--------|
| Selective Context | Validates RFC-007 hypothesis (Full vs Selective context) | Active |
| Cognitive Reuse | Validates RFC-008 hypothesis (reuse + invalidation) | Active |
| Failure & Recovery | Validates RFC-009 hypothesis (atomicity + idempotency + recovery) | Active |
| Economic Cost | Validates RFC-010 hypothesis (token vs total-cost divergence, deterministic-first) | Active |
| Supplemental Model Comparison | Repeated multi-model validation using opencode and harder workloads | Supplemental |
| Economic Cost (real-model) | RFC-010 calibration and policy comparison with two models | Supplemental |
| Conformance (planned) | RFC-003/004 conformance checks | Planned |

---

End of Document
