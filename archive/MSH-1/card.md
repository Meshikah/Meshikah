# MSH-1 · Scaffold the meshikah repository

- Level: Light (confirmed by human:armando, 2026-11-01)
- Highest data class: Internal
- Owner: Armando
- Type: task
- Area / project / epic: Professional / MeshikahAI / Repository

## Library links
- library/index.md — map of the repository
- docs/03-runtime.md — native layout this scaffold follows

## Problem
MeshikahAI existed as loose documents. It needs a product repository that follows its own method: library, work cards, record, kernel, packs and a CLI skeleton.

## In scope
- Method docs 01–06, framework 2.0 reference, kernel schemas, software and finance packs, `mshkh` skeleton, examples, CI.
- The repository's own library (decisions, questions, lessons) and its first cards.

## Out of scope
- Implementing any `mshkh` command (moved to MSH-2, roadmap 0.2).

## Acceptance
### 1. Repository exists and is clean
- GIVEN the scaffold in `C:\dev\MeshikahOS`
- WHEN the first commit is made
- THEN the tree matches the agreed structure and no client names or personal data appear

### 2. Skeleton runs
- GIVEN the CLI skeleton
- WHEN `pytest` runs in `cli/`
- THEN all non-pending tests pass and pending ones are marked xfail

## Open questions
- None
