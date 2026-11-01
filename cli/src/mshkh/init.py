"""`mshkh init`: create the library skeleton and MESHIKAH.md if missing (docs/04-cli-mvp.md).

Preview by default; writes only with --apply; never overwrites; never touches Git.
"""

from __future__ import annotations

from pathlib import Path

from mshkh import templates
from mshkh.repo import DEFAULTS


def plan_init(root: Path, config: dict, with_config: bool):
    paths = dict(DEFAULTS)
    paths.update(config.get("paths") or {})
    library = Path(paths["library"])
    files = [
        (Path(paths["index"]), templates.INDEX.encode("utf-8")),
        (library / "lessons.md", templates.LESSONS.encode("utf-8")),
        (Path(paths["work"]) / ".gitkeep", b""),
        (Path(paths["archive"]) / ".gitkeep", b""),
        (Path("MESHIKAH.md"), templates.MESHIKAH.encode("utf-8")),
    ]
    if with_config:
        files.append((Path("meshikah.yaml"), templates.CONFIG.encode("utf-8")))
    notes = []
    if (root / paths["work"]).is_dir() and any((root / paths["work"]).iterdir()):
        notes.append(f"{paths['work']}/ already has content; only missing files are created.")
    return files, notes
