# DEC-008 · Human-decision gap commands join the MVP in 0.3

- **Date:** 2026-11-01
- **Approver:** Armando
- **Status:** Accepted. Resolves Q-CLI-4 (reference CLI spec §15).

**Decision.** Three commands join the MVP in roadmap 0.3: `mshkh decide <KEY> level --set <Level>`, `mshkh release <KEY> …` and `mshkh correct <KEY> …`. They use the same human-only controls as `decide`: interactive terminal, typed confirmation, and refusal when `MESHIKAH_AGENT=1`.

**Rationale.** Without them, `level_confirmed`, `released` and `correction` events are written by hand, which is error-prone (hash chain) and is exactly what the CLI exists to make safe.

**Consequences.** `docs/04-cli-mvp.md` and the roadmap list them. Until 0.3, these events are written by hand, at a human's dictation (`MESHIKAH.md` rule 5), and `lint` validates them.
