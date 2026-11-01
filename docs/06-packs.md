# 06 · Packs

**Status: draft proposal.**

A pack adapts the kernel to one domain without changing it. It may **narrow** kernel rules (stricter defaults, extra checks), never loosen them.

## What a pack contains

```text
packs/<name>/
├── pack.yaml          # Metadata, defaults, risk signals, checkpoint meanings, checks
├── README.md          # What the pack is for, how to use it
└── templates/         # Optional overrides of kernel templates (card.md, plan.md, evidence.md, context.json)
```

A pack that doesn't override a template uses the kernel's (`templates/work-card/`). One copy of durable truth applies to templates too.

## `pack.yaml` fields

| Field | Meaning |
|---|---|
| `name`, `version`, `status` | Identity and maturity |
| `key_prefix` | Suggested card key prefix (e.g. `FIN`) |
| `default_data_class` | Starting data class for new cards; can only be raised |
| `allowed_data_classes` | Classes the pack is designed for |
| `level_signals` | Signals per level (Light, Standard, Heavy, Critical), in the domain's language |
| `checkpoints` | What each checkpoint means in this domain |
| `checks` | Extra checks the pack adds to `mshkh lint` |
| `never_store` | Data that must never appear in any artifact for this domain |

## Available packs

| Pack | Status | Domain |
|---|---|---|
| [`software`](../packs/software/) | 0.1, default | Building software with AI coding agents |
| [`finance`](../packs/finance/) | 0.1, draft | Personal finance projects |

## Rules for new packs

1. A new pack starts as a draft and is tested by hand on at least three real cards in a private instance.
2. It declares its `never_store` list before its first card.
3. It reuses kernel templates unless the domain genuinely needs different sections.
4. Its checkpoint meanings must keep the kernel rule: humans decide, agents prepare.
