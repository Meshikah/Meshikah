# MSH-2 · Implement `mshkh` 0.2: `init`, `new`, `lint`

- Level: Standard (confirmed by human:armando, 2026-11-01)
- Highest data class: Internal
- Owner: Armando
- Type: story
- Area / project / epic: Professional / MeshikahAI / CLI MVP

## Library links
- docs/04-cli-mvp.md — the command contract and MVP tests
- docs/03-runtime.md — layout, `context.json`, record format
- kernel/README.md — schemas the commands validate against

## Problem
The method can only be run by hand. Roadmap 0.2 needs the three commands that create and check cards, so the first real cards can be opened and linted without copying templates manually.

## In scope
- `mshkh init`: create missing `library/index.md`, `work/`, `archive/`, `MESHIKAH.md`; preview unless `--apply`.
- `mshkh new`: create a card from the kernel or the configured pack's templates; data-class floor; never overwrite.
- `mshkh lint`: checks `card-files`, `acceptance`, `context`, `archive-refs`, `links`, `record`, `sensitive`, `budget`.

## Out of scope
- `request`, `decide`, `status` logic (roadmap 0.3); Docs Hub profiles; policy hooks.

## Acceptance
### 1. MVP tests 1–4 and 7–9 pass
- GIVEN the contract tests in `cli/tests/test_mvp_contract.py`
- WHEN the suite runs on Windows and Linux
- THEN tests 1, 2, 3, 4, 7 and 8 pass and are no longer marked xfail

### 2. Never overwrites
- GIVEN an existing card with a user edit
- WHEN `mshkh new` runs again with `--apply`
- THEN every file is reported as SKIP and the edit is intact

### 3. Secrets are never printed
- GIVEN a card containing a token-like string
- WHEN `mshkh lint` runs
- THEN it exits 6 and prints the file and line, never the value

## Open questions
- Should `new` read the pack's templates from `packs/<name>/` in the product repo, or from an installed copy? — owner: Armando
