# MeshikahAI Operating System

**Document type:** Technical specification, Layer 3: *files, schemas and permissions: how MeshikahAI runs in a repository*
**Status:** Specification. Partially proven by hand (see §15). Tool-agnostic.
**Version:** 2.0, aligned with the MeshikahAI package v0.1 (`docs/03-runtime.md`). Supersedes OS 1.1 (formerly "Context-OS").
**Implements:** [`MeshikahAI_operating_standard.md`](MeshikahAI_operating_standard.md) 2.0 ("Standard §n") and [`MeshikahAI_operating_model.md`](MeshikahAI_operating_model.md) 2.0 ("Model §n")
**Reference CLI:** [`MeshikahOS_cli_technical_spec.md`](MeshikahOS_cli_technical_spec.md) ("CLI §n") · **Decomposition:** [`MeshikahAI_operating_sub_systems.md`](MeshikahAI_operating_sub_systems.md)
**Audience:** Engineers who build, configure or audit the runtime: bindings, the CLI, checks, CI and connectors

> **Precedence:** Standard > Model > this specification > CLI and tool bindings > project configuration. A binding implements this specification in one tool; it never redefines its contracts.

---

## 1. Purpose and conformance

The runtime is what makes the Model work in real repositories and tools. It:

1. **Selects context deterministically:** for any card and role, the exact files in scope.
2. **Bounds actions:** what each role may read, write and run, enforced in configuration wherever the tool allows.
3. **Records decisions:** an append-only, tamper-evident record per card.
4. **Verifies:** deterministic checks plus evidence for human checkpoints.
5. **Captures knowledge:** lessons and promotions routed through Learn.

It does **not** make AI output deterministic, decide checkpoints, or authorize side effects. A pointer is not a permission (Standard §6.2).

Keywords: **MUST** is required for conformance; **SHOULD** is recommended unless there's a documented reason; **MAY** is optional.

## 2. Components

```text
                ┌─────────────────────────────────────────────┐
                │   Humans: Owner and Approvers (decisions)    │
                └──────────────────────┬──────────────────────┘
                                       │ decided / level_confirmed / released (C6)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                              MESHIKAHAI RUNTIME                              │
│  C1 Library ──▶ C2 Context index ──▶ C3 Loader ──▶ AGENT SESSION (Builder/Checker) │
│                                                          │                   │
│  C4 Policy engine ◀───────────── every tool action ──────●                   │
│                                                          ▼                   │
│  C5 Prompt library      C6 Record (record.jsonl)     C7 Checks (mshkh lint, CI) │
│  C8 Scaffolding (mshkh) C9 Connectors (SF CLI, MCP)  C10 Knowledge capture    │
└──────────────────────────────────────────────────────────────────────────────┘
```

| ID | Component | Responsibility | Realized by | Sub-system |
|---|---|---|---|---|
| C1 | Library | Durable truth under version control | `library/`, `archive/` | 1 Context |
| C2 | Context index | Navigation and per-card pointers | `library/index.md`, `work/<KEY>/context.json` | 1 Context |
| C3 | Loader | The four-step load order and path resolution | `MESHIKAH.md` plus the binding | 1 Context |
| C4 | Policy engine | Action classes, role capabilities, stop conditions | Binding configuration; `mshkh policy` (later, CLI §7) | 4 Governance |
| C5 | Prompt library | ID-stable role and task prompts | `library/prompts/` or workspace library | 2 Orchestration |
| C6 | Record | Append-only requests and decisions | `work/<KEY>/record.jsonl` | 2 Orchestration |
| C7 | Checks | Structural checks and evidence | `mshkh lint`, project tests, CI | 3 Verification |
| C8 | Scaffolding | Safe creation of the library skeleton and cards | `mshkh init`, `mshkh new`; legacy script (Appendix A) | 6 Toolchain |
| C9 | Connectors | Governed access to live and enterprise systems | Salesforce CLI; enterprise search via MCP | 6 Toolchain |
| C10 | Knowledge capture | Lessons, promotions, drift notes, metrics | Librarian outputs; `mshkh promote`, `metrics` (later) | 5 Knowledge |

## 3. Files and paths

### 3.1 Layout

The native layout is defined in Standard §3.1: `MESHIKAH.md`, `meshikah.yaml`, `library/`, `work/<KEY>/`, `archive/`.

A **repository root** is the nearest directory that contains `meshikah.yaml`, or else both the library index and the work directory at their default or mapped paths. Tools MUST refuse to write outside a recognized root.

### 3.2 `meshikah.yaml`

Optional. Absent means native names and defaults.

