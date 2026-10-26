# Execution record — GT-P004 (E1 option B: freeze, execute, interpret)

- **Prompt:** `provenance/prompts/GT-P004-agent-input.md` (agent transcription, 18,630 bytes, sha256 `696094b8…`; ledger row of 2026-10-14).
- **Agent:** Claude Opus 5.5.
- **Branch:** `research/gravity-time-admissibility`. Draft PR #6, not merged.
- **Starting commit:** `31620b6` (GT-P003 close). It was verified as the remote head, with a clean worktree, PR #6 an open draft and CI green on both events. The OTR definition was unchanged (sha256 `2d902395…`).
- **Method:** OTR 1.0.

## Mandate kept

- **Option B only.** That is 8 HELD N=7 W4 cells plus 24 W3/W16 cells at HELD N=5 and 6, with 16 labelled re-derivations of published N=5 and 6 W4 cells.
- **Not run:** FREE N=7, any further grade, alphabet or size, and any new round (E2, G2, G3).
- **No new primitive, no grammar change, no post-result tuning.** The plan was frozen and pushed before any round cell ran, and nothing in it changed afterwards.
- **Preserved unchanged:** the G0, G1, E0A, E0B and GT-P003 plans, tables and documents. The GT-P003 design draft's exposure list named FREE CLOSE as run; it was never run. The frozen plan records the correct exposure, and the draft is left as written.
- **Not edited:** CBO and the other programmes' branches.

## Chronology

| Commit | Content |
| --- | --- |
| `729f30c` | GT-P004 prompt stored; ledger row |
| `43105de` | Engineering: `gte1` round runner, `gtobs.event_pattern_probabilities` (split out of `event_order`, no change in behaviour), CLI wiring, 46 tests. Suite 556 passed |
| `4ba2839` | **Frozen plan** `plans/round-e1-plan.json`, hash `c6328d51b3062732cc451f2fefb84557972252ec06b7fb35a588eafd9cc4f144`; pushed. Plan file sha256 `d7b8a73e…` |
| `4b6bbf0` | Journey step 9 (E1 opened under `4ba2839`); pushed before execution |
| — | Execution 14:00:02–14:24:09 UTC. `gte1 run` checked that the frozen commit is an ancestor of HEAD, is on the remote, and that the contract has not drifted |
| `730ef32` | **Result commit:** tables (payload `f1727f9d3c3f…`, file sha256 `f6ab204a…`), atlas and its generator, one more test |
| (this commit) | Report, reflection, post hoc decomposition, ledger, register, ontology proposals, README, roadmap status, execution record, journey close |

## Pre-freeze work and exposure

- **Engineering** used only synthetic N=4 cells (W4, W3, W16) and published N=5 and 6 W4 cells. The published cells used were CSPH, PATHH, NULL and CLOSEW at N=5, plus CSPH at N=6 for timing.
- **Budget** was checked on this host using the theorem-fixed HELD N=7 CLOSE strong_favour fixture, which is not a round cell; only costs and solver checks were read. The full pipeline took 156 s at 590 MB. The published N=6 CSPH cell took 43 s at 300 MB.
- **Normalised-margin guard.** At N=4 the null ceiling r0 is 1, so the normalised margin is undefined. A guard returning None was added before freezing. It cannot trigger at N=5–7.
- **Tests** rebuilt the HELD N=5 W16 PATHF kernel (weights only).
- **Full exposure declaration:** in the plan, `pre_freeze_exposure`, with hashes of 20 reference files.

## Execution

- **Workers and time.** Four worker processes, single-threaded BLAS. Round wall time 1,446 s against a 14,400 s cap. Sum over cells 5,826 s.
- **Statuses.** 48 complete; none unresolved, killed by the watchdog, failed or capped.
- **Cost against estimate.** The N=7 cells took 287–615 s each against the 3–6 minute estimate. They ran four at a time, which plausibly explains the difference, but that was not measured separately. Peak memory was 592–603 MB.
- **Numerical checks.** Every cell passed every per-cell check:
  - stationary residual and two-start agreement;
  - a third start from the fullest state;
  - the per-entry long-double residual, with no zero-mass state;
  - the GTH referee at N≤6;
  - the rule strings evaluated exactly on 128–402 sampled states;
  - the symmetry check;
  - the autocorrelation series below its cap.
