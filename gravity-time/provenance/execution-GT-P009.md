# Execution record: GT-P009 (FREE persistence, turnover, endogenous reference feasibility)

- **Prompt.** `provenance/prompts/GT-P009-agent-input.md`.
  - It is an agent transcription: 35,221 bytes, sha256 `058c120ddbf6032101d3a5f8205c7e9822dabba5df79adde0f7db451b63f456c`.
  - It has not been compared with the authored external file, and no byte identity is claimed.
- **Agent.** Claude Opus 5.5, assisting one human researcher.
- **Branch.** `research/gravity-time-admissibility`; draft PR #6, not merged.
- **Mandate.**
  - Authorised: definitions and engineering, **one** frozen-and-pushed E5A round, then reflection and coherence updates.
  - Not authorised: **E5B.**

## Starting state (verified)

- **Heads.** Remote head `a73cd0260f38885121a89a607efa73e98732e59f`, the same as the local head and the expected GT-P008 baseline. Worktree clean.
- **PR #6.** Open, draft; base `research/constraint-lab-v0.8g-formal-integration`.
- **CI on `a73cd02`.** Success: push run 38696273921, pull_request run 38696281378.
- **`main`.** `05b15b0`.
- **OTR.** sha256 `2d902395…88dd`, identical on the branch and on `main`.
- **Existing E5 artefacts.** No E5 plan, table or report existed, and the branch had not moved.
- **Environment.** Python 3.12.3, numpy 2.5.3; scipy not installed. Full suite: 796 passed (163 s).

## Chronology (pre-freeze)

| Commit | Content |
| --- | --- |
| `2bd18c6` | Prompt transcription and prompt ledger row |
| `e72e3e8` | `docs/e5-coverage-and-definition-audit.md`: baseline, exposure (all 12 kernels are published E0B cells), decisions D-1 to D-11, risks. **Before any E5 computation** |
| `1ba3fe7` | `docs/e5-definitions-and-null-construction.md` (T1–T8 with proofs); `rs_constraint_lab.gtpersist`; `rs_constraint_lab.gte5a`; `tests/test_gtpersist.py` (31) and `tests/test_gte5a.py` (7), on synthetic chains and N ≤ 4 only. Full suite 834 passed |
| `1c91766` | `gte5a` publishes the plan's source commit in the tables |

## Pre-freeze computations (none on an E5A cell)

| Computation | Fixture | Purpose |
| --- | --- | --- |
| NULL closed forms, episode flux, Ω, lag decay | N = 3, 4 NULL; two-state CTMC; random rate chains on 6 slots | Proof verification (tests) |
| Families at N = 4 (not an E5A size) | NULL, PATHF ws, PATHH wf, CSPH, CLOSEW, PCOMP | Covariance, intact-turnover theorem, PCOMP uniformity, lumpability, expm checks, runner plumbing (tests) |
| ND | Synthetic non-uniform p_k at N = 4, including a 10^−13 interior bin | Construction checks |
| Stiff expm | N = 4 CLOSEW with a synthetic factor of 2^6 (reversible), against an exact symmetrised eigen-solution | Accuracy |
| Timing, N = 6 | NULL N=6 with all rates × 2^24 (synthetic; values follow from NULL by time rescaling); a synthetic covariant density-only rule with dissolution 2^k (not a GT family) | Cost: predicates (12 instances) 0.1 s, stationary 1 s, lagged hub 11–24 s per law, killed solves under 1 s; peak 632 MB. Only timings and numerical checks were printed |

**A finding during engineering.** An interior ND bin of 10^−13 makes the ND chain nearly reducible: its smallest unscaled rate was 2×10^−12, and the iterative solvers did not converge in 2,000,000 iterations. ND's law is therefore taken in its analytic form, verified by balance, and the iterative solve is a cross-check only. This was declared before freezing (definitions §5).

## Freeze, execution and results

- **Frozen plan commit:** `1dc43c66ced3d01add844b46b43fe60335222562`, containing only `plans/round-e5a-plan.json` (22,091 bytes, file sha256 `7d79ebbf877d08575971d9585e5150d412e9d524b7a68724396ab0a417e7aff3`, plan_hash `31202d70b850b1ca046d4897b3e551bb40c2df68e81d8ddd701aab347b0d97a8`).
- **Source commit:** `1c91766`. CI succeeded there before the freeze (push run 38710597748, pull_request run 38710607908).
- **Remote check:** the plan commit was pushed and `origin/research/gravity-time-admissibility` contains it. The plan bytes at the commit re-hash to the file sha256 above.
- **Journey step 24:** recorded before execution.

