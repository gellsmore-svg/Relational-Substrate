# GT-P010 audit: live baseline, hub pin and E5B pre-freeze decisions

*Deliverable 1 of GT-P010, 15 October 2026. Written before any E5B scientific quantity was evaluated. No N=5 or N=6 E5B observable has been computed.*

## 1. Live baseline (verified)

| Item | Expected (prompt) | Observed |
| --- | --- | --- |
| GT branch `research/gravity-time-admissibility` | `79fa6b0119449bd56359acf4436015df27855f43` | same; clean worktree; CI green at this head |
| PR #6 | open, draft | open, draft, head `79fa6b0` |
| E5A frozen plan / results / close | `1dc43c6` / `59eb682` / `79fa6b0` | present; plan_hash `31202d70…97a8`; payload `6e978571d83e…` |
| E5B plan or result | none | none (`plans/round-e5b-plan.json` absent) |
| Hub `main` | `38c2501bbab22ca1eb2288ea76a962ac0170d5e6` | same |

The GT branch has no `research-synthesis/` directory and none is added. The hub was read with `git show 38c2501…:research-synthesis/<path>` only; nothing was merged, cherry-picked or written.

## 2. Hub commit consulted and its pins

**Consulted hub commit (frozen into the E5B plan): `38c2501bbab22ca1eb2288ea76a962ac0170d5e6`.** A later movement of `main` does not re-motivate E5B.

Pins recorded by the hub manifest at that commit:

| Source | Hub status | Pinned commit | Unreviewed generations |
| --- | --- | --- | --- |
| CL | included | `e650d71` | 008N |
| GT | included | `79fa6b0` | GT-P009 |
| CL-8G | lineage only | `22e252e` | — |
| SC | catalogued only | `aa06213` | — |
| OTR | catalogued only | `05b15b0` | — |
| EXT-SYNTH-20261015 | external, stored | — | — |
| HIST | pending intake | — | — |

The hub holds nine cross-programme connections and questions XQ::01 to XQ::07 (XQ::05 pending a source). Hub ingestion does not strengthen GT-P009 or CL 008N: both remain closed but unreviewed.

Files read at the hub commit: `README.md`, `docs/branch-integration.md`, `docs/runbook.md`, `docs/cadence.md`, `docs/epistemic-policy.md`, `sources/pin-spec.json`, `sources/manifest.json`, `generated/index.md`, `generated/questions.md`, `generated/round-trips.md`, and themes `matched-control-design`, `occupancy-vs-process`, `passage-and-persistence`, `selection-vs-persistence`, `history-as-predictive-variable`.

## 3. Shared questions consulted

| Question | How it shapes E5B (as a discriminating question, not a conclusion) |
| --- | --- |
| **XQ::01** (kinetic comparators) | Motivates NK, a layer-traffic-matched comparator, and the anchor-local event count. Its proposed CL-style matched-source test is examined in §4 and not transplanted. |
| **XQ::04** (identity through replacement) | Motivates entry-set tracking, distinct departures, complete renewal and the flicker diagnostic, all as read-only trajectory observables. |
| **XQ::07** (common operator or common question) | E5B's quantities are generator/stopping-set functionals (hitting probabilities, killed sums). The handoff will state whether any maps to a CL functional in the same sense. |
| XQ::03 (background) | CT, global jump count and anchor-local count are three functionals of one full process, not a projection with hidden events. |

Existing hub links X::0001, X::0002 and X::0009 are background only. E5B is not an independent confirmation of them.

## 4. CL controlled-passage assumptions (pinned CL `e650d71`, `constraint-lab/formal/history-controlled-passage.md`)

- **CL-T85.** Matched sources: the stationary-conditional kernel Kpi on the projected state (P, h1), with sources drawn from the stationary law conditioned on a graph class, gives equal first-step labelled material flows and equal initial UP/DOWN masses. Longer paths need not agree.
- **CL-T88.** Kac: for a finite positive recurrent chain, E[τ_D⁺] = 1/π(D) from π conditioned on D. Same-set recurrence is fixed by occupancy and is not a persistence test.
- **CL-T89.** A first-order kernel on exactly (P, h1) matching the full stationary adjacent joint is uniquely Kpi; a passage difference therefore excludes that matched class only.

**Eight-dimension scope comparison with the planned NK comparator:**

