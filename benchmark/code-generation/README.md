# Code Generation Benchmark

This supplemental benchmark measures whether VIAL-style selective Context
preserves code correctness while reducing the Context sent to an `opencode`
model. It is not a replacement for RFC-007 through RFC-010.

Run with an authenticated model supported by `opencode`:

```text
python benchmark/code-generation/run_opencode.py --model openai/gpt-5.5 --limit 2
```

Metrics include test pass rate, Context tokens, model tokens, elapsed time and
the Full versus Selective quality delta. A generated solution is successful
only when its task tests pass in an isolated temporary workspace.