### Execution

- **Command:** `python -m rs_constraint_lab.gte5a run --commit 1dc43c6…`. The runner refuses a plan commit that is not on a remote-tracking branch or whose manifest has drifted.
- **Timing:** started 2026-10-15T09:11:09Z, finished 09:13:27Z.
- **Items:** 12/12 complete, on 4 workers.
  - N=5 items: under 1 s each.
  - N=6 items: 38–110 s each, peak 669 MB.
  - No watchdog fired, and the wall cap was not reached.
- **Generated item files:** `gravity-time/generated/round-e5a/` (gitignored).
- **Publication:** `python -m rs_constraint_lab.gte5a publish` and `atlas`. Tables payload `6e978571d83ea17448dfcb03eb59083eca71dda4c1fbbd01a4d2dad7e1a73633`.
- **Results commit:** `59eb682`.

### Frozen checks: 32 of 34 hold

**Holding:**
- every replication of the published E0B laws (class masses and mean rates within max(10^−10, 10^−8 × published));
- the NULL closed forms and NULL lag closed forms at N = 5, 6;
- the ND fixed point;
- PCOMP CT uniformity;
- PCOMP ND = scaled NULL;
- every per-item check on 10 of 12 items.

**Not holding (recorded, not repaired):**
- `Z-FREE-N6-PATHH-weak_favour`. The CT lag propagator:
  - row-sum error 9.7×10^−9;
  - stationarity L1 6.6×10^−9;
  - the comparison-degree spread 9.2×10^−9.

  The frozen tolerance is 10^−9 for all three. The matrix exponential needed 22 squarings (25 in the semigroup check).
- `Z-FREE-N6-CSPH-strong_favour+weak_favour`. The CT lag propagator row-sum error was 3.4×10^−9, after 21 squarings.
- **Independent checks on both items held:** the non-dyadic semigroup check (≤ 2.4×10^−10), lumpability (0), lumped against full jump chain (≤ 9×10^−16) and pair-permutation covariance (0).
- **Interpretation:** rounding accumulates over repeated squaring of a stiff generator, with rates spanning about 10^7. The CT lag values of these two items are reported as **numerically qualified**, with errors of about 10^−8. Their JT lag values and every episode, turnover and ND channel are unaffected.

### Secondary channel

All 144 killed-chain solves (12 items × target and ND × 6 predicates) converged. The entrance first-passage mean reproduces every flux lifetime within 2.6×10^−10, and residual life obeys the Palm bound everywhere.

### Post hoc identities (derived after the results; verified on the published tables)

- **ND matches edge lifetime.** E_π[q] = 2M·J_edge, so ND's CT edge present-lifetime equals the target's: within 7×10^−15 on 12 items.
- **Form-only intact lifetime.** Formation-only families give an intact-motif L_CT of exactly 1/r.
- **PATHF's ND is fully matched.** It has c = 1, unit deaths and the same JT density (L1 ≤ 2×10^−14).

These are labelled post hoc in every document.

### Deviations

1. **No change to plan, cells, predicates, comparators or tolerances after freezing.**
2. **Two frozen checks failed.** See above: they were recorded, not repaired.
3. **The ND comparator proved weaker than intended.** It controls density and average edge lifetime, but not the arrangement of activity (GT-F78, GT-F79). This is recorded as a lesson for a later round, not corrected in this one.

### Documents (after results)

- `reports/gt-e5a-report.md`, `reports/gt-e5a-reflection.md`, `docs/gt-e5a-cross-programme-transfer.md`.
- Bridge map section 11 (revision 4; sections 1–10 byte-identical).
- Ledger GT-F74 to GT-F82, GT-Q21, GT-Q22, GT-R128 to GT-R142; views; snapshot `through-gt-e5a.md`.
- Hypotheses: E5 columns (earlier fields unchanged) and the new artefact X-KINHET.
- OP-19.
- README; roadmap.
- Journey step 25.

**No E5B was frozen or executed.**

## Tests and CI

The full suite count and the CI result after the push are recorded in the execution row of `provenance/ledger.jsonl`. This file is part of the commit being tested.

