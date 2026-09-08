"""Reuse Engine for RFC-008 - Cognitive Reuse.

Implements RFC-004 §23-27 and RFC-008 §2.3:
- deterministic Reuse Signature per operation;
- cache lookup with State compatibility verification;
- invalidation when referenced State has changed;
- no executor invocation on cache hits.
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from .context import Context, Task
from .state import Organization


def reuse_signature(task: Task, base_commit: str = "",
                    workspace_digest: str = "",
                    dependency_hash: str = "",
                    toolchain_id: str = "",
                    context_fingerprint: str = "") -> str:
    """Deterministic key from operation semantics (type + params) and
    workspace context (RFC-008 §2.2).

    Includes workspace context to prevent reuse from semantically different
    workspaces that happen to have the same task and file set.

    If context_fingerprint is provided, it is included in the signature
    to ensure consistency with the Context's fingerprint. This enables
    cognitive reuse by allowing the system to recognize when the same
    task is executed in the same environment.
    """
    sig_data = {
        "op": task.op,
        "args": task.args,
    }
    # Add workspace context if provided (non-empty)
    if base_commit:
        sig_data["base_commit"] = base_commit
    if workspace_digest:
        sig_data["workspace_digest"] = workspace_digest
    if dependency_hash:
        sig_data["dependency_hash"] = dependency_hash
    if toolchain_id:
        sig_data["toolchain"] = toolchain_id
    if context_fingerprint:
        sig_data["context_fingerprint"] = context_fingerprint
    return json.dumps(sig_data, sort_keys=True)


@dataclass
class CachedResult:
    """A validated cognition result with its State compatibility envelope."""
    signature: str
    outcome: Any
    quality: float
    state_version: int
    referenced_fields: dict[str, Any]  # field key -> value at validation time
    provenance: str
    created_at: float = field(default_factory=time.time)


class ReuseEngine:
    """Validates and reuses organizational cognition (RFC-008 §2.3)."""

    def __init__(self, org: Organization):
        self.org = org
        self.cache: dict[str, CachedResult] = {}
        self.reuse_hits = 0
        self.recomputes = 0
        self.invalidations = 0

    def lookup(self, task: Task, base_commit: str = "",
               workspace_digest: str = "", dependency_hash: str = "",
               toolchain_id: str = "",
               context_fingerprint: str = "") -> tuple[CachedResult | None, str]:
        """Return (cached_result, outcome). outcome in {hit, miss, stale}.

        A stale entry is invalidated and treated as a miss (RFC-008 §2.3.5).
        """
        sig = reuse_signature(task, base_commit, workspace_digest,
                              dependency_hash, toolchain_id, context_fingerprint)
        entry = self.cache.get(sig)
        if entry is None:
            return None, "miss"
        if not self._compatible(entry, task):
            self.invalidations += 1
            del self.cache[sig]
            return None, "stale"
        return entry, "hit"

    def _compatible(self, entry: CachedResult, task: Task) -> bool:
        """State compatibility: referenced fields have the same values now
        (RFC-008 §2.2, RFC-004 §25)."""
        for key, value in entry.referenced_fields.items():
            f = self.org.fields.get(key)
            if f is None or f.value != value:
                return False
        return True

    def store(self, task: Task, outcome: Any, quality: float,
              ctx: Context, provenance: str, base_commit: str = "",
              workspace_digest: str = "", dependency_hash: str = "",
              toolchain_id: str = "",
              context_fingerprint: str = "") -> CachedResult:
        """Store a validated result with references to the State it used."""
        fields = {
            key: self.org.fields[key].value
            for key in _ctx_field_keys(ctx)
            if key in self.org.fields
        }
        entry = CachedResult(
            signature=reuse_signature(task, base_commit, workspace_digest,
                                      dependency_hash, toolchain_id,
                                      context_fingerprint),
            outcome=outcome,
            quality=quality,
            state_version=self.org.state_version,
            referenced_fields=fields,
            provenance=provenance,
        )
        self.cache[entry.signature] = entry
        return entry

    def stats(self) -> dict:
        return {
            "reuse_hits": self.reuse_hits,
            "recomputes": self.recomputes,
            "invalidations": self.invalidations,
        }


def _ctx_field_keys(ctx: Context) -> list[str]:
    keys = []
    for ref in ctx.references:
        if ref.startswith("state:"):
            keys.append(ref[len("state:"):])
    return keys
