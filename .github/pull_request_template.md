## Summary

Briefly describe the change.

## Type

- [ ] Documentation (specs, RFC, ADR, SDK)
- [ ] Prototype (Python, `prototype/`)
- [ ] Benchmark (harness or workload, `benchmark/`)
- [ ] Tooling / build / CI

## Evidence

VIAL requires **evidence over authority**. Every claim must be backed by a
reproducible benchmark under `benchmark/`.

- [ ] No `prototype/` behavior changed
- [ ] If `prototype/` changed, all deterministic benchmarks report
      `hypotheses_supported: true`
- [ ] If a new hypothesis was introduced, an RFC + benchmark is included

## Conventions

- [ ] New references point to existing documents (no invented identifiers)
- [ ] Errors use the structured `VIALError` model (SDK-001 §30-31)
- [ ] Documents written in English; code uses `from __future__ import annotations`
