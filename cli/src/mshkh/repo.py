"""Repository discovery (reference OS §3.1–§3.2). Read-only."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULT_KEY_PATTERN = r"^[A-Z][A-Z0-9]+-\d+$"
DEFAULTS = {"library": "library", "work": "work", "archive": "archive", "index": "library/index.md"}


@dataclass
class Repo:
    root: Path
    config: dict = field(default_factory=dict)

    @property
    def paths(self) -> dict:
        merged = dict(DEFAULTS)
        merged.update((self.config.get("paths") or {}))
        return merged

    @property
    def key_pattern(self) -> str:
        return self.config.get("key_pattern", DEFAULT_KEY_PATTERN)

    def valid_key(self, key: str) -> bool:
        return re.fullmatch(self.key_pattern.strip("^$"), key) is not None


def find_repo(start: Path) -> Repo | None:
    """Nearest ancestor with meshikah.yaml, or with both the default index and work directory."""
    start = start.resolve()
    for candidate in [start, *start.parents]:
        cfg_file = candidate / "meshikah.yaml"
        if cfg_file.is_file():
            config = yaml.safe_load(cfg_file.read_text(encoding="utf-8")) or {}
            return Repo(candidate, config)
        if (candidate / DEFAULTS["index"]).is_file() and (candidate / DEFAULTS["work"]).is_dir():
            return Repo(candidate, {})
    return None
