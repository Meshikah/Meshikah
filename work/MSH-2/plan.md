# Plan · MSH-2

## Approach
Implement the three commands as small modules behind the existing argument parser, reusing `repo.py` for discovery. Templates are read from the repository (kernel `templates/` or the pack's `templates`), filled with simple token replacement, JSON-escaped for `.json` files.

## Files to touch
| File | Change |
|---|---|
| cli/src/mshkh/cli.py | Wire `init`, `new`, `lint` to their modules |
| cli/src/mshkh/init.py | New: `init` |
| cli/src/mshkh/new.py | New: `new` |
| cli/src/mshkh/lint.py | New: checks |
| cli/src/mshkh/record.py | New: hash-chain helpers |
| cli/tests/*.py | Remove xfail on tests 2, 3, 7, 8; add tests |

## Files not to touch
- library/ (changes only through Learn)
- docs/ and docs/reference/ (contract changes need their own card)
- kernel/schemas/ (contract changes need their own card)

## Acceptance → test map
| Acceptance | Test | Type |
|---|---|---|
| 1 | cli/tests/test_mvp_contract.py tests 1–4, 7–8 + CI matrix (test 9) | Automated |
| 2 | test_3_new_twice_skips_and_keeps_edits | Automated |
| 3 | test_8_token_like_string_exits_6, asserting the value is absent from output | Automated |

## Steps
1. `record.py` hash helpers and their tests.
2. `lint` checks, one function per check.
3. `new`, then `init`.
4. Remove xfail markers as tests pass.

## Risks and rollback
- Token replacement breaking JSON: escape values; validate the generated `context.json` against the schema in the test.
- Rollback: revert the branch; no repository data is migrated.
