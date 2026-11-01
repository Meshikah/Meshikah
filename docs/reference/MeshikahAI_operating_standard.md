# MeshikahAI Operating Standard

**Status:** Canonical
**Version:** 2.0, aligned with the MeshikahAI package v0.1 (`docs/01-principles.md`). Supersedes Standard 1.1.
**Framework layer:** Layer 1, the Standard: *what must always be true, and why*
**Scope:** Any repository where people build software with AI agents, in any technology
**Applies to:** Human contributors and AI coding agents

> **Precedence:** Standard > [Model](MeshikahAI_operating_model.md) > [Operating System](MeshikahAI_operating_system.md) > [CLI](MeshikahOS_cli_technical_spec.md) and tool bindings > project configuration. Lower layers may narrow this standard, never loosen it.

---

## 1. Purpose

MeshikahAI is **context engineering for teams that build software with AI agents**: a working method plus a small toolchain. For every piece of AI-assisted work it answers three questions:

1. **What should the agent read?** Exactly the context the task needs, and nothing stale or unrelated.
2. **What may it change?** A declared set of files and actions, checked before and after.
3. **Who decided it was done, and on what evidence?** A human, recorded, with proof attached.

### 1.1 Why it exists

AI agents rarely fail in real repositories for lack of intelligence. They fail on bad context:

- **Drift:** wikis and READMEs that no longer match the code.
- **Duplication:** the same rule written three different ways across tickets and docs.
- **Crawling:** whole repositories dumped into a prompt, mixing old and unrelated material into the task.
- **Tribal knowledge:** decisions that only ever lived in a chat thread or a meeting.

MeshikahAI treats context as an engineered asset, with an owner, a structure and checks, instead of a pile of files.

### 1.2 The shape: library, work card, record

```text
┌─────────────────────────┐     points to      ┌──────────────────────────┐
│  LIBRARY  (library/)    │◀───────────────────│  WORK CARD (work/<KEY>/) │
│  Durable truth, 1 copy  │                    │  Only what changes now   │
│  architecture, models,  │   promotes back    │  card, plan, context,    │
│  standards, lessons     │◀───── (human) ─────│  evidence                │
└─────────────────────────┘                    └────────────┬─────────────┘
                                                            │ appends
                                               ┌────────────▼─────────────┐
                                               │  RECORD (record.jsonl)   │
                                               │  Every human decision,   │
                                               │  append-only             │
                                               └──────────────────────────┘
```

| Concept | What it is | Where it lives |
|---|---|---|
| **Library** | The one place durable knowledge lives: architecture, data models, standards, lessons | `library/` |
| **Work card** | A lean folder per work item: the delta, the acceptance contract, the evidence. It links to the library instead of copying it. | `work/<KEY>/` |
| **Record** | An append-only log of requests and human decisions for one work card | `work/<KEY>/record.jsonl` |
| **Archive** | Superseded material and closed cards, visible but out of active context | `archive/` |
| **Orientation file** | The always-on agent instructions, budgeted | `MESHIKAH.md` |

### 1.3 The framework layers

| Layer | Document | Answers | Package equivalent |
|---|---|---|---|
| 1 Standard | This document | What must always be true, and why | `docs/01-principles.md` |
| 2 Model | [`MeshikahAI_operating_model.md`](MeshikahAI_operating_model.md) | Who does what, when, at which risk level, with what proof | `docs/02-operating-model.md` |
| 3 Operating System | [`MeshikahAI_operating_system.md`](MeshikahAI_operating_system.md) and [`MeshikahAI_operating_sub_systems.md`](MeshikahAI_operating_sub_systems.md) | Files, schemas, permissions: how it runs in a repository | `docs/03-runtime.md` |
| 3 Reference CLI | [`MeshikahOS_cli_technical_spec.md`](MeshikahOS_cli_technical_spec.md) | The `mshkh` command-line tool | `docs/04-cli-mvp.md` |