```yaml
version: 1
paths:
  library: library            # e.g. docs
  work: work                  # e.g. stories
  archive: archive            # e.g. docs/archive
  index: library/index.md     # e.g. docs/00_documentation_index.md
profile: native               # native | docs-hub-flat | docs-hub-nested (§3.3)
key_pattern: "^[A-Z][A-Z0-9]+-\\d+$"
data_classes: [Public, Internal]           # classes this project may touch
instruction_budget: 150
instruction_files: [MESHIKAH.md, CLAUDE.md, AGENTS.md]
tracker:
  system: jira
  state_map:                                # Model §21
    "Requirement Gathering": [opened, scoped]
    "In Development": [planned, building]
    "Ready in QA": [reviewed, checking]
    "Deployed to prod": [released]
    "Completed": [learned]
change_patterns: library/standards/change_patterns.md   # Model §5.2
service_targets_days: {Scope: 1, Plan: 2, Review: 0, Accept: 2, Learn: 5}
checks:
  blocking: [context, links, record, sensitive]
  advisory: [card-files, acceptance, budget, archive-refs, duplicates]
```

Precedence for any setting: command-line flag > `meshikah.yaml` > statement in `MESHIKAH.md` (layout only) > auto-detection > defaults.

### 3.3 Profiles for existing repositories

A profile maps the four card roles onto file names, so older repositories run unchanged.

| Card role | `native` | `docs-hub-flat` | `docs-hub-nested` |
|---|---|---|---|
| Card | `card.md` | `00_story_details.md` | `02-story/00_story_details.md` |
| Plan | `plan.md` | `01_delta_implementation_plan.md` | `03-implementation/01_delta_implementation_plan.md` |
| Acceptance | in `card.md` | `02_acceptance_tests.md` | `05-testing/02_acceptance_tests.md` |
| Evidence | `evidence.md` | `05-testing/00_evidence_index.md` | `05-testing/00_evidence_index.md` |
| Context | `context.json` | `context_manifest.json` | `context_manifest.json` |
| Record | `record.jsonl` | `handoffs/record.jsonl` | `handoffs/record.jsonl` |
| Notes | `notes/` | `03-implementation/` | `03-implementation/` |

Detection when `profile` is not set: if any card folder contains `02-story/`, use `docs-hub-nested`; else if any contains `00_story_details.md`, use `docs-hub-flat`; else `native`. Tools never migrate cards between profiles.

For Docs Hub profiles, `context_manifest.json` keys map to `context.json` fields: `story_id` → `key`, `required_hub_docs` → `library`, `target_metadata` → `may_change`, `test_classes` → `tests`, `metadata_to_retrieve` → `retrieve` (§4.1). A project validator that rejects unknown keys keeps working, because tools write only the keys the profile declares.

### 3.4 Path resolution

To resolve "which file is X for card K", tools MUST use this order:

1. An explicit path in `context.json`.
2. An explicit path in an approved plan (`plan.md` files to touch).
3. The project profile (§3.3).
4. Native defaults.

Tools MUST NOT hardcode library file names across projects.

### 3.5 Numbering in `notes/`

New files in `notes/` take `NN = max(existing two-digit prefixes) + 1`, zero-padded, never reusing a number. Handoff notes are named `NN_<from>_to_<to>[_rN].md` (§5.3).

## 4. Data contracts

### 4.1 `context.json`

| Field | Type | Required | Meaning |
|---|---|---|---|
| `key` | string matching `key_pattern` | ✓ | Card key; equals the folder name |
| `title` | string | ✓ | Card title |
| `level` | `Light` \| `Standard` \| `Heavy` \| `Critical` | ✓ | As proposed or confirmed; the record is authoritative |
| `data_class` | `Public` \| `Internal` \| `Confidential` \| `Regulated` | ✓ | Highest class the card could touch |
| `library` | array of paths | ✓ | Library documents to load (step 2) |
| `source` | array of paths | ✓ | Source files to read (step 3) |
| `may_change` | array of paths or globs | ✓ | Files the Builder may edit |
| `tests` | array | ✓ | Test targets |
| `retrieve` | array of `Type:Member` | optional | Live metadata to retrieve; still needs authorization |

Rules: paths are repository-relative and exist, except `may_change` entries the plan creates; nothing points into `archive/` unless the card is about history; unknown keys are rejected; `data_class` must be one the project declares in `meshikah.yaml`.

### 4.2 `card.md`

The header fields in Model §9.1, then the template sections (Standard §7). Acceptance criteria are numbered; the numbers are the keys used in `evidence.md` and the record.

### 4.3 `record.jsonl`

One JSON object per line. Never edited, never deleted.

