# DEC-005 · CLI distribution: Python with pipx and a zip app

- **Date:** 2026-11-01
- **Approver:** Armando
- **Status:** Accepted. Resolves Q-001. Completes DEC-003.

**Decision.** `mshkh` stays in Python 3.11+. It ships two ways: `pipx install mshkh`, and a single-file zip app for machines without a package manager. A compiled port (Go or Rust) is considered only if a real pilot customer cannot run Python.

**Rationale.** It keeps the existing skeleton and tests, needs no admin rights, and adds no build pipeline before there is demand for one.

**Alternatives.** Compiled binary from 0.2 (rejected: rewrite cost, no evidence it's needed yet); postpone (rejected: blocks release planning).

**Consequences.** Packaging is checked again before roadmap 1.0, using pilot feedback.