The package documents are the short, product-facing form. These four documents are the full reference: they carry the same contracts plus the enterprise depth (authority rules, Salesforce profile, bindings, security model, acceptance tests). **If a package document and its reference document disagree, fix the disagreement; until then the reference document governs.**

**Layering rules**

- **Lower layers govern higher ones.** The Model, the OS and the CLI can narrow this standard, never loosen it.
- **Selection is deterministic; outcomes are not.** MeshikahAI makes *what an agent reads and may change* repeatable. AI output stays probabilistic, which is why evidence and human decisions stay mandatory.
- **One runtime, many tools.** A Claude Code, Cursor, Copilot or Devin binding implements the same contracts; it never redefines them.
- **Project specifics live in the project.** A project's own rules go in its configuration and extension documents, which link here and narrow, never loosen.

### 1.4 Lineage

| Stage | Form | Main contribution |
|---|---|---|
| Prompt-metadata folders (2024) | Personal practice | Per-requirement context folders reused across chats |
| Docs Hub pattern 1.0–3.1 | Enterprise pilot standard | Hub-and-spoke docs, staged loading, gates, Context-OS |
| AetherOS | Operating sub-systems | Six named sub-systems decomposing the runtime |
| MeshikahAI framework 1.0–1.1 | Generalized reference docs | Client identifiers removed; data classes; traceability; CLI spec |
| **MeshikahAI package v0.1 / framework 2.0** | Product method | Plain vocabulary (library, work card, record, Light–Critical, Scope–Learn), nine principles, `mshkh` MVP |

## 2. The nine principles

These principles are the core of MeshikahAI. Every other document applies them; none may weaken them. Each has a rule, a reason, and a check.

### 2.1 One copy of durable truth

- **Rule:** Architecture, data models, standards and hard-won lessons live in the library, once. Everything else links to them.
- **Why:** Two copies of a rule become two different rules the first time one changes.
- **Check:** No work card contains a verbatim copy of a library document.

### 2.2 Work cards carry the delta only

- **Rule:** A work card says what changes for this item, how we will know it works, and what proved it. It does not restate the system.
- **Why:** Cards are read by agents under a tight attention budget. Every repeated paragraph is noise and a future contradiction.
- **Check:** A card can be read in full in a few minutes and has links, not copies.

### 2.3 Load by pointer, not by crawl

- **Rule:** Each card lists the exact library documents and source files in scope (`context.json`). Agents load that list, in a fixed order, and nothing else by default.
- **Why:** Ingesting a whole repository mixes old and unrelated material into the task and wastes tokens.
- **Check:** Every file an agent reports having read is on the list, or the agent explains why it went beyond it.

### 2.4 History is visible but out of the way

- **Rule:** Superseded material is marked as such, points to its replacement, and lives in `archive/`. Context lists never point there unless the task is about history.
- **Why:** Old rationale is valuable; old rules presented as current are dangerous.
- **Check:** No active context list points into `archive/`.

### 2.5 Instructions that ride along are budgeted

- **Rule:** Agent instruction files that load in every session (`MESHIKAH.md`, `CLAUDE.md`, `AGENTS.md`, rules files) have an owner, a review date and a size cap (default 150 lines). They point to the library instead of restating it.
- **Why:** Always-on instructions compete for attention. Past a point, adding a rule makes every rule less reliable.
- **Check:** Each file declares its owner, review date and current size, and the check flags any file over the cap or past its review date.

### 2.6 Humans decide; agents prepare

- **Rule:** Agents draft, implement, test and report. Humans approve scope, design, acceptance, release and anything destructive. An agent can request a decision; it can never record one.
- **Why:** Accountability can't be delegated to a probabilistic system.
- **Check:** Every decision in the record has a human actor.

### 2.7 Evidence, or "not verified"

- **Rule:** A claim of done carries real output: a command and its result, a test run, a deployment ID. Anything not checked is reported as `NOT VERIFIED`.
- **Why:** Confident, illustrative results are the most expensive kind of AI error.
- **Check:** Every acceptance criterion has a result of `PASS`, `FAIL` or `NOT VERIFIED`, with a pointer to the evidence.

