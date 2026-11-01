# Contributing

This repository runs on its own method.

1. **Every change starts as a request** and becomes a card in `work/<KEY>/` (keys `MSH-<n>`). Copy `templates/work-card/` until `mshkh new` exists.
2. **Set a level** (Light, Standard, Heavy, Critical) and get it confirmed by a human before work starts.
3. **List context in `context.json`.** Agents load that list and nothing else by default.
4. **Change only files in `may_change`.** Anything else: stop and ask.
5. **Record evidence** in `evidence.md`: real command output, or `NOT VERIFIED`.
6. **Request checkpoints; humans decide them.** Append events to `record.jsonl` (format: `docs/03-runtime.md`; schema: `kernel/schemas/record-event.schema.json`).
7. **Library changes go through Learn.** Durable knowledge lands in `library/` only after a human decision.

Branches: `<type>/<KEY>-<short-purpose>`. Commit messages state the card key, the scope and why.

Never commit secrets, personal data or real financial data. Examples use synthetic data only.
