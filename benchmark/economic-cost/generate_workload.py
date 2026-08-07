"""Deterministic generator for the RFC-010 economic-cost workload.

Produces an operation stream with a declared price table and two cost
scenarios designed to test the RFC-010 hypotheses:
- a "cheap verbose" tier vs an "expensive terse" tier, so token-optimal and
  total-cost-optimal policies can diverge (H1);
- a mix of deterministic-solvable and reasoning-required operations, so a
  Deterministic First selector is cheaper than reasoning about everything (H2).

Usage:
    python benchmark/economic-cost/generate_workload.py \
        --operations 80 --deterministic-fraction 0.5 --out workloads/economic.json
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def _price_table() -> dict:
    """Plausible economics: terse 'advanced' model is pricey per token; verbose
    'flash' model is cheap per token but verbose (more tokens)."""
    return {
        # token accounting price (per 1k tokens)
        "tokens_per_1k": 0.0002,
        # inference prices per 1k tokens (input / output) BEFORE tier multiplier
        "inference_input_per_1k": 0.0015,
        "inference_output_per_1k": 0.0020,
        # latency priced per second, scaled by tokens
        "latency_per_second": 0.001,
        "retrieval_per_op": 0.0001,
        "construction_per_context": 0.0002,
        "validation_per_op": 0.0003,
    }


def _reasoning_op(rng: random.Random) -> dict:
    """A reasoning-required operation. Token volume depends on tier:
    flash is verbose (more tokens, cheap per token), advanced is terse
    (fewer tokens, expensive per token)."""
    base = rng.randint(200, 300)
    return {
        "capable_tiers": ["flash", "advanced"],
        "tier_tokens": {
            "flash": base + rng.randint(150, 250),
            "advanced": base - rng.randint(80, 120),
        },
        "tier_multipliers": {"flash": 1.0, "advanced": 6.0},
        "retrievals": rng.randint(0, 3),
        "validations": 1,
        "output_tokens": rng.randint(30, 80),
    }


def generate(n_operations: int, deterministic_fraction: float, seed: int) -> dict:
    rng = random.Random(seed)

    operations = []
    for i in range(n_operations):
        is_det = rng.random() < deterministic_fraction
        if is_det:
            operations.append({
                "id": f"op_{i:04d}",
                "deterministic_solvable": True,
                "capable_tiers": ["deterministic"],
                "tier_tokens": {"deterministic": rng.randint(60, 120)},
                "tier_multipliers": {"deterministic": 0.0},
                "retrievals": 0,
                "validations": 1,
                "output_tokens": 5,
            })
        else:
            op = _reasoning_op(rng)
            op["id"] = f"op_{i:04d}"
            op["deterministic_solvable"] = False
            operations.append(op)

    return {
        "name": "economic-cost-bench",
        "org_id": "eco-org",
        "seed": seed,
        "quality_tolerance": 0.10,
        "price_table": _price_table(),
        "tier_order": ["deterministic", "flash", "advanced"],
        "operations": operations,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--operations", type=int, default=80)
    ap.add_argument("--deterministic-fraction", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="workloads/economic.json")
    args = ap.parse_args()

    wl = generate(args.operations, args.deterministic_fraction, args.seed)
    out = Path(__file__).resolve().parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(wl, indent=2), encoding="utf-8")
    det = sum(1 for o in wl["operations"] if o["deterministic_solvable"])
    print(json.dumps({
        "workload": wl["name"],
        "operations": len(wl["operations"]),
        "deterministic": det,
        "reasoning": len(wl["operations"]) - det,
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
