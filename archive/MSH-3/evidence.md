# Evidence · MSH-3

| Acceptance | Result | Proof | Environment | Date |
|---|---|---|---|---|
| 1 | PASS | `mshkh lint` in `examples/demo-software` and `examples/demo-finance`: 0 blocking, 0 advisory, exit 0 | Linux, Python 3.11.18 | 2026-11-01 |
| 2 | PASS | `mshkh lint --only sensitive` in both examples: 0 findings; manual read: only synthetic names and amounts | Linux, Python 3.11.18 | 2026-11-01 |
| 3 | PASS | `test_new_preview_counts_files_that_would_be_created`; manual run printed `6 would be created, 0 skipped` | Linux, Python 3.11.18 | 2026-11-01 |

## Details

### Acceptance 1 — Both examples lint clean
- Command or steps: `mshkh lint` in each example folder
- Expected: 0 blocking, 0 advisory, exit 0
- Actual: `lint: 0 blocking, 0 advisory`, exit 0, in both (before: demo-software 1 blocking + 3 advisory; demo-finance 3 advisory)
- Result: PASS

### Acceptance 2 — Examples stay synthetic
- Command or steps: `mshkh lint --only sensitive`; read every added file
- Expected: no findings; no real names, accounts or amounts
- Actual: no findings; amounts are labeled synthetic; no account or contract numbers
- Result: PASS

### Acceptance 3 — Preview reports what would be created
- Command or steps: `mshkh new ABC-1 --title x --level Light` without `--apply`; `pytest`
- Expected: `6 would be created, 0 skipped`; nothing written
- Actual: `new ABC-1 (Light, Internal) preview (use --apply to write): 6 would be created, 0 skipped`; full suite `37 passed, 1 xfailed` (new tests for `new` and `init` previews)
- Result: PASS

## Notes
- The example TypeScript stubs are illustrative and are not built or run (out of scope).
- Windows was not re-run for this card: the CLI change is a summary string, covered by the platform-independent tests.
