# Supplemental Model Comparison

This is a non-normative validation protocol that complements RFC-007, RFC-008
and RFC-009. It does not replace their deterministic benchmarks.

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

The comparison report is written under `benchmark/model-comparison/results/`.
A model/provider authentication failure is a failed run, not evidence of
quality or cost.
