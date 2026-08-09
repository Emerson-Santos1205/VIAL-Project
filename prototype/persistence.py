"""Atomic JSON persistence boundary for reference deployments."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .errors import VIALStateError, VIALValidationError


class JsonRepository:
    """Persist JSON records with replace-based atomic writes."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, value: Any) -> Path:
        if not name or Path(name).name != name or not name.endswith(".json"):
            raise VIALValidationError(
                "INVALID_RECORD_NAME", "name must be a single .json filename")
        destination = self.root / name
        fd, temporary = tempfile.mkstemp(dir=self.root, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(value, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, destination)
        except Exception:
            if os.path.exists(temporary):
                os.unlink(temporary)
            raise
        return destination

    def load(self, name: str) -> Any:
        path = self.root / name
        if not path.exists():
            raise VIALStateError(
                "RECORD_NOT_FOUND", f"record '{name}' does not exist")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise VIALStateError(
                "RECORD_INVALID", f"record '{name}' cannot be loaded") from exc
