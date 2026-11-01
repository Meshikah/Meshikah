# 01 · Principles

These nine principles are the core of MeshikahAI. Every other document applies them; none may weaken them. Each principle has a rule, the reason for it, and a way to check it.

## 1. One copy of durable truth

- **Rule:** Architecture, data models, standards and hard-won lessons live in the library, once. Everything else links to them.
- **Why:** Two copies of a rule become two different rules the first time one changes.
- **Check:** No work card contains a verbatim copy of a library document.

## 2. Work cards carry the delta only

- **Rule:** A work card says what changes for this item, how we will know it works, and what proved it. It does not restate the system.
- **Why:** Cards are read by agents under a tight attention budget. Every repeated paragraph is noise and a future contradiction.
- **Check:** A card can be read in full in a few minutes and has links, not copies.

## 3. Load by pointer, not by crawl

- **Rule:** Each card lists the exact library documents and source files in scope (`context.json`). Agents load that list, in a fixed order, and nothing else by default.
- **Why:** Ingesting a whole repository mixes old and unrelated material into the task and wastes tokens.
- **Check:** Every file an agent reports having read is on the list, or the agent explains why it went beyond it.

## 4. History is visible but out of the way

- **Rule:** Superseded material is marked as such, points to its replacement, and lives in `archive/`. Context lists never point there unless the task is about history.
- **Why:** Old rationale is valuable; old rules presented as current are dangerous.
- **Check:** No active context list points into `archive/`.

## 5. Instructions that ride along are budgeted

- **Rule:** Agent instruction files that load in every session (`MESHIKAH.md`, `CLAUDE.md`, `AGENTS.md`, rules files) have an owner, a review date and a size cap (default 150 lines). They point to the library instead of restating it.
- **Why:** Always-on instructions compete for attention. Past a point, adding a rule makes every rule less reliable.
- **Check:** Each file declares its owner, review date and current size, and the check flags any file over the cap or past its review date.

## 6. Humans decide; agents prepare

- **Rule:** Agents draft, implement, test and report. Humans approve scope, design, acceptance, release and anything destructive. An agent can request a decision; it can never record one.
- **Why:** Accountability can't be delegated to a probabilistic system.
- **Check:** Every decision in the record has a human actor.

## 7. Evidence, or "not verified"

- **Rule:** A claim of done carries real output: a command and its result, a test run, a deployment ID. Anything not checked is reported as `NOT VERIFIED`.
- **Why:** Confident, illustrative results are the most expensive kind of AI error.
- **Check:** Every acceptance criterion has a result of `PASS`, `FAIL` or `NOT VERIFIED`, with a pointer to the evidence.

## 8. Sensitive data never enters context

- **Rule:** Every project declares which data classes it touches, and which tools and models may see each class.

  | Class | Examples | Rule |
  |---|---|---|
  | Public | Open docs, open-source code | Any approved tool |
  | Internal | Source code, architecture, sanitized cards | Organization-approved tools only |
  | Confidential | Customer configuration, non-health personal data | Sanitized identifiers in every artifact |
  | Regulated | Health records, payment data, production extracts | Never enters a prompt, log or artifact. Agents work on schema and synthetic data only. |

- **Why:** Once data is in a prompt or a log, you can't take it back.
- **Check:** The card states its highest data class, and the scanner finds no secrets or personal data in its artifacts.

## 9. Process scales with risk

- **Rule:** A typo fix and a security change don't get the same ceremony. The risk level of a card decides which checkpoints and checks apply (see `02`).
- **Why:** Process that is too heavy for small work gets skipped, and then it is skipped for big work too.
- **Check:** Every card has a risk level confirmed by a human, and only that level's checkpoints are required.

---

### What MeshikahAI does not promise

It makes **what an agent reads and may change** repeatable. It does not make AI output deterministic, and it does not guarantee defect-free delivery. That is why evidence and human decisions stay mandatory. Any published benefit needs a baseline, a period, a sample and a stated method.
