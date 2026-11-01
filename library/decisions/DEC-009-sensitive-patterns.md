# DEC-009 · Default sensitive-data patterns

- **Date:** 2026-11-01
- **Approver:** Armando
- **Status:** Accepted. Resolves Q-CLI-3.

**Decision.** `mshkh lint` ships with these default patterns: secrets and keys (tokens, private keys, connection strings), email addresses, phone numbers, payment card numbers (validated with Luhn), bank identifiers (CLABE, IBAN), and Mexican personal IDs (CURP, RFC). Health-record patterns are off by default; packs that need them turn them on.

**Rationale.** It covers the common leaks across domains while keeping false positives low for software work. Health patterns are noisy outside health projects.

**Alternatives.** Everything on by default (rejected: noise); secrets only (rejected: misses personal data).

**Consequences.** A hit prints its location, never its value (exit 6). Projects may add patterns, never remove the defaults. The finance pack inherits all defaults.
