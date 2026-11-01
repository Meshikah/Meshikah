"""`mshkh new`: create a work card from templates (docs/04-cli-mvp.md; reference CLI spec §5.2).

Preview by default; writes only with --apply; never overwrites.
"""

from __future__ import annotations

import getpass
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import yaml

from mshkh import record, templates
from mshkh.repo import Repo

LEVEL_ORDER = ["Light", "Standard", "Heavy", "Critical"]
FLOOR = {"Regulated": "Critical", "Confidential": "Standard"}


class NewError(Exception):
    """Invalid input: maps to exit 2."""


def load_pack(repo: Repo) -> dict:
    name = repo.config.get("pack")
    if not name:
        return {}
    pack_file = repo.root / "packs" / name / "pack.yaml"
    if pack_file.is_file():
        return yaml.safe_load(pack_file.read_text(encoding="utf-8")) or {}
    return {"name": name}


def resolve_data_class(repo: Repo, pack: dict, requested: str | None) -> str:
    data_class = requested or pack.get("default_data_class") or "Internal"
    declared = repo.config.get("data_classes")
    if declared and data_class not in declared:
        raise NewError(f"Data class {data_class} is not declared in meshikah.yaml (declared: {', '.join(declared)}).")
    allowed = pack.get("allowed_data_classes")
    if allowed and data_class not in allowed:
        raise NewError(f"Data class {data_class} is not allowed by pack {pack.get('name')} (allowed: {', '.join(allowed)}).")
    return data_class


def apply_floor(level: str, data_class: str) -> tuple[str, str | None]:
    floor = FLOOR.get(data_class)
    if floor and LEVEL_ORDER.index(level) < LEVEL_ORDER.index(floor):
        return floor, f"Level raised from {level} to {floor}: {data_class} data sets that floor (Model §5.1)."
    return level, None


def template_text(repo: Repo, pack: dict, role: str, builtin: str) -> str:
    pack_templates = pack.get("templates") or {}
    if role in pack_templates:
        candidate = repo.root / pack_templates[role]
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    kernel_name = {"card": "card.md", "plan": "plan.md", "evidence": "evidence.md", "context": "context.json"}.get(role)
    if kernel_name:
        candidate = repo.root / "templates" / "work-card" / kernel_name
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    return builtin


def render(text: str, tokens: dict[str, str], json_file: bool = False) -> str:
    for token, value in tokens.items():
        if json_file:
            value = json.dumps(value)[1:-1]  # escape for a JSON string body
        text = text.replace(token, value)
    return text


def actor() -> str:
    if os.environ.get("MESHIKAH_AGENT") == "1":
        return "agent:builder"
    try:
        name = getpass.getuser()
    except Exception:  # pragma: no cover - unusual environments
        name = "unknown"
    return f"human:{name or 'unknown'}"


def plan_card(repo: Repo, key: str, title: str, level: str, data_class: str | None, card_type: str):
    """Return (files, notices, final_level, data_class). files: list of (relative path, content bytes)."""
    if (repo.config.get("profile") or "native") != "native":
        raise NewError(f"Profile {repo.config.get('profile')!r} is not supported by mshkh 0.2 (native only).")
    pack = load_pack(repo)
    data_class = resolve_data_class(repo, pack, data_class)
    final_level, notice = apply_floor(level, data_class)
    tokens = {
        "{{KEY}}": key, "{{TITLE}}": title, "{{LEVEL}}": final_level,
        "{{DATA_CLASS}}": data_class, "{{INDEX}}": repo.paths["index"],
    }
    card_dir = Path(repo.paths["work"]) / key
    context_text = render(template_text(repo, pack, "context", templates.CONTEXT), tokens, json_file=True)
    context = json.loads(context_text)
    context.update({"key": key, "title": title, "level": final_level, "data_class": data_class})
    opened = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "card": key, "event": "opened", "by": actor(), "level": final_level,
        "text": f"Opened as {card_type}; level proposed, awaiting human confirmation.",
    }
    files = [
        (card_dir / "card.md", render(template_text(repo, pack, "card", templates.CARD), tokens).encode("utf-8")),
        (card_dir / "plan.md", render(template_text(repo, pack, "plan", templates.PLAN), tokens).encode("utf-8")),
        (card_dir / "context.json", (json.dumps(context, indent=2, ensure_ascii=False) + "\n").encode("utf-8")),
        (card_dir / "evidence.md", render(template_text(repo, pack, "evidence", templates.EVIDENCE), tokens).encode("utf-8")),
        (card_dir / "notes" / "README.md", render(templates.NOTES, tokens).encode("utf-8")),
        (card_dir / "record.jsonl", record.first_line(opened)),
    ]
    return files, [n for n in [notice] if n], final_level, data_class


def write_files(root: Path, files, apply: bool) -> list[tuple[str, str]]:
    """Create missing files only. Returns (status, relative path) pairs."""
    results = []
    for rel, content in files:
        target = root / rel
        if target.exists():
            results.append(("SKIP (exists)", rel.as_posix()))
            continue
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as handle:  # 'x' refuses to overwrite even under a race
                handle.write(content)
            results.append(("CREATE", rel.as_posix()))
        else:
            results.append(("WOULD CREATE", rel.as_posix()))
    return results
