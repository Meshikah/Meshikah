# 04 · `mshkh` CLI: minimum viable tool

**Status: proposed. Not implemented.** Each item below is a contract to build and test.

## Purpose

`mshkh` turns the runtime contracts into repeatable commands that a human, CI or an agent binding can call. It governs agents; it is not one, and it makes no AI calls.

## Design rules

1. **Preview first.** Every write command shows what it would do and writes only with `--apply`.
2. **Never overwrite.** It creates missing files only. A second run reports everything as skipped.
3. **No side effects outside the repository.** No network, no deployments, no Git writes.
4. **Files are the database.** Deleting the tool leaves a fully readable repository.
5. **Human decisions are structurally separate.** `decide` needs an interactive terminal and a typed confirmation, and refuses agent environments.
6. **Machine-friendly.** Every command supports `--json` and has stable exit codes.

## MVP commands

| Command | Does | Writes |
|---|---|---|
| `mshkh init` | Creates `library/index.md`, `work/`, `archive/` and `MESHIKAH.md` if missing | Starter files |
| `mshkh new <KEY> --title "…" --level Standard` | Creates a work card from the templates | `work/<KEY>/` |
| `mshkh lint [<KEY>]` | Checks the card's files, `context.json`, links, record chain, and instruction budgets | Nothing |
| `mshkh request <KEY> <checkpoint>` | Records that a checkpoint is ready for a human | `record.jsonl` |
| `mshkh decide <KEY> <checkpoint> --approve/--reject --by "<name>"` | Records a human decision | `record.jsonl` |
| `mshkh status [<KEY>]` | Shows the level, checkpoints, last event, and any blocked or overdue items | Nothing |

Later, not in the MVP: `promote` (draft a library promotion), `archive`, `metrics`, `policy` (allow/ask/deny answers for binding hooks), and a read-only MCP server.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | A blocking check failed |
| 2 | Invalid input |
| 3 | Not a MeshikahAI repository |
| 4 | Checkpoint order or evidence missing |
| 5 | Record inconsistent |
| 6 | Sensitive data detected |
| 7 | Human-only command in a non-human context |

## Definition of done for the MVP

| # | Test | Expected |
|---|---|---|
| 1 | `new` outside a repository | Exit 3, nothing written |
| 2 | `new` without `--apply` | Nothing written; prints the plan |
| 3 | `new` twice | Second run skips every file; user edits intact |
| 4 | Invalid key | Exit 2 |
| 5 | `decide` with `MESHIKAH_AGENT=1` set or no terminal | Exit 7; record unchanged |
| 6 | `decide Accept` before `Review` is approved | Exit 4 |
| 7 | A hand-edited record line | `lint` exits 5 |
| 8 | A token-like string in a card | `lint` exits 6, without printing the value |
| 9 | Windows and Linux | All tests pass on both |

## Open decisions

- Implementation language and packaging (single binary vs. a package manager install).
- License model if commercialized.
- Which sensitive-data patterns ship by default.
