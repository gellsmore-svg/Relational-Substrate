# Research provenance

The laboratory keeps five different records. They are not interchangeable.

| Record | What it is |
| --- | --- |
| AUTHORED_PROMPT | The Markdown file as authored, before any harness or capture step |
| AGENT_INPUT_PROMPT | The bytes the implementing agent actually received |
| EXECUTION | The branch, commits, and experiment ids that instruction produced |
| REVIEW | An assessment of those results, written after the execution |
| NEXT_PROMPT | A new instruction. It does not rewrite the previous prompt |

Semantic equivalence is not byte identity. A ledger entry records both representations when both are known.

| Field | Meaning |
| --- | --- |
| `authored_prompt_path`, `authored_prompt_sha256`, `authored_prompt_bytes` | The authored artifact |
| `agent_input_prompt_path`, `agent_input_prompt_sha256`, `agent_input_prompt_bytes` | The agent-input artifact |
| `relationship` | `exact`, `normalised`, `transformed`, or `unknown` |

`exact` means the two byte strings were compared and are identical. `normalised` means a formatting or capture difference is known, whether or not every byte of the mechanism has been reconstructed. `transformed` means the wording itself differs. `unknown` means the two artifacts have not been compared. Do not write `exact` because the prose looks similar.

Unknown hashes and paths stay `null`. Do not reconstruct a missing file and label the reconstruction exact.

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
| 003 | Independent triadic relation and Generation 3 | agent input and the execution-time capture; authored Markdown pending |
| 004 | Memory-clock refinement and N=4 higher-order reconfiguration | `prompts/004-v0.4-n4-higher-order-reconfiguration.md` is the agent input; authored Markdown pending |

The verbatim text of 001 and 002 can be inserted later from the ChatGPT conversation, as new prompt files plus a new ledger line. Do not reconstruct them from memory.

Prompt 003 has two stored representations. `prompts/003-v0.3-higher-order-relations.md` is the file captured at execution time (25,995 bytes, sha256 `9ac0de2c5d4cdd33749fec03a232f2d35fe5f6dbead9b0f572cafce4e23cbccb`). `prompts/003-v0.3-agent-input.md` is the `user_query` body from the implementing session (25,996 bytes). The captured file is that body with the leading newline removed. Neither file is the ChatGPT-authored Markdown, which the external review reported at 27,580 bytes and which is not in this working environment. `content_status: verbatim` on the original ledger line means verbatim relative to the execution-time capture. It does not mean byte identity with the authored file. A later ledger line records that qualification. Do not overwrite either file.

Reviews live in `reviews/`. Review 002 records an external ChatGPT reading of v0.2. It says what was inspected and what was concluded. It is not a line-by-line audit of generated artifacts.

Executions live in `executions/`. An execution record names the branch, the commit range, and the experiment ids a prompt produced. It may record divergences. It is not a review, and it does not rewrite the prompt.
