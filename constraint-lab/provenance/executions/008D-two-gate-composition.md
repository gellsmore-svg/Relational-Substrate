# Execution 008D — two-gate composition atlas

This is the execution record for prompt 008D. It closes that prompt. It does not close prompt 008C.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 008D |
| agent_input_path | `constraint-lab/provenance/prompts/008D-v0.8d-agent-input.md` |
| agent_input_sha256 | `73a830bab3f5ca7a99f50bc46b90119370f64a4540c6549f9ba537f4c2e73ee1` |
| agent_input_bytes | 35550 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-13 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7, continued by Claude Opus 5.5 from `093e460e9992e3ddc4fd24cdb43d6d5397de4e29` |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.8c-mechanism` |
| starting_commit | `41ec34e72191f93647f28838f16296fa2c2880a3` |

The stored file is the agent input. It includes one leading newline and one trailing newline. It does not contain its own sha256. No separate authored Markdown was byte-compared. Prompt 008C is not overwritten. The authored hash stays null.

The same prompt text was supplied again when the work continued in a second session. That copy was not byte-compared with the stored file, and the stored file was not replaced.

## Result

Branch `research/constraint-lab-v0.8d-two-gate-composition`.

The inclusive commit range produced by prompt 008D, through the coherence snapshot, is:

```text
6a8f35e35d2e95f1ff27592db0f628435166ea16
36cb89cbf1125cd5837afd9f02722671007c6832
```

The parent of the first commit is `41ec34e72191f93647f28838f16296fa2c2880a3`. The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit.

Commits in the range:

```text
6a8f35e provenance: record External Review 008C and Prompt 008D
563305b docs: correct the Generation 8C Jensen-Shannon ratio
f62f1c3 docs: record the Generation 8C coherence corrections
e191203 docs: define the Generation 8D two-gate question
08af50b feat: enumerate two-gate systems and read their local composition
bdbd949 test: check the two-gate algebra and the D0 execution contract
ac037f3 research: freeze the Generation 8D Round D0 analysis plan
d3bf0f7 research: record the Round D0 composition question before execution
cbfdae8 test: keep opposite directions and a same-gate partition
093e460 research: publish the Generation 8D Round D0 composition tables
9cfbde0 research: record the Round D0 result in the journey
7dc3883 docs: publish the Generation 8D two-gate composition atlas
36cb89c coherence: publish the through-generation-008d snapshot
```

Experiment id:

- `generation-008d-two-gate-composition`

Reports:

- `constraint-lab/reports/generation-008c-errata.md`
- `constraint-lab/reports/generation-008d-two-gate-composition-atlas.md`
- `constraint-lab/reports/generation-008d-round-d0-tables.json`
- `constraint-lab/reports/tables/generation-008d-structural-orbits.json`
- `constraint-lab/reports/tables/generation-008d-structural-orbits.csv`
- `constraint-lab/reports/tables/generation-008d-weighted-systems.json`
- `constraint-lab/reports/tables/generation-008d-weighted-systems.csv`
- `constraint-lab/reports/tables/generation-008d-truth-tables.jsonl`
- `constraint-lab/reports/tables/generation-008d-information.json`
- `constraint-lab/reports/tables/generation-008d-ablations.json`
- `constraint-lab/reports/tables/generation-008d-identities.json`

Review:

- `constraint-lab/provenance/reviews/008C-chatgpt-review-v0.8c.md`

Journey:

- `constraint-lab/exploration/generation-008d/journey.jsonl`

Charter:

- `constraint-lab/exploration/generation-008d/charter.md`

Frozen analysis plan, pushed before Round D0 executed:

- Round D0: `ac037f32df81271e04381c79efebf6f5b3d0b607`
- plan hash: `10a3114bcf7a1a914e9eff19e08f77a9fbcf71852bc4a22f14f04d723912ce07`
- plan file: `constraint-lab/exploration/generation-008d/round-d0-plan.json`

The tables commit is `093e460e9992e3ddc4fd24cdb43d6d5397de4e29`. Journey step 2 records that sha as `result_commit`. Journey step 1 still has `result_commit` null. That opening line is unchanged.

The report commit is `7dc388352b30b87ced08abd67cead0dffa37dd82`. The snapshot commit is `36cb89cbf1125cd5837afd9f02722671007c6832`.

Round D1 was not opened.

Coherence snapshot:

- path: `constraint-lab/coherence/snapshots/through-generation-008d.md`
- file sha256: `89aa32b9f96ba311fffd0dd55f3fbe108022eec545eed58e30879a3a0caac895`
- canonical ledger sha256 recorded in that snapshot: `b665dc7f507470bd3af280c104b66c6faff1a78f1f84da7cc8c0a76692ba272b`

The snapshot hashes the findings and relations ledger. It does not hash this execution file.

## What ran

Mode B. Round D0 only. Exact local reading of every two-rule system of one-gate `T->P` rules at N=4, H=0. 96 labelled rules, 4560 unordered pairs, 236 S4 structural orbits, 3584 W4 weighted canonical systems. No new stochastic trajectories. No parameter fit. No new controls. Root `constraint-lab/generated/generation-008d/round-d0`. The supervisor was not used. Each item is an in-process exact computation under a 120-second watchdog.

237 items ran: 236 orbit items and the one-gate surface item. The items were written between 10:19:04 and 10:27:36 local time on 2026-10-13, after the plan freeze at 10:18:20. The longest wall was 5.583469599999717 seconds.

`generation008d verify --frozen-plan-commit ac037f32df81271e04381c79efebf6f5b3d0b607` on that root returned `complete: true`, `missing_count: 0`, and the plan hash above. The published tables record `validation.ok: true` and an empty problem list. Their `frozen_analysis_plan_commit` is `ac037f32df81271e04381c79efebf6f5b3d0b607`.

`constraint-lab/generated/` is gitignored. CI does not recompute the census. The published numerical record is the report and the tables. The summary file is 5,196 bytes, sha256 `dba485576e3ed30d2c7d885490c7f186dcdb6a5d55489e4abf2f0b79d2af5fb2`. Its payload sha256 is `f33ff7eb8549df7679a85c5756f778904b7a8ea5ffeae368e420827bbea9a553`. A test recomputes the payload hash and each column table's canonical hash from the committed files.

## Divergences from the prompt

- Round D1 was not defined. D0 yields a closed local grammar, and its law equivalences are kernel conjugacies that transfer to global dynamics without a further computation. Seven candidate follow-ups with attention vectors are recorded in the report and in journey step 2.
- Commit `cbfdae8a5ffb4118abcacc33a8285894f76435bf` lies between the plan freeze and the tables. It corrected two checks in `validate_orbit_result`: form and dissolve on one slot with one literal are two rules, and two actions on opposite literals of one gate have no realised both-active state. The correction changed the validator, not the estimands, the analysis functions, or any stored item. Every item file predates it. Re-assembly of the stored items with the published code reproduces the summary file byte for byte. ORB-0000, ORB-0028, ORB-0117, ORB-0235, and the surface item were re-executed and reproduce the stored items exactly, wall time excluded.
- Section 37 of the prompt lists six reducibility classes. R0 and R1G are empty. The report explains why.
- Same action, same gate, same literal is not executable: the grammar rejects a repeated structural rule. The kernel product on a forced duplicate is recorded.
- Four readings in the report are taken from the published tables after D0 and are not frozen estimands: the switched versus jointly activated split of dimension two, the invariance groups of balanced information, the chain-rule check, and the grid comparison of I(m) with I(1/m).
- No separate authored Markdown was imported. The authored hash stays null.
- Actions run `38375394924` on `d3bf0f79b65f3d85e9a95e681b875c0f45b3a966` succeeded before the D0 tables were published. That run is the journey-question head. It is not a run of the tables commit or of the report.

## Local checks

Before the snapshot head was pushed, the constraint-lab suite reported 221 passed at `cbfdae8` and the Generation 8D and coherence tests reported 26 passed after the report changes. `generation008d verify` returned complete, with the plan hash above.

## CI

Actions run `38392111816` is the push of `36cb89cbf1125cd5837afd9f02722671007c6832`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38392111816`.

`gh run view 38392111816` reported conclusion success on `36cb89cbf1125cd5837afd9f02722671007c6832`. Jobs `constraint-lab` and `books` both completed. The constraint-lab job reported 227 passed in 131.61 seconds.

This execution file is a later commit. The run id is not a run id for the commit that adds this file.
