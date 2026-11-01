# MeshikahOS-cli Technical Specification

**Command:** `mshkh`
**Status:** Proposed. **Not implemented.** Every command is a contract to build and test.
**Version:** 0.2, aligned with the MeshikahAI package v0.1 (`docs/04-cli-mvp.md`). Supersedes CLI spec 0.1.
**Implements:** [`MeshikahAI_operating_system.md`](MeshikahAI_operating_system.md) 2.0 ("OS §n"), under the [Model](MeshikahAI_operating_model.md) 2.0 ("Model §n") and [Standard](MeshikahAI_operating_standard.md) 2.0 ("Standard §n")
**Sub-system:** 6 Toolchain & Runtime, with operating surfaces for Context (C2), Orchestration (C6), Verification (C7) and Knowledge (C10)

> **Precedence:** Standard > Model > OS > this CLI. The CLI may enforce a contract more strictly, never more loosely. If this document and the OS disagree, the OS wins.

---

## 1. Purpose

`mshkh` turns the runtime contracts into repeatable commands that a human, CI or an agent binding can call. **It governs agents; it is not one, and it makes no AI calls.**

| It does | It does not |
|---|---|
| Create the library skeleton and work cards safely | Write code or decide designs |
| Check cards, `context.json`, links, the record and instruction budgets | Grant permissions (a pointer is not a permission) |
| Record checkpoint requests, and human decisions through a separate path | Let an agent record a decision |
| Show card state derived from the record | Deploy, retrieve from orgs, or write to trackers |
| (Later) answer allow/ask/deny for binding hooks; derive metrics | Score people |

## 2. Design rules

1. **Preview first.** Every write command shows what it would do and writes only with `--apply`.
2. **Never overwrite.** It creates missing files only. A second run reports everything as skipped.
3. **No side effects outside the repository.** No network, no deployments, no Git writes.
4. **Files are the database.** Deleting the tool leaves a fully readable repository.
5. **Human decisions are structurally separate.** `decide` needs an interactive terminal and a typed confirmation, and refuses agent environments.
6. **Machine-friendly.** Every command supports `--json` and has stable exit codes.
7. **Deterministic.** The same repository state and arguments give the same result.
8. **Project conventions win.** Paths come from `meshikah.yaml` and the detected profile (OS §3.2–§3.3).

## 3. Runtime and installation

Language and packaging are an **open decision** in the package (§15). Recommendation for 0.2:

| Item | Recommendation | Why |
|---|---|---|
| Language | Python 3.11+ | Pilot validators are Python; Windows, macOS and Linux |
| Install | `pipx install mshkh`, plus a single-file zip app for locked-down laptops | No admin rights |
| Dependencies | Standard library, `pyyaml`, `jsonschema` | Small audit surface |
| Network | None | Works air-gapped |
| Encoding | UTF-8 without BOM; LF written; CRLF tolerated on read | Matches the pilot |

A compiled single binary (Go or Rust) is the alternative if enterprise laptops block Python.

## 4. Repository discovery and configuration

- The repository root is the nearest directory containing `meshikah.yaml`, or else both the library index and the work directory (OS §3.1). `--repo <path>` overrides discovery.
- Outside a root, every command exits `3` and writes nothing.
- Configuration is `meshikah.yaml` (OS §3.2). Without it, `mshkh` uses native names and auto-detects the profile, and says so in its output.

### Global flags

| Flag | Meaning |
|---|---|
| `--apply` | Perform the writes. Without it, write commands only preview. |
| `--repo <path>` | Repository root |
| `--json` | Machine-readable output on stdout; messages on stderr |
| `--quiet`, `--verbose` | Output level |
| `--no-color` | Plain output (automatic when not a terminal) |

Write commands print one line per file (`CREATE`, `SKIP (exists)`, or `WOULD CREATE`) and a summary line.

## 5. MVP commands

