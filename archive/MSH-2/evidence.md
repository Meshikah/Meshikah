# Evidence · MSH-2

| Acceptance | Result | Proof | Environment | Date |
|---|---|---|---|---|
| 1 | PASS | Windows 11 (10.0.26300) + Python 3.11.9: 35 passed, 1 xfailed; Linux + Python 3.11.18: 33 passed, 1 xfailed. Same steps as CI | Windows and Linux, Python 3.11 | 2026-11-01 |
| 2 | PASS | `test_3_new_twice_skips_and_keeps_edits`, `test_init_preview_then_apply_then_skip` | Linux, Python 3.10.12 | 2026-11-01 |
| 3 | PASS | `test_8_token_like_string_exits_6` asserts the value is absent from stdout and stderr | Linux, Python 3.10.12 | 2026-11-01 |

## Details

### Acceptance 1 — MVP tests 1–4 and 7–9 pass
- Command or steps: `cd cli && python -m pytest -q`
- Expected: tests 1, 2, 3, 4, 7, 8 pass without xfail; CI green on Windows and Linux (test 9)
- Actual, Linux, Python 3.11.18 (2026-11-01T17:17:46Z), reproducing the CI steps in a fresh venv (`pip install -e cli pytest`, then `python -m pytest -q` in `cli/`): `33 passed, 1 xfailed in 0.48s`. `mshkh --version` → `mshkh 0.1.0.dev0`; `mshkh lint` on this repository → `0 blocking, 0 advisory`, exit 0.
- Actual, Linux, Python 3.10.12: `33 passed, 1 xfailed`.
- Tests 1–5, 7 and 8 pass; 6 stays xfail by design (checkpoint order is roadmap 0.3).
- Actual, Windows 10.0.26300, Python 3.11.9 (2026-11-01 11:22 local), same steps run locally with `.meshikah/windows-check.cmd` because GitHub Actions is blocked by an account billing lock: `PIP_EXIT=0`; `35 passed, 1 xfailed in 15.50s`, `PYTEST_EXIT=0`; `mshkh 0.1.0.dev0`; `mshkh lint` → `0 blocking, 0 advisory`, `LINT_EXIT=0`. The two extra passing tests are the dogfood schema checks for card MSH-3, created after the Linux run.
- Result: PASS
- Proof: `.meshikah/windows-check.log` on the owner's machine (not committed); Linux session output 2026-11-01. The GitHub Actions run itself is still pending (billing lock) and is not part of this proof.

### Acceptance 2 — Never overwrites
- Command or steps: `test_3_new_twice_skips_and_keeps_edits`; `test_init_preview_then_apply_then_skip`
- Expected: second run reports SKIP; user edits intact
- Actual: both pass; files are opened with exclusive create (`open(..., "xb")`)
- Result: PASS
- Proof: session output 2026-11-01

### Acceptance 3 — Secrets are never printed
- Command or steps: `test_8_token_like_string_exits_6`
- Expected: exit 6; file and line shown; value never shown
- Actual: passes; the test asserts the token is absent from stdout and stderr
- Result: PASS
- Proof: session output 2026-11-01

## Extra checks
- `mshkh lint` on this repository: `0 blocking, 0 advisory`, exit 0.
- `mshkh lint` on `examples/demo-software`: 1 blocking (`source` path `src/sync/client.ts` does not exist) and 3 advisory (missing plan, evidence, record). Real findings in the examples, outside this card's `may_change`; proposed as a follow-up card.
- New tests in `cli/tests/test_v02_commands.py`: init preview/apply/skip, init → new → lint clean, JSON escaping of titles, data-class floors (Regulated → Critical, Confidential → Standard), undeclared data class rejected with nothing written, agent actor marking, archive references and broken links, human-only event by an agent (exit 5), sensitive patterns and false-positive guards, unknown check name (exit 2).

## Known limitations
- `--changed-only` is accepted but checks everything (reported in the summary).
- Docs Hub profiles are not supported by `new` (exit 2 with a message); native layout only.
- Phone and RFC patterns are heuristics; false positives or misses are possible.
