"""Token counting for cognitive cost measurement (RFC-007)."""
from __future__ import annotations

try:
    import tiktoken

    _ENC = tiktoken.get_encoding("cl100k_base")
    HAS_TIKTOKEN = True
except Exception:  # pragma: no cover - fallback path
    _ENC = None
    HAS_TIKTOKEN = False


def count_tokens(text: str) -> int:
    """Count tokens deterministically. Uses cl100k_base when available,
    else a whitespace word-count fallback."""
    if HAS_TIKTOKEN:
        return len(_ENC.encode(text))
    return len(text.split())


def count_tokens_in_parts(parts: list[str]) -> int:
    return sum(count_tokens(p) for p in parts)