- **Controls.**

  | Control | Holds |
  | --- | --- |
  | Z1 NULL identity | 3/3 |
  | Z2 gradient law | 3/3 |
  | Z3 non-gradient rates | 42/42 |
  | Z4 published replication | 16/16 |
  | Z5 numerical acceptance | 48/48 |
  | Z6 hub-frame controls | 6/6 |

- **Rare conditionals.** Conditionals on rare mass (below 1e-12) are flagged in 37 cells, all at high free-relation counts. They are kept and not interpreted.

## Per-cell cost

| Item | Tranche | Role | Status | Wall s | Peak MB |
| --- | --- | --- | --- | --- | --- |
| HELD-N7-W4-CSPH-strong_favour+weak_favour | I | open_scientific | complete | 615.4 | 593 |
| HELD-N7-W4-CSPF-strong_favour+weak_suppress | I | open_scientific | complete | 511.9 | 592 |
| HELD-N7-W4-CWPH-weak_favour+weak_favour | I | open_scientific | complete | 527.0 | 592 |
| HELD-N7-W4-CWPF-weak_favour+weak_suppress | I | open_scientific | complete | 351.3 | 603 |
| HELD-N7-W4-PATHF-weak_suppress | I | open_scientific | complete | 287.5 | 594 |
| HELD-N7-W4-PATHH-weak_favour | I | open_scientific | complete | 484.5 | 603 |
| HELD-N7-W4-NULL-none | I | identity_control_exposed | complete | 437.1 | 593 |
| HELD-N7-W4-CLOSEW-weak_favour | I | gradient_control | complete | 555.3 | 603 |
| HELD-N5-W4-CSPH-strong_favour+weak_favour | baseline | baseline_rederivation_published | complete | 0.2 | 45 |
| HELD-N5-W4-CSPF-strong_favour+weak_suppress | baseline | baseline_rederivation_published | complete | 0.1 | 45 |
| HELD-N5-W4-CWPH-weak_favour+weak_favour | baseline | baseline_rederivation_published | complete | 0.1 | 45 |
| HELD-N5-W4-CWPF-weak_favour+weak_suppress | baseline | baseline_rederivation_published | complete | 0.2 | 45 |
| HELD-N5-W4-PATHF-weak_suppress | baseline | baseline_rederivation_published | complete | 0.1 | 45 |
| HELD-N5-W4-PATHH-weak_favour | baseline | baseline_rederivation_published | complete | 0.1 | 45 |
| HELD-N5-W4-NULL-none | baseline | baseline_rederivation_published | complete | 0.1 | 45 |
| HELD-N5-W4-CLOSEW-weak_favour | baseline | baseline_rederivation_published | complete | 0.1 | 45 |
| HELD-N6-W4-CSPH-strong_favour+weak_favour | baseline | baseline_rederivation_published | complete | 89.3 | 301 |
| HELD-N6-W4-CSPF-strong_favour+weak_suppress | baseline | baseline_rederivation_published | complete | 90.4 | 302 |
| HELD-N6-W4-CWPH-weak_favour+weak_favour | baseline | baseline_rederivation_published | complete | 82.3 | 301 |
| HELD-N6-W4-CWPF-weak_favour+weak_suppress | baseline | baseline_rederivation_published | complete | 92.1 | 302 |
| HELD-N6-W4-PATHF-weak_suppress | baseline | baseline_rederivation_published | complete | 102.2 | 302 |
| HELD-N6-W4-PATHH-weak_favour | baseline | baseline_rederivation_published | complete | 96.1 | 302 |
| HELD-N6-W4-NULL-none | baseline | baseline_rederivation_published | complete | 98.7 | 301 |
| HELD-N6-W4-CLOSEW-weak_favour | baseline | baseline_rederivation_published | complete | 95.9 | 302 |
| HELD-N5-W3-CSPH-strong_favour+weak_favour | II | open_scientific_bracket | complete | 0.2 | 45 |
| HELD-N5-W3-CSPF-strong_favour+weak_suppress | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N5-W3-CWPH-weak_favour+weak_favour | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N5-W3-CWPF-weak_favour+weak_suppress | II | open_scientific_bracket | complete | 0.2 | 45 |
| HELD-N5-W3-PATHF-weak_suppress | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N5-W3-PATHH-weak_favour | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N5-W16-CSPH-strong_favour+weak_favour | II | open_scientific_bracket | complete | 0.2 | 45 |
| HELD-N5-W16-CSPF-strong_favour+weak_suppress | II | open_scientific_bracket | complete | 0.2 | 45 |
| HELD-N5-W16-CWPH-weak_favour+weak_favour | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N5-W16-CWPF-weak_favour+weak_suppress | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N5-W16-PATHF-weak_suppress | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N5-W16-PATHH-weak_favour | II | open_scientific_bracket | complete | 0.1 | 45 |
| HELD-N6-W3-CSPH-strong_favour+weak_favour | II | open_scientific_bracket | complete | 109.2 | 301 |
| HELD-N6-W3-CSPF-strong_favour+weak_suppress | II | open_scientific_bracket | complete | 108.1 | 301 |
| HELD-N6-W3-CWPH-weak_favour+weak_favour | II | open_scientific_bracket | complete | 120.5 | 302 |
| HELD-N6-W3-CWPF-weak_favour+weak_suppress | II | open_scientific_bracket | complete | 114.7 | 301 |
| HELD-N6-W3-PATHF-weak_suppress | II | open_scientific_bracket | complete | 114.5 | 301 |
| HELD-N6-W3-PATHH-weak_favour | II | open_scientific_bracket | complete | 116.0 | 302 |
| HELD-N6-W16-CSPH-strong_favour+weak_favour | II | open_scientific_bracket | complete | 115.3 | 301 |
| HELD-N6-W16-CSPF-strong_favour+weak_suppress | II | open_scientific_bracket | complete | 116.1 | 301 |
| HELD-N6-W16-CWPH-weak_favour+weak_favour | II | open_scientific_bracket | complete | 117.0 | 301 |
| HELD-N6-W16-CWPF-weak_favour+weak_suppress | II | open_scientific_bracket | complete | 115.7 | 301 |
| HELD-N6-W16-PATHF-weak_suppress | II | open_scientific_bracket | complete | 80.2 | 302 |
| HELD-N6-W16-PATHH-weak_favour | II | open_scientific_bracket | complete | 78.6 | 302 |

