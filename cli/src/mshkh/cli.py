"""Command-line entry point. MVP commands: init, new, lint, request, decide, status.

Implemented in 0.2: init, new, lint (card MSH-2). request, decide and status keep only
their guards until 0.3 (repository discovery, key validation, the human-only guard on `decide`).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from mshkh import __version__
from mshkh.exitcodes import Exit
from mshkh import lint as lint_mod
from mshkh.init import plan_init
from mshkh.new import NewError, plan_card, write_files
from mshkh.repo import find_repo

CHECKPOINTS = ["Scope", "Plan", "Review", "Accept", "Release", "Learn"]
LEVELS = ["Light", "Standard", "Heavy", "Critical"]
DATA_CLASSES = ["Public", "Internal", "Confidential", "Regulated"]


def _emit(args: argparse.Namespace, code: Exit, message: str, **extra) -> int:
    if getattr(args, "json", False):
        print(json.dumps({"exit": int(code), "status": code.name.lower(), "message": message, **extra}))
    else:
        stream = sys.stdout if code == Exit.OK else sys.stderr
        print(message, file=stream)
    return int(code)


def _require_repo(args: argparse.Namespace):
    repo = find_repo(Path(args.repo) if args.repo else Path.cwd())
    if repo is None:
        return None, _emit(args, Exit.NOT_A_REPOSITORY, "Not a MeshikahAI repository (no meshikah.yaml, or library/index.md + work/). Nothing written.")
    return repo, None


def _not_implemented(args: argparse.Namespace, name: str) -> int:
    return _emit(args, Exit.NOT_IMPLEMENTED, f"mshkh {name}: not implemented (see docs/04-cli-mvp.md and ROADMAP.md).")


def _is_human_context() -> bool:
    if os.environ.get("MESHIKAH_AGENT") == "1":
        return False
    return sys.stdin is not None and sys.stdin.isatty()


def _report_writes(args, results, notices, summary: str) -> int:
    if getattr(args, "json", False):
        return _emit(args, Exit.OK, summary, files=[{"status": s, "path": p} for s, p in results], notices=notices)
    for note in notices:
        print(f"NOTE    {note}")
    for status, path in results:
        print(f"{status:<14}{path}")
    print(summary)
    return int(Exit.OK)


def _counts(results, apply: bool) -> str:
    skipped = sum(1 for s, _ in results if s.startswith("SKIP"))
    if apply:
        created = sum(1 for s, _ in results if s == "CREATE")
        return f"applied: {created} created, {skipped} skipped"
    would = sum(1 for s, _ in results if s == "WOULD CREATE")
    return f"preview (use --apply to write): {would} would be created, {skipped} skipped"


def cmd_init(args):
    root = (Path(args.repo) if args.repo else Path.cwd()).resolve()
    if not root.is_dir():
        return _emit(args, Exit.INVALID_INPUT, f"Target folder does not exist: {root}. Nothing written.")
    config = {}
    if (root / "meshikah.yaml").is_file():
        import yaml
        config = yaml.safe_load((root / "meshikah.yaml").read_text(encoding="utf-8")) or {}
    files, notices = plan_init(root, config, args.with_config)
    results = write_files(root, files, args.apply)
    return _report_writes(args, results, notices, f"init {_counts(results, args.apply)}, root {root}")


def cmd_new(args):
    repo, err = _require_repo(args)
    if err is not None:
        return err
    if not repo.valid_key(args.key):
        return _emit(args, Exit.INVALID_INPUT, f"Invalid key '{args.key}' (pattern {repo.key_pattern}). Nothing written.")
    try:
        files, notices, level, data_class = plan_card(repo, args.key, args.title, args.level, args.data_class, args.type)
    except NewError as exc:
        return _emit(args, Exit.INVALID_INPUT, f"{exc} Nothing written.")
    results = write_files(repo.root, files, args.apply)
    return _report_writes(args, results, notices, f"new {args.key} ({level}, {data_class}) {_counts(results, args.apply)}")


def cmd_lint(args):
    repo, err = _require_repo(args)
    if err is not None:
        return err
    if args.key and not repo.valid_key(args.key):
        return _emit(args, Exit.INVALID_INPUT, f"Invalid key '{args.key}'.")
    unknown = set(args.only or []) - set(lint_mod.ALL_CHECKS)
    if unknown:
        return _emit(args, Exit.INVALID_INPUT, f"Unknown check(s): {', '.join(sorted(unknown))}. Known: {', '.join(lint_mod.ALL_CHECKS)}.")
    findings = lint_mod.Linter(repo, args.only).run(args.key)
    code = lint_mod.exit_code(findings)
    blocking = sum(1 for f in findings if f.blocking)
    summary = f"lint: {blocking} blocking, {len(findings) - blocking} advisory"
    if args.changed_only:
        summary += " (--changed-only not implemented yet: checked everything)"
    if getattr(args, "json", False):
        print(json.dumps({"exit": int(code), "status": code.name.lower(), "message": summary,
                          "findings": lint_mod.as_dicts(findings)}))
        return int(code)
    for f in findings:
        where = f"{f.path}:{f.line}" if f.line else f.path
        print(f"{'BLOCK' if f.blocking else 'WARN ':<5} {f.check:<12} {where}  {f.message}")
    print(summary)
    return int(code)


def cmd_request(args):
    repo, err = _require_repo(args)
    if err is not None:
        return err
    if not repo.valid_key(args.key):
        return _emit(args, Exit.INVALID_INPUT, f"Invalid key '{args.key}'.")
    return _not_implemented(args, "request")


def cmd_decide(args):
    if not _is_human_context():
        return _emit(args, Exit.HUMAN_ONLY, "mshkh decide is human-only: refused (MESHIKAH_AGENT=1 or no interactive terminal). Record unchanged.")
    repo, err = _require_repo(args)
    if err is not None:
        return err
    if not repo.valid_key(args.key):
        return _emit(args, Exit.INVALID_INPUT, f"Invalid key '{args.key}'.")
    return _not_implemented(args, "decide")


def cmd_status(args):
    repo, err = _require_repo(args)
    if err is not None:
        return err
    if args.key and not repo.valid_key(args.key):
        return _emit(args, Exit.INVALID_INPUT, f"Invalid key '{args.key}'.")
    return _not_implemented(args, "status")


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", help="Repository root (skips discovery)")
    common.add_argument("--json", action="store_true", help="Machine-readable output")
    common.add_argument("--apply", action="store_true", help="Perform writes (default: preview only)")

    p = argparse.ArgumentParser(prog="mshkh", description="MeshikahAI CLI. Governs agents; is not one.")
    p.add_argument("--version", action="version", version=f"mshkh {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("init", parents=[common], help="Create the library skeleton and MESHIKAH.md if missing")
    s.add_argument("--with-config", action="store_true")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("new", parents=[common], help="Create a work card from the templates")
    s.add_argument("key")
    s.add_argument("--title", required=True)
    s.add_argument("--level", choices=LEVELS, required=True)
    s.add_argument("--data-class", choices=DATA_CLASSES)
    s.add_argument("--type", default="story")
    s.set_defaults(func=cmd_new)

    s = sub.add_parser("lint", parents=[common], help="Check cards, context.json, links, record chain, budgets")
    s.add_argument("key", nargs="?")
    s.add_argument("--only", nargs="+")
    s.add_argument("--changed-only", action="store_true")
    s.set_defaults(func=cmd_lint)

    s = sub.add_parser("request", parents=[common], help="Record that a checkpoint is ready for a human")
    s.add_argument("key")
    s.add_argument("checkpoint", choices=CHECKPOINTS)
    s.add_argument("--evidence", nargs="*", default=[])
    s.set_defaults(func=cmd_request)

    s = sub.add_parser("decide", parents=[common], help="Record a human decision (human-only)")
    s.add_argument("key")
    s.add_argument("checkpoint", choices=CHECKPOINTS + ["level"])
    group = s.add_mutually_exclusive_group(required=True)
    group.add_argument("--approve", action="store_true")
    group.add_argument("--reject", action="store_true")
    group.add_argument("--changes-requested", action="store_true")
    group.add_argument("--set", choices=LEVELS, help="With 'level': confirm the card's level")
    s.add_argument("--by", required=True)
    s.add_argument("--aspect", choices=["security", "second-human"])
    s.add_argument("--control")
    s.add_argument("--pattern")
    s.set_defaults(func=cmd_decide)

    s = sub.add_parser("status", parents=[common], help="Show level, checkpoints and last event")
    s.add_argument("key", nargs="?")
    s.add_argument("--overdue", action="store_true")
    s.set_defaults(func=cmd_status)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse uses 2 for usage errors, matching Exit.INVALID_INPUT
        return int(exc.code or 0)
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover - last-resort guard
        print(f"mshkh internal error: {exc}", file=sys.stderr)
        return int(Exit.INTERNAL_ERROR)
