# Execution record — GT-P003 (E1 observable scaling and pre-freeze review)

- **Prompt:** `provenance/prompts/GT-P003-agent-input.md` (agent transcription; ledger row of 2026-10-14).
- **Agent:** Claude Opus 5.5.
- **Branch:** `research/gravity-time-admissibility`. Draft PR #6, not merged.
- **Starting commit:** `4dacd11` (E1 kernel step). CI on it was green.
- **Method:** OTR 1.0. The definition on this branch is byte-identical to `main` (sha256 `2d902395…dd`). Only `research-methods/README.md` differed; it was synced from `main` in `4ed3e22`, so the branch carries one version.

## Boundary kept

- **No E1 plan was created, frozen or pushed.** There is no `plans/round-e1-plan.json` and no E1 entry in `plans/journey.jsonl`.
- **No N=7 scientific cell was computed.** No E0C, G2 or substitute round was opened.
- PR #6 is not merged. CBO, Appendix E, the RS baseline and other laboratory branches are untouched. No cherry-picks.
- G0, G1, E0A and E0B plans, tables and payloads are unchanged. Their qualifications are ledger entries (GT-F34, GT-F35), not edits.

## Commits

| Commit | Content |
| --- | --- |
| `4ed3e22` | GT-P003 prompt stored; OTR README synced from `main` |
| `8414d7c` | Code: `gtobs`, `gtobs_validate`, `gtobs_fixtures`, `gtscale`; `gtkernel` alphabet argument; 86 tests |
| (this commit) | Documents, census and decomposition reports, fixture records, validation log, ledger GT-F34/F35, roadmap proposal, execution record |

## Kinds of operation

| Kind | What | Exposure |
| --- | --- | --- |
| Engineering validation | Recomputation of all 84 published E0 cells (N=5, 6) by `gtobs`, with GTH and strict two-start referees; exact rational GTH solve of HELD N5 PATHF weak_favour | Already-published cells only |
| Mathematical analysis | Witness bounds and null means (closed form); census over the candidate space for N=5, 6, 7 | Law-free |
| Theorem-fixed baselines | NULL occupancy baselines at N=5, 6, 7 (uniform law by theorem) | Theorem-fixed values |
| Cost fixtures at N=7 | HELD and FREE NULL; HELD CLOSE strong_favour, full pipeline. Only costs and solver checks recorded (`provenance/e1-fixtures/`). FREE CLOSE was not run, because FREE NULL already measured the cost | Theorem-fixed (uniform law; closed-form Gibbs law). CLOSE is not a proposed E1 cell |
| Post hoc channels on published cells | Engaged witness census, margin decomposition, hub structure at N=5, 6 (`reports/e1-engaged-witness-n5-n6.json`, `reports/e1-margin-decomposition-n5-n6.json`) | Labelled post hoc; recorded as GT-F34 (qualification of GT-F26) |
| Scientific E1 execution | None | — |

Pre-freeze exposure carried forward for an eventual E1 plan:
- the HELD N7 PATHF weak_suppress chain build (E1 kernel step);
- the theorem-fixed fixtures and baselines above;
- the post hoc N≤6 channels.

## Results

- **Reproduction.** 84 of 84 published cells. 67 agree on every compared channel; 17 differ only where a referee shows E0 wrong (15 dense-solve, 2 unconverged iteration); 0 are unexplained. Log: `provenance/e1-observables-validation.log` (code `8414d7c`, 12 min, 347 MB).
- **Tests.** Full constraint-lab suite: 510 passed (424 before, plus 86 new), locally, at `8414d7c`.
- **Fixtures at N=7.** HELD 136 s and 450 MB per cell. FREE NULL 25 min and 3.2 GB. The solver reproduces the analytic Gibbs law to 2.7e-16 at HELD N7.
- **Main design observations.**
  - The CSPH margin is clock- and density-dependent (GT-F34).
  - The engaged witness load of non-gradient composites grows far less than the null witness count.
  - The existing W3/W16 sensitivity alphabets give a within-grammar strength bracket.
  - Option B is recommended for review (`docs/e1-design-alternatives.md`).

## Deviations and notes

- **Autocorrelation factor.** An early draft of the autocorrelation series had the lazy-chain factor inverted (2 instead of ½). It was caught by the first reproduction of HELD N5 NULL (τ = ½ for an edge indicator) and fixed before any commit.
- **GT-F35 corrected before commit.** It was first drafted from N=5 evidence (2.9e-6 relative). The final N=6 run showed much larger errors at negligible mass (clipped states, spurious one-sided transitions), and the entry was corrected before it was committed.
- **Autocorrelation timings.** The loop was made allocation-free after the fixtures ran (HELD N7 90 s → 73 s, results unchanged). The fixture records keep the earlier, conservative times.