| Command | Does | Writes |
|---|---|---|
| `mshkh init` | Creates `library/index.md`, `work/`, `archive/` and `MESHIKAH.md` if missing | Starter files |
| `mshkh new <KEY> --title "…" --level Standard` | Creates a work card from the templates | `work/<KEY>/` |
| `mshkh lint [<KEY>]` | Checks card files, `context.json`, links, record chain, instruction budgets | Nothing |
| `mshkh request <KEY> <checkpoint>` | Records that a checkpoint is ready for a human | `record.jsonl` |
| `mshkh decide <KEY> <checkpoint> --approve/--reject --by "<name>"` | Records a human decision | `record.jsonl` |
| `mshkh status [<KEY>]` | Shows level, checkpoints, last event, blocked or overdue items | Nothing |

### 5.1 `mshkh init`

```text
mshkh init [--with-config] [--apply]
```

- Creates only what is missing: the library index (listing only paths that exist), `work/`, `archive/`, `MESHIKAH.md` from the template with its owner, review-date and budget header, and `meshikah.yaml` with `--with-config` (auto-detected values filled in).
- On a repository with a Docs Hub profile it creates nothing under the mapped paths that would conflict, and reports the detected profile.
- Never renames or migrates anything.

### 5.2 `mshkh new`

```text
mshkh new <KEY> --title "<title>" --level Light|Standard|Heavy|Critical
          [--data-class Public|Internal|Confidential|Regulated] [--type story|bug|…] [--apply]
```

1. Validates `<KEY>` against `key_pattern`; exit `2` on mismatch.
2. Validates `--data-class` against the classes in `meshikah.yaml`; exit `2` if the project doesn't declare it.
3. Applies the data floor: `Regulated` raises the level to `Critical`, `Confidential` to at least `Standard`, and says so (Model §5.1).
4. Creates, per the profile: `card.md`, `plan.md`, `context.json`, `evidence.md`, `notes/`, and `record.jsonl` with one `opened` event (`by` is the invoking actor, `level` marked proposed).
5. Fills `{{KEY}}`, `{{TITLE}}`, `{{LEVEL}}`; JSON values are escaped.
6. Never overwrites: a second run reports every file as `SKIP`, and user edits stay intact.
7. Runs no Git, org or network command.

### 5.3 `mshkh lint`

```text
mshkh lint [<KEY>] [--only <check>…] [--changed-only] [--json]
```

Runs the check catalog in OS §7.1 (`card-files`, `acceptance`, `context`, `archive-refs`, `links`, `record`, `sensitive`, `budget`, `duplicates`, `release-trace`), with blocking or advisory status from `meshikah.yaml`.

| Result | Exit |
|---|---|
| Everything passes, or only advisory findings | `0` |
| A blocking check fails | `1` |
| Record hash chain broken or record contradicts files | `5` |
| Secret-like or personal-data-like string found (location printed, never the value) | `6` |

When several apply, the highest-priority code wins in this order: `6`, `5`, `1`.

### 5.4 `mshkh request`

```text
mshkh request <KEY> <Scope|Plan|Review|Accept|Release|Learn> [--evidence <path>…] [--apply]
```

- Appends a `requested` event (OS §4.3). Agents and humans may run it.
- Refuses with exit `4` if the checkpoint doesn't apply to the card's level, or if an earlier required checkpoint isn't approved.
- Checks that the minimum evidence for the checkpoint exists (OS §7.2); missing evidence is exit `4`.

### 5.5 `mshkh decide`

```text
mshkh decide <KEY> <checkpoint> --approve | --reject | --changes-requested --by "<name>"
             [--aspect security|second-human] [--control "<small-team control>"] [--pattern SCP-###]
```

Human only. In order, it:

1. refuses with exit `7` if `MESHIKAH_AGENT=1` is set or stdin is not an interactive terminal;
2. asks the person to type the card key and checkpoint to confirm;
3. refuses with exit `4` if checkpoints are out of order (Accept needs Review approved; Release needs Accept approved) or the minimum evidence is missing;
4. for Critical cards, requires an `--aspect security` decision before Accept is complete, and a second, different person's `--aspect second-human` decision before Release is complete (Model §3.6);
5. counts rework: a third `--reject` or `--changes-requested` at Review or Accept appends a `blocked` event (Model §6.1);
6. appends a `decided` event with `by: human:<name>`.

