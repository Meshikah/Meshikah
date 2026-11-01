# 03 · Runtime

How MeshikahAI lives in a real repository. Tool-agnostic: any agent (Claude Code, Cursor, Copilot, others) connects through a *binding* that maps these contracts to the tool's own features.

## Repository layout

```text
repo/
├── MESHIKAH.md            # Always-on orientation for agents (budgeted, ≤150 lines)
├── meshikah.yaml          # Optional config: path mapping, key pattern, data classes
├── library/               # Durable truth
│   ├── index.md           # Map of every current document
│   ├── architecture/
│   ├── data/
│   ├── standards/
│   └── lessons.md         # Reproduced and resolved pitfalls
├── work/
│   └── <KEY>/             # One work card per item
│       ├── card.md        # Problem, scope, acceptance (Given / When / Then)
│       ├── plan.md        # Files to touch, files not to touch, test map
│       ├── context.json   # Pointers: what to load, what may change
│       ├── evidence.md    # Results per criterion
│       ├── notes/         # Optional: logs, findings, drafts
│       └── record.jsonl   # Append-only decisions
└── archive/               # Superseded material and closed cards
```

**Existing repositories keep their names.** If a project already uses `docs/` and `stories/`, `meshikah.yaml` maps them:

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

## Load order (every agent session)

1. **Orient:** `MESHIKAH.md`, `library/index.md`, the card's `context.json`.
2. **Library:** only the documents in `context.json → library`.
3. **Work:** `card.md`, `plan.md`, the files in `context.json → source`, and `git status`.
4. **Verify:** run the checks, record the real output in `evidence.md`, and report.

## `context.json`

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

Rules:
- Paths are repo-relative and must exist. The exception is `may_change` entries the plan creates.
- No path points into `archive/` unless the card is about history.
- **A pointer is not a permission.** Listing a file grants nothing on its own; actions are governed below.

## `record.jsonl`

One JSON object per line, never edited, never deleted.

```json
{"at":"2026-11-02T17:00:00Z","card":"ABC-123","event":"requested","checkpoint":"Review","by":"agent:builder","evidence":["work/ABC-123/evidence.md"],"prev":"sha256:…"}
{"at":"2026-11-02T18:10:00Z","card":"ABC-123","event":"decided","checkpoint":"Review","decision":"approved","by":"human:armando","prev":"sha256:…"}
```

| Event | Who may write it |
|---|---|
| `opened`, `requested`, `note`, `blocked`, `unblocked` | Human or agent |
| `level_confirmed`, `decided`, `released`, `correction` | Human only |

- `prev` is the hash of the previous line, so an edit or a deletion is detectable. The record is tamper-evident, not tamper-proof; Git history is the second line of defense.
- Current state is derived from the record. Any summary view is generated from it and never edited by hand.
- Corrections are new `correction` events that reference the line they supersede.

## Action classes

Bindings map every tool action to a class and enforce the default. Projects may tighten a default, never loosen it.

| Class | Examples | Default |
|---|---|---|
| **Read** | Read files, search, `git status`, `git diff` | Allow |
| **Verify** | Local tests, lint, type checks, dry runs | Allow |
| **Write: local** | Edit files listed in `may_change` | Allow inside the list; ask outside it |
| **Write: shared** | `git commit`, `git push`, branch operations | Ask |
| **Write: external** | Deployments, data changes, tracker or wiki writes | Human only, per action |
| **Destructive** | Deletes, history rewrites, secrets files | Deny |

Where a tool can enforce a rule in configuration (deny rules, hooks, sandboxes), the binding uses that. Where it can only instruct, the Review checkpoint verifies the result through the diff.

## Stop conditions

Any agent or tool stops and hands back to the owner when:
- the target environment can't be confirmed;
- a needed file is outside `may_change`;
- `context.json` is invalid;
- secrets or sensitive data appear;
- the library and the live system disagree and no rule settles which one wins;
- required checks can't run;
- the record is inconsistent;
- the requested action needs a checkpoint that hasn't been decided.

## Bindings

A binding is a short document plus configuration that implements this runtime in one tool. It states how the tool provides each of these:

| # | Capability |
|---|---|
| 1 | Always-on orientation (`MESHIKAH.md` or the tool's equivalent) |
| 2 | Fresh, isolated sessions for the Checker |
| 3 | Path-scoped writes |
| 4 | Ask/deny rules per action class |
| 5 | A way for agents to request, but not decide, checkpoints |
| 6 | A different model for the Checker |

Every gap is marked honestly. The first planned binding is Claude Code.
