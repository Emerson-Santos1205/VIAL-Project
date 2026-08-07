"""RFC-010 validation harness.

Evaluates execution policies against the economic cost model (RFC-010 §2.5):

Policy A (token-optimal): chooses the tier minimizing TOKEN count.
Policy B (total-cost-optimal): chooses the tier minimizing TOTAL cost.
Policy C (deterministic-first): follows RFC-004 §23 / RFC-010 §2.4.
Policy D (reason-everything): uses the most expensive capable tier always.

Metrics: divergence_exists (argmin tokens != argmin total), cost ratios,
quality parity. Quality is modeled per RFC-010 §2.2 (all policies preserve
correctness; divergence is about cost, not correctness).

Usage:
    python benchmark/economic-cost/run_benchmark.py [--workload workloads/economic.json] [--out results]
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(HERE))

from prototype.cost import CostComponents, CostModel  # noqa: E402

import importlib.util  # noqa: E402

_SC_HARNESS = BASE / "benchmark" / "selective-context" / "run_benchmark.py"
_spec = importlib.util.spec_from_file_location("sc_run_benchmark", _SC_HARNESS)
_sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sc)
load_workload = _sc.load_workload


def _eval_policy(ops: list[dict], tier_for_op, cm: CostModel) -> dict:
    total = CostComponents()
    for op in ops:
        tier = tier_for_op(op)
        input_tokens = op["tier_tokens"].get(tier, 0)
        output_tokens = op.get("output_tokens", 0)
        mult = op.get("tier_multipliers", {}).get(tier, 0.0)
        comps = [
            cm.infer(input_tokens, output_tokens, mult),
            cm.retrieval(op.get("retrievals", 0)),
            cm.construction(1),
            cm.validation(op.get("validations", 1)),
        ]
        total = cm.sum(total, *comps)
    return total.to_dict()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", default="workloads/economic.json")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    wl = load_workload(base / args.workload)
    ops = wl["operations"]
    cm = CostModel(wl["price_table"])
    order = wl["tier_order"]

    # Policy A: token-optimal (minimize total token count per operation)
    def policy_token(op):
        if op["deterministic_solvable"]:
            return "deterministic"
        return min(op["capable_tiers"], key=lambda t: op["tier_tokens"].get(t, 0))

    # Policy B: total-cost-optimal (minimize total across capable tiers)
    def policy_total(op):
        if op["deterministic_solvable"]:
            return "deterministic"
        best, best_cost = None, float("inf")
        for tier in op["capable_tiers"]:
            input_tokens = op["tier_tokens"].get(tier, 0)
            mult = op.get("tier_multipliers", {}).get(tier, 0.0)
            comp = cm.infer(input_tokens, op.get("output_tokens", 0), mult)
            cost = comp.total()
            if cost < best_cost:
                best, best_cost = tier, cost
        return best

    # Policy C: deterministic-first (RFC-010 §2.4) = cheapest capable tier
    def policy_det_first(op):
        if op["deterministic_solvable"]:
            return "deterministic"
        for tier in order:
            if tier in op["capable_tiers"]:
                return tier
        raise ValueError("no capable tier")

    # Policy D: reason-everything (always most expensive capable tier)
    def policy_reason_everything(op):
        if op["deterministic_solvable"]:
            return "deterministic"  # still deterministic-solvable
        for tier in reversed(order):
            if tier in op["capable_tiers"]:
                return tier
        raise ValueError("no capable tier")

    a = _eval_policy(ops, policy_token, cm)
    b = _eval_policy(ops, policy_total, cm)
    c = _eval_policy(ops, policy_det_first, cm)
    d = _eval_policy(ops, policy_reason_everything, cm)

    policies = {"token": a, "total": b, "det_first": c, "reason": d}
    token_cheapest = min(policies, key=lambda k: policies[k]["tokens"])
    total_cheapest = min(policies, key=lambda k: policies[k]["total"])
    divergence_exists = token_cheapest != total_cheapest

    h2 = (c["total"] <= d["total"])
    verdict = {
        "divergence_exists": divergence_exists,
        "token_cheapest_policy": token_cheapest,
        "total_cheapest_policy": total_cheapest,
        "h1_token_total_divergence": divergence_exists,
        "det_first_total": c["total"],
        "reason_total": d["total"],
        "det_first_le_reason": h2,
        "h2_deterministic_first": h2,
        "hypotheses_supported": divergence_exists and h2,
    }

    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_dir = base / args.out / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "run_id": run_id,
        "rfc": "RFC-010",
        "workload": wl["name"],
        "seed": wl.get("seed"),
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform()},
        "price_table": wl["price_table"],
        "policies": {"token_optimal": a, "total_cost_optimal": b,
                     "deterministic_first": c, "reason_everything": d},
        "token_cheapest_policy": token_cheapest,
        "total_cheapest_policy": total_cheapest,
        "verdict": verdict,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "token_optimal": a,
        "total_cost_optimal": b,
        "deterministic_first": c,
        "reason_everything": d,
        "token_cheapest_policy": token_cheapest,
        "total_cheapest_policy": total_cheapest,
        "verdict": verdict,
        "artifacts": str(out_dir),
    }, indent=2))
    return 0 if verdict["hypotheses_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