## Post-result analysis and deviations

- **Post hoc decomposition.** After the results, the change in each margin was split into an occupancy part and a preference part (`reports/e1-margin-composition-posthoc.json`). It is labelled post hoc everywhere and is not a frozen comparison. It changed the report: a first draft said CSPH's N=7 loss was "a change of occupied density, not a loss of the local preference". The decomposition shows that about two thirds of the loss is preference. The draft was corrected before publication.
- **Numbers checked before publication.** Every number in the report and reflection was checked against the tables before commit. Four unverified or rounded values were corrected: detachment ranges, the per-density excess, the a/k entries at k = 4–5, and the crowding-adjusted range.
- **Attention coordinates.** The six-coordinate attention scale used in earlier journey rows is not defined in GT records. The next-step comparison therefore lists the OTR section 6 factors separately (reflection, section 6), and the journey row says so.
- **Spectrum.** The spectrum is unavailable in every E1 cell, because gtobs does not compute it. It is recorded as unavailable, not zero.

## Results (summary)

See `reports/gt-e1-report.md`.
- CSPH's basin-with-arrow coexistence does not survive to N=7 (GT-F36).
- The handover orientation holds in 30 of 30 non-gradient cells (GT-F37).
- Engaged witness load is size-stable (GT-F38).
- Strengthening is not a quantitative proxy for size (GT-F39).
- Strengthening splits CSPH's clocks (GT-F40).
- The gradient control's standardised preference grows with N (GT-F41).
- Recommended next step, not executed: a handover-mechanism investigation (`reports/gt-e1-reflection.md`, section 6).
