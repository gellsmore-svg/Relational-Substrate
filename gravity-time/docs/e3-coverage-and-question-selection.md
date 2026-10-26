# GT-P006 coverage audit and question selection (before E3A)

*Prompt GT-P006, deliverable 1. Written before the E3A plan was frozen and before any E3A cell was computed.*

## 1. Starting state (verified)

- **Repository.** Branch `research/gravity-time-admissibility` at `afb5d73`. Clean worktree; CI green on both events; PR #6 an open draft. OTR 1.0 is byte-identical to `main`.
- **Test baseline.** 608 tests at `afb5d73`.
- **Materials read:**
  - the GT charter, roadmap, ontology proposals, register, journey and ledger;
  - all GT-P005 documents, plans, tables and code (`gte2a`, `gte2b`, `gtobs`, `gtkernel`, `gte1`);
  - read-only from the laboratory: the plan discipline and 8G gate, `open-problems.md` (CL-Q04, CL-Q05), the theorem catalogue (CL-T18, CL-N02, CL-Q05), and `passage.py` (its eventual hit-before-return committor on O=3 pair-class epochs).

## 2. What E2 already settled, and what it did not

| Question (GT-P006 section 3) | Settled by E2? | What remains |
| --- | --- | --- |
| Q1 What generates and orients one-way release | Partly. One-way transitions are releases (E2B); orientation + for soft σ ∈ {0, +log 2, −log 2} | Why +? How does the hard zero relate to soft suppression? Can any available opposing term reverse it? |
| Q2 How is a released relation recovered | No | Routes, gate distance, probability, time |
| Q3 Temporary non-reformability against arrest, absorption, persistence | Partly: absorption under hard dissolution prohibition (E2) | That HPF releases are always recoverable is now proved (T3); recovery kinetics are unmeasured |
| Q4 Conditional persistence | No | Absence duration after witnessed versus unwitnessed release; direct versus gated recovery |
| Q5 One-way release with weak or reversed aggregate | No | Partner-index split into pairs with and without one-way steps; strongest available opposing dissolution |
| Q6 Imposed versus emergent reference | Partly: the held source is a hard witness (E2) | The held source as a *soft* witness (strong suppression) |
| Q7 Preconditions for direction or displacement | Not addressed | Only definitions; no displacement observable exists (bridge map) |
| Q8 Unexpected boundaries | — | Open |
| GT-Q12 | Regularity 36/36; no proof | Bounded counterexample search |

## 3. Novelty and equivalence audit

- **Relabelling.** Every template is label-covariant. Cells differing only by labels are not separate cells.
- **Rate rescaling.** Multiplying every rate by a constant leaves the jump chain, the event order and the partner index unchanged, and rescales continuous times. No cell differs from another only by a global factor.
- **Clock.**
  - Recovery is reported in jump events *and* in continuous time; neither is primary.
  - Gate distance counts admissible steps and has no clock.
- **Projection.**
  - The partner frame is defined per state, from degrees. The class-free and hub frames are kept beside it (gte2a channels).
  - The release classes ("witnessed" or not) are structural; they do not depend on any rule.
- **Reused kernels.** 8 of the 27 cells are published E2A/E2B kernels at N=5 (listed in the plan). Their earlier channels are known; recovery, gate, split and scan channels are new.
- **Equivalence within the round.**
  - PFD strong_suppress+strong_suppress (W16) and NULL have the same (uniform) law, but different kinetics. That makes them the right pair to separate law from kinetics in recovery.
  - EXCL and NULL differ in support (EXCL forbids triangles).
- **Not repeated.**
  - Every E2 grade of the single path components at N=5 (E2A covers them).
  - E2B's hard closure and adjacency exclusions: no one-way edges (closure), or inert paths (adjacency).
  - N=6, and N=7 FREE.

## 4. Selected questions and why they serve several possibilities at once

1. **The formation ladder** (factor 1/2, 1/4, 1/9, 1/16, 0; FREE N=4 and 5).
   - It separates "one-way release is the extreme of soft formation suppression" from "it is a distinct admissibility mechanism".
   - It measures persistence of absence as a function of how hard re-formation is.
   - Its soft rungs give the matched comparison for the hard rung's releases.
   - The rungs use the existing W4, W3 and W16 alphabets only. The hard zero is not treated as their limit.
2. **Hard path-form exclusion against the strongest available opposing dissolution** (soft σ = −log 2, −log 4, −log 16). This tests whether the one-way orientation can be reversed at all within the grammar. It matters for Q5 and for the domain of the σ account.
3. **Soft controls:**
   - a rate-symmetric σ = 0 pair, uniform and reversible, with strong suppression on both sides;
   - a soft σ < 0 pair without a hard component, to show what soft reversal looks like with the same dissolution term.
4. **Reversible hard exclusion (EXCL) and NULL.** These give the structural baseline for recovery: how long a path-witnessed relation stays absent when no rule reads path witnesses.
5. **HELD scaffold.** The held triangle as a soft witness (strong suppression, W4 and W16) and as a hard one.
6. **GT-Q12 scan.** A bounded counterexample search over synthetic factor pairs at FREE N=4 and 5. This is a mathematical search, declared as such. It is not a model of hard limits and not a new alphabet.

**Scale.** 27 cells (8 reused, 19 new) plus 2 scans of 81 points: 29 analyses. Estimated cost is a few minutes (execution record).

## 5. Exposure before freezing

- **E2 tables.** All read.
- **GT-P005 pre-freeze smoke.** It printed flux, partner index and one-way counts for FREE N=4 W4 PATHF weak_suppress, strong_suppress and prohibit, EXCL and NULL. These are now E3A cells.
- **Proof fixtures.** Synthetic factor tables and HELD N=4 only. The reachable-set sizes 54 and 341 for HPF are structural; the 341 was already published in E2.
- **Nothing else.** No round cell's recovery, gate, split or scan value was computed before freezing.
