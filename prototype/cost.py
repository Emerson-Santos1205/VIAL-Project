"""Economic cost model and cost-aware selector (RFC-004 §21-23, RFC-010).

Total cost = tokens + inference + latency + retrieval + construction + validation,
using a workload-declared price table (RFC-010 §2.2, §2.3).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .errors import VIALValidationError


@dataclass
class CostComponents:
    tokens: float = 0.0
    inference: float = 0.0
    latency: float = 0.0
    retrieval: float = 0.0
    construction: float = 0.0
    validation: float = 0.0

    def total(self) -> float:
        return (self.tokens + self.inference + self.latency
                + self.retrieval + self.construction + self.validation)

    def to_dict(self) -> dict:
        return {
            "tokens": round(self.tokens, 6),
            "inference": round(self.inference, 6),
            "latency": round(self.latency, 6),
            "retrieval": round(self.retrieval, 6),
            "construction": round(self.construction, 6),
            "validation": round(self.validation, 6),
            "total": round(self.total(), 6),
        }


class CostModel:
    """Applies the workload price table to operation costs."""

    def __init__(self, price_table: dict):
        self.p = price_table

    def infer(self, input_tokens: int, output_tokens: int,
              tier_multiplier: float = 1.0) -> CostComponents:
        """Inference cost from token volumes, scaled by reasoning tier."""
        c = CostComponents()
        c.tokens = (input_tokens + output_tokens) * self.p.get("tokens_per_1k", 0.0) / 1000.0
        c.inference = (
            input_tokens * self.p.get("inference_input_per_1k", 0.0)
            + output_tokens * self.p.get("inference_output_per_1k", 0.0)
        ) / 1000.0 * tier_multiplier
        c.latency = self.p.get("latency_per_second", 0.0) * (input_tokens + output_tokens) / 1000.0
        return c

    def retrieval(self, n_ops: int) -> CostComponents:
        c = CostComponents()
        c.retrieval = n_ops * self.p.get("retrieval_per_op", 0.0)
        return c

    def construction(self, n_contexts: int) -> CostComponents:
        c = CostComponents()
        c.construction = n_contexts * self.p.get("construction_per_context", 0.0)
        return c

    def validation(self, n_validations: int) -> CostComponents:
        c = CostComponents()
        c.validation = n_validations * self.p.get("validation_per_op", 0.0)
        return c

    def sum(self, *components: CostComponents) -> CostComponents:
        out = CostComponents()
        for c in components:
            out.tokens += c.tokens
            out.inference += c.inference
            out.latency += c.latency
            out.retrieval += c.retrieval
            out.construction += c.construction
            out.validation += c.validation
        return out


class ResourceSelector:
    """Cost-aware, Deterministic First selector (RFC-004 §23, RFC-010 §2.4)."""

    def __init__(self, tiers: dict[str, float], order: list[str]):
        """tiers: tier name -> cost multiplier (higher = more expensive).
        order: capability order from cheapest to most expensive."""
        self.tiers = tiers
        self.order = order  # e.g. ["deterministic", "light", "advanced"]

    def select(self, deterministic_solvable: bool, capable_tiers: list[str]) -> str:
        """Choose the cheapest capable tier; deterministic path first."""
        if deterministic_solvable:
            return "deterministic"
        for tier in self.order:
            if tier in capable_tiers:
                return tier
        raise VIALValidationError(
            "NO_CAPABLE_TIER",
            "no capable tier",
            details={"capable_tiers": capable_tiers})
