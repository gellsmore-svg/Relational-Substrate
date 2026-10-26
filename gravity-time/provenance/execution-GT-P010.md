# Execution record: GT-P010 (FREE persistence, genuine replacement, kinetic controls, federated synthesis)

- **Prompt.** `provenance/prompts/GT-P010-agent-input.md`. It is the author's file `GT-P010-FREE-Persistence-Replacement-and-Federated-Synthesis.md`, copied byte for byte: 39,584 bytes, sha256 `32895bb95e27fd88…`, compared with the original.
- **Agent.** Claude Opus 5.5, assisting one human researcher.
- **Branch.** `research/gravity-time-admissibility`; draft PR #6, not merged.
- **Mandate.**
  - Authorised: audit, definitions and engineering, **one** frozen-and-pushed E5B round, synthesis, and a hub handoff.
  - Not authorised: E5C, N=7, strength sweeps, CL runs, and any write to `main`, the hub, CL, SC, books or ontology.

## Starting state (verified)

- **Heads.** GT remote head `79fa6b0119449bd56359acf4436015df27855f43`, equal to the local head and to the prompt baseline; worktree clean.
- **PR #6.** Open, draft; CI on `79fa6b0` success.
- **Hub.** `main` at `38c2501bbab22ca1eb2288ea76a962ac0170d5e6`, equal to the prompt baseline. It was read with `git show` only.
- **E5B.** No E5B plan or result existed.
- **Environment.** Python 3.12.3, numpy 2.5.3; scipy not installed. Baseline full suite: 834 passed (167 s).

## Chronology

| Commit | Content |
| --- | --- |
| `9719cab` | Prompt (verbatim) and `docs/gt-p010-hub-and-e5b-audit.md`: baseline, hub pin and pins, shared questions, CL-T85/T88/T89 scope comparison, the E5A **2/30** qualification, exposure, and pre-freeze decisions. **Before any E5B computation** |
| `82f78fb` | `docs/e5b-definitions-controls-and-feasibility.md` (T9–T11); `rs_constraint_lab.gtrenew`; `rs_constraint_lab.gte5b`; tests `test_gtrenew.py` (21) and `test_gte5b.py` (10). Full suite 865 passed (187 s); CI success, run 38783784368 |
| `fc3ec7d` | **Freeze:** `plans/round-e5b-plan.json`, plan_hash `c35bc3bb…d944`, source `82f78fb`, consulted hub `38c2501` |
| `86e2df1` | Journey step 26, pushed before execution |
| (run) | 2026-10-15 18:17:44Z to 18:20:38Z: `python -m rs_constraint_lab.gte5b run --commit fc3ec7d…`; 12/12 complete |
| `fcb17ae` | **Results:** `reports/round-e5b-tables.json` (payload `0d307350d1ac…c2d1`) and `reports/gt-e5b-atlas.md` |
| this commit | Report, reflection, ledger GT-F83–F90, GT-Q23–Q24, GT-R143–R155; map; snapshot `through-gt-e5b.md`; hypotheses (E5B columns); bridge-map section 12; OP-20; transfer note T-17–T-20; hub handoff; README; roadmap; journey step 27; this record |
| close | Provenance ledger row with the CI result of the synthesis commit |

## Pre-freeze computations (no E5B quantity of an N=5 or N=6 scientific cell)

| Computation | Fixture | Purpose |
| --- | --- | --- |
| NULL analytic control (L_local = \|LOCAL\|·L_CT), flicker closed form 1/M | NULL N = 3, 4 | Proofs (tests) |
| Independent augmented-observer route | N = 4 NULL, PCOMP, CLOSEW; synthetic N = 5 neighbourhood rule (not a GT family) | Renewal and departure solver verification (agreement 1e-9, 1e-8) |
| Monte Carlo trajectories | N = 4 NULL, 40,000 episodes | Independent check of L_local and renewal |
| NK propositions | synthetic uniform-law heterogeneous chains, N = 4, 5 | T11 checks; analytic law against an independent solve |
| Runner plumbing | the six families at N = 4 | Checks, assembly, CLI refusal |
| Timing | published NULL N = 6 (permitted by the prompt) | about 9 s per law per anchor set; peak 330 MB. Only timings and solver sizes were printed |

**One numerical fix before freezing.** Within-layer variance was first computed as E[q²] − E[q]², which cancelled catastrophically; NK's exactly zero dispersion showed as 1.4×10⁻⁵. It was replaced by a two-pass formula, and the fixture test caught the error.

## Execution and checks

- 12/12 items complete; 36/36 predicate analyses; every per-item frozen check passes; the N0 analytic control passes at both sizes.
- E5A replication: exact (worst/tolerance 0).
- Hitting solves: at most 29 iterations, relative residual ≤ 1e-12; dense against iterative ≤ 3.0×10⁻¹²; no bound violations; no unresolved channel.
- NK resolved for every law. Rare layers were flagged as frozen (for example N=6 PATHF and PATHH layers down to about 10⁻⁴⁰), and nothing was smoothed.
- F_STAR complete renewal is labelled STRUCTURALLY_IMPOSSIBLE for every law, both sizes, and every comparator.
- Total wall time is about 3 minutes, against the 3 h cap.

## Deviations and qualifications

- None from the frozen plan.
- The optional durable-renewal filter and the anchor-local sensitivity analysis were deliberately not attempted; this was recorded before the freeze.
- E5A's two numerically qualified CT hub-lag channels are outside E5B and were not reclassified.
- E5A's intact count is corrected to 2/30 (append-only, GT-F90). GT-P009's files are unedited.

## Hub boundary

No file under `research-synthesis/` exists on, or was added to, the GT branch. No hub command was run, and the hub GT pin stays at `79fa6b0` until a reviewed update. The handoff is `docs/gt-p010-shared-synthesis-handoff.md`.

## Stop

No E5C, no merge, no ontology change. Recommended next (not run): a durable-renewal test on the rows above NK, or no further round.
