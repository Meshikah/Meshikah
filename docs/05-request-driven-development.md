# 05 · Request-driven development

**Status: draft proposal.** It extends the method beyond software. It doesn't change `01`–`04`; if it ever conflicts with them, they win until this document is approved.

## The idea

Every piece of work starts as a **request**: a need, stated by a person, with an outcome that can be checked. The request becomes a work card, and the context is assembled **for the request**, not the other way around.

```text
need ─▶ request ─▶ card ─▶ context (pointers) ─▶ action ─▶ evidence ─▶ human decision ─▶ lesson
  ▲                                                                                       │
  └───────────────────────────── library (durable truth) ◀──────── Learn ◀────────────────┘
```

This is the same loop for a software story and for a personal-finance goal. Only the pack changes.

## A systems view

Systems theory gives the design its vocabulary. These are design principles, not decoration:

| Systems concept | In MeshikahAI |
|---|---|
| **Boundary** | The card: what is in scope, what is out, which files may change |
| **Goal** | The request's acceptance criteria |
| **Stocks** | The library (accumulated knowledge); in finance, also balances and commitments |
| **Flows** | Cards moving through checkpoints; in finance, money in and out |
| **Feedback loop** | Evidence → human decision → lesson → library → better next card |
| **Controller** | The human who decides; agents are actuators and sensors, never the controller |
| **Requisite variety** | Process scales with risk: Light for small requests, Critical for dangerous ones |

## Structure: area → project → epic → card

Requests group naturally, but the folder structure stays flat:

| Level | Example (software) | Example (finance) |
|---|---|---|
| **Area** | Professional | Finance |
| **Project** | Engagement Centers CRM | Debt-free 2027 |
| **Epic** | Log-a-meeting integration | Refinance the car loan |
| **Card** | ABC-123 Retry failed sync calls | FIN-7 Compare three refinance offers |

- The card key is the identity and the folder name (`work/<KEY>/`).
- Area, project and epic are **metadata** in the card header and in `library/index.md`, never nested folders. Moving a card between epics is a metadata edit, not a file move.

## One kernel, many implementations

| Layer | Owns | Stays the same across domains? |
|---|---|---|
| **Kernel** | Principles, card and record format, checkpoints, data classes, `mshkh` | Yes |
| **Pack** | Templates, risk signals, what each checkpoint means, domain checks | No, one per domain |
| **Instance** | A repository using one or more packs, with its own library | No, one per person or team |

## What must not change when the domain changes

- Humans decide; agents prepare.
- Evidence, or `NOT VERIFIED`.
- Sensitive data never enters context. Personal finance and health are **Confidential** at minimum; account numbers, identity documents and medical records are **Regulated** and never enter any artifact.
- Process scales with risk. Most personal requests are **Light**; a life that needs a checkpoint for every errand is a life that abandons the system.

## Open questions

- Does the method hold outside software? Test: three real finance cards run by hand before the pack goes past draft.
- Should one person run one instance with several packs, or one instance per area? Default proposal: one private instance, several packs.
- Where does an instance live for privacy: local-only Git, or an encrypted remote?
