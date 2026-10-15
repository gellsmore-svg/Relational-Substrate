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
