# Plan · MSH-3

## Approach
Give DEMO-1 the source and test files its `context.json` already points to, as short synthetic stubs, rather than removing the pointers: the example should show real pointers. Complete both example cards with plan, evidence and an opening record line so they model a full card.

## Files to touch
| File | Change |
|---|---|
| examples/demo-software/src/sync/client.ts | New: synthetic stub (retry wrapper outline) |
| examples/demo-software/test/sync/client.test.ts | New: synthetic test outline |
| examples/demo-software/work/DEMO-1/{plan.md, evidence.md, record.jsonl} | New |
| examples/demo-finance/work/FIN-1/{plan.md, evidence.md, record.jsonl} | New |
| cli/src/mshkh/cli.py | Preview summary counts files that would be created |
| cli/tests/test_v02_commands.py | Test for the preview summary |

## Files not to touch
- library/ (changes only through Learn)
- docs/, kernel/, and every other file in cli/

## Acceptance → test map
| Acceptance | Test | Type |
|---|---|---|
| 1 | `mshkh lint` in each example | Automated |
| 2 | `mshkh lint --only sensitive` in each example; manual read | Automated + manual |
| 3 | `test_new_preview_counts_files_that_would_be_created` | Automated |

## Steps
1. Add the two stub files.
2. Add plan, evidence and record to DEMO-1 and FIN-1.
3. Run `mshkh lint` in both examples; record the output in `evidence.md`.

## Risks and rollback
- None beyond example content; revert the commit.
