# Research provenance

The laboratory keeps four different records. They are not interchangeable.

| Record | What it is |
| --- | --- |
| PROMPT | The instruction that was given, stored verbatim |
| EXECUTION | The branch, commits, and experiment ids that instruction produced |
| REVIEW | An assessment of those results, written after the execution |
| NEXT PROMPT | A new instruction. It does not rewrite the previous prompt |

## Rules

Every externally executed substantive research prompt must be preserved verbatim and linked to the branch, commits, and results it caused, and to the subsequent review that assessed those results.

Prompts are immutable historical evidence. Amendments create new prompts; they do not rewrite old ones.

If an implementation differs from its prompt, record the divergence in the ledger or in the execution record. Do not edit the prompt so that it matches the code.

## Ledger

`ledger.jsonl` is append-only. One JSON object per line. A later line may add an execution link for an earlier prompt. Do not edit an earlier line.

Unknown fields stay `null`. Do not invent a date, a model name, a commit, or prompt wording.

Prompt identifiers:

| Id | Role | Text |
| --- | --- | --- |
| 001 | Constraint Laboratory bootstrap / repository reorganisation / Generation 1 | `content_status: pending_verbatim_import` |
| 002 | v0.2 robustness, structural normalisation, and Generation 2 | `content_status: pending_verbatim_import` |
| 003 | Independent triadic relation and Generation 3 | `prompts/003-v0.3-higher-order-relations.md` |

The verbatim text of 001 and 002 can be inserted later from the ChatGPT conversation, as new prompt files plus a new ledger line. Do not reconstruct them from memory.

Reviews live in `reviews/`. Review 002 records an external ChatGPT reading of v0.2. It says what was inspected and what was concluded. It is not a line-by-line audit of generated artifacts.