### 2.8 Sensitive data never enters context

- **Rule:** Every project declares which data classes it touches, and which tools and models may see each class (§8.1).
- **Why:** Once data is in a prompt or a log, you can't take it back.
- **Check:** The card states its highest data class, and the scanner finds no secrets or personal data in its artifacts.

### 2.9 Process scales with risk

- **Rule:** A typo fix and a security change don't get the same ceremony. The risk level of a card decides which checkpoints and checks apply (Model §5–§6).
- **Why:** Process that is too heavy for small work gets skipped, and then it is skipped for big work too.
- **Check:** Every card has a risk level confirmed by a human, and only that level's checkpoints are required.

## 3. Repository layout

### 3.1 Native layout

```text
repo/
├── MESHIKAH.md            # Always-on orientation for agents (budgeted, ≤150 lines)
├── meshikah.yaml          # Optional config: path mapping, key pattern, data classes
├── library/               # Durable truth
│   ├── index.md           # Map of every current document
│   ├── architecture/
│   ├── data/
│   ├── standards/
│   ├── decisions/         # Decision records (DEC-###)
│   ├── questions/         # Open questions needing a human (Q-###)
│   └── lessons.md         # Reproduced and resolved pitfalls (L-###)
├── work/
│   └── <KEY>/             # One work card per item
│       ├── card.md        # Problem, scope, acceptance (Given / When / Then)
│       ├── plan.md        # Files to touch, files not to touch, test map
│       ├── context.json   # Pointers: what to load, what may change
│       ├── evidence.md    # Results per criterion
│       ├── notes/         # Optional: logs, findings, drafts, handoff notes
│       └── record.jsonl   # Append-only decisions
└── archive/               # Superseded material and closed cards
```

The library is a menu, not a requirement to create empty folders. Create only what is used. `decisions/` and `questions/` are optional additions to the package layout for teams that need formal decision records.

### 3.2 Existing repositories keep their names

MeshikahAI never forces a rename or a migration. If a project already uses `docs/` and `stories/`, `meshikah.yaml` maps them:

```yaml
version: 1
paths:
  library: docs
  work: stories
  archive: docs/archive
key_pattern: "^[A-Z][A-Z0-9]+-\\d+$"
data_classes: [Public, Internal]
instruction_budget: 150
```

Repositories that grew under the Docs Hub pattern (for example nested story folders such as `02-story/00_story_details.md`) keep that structure. The OS defines a **legacy profile** that maps those file names onto card, plan, context and evidence (OS §3.3). Structural migrations are proposed separately and never run automatically.

### 3.3 Several repositories

A team with several repositories may keep a **workspace library** (for example `Projects/library/`) for cross-project practice: this standard, the prompt library, shared lessons. A project never owns another project's rules; project-specific conventions stay in that project.

## 4. Knowledge lifecycle

| State | Meaning | Where |
|---|---|---|
| **Current** | Approved description of the system as it is now, with a source, decision or verification date where relevant | `library/` |
| **Proposed** | Designs and roadmaps not yet approved, labeled as proposals | `library/` (marked) or the card |
| **Decision** | Decision, rationale, approver, date, alternatives, consequences. Immutable; later decisions supersede. | `library/decisions/` |
| **Card delta** | Scope, plan and evidence for one item | `work/<KEY>/` |
| **Promotion** | Durable knowledge from a card becomes current truth through the **Learn** checkpoint (Model §6), linked back to the card | `library/` |
| **Archived** | Superseded or closed; marked, pointing to its replacement, out of active context | `archive/` |

Preserve useful rationale, but always distinguish it from current truth. Don't delete or relocate records without authorization.

### 4.1 Spec-to-release traceability

Every release must trace back to the intent that produced it. For each deployment the record holds a `released` event with:

- the commit containing the final card, plan and `context.json` (the **spec version**);
- the deployed commit or package and the deployment ID;
- the environment;
- the human decisions that authorized it.

A reviewer must be able to answer "which version of which card produced this deployed behavior?" from the repository alone.

