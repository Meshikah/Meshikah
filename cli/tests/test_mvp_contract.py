"""MVP definition-of-done tests (docs/04-cli-mvp.md). Pending tests are xfail until implemented."""

from pathlib import Path

import pytest

from mshkh.cli import main
from mshkh.exitcodes import Exit


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "meshikah.yaml").write_text("version: 1\n", encoding="utf-8")
    (tmp_path / "library").mkdir()
    (tmp_path / "library" / "index.md").write_text("# Index\n", encoding="utf-8")
    (tmp_path / "work").mkdir()
    return tmp_path


def snapshot(root: Path) -> set[str]:
    return {str(p.relative_to(root)) for p in root.rglob("*")}


def test_1_new_outside_repository_exits_3_and_writes_nothing(tmp_path):
    before = snapshot(tmp_path)
    code = main(["new", "ABC-1", "--title", "x", "--level", "Light", "--repo", str(tmp_path), "--apply"])
    assert code == Exit.NOT_A_REPOSITORY
    assert snapshot(tmp_path) == before


@pytest.mark.xfail(reason="mshkh new not implemented (roadmap 0.2)", strict=True)
def test_2_new_without_apply_writes_nothing_and_prints_plan(repo, capsys):
    before = snapshot(repo)
    code = main(["new", "ABC-1", "--title", "x", "--level", "Light", "--repo", str(repo)])
    assert code == Exit.OK
    assert snapshot(repo) == before
    assert "WOULD CREATE" in capsys.readouterr().out


@pytest.mark.xfail(reason="mshkh new not implemented (roadmap 0.2)", strict=True)
def test_3_new_twice_skips_and_keeps_edits(repo):
    assert main(["new", "ABC-1", "--title", "x", "--level", "Light", "--repo", str(repo), "--apply"]) == Exit.OK
    card = repo / "work" / "ABC-1" / "card.md"
    card.write_text("edited", encoding="utf-8")
    assert main(["new", "ABC-1", "--title", "x", "--level", "Light", "--repo", str(repo), "--apply"]) == Exit.OK
    assert card.read_text(encoding="utf-8") == "edited"


def test_4_invalid_key_exits_2(repo):
    assert main(["new", "abc_1", "--title", "x", "--level", "Light", "--repo", str(repo), "--apply"]) == Exit.INVALID_INPUT


def test_5_decide_refused_in_agent_environment(repo, monkeypatch):
    monkeypatch.setenv("MESHIKAH_AGENT", "1")
    code = main(["decide", "ABC-1", "Review", "--approve", "--by", "someone", "--repo", str(repo)])
    assert code == Exit.HUMAN_ONLY


@pytest.mark.xfail(reason="checkpoint order not implemented (roadmap 0.3)", strict=True)
def test_6_accept_before_review_exits_4(repo):
    assert main(["decide", "ABC-1", "Accept", "--approve", "--by", "someone", "--repo", str(repo)]) == Exit.CHECKPOINT_ORDER_OR_EVIDENCE


@pytest.mark.xfail(reason="mshkh lint not implemented (roadmap 0.2)", strict=True)
def test_7_hand_edited_record_line_exits_5(repo):
    assert main(["lint", "--repo", str(repo)]) == Exit.RECORD_INCONSISTENT


@pytest.mark.xfail(reason="mshkh lint not implemented (roadmap 0.2)", strict=True)
def test_8_token_like_string_exits_6(repo):
    assert main(["lint", "--repo", str(repo)]) == Exit.SENSITIVE_DATA


# Test 9 (Windows and Linux) is the CI matrix in .github/workflows/ci.yml.
