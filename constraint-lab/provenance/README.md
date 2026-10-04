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
| 003 | Independent triadic relation and Generation 3 | agent input and the execution-time capture; authored Markdown externally verified and pending import |
| 004 | Memory-clock refinement and N=4 higher-order reconfiguration | `prompts/004-v0.4-n4-higher-order-reconfiguration.md` is the agent input; authored Markdown externally verified and pending import. Execution 004 records the result. Review 004 records the external reading of v0.4 |
| 005 | Provenance completion, controlled reconfiguration, eventual committors, and the targeted two-rule search | `prompts/005-v0.5-agent-input.md` is the agent input. Authored Markdown is externally verified and pending import. Execution 005 records the result. Review 005 records the external reading of v0.5 |
| 006 | Graded interaction, matched lower-order controls, and higher-order specificity | `prompts/006-v0.6-agent-input.md` is the agent input. No separate authored file was byte-compared. Execution 006 is written at close-out. Review 006 is pending |

The verbatim text of 001 and 002 can be inserted later from the ChatGPT conversation, as new prompt files plus a new ledger line. Do not reconstruct them from memory.

Prompt 003 has two stored representations. `prompts/003-v0.3-higher-order-relations.md` is the file captured at execution time (25,995 bytes, sha256 `9ac0de2c5d4cdd33749fec03a232f2d35fe5f6dbead9b0f572cafce4e23cbccb`). `prompts/003-v0.3-agent-input.md` is the `user_query` body from the implementing session (25,996 bytes). The captured file is that body with the leading newline removed. Neither file is the ChatGPT-authored Markdown. `content_status: verbatim` on the original ledger line means verbatim relative to the execution-time capture. It does not mean byte identity with the authored file. A later ledger line records that qualification. Do not overwrite either file.

Review 004 records an external verification of the Prompt 003 and Prompt 004 authored Markdown files. Those files are not in this working environment. Their externally verified metadata is stored separately from the local artifacts, with `authored_prompt_status: externally_verified_pending_import`:

| Prompt | Externally verified bytes | Externally verified sha256 | Local agent-input bytes | Local agent-input sha256 |
| --- | --- | --- | --- | --- |
| 003 | 27,580 | `5acdf96aa311273fa02207e64c08b5509d144cc4f1921c9f101cd02570f77ede` | 25,996 | `451f462d1d6675023d836939b9647422cfb098926bc62bec15da371edc33e92e` |
| 004 | 32,018 | `ae1979b484da8d30614776445e46f8b674e0d1a991688884685ba327296f398a` | 32,011 | `f261527e522cc780f0937097b7de7706f7953f8bf69c59837442bbb7e1cf76ef` |
| 005 | 39,468 | `ec8b7df93edc98525aebddb866a845d8a11a57df497dd941797d5be489066e5d` | 39,466 | `e420caddf967d954c0b8b37aaa115b38c09341123a4047835e22e03ba64557c4` |

Do not assign those authored hashes to the stored files. Do not manufacture a file from an agent-input representation in order to match them.

Prompt 005 is stored at `prompts/005-v0.5-agent-input.md`. That file is the `user_query` body from the implementing session, including its leading newline and excluding the tags. Review 005 externally verified a separate authored Markdown file of 39,468 bytes, sha256 `ec8b7df93edc98525aebddb866a845d8a11a57df497dd941797d5be489066e5d`. That file is not in this working environment. Its hash is not assigned to the stored agent-input file. `authored_prompt_status` is `externally_verified_pending_import`. The relationship of that authored file to the agent input stays `unknown`, because no byte comparison was possible. The earlier comparison of the agent input with the harness prompt history remains `normalised`. That harness history is not an authored artifact.

Prompt 006 is stored at `prompts/006-v0.6-agent-input.md`. That file is the `user_query` body from the implementing session, including its leading newline and one trailing newline, excluding the tags: 42,694 bytes, sha256 `980d809393477c146fd45b63bf41e7d0af4cb1ef84141d7062d6e82965c487b0`. No separate authored Markdown file was found, so none was imported and none was reconstructed. The relationship of an authored file to this agent input is `unknown`.

Reviews live in `reviews/`. Review 002 records an external ChatGPT reading of v0.2. Review 003 records an external ChatGPT reading of v0.3 at `e04e0d4dcf979197b62d8d73fd747a0a2084c2b6`. Review 004 records an external ChatGPT reading of v0.4 at `777ef71d123e8f85e6d1372225b5028744fc5ffe` and is linked to prompt 004 and execution 004. Review 005 records an external ChatGPT reading of v0.5 at `003a7c64a35ce8e781e7208117e09702ce63a715` and is linked to prompt 005 and execution 005. Each says what was inspected and what was concluded. None is a line-by-line audit of generated artifacts. Review 006 is not in this repository.

The permanent CI convention is that a ledger line may record a run on a parent commit and must say that it is not a run id for the commit that adds it. The external review of a completed branch is the place that records the Actions run of that branch's final head. Do not add commits whose only purpose is to record the run of the commit that records the previous run.

Executions live in `executions/`. An execution record names the branch, the commit range, and the experiment ids a prompt produced. It may record divergences. It is not a review, and it does not rewrite the prompt. Execution 003 closes prompt 003. Execution 004 closes prompt 004. Execution 005 closes prompt 005. The close-out commit that adds an execution record is not inside the commit range that record lists. Review 006 is not in this repository.
