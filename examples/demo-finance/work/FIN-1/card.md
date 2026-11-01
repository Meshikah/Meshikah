# FIN-1 · Compare three refinance offers for the car loan

- Level: Heavy (proposed; you confirm it). Becomes Critical if you decide to sign.
- Highest data class: Confidential
- Owner: Demo person
- Area / project / epic: Finance / Debt-free 2027 / Refinance the car loan

## Library links
- library/index.md — goals and budget rules

## Need
The current car loan costs too much interest. Find out whether refinancing saves money after all fees. **All numbers below are synthetic.**

## Constraints
- Amount or range: remaining balance 120,000 MXN (synthetic)
- Deadline: decide by the end of next month
- Risk tolerance: fixed rate only
- Things I won't do: extend the term beyond the current end date

## Acceptance
### 1. Total cost compared
- GIVEN the current loan and three offers, each with its source document
- WHEN total remaining cost (interest + fees) is calculated for each
- THEN the cheapest option and the saving versus staying are shown, with every number traced to its source

### 2. Guardrail: payment cap
- GIVEN the monthly budget rule
- WHEN an option is recommended
- THEN its monthly payment does not exceed the current payment

## Open questions
- Does the current loan charge an early-payoff penalty? — owner: Demo person
