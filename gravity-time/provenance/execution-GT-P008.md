# Execution record — GT-P008 (sorting mechanism, reference architecture)

- **Prompt.** `provenance/prompts/GT-P008-agent-input.md`, an agent transcription: 34,068 bytes, sha256 `c9184c9fa8310b4c5ea79b1370baab8f8358ec89fbba6c6f361b0f4952a5ea6e`. It has not been compared with the authored external file, and no byte identity is claimed.
- **Agent.** Claude Opus 5.5, assisting one human researcher.
- **Branch.** `research/gravity-time-admissibility`. Draft PR #6, not merged.
- **Mandate.** A mathematical and architectural consolidation. **No E5 round was opened, frozen or executed. No new scientific cell was computed.**

## Starting state (verified)

- **Remote head:** `11f62df0c56a866e46c212fbb86f4dc5623fb2e6`, equal to the local head; worktree clean.
- **PR #6:** open and draft. **CI:** success on `11f62df`. **`main`:** `05b15b0`. OTR sha256 `2d902395…88dd` on the branch and on `main`.
- **E4 tables:** payloads `f050380ac32e` and `169e71c33b38` re-hashed from canonical JSON and matching.
- **Earlier records:** no published plan or report changed since `11f62df`. The recorded suite at GT-P007 close was 748 passed.
- **The baseline had not moved.**

## Chronology

| Commit | Content |
| --- | --- |
| `fe7701a` | Prompt stored; prompt ledger row |
| `56ae926` | **Coverage and integrity audit**, with definitions D1–D8 of every secondary quantity, pushed **before** any derived quantity was computed. Qualifications Q-1 to Q-3 |
| `6bd1e0c` | `rs_constraint_lab.gtsort` (witness algebra, first-order coefficients, an independent CLOSEW Gibbs law, D1–D8 views); `tests/test_gtsort.py` (48 tests); `reports/gt-p008-secondary-analyses.json` |
| `fb04d72` | Workstream A: `docs/e4-sorting-mechanism-derivation.md`, `reports/gt-p008-secondary-analyses.md`, audit addendum (Q-4) |
| `1b5587c` | Workstream B: `docs/reference-architecture-review.md`, `docs/gt-p008-next-round-options.md` |
| (this commit) | Consolidation report; bridge-map revision 3 (sections 1–9 unchanged); transfer note; ledger GT-F67–F73, GT-Q18–Q20, GT-R111–R127; views and snapshot `through-gt-p008.md`; hypotheses (GT-P008 column; H-META); OP-16 qualification and OP-18; README; roadmap; journey step 23; this record |

## What was computed, and on what

| Computation | Data | Status |
| --- | --- | --- |
| Template algebra, floors, NULL expectations, first-order coefficients | None: pure combinatorics, exact fractions | Algebra |
| Enumeration of connected held graphs on ≤ 5 vertices (floor and closed-form checks; first-order reversal search) | None: closed-form expressions over graphs, no dynamics | Algebra |
| Per-event first-order covariance | The uniform NULL product law, enumerated (≤ 2^14 configurations) | Algebra: NULL is uniform by theorem |
| CLOSEW Gibbs law | Recomputed independently from π ∝ 2^(#triangles) for the 8 published CLOSEW geometries | **Extraction check** against published values (agreement to 3e-15); not new science |
| Proof fixtures | Synthetic-ε (±10^−4, and ln 2 for PCOMP and CLOSEW) kernels at **N = 4** (not an E4 or E5 size) under K2, P3, K3 and a two-edge star; random synthetic rate chains on 6 slots | Proof verification only; no E4 observable read |
| Post hoc views D1–D8 | Published E4A and E4B tables only | Explanatory; **not E5 evidence**; the data were fully exposed beforehand |

No E4 cell was rerun. No N=7 or FREE N=7 computation, no grade sweep, and no multi-source dynamics.

## Tests and CI

- `tests/test_gtsort.py`: 48 passed.
- Full suite: see the execution row in `provenance/ledger.jsonl`. The count and the CI result are recorded there after the push, because this file is part of the commit being tested.

## Deviations and notes

1. **An extra extraction check was added after the definitions were fixed:** NULL witness means against the S4 closed form. It is declared in the audit addendum (§7). It is a correctness check, not a scientific quantity.
2. **Wording corrections before commit:**
   - the derivation's template-count range was 11–24, now 10–24;
   - the opening statement of the lever now says "factor as 2^(−floor) × a residue", not "multiplies by exactly ½";
   - the report's triangle reversal is now restricted to 5 entities.
3. **Earlier documents were not edited.** Qualifications of GT-P007 wording are recorded append-only:
   - audit Q-1 to Q-4;
   - ledger GT-F73;
   - OP-16 qualification.

## Results (summary)

See `reports/gt-p008-consolidation-report.md`.
- **Exact floor lever in the odds** (GT-F67).
- **First-order sorting index** floor + (7 − N)·held degree, with weak-coupling reversals (GT-F68).
- **Clock-separated sorting**, and the first-order equality of the equal-ratio pair (GT-F69).
- **The margin changes sign with strength** for K3 N=5 (GT-F70).
- **Post hoc decomposition:** the floor term is 71–100% of the contrasts, and the index has the right sign in 16/16 continuous and 19/20 per-event contrasts (GT-F71).
- **No labelled centre at finite N;** emergent references can only be metastable (GT-F72).
- **Qualifications** of the GT-P007 wording (GT-F73).
- **Recommended, not run:** option C (FREE persistence feasibility, definitions first); fall-back option B (floor-reversal test).