```json
{"at":"2026-11-02T17:00:00Z","card":"ABC-123","event":"requested","checkpoint":"Review","by":"agent:builder","evidence":["work/ABC-123/evidence.md"],"prev":"sha256:…"}
{"at":"2026-11-02T18:10:00Z","card":"ABC-123","event":"decided","checkpoint":"Review","decision":"approved","by":"human:armando","prev":"sha256:…"}
```

| Field | Present on | Rule |
|---|---|---|
| `at` | all | ISO 8601 UTC |
| `card` | all | Equals the folder name |
| `event` | all | See the event table |
| `by` | all | `human:<name>` or `agent:<role>` (Model §3.3) |
| `prev` | all | `sha256:` of the previous line's exact bytes; `null` on the first line |
| `checkpoint` | `requested`, `decided` | `Scope` \| `Plan` \| `Review` \| `Accept` \| `Release` \| `Learn` |
| `decision` | `decided` | `approved` \| `rejected` \| `changes-requested` |
| `evidence` | `requested`, `decided` | Paths to the proof |
| `level` | `opened`, `level_confirmed` | Proposed or confirmed level |
| `aspect` | `decided` (optional) | `security` for the Critical security decision; `second-human` for the Critical Release co-decision |
| `control` | `decided` (optional) | The small-team control used (Model §3.6) |
| `pattern` | `decided` Plan (optional) | Change pattern ID (Model §5.2) |
| `supersedes` | `correction` | Line number being corrected |
| `text` | `note`, `blocked`, `unblocked`, `correction` | Short, sanitized text |

| Event | Who may write it |
|---|---|
| `opened`, `requested`, `note`, `blocked`, `unblocked` | Human or agent |
| `level_confirmed`, `decided`, `released`, `correction` | Human only |

- The hash chain makes edits and deletions **detectable**. The record is tamper-evident, not tamper-proof; Git history is the second line of defense.
- Current state is **derived** from the record (§5.2). Any summary view is generated and never edited by hand.
- Corrections are new `correction` events that reference the line they supersede.

### 4.4 `evidence.md`

A summary table (`Acceptance | Result | Proof | Environment | Date`), one row per criterion, every row starting as `NOT VERIFIED`, followed by a details block per criterion in the Model §12.2 format.

### 4.5 Lesson entry

In `library/lessons.md`:

```markdown
### L-012: <short title>
- **Symptom:** <observable behavior>
- **Root cause:** <verified cause>
- **Resolution:** <what fixed it>
- **Evidence:** <card key, log or test link>
```

IDs are sequential per project. A lesson is added only after the fix is verified, through Learn. No speculation, secrets or credentials.

### 4.6 Notes and logs

`notes/NN_<topic>.md` holds implementation logs, retrieval diffs, findings and handoff notes. A log records date, environment, hub links (not copies), issues and root causes, changes (file → delta), verification (command → result, IDs), deployment status, and open items.

### 4.7 Context-sync note

```markdown
# Context sync: <KEY> — <milestone>
- Updated (UTC):
- Tracker status:
- Card state (from record):
- Implemented behavior:
- Changed files:
- Tests (command → result):
- Deployment (ID / environment, or "not deployed"):
- Known limitations:
- Open decisions (Q-### / DEC-###):
- Next steps:
- Sources (links):
```

It MUST be sanitized and is never a decision.

### 4.8 Enterprise finding

```markdown
### Enterprise finding: <short title>
- Card: <KEY>
- Source: <title and URL>
- Retrieved: <timestamp>
- Finding: <sanitized statement>
- Evidence: <relevant excerpt or decision>
- Confidence: High | Medium | Low
- Promotion: Card only | Library (via Learn) | Not promoted
```

### 4.9 Identifiers

| Artifact | ID | Scope |
|---|---|---|
| Work card | Tracker key (`key_pattern`) | Project |
| Decision record | `DEC-###` | Project |
| Open question | `Q-###` | Project |
| Lesson | `L-###` | Project |
| Change pattern | `SCP-###` | Project |
| Prompt | `P-###` | Prompt library |
| Checkpoint | `Scope`, `Plan`, `Review`, `Accept`, `Release`, `Learn` | Model |

### 4.10 Session report

The format is Model §16. Every agent session MUST end with it.

### 4.11 `released` event

Written by a human at Release, after the deployment:

```json
{"at":"…","card":"ABC-123","event":"released","by":"human:armando","spec_version":"<commit with final card, plan, context.json>","deployed_ref":"<commit or package>","deployment_id":"<id>","environment":"<org or env>","prev":"sha256:…"}
```

It answers "which version of which card produced this deployed behavior?" (Standard §4.1).

### 4.12 Instruction-file header

Every always-on instruction file starts with:

