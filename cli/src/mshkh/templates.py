"""Built-in kernel templates, used when a repository has no templates of its own.

They mirror templates/ in the product repository. Tokens: {{KEY}}, {{TITLE}}, {{LEVEL}}, {{DATA_CLASS}}.
"""

CARD = """# {{KEY}} · {{TITLE}}

- Level: {{LEVEL}} (proposed; a human confirms it)
- Highest data class: {{DATA_CLASS}}
- Owner: <name>

## Library links
- <library/...> — why it matters here

## Problem
<What is wrong or missing, for whom>

## In scope
-

## Out of scope
-

## Acceptance
### 1. <name>
- GIVEN <precondition>
- WHEN <action>
- THEN <observable result>

### 2. <negative or boundary case>
- GIVEN
- WHEN
- THEN

## Open questions
- <question> — owner: <name>
"""

PLAN = """# Plan · {{KEY}}

## Approach
<One paragraph: what changes and why this way>

## Files to touch
| File | Change |
|---|---|

## Files not to touch
- library/ (changes only through Learn)
-

## Acceptance → test map
| Acceptance | Test | Type |
|---|---|---|

## Steps
1.

## Risks and rollback
-
"""

EVIDENCE = """# Evidence · {{KEY}}

| Acceptance | Result | Proof | Environment | Date |
|---|---|---|---|---|
| 1 | NOT VERIFIED | | | |
| 2 | NOT VERIFIED | | | |

## Details

### Acceptance 1
- Command or steps:
- Expected:
- Actual:
- Result: PASS | FAIL | NOT VERIFIED
- Proof:
"""

CONTEXT = """{
  "key": "{{KEY}}",
  "title": "{{TITLE}}",
  "level": "{{LEVEL}}",
  "data_class": "{{DATA_CLASS}}",
  "library": ["{{INDEX}}"],
  "source": [],
  "may_change": [],
  "tests": []
}
"""

NOTES = "Logs, findings and handoff notes for {{KEY}} (`NN_<topic>.md`).\n"

MESHIKAH = """<!-- owner: <name> · review by: <YYYY-MM-DD> · budget: 150 lines -->
# MESHIKAH.md — agent orientation

You are working in a MeshikahAI repository.

1. Read `library/index.md`, then the work card's `context.json`.
2. Load only what `context.json` lists. If you need more, say what and why before reading it.
3. Change only files in `may_change`. Anything else: stop and ask.
4. Run the checks and write the real output to `evidence.md`. If something wasn't checked, write `NOT VERIFIED`.
5. You may request a checkpoint (`mshkh request`). Never record a decision.
6. Never put secrets, personal data or regulated data in any file, prompt or log.
7. End every session with: what changed, which files, which tests passed or failed, and what is still open.

Project-specific rules:
- <add only what differs from the library; link, don't copy>
"""

INDEX = """# Library index

Map of every current document. List only paths that exist; mark planned documents as planned.

## Architecture

## Data

## Standards

## Decisions

## Lessons
- [Lessons](lessons.md)
"""

LESSONS = """# Lessons

Reproduced and resolved pitfalls. Add an entry only after the fix is verified, through Learn.

<!-- ### L-001: <short title>
- **Symptom:**
- **Root cause:**
- **Resolution:**
- **Evidence:** -->
"""

CONFIG = """version: 1
paths:
  library: library
  work: work
  archive: archive
  index: library/index.md
profile: native
key_pattern: "^[A-Z][A-Z0-9]+-\\\\d+$"
data_classes: [Public, Internal]
instruction_budget: 150
instruction_files: [MESHIKAH.md, CLAUDE.md, AGENTS.md]
checks:
  blocking: [context, links, record, sensitive]
  advisory: [card-files, acceptance, budget, archive-refs]
"""
