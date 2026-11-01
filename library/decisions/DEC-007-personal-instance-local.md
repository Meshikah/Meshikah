# DEC-007 · Personal instance: local Git with encrypted backup

- **Date:** 2026-11-01
- **Approver:** Armando
- **Status:** Accepted. Resolves Q-003. Applies DEC-004.

**Decision.** The personal instance (`mi-vida`) is a local Git repository outside OneDrive (for example `C:\dev\mi-vida`). Backups go to an encrypted volume or encrypted archive. Financial and other personal data never go to a cloud service unencrypted.

**Rationale.** Personal finance is Confidential data, and account identifiers are Regulated (never stored). Git inside OneDrive conflicts with sync.

**Alternatives.** Private GitHub remote with client-side encryption, e.g. git-crypt or age (possible later); private GitHub without encryption (rejected).

**Consequences.** The first finance cards can start. Backup is a manual step until it is scripted.
