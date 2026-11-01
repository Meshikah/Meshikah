# 02 · Operating model

Who does what, when, and with what proof.

## Roles

| Role | Type | Owns |
|---|---|---|
| **Owner** | Human | The outcome. Frames the problem, sets the risk level, reviews plans and diffs, and runs releases. |
| **Approver** | Human | The decision at a checkpoint: business, architecture, security or release, depending on the checkpoint. |
| **Builder** | AI agent | Explores, plans, implements and tests within the card's scope. Reports honestly. |
| **Checker** | AI agent | Independently verifies the builder's work in a fresh session, ideally on a different model. |
| **Librarian** | AI agent or human | At close, proposes what should be promoted into the library. |

One person can hold several human roles. The roles stay distinct even when the person is the same (see "Small teams").

## Risk levels

The owner proposes a level when the card opens and a human confirms it before work starts.

| Level | Typical signals | Shape |
|---|---|---|
| **Light** | Typo, comment, docs-only, one-line config | Builder only |
| **Standard** | One component, clear acceptance, no schema or security impact | Builder, then an independent Checker |
| **Heavy** | Several components, data-contract change, unclear requirements | Builder with an explicit plan review, plus Checker and Librarian |
| **Critical** | Security, permissions, regulated data, integrations, migrations, destructive change | Everything in Heavy, plus a separate security review and a second human at Release |

- Anyone who finds signs of a higher level stops and returns the card to the owner.
- Lowering a level needs human agreement.
- Data sets a floor: Regulated data means Critical, and Confidential data means at least Standard.

## Checkpoints

A checkpoint is a human decision, recorded with who decided, when and on what evidence.

| Checkpoint | Question | Evidence | Light | Standard | Heavy | Critical |
|---|---|---|---|---|---|---|
| **Scope** | Do we understand and bound the work? | `card.md` with testable acceptance | — | ✓ | ✓ | ✓ |
| **Plan** | Is the approach sound and the change bounded? | `plan.md`: files to touch, files not to touch, test map | — | — | ✓ | ✓ |
| **Review** | Does the diff match the plan? | Diff against base, test and lint output | ✓ | ✓ | ✓ | ✓ |
| **Accept** | Does it meet the contract? | `evidence.md`, with every criterion classified | — | ✓ | ✓ | ✓ |
| **Release** | May this exact change be deployed? | Package matching the diff, dry run, rollback note | if deployed | if deployed | if deployed | ✓ (2 humans) |
| **Learn** | What becomes durable knowledge? | Promotion proposal with links back to the card | — | — | ✓ | ✓ |

Agents may **request** a checkpoint. Only humans **decide** one. A rejected checkpoint sends the card back for rework, and after two rework rounds the owner must re-scope or re-plan.

## Flow

```text
open → set level → [Scope] → [Plan] → build + test → [Review]
     → independent check → [Accept] → [Release] → [Learn] → archive
```

Checkpoints that don't apply to the level are skipped.

## Small teams (one person, several hats)

When the person who reviews is also the person who built or planned, independence comes from somewhere else:

| Level | Compensating control |
|---|---|
| Light | None needed |
| Standard | The Checker runs in a fresh session on a different model family |
| Heavy | The Standard control, plus the plan is reviewed at least one working session after it was written |
| Critical | The Standard control, plus a second human for security and Release. With no second human, the work is not run as Critical. |

The record notes which control was used.

## Evidence format

```markdown
- Criterion:   <Given / When / Then reference>
- Environment: <where it ran>
- Command or steps:
- Expected:
- Actual:
- Result:      PASS | FAIL | NOT VERIFIED
- Proof:       <log path, job ID, screenshot>
```

## Definition of done

A card is done when:
- only planned files changed;
- every acceptance criterion has a result and proof;
- a human decided each required checkpoint;
- the owner understands every change;
- the next session could resume from the card and the library alone.
