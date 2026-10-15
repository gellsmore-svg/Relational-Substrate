# Execution record: GT-P011 (durable relational reconstruction; shared synthesis milestone)

- **Prompt.** `provenance/prompts/GT-P011-agent-input.md`: the author's file, copied byte for byte (48,435 bytes, sha256 `a4768999…f404`).
- **Agent.** Claude Opus 5.5, assisting one human researcher.
- **Branch.** `research/gravity-time-admissibility`; draft PR #6, not merged.
- **Mandate.** One frozen E5C round, then a separate hub milestone for GT-P010 and GT-P011, without faking the named-human pin gate.

## Starting state (verified)

- GT `4aaf04c` (= GT-P010 close), clean worktree, CI green.
- Hub `main` `38c2501`.
- No E5C artefacts and no concurrent E5C or hub branch.
- CL 8O closed at `99565d1` (context only).
- Baseline suite: 865 tests (GT-P010 close).

## Chronology

| Commit | Content |
| --- | --- |
| `105b1e8` | Prompt (verbatim) and `docs/gt-p011-starting-audit.md`. **Before any E5C computation** |
| `9508f00` | `docs/e5c-durable-renewal-definitions.md` (T12–T15); `gtdurable.py`, `gte5c.py`; tests `test_gtdurable.py` (12) and `test_gte5c.py` (6). Full suite 883 passed; CI success, run 38799699230 |
| `469ee28` | **Freeze:** `plans/round-e5c-plan.json`, plan_hash `bab7a59d…6e47`, source `9508f00`, hub `38c2501` |
| `fa5f3b3` | Journey step 28, pushed before execution |
| (run) | 2026-10-15 20:15:19Z to 20:20:27Z; 12/12 complete |
| `5080199` | **Results:** `round-e5c-tables.json` (payload `582e845ba338…e5f1`) and `gt-e5c-atlas.md` |
| this commit | Report, reflection, ledger GT-F91–F97, GT-Q25, GT-R156–R166; map; snapshot `through-gt-e5c.md`; hypotheses (E5C columns); bridge-map section 13; ontology note; transfer T-21–T-24; GT-side handoff; README; roadmap; journey step 29; this record |
| close | Provenance ledger row with the CI result of the synthesis commit |

## Pre-freeze computations (no E5C quantity of an N=5 or N=6 scientific cell)

| Fixture | Purpose |
| --- | --- |
| N = 4 NULL, PCOMP, CLOSEW (F_TRI) | Independent propagation route, R0 replication |
| Synthetic neighbourhood rules at N = 5, 6 (not GT families) | Independent route at N = 5; identities; first-hit versus stationary; remote-rate effect; relabelling; T14 labels; timing (about 21 s per law, 346 MB) |
| Monte Carlo trajectories, N = 4 NULL, 60,000 episodes | U_0 to U_2 |

**Pre-freeze discovery (structural, law-independent).** On the synthetic N = 5 rule, F_2PATH could not survive any local event after renewal. This became theorem T14 and the status `STRUCTURALLY_ZERO_FOR_H_GE_1`, frozen before execution.

**A pre-freeze test correction.** The T14 test at N = 6 first used NULL N = 6 (a science cell; only a structural label was asserted and no value printed). It was switched to the synthetic N = 6 rule before freezing.

## Execution and checks

- 12/12 items complete; 24/24 predicate analyses (F_2PATH STRUCTURALLY_ZERO_FOR_H_GE_1 at N = 5; F_TRI size N−2 classes STRUCTURALLY_IMPOSSIBLE).
- Every frozen check passes:
  - R0 replicates E5B renewal for the target, ND and NK;
  - T13 has zero violations;
  - return + exit = 1;
  - monotonicity and U = R0·C hold;
  - relabelled anchors agree;
  - the NULL fixed point holds at both sizes;
  - PCOMP's law is uniform.
- No unresolved solve.

## Deviations

None from the frozen plan. The optional continuous-time channel and F_STAR partial-renewal durability were excluded before freezing.

## Hub boundary and next step

No `research-synthesis/` file exists on the GT branch. The hub milestone (a separate worktree and branch from `main`) follows this close. Its branch, pin proposal, staged report and PR are recorded in the PR #6 description. Pin adoption requires a named human reviewer.
