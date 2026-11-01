# `mshkh` CLI (skeleton)

Contract: [`docs/04-cli-mvp.md`](../docs/04-cli-mvp.md) and the full spec [`docs/reference/MeshikahOS_cli_technical_spec.md`](../docs/reference/MeshikahOS_cli_technical_spec.md).

**Status:** argument parsing, exit codes and three guards are in place. No command performs its work yet.

| Guard | MVP test | Implemented |
|---|---|---|
| Outside a MeshikahAI repository → exit 3, nothing written | 1 | ✓ |
| Invalid card key → exit 2 | 4 | ✓ |
| `decide` with `MESHIKAH_AGENT=1` or no terminal → exit 7 | 5 | ✓ |
| Everything else | 2, 3, 6, 7, 8, 9 | Pending (roadmap 0.2–0.3) |

Commands that pass their guards print `not implemented` and exit `69`.

## Develop

```bash
cd cli
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest
mshkh --help
```
