# DEC-004 · Product repository separate from personal instances

- **Date:** 2026-10-31
- **Approver:** Armando
- **Status:** Accepted

**Decision.** This repository holds the product only: method, kernel, packs, CLI, bindings and synthetic examples. Personal use (for example a private finance instance) lives in a **separate, private, local-first** repository that uses this one.

**Rationale.** Personal and financial data must never enter the product repository (principle 8). It also keeps intellectual property clean: nothing from client work or personal life lands here.

**Consequences.** Examples use synthetic data only. `.gitignore` excludes `.env*`, `.meshikah/` and `private/` folders as a backstop, not as the control.
