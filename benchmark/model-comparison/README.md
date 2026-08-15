# Supplemental Model Comparison

This is a non-normative validation protocol that complements RFC-007, RFC-008,
RFC-009 and RFC-010. It does not replace their deterministic benchmarks.

The protocol compares models available through the `opencode` CLI using:

- a harder multi-entry reasoning workload for Selective Context;
- repeated runs;
- actual model token counts and elapsed time;
- per-run quality and hypothesis verdicts;
- explicit provider/model failures instead of silently treating them as quality results.

Generate the harder workload:

```text
python benchmark/selective-context/generate_llm_workload.py --entries 200 --tasks 20 --seed 42 --difficulty hard --out workloads/hard-reasoning.json
```

Run a comparison:

```text
python benchmark/model-comparison/run_comparison.py --models openai/gpt-5.5 opencode/deepseek-v4-flash-free --repeats 2
```

For a bounded smoke comparison, reduce the workload and per-task timeout:

```text
python benchmark/model-comparison/run_comparison.py --models openai/gpt-5.5 opencode/deepseek-v4-flash-free --benchmarks selective --repeats 1 --limit 2 --timeout 60
```

The comparison report is written under `benchmark/model-comparison/results/`.
A separate directory is used for each model, repeat and benchmark so repeated
runs do not overwrite one another. The report includes per-model success
counts, failed provider calls and the UTC generation timestamp.
A model/provider authentication failure is a failed run, not evidence of
quality or cost.

RFC-010 is a paired-model benchmark. When selected, pass exactly two models;
the harness performs calibration and then evaluates frozen economic policies.
An unsupported H1 or H2 is a valid negative result, not a runner failure.

Results are intentionally excluded from version control. Preserve reports
outside the repository when maintaining a historical evidence archive, along
with the commit, model identifiers, workload version and run configuration.
