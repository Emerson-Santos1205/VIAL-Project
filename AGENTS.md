# AGENTS.md

Instructions for AI agents and human contributors working on the VIAL Platform.

This file is read automatically by AI coding assistants. It complements
`CONTRIBUTING.md` (human-facing) and `CODE_OF_CONDUCT.md` (behavior).

---

## Project Identity

VIAL is a **distributed cognitive architecture**: a persistent Organization
(which remembers, decides and learns) distinct from Execution Resources
(which may change). It is not a communication protocol and not a single AI
model. See `README.md`, `ADR-0001` and `FCP-002A`.

## Repository Layout

```text
fundation/   Foundations and principles (FCP-xxx, TDOC-xx)
adr/         Architecture Decision Records (ADR-xxxx)
rfc/         Request for Comments — falsifiable hypotheses (RFC-xxxx)
runtime/     Runtime engine specifications (RUNTIME-xxx)
sdk/         API specifications (SDK-xxx)
tools/       Tool specification documents (TOOLS-xxx)
examples/    Usage examples (EXAMPLE-xxx)
prototype/   Minimal reference implementation (Python)
benchmark/   Hypothesis validation harnesses + workloads (Python)
```

## Evidence Over Authority

- The project's central discipline is **hypothesis → RFC → minimal prototype →
  reproducible benchmark → validation**.
- A claim is accepted only when backed by a reproducible benchmark under
  `benchmark/`, not by assertion.
- Do NOT change behavior of the `prototype/` without re-running the affected
  deterministic benchmarks:
  `benchmark/selective-context/run_benchmark.py`,
  `benchmark/cognitive-reuse/run_benchmark.py`,
  `benchmark/economic-cost/run_benchmark.py`,
  `benchmark/failure-recovery/run_benchmark.py`.
- New ideas should be added as a new RFC + benchmark before being treated as
  normative.

## Change Process

- **Documentation references** must point to existing documents. Do not invent
  identifiers (e.g. `RFC-001` does not exist; the template is `RFC-0001`).
- **SDK-005 is the Decision API**; there is no `SDK-005 — State API` (ADR-0005).
- **Architectural changes** go through the FCP/ADR mechanism (see `adr/ADR-0003`).
- **Breaking changes** must be documented and follow ADR-0000.

## Core Contract Boundary

**Rule 1 — Composition Only:**
VIAL Code Agent MUST extend VIAL Core exclusively through composition,
configuration, adapters, strategies, and additive gates. It MUST NOT
subclass, replace, monkey-patch, or alter VIAL Core contracts.

**Rule 2 — ADR + Compatibility Test:**
Any feature that changes the semantics of a Core contract requires an ADR
and a compatibility test before implementation.

**Implementation guidance:**
- The Agent Runtime (`vial_runtime.py`) is a **composition layer** over Core
  components (state, decision, authorization, tools, resources, identity,
  persistence, coordination).
- New backends (e.g., PostgreSQL persistence, N-model consensus) implement
  existing Core interfaces — they do not replace or alter the interface itself.
- Core identity (context_id, resource_id, decision_id) is immutable. Contextual
  extensions (context_fingerprint, execution_fingerprint) are separate fields,
  not modifications to Core identity semantics.

## Examples Are Not a Second Specification

- Examples MAY instantiate normative concepts, but MUST NOT introduce new
  normative states, fields, lifecycle values, identifiers or error codes
  unless explicitly marked as illustrative (VCG-001 §2, CONTRIBUTING §8.1).
- Prefer canonical tokens: use `RESOURCE_UNAVAILABLE` (SDK-003 §77), not
  domain codes like `PUMP_NOT_AVAILABLE`; use `objective:`/`outcome:`
  (SDK-005 §10/§12), not `intent:`/`proposed_action:`; use `FAILED`
  (RUNTIME-001 outcomes), not `FAILURE` as a state.
- The `audit002.py` check K validates this automatically: any ALL-CAPS
  code-like token in `examples/` that does not occur in the normative corpus
  (sdk/, runtime/, rfc/, tools/, fundation/) fails.

## Prototype Conventions

- `prototype/` is a minimal reference implementation, additive and
  backward-compatible: benchmarks must keep passing unchanged.
- New surfaces conform to the SDK/RUNTIME documents they cite (document the
  section number in the module docstring).
- Errors must use the structured `VIALError` model (`prototype/errors.py`,
  SDK-001 §30-31), never raw exceptions escaping across boundaries.
- Keep dependency footprint minimal (stdlib + `tiktoken`/`httpx` where needed).

## Language and Style

- Documents are written in English (technical terms per `fundation/VCG-001`).
- Code: Python 3.10+, `from __future__ import annotations`, type hints.
- Do not add comments unless they explain *why*, not *what*.

## Verification

Before finishing a change that touches `prototype/`, run:

```text
python benchmark/selective-context/run_benchmark.py --out results/_check
python benchmark/cognitive-reuse/run_benchmark.py --out results/_check
python benchmark/economic-cost/run_benchmark.py --out results/_check
python benchmark/failure-recovery/run_benchmark.py --out results/_check
```

All four must report `hypotheses_supported: true`. Remove the `results/_check`
artifacts afterwards (they are git-ignored but keep the tree clean).

Run the canonical integrity audit after touching `examples/`, `sdk/`,
`runtime/`, `rfc/`, `tools/` or `fundation/`: the audit (check K) fails when
examples invent ALL-CAPS normative tokens absent from the normative corpus.
