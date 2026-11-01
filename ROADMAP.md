# Roadmap

Progress is measured by what a real user can do, not by how many components exist.

## Kernel and software pack

| Version | Scope | Done when |
|---|---|---|
| **0.1** | Method documents, templates, schemas, CLI skeleton (this commit) | A reader can run a work card by hand from the docs alone |
| **0.2** | `mshkh init`, `new`, `lint` | MVP tests 1–4 and 7–9 pass |
| **0.3** | `mshkh request`, `decide`, `status`; hash-chained record; gap commands (`decide level`, `release`, `correct`) | MVP tests 5–6 pass; one card run end to end |
| **0.4** | Claude Code binding: orientation file, Checker setup, permission rules, hook calling `mshkh` | One Standard card built and checked in Claude Code |
| **0.5** | Demo repository with synthetic data and a 5-minute walkthrough | Shown to 3 outside engineers; their feedback recorded |
| **1.0** | First paid pilot with a measured baseline | Before/after numbers with period, sample and method |

## Packs

| Version | Scope | Done when |
|---|---|---|
| **finance 0.1** | Pack draft: templates, risk signals, data-class defaults (this commit) | Three real personal-finance cards run by hand in a private instance |
| **finance 0.2** | Lessons from those cards folded back into the pack | The method holds outside software, or the pack is dropped |

## Not now

- Writes to trackers, wikis, banks or deployment systems.
- Dashboards or servers.
- Multi-agent specialist pipelines beyond Builder and Checker.
- More life domains (health, family) before finance proves the kernel generalizes.