## 5. Source of truth and live systems

There is no universal source-of-truth rule. Each project states, in its configuration or extension, which source governs code, configuration, runtime data, and environment-specific behavior. Examples:

- In a version-controlled application, reviewed repository source is the implementation baseline.
- In an org-driven Salesforce workflow, selected metadata may need targeted retrieval from the authorized org.
- Runtime data, deployed configuration and local metadata may have different authorities; document that distinction.

When sources disagree and no rule settles which one wins, work **stops** and a human decides (Model §8, OS §9.3). Nothing is silently overwritten.

## 6. Context loading

### 6.1 Load order (every agent session)

1. **Orient:** `MESHIKAH.md`, `library/index.md`, the card's `context.json`.
2. **Library:** only the documents in `context.json → library`.
3. **Work:** `card.md`, `plan.md`, the files in `context.json → source`, and `git status`.
4. **Verify:** run the checks, record the real output in `evidence.md`, and report.

If the agent needs more, it says what and why before reading it. Where live metadata must be retrieved, an authorized, targeted retrieval happens after `git status` and before the retrieved files are used as a baseline.

### 6.2 `context.json`

```json
{
  "key": "ABC-123",
  "title": "Retry failed sync calls",
  "level": "Standard",
  "data_class": "Internal",
  "library": ["library/index.md", "library/architecture/sync.md"],
  "source": ["src/sync/client.ts"],
  "may_change": ["src/sync/client.ts", "test/sync/*.test.ts"],
  "tests": ["test/sync/client.test.ts"]
}
```

- Paths are repository-relative and must exist, except `may_change` entries the plan creates.
- No path points into `archive/` unless the card is about history.
- **A pointer is not a permission.** Listing a file grants nothing on its own. Actions are governed by the OS action classes (OS §6).

## 7. Templates

The package `templates/` folder holds the starter files. Their required content:

| File | Must contain |
|---|---|
| `MESHIKAH.md` | Owner, review date, budget header; the seven agent rules (load by list, change only `may_change`, real evidence, request never decide, no sensitive data, end-of-session report); project-specific rules only where they differ from the library |
| `card.md` | Key and title; proposed level; highest data class; owner; library links (with why each matters); problem; in scope; out of scope; acceptance in Given/When/Then including at least one negative or boundary case; open questions with owners |
| `plan.md` | Approach; files to touch; files not to touch (always including `library/`, which changes only through Learn); acceptance → test map; steps; risks and rollback |
| `evidence.md` | One row per acceptance criterion, starting as `NOT VERIFIED`; details per criterion: command or steps, expected, actual, result, proof |
| `context.json` | The §6.2 fields |
| `library/index.md` | Only paths that exist, grouped by architecture, data, standards, decisions, lessons; planned documents marked as planned |
| `library/lessons.md` entry | `L-###` title; symptom; root cause; resolution; evidence (card key or proof link). Added only after the fix is verified, through Learn. |

## 8. Security, quality, and verification

The standard sets principles; project CI and platform policy enforce them.

- Don't hardcode secrets or environment-specific identifiers.
- Validate input; use parameterized queries or the platform's safe query APIs.
- Apply least privilege and the project's authorization model.
- Add or update tests for behavior changes, with meaningful positive and negative assertions.
- Run focused tests, then the applicable suite, lint and type checks, and build or deploy validation.
- Follow project coverage thresholds; **coverage alone is not proof of behavior**.
- Report exactly what was run and the result. Never claim unverified test, deployment, compliance or coverage success.

### 8.1 Data classes

| Class | Examples | Rule |
|---|---|---|
| **Public** | Open docs, open-source code | Any approved tool |
| **Internal** | Source code, architecture, sanitized cards | Organization-approved tools and models only; no personal accounts |
| **Confidential** | Customer configuration, non-health personal data | Sanitized identifiers in every artifact; tools approved for confidential data; cloud handoff only where policy allows |
| **Regulated** | Health records (e.g. PHI under HIPAA), payment data, production extracts | Never enters a prompt, log or artifact. Agents work on schema and synthetic data only. |

