# Bindings

A binding implements the runtime in one tool. It states how the tool provides each capability and marks every gap honestly (reference OS §12):

| # | Capability |
|---|---|
| 1 | Always-on orientation (`MESHIKAH.md` or the tool's equivalent pointing to it) |
| 2 | Fresh, isolated sessions for the Checker |
| 3 | Path-scoped writes (`may_change`) |
| 4 | Ask/deny rules per action class |
| 5 | A way for agents to request, but not decide, checkpoints |
| 6 | A different model for the Checker |

| Tool | Status |
|---|---|
| [Claude Code](claude-code/) | Planned, roadmap 0.4 |
| Others | Not started |
