# Specification Coverage

`spec_coverage.json` is an explicit traceability matrix for selected
requirements that are currently implemented by the reference prototype. It is
not a claim that the whole VIAL specification is implemented.

Run the report with:

```text
python audit/spec_coverage.py
```

The matrix distinguishes `covered`, `partial` and `uncovered` requirements.
New prototype behavior should add a requirement row and a direct test before
being described as implemented.
