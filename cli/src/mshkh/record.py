"""Record helpers (reference OS §4.3): read, verify and append hash-chained events."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

EVENTS = {"opened", "requested", "note", "blocked", "unblocked", "level_confirmed", "decided", "released", "correction"}
HUMAN_ONLY = {"level_confirmed", "decided", "released", "correction"}


def line_hash(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


@dataclass
class RecordProblem:
    line: int
    message: str


def read_lines(path: Path) -> list[bytes]:
    return [line for line in path.read_bytes().split(b"\n") if line.strip()]


def verify(path: Path, card_key: str | None = None) -> list[RecordProblem]:
    """Check JSON, the hash chain, event names, card key and human-only actors."""
    problems: list[RecordProblem] = []
    prev = None
    for number, raw in enumerate(read_lines(path), start=1):
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            problems.append(RecordProblem(number, "not valid JSON"))
            prev = line_hash(raw)
            continue
        if event.get("prev") != prev:
            problems.append(RecordProblem(number, "hash chain broken (prev does not match the previous line)"))
        if event.get("event") not in EVENTS:
            problems.append(RecordProblem(number, f"unknown event {event.get('event')!r}"))
        if card_key and event.get("card") != card_key:
            problems.append(RecordProblem(number, f"card {event.get('card')!r} does not match folder {card_key!r}"))
        by = str(event.get("by", ""))
        if not (by.startswith("human:") or by.startswith("agent:")):
            problems.append(RecordProblem(number, "actor must be human:<name> or agent:<role>"))
        if event.get("event") in HUMAN_ONLY and not by.startswith("human:"):
            problems.append(RecordProblem(number, f"{event.get('event')} is human-only but actor is {by!r}"))
        if event.get("event") == "released":
            missing = [k for k in ("spec_version", "deployed_ref", "deployment_id") if not event.get(k)]
            if missing:
                problems.append(RecordProblem(number, "released event missing " + ", ".join(missing)))
        prev = line_hash(raw)
    return problems


def encode(event: dict) -> bytes:
    return json.dumps(event, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def first_line(event: dict) -> bytes:
    """The opening line of a new record: prev is null."""
    return encode({**event, "prev": None}) + b"\n"


def append(path: Path, event: dict) -> None:
    lines = read_lines(path) if path.exists() else []
    event = {**event, "prev": line_hash(lines[-1]) if lines else None}
    raw = path.read_bytes() if path.exists() else b""
    with path.open("ab") as handle:
        if raw and not raw.endswith(b"\n"):
            handle.write(b"\n")
        handle.write(encode(event) + b"\n")
