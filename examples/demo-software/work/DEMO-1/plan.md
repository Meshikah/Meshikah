# Plan · DEMO-1

## Approach
Wrap the partner-API call in a small retry loop that retries only transient statuses (502, 503, 504) with exponential backoff, up to three attempts. Permanent errors fail on the first attempt so they surface quickly.

## Files to touch
| File | Change |
|---|---|
| src/sync/client.ts | Add `syncRecord` with retry and backoff |
| test/sync/client.test.ts | Tests for acceptance 1 and 2 |

## Files not to touch
- library/ (changes only through Learn)
- The partner API contract

## Acceptance → test map
| Acceptance | Test | Type |
|---|---|---|
| 1 | `transient failure is retried` | Unit |
| 2 | `permanent failure is not retried` | Unit |

## Steps
1. Write both tests first.
2. Implement `syncRecord`.
3. Run the tests and record the output in `evidence.md`.

## Risks and rollback
- Retries multiply load on the partner API during an outage: capped at three attempts with backoff.
- Rollback: revert the change; no data migration.