The card's highest data class sets a floor on its risk level (Model §5) and on the enforcement strength the runtime must provide (OS §6.3).

## 9. Prompt library

Reusable prompts live in the library (for example `library/prompts/`) or the workspace library, each with a stable ID (`P-###`) and a dated history. A prompt points to library documents rather than restating them, names its required inputs and expected outputs, states its verification steps, and never contains secrets, personal data or production data. New prompts become canonical through Learn.

## 10. Human skill portfolio

A person may keep a private, evidence-based capability portfolio. At card close, the owner may record their own contribution (distinguished from AI and teammate contributions), the skills applied, and links to approved evidence. **"No portfolio change" is a valid outcome.** Estimates are labeled until substantiated. The portfolio belongs to the person, contains no credentials, personal data or confidential feedback, and is never shared or committed without the person's consent and company policy allowing it. Metrics in MeshikahAI describe the process, never individuals.

## 11. Governance and safe automation

Adopt incrementally:

1. Assign library owners for the workspace and each project.
2. Index current sources; mark canonical documents, gaps and superseded material.
3. Write each project's source-of-truth and retrieval policy (§5).
4. Run new and active work as cards; don't mass-migrate history without a reviewed plan.
5. Automate only validated rules, after documenting exceptions and owners.
6. Measure before publishing any benefit (§14).
7. Review the standard when tools or practice change.

Any automation (scripts, the CLI, bindings) must be safe by default:

- validate the repository root before writing;
- preview before writing;
- create only missing files; never overwrite, move or delete by default;
- no implicit side effects: no Git writes, no org or network access, no enterprise writes;
- report what was created or skipped, and exit clearly on errors;
- generated content is reviewed before it becomes canonical.

## 12. Salesforce profile

Applies only to Salesforce repositories:

1. Confirm the target org and authenticated alias through approved configuration or with the owner.
2. Run `git status` and protect uncommitted work before any retrieval; retrieval can overwrite local metadata.
3. Retrieve only what the card lists, for example:

   ```bash
   sf project retrieve start --metadata ApexClass:<CLASS_NAME> --target-org <alias>
   sf project retrieve start --metadata LightningComponentBundle:<BUNDLE_NAME> --target-org <alias>
   ```

4. Compare retrieved files with the repository and record differences and provenance in `notes/`.
5. Never deploy, delete or change org data without the human decisions the level requires (Release, and the destructive-change procedure in Model §11.4).
6. Use the project's approved Apex security patterns: sharing, CRUD/FLS checks, user-mode queries and DML where required. Bulkify and respect governor limits.
7. Verify OmniStudio and managed-package metadata support against the installed CLI and plugins.
8. Keep schema snapshots dated, attributed to an org, and free of sensitive data.
9. Health Cloud and other regulated orgs default to the **Regulated** data class for any card that could touch clinical or personal records.

Targeted retrieval is not a blanket requirement for every card. A `context.json` entry never authorizes org access.

## 13. Capability branches and maturity

The library-card-record method is the core. These branches are optional and each is introduced only after ownership, security, failure handling and human-decision boundaries are defined.

| Branch | Capability | Control | Sub-system |
|---|---|---|---|
| 1 | Linting in CI: required card files, Given/When/Then present, links resolve, `context.json` valid, record chain intact, instruction budgets | Deterministic checks first; semantic duplication is never blocking without human review | 3 Quality & Verification |
| 2 | The `mshkh` CLI: `init`, `new`, `lint`, `request`, `decide`, `status` | Preview first; create only missing files; human decisions structurally separate | 6 Toolchain & Runtime |
| 3 | Specialist agent roles beyond Builder and Checker | Only where coordination cost is lower than the value; humans keep every decision | 2 Orchestration |
| 4 | Enterprise-tool synchronization (tracker, wiki, ITSM, portals) | Field-level authority matrix, least privilege, idempotency, retries and conflict queues, audit trail, human approval. Read-only retrieval first. | 4 Governance · 6 Toolchain |
| 5 | Drift telemetry: code inventory vs library | Advisory findings routed to an owner; never rewrites the library automatically | 5 Knowledge & Telemetry |

