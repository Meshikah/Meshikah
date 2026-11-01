# MSH-3 · Make the examples lint-clean

- Level: Light (confirmed by human:armando, 2026-11-01)
- Highest data class: Internal
- Owner: Armando
- Type: task
- Area / project / epic: Professional / MeshikahAI / Examples

## Library links
- docs/03-runtime.md — what a complete card contains
- examples/README.md — purpose of the examples

## Problem
`mshkh lint` (MSH-2) finds real problems in the examples. In `examples/demo-software`, DEMO-1's `context.json` points to `src/sync/client.ts`, which doesn't exist (blocking). Both DEMO-1 and FIN-1 are missing `plan.md`, `evidence.md` and `record.jsonl` (advisory). Examples that fail our own checks teach the wrong thing.

## In scope
- Add a small synthetic `src/sync/client.ts` and `test/sync/client.test.ts` to `examples/demo-software` so DEMO-1's pointers are real.
- Add `plan.md`, `evidence.md` and a valid `record.jsonl` (one `opened` event) to DEMO-1 and FIN-1.
- Fix the preview summary of `mshkh init` and `mshkh new`: it reports `0 created` instead of how many files would be created (added at the owner's request).

## Out of scope
- Making the example code runnable or tested; it is illustrative only.
- Any other change to the CLI, and any change to docs or schemas.

## Acceptance
### 1. Both examples lint clean
- GIVEN `examples/demo-software` and `examples/demo-finance`
- WHEN `mshkh lint` runs in each
- THEN it reports 0 blocking and 0 advisory findings and exits 0

### 2. Examples stay synthetic
- GIVEN the files added by this card
- WHEN the sensitive-data check runs
- THEN it finds nothing, and no real names, accounts or amounts appear

### 3. Preview reports what would be created
- GIVEN a repository without card ABC-1
- WHEN `mshkh new ABC-1 ...` runs without `--apply`
- THEN the summary says `6 would be created, 0 skipped` and nothing is written

## Open questions
- None
