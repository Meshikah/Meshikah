# DEMO-1 · Retry failed sync calls

- Level: Standard (proposed; a human confirms it)
- Highest data class: Internal
- Owner: Demo owner
- Area / project / epic: Professional / Demo app / Sync reliability

## Library links
- library/index.md — map of current documents

## Problem
Sync calls to the partner API fail on transient network errors and are never retried, so records go missing.

## In scope
- Retry transient failures (timeouts, HTTP 502/503/504) up to 3 times with backoff.

## Out of scope
- Changing the partner API contract.

## Acceptance
### 1. Transient failure is retried
- GIVEN the partner API returns 503 twice and then 200
- WHEN a sync call runs
- THEN the record syncs and three attempts are logged

### 2. Permanent failure is not retried
- GIVEN the partner API returns 400
- WHEN a sync call runs
- THEN it fails after one attempt with the error surfaced

## Open questions
- Maximum total wait before giving up? — owner: Demo owner
