# Execution 006 — graded interaction and matched lower-order controls

This is the execution record for prompt 006. It is not a review. Review 006 is pending and is not written here.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 006 |
| agent_input_path | `constraint-lab/provenance/prompts/006-v0.6-agent-input.md` |
| agent_input_sha256 | `980d809393477c146fd45b63bf41e7d0af4cb1ef84141d7062d6e82965c487b0` |
| agent_input_bytes | 42694 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-04 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.5` |
| starting_commit | `003a7c64a35ce8e781e7208117e09702ce63a715` |

The stored file is the agent input. It is the `user_query` body, including one leading newline and one trailing newline, excluding the tags. No separate authored Markdown file was byte-compared, so none was imported and none was reconstructed. The prompt file was not edited after it was stored. Its own sha256 is not written inside the file.

Prompt 005's authored metadata was appended in this round from the external verification in the prompt: 39,468 bytes, sha256 `ec8b7df93edc98525aebddb866a845d8a11a57df497dd941797d5be489066e5d`. That file is not in this working environment. The hash is not assigned to `prompts/005-v0.5-agent-input.md`. The relationship stays `unknown`.

Review 005, which this prompt required, is `constraint-lab/provenance/reviews/005-chatgpt-review-v0.5.md`. It is linked to prompt 005 and to execution 005. It records Actions run `37151937623` on `003a7c64a35ce8e781e7208117e09702ce63a715`. It is not a review of the results below.

## Result

Branch `research/constraint-lab-v0.6`.

The inclusive commit range produced by the prompt, through the analysis report, is:

```text
63ccc84aa2b55e1118803d584c073928d23cfecb
ccb8a38f0dc7d6c887f66e43871e50fce060b44a
036bd9a1df151ffb58bff5cb4c6d73826a1b8e99
56fd36882c683bcda6c9e9f11ae80d95d2a3be1a
fc94a168fa1645053ef1a4f8e4a872dadaa57fd8
89ad5dd6253b65dda6b3604e389243806e18f3c8
a7307ed1c846b19df071b7d525d8b530c56e04d1
a359af33e396d7f5325145f2b51ee3262dca7fe6
```

The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit. It is not inside the analysis range above.

Experiment id:

- `generation-006-graded-matched-control-lattice`

There is no secondary experiment id. Recursive Pass 3 did not select one.

Report:

- `constraint-lab/reports/generation-006-graded-matched-control-lattice.md`

Design passes:

- `constraint-lab/docs/generation-006-design-passes.md`

Generations 1, 1b, 2, 3, 3b, 3c, 4, 4a, and 5, their reports, their specifications, and their generated artifacts were not edited.

## What ran

Generation 6. Specification hash `b9b60e103ab5abdb6f4ab5ab5fc5ae4b59dea234244604cd802ba3f2df3865b4`. Catalogue sha256 `60a80a31dacb92798c2e9f1ed1a846666b21f5eb8ffdf8934c6708689f5cfd7f`. Ten shards. Shard items 10. Workers 2. Quarantined 0. Failed 0. One coordinator invocation. Summary field `runtime_seconds` is 96.00385372998426. Shard-work is 95.53377 seconds. Summary sha256 `aee5695d9387396f08c54be10048312153a391e50cee615de96be581210b910b`. Row table sha256 `9f078891f01de14c9c9e2e270ecca3f68f7810af19a811db5172f5b4defd0c33`. Surface sha256 `3b094edc965f78a7fcea76b836e03f94a4ccb0e76b4ce95f174ce6043f12aba0`. 100 canonical targets, from 1,200 labelled targets. 15 canonical condition-erased controls. 100 canonical face controls. The summary `git_commit` is `89ad5dd6253b65dda6b3604e389243806e18f3c8`, the commit loaded at merge. The summary was not re-merged to insert a later commit into that field.

The effect floor stayed `1e-8`. The worst preflight reference gap was `3.397282455352979e-14`. The confirmatory direct-versus-iterative gap on the validation rows was `2.930988785010413e-14`. Neither figure was used to retune the floor.

## Divergences from the prompt

These are recorded here. The prompt was not rewritten to match them.

- The in-process benchmark times two rows, the anchor and the next catalogue row. An earlier note inside the module said three rows. The published plan says two.
- Shard length 10 was kept after that benchmark. Each row was about one second in-process. The completed wall clock was 96.0 seconds with 2 workers. Pass 2's serial estimate of about 102 to 130 seconds was not rewritten after the run.
- `contains_t_action_edge` targets are matched to erasure and one adjacent face. The disjoint gate is a face of the other geometry and is not attached. Control 3 is not added.
- Ten erased canonical ids are shared by swapped unequal weights. The interaction residual is symmetric in the two rules. The row records the weight-assigned role.
- Target `I`, `G`, and `Delta_S` agree across polarity and across the two geometries to about `1e-15`. Control margins do not, because the matched face sets differ.
- State-resolved vectors are stored for the ten validation targets on the primary probe. Other shard rows store the sign summary.
- Alphabet names `W3` and `W16` keep the grade names and change the base. `rho3` does not rename a grade.
- The positive `G_margin` selection kept the earliest target id at the exact maximum. A later row inside the floor was not added.
- No secondary family was run.
- Published summaries store the merge-time `git_commit`. They were not re-merged.
- Review 006 is not written here.
- Float64 solutions are not called exact.

## Local checks

Before the close-out commit, `python -m pytest -q` in `constraint-lab` reported 72 passed in 125.39 seconds. An earlier run of the same suite, before the census, reported 72 passed in 119.85 seconds. These checks do not include the Generation 6 census. CI runs Generation 0 only.

## CI

`gh run view 37192986304` reported conclusion success on `a359af33e396d7f5325145f2b51ee3262dca7fe6`. Jobs `constraint-lab` and `books` both completed. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/37192986304`. This execution file is a later commit. The run id is not a run id for the commit that adds this file. Review 006 remains the place that records the Actions run of the final head.