### 13.1 Maturity sequence

1. **Core:** library, cards, record by hand, human decisions.
2. **Templates and pointers:** standard card templates and `context.json` on every card.
3. **Deterministic linting:** paths, links, structure, record chain; tune before blocking.
4. **CLI and bindings:** `mshkh` and the first tool binding (Claude Code), piloted on real cards.
5. **Integrations and telemetry:** only after authority, privacy, security, conflict handling and support ownership are approved.

**Current position (2026-10-31):** the method was proven by hand in the Docs Hub pilot under its earlier vocabulary (steps 1–2), with partial validators (step 3). The v0.1 package documents and templates exist; no `mshkh` command is implemented yet. Progress is measured by what a real user can do, not by how many components exist.

## 14. What MeshikahAI promises, and what it doesn't

MeshikahAI makes **what an agent reads and may change** repeatable, and makes **who decided, on what evidence** auditable. It intends to improve discoverability, reduce duplicate maintenance, preserve decisions and focus agent context.

It does **not** make AI output deterministic, eliminate hallucination, or guarantee defect-free delivery. Any published benefit (onboarding time, rework, escaped defects, context size, cycle time) needs a **baseline, a period, a sample and a stated method**, with limitations reported.

## 15. Terminology map (framework 1.1 → 2.0)

| 1.1 term | 2.0 term |
|---|---|
| Hub, project hub, `docs/` | Library, `library/` (or mapped via `meshikah.yaml`) |
| Spoke, story packet, `stories/<KEY>/` | Work card, `work/<KEY>/` |
| `00_story_details.md` | `card.md` |
| `01_delta_implementation_plan.md` | `plan.md` |
| `02_acceptance_tests.md` + evidence index | Acceptance in `card.md`; results in `evidence.md` |
| `context_manifest.json` | `context.json` |
| Pipeline log + handoff ledger + `ledger.jsonl` | `record.jsonl` |
| `99-historical/` | `archive/` |
| `AGENTS.md` (orientation) | `MESHIKAH.md` (tool files such as `AGENTS.md`/`CLAUDE.md` may point to it) |
| Known gotchas `KG-###` | Lessons `L-###` in `library/lessons.md` |
| Tiers T0 / T1 / T2 / T3 | Levels Light / Standard / Heavy / Critical |
| Gates G1 / G2 / G3 / G5 / R / G6 | Checkpoints Scope / Plan / Review / Accept / Release / Learn |
| Gate G4 Security | Separate security review inside Critical (decided as part of Accept and Release) |
| Orchestrator / responsible engineer | Owner |
| Product owner, architect, QA/release, security, documentation owner | Approver (by checkpoint) |
| SoftwareEngineer-AI, Agent 3 Developer | Builder |
| Agent 4 QA & Security Auditor | Checker |
| Knowledge Steward | Librarian |
| Agent 1 BA, Agent 2 Architect | Optional specialist roles (Model §18) |
| Data classes D0 / D1 / D2 / D3 | Public / Internal / Confidential / Regulated |
| Command classes K0–K6 | Action classes: Read, Verify, Write: local, Write: shared, Write: external, Destructive |
| Context-OS | MeshikahAI runtime (the Operating System layer) |

## 16. Document history

| Version | Change |
|---|---|
| Docs Hub 3.1 | Source standard |
| 1.0 | Generalized from Docs Hub 3.1; client identifiers removed |
| 1.1 | Principle on standing instructions; traceability; data classes D0–D3; CLI renamed MeshikahOS-cli (`mshkh`) |
| **2.0** | Aligned with MeshikahAI package v0.1: library / work card / record model; nine principles with rule, why and check; native layout with `meshikah.yaml` mapping for existing repositories; plain data classes; Light–Critical levels and Scope–Learn checkpoints by reference; capability branches renamed to the CLI MVP; terminology map. Breaking rename of all file and term names. |
