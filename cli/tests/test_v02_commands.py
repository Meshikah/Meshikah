"""Extra tests for mshkh 0.2 (card MSH-2): init, new, lint."""

import json
from pathlib import Path

import pytest

from mshkh.cli import main
from mshkh.exitcodes import Exit


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "meshikah.yaml").write_text(
        "version: 1\ndata_classes: [Public, Internal, Confidential, Regulated]\n", encoding="utf-8")
    (tmp_path / "library").mkdir()
    (tmp_path / "library" / "index.md").write_text("# Index\n", encoding="utf-8")
    (tmp_path / "work").mkdir()
    return tmp_path


def files(root: Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def test_init_preview_then_apply_then_skip(tmp_path, capsys):
    assert main(["init", "--repo", str(tmp_path)]) == Exit.OK
    assert files(tmp_path) == set()
    assert main(["init", "--repo", str(tmp_path), "--with-config", "--apply"]) == Exit.OK
    created = files(tmp_path)
    assert {"MESHIKAH.md", "meshikah.yaml", "library/index.md", "library/lessons.md", "work/.gitkeep", "archive/.gitkeep"} <= created
    (tmp_path / "MESHIKAH.md").write_text("edited", encoding="utf-8")
    capsys.readouterr()
    assert main(["init", "--repo", str(tmp_path), "--apply"]) == Exit.OK
    assert (tmp_path / "MESHIKAH.md").read_text(encoding="utf-8") == "edited"
    assert "CREATE" not in capsys.readouterr().out


def test_init_then_new_then_lint_is_clean(tmp_path):
    assert main(["init", "--repo", str(tmp_path), "--with-config", "--apply"]) == Exit.OK
    assert main(["new", "ABC-7", "--title", "First card", "--level", "Standard", "--repo", str(tmp_path), "--apply"]) == Exit.OK
    assert main(["lint", "--repo", str(tmp_path), "--only", "context", "links", "record", "sensitive"]) == Exit.OK


def test_new_creates_card_files_and_opened_event(repo):
    assert main(["new", "ABC-2", "--title", 'Quote "and" backslash \\ test', "--level", "Standard",
                 "--repo", str(repo), "--apply"]) == Exit.OK
    card = repo / "work" / "ABC-2"
    assert {"card.md", "plan.md", "context.json", "evidence.md", "record.jsonl", "notes/README.md"} == {
        p.relative_to(card).as_posix() for p in card.rglob("*") if p.is_file()}
    ctx = json.loads((card / "context.json").read_text(encoding="utf-8"))
    assert ctx["key"] == "ABC-2" and ctx["title"] == 'Quote "and" backslash \\ test' and ctx["level"] == "Standard"
    event = json.loads((card / "record.jsonl").read_text(encoding="utf-8"))
    assert event["event"] == "opened" and event["prev"] is None and event["card"] == "ABC-2"


def test_new_regulated_raises_level_to_critical(repo, capsys):
    assert main(["new", "ABC-3", "--title", "x", "--level", "Light", "--data-class", "Regulated",
                 "--repo", str(repo), "--apply"]) == Exit.OK
    assert "raised from Light to Critical" in capsys.readouterr().out
    ctx = json.loads((repo / "work" / "ABC-3" / "context.json").read_text(encoding="utf-8"))
    assert ctx["level"] == "Critical" and ctx["data_class"] == "Regulated"


def test_new_confidential_raises_light_to_standard(repo):
    assert main(["new", "ABC-4", "--title", "x", "--level", "Light", "--data-class", "Confidential",
                 "--repo", str(repo), "--apply"]) == Exit.OK
    assert json.loads((repo / "work" / "ABC-4" / "context.json").read_text(encoding="utf-8"))["level"] == "Standard"


def test_new_undeclared_data_class_exits_2(tmp_path):
    (tmp_path / "meshikah.yaml").write_text("version: 1\ndata_classes: [Public, Internal]\n", encoding="utf-8")
    (tmp_path / "library").mkdir(); (tmp_path / "library" / "index.md").write_text("# I\n", encoding="utf-8")
    (tmp_path / "work").mkdir()
    before = files(tmp_path)
    assert main(["new", "ABC-5", "--title", "x", "--level", "Light", "--data-class", "Regulated",
                 "--repo", str(tmp_path), "--apply"]) == Exit.INVALID_INPUT
    assert files(tmp_path) == before


def test_new_marks_agent_actor(repo, monkeypatch):
    monkeypatch.setenv("MESHIKAH_AGENT", "1")
    assert main(["new", "ABC-6", "--title", "x", "--level", "Light", "--repo", str(repo), "--apply"]) == Exit.OK
    assert json.loads((repo / "work" / "ABC-6" / "record.jsonl").read_text(encoding="utf-8"))["by"] == "agent:builder"


def test_lint_flags_archive_reference_and_broken_link(repo):
    assert main(["new", "ABC-8", "--title", "x", "--level", "Light", "--repo", str(repo), "--apply"]) == Exit.OK
    ctx_path = repo / "work" / "ABC-8" / "context.json"
    ctx = json.loads(ctx_path.read_text(encoding="utf-8"))
    ctx["may_change"] = ["archive/old.md"]
    ctx_path.write_text(json.dumps(ctx), encoding="utf-8")
    with (repo / "work" / "ABC-8" / "card.md").open("a", encoding="utf-8") as fh:
        fh.write("\nSee [missing](nowhere.md)\n")
    assert main(["lint", "--repo", str(repo), "--json"]) == Exit.BLOCKING_CHECK_FAILED


def test_lint_human_only_event_by_agent_exits_5(repo):
    assert main(["new", "ABC-9", "--title", "x", "--level", "Light", "--repo", str(repo), "--apply"]) == Exit.OK
    from mshkh import record
    record.append(repo / "work" / "ABC-9" / "record.jsonl",
                  {"at": "2026-11-01T00:00:00Z", "card": "ABC-9", "event": "decided", "checkpoint": "Review",
                   "decision": "approved", "by": "agent:builder"})
    assert main(["lint", "--repo", str(repo)]) == Exit.RECORD_INCONSISTENT


@pytest.mark.parametrize("line,expected", [
    ("contact me at someone@realmail.com", "email address"),
    ("card 4111 1111 1111 1111", "payment card number"),
    ("clabe 012180001234567891", "CLABE"),
    ("password = hunter2hunter2hunter2", "credential assignment"),
])
def test_sensitive_patterns(line, expected):
    from mshkh.sensitive import scan_line
    assert expected in scan_line(line)


@pytest.mark.parametrize("line", [
    "Date 2026-11-01, commit 35e7f72, 12 passed, 5 xfailed",
    "sha256:441e1fe40f9b75cd4d9c92595fd504161a51ae842847e30d2d468335acf9d4e0",
    "author 157664195+Meshikah@users.noreply.github.com",
])
def test_sensitive_ignores_ordinary_text(line):
    from mshkh.sensitive import scan_line
    assert scan_line(line) == []


def test_lint_unknown_check_exits_2(repo):
    assert main(["lint", "--repo", str(repo), "--only", "nope"]) == Exit.INVALID_INPUT