```markdown
<!-- owner: <name> · review by: <YYYY-MM-DD> · budget: 150 lines -->
```

The budget check counts non-empty instruction lines.

## 5. Runtime execution

### 5.1 Session lifecycle

```text
BOOT ─▶ ORIENT ─▶ LOAD ─▶ ACT ─▶ VERIFY ─▶ REPORT ─▶ CLOSE
          │         │       │       │         └ session report (§4.10); request a checkpoint if ready
          │         │       │       └ run checks; real output into evidence.md
          │         │       └ actions within the role's classes (§6); stop on any stop condition
          │         └ library list → card, plan, source; `git status` first
          └ MESHIKAH.md, library/index.md, context.json
```

### 5.2 Card state

State is derived from the record and the card's location, never stored separately.

```text
opened ─(level_confirmed)─▶ ready ─Scope─▶ scoped ─Plan─▶ planned ─▶ building
   building ─(requested Review)─▶ in review ─Review─▶ checking ─Accept─▶ accepted
   accepted ─Release─▶ released ─Learn─▶ learned ─(folder moved to archive/)─▶ archived
   any state ─blocked─▶ blocked ─unblocked─▶ previous state
   rejected / changes-requested at a checkpoint ─▶ back to building (or planned, for Accept)
```

- Checkpoints that don't apply to the level are skipped: a Light card goes from `ready` to `building`, a Standard card skips `planned`, a card that isn't deployed skips `released`.
- A third rejection at Review or Accept sets `blocked` until the owner re-scopes or re-plans (Model §6.1).
- If the record's hash chain fails, or the record contradicts the files (for example, `released` without an approved Release), the state is `inconsistent` and work stops (§6.4).

### 5.3 Sequences and handoffs

**Standard:**

```text
Owner → Builder        : open card, level, context.json            (opened, level_confirmed, decided Scope)
Builder → repo         : load (§5.1), build, test                  (note …)
Builder → record       : requested Review + evidence.md
Owner                  : decided Review
Owner → Checker (fresh session, different model): card, plan, diff, evidence — not the Builder's reasoning
Checker → notes/       : NN_checker_report.md; evidence.md updated (requested Accept)
Approvers              : decided Accept → decided Release (if deployed) → released
```

**Heavy:** the same, with a Plan decision before building and a Librarian proposal at Learn.
**Critical:** Heavy, plus a separate security review in its own session and two human decisions at Release (`aspect: second-human`).

Handoffs between agents are files in `notes/` (`NN_builder_to_checker.md`) plus a `note` event. A handoff note lists files actually read, outputs, allowed write locations for the next role, verification commands with real output, and open questions.

## 6. Policy and permissions

### 6.1 Action classes

Bindings MUST map every tool action to a class and enforce the default. Projects may tighten a default, never loosen it.

| Class | Examples | Default |
|---|---|---|
| **Read** | Read files, search, `git status`, `git diff`, `git log` | Allow |
| **Verify** | Local tests, lint, type checks, validators, dry-run deploys | Allow |
| **Write: local** | Edit files listed in `may_change` | Allow inside the list; ask outside it |
| **Write: shared** | `git commit`, `git push`, branch operations | Ask |
| **Write: external** | Deployments, org data changes, tracker or wiki writes | Human only, per action |
| **Destructive** | Deletes, destructive packages, history rewrites, `.env*` and `.git/**` writes, `git config` | Deny |

**External reads** (targeted org retrieval, enterprise search over MCP) are not named in the package. This specification treats them as **Ask**, limited to `context.json → retrieve` and the card's search terms. *Proposed addition to package `03-runtime.md`.*

### 6.2 Role capabilities

| Role | Read | Verify | Write: local | Write: shared | Write: external | Destructive |
|---|---|---|---|---|---|---|
| Owner (human) | ✓ | ✓ | Any | ✓ | ✓ per action, after the required decisions | Approved procedure only (Model §11.4) |
| Builder | ✓ | ✓ | `may_change`, card files, `notes/` | Ask, only when assigned | ✗ | ✗ |
| Checker | ✓ | ✓ | `evidence.md`, `notes/`; tests only if project policy allows | ✗ | ✗ | ✗ |
| Librarian | ✓ | ✗ | Promotion proposals in `notes/` | ✗ | ✗ | ✗ |
| Specialists (Model §18) | ✓ | per role | Their own draft files | ✗ | ✗ | ✗ |

### 6.3 Enforcement strength

