# Kernel

The domain-agnostic core of MeshikahAI: data contracts that every pack and every tool binding share.

| Schema | Validates | Spec |
|---|---|---|
| [`schemas/context.schema.json`](schemas/context.schema.json) | `work/<KEY>/context.json` | `docs/03-runtime.md`, reference OS §4.1 |
| [`schemas/record-event.schema.json`](schemas/record-event.schema.json) | One line of `work/<KEY>/record.jsonl` | `docs/03-runtime.md`, reference OS §4.3 |
| [`schemas/meshikah.schema.json`](schemas/meshikah.schema.json) | `meshikah.yaml` (after YAML parsing) | Reference OS §3.2 |
| [`schemas/pack.schema.json`](schemas/pack.schema.json) | `packs/<name>/pack.yaml` | `docs/06-packs.md` |

Schemas check structure. Rules that span files (the hash chain, checkpoint order, human-only events, paths that must exist) are checked by `mshkh lint`.
