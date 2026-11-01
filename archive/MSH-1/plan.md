# Plan · MSH-1

## Approach
Copy the scaffold prepared in the OneDrive folder to `C:\dev\MeshikahOS` (outside OneDrive), drop leftovers from an older 2025 init script, add CI, then initialize Git with human checkpoints before staging and before the first commit.

## Files to touch
| File | Change |
|---|---|
| Whole repository | Initial scaffold (76 files) |
| .github/workflows/ci.yml | New: pytest on Python 3.11, Ubuntu and Windows |

## Files not to touch
- The OneDrive copy (left as it was)

## Acceptance → test map
| Acceptance | Test | Type |
|---|---|---|
| 1 | File list review; sanitization search | Manual |
| 2 | `cd cli && pytest` | Automated |

## Steps
1. Copy, excluding `initialize_meshikah_structure.ps1` and empty `config/`, `scripts/`, `src/`, `tests/`.
2. Add CI. Run tests and the sanitization search.
3. `git init -b main`, stage, first commit after approval.

## Risks and rollback
- Git inside OneDrive conflicts with sync: avoided by working in `C:\dev`.
