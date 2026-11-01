# MeshikahAI

**Request-driven context engineering for people who work with AI agents.**

MeshikahAI is a working method plus a small toolchain. Every piece of AI-assisted work starts as a **request** and becomes a **work card**. For each card it answers three questions:

1. **What should the agent read?** Exactly the context the request needs, and nothing stale or unrelated.
2. **What may it change?** A declared set of files and actions, checked before and after.
3. **Who decided it was done, and on what evidence?** A human, recorded, with proof attached.

It started as context management for software teams. The kernel is domain-agnostic, so the same method can run other kinds of projects through **packs**: software engineering first, personal finance next.

## The shape

```text
REQUEST ──▶ WORK CARD (work/<KEY>/) ──appends──▶ RECORD (record.jsonl)
               │   ▲                               human decisions, append-only
     points to │   │ promotes back (human, via Learn)
               ▼   │
            LIBRARY (library/)  — durable truth, one copy
```

| Concept | What it is |
|---|---|
| **Library** | The one place durable knowledge lives |
| **Work card** | One folder per request: the delta, the acceptance contract, the evidence |
| **Record** | Append-only log of requests and human decisions for a card |
| **Pack** | Domain configuration on top of the kernel: templates, risk signals, checkpoint meanings, checks |

## Repository map

| Path | What's there |
|---|---|
| [`docs/`](docs/) | The method: principles, operating model, runtime, CLI MVP, request-driven development, packs |
| [`docs/reference/`](docs/reference/) | Full reference framework 2.0 (Standard, Model, Operating System, sub-systems, CLI spec) |
| [`kernel/schemas/`](kernel/schemas/) | JSON Schemas for `context.json`, `record.jsonl` lines and `meshikah.yaml` |
| [`templates/`](templates/) | Kernel templates: `MESHIKAH.md` and a work card |
| [`packs/`](packs/) | Domain packs: `software` (default), `finance` (draft) |
| [`cli/`](cli/) | The `mshkh` command-line tool (Python, skeleton only) |
| [`bindings/`](bindings/) | Tool bindings; Claude Code first |
| [`examples/`](examples/) | Demo repositories with synthetic data only |
| [`library/`, `work/`, `archive/`](library/index.md) | This repository's own development, run with MeshikahAI |

This repository is **dogfooded**: its own work is tracked as cards in `work/`. Closed cards are in `archive/`: [`MSH-1`](archive/MSH-1/card.md) (the scaffold) and [`MSH-2`](archive/MSH-2/card.md) (`mshkh` 0.2: init, new, lint). The current card is [`MSH-3`](work/MSH-3/card.md) (lint-clean examples).

## Status

Version 0.1, draft. Method documents, templates, schemas and a CLI skeleton. **No `mshkh` command is implemented yet**; every command in `docs/04-cli-mvp.md` is a contract to build and test. See [`ROADMAP.md`](ROADMAP.md).

## License

© 2026 Armando. All rights reserved until a license is chosen. See [`LICENSE.md`](LICENSE.md).
