# Execution 005 — controlled reconfiguration and targeted pair interaction

This is the execution record for prompt 005. It is not a review. Review 005 is pending and is not written here.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 005 |
| agent_input_path | `constraint-lab/provenance/prompts/005-v0.5-agent-input.md` |
| agent_input_sha256 | `e420caddf967d954c0b8b37aaa115b38c09341123a4047835e22e03ba64557c4` |
| agent_input_bytes | 39466 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| relationship of agent input to harness prompt history | `normalised` |
| harness prompt history sha256 | `dffc33fd4ea26411f1e05092e25046279e72c5a37d298c1bf90b88395071b8ae` |
| harness prompt history bytes | 39464 |
| date | 2026-10-03 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting branch | `research/constraint-lab-v0.4` |
| starting commit | `777ef71d123e8f85e6d1372225b5028744fc5ffe` |

The stored file is the agent input. It is the `user_query` body, including its leading newline and excluding the tags. No separate authored Markdown file was byte-compared, so none was imported and none was reconstructed. The comparison with the harness prompt history was performed: that history is the same text with the surrounding U+000A characters removed. The prompt file was not edited after it was stored.

Review 004, which this prompt required, is `constraint-lab/provenance/reviews/004-chatgpt-review-v0.4.md`. It is linked to prompt 004 and to execution 004. It is not a review of the results below.

Prompt 003 authored Markdown remains externally verified and not imported: 27,580 bytes, sha256 `5acdf96aa311273fa02207e64c08b5509d144cc4f1921c9f101cd02570f77ede`. Prompt 004 authored Markdown remains externally verified and not imported: 32,018 bytes, sha256 `ae1979b484da8d30614776445e46f8b674e0d1a991688884685ba327296f398a`. Those hashes are not assigned to the stored agent-input files.

## Result

Branch `research/constraint-lab-v0.5`.

The inclusive commit range produced by the prompt, through the analysis report, is:

```text
c1d1a1d71207b499eca018c6b19bb1a1677d17e3
a6236dcd480a980491478a82941429493d8821fb
1ddfc289e19668fae5238beb11ffff58a4cb4e29
6506f4cabf2976511778a95dfc6c86ac1429d165
0f6903b9f9916cd659e64118d2047e834afede6e
1c7726f8d431ea54baeb478bf2171d0703046ea2
0c9bf3a3f673b5f191e47ef46c6ac3ca10c0e414
335c876b0ef80cbff2b1a1985a006b07f0992bdc
d8c97964850194577ecf084a0fb00c209378957c
```

The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit, or the commit that follows it if the line is split off. Neither is inside the analysis range above.

Experiment ids:

- `generation-004a-reconfiguration-sensitivity`
- `generation-005-targeted-tp-pp-pairs`

Reports:

- `constraint-lab/reports/generation-004a-reconfiguration-sensitivity.md`
- `constraint-lab/reports/generation-005-targeted-tp-pp-pairs.md`

Generations 1, 1b, 2, 3, 3b, 3c, and 4, their reports, their specifications, and their generated artifacts were not edited.

## What ran

Generation 4a. Specification hash `9ec57d9ffa21c83a824650b4397f541daee40aed3eb327b4c304571ff4075fec`. Ten shards. Shard items 200. Workers 2. Quarantined 0. Failed 0. Summary field `runtime_seconds` is 132.8163948400179. Shard-work is 236.631408 seconds. Summary SHA-256 `2fb9601c2968c54781384f98ae34e3e549c397c9d4af4ad5bfc526244bd1561c`. Row table SHA-256 `c201f540597fbd4e7063e6be437abf0804c510cfa98407701bbfe8934ee50c9f`. 160 canonical weighted singletons. The summary `git_commit` is `1c7726f8d431ea54baeb478bf2171d0703046ea2`, the plan-time commit.

Generation 5. Specification hash `c0372859f77626cec7af10c22cd35d0518ff3772ad907f7d6b08350fa17708af`. Catalogue SHA-256 `d2994cead5190422a27ac1a135494fc6a2dd469dc914cb88ee0fed8192e10c57`. Six shards. Shard items 384. Workers 2. Quarantined 0. Failed 0. One coordinator invocation. Summary field `runtime_seconds` is 305.6155730149767. Shard-work is 554.452213 seconds. Summary SHA-256 `5651a656c3404d833c296322216255b8de71ef56a3f046f2f1dfbf8a4220f154`. Row table SHA-256 `d479775aafacb9bb6b6c5aea7522443f05ab4d581b92864a4cc1a7ff70e12c0e`. 2,304 canonical weighted pairs, from 50,688 weighted labelled pairs. The summary `git_commit` is `1c7726f8d431ea54baeb478bf2171d0703046ea2`, the plan-time commit. The plan header was not rewritten after the analysis commits.

The label grid `8 × 10 × 2 × 2 = 320` was not used as the canonical count. The full cardinality-2 grammar of 85,175 canonical structurally-simple pairs was not executed.

## Divergences from the prompt

These are recorded here. The prompt was not rewritten to match them.

- Cross-order labels are stored as ASCII `P->P`, `P->T`, `T->P`, and `T->T`.
- At `N = 4` the stationary solve, the epoch kernel, and the committor are float64. Residuals are stored. The numbers are not called exact.
- The effect floor is `1e-8`. It was written into both specifications before either census, from the reference-kernel residuals. It was not retuned after the extrema were seen.
- The one-step same-edge-count flux remains a named invariant. It is not a success criterion of Generation 4a or Generation 5.
- Generation 4a recomputes the horizon-16 passage on every sensitivity probe. It does not recompute the eventual committor on those probes. Whole-census robustness is not claimed for the eventual committor.
- Generation 4a shard rows store the state-resolved summary: weighted mean, both extrema, and the attaining states and triads. They do not store the full committor array. Generation 5 stores the full state-resolved interaction vector in the gitignored shard result and drops it from the published summary. The validation block keeps the extrema of the predeclared rows.
- The plan's solver-memory figure multiplies the landing size by the shard length. Workers release each pair landing after the row is stored, so that figure overstates retained memory.
- Shard length 384 was chosen from the measured eight-pair sample on this machine. Workers stayed at 2.
- Several canonical pairs share an interaction residual to within the effect floor. The discovery ranking keeps one pair id per predeclared quantity and does not collapse the tie. `ranking_changed` is false. The recomputed gaps on the selected ids are 0.
- `G` was not recomputed at the alternate `rho3` values. The recorded robustness quantities on the extrema are the interaction residual, the pair delta, and `Delta_S`.
- Alphabet probes on an extremum were skipped when both weights were prohibit. Prohibit is zero in `W3`, `W4`, and `W16`.
- Published summaries store the plan-time `git_commit`. They were not re-merged to insert a later commit into that field.
- Review 005 is not written here.

## Local checks

Before this close-out commit, `python -m pytest -q` in `constraint-lab` reported 60 passed in 55.84 seconds. These checks do not include the Generation 4a or Generation 5 censuses. CI runs Generation 0 only. The final-head Actions run id is not yet known and is not invented here.
