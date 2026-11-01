# Plan · FIN-1

## Approach
Compare the current loan with the three offers on total remaining cost (interest plus every fee), using only numbers taken from each offer's document. Filter out any option whose monthly payment is above the current payment. The agent prepares the comparison; the person decides and, if refinancing, signs.

## Options compared
| Option | Source document | Monthly payment | Total remaining cost |
|---|---|---|---|
| Stay with the current loan | Current statement (synthetic) | | |
| Offer A | Offer letter A (synthetic) | | |
| Offer B | Offer letter B (synthetic) | | |
| Offer C | Offer letter C (synthetic) | | |

## What I will not do
- Extend the term beyond the current end date.
- Store account numbers, contract numbers or identity documents in this card.
- Let the agent contact a lender or sign anything.

## Acceptance → check map
| Acceptance | Check | Type |
|---|---|---|
| 1 | Every number in the table cites its source document | Manual review |
| 2 | Recommended option's monthly payment ≤ current payment | Manual review |

## Steps
1. Collect the four source documents (outside this repository).
2. Fill the table with numbers copied from the documents, citing each one.
3. Compute total remaining cost; mark the cheapest option that passes the payment cap.

## Risks and rollback
- Hidden fees: read each offer's fee section before computing totals.
- Nothing to roll back until a contract is signed (Release, by the person only).
