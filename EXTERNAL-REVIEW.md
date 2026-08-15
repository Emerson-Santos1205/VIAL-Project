# External Review Guide

This checklist supports an independent review of VIAL. It is deliberately
separate from the automated audit: a passing audit establishes repository
consistency, not architectural validity.

## Reproduction

1. Clone the repository at the commit under review.
2. Run `python -m unittest discover -s tests -p "test_*.py" -v`.
3. Run `python audit/run_all.py --full`.
4. Run `python audit/spec_coverage.py`.
5. If model credentials are available, run the protocol in
   `benchmark/model-comparison/README.md` and preserve failed provider runs.

## Questions

- Are the hypotheses falsifiable and compared with a credible baseline?
- Do deterministic benchmarks measure the claimed mechanism rather than only
  an implementation detail?
- Are model-based results reported with enough repetitions and quality metrics?
- Does the prototype enforce capability and authority as separate concepts?
- Are security-critical Tool paths covered by negative tests?
- Which normative requirements remain uncovered or only partially covered?
- Are the conclusions limited to the workloads, models and versions tested?

## Review Record

| Reviewer | Commit | Date | Findings | Decision |
|---|---|---|---|---|
| _name_ | _sha_ | _YYYY-MM-DD_ | _link or summary_ | _pending_ |
