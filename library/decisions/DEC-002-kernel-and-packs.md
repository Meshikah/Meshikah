# DEC-002 · Kernel plus packs

- **Date:** 2026-10-31
- **Approver:** Armando
- **Status:** Accepted (finance pack stays draft)

**Decision.** Split the product into a domain-agnostic **kernel** (principles, card and record formats, schemas, `mshkh`) and domain **packs** (templates, risk signals, checkpoint meanings, checks). Software is the default pack; finance is the first non-software pack.

**Rationale.** The vision covers more than software (request-driven development across life areas). A kernel/pack split lets the method grow without forking it.

**Alternatives.** Separate products per domain (rejected: duplicated core); one generic template set for everything (rejected: domain risks differ, e.g. money movement).

**Consequences.** The kernel may not contain domain specifics. A pack may narrow kernel rules, never loosen them. Finance stays draft until three real cards are run by hand.
