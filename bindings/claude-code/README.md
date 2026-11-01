# Binding: Claude Code (planned, roadmap 0.4)

**Status: not written.** Each mechanism below is an expectation to verify against Claude Code's current documentation before anything is published.

| # | Capability | Expected mechanism | Verified |
|---|---|---|---|
| 1 | Always-on orientation | `CLAUDE.md` that points to `MESHIKAH.md` | No |
| 2 | Fresh Checker sessions | A Checker subagent or a separate session given only card, plan, diff and evidence | No |
| 3 | Path-scoped writes | Permission rules derived from `context.json → may_change` | No |
| 4 | Ask/deny per action class | Permission allow/ask/deny rules; a pre-action hook calling `mshkh policy check` (later) | No |
| 5 | Request, never decide | Deny rules for `mshkh decide`, `mshkh release`, `mshkh correct`; set `MESHIKAH_AGENT=1` for agent sessions | No |
| 6 | Different model for the Checker | Model selection on the Checker | No |

Done when: one Standard card is built and checked in Claude Code, with the record showing human decisions only.