| Strength | Mechanism | What it guarantees |
|---|---|---|
| **Enforced** | Tool configuration: deny rules, restricted tool lists, hooks that block, OS sandbox | The agent can't bypass it |
| **Asked** | Ask rules; confirmation prompts | A human sees each action |
| **Instructed** | `MESHIKAH.md`, prompts, plan constraints | Advisory; verified at Review through the diff |
| **Decided** | A human checkpoint with recorded evidence | Final control |

Bindings SHOULD make Write: shared, Write: external and Destructive **Enforced** or **Asked**, and path-scoped Write: local **Enforced** where the tool supports path rules.

**Critical cards and Regulated data MUST run with Enforced controls** for every Write and Destructive class, including a sandbox or equivalent that stops shell commands from bypassing file rules (§16). If a tool can't enforce a control, a human performs that step.

### 6.4 Stop conditions

Any agent or tool stops and hands back to the owner when:

- the target environment can't be confirmed;
- a needed file is outside `may_change`;
- `context.json` is invalid;
- secrets or sensitive data appear;
- the library and the live system disagree and no rule settles which one wins;
- required checks can't run;
- the record is inconsistent;
- the requested action needs a checkpoint that hasn't been decided.

## 7. Checks

### 7.1 Catalog

The checks run by `mshkh lint` (CLI §5.3) and CI:

| Check | Verifies | Default |
|---|---|---|
| `card-files` | Card, plan, context and evidence exist per profile | Advisory |
| `acceptance` | Numbered Given/When/Then criteria, including a negative or boundary case | Advisory |
| `context` | `context.json` schema; paths exist; declared data class | Blocking |
| `archive-refs` | No active `context.json` points into `archive/` | Blocking candidate |
| `links` | Relative links in the library index and card resolve | Blocking |
| `record` | Hash chain intact; human-only events have human actors; checkpoint order valid | Blocking |
| `sensitive` | No secret-like or personal-data-like strings in card artifacts (location printed, never the value) | Blocking |
| `budget` | Instruction files declare owner, review date and budget; within cap; not past review | Advisory |
| `duplicates` | Exact copies of library text inside cards | Advisory |
| `release-trace` | Every `released` event has spec version, deployed reference and deployment ID | Blocking candidate |
| Project tests, lint, type checks, dry-run deploys | Per project | Per project CI |

Semantic duplication is never a blocking check without human review. Checks verify structure, not meaning.

### 7.2 Minimum evidence per checkpoint

| Checkpoint | Minimum machine evidence |
|---|---|
| Scope | `card.md` passing `acceptance` |
| Plan | `plan.md` with files to touch, files not to touch, test map |
| Review | `git diff --stat <base>`, focused test output, lint output |
| Accept | `evidence.md` with every criterion classified; Critical: security review with file and line references |
| Release | Package matching the diff, dry-run job ID, test results, rollback note |
| Learn | Promotion diff linked to the card and decision |

## 8. Scaffolding

`mshkh init` creates the library skeleton and `MESHIKAH.md`; `mshkh new` creates a card from the templates (CLI §5.1–§5.2). Both preview without `--apply`, create only missing files, and never touch Git, an org or the network.

Until `mshkh` exists, cards are created by hand from the package templates. The Docs Hub pilot's PowerShell scaffolder remains available for repositories on a Docs Hub profile (Appendix A); it is **legacy** and is replaced once `mshkh new` passes its test record.

## 9. Connectors

### 9.1 Salesforce CLI

1. Confirm the org alias (stop condition otherwise).
2. Run `git status`; protect uncommitted work.
3. Retrieve only `context.json → retrieve`, into a directory **outside** the working tree.
4. Compare with the repository; record differences and provenance in `notes/`.
5. Never deploy, delete or change org data without the decisions the level requires.

Verify metadata-type support for OmniStudio and managed packages against the installed CLI and plugins.

### 9.2 Enterprise search (MCP)

1. Load the card's library documents first.
2. Stop if the connector is unavailable.
3. Search with the card key, approved terms and component names.
4. Prefer current approved decisions over comments and duplicates.
5. Reconcile with live metadata and acceptance.
6. Persist only §4.8 records.
7. Never persist tokens, cookies, personal data or search dumps.

### 9.3 Conflicts between sources

When sources disagree, the tool records both values, their sources and the retrieval time in `notes/`, applies the authority rules (Model §8) and the project's source-of-truth policy (Standard §5), opens a `Q-###` for a human, adds a `blocked` event, and **never silently overwrites** either source.

### 9.4 Write connectors

Writing to trackers, wikis, ITSM tools or portals is out of scope until the controls in Standard §13 (branch 4) exist.

## 10. Security and data protection

