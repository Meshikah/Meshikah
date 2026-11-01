# DEC-003 · CLI skeleton in Python

- **Date:** 2026-10-31
- **Approver:** Armando
- **Status:** Accepted for the skeleton; final packaging still open (Q-001)

**Decision.** Start `mshkh` in Python 3.11+ with `pyyaml` and `jsonschema` only.

**Rationale.** Pilot validators are already Python; it runs on Windows, macOS and Linux; small dependency surface.

**Alternatives.** TypeScript/Node; a compiled single binary (Go or Rust) for locked-down laptops.

**Consequences.** If enterprise laptops block Python, revisit packaging (zip app or a compiled port) before 1.0.
