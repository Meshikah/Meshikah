<!-- owner: Armando · review by: 2027-01-31 · budget: 150 lines -->
# MESHIKAH.md — agent orientation

You are working in the MeshikahAI product repository. It is developed with its own method.

1. Read `library/index.md`, then the work card's `context.json` in `work/<KEY>/`.
2. Load only what `context.json` lists. If you need more, say what and why before reading it.
3. Change only files in `may_change`. Anything else: stop and ask.
4. Run the checks and write the real output to `evidence.md`. If something wasn't checked, write `NOT VERIFIED`.
5. You may request a checkpoint (append a `requested` event, or `mshkh request` once it exists). Never record a decision.
6. Never put secrets, personal data, real financial data or regulated data in any file, prompt or log. Examples are synthetic.
7. End every session with: what changed, which files, which tests passed or failed, and what is still open.

Project-specific rules:
- `docs/01`–`04` are the short, product-facing method; `docs/reference/` is the full reference. If they disagree, raise an open question; don't silently fix one to match the other.
- The kernel (`kernel/`, `templates/`, `cli/`) must stay domain-agnostic. Domain specifics belong in `packs/<domain>/`.
- `mshkh` makes no AI calls and no network calls.