- **Secrets** never appear in prompts, cards, records, notes, prompts or configuration. Use the tool's secret manager or the environment. `.env*` writes are Destructive (denied).
- **Personal and regulated data** never enter any artifact. Use sanitized identifiers; redact raw meeting notes before they are input.
- **Approved tools and models only**, per data class (Standard §8.1). Cloud handoff only where policy allows.
- **Audit trail:** Git history plus the hash-chained record. Never rewrite history.
- **Least privilege:** org aliases and connector credentials have the narrowest scope possible. Agent roles get no more than §6.2.

## 11. Metrics from the record

| Metric | Derived from |
|---|---|
| Rework rounds | `decided` events with `rejected` or `changes-requested`, per card |
| Checkpoint cycle time | Time from `requested` to `decided`, per checkpoint, against service targets |
| Early catch rate | Rejections at Scope, Plan or Review versus defects found after Accept |
| Defects after Accept | Bugs linked to the card in the tracker (needs a tracker export) |
| Context size | Number of files in `context.json` and files read beyond it (session reports) |
| Knowledge yield | Lessons and promotions decided at Learn, per card |

Metrics describe the process, never individuals. Published numbers need a baseline, period, sample and method (Standard §14).

## 12. Bindings

A binding is a short document plus configuration that implements this runtime in one tool. It states how the tool provides each capability, and marks every gap honestly.

