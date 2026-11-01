# Pack: finance (draft)

Run personal-finance goals as requests and cards: same kernel, same discipline, different domain.

**Status: draft.** Before it goes further, run three real cards by hand in a **private** instance and fold the lessons back here.

## How it maps

| Kernel | In finance |
|---|---|
| Library | Goals, budget rules, account structure (no numbers), past decisions, lessons |
| Work card | One request: "Compare three refinance offers", "Build a 3-month emergency fund" |
| Evidence | Calculations with their sources; statement summaries, never raw statements |
| Release | You move the money or sign. Never the agent. |
| Learn | Rules worth keeping: "Never pay a fee above X% for Y" |

## Hard rules

- Cards are **Confidential** by default; anything touching debt, investments, taxes or identity is **Critical**.
- The `never_store` list in [`pack.yaml`](pack.yaml) is absolute: no full account numbers, credentials or identity document numbers in any file, prompt or log.
- Your instance repository is **private and local-first**. Don't push it to a public remote; don't put it in this product repository.
- Every amount in a plan or evidence must cite where it came from (statement month, offer document), or be marked as an estimate.
- An agent may analyze, compare and draft. It never logs into a bank, executes a transfer, or submits a form.

## Example

See [`examples/demo-finance/`](../../examples/demo-finance/) (synthetic numbers only).