`--pattern` is accepted only on Plan for Heavy cards, only if the pattern ID is registered, and never for Confidential or Regulated data (Model §5.2).

### 5.6 `mshkh status`

```text
mshkh status [<KEY>] [--json] [--overdue]
```

- With a key: level (proposed or confirmed), derived state (OS §5.2), each checkpoint as `skipped`, `pending`, `requested`, `approved`, `rejected`, the last event, and any stop condition.
- Without a key: all open cards, highlighting `blocked`, `inconsistent`, and requests older than their service target (Model §5.3).
- An inconsistent record shows `inconsistent` and exits `5`.

## 6. Gaps in the package MVP, proposed here

The package MVP has no command for three human-only record events. Until they exist, the person writes them by hand, which the `record` check then validates.

| Event | Proposed command | Rules |
|---|---|---|
| `level_confirmed` | `mshkh decide <KEY> level --set Standard --by "<name>"` | Same human-only controls as `decide`; respects the data floor |
| `released` | `mshkh release <KEY> --deployed-ref <ref> --deployment-id <id> --env <name> --by "<name>"` | Human only; needs Release approved; fills `spec_version` from the commit holding the card (OS §4.11) |
| `correction` | `mshkh correct <KEY> --supersedes <line> --text "…" --by "<name>"` | Human only; the only sanctioned fix to a record |

These are **proposed additions to package `04-cli-mvp.md`**, in scope for 0.3.

## 7. Later commands (not in the MVP)

| Command | Purpose | Notes |
|---|---|---|
| `mshkh promote <KEY>` | Draft a library promotion or lesson (`L-###`) into `notes/` and request Learn | Never writes the library directly |
| `mshkh archive <KEY> --apply` | Move a learned card to `archive/` | Only command that moves files; uses `git mv`; human only; needs confirmation |
| `mshkh metrics` | Derive OS §11 metrics from records | Reports period and sample size; never per person |
| `mshkh policy check` | Allow/ask/deny for binding hooks | Exit `0` allow, `10` ask, `11` deny; an unclassifiable action is always `ask`; Critical and Regulated cards deny anything not provably allowed |
| `mshkh context <KEY>` | Print the load order and allowed write paths for a role | Reads only; grants nothing |
| `mshkh sync <KEY>` | Generate the sanitized context-sync note (OS §4.7) | Blocked on a `sensitive` hit; local only |
| MCP server | Read-only `status`, `lint`, `context` for agents | Never exposes `decide`, `release` or `correct` |

`policy check` example for a Claude Code pre-action hook:

```text
mshkh policy check --role builder --card ABC-123 --action write --path src/sync/client.ts
mshkh policy check --role builder --action exec --command "git push origin HEAD"
```

## 8. Security model

| Human-only command | Why |
|---|---|
| `decide` (including `level`) | Humans decide checkpoints (Standard §2.6) |
| `release` | Tied to the Release decision |
| `correct` | Changes the audit record |
| `archive --apply` | Moves files |

Controls: interactive terminal and typed confirmation; refusal when `MESHIKAH_AGENT=1` is set or stdin isn't a terminal; a `human:<name>` actor on the event.

**Limitation:** a determined process can fake a terminal, so the CLI alone can't prove a person is present. The real control is the binding: agent profiles MUST deny `mshkh decide`, `mshkh release`, `mshkh correct` and `mshkh archive` outright, and MUST set `MESHIKAH_AGENT=1` (OS §6.3). Projects that want more assurance can require signed commits for changes to `record.jsonl` and verify them in CI.

The record's hash chain is tamper-evident, not tamper-proof. The sensitive-data scan is a backstop; the Regulated rule (no regulated data in any artifact) still applies.

`mshkh` stores no credentials, opens no org sessions and reads no `.env*` files.

## 9. Exit codes

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
| 10 | Policy: ask (later) |
| 11 | Policy: deny (later) |
| 64+ | Internal error; report as a bug |

## 10. Files

