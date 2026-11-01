"""`mshkh lint`: structural checks (docs/04-cli-mvp.md; reference OS §7.1). Writes nothing."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from mshkh import record, sensitive
from mshkh.exitcodes import Exit
from mshkh.repo import Repo

ALL_CHECKS = ["card-files", "acceptance", "context", "archive-refs", "links", "record", "sensitive", "budget"]
DEFAULT_BLOCKING = ["context", "links", "record", "sensitive"]
CARD_FILES = ["card.md", "plan.md", "context.json", "evidence.md", "record.jsonl"]
LEVELS = {"Light", "Standard", "Heavy", "Critical"}
DATA_CLASSES = {"Public", "Internal", "Confidential", "Regulated"}
REQUIRED_CONTEXT = ["key", "title", "level", "data_class", "library", "source", "may_change", "tests"]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADER = re.compile(r"owner:\s*(?P<owner>[^·]+?)\s*·\s*review by:\s*(?P<review>\S+)\s*·\s*budget:\s*(?P<budget>\d+)\s*lines")
TEXT_SUFFIXES = {".md", ".json", ".txt", ".yaml", ".yml", ".csv"}


@dataclass
class Finding:
    check: str
    path: str
    line: int | None
    message: str
    blocking: bool = False


class Linter:
    def __init__(self, repo: Repo, only: list[str] | None = None):
        self.repo = repo
        self.root = repo.root
        cfg = repo.config.get("checks") or {}
        self.blocking = set(cfg.get("blocking") or DEFAULT_BLOCKING)
        self.enabled = set(only or ALL_CHECKS)
        self.findings: list[Finding] = []

    # -- helpers -------------------------------------------------------------
    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    def add(self, check: str, path: Path, line: int | None, message: str) -> None:
        if check in self.enabled:
            self.findings.append(Finding(check, self.rel(path), line, message, check in self.blocking))

    def cards(self, key: str | None) -> list[Path]:
        work = self.root / self.repo.paths["work"]
        if not work.is_dir():
            return []
        if key:
            return [work / key]
        return sorted(p for p in work.iterdir() if p.is_dir() and not p.name.startswith("."))

    # -- card checks -----------------------------------------------------------
    def check_card(self, card: Path) -> None:
        if not card.is_dir():
            self.add("card-files", card, None, "card folder does not exist")
            return
        for name in CARD_FILES:
            if not (card / name).is_file():
                self.add("card-files", card / name, None, "missing")
        self.check_acceptance(card / "card.md")
        self.check_context(card)
        for name in ("card.md", "plan.md"):
            self.check_links(card / name)
        if (card / "record.jsonl").is_file():
            for problem in record.verify(card / "record.jsonl", card.name):
                self.add("record", card / "record.jsonl", problem.line, problem.message)
        self.check_sensitive(card)

    def check_acceptance(self, card_md: Path) -> None:
        if not card_md.is_file():
            return
        text = card_md.read_text(encoding="utf-8")
        match = re.search(r"^## Acceptance\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not match:
            self.add("acceptance", card_md, None, "no '## Acceptance' section")
            return
        body = match.group(1)
        if not re.search(r"^### ", body, re.M):
            self.add("acceptance", card_md, None, "no numbered criteria ('### 1. ...')")
        for word in ("GIVEN", "WHEN", "THEN"):
            if not re.search(rf"^\s*-\s*{word}\b", body, re.M):
                self.add("acceptance", card_md, None, f"no {word} line in acceptance")

    def check_context(self, card: Path) -> None:
        path = card / "context.json"
        if not path.is_file():
            return
        try:
            ctx = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.add("context", path, exc.lineno, "not valid JSON")
            return
        if not isinstance(ctx, dict):
            self.add("context", path, None, "must be a JSON object")
            return
        for field in REQUIRED_CONTEXT:
            if field not in ctx:
                self.add("context", path, None, f"missing field '{field}'")
        unknown = set(ctx) - set(REQUIRED_CONTEXT) - {"retrieve"}
        if unknown:
            self.add("context", path, None, "unknown fields: " + ", ".join(sorted(unknown)))
        if ctx.get("key") is not None and ctx.get("key") != card.name:
            self.add("context", path, None, f"key {ctx.get('key')!r} does not match folder {card.name!r}")
        if "level" in ctx and ctx["level"] not in LEVELS:
            self.add("context", path, None, f"invalid level {ctx['level']!r}")
        if "data_class" in ctx:
            declared = self.repo.config.get("data_classes")
            if ctx["data_class"] not in DATA_CLASSES:
                self.add("context", path, None, f"invalid data_class {ctx['data_class']!r}")
            elif declared and ctx["data_class"] not in declared:
                self.add("context", path, None, f"data_class {ctx['data_class']} is not declared in meshikah.yaml")
        archive = self.repo.paths["archive"].rstrip("/") + "/"
        for field in ("library", "source", "may_change"):
            values = ctx.get(field, [])
            if not isinstance(values, list):
                self.add("context", path, None, f"'{field}' must be a list")
                continue
            for value in values:
                if not isinstance(value, str) or not value:
                    self.add("context", path, None, f"'{field}' has an empty or non-string entry")
                    continue
                if value.startswith(("/", "../")) or re.match(r"^[A-Za-z]:", value):
                    self.add("context", path, None, f"'{field}' path must be repository-relative: {value}")
                    continue
                if value.startswith(archive):
                    self.add("archive-refs", path, None, f"'{field}' points into {archive}: {value}")
                is_glob = any(ch in value for ch in "*?[")
                if field != "may_change" and not is_glob and not (self.root / value).exists():
                    self.add("context", path, None, f"'{field}' path does not exist: {value}")

    def check_links(self, md: Path) -> None:
        if not md.is_file():
            return
        for number, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            for target in LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                    continue
                target_path = target.split("#", 1)[0]
                if target_path and not (md.parent / target_path).exists():
                    self.add("links", md, number, f"broken link: {target}")

    def check_sensitive(self, card: Path) -> None:
        for path in sorted(card.rglob("*")):
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES | {".jsonl"}:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            for number, line in enumerate(lines, start=1):
                if path.suffix == ".jsonl":
                    try:
                        line = str(json.loads(line).get("text", ""))
                    except (json.JSONDecodeError, AttributeError):
                        pass
                for name in sensitive.scan_line(line):
                    self.add("sensitive", path, number, f"possible {name} (value not shown)")

    # -- repository checks -----------------------------------------------------
    def check_budget(self) -> None:
        files = self.repo.config.get("instruction_files") or ["MESHIKAH.md", "CLAUDE.md", "AGENTS.md"]
        cap = int(self.repo.config.get("instruction_budget", 150))
        for name in files:
            path = self.root / name
            if not path.is_file():
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
            header = HEADER.search(lines[0]) if lines else None
            if not header:
                self.add("budget", path, 1, "missing header: <!-- owner: … · review by: YYYY-MM-DD · budget: N lines -->")
                continue
            budget = min(int(header["budget"]), cap)
            used = sum(1 for line in lines if line.strip())
            if used > budget:
                self.add("budget", path, None, f"{used} non-empty lines, over the budget of {budget}")
            try:
                if date.fromisoformat(header["review"]) < date.today():
                    self.add("budget", path, 1, f"review date {header['review']} has passed")
            except ValueError:
                self.add("budget", path, 1, f"review date {header['review']!r} is not YYYY-MM-DD")

    def run(self, key: str | None = None) -> list[Finding]:
        for card in self.cards(key):
            self.check_card(card)
        if key is None:
            self.check_budget()
            index = self.root / self.repo.paths["index"]
            if index.is_file():
                self.check_links(index)
            else:
                self.add("card-files", index, None, "library index missing")
        return self.findings


def exit_code(findings: list[Finding]) -> Exit:
    blocking = {f.check for f in findings if f.blocking}
    if "sensitive" in blocking:
        return Exit.SENSITIVE_DATA
    if "record" in blocking:
        return Exit.RECORD_INCONSISTENT
    if blocking:
        return Exit.BLOCKING_CHECK_FAILED
    return Exit.OK


def as_dicts(findings: list[Finding]) -> list[dict]:
    return [asdict(f) for f in findings]
