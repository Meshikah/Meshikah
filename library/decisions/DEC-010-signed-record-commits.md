# DEC-010 · Signed commits for Critical records

- **Date:** 2026-11-01
- **Approver:** Armando
- **Status:** Accepted. Resolves Q-CLI-5.

**Decision.** A commit that changes `record.jsonl` of a **Critical** card must be signed. CI rejects unsigned changes to those records. For other levels signing is optional.

**Rationale.** The hash chain detects edits but can't show who made a decision. A signature ties Critical decisions to a person at low cost.

**Alternatives.** Optional everywhere (rejected for Critical); mandatory everywhere (rejected: friction on light work).

**Consequences.** Contributors working on Critical cards need commit signing set up (SSH or GPG). The CI check is added with `lint` in roadmap 0.2–0.3.