| Path | Written by | Rule |
|---|---|---|
| `library/index.md`, `MESHIKAH.md`, `work/`, `archive/` | `init` | Create only |
| `meshikah.yaml` | `init --with-config` | Create only |
| `work/<KEY>/card.md`, `plan.md`, `context.json`, `evidence.md`, `notes/` | `new` | Create only |
| `work/<KEY>/record.jsonl` | `new`, `request`, `decide`, `release`, `correct` | Append only, hash-chained |
| `work/<KEY>/notes/NN_*.md` | `promote`, `sync` (later) | New files only |
| `library/` content beyond the index | Nobody | Changes only by a human after Learn |

## 11. Integration

- **CI:** `mshkh lint --changed-only --json` on pull requests. CI never decides checkpoints or writes the record.
- **Git hooks (opt-in, never installed by `init`):** `pre-commit` runs `mshkh lint --only record sensitive --changed-only`.
- **Bindings:** the Claude Code binding (package roadmap 0.4) uses `MESHIKAH.md` as orientation, a fresh Checker session on a different model, permission rules per action class, and later a pre-action hook calling `mshkh policy check`. Each mechanism must be verified against the tool's current documentation (OS §12).

## 12. Acceptance tests

### 12.1 MVP definition of done (package `04-cli-mvp.md`)

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

### 12.2 Additional tests (this specification)

| # | Test | Expected |
|---|---|---|
| 10 | `new --data-class Regulated --level Standard` | Level raised to Critical; message explains why |
| 11 | `new` on a `docs-hub-nested` repository | Files land at the nested profile paths (OS §3.3) |
| 12 | `request Plan` on a Standard card | Exit 4 (checkpoint doesn't apply) |
| 13 | Third rejection at Review | `blocked` event appended |
| 14 | Critical card: Release decided by the same person twice | Second-human decision refused; exit 4 |
| 15 | `context.json` pointing into `archive/` | `lint` reports `archive-refs` |
| 16 | Instruction file over 150 lines or past its review date | `lint` reports `budget` (advisory) |
| 17 | `released` event missing `deployment_id` | `lint` reports `release-trace` |

## 13. Roadmap (from the package)

| Version | Scope | Done when |
|---|---|---|
| **0.1** | Method documents and templates | A reader can run a work card by hand from the docs alone |
| **0.2** | `mshkh init`, `new`, `lint` | MVP tests 1–4 and 7–9 pass |
| **0.3** | `mshkh request`, `decide`, `status`; hash-chained record; §6 gap commands | MVP tests 5–6 pass; one card run end to end |
| **0.4** | Claude Code binding: orientation file, Checker setup, permission rules, hook calling `mshkh` | One Standard card built and checked in Claude Code |
| **0.5** | Demo repository with synthetic data and a 5-minute walkthrough | Shown to 3 outside engineers; feedback recorded |
| **1.0** | First paid pilot with a measured baseline | Before/after numbers with period, sample and method |

## 14. Not now

- Writes to trackers, wikis or deployment systems.
- Dashboards or servers.
- Multi-agent specialist pipelines beyond Builder and Checker.
- AI calls of any kind inside `mshkh`.
- Per-person reporting.

## 15. Open decisions

| ID | Decision | Owner |
|---|---|---|
| Q-CLI-1 | Implementation language and packaging: Python package vs single binary | Product owner |
| Q-CLI-2 | License model if commercialized (open core vs proprietary) | Product owner |
| Q-CLI-3 | Which sensitive-data patterns ship by default, including health-record patterns | Security |
| Q-CLI-4 | Whether the §6 gap commands join the package MVP | Product owner |
| Q-CLI-5 | Whether signed commits for record changes are the default for Critical | Security |

## 16. Document history

| Version | Change |
|---|---|
| 0.1 | First proposed specification (14 command families, `.meshikah/config.yaml`, `MSHKH_AGENT`) |
| **0.2** | Aligned with package v0.1: six MVP commands (`init`, `new`, `lint`, `request`, `decide`, `status`); preview by default with `--apply`; `meshikah.yaml`; `MESHIKAH_AGENT=1`; checkpoints Scope–Learn; package MVP tests 1–9 plus 8 extra; package roadmap; three gap commands proposed (`decide level`, `release`, `correct`) |