| Dimension | CL 008N Kpi | GT E5B NK |
| --- | --- | --- |
| State | ordinary X plus history h1, h2 at pair epochs | FREE graph x ∈ {0,1}^M, no history |
| Transition law | 8M triad-blind controllers on Z = (P, h1, h2) | GT order-2 single-toggle W4 templates |
| Support | recurrent class of the augmented chain | full hypercube, all rates positive |
| Clock | pair-event epochs (discrete) | CT, plus jump and anchor-local counts |
| Projection | (P, h1): drops the older history coordinate | edge count k |
| Intervention | none (comparison of kernels) | none (comparison of generators) |
| Horizon | first return, MFPT, committors | entrance episodes to first exit |
| Conditioning | stationary source conditioned on a graph class | Palm entrance into the predicate set |

**Relationship.** NK's projected layer process has up-rate J[k,k+1]/p_k and down-rate J[k−1,k]/p_k. Those are the target's stationary-conditional layer rates, so NK is a Kpi analogue *on the projection K*, lifted uniformly within each layer. It is not CL's construction: GT has no hidden history coordinate, the clock is continuous, the projection is a count, and the lift (uniform within a layer) is a modelling choice with no CL counterpart. **E5B does not implement a CL matched-source control.** This is recorded as a cross-programme analogy to be stated in the handoff, with the differences above. GT and CL share the 8G kernel and validator lineage, so no independent validation is claimed.

## 5. E5A qualification (append-only): the intact-motif count is 2/30, not 1/30

GT-P009 prose (`gt-e5a-report.md` §1, `gt-e5a-reflection.md`, finding `GT-F74`) says intact motifs outlive ND in continuous time in "1/30" non-NULL rows, then names two rows. From the unrounded `round-e5a-tables.json` (target `lifetime_ct` / ND `lifetime_ct`, 5 non-NULL families × 3 intact predicates × 2 sizes = 30 rows):

| Classification (E5A tie rule, relative 10⁻⁹) | Rows |
| --- | --- |
| Target longer than ND | **2/30**: PATHH I_STAR, N=5 (×1.0043583) and N=6 (×1.0932716) |
| Tie | **6/30**: PATHF I_TRI, I_STAR, I_2PATH at N=5 and N=6 (ratios 1 ± 7×10⁻¹⁵; exact equality by GT-F75) |
| Target shorter than ND | 22/30 |

The count of distinct family–predicate pairs is 1 (PATHH star), which is how the report arrived at "once". The row count is 2/30. The effect is small at N=5 (0.4%). GT-P009's files are not edited; the correction is recorded here and as an appended GT finding at E5B close.

## 6. What is already exposed

E5A exposed, for the same 12 laws and the three flexible predicates: target, N0 and ND values of π(A), J_A, L_CT, L_JT, Ω, ρ, prevalence in both clocks, JT density profiles, and the lagged-hub series. E5B's new quantities are:
- the anchor-local event count;
- entry-set tracking (distinct departures, complete renewal, feasibility classes);
- the immediate-reversal (flicker) diagnostic;
- the NK comparator and its layer diagnostics;
- within-layer rate dispersion.

E5B is a newly frozen follow-up with new readouts on exposed laws. It is not a blind confirmation of E5A.

## 7. Permitted pre-freeze work

- Definitions, algebra and feasibility proofs (`docs/e5b-definitions-controls-and-feasibility.md`).
- Observable-only code and tests on synthetic finite chains and N ≤ 4 fixtures, including a PCOMP-like uniform-law heterogeneous-kinetics synthetic chain.
- Cost estimates on synthetic fixtures and on published NULL only.
- Reproduction of published E5A stationary laws as a replication check, not as new evidence.
- No N=5 or N=6 target value of any new E5B quantity is computed before the freeze is pushed.

## 8. Decisions that must precede the freeze

1. Exact entry-set definitions, the complete-renewal event and the feasibility rule for each predicate.
2. The flicker diagnostic: an exact immediate-reversal flux, defined below.
3. The local-event mask per predicate.
4. NK construction, its rare-layer policy and its numerical identities.
5. The augmented-observer solve: method, quotient, tolerance, caps and the UNRESOLVED rule.
6. Frozen checks, tolerances (from synthetic convergence), budget and watchdogs.
7. The optional durable-renewal filter: decide before the freeze whether to include it, or record it as not attempted.
