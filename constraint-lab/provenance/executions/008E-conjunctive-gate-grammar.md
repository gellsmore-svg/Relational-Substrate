# Execution 008E — conjunctive gate grammar

This is the execution record for prompt 008E. It closes that prompt. It does not close prompt 008D.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 008E |
| agent_input_path | `constraint-lab/provenance/prompts/008E-v0.8e-agent-input.md` |
| agent_input_sha256 | `ce1efd0a5463496bd26dd0d171d7111ec1414ccc27a6481bd0ea48ea4194f6a2` |
| agent_input_bytes | 44734 |
| content_status | agent transcription of the session input, not a byte capture |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-13 |
| target | Claude Opus 5.5 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.8d-two-gate-composition` |
| starting_commit | `50e3f4dfeac19d8e075964c51560d4d3f08b85c8` |

The stored file was written out by the implementing agent from the pasted prompt. It was not byte-captured from the session, and one transcription slip in the final question was corrected before storage. Byte identity with the authored prompt is therefore not established. Prompt 008D is not overwritten.

## Result

Branch `research/constraint-lab-v0.8e-conjunctive-gates`.

The inclusive commit range produced by prompt 008E, through the coherence snapshot, is:

```text
70a931cb486a8178cad3e05630b2fbb0f4a5c8aa
fa46cb5a5bd2618076e96d4d7a090287062abb24
```

The parent of the first commit is `50e3f4dfeac19d8e075964c51560d4d3f08b85c8`. The commit that adds this execution file is outside that range.

```text
70a931c provenance: record External Review 008D and Prompt 008D authored metadata
ba50fd4 docs: add the Generation 8D scope erratum and coherence qualification
f9c15c7 docs: define the Generation 8E K3 question
b238bba feat: enumerate K3 conjunction rules and read their local law
e8096db test: add K3 parser, algebra, XOR/XNOR, and coherence tests
5303388 research: freeze the Generation 8E Round E0 analysis plan
b2811bd research: record the Round E0 conjunction question before execution
2daf1ce research: publish the Generation 8E Round E0 conjunction tables
53d3333 research: record the Round E0 result in the journey
11abbd2 docs: publish the Generation 8E conjunctive-gate report
fa46cb5 coherence: publish the through-generation-008e snapshot
```

Experiment id: `generation-008e-conjunctive-gates`.

Reports:

- `constraint-lab/reports/generation-008d-errata.md`
- `constraint-lab/reports/generation-008e-conjunctive-gate-grammar.md`
- `constraint-lab/reports/generation-008e-round-e0-tables.json`
- `constraint-lab/reports/tables/generation-008e-*` (structural orbits, weighted systems, truth tables, interaction, comparison against 8D, basis)

Review: `constraint-lab/provenance/reviews/008D-chatgpt-review-v0.8d.md`. Journey: `constraint-lab/exploration/generation-008e/journey.jsonl`. Charter: `constraint-lab/exploration/generation-008e/charter.md`.

Frozen analysis plan, pushed before Round E0 executed:

- Round E0: `5303388815a3695ac6bf4eb4176c0102b9ca460c`
- plan hash: `ec515306c2d3fa669f15ce31a86cdaac78f5fcab0d01ea7ad82533fde71c9be6`
- plan file: `constraint-lab/exploration/generation-008e/round-e0-plan.json`

The tables commit is `2daf1ce3f54f8bacbc331b6bc575b44ed3f20c27`, which journey step 2 records as `result_commit`. Journey step 1 (`b2811bd`) still has `result_commit` null. The report commit is `11abbd2cb99a641f191f2f43648a5f5b93c0d02e`. The snapshot commit is `fa46cb5a5bd2618076e96d4d7a090287062abb24`.

Round E1 was not opened.

Coherence snapshot:

- path: `constraint-lab/coherence/snapshots/through-generation-008e.md`
- file sha256: `4df5e866fcb494b4ebe94d3a7421a599badd3e3cb4a9f1beb4bee485b7947e63`
- canonical ledger sha256 recorded in that snapshot: `64c0493701fb703e573fcd550a2428bc90aa2034d95754c652ad4157fed06470`

## What ran

Mode B, Round E0 only. This is the exact local reading of every single K=3 rule with a pair action and two distinct triad literals, at N=4, H=0, L=0: 288 labelled rules, 20 S4 orbits and 80 W4 systems, together with seven algebra items. No stochastic trajectories, no stationary census, no parameter fit and no new controls were run. The root is `constraint-lab/generated/generation-008e/round-e0`.

All 27 items ran, none skipped. The longest item wall was 3.44 seconds. `generation008e verify` returned complete with the plan hash above, and assembly validation was ok with no problems. `constraint-lab/generated/` is gitignored. The summary payload sha256 is `231b4a1b6413d4f332272e161802265cbf115f224d11c2da1d3d6838ecb65b46`.

## Divergences from the prompt

- **Pre-freeze values.** Before the freeze, orbit K3-00 was analysed as a smoke test, and the unit tests analysed K3-00 and K3-03 and ran the algebra items. The plan records this in `timing_sample`. Generation 8D's plan recorded a full timing pass in the same way.
- **Prompt storage.** Prompt 008E was stored as an agent transcription, not a byte capture, as described above.
- **Scope of the r-literal law.** The general law was checked on one placement for r = 1 to 4. It is a targeted check of a derivation, not a K=4 or K=5 census.
- **Four-corner example.** The measured four-corner construction uses the four W4 grades. It turned out to be additive (`d = 0`), and the report records this.
- **E1.** E1 was not defined. Seven candidates with attention vectors are recorded in the report and in journey step 2.

## Local checks

Before the snapshot was pushed, the full constraint-lab suite passed 242 tests at `e8096db`, and the 8E and coherence tests passed 26 after the report.

## CI

Actions run `38412283706` is the push of `fa46cb5a5bd2618076e96d4d7a090287062abb24` (https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38412283706). The run's conclusion was success. Jobs `constraint-lab` and `books` both completed, and the constraint-lab job reported 245 passed in 104.45 seconds. This execution file is a later commit, so that run id is not a run of the commit that adds this file.