| # | Capability | Spec reference |
|---|---|---|
| 1 | Always-on orientation (`MESHIKAH.md` or the tool's equivalent pointing to it) | §5.1 |
| 2 | Fresh, isolated sessions for the Checker | §5.3 |
| 3 | Path-scoped writes (`may_change`) | §6.2 |
| 4 | Ask/deny rules per action class | §6.1, §6.3 |
| 5 | A way for agents to request, but not decide, checkpoints | §4.3 |
| 6 | A different model for the Checker | Model §3.6 |

Detailed mechanisms a binding documents: reusable procedures per role (skills or prompts), tool restrictions per role, hook points for `mshkh policy` (later), governed enterprise reads, and safety for unattended or background sessions.

| Tool | Status |
|---|---|
| **Claude Code** | First planned binding (package roadmap 0.4): orientation file, Checker setup, permission rules, a hook calling `mshkh`. Every mechanism must be verified against Claude Code's current documentation before the binding is published. |
| Devin | Pilot binding v1.2 written for the 1.x contracts. Needs updating to 2.0 names and record format before reuse. |
| Cursor, Copilot, Windsurf, others | Not started |

## 13. Failure modes and recovery

| Failure | Detection | Recovery |
|---|---|---|
| Agent edits outside `may_change` | Review diff; path rules | Reject at Review; revert out-of-scope changes; tighten the binding |
| `context.json` drift (missing or renamed files) | `lint context` | Stop; owner updates `context.json`; re-run |
| Stale or archived context used | Session report "files read" | Re-run with the corrected list; mark the source superseded |
| Illustrative or invented results | Checker re-run; Review or Accept | Reject; note the incident; re-run verification |
| Record inconsistent | `lint record` | Owner reconciles with a `correction` event |
| Source conflict (enterprise vs org) | §9.3 | Open `Q-###`; human decides |
| Retrieval overwrote local work | `git status` before and after | Restore from Git; retrieve outside the working tree next time |
| Third rework round | Record | Card `blocked`; owner re-scopes or re-plans |
| Background agent blocked by permissions | Tool denial | Resume in the foreground and approve, or adjust the binding |

## 14. Versioning

| Artifact | Version | Compatible with |
|---|---|---|
| Standard | 2.0 | — |
| Model | 2.0 | Standard 2.x |
| Operating System (this spec) | 2.0 | Standard 2.x, Model 2.x |
| Sub-systems | 2.0 | OS 2.x |
| MeshikahOS-cli spec | 0.2 (proposed) | OS 2.x |
| Package | v0.1 | Framework 2.0 |
| Devin binding | 1.2 | OS 1.x only |

Rules:

- A breaking change to a data contract (§4) or an action class (§6) needs a **major** version and a review of every binding in the same change.
- 2.0 is breaking against 1.x: file names, record format (`ledger.jsonl` + pipeline log → `record.jsonl`), checkpoint names, level names and role identifiers all changed. Repositories on 1.x layouts run through a Docs Hub profile (§3.3); their 1.x ledgers are not converted automatically.
- Bindings cite section numbers and must be re-checked when sections are renumbered.

## 15. Implementation status (2026-10-31)

| Component | Status |
|---|---|
| C1 Library | Proven by hand in the Docs Hub pilot (1.x names); package templates exist |
| C2 Context index | Pilot manifests in use under the 1.x schema; `context.json` defined, not yet used on real cards |
| C3 Loader | `MESHIKAH.md` template exists; pilot used a 1.x skill |
| C4 Policy engine | Designed; no binding installed for 2.0 |
| C5 Prompt library | Architecture and a few templates (1.x); category files pending |
| C6 Record | Format defined; not yet used on real cards |
| C7 Checks | Pilot validators (1.x); `mshkh lint` proposed |
| C8 Scaffolding | Legacy PowerShell script tested for 1.x layouts; `mshkh init` and `new` proposed |
| C9 Connectors | Salesforce CLI in use; enterprise-search read connector piloted |
| C10 Knowledge capture | Lessons registry in use under the 1.x name (`KG-###`); Librarian role defined |

## 16. Limitations

- Agent behavior is probabilistic. Instructed and Decided controls depend on human review.
- Path scoping depends on the tool; shell commands can bypass file rules unless a sandbox is used.
- Checks verify structure, not meaning.
- The record detects tampering; it doesn't prevent it.
- Tool features used by bindings change often; bindings must be re-verified.

## 17. Document history

| Version | Change |
|---|---|
| Docs Hub OS 1.0 | Context-OS: components C1–C10, path resolution, data contracts, command classes, scaffolding, connectors, binding contract |
| 1.0 | Generalized; client identifiers removed |
| 1.1 | Handoff front matter with input hashes; `ledger.jsonl`; release stamp; instruction budget; enforced controls for T3/D3 |
| **2.0** | Aligned with MeshikahAI package v0.1: native layout and `meshikah.yaml`; profiles for Docs Hub repositories; `context.json`; one hash-chained `record.jsonl` replacing the pipeline log, handoff ledger and release stamp; six action classes replacing K0–K6; Enforced/Asked/Instructed/Decided replacing E1–E4; card state derived from the record; six-capability binding contract; Claude Code as first binding; external reads added as Ask (proposed for the package). |

---

## Appendix A: Legacy scaffolder (Docs Hub profiles)

For repositories still on the `docs-hub-flat` or `docs-hub-nested` profile. It creates 1.x file names and a 1.x pipeline log, not a 2.0 record. Retire it when `mshkh new` passes the same tests on those profiles.

**Contract:** validates the repository root; detects the layout; supports `-WhatIf`; creates only missing files; never overwrites, moves or deletes; never touches Git or an org; reports each file as created or skipped.

**Test record (2026-10-22, temporary repository, PowerShell 5):** a non-root path is rejected (exit 1); `-WhatIf` writes nothing; the first run creates 5 files; a rerun skips everything and keeps a user edit intact; an invalid key is rejected; the generated manifest passes the pilot validator. The Release row was added to the pipeline-log template afterwards, so the `-WithPipelineLog` path needs a re-run before it is reported as tested.

```powershell
<#
.SYNOPSIS
  Safely scaffold a MeshikahAI story spoke (standard §11 safe-bootstrap rules).
.DESCRIPTION
  Creates only missing starter files for one story. Never overwrites, moves, or deletes files;
  never touches Git or a Salesforce org. Use -WhatIf to preview.
.EXAMPLE
  .\New-MeshikahStorySpoke.ps1 -StoryKey APP-5000 -StoryTitle "Example change" -Tier T2 -WhatIf
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)][ValidatePattern('^[A-Z][A-Z0-9]+-\d+$')][string]$StoryKey,
    [Parameter(Mandatory = $true)][ValidateNotNullOrEmpty()][string]$StoryTitle,
    [ValidateSet('T0', 'T1', 'T2', 'T3')][string]$Tier = 'T2',
    [ValidateSet('Auto', 'Nested', 'Flat')][string]$Layout = 'Auto',
    [string]$RepoRoot = (Get-Location).Path,
    [switch]$WithManifest,
    [switch]$WithPipelineLog
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$index = Join-Path $RepoRoot 'docs\00_documentation_index.md'
$storiesRoot = Join-Path $RepoRoot 'stories'
if (-not (Test-Path -LiteralPath $index) -or -not (Test-Path -LiteralPath $storiesRoot)) {
    Write-Error "Not a MeshikahAI repository root (need docs\00_documentation_index.md and stories\): $RepoRoot"
    exit 1
}

if ($Layout -eq 'Auto') {
    $nested = Get-ChildItem -LiteralPath $storiesRoot -Directory |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName '02-story') } | Select-Object -First 1
    $Layout = if ($nested) { 'Nested' } else { 'Flat' }
}

$paths = if ($Layout -eq 'Nested') {
    @{ Story = '02-story\00_story_details.md'; Plan = '03-implementation\01_delta_implementation_plan.md'; Tests = '05-testing\02_acceptance_tests.md' }
} else {
    @{ Story = '00_story_details.md'; Plan = '01_delta_implementation_plan.md'; Tests = '02_acceptance_tests.md' }
}

$storyDir = Join-Path $storiesRoot $StoryKey
$rel = { param($p) ("stories/$StoryKey/" + $p).Replace('\', '/') }
$tokens = @{
    '{{KEY}}' = $StoryKey; '{{TITLE}}' = $StoryTitle; '{{TIER}}' = $Tier
    '{{STORY}}' = (& $rel $paths.Story); '{{PLAN}}' = (& $rel $paths.Plan); '{{TESTS}}' = (& $rel $paths.Tests)
}

$templates = [ordered]@{}
$templates[$paths.Story] = @'
# Story Details: {{KEY}} — {{TITLE}}

## Hub context pointers
- Documentation index: docs/00_documentation_index.md
- Architecture: <add the relevant current document from the index>
- Data model: <add if applicable>
- Standards: <add the relevant standard(s)>

## Issue metadata
- Issue key: {{KEY}}
- Summary: {{TITLE}}
- Tier: {{TIER}} (proposed; confirm at triage)

## Business context and scope
- In scope:
- Out of scope:

## Acceptance criteria
### Scenario 1: <name>
- GIVEN <precondition>
- WHEN <action>
- THEN <observable result>

## Open questions
- <question> — owner:
'@
$templates[$paths.Plan] = @'
# Delta Implementation Plan: {{KEY}}

## Objective and scope
<What changes, and what must remain unchanged>

## Affected components
| File/component | Intended delta | Boundary/notes |
|---|---|---|

## Must-not-change
- docs/ (canonical hub) — promotion only via G6

## Non-functional guardrails
- <cite the project standard for each guardrail>

## AC → test map
| Acceptance criterion | Test target | Type |
|---|---|---|

## Implementation sequence
1. <step>

## Dependencies, risks, and decisions
- <links and unresolved questions>

## Verification
- <focused tests, lint, dry-run command>
'@
$templates[$paths.Tests] = @'
# Acceptance Tests: {{KEY}}

## Scenario 1: <name>
- Setup:
- Action:
- Expected observable result:
- Negative / permission / boundary case:
'@
if ($WithPipelineLog) {
    $templates['handoffs\00_pipeline_log.md'] = @'
# Pipeline Log: {{KEY}}

- Tier: {{TIER}} (confirmed by <human>, <date>)

| Gate | Phase | Status | Approver | Timestamp (UTC) | Evidence |
|---|---|---|---|---|---|
| G1 | Scope | Pending | | | {{STORY}} |
| G2 | Design | Pending | | | {{PLAN}} |
| G3 | Diff review | Pending | | | <diff base + implementation log> |
| G4 | Security (T3) | Pending / N/A | | | <security review> |
| G5 | Acceptance | Pending | | | <verification report + UAT evidence> |
| R | Release | Pending / N/A | | | <manifest, dry-run job ID, deployment ID> |
| G6 | Promotion | Pending | | | <promotion proposals> |
'@
}
if ($WithManifest) {
    # Pilot project manifest schema (scripts/ci/validate_context_manifest.py); adjust keys for other projects.
    $templates['context_manifest.json'] = @'
{
  "story_id": "{{KEY}}",
  "title": "{{TITLE}}",
  "required_hub_docs": ["docs/00_documentation_index.md"],
  "metadata_to_retrieve": [],
  "target_metadata": [],
  "test_classes": []
}
'@
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$created = 0; $skipped = 0
foreach ($relPath in $templates.Keys) {
    $target = Join-Path $storyDir $relPath
    if (Test-Path -LiteralPath $target) { Write-Host "SKIP    $target (exists)"; $skipped++; continue }
    $text = $templates[$relPath]
    foreach ($t in $tokens.Keys) {
        $value = $tokens[$t]
        if ($relPath -like '*.json') { $value = $value.Replace('\', '\\').Replace('"', '\"') }
        $text = $text.Replace($t, $value)
    }
    if ($PSCmdlet.ShouldProcess($target, 'Create file')) {
        $parent = Split-Path -Parent $target
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        [System.IO.File]::WriteAllText($target, $text, $utf8NoBom)
        Write-Host "CREATE  $target"; $created++
    }
}
Write-Host "Layout: $Layout | created: $created | skipped: $skipped | repo: $RepoRoot"
```

**Installation:** review the script, copy it into a project's `scripts\`, and run it with `-WhatIf` first:

```powershell
.\scripts\New-MeshikahStorySpoke.ps1 -StoryKey APP-5000 -StoryTitle "Example change" -Tier T2 -WithPipelineLog -WithManifest -WhatIf
```
