# VIAL Audit Framework

This directory contains the repository's independent, repeatable audit layer.
Audit documents describe scope and acceptance criteria; `run_all.py` executes
the automated checks and writes a machine-readable report.

The audit layer is separate from normative VIAL documents. It validates the
repository, specifications, prototype and release state without defining new
runtime semantics.

## Run

Static and conformance checks:

```text
python audit/run_all.py
```

Full verification, including the four deterministic benchmarks:

```text
python audit/run_all.py --full
```

The report is written to `audit/results/latest.json`. Generated benchmark
artifacts under `results/_audit_check` are removed after a full run.

## Audits

| ID | Scope |
| --- | --- |
| AUDIT-000 | Framework and execution contract |
| AUDIT-001 | Repository integrity |
| AUDIT-002 | Dependency and reference integrity |
| AUDIT-003 | Normative alignment |
| AUDIT-004 | Canonical model alignment |
| AUDIT-005 | Cross-layer consistency |
| AUDIT-006 | Runtime conformance |
| AUDIT-007 | SDK conformance |
| AUDIT-008 | Tools conformance |
| AUDIT-009 | Examples conformance |
| AUDIT-010 | Security and authority |
| AUDIT-011 | Lifecycle consistency |
| AUDIT-012 | Terminology and identifier consistency |
| AUDIT-013 | Documentation quality |
| AUDIT-014 | Dependency graph / DAG |
| AUDIT-015 | Release readiness |

An audit result is `PASS`, `FAIL` or `SKIP`. `--full` is required before a
release-readiness claim because it runs the deterministic evidence suite.
