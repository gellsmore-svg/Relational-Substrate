
# GT-P009 — FREE Relational Persistence, Turnover and Endogenous Reference Feasibility

**Agent:** Claude Opus 5.5 operating in the `gellsmore-svg/Relational-Substrate` repository  
**Programme:** Gravity, Temporality and Emergent Spatiality (GT)  
**Method:** Open-Thetical Research (OTR 1.0): coherence-guided, recursively adaptive directed exploration  
**Working branch:** `research/gravity-time-admissibility`  
**Pull request:** draft PR #6, base `research/constraint-lab-v0.8g-formal-integration`  
**Expected baseline for verification, not assumption:** `a73cd0260f38885121a89a607efa73e98732e59f` (GT-P008)  
**Authorisation:** Definitions and engineering, **one frozen-and-pushed E5A scientific round**, scientific reflection and coherence updates. **No E5B execution without a later human instruction.**

---

## 0. Mission and the two complementary lenses

The programme follows two interacting paths of inquiry:

- **Lens A — foundational / ontological depth:** identify and challenge the possible prerequisites between constrained stochastic relational actualisation and higher-level phenomena: persistence, reference, identity, relative separation, directional change, and ultimately phenomena that might bear on gravity or temporality. This is a partial, revisable dependency map, **not** a presupposed sequence or an assertion of a real physical substrate.
- **Lens B — mathematical possibility:** determine what the existing, explicitly specified relational stochastic grammar can actually generate without inserting the desired higher-level behaviour into the primitives.

We need not chase an attractive basin, a gravitational analogy, or acceleration during each round. We should investigate what is most informative at the foundational level. Nevertheless, **never relabel a long-lived graph motif as a body, its edge turnover as movement, or its lifetime as physical time.**

**Central E5 question:**

> Without any held reference, do the existing label-covariant relational constraints sustain recognisable configurations longer than appropriate null dynamics would, and can an organisation persist through turnover of some of its constituent relations?

We want to distinguish several possible outcomes, including:

1. Ordinary intact motifs last longer merely because their edges are slow or because the graph has a particular density.
2. Motifs display genuine dynamical longevity relative to comparators with the same stationary density and overall activity.
3. Some patterns persist while their participating relationships change; this is **not yet full identity of a moving object**, but it is stronger than preservation of a fixed set of edges.
4. Instantaneous hubs have no lagged persistence beyond selection bias.
5. Closure-based, path-based and equal-ratio rules produce different kinds of longevity or apparent persistence, perhaps with opposite conclusions across clocks.
6. No family displays convincing persistence beyond controls at N=5 or 6. **A null result is an important finding.**
7. An unanticipated mechanism or a failure of these definitions warrants revision *after*, not during, the frozen round.

**Do not try to establish that gravity exists in this system.** This round addresses a plausible but not proven foundational prerequisite.

---

## 1. Establish the actual baseline and read its boundaries

Before making changes:

1. Confirm remote branch, current commit, clean working tree, PR status/base/head, relevant GitHub Actions status, and the exact OTR text on the GT branch versus `main`. If anything differs from the baseline above, inspect and document it before proceeding; do not overwrite concurrent work.
2. Read, at minimum:
  - `research-methods/open-thetical-research.md`;
  - `gravity-time/charter.md`, `gravity-time/README.md`, `gravity-time/docs/roadmap.md`;
  - `gravity-time/reports/gt-p008-consolidation-report.md`;
  - `gravity-time/docs/reference-architecture-review.md`;
  - `gravity-time/docs/gt-p008-next-round-options.md`;
  - `gravity-time/docs/e4-sorting-mechanism-derivation.md`;
  - `gravity-time/docs/foundational-bridge-map.md`;
  - `gravity-time/docs/gt-p008-coverage-and-integrity-audit.md`;
  - `gravity-time/provenance/execution-GT-P008.md`;
  - the E0–E4 results, code and relevant experimental plans when needed to avoid repeat work;
  - the active hypothesis register, `gravity-time/coherence/` and `gravity-time/plans/journey.jsonl`;
  - read-only: `constraint-lab/docs/scientific-plan-discipline.md`, its 8G compilation gate and `constraint-lab/formal/open-problems.md`, particularly CL-Q03/CL-Q05.
3. Verify these prior boundaries rather than assuming them:
  - GT-P008 is a consolidation, not an E5 data source. It added no new E5 scientific cell.
  - Its witness-floor odds factorisation and first-order sorting index are mathematical results **within the finite grammar**.
  - Its 16/16 agreement with E4 within-scaffold orderings is **post hoc**.
  - Previous FREE stationary laws may already exist for the selected families and sizes; **reusing their published laws and rates is not independent replication**. New predeclared lifetime and lag channels can nonetheless be meaningful analyses. Identify exactly which kernels/laws are pre-exposed.
  - GT-P008 identified held, instantaneously selected, metastable and identity-tracked reference regimes as distinct. No emergent persistent reference has been established.
  - The E4 positive raw gathering was predominantly density-compositional; retaining this caution is compulsory.
4. Record the starting SHA, relevant hashes, exposed cells/channels, interpreter/library versions, known failures/limits, and current testing baseline in `gravity-time/docs/e5-coverage-and-definition-audit.md` **before doing E5 computations**.

The source programme has one human researcher working with coding agents; do not invent a human research team.

---

## 2. Scientific definitions: agree them operationally *inside the pre-freeze record*

**This section authorises the definitions below as the E5A starting specification.** Your job is to audit their mathematical consistency and refine implementation details *before* any E5 scientific observation is computed. Do not send them back for an unnecessary extra approval if they are internally coherent. If a fundamental ambiguity cannot be resolved without changing the scientific question, **stop before freezing** and give the human a clearly delineated decision note. Never silently redefine a metric after seeing E5 results.

### 2.1 Dynamics and scope

Use the unchanged GT order-2 single-pair-toggle grammar, with all relations FREE, no scaffold or externally prohibited edge, N = 5 and 6. The actual rules are label-covariant and positive-rate in the six selected families; thus the finite FREE chain is irreducible and has a unique exchangeable stationary distribution. Preserve the observed distinction between:

- **continuous time (CT):** generator rates `W(x,e)` and stationary law `π`;
- **per-event / jump time (JT):** `P(x,y)=W(x,y)/q(x)` where `q(x)=Σ_e W(x,e)`, and stationary law `ν(x)=π(x)q(x)/E_π[q]`.

The model clocks are conventions, not established physical time. No source-labelled rules, compensating factors, additional state variables, history H>0, meta L>0, new grammar primitives, or externally imposed reference.

### 2.2 Two fundamentally different notions of motif persistence

**A. Fixed-instance / intact motif.** On one pre-specified embedded set of vertices, require the named relations to be present; other relations are unconstrained (*non-induced motif*). These predicates test survival of a specific intact pattern, **not** identity through constituent turnover:

- `I_TRI(a,b,c)`: `ab`, `bc`, `ac` present, with a,b,c distinct.
- `I_STAR(c;a,b,d)`: the three spokes `ca`, `cb`, `cd` present, four distinct vertices. Extra leaf–leaf edges allowed.
- `I_2PATH(a,b,c)`: `ab` and `bc` present, distinct vertices; the closing `ac` is allowed.

Because a required edge dissolving destroys such a predicate, the number of required-edge turnovers that preserve it is identically zero. **Prove and report this structural limitation; do not claim an intact motif persisted through replacement of required edges.**

**B. Flexible / anchored organisation.** Use a fixed observational anchor as a *tracking index*, not as a dynamical privilege; predicates remain covariant under simultaneous relabelling of the state and anchor:

- `F_TRI(e={a,b})`: the anchor edge `ab` is present and at least one other vertex `c` completes a triangle with it (`ac` and `bc` present). Different triangle-completing vertices may replace one another while the predicate remains true. The anchor edge itself cannot turn over during an episode.
- `F_STAR(c)`: centre `c` has degree at least 3. The set of its neighbours may change while the predicate remains true.
- `F_2PATH(c)`: centre `c` has degree at least 2. The identities of its neighbours may change while the predicate remains true.

These are deliberately broad, non-induced predicates. `F_STAR` implies `F_2PATH`; they are **not independent competing species**. A persistent anchored centre is also **not yet an unlabelled mobile structure**. Keep these limitations explicit. One representative anchor/instance per permutation orbit suffices for the law, but use covariant relabelling checks to exclude anchor-label artefacts.

Use simple names throughout: *intact-motif episode*, *flexible-organisation episode*, *within-episode turnover*, *lagged frame persistence*. Do not collapse them into one ambiguous quantity called “emergence.”

### 2.3 Episode definitions and stationary entrance measure

For a predicate set `A={x:P(x)=true}`, an **episode** begins on a transition from `Aᶜ` into `A` and ends on its first transition from `A` back into `Aᶜ`.

Compute all means as **stationary entrance-episode averages**, not by sampling a random state already in `A` (which would length-bias episodes). Explicitly derive and independently check the flux identities:

- `J_A = Σ_{x∈A,y∉A} π(x) W(x,y) = Σ_{x∉A,y∈A} π(x) W(x,y)` (CT episode-boundary flux).
- CT mean episode lifetime: `L_CT(A)=π(A)/J_A`.
- JT mean length in jump transitions: `L_JT(A)=E_π[q(x) 1_A(x)]/J_A`, equivalently `ν(A)/(J_A/E_π[q])`.
- Define and report the CT and JT off-episode/recurrence counterparts carefully. For recurrence to an entry after an episode, use the exact entry flux and specify whether time is counted from one entry to the next or from exit to next entry. Avoid describing algebraically dependent summaries as independent confirmations.
- `π(A)=0` or `J_A=0`: classify as absent, closed, absorbing or unresolved as appropriate. Do **not** divide by zero, invent a lifetime or silently condition away the problem. All selected positive-rate FREE cells should be ergodic but verify that they are.

Where valuable, compute survival tails from an entrance distribution and a killed generator only if tractable within the frozen budget; a full survival curve is optional and **not** a condition for completion. Stationary-flow identities are the primary exact estimators and avoid costly 32,768-state first-passage matrix inversion.

### 2.4 Constituent turnover and relative longevity

For an intact instance, report the mean lifetime and constituent edge dwell statistics, but acknowledge that all required edges remain present throughout its episode.

For a flexible predicate, predeclare **eligible internal turnover events** that change its participating edge set while leaving the predicate true on both sides of the event:

- `F_TRI`: an edge incident on an anchor endpoint but different from anchor edge `ab`, whose toggle changes the set of vertices currently completing a triangle with `ab`, while `F_TRI` survives. Exclude irrelevant toggles.
- `F_STAR` / `F_2PATH`: an edge incident on anchored centre `c` whose toggle preserves the respective degree threshold; other events are not constituent turnovers.

Compute `Ω(A) = (stationary CT flux of eligible internal toggles x→y with x,y∈A) / J_A` = mean number of eligible internal toggles per stationary entrance episode. Report CT/JT interpretations (event count is common to both episode clocks; measures differ in the way episode time is weighted). Also report how frequently intact versus flexible episodes occur, so an extremely rare but long-lived motif is not misreported as a commonly maintained reference.

Separately define the ordinary **edge present-episode lifetime** for a uniformly specified, non-privileged slot `e` by the same flux formula, under the same family and clock. Compute:

- `ρ_CT(A) = L_CT(A)/L_CT(edge)`;
- `ρ_JT(A) = L_JT(A)/L_JT(edge)`.

The raw ratio `ρ` is **not a sufficient test of self-maintenance**: flexible predicates may be more prevalent simply by having many interchangeable witnesses. Compare `ρ`, `Ω`, motif prevalence and episode lifetime to the appropriate controls side by side. Do not tune a universal threshold for “emergence” from these values. In particular, `ρ>1` alone proves neither identity through arbitrary replacement nor gravity.

### 2.5 Density- and kinetics-aware NULL comparator: explicitly define a *process*

**Do not reweight the NULL stationary density histogram and call it a lifetime comparator.** A distribution alone does not determine event rates, first-passage times or lifetimes.

Provide **two distinct controls**:

**Control N0 — ordinary FREE NULL**, all formation/dissolution rates 1, with the *same predicate and same episode formulas*. This is the familiar unadjusted law-and-kinetics baseline. It also tests that the machinery returns known elementary flip-chain results.

**Control ND — a fully declared density-matched, exchangeable Markov process** constructed separately for each target family and N, *using a fixed algorithm declared before its density data are observed*:

1. From the target cell's **continuous-time** stationary law compute `p_k = Σ_{|x|=k} π_target(x)`, for k=0,…,M, where `M=binom(N,2)`.
2. Define a desired comparator stationary weight for each labelled graph `x` with k edges: `φ_k = p_k / binom(M,k)`. (With positive rates all p_k should be positive; check numerical support and conditioning.)
3. For a FREE single-edge toggle `x↔x+e` with |x|=k, set unscaled comparator rates:
  - birth: `b_k = min(1, φ_(k+1)/φ_k)`;
  - death (backward): `d_(k+1) = min(1, φ_k/φ_(k+1))`.
    This is an explicitly reversible Metropolis-type chain, invariant under all label permutations. It exactly matches `p_k` in CT while being uniform conditional on k.
4. Multiply **all** its rates by one scalar `c = E_(π_target)[q_target] / E_(π_ND,unscaled)[q_ND,unscaled]` so its CT stationary mean event rate matches the target's. This predeclared kinetic calibration does **not** change its CT distribution or jump-chain law.
5. Independently verify detailed balance, `π_ND(k)=p_k` within declared tolerance, the total activity calibration, normalisation, and the exact NULL fixed point (`target=NULL` gives ND=NULL). Construct the comparator from target observables without inspecting the direction of lifetime contrasts or adjusting any choices.

**Limitations to state in every result:** ND matches the *CT density marginal* and the *mean CT event rate*, **not** the full state distribution, local rates, temporal correlations, or necessarily the **jump-clock density marginal**. Consequently, the CT comparison is density/activity matched under one precisely stated comparator; the JT comparison is a legitimate kinetic diagnostic but not a fully density-matched JT experiment. Report the jump-density discrepancy between target and ND and, if necessary, a **static** event-density null reference without misrepresenting that static reference as a stochastic process. If rare k bins make the comparator numerically unstable, flag them and their masses; do not silently smooth away positive p_k or change the construction.

The ND control is deliberately only **one** reasonable dynamics at a matched density profile. An apparent effect relative to ND is therefore a fact about that comparison, not proof of a comparator-independent emergence mechanism. Preserve this underdetermination as an explicit open question.

### 2.6 Primary comparisons; no single success score

For every motif and family at each N, report both clocks for:

- stationary prevalence `π(A)` and `ν(A)`;
- episode-entry flux and intact/flexible episode lifetime;
- edge present-lifetime and `ρ`;
- flexible-pattern internal turnover `Ω`, with the anchored definition and any non-changing transitions excluded;
- ratios or differences relative to both N0 and ND, with readable signs and null/reference values;
- any conditioning/rarity/overlap warnings;
- if feasible, exact or bounded errors from numerical tolerance and conditioning.

Pre-register a **discovery matrix**, not a scalar threshold: possible patterns include sustained episode lifetime but Ω≈0; Ω>0 but only trivial ND-like lifetime; enhancement in CT but not JT; closure-only persistence; path-family persistence accompanied by nonzero handover circulation; no enhancement; and unexpected distinctions. If an estimate is zero or sign-indeterminate at the frozen precision, report exactly that.

---

## 3. Independent lagged-hub control: selection is not persistence

FREE systems have no designated centre. An instantaneous maximum-degree hub is selected by observation. Its high initial degree follows from that selection and must not be called emergent stability.

In each selected law and in controls N0 and ND:

1. At a stationary initial state `x_0`, choose a maximum-degree vertex, splitting ties uniformly by an **S_N-covariant** rule. Freeze that choice for follow-up; **do not reselect the hub at each lag**.
2. Compare the selected vertex's expected degree at lag with a uniformly chosen comparison vertex, matched within that same starting state. Report the unnormalised gap and, where the t=0 gap is nonzero, its normalised decay.
3. Freeze the lag set before execution: `Δ_events ∈ {0,1,2,4,8,16}` for the jump chain; for CT use `t = Δ/E_π[q]` for the same positive Δ, plus t=0. This scale translates average activity, **not** an assertion that the clocks are equivalent.
4. Where inexpensive, also report retention of the originally selected vertex's neighbour set; distinguish neighbour churn from its degree alone.
5. Compute exact expectations through sparse matrix-vector propagation or a validated alternative; no sampled trajectories are needed for the primary lag channel. Treat any simulations as qualitative illustrations, secondary and seeded.
6. Avoid claiming the long-run existence of a labelled centre: with positive rates and label covariance, stationary exchangeability rules that out. A slowly decaying *selected-frame memory* is not a permanently distinguished entity.

If a rigorous lag calculation is infeasible under resource limits, record why and preserve at least the shorter predeclared lags; do not replace them with more favourable lags after viewing outputs.

---

## 4. E5A matrix, exactly one authorised scientific round

**Target systems:** FREE, N=5 and N=6, with published W4 grades and unchanged rule expressions:

| Family | Components / grade | Role |
| --- | --- | --- |
| NULL | none | Unadjusted null; also tests ND fixed point |
| PATHF | `path_form weak_suppress` | Directional path family acting on formation |
| PATHH | `path_dissolve weak_favour` | Directional path family acting on dissolution |
| CSPH | `close_form strong_favour` + `path_dissolve weak_favour` | Closure + non-gradient composite |
| CLOSEW | `close_form weak_favour` | Reversible structural persistence control |
| PCOMP | `path_form weak_favour` + `path_dissolve weak_favour` | Equal-ratio kinetics control (uniform CT law, nontrivial jump statistics) |

Check the exact established grade spellings against the repository and cite the prior cell IDs. **Do not substitute similarly named but different families.**

- **12 distinct science kernels/laws** = 6 families × 2 values of N. Explicitly tag all previously published laws/channels that are reused.
- **36 fixed-instance analyses** = 12 kernels × 3 intact predicates.
- **36 flexible-organisation analyses** = 12 kernels × 3 flexible predicates.
- Therefore **72 predicate analyses**, plus N0/ND comparisons and one lagged-hub analysis per unique kernel/control, reusing the same kernel rather than pretending every predicate constitutes an independent model.
- An instance for each predicate must be defined with valid vertices at both sizes, and all equivalent labelled instances must agree by symmetry.
- Preserve initial-condition semantics: primary estimates are of the unique stationary FREE class. Transient observations or cold-start histories, if any, must be separately labelled.

No N=7, no held source, no multi-source dynamics, no new grammar, no hard prohibitions, no rate-strength sweep, no broad family search, no E5B, no spontaneous-symmetry-breaking claim, and no physical acceleration measurement.

### Time and resource discipline

This is a **small exact-study** round, not a large numerical expansion. Reuse existing sparse kernels and stationary solvers, vectorise predicate masks and flux computations, and avoid dense 32,768×32,768 matrices. Implement a bounded watchdog with per-item resume/status and an explicit overall ceiling declared in the frozen plan. The estimate in `gt-p008-next-round-options.md` is under 30 minutes and under 1 GB, not a promise. Measure/estimate feasibility with N=4 proof fixtures and old published timing evidence before freezing. If the full matrix is infeasible, reduce it transparently **before** the freeze while preserving the key comparisons. After freeze, log unresolved items rather than quietly downscaling or skipping negatives.

---

## 5. Required sequence: audit → definitions → engineering → freeze → science

### Phase 0 — confirm the scientific identity of the task

- Store this prompt, its hash, agent identity and authorisation in the GT provenance system. Compare actual prompt bytes if an external copy is available; otherwise label the repository copy as a transcription without asserting byte identity.
- Confirm that E5 has not already been executed by a concurrent agent. If the branch moved, reconcile before running.
- Update the coverage/exposure audit, including exactly which N5/N6 FREE stationary laws and observables are already published.

### Phase 1 — design and mathematical audit, before scientific observation

Write `gravity-time/docs/e5-definitions-and-null-construction.md` with formal predicates, entry/exit flux equations, turnover conventions, the ND Markov rates, activity calibration, lagged control and null expectations. Independently check:

- stationary episode mass/flux identities in both clocks;
- fixed-instance “cannot replace required edges while intact” result;
- covariance of all predicates and hub tie rules;
- reversibility and stationary law of ND, including under strongly nonuniform p_k;
- correct units under uniform rescaling of all transition rates;
- distinction between mean lifetimes under entrance sampling and residual lifetimes under occupation sampling;
- distinction between static density standardisation and a true dynamical comparator;
- the possible degeneracy of Ω for very small N, particularly for `F_TRI`;
- limits of the selected observables as claims about reference stability.

Do not write a model rule that reads the selected hub, source labels, anchor labels or a history register. All anchor choices remain **measurement-only**.

### Phase 2 — build reusable observables and validate engineering

Add focused, tested code (for example `rs_constraint_lab.gte5a`, `rs_constraint_lab.gtpersist`) using existing kernel/solver patterns. Add independent reference implementations for the new episode-flux channels and ND rates on synthetic CTMCs and/or N=4 proof fixtures **not from proposed E5A cells**. Tests should include:

- a two-state CTMC with known episode lifetimes;
- independent unit-rate bits: analytic NULL law, per-edge dwell, typical motif probability and boundary flux;
- PCOMP's known uniform continuous law; ensure you don't falsely infer identical JT law or episode lifetime;
- a reversible density-only comparator at a deliberately nonuniform synthetic p_k;
- relabelling and anchor covariance, including tie handling;
- equality of stationary entry and exit boundary flux;
- CT/JT conversion using rate-weighted stationary expectations;
- Ω=0 for required-edge turnover within an intact motif;
- an example where a flexible star/2-path retains its predicate across an incident edge toggle;
- zero-probability/zero-flux and ill-conditioned cases handled explicitly;
- deterministic reproduction with a stored precision/tolerance policy.

Proof verification using small synthetic chains or analytically fixed cases is permitted. **Do not execute or inspect new motif-lifetime, turnover, matched-density or lagged-hub results for the actual E5A N5/N6 cells before freeze.** If an unavoidable timing/smoke test uses a representative E5 cell, log that exposure and adjust pre-freeze status honestly; do not call its repeated measurement independent discovery.

Commit and push the definition note, engineering and proof fixtures before freezing. Preserve previous publications unchanged.

### Phase 3 — predeclare and freeze E5A

Create `gravity-time/plans/round-e5a-plan.json` (plus a human-readable digest if useful), using the same plan discipline as E1–E4, with:

- explicit round ID, analysis version, all 12 kernel IDs and 72 predicate IDs;
- exact rules, grades, clocks and stationary-start conventions;
- intact and flexible predicate definitions and all exclusion criteria;
- exact mathematical estimands and episode-entry distributions;
- N0 and ND process definitions including activity scaling, rare-bin handling and a record that ND is only CT-density matched;
- lag set, tie-splitting and comparison vertex definition;
- explicit primary and secondary channels, baseline descriptions, negative/zero cases, numerical checks and failure states;
- deterministic precision and tolerances, condition numbers/residual criteria, solver caps and time/memory budgets;
- the synthetic proof fixtures used and actual prior science exposed before freeze;
- source commit SHA, relevant source hashes, payload format and provenance.

Do not predeclare results as successful. Do not choose thresholds by seeing outcomes. Use positive and negative expected identities only where mathematically justified. Freeze the plan bytes and content hash in a dedicated Git commit, **push it to GitHub**, verify remote ancestry/hash, record its SHA in `plans/journey.jsonl` and provenance, and **only then execute science**. A frozen-check failure is a recorded failure until independently explained; no secret repair, cell replacement or changed tolerance. Abort or label partial if validation fails in a way that undermines the interpretation.

### Phase 4 — E5A execution

Execute only the frozen scientific matrix, with durable atomic per-kernel/per-predicate result files and restart/resume semantics. The results must carry plan hash, analysis version, code revision and all numerical diagnostics.

Separately validate:

- the target stationary distribution and both clocks;
- ND stationary CT density and mean-rate agreement;
- individual motif episode-entry and exit flux equality;
- NULL analytic fixtures and PCOMP continuous-law symmetry;
- full permutation invariance at the observable level;
- consistency of mean life = stationary episode occupancy/entry flux;
- sensitivity to extreme rarity, ill-conditioned density bins and below-tolerance differences;
- mean episode duration versus occupation-conditioned residual life (not conflated);
- the hub frame selected once and followed through predeclared lags.

Keep all completed, failed, numerically qualified and uncomputable items. **A weak, unexciting, contradictory or null finding must not trigger a grade search or a different motif definition in the frozen round.**

### Phase 5 — Open-Thetical synthesis and stop

Write a substantive plain-English report and a rigorous technical atlas, plus a reflection that:

1. Answers whether intact motifs, flexible motifs and selected hubs exhibit distinct kinds of persistence.
2. Separates genuine survival through *some* constituent edge turnover from the trivial durability of fixed required edges.
3. Compares findings across both clocks, N=5 vs N=6, and target vs N0 vs ND; states explicitly where ND is or is not a valid density/activity control.
4. Distinguishes kinetic slowing, prevalence/composition, density, hub-selection bias, closure-driven organisation, path-driven circulation and other plausible mechanisms.
5. Preserves all negative, anomalous, fragile, contradictory and numerically qualified outcomes; no best-of-six cherry-picking.
6. Checks whether any candidate is a **reasonable motif-persistence signal** within this finite model, without prematurely declaring an emergent reference or a spontaneously selected physical centre.
7. Asks whether the results illuminate GT-Q18–Q20 and the two-lens foundational bridge map; if they show only intact-edge retention, say so.
8. Compares at least three alternative *future* directions, factor by factor (not by a made-up aggregate score): e.g. identity tracking through motif changes, floor-reversal test, a stronger yet still compilable current-state rule, or no further motif work. Clearly distinguish suggested experiments from authorised ones.
9. Provides a sharply defined next-step proposal **but does not freeze or execute E5B**.

Any mathematical theorem must carry assumptions and a proof; finite-model numerical observation must be labelled observation; an RS ontological reading is a separate conjectural layer, not a physical result.

---

## 6. Deliverables and file organisation

Use repo conventions, with sensible names and stable links. At minimum produce:

1. `gravity-time/docs/e5-coverage-and-definition-audit.md` — baseline, known exposure, definition decisions, allowed tests and risks.
2. `gravity-time/docs/e5-definitions-and-null-construction.md` — motif predicates, exact episode and turnover mathematics, two clocks, N0/ND construction and limitations.
3. A tested implementation in `constraint-lab/src/rs_constraint_lab/` and new targeted tests; the full existing test suite must continue passing.
4. `gravity-time/plans/round-e5a-plan.json` — frozen and pushed **before** any scientific E5A calculation.
5. `gravity-time/reports/round-e5a-tables.json` and an atlas of **all** cells, predicates, comparators and diagnostics.
6. `gravity-time/reports/gt-e5a-report.md` — accessible plain-English account, including null outcomes and limitations.
7. `gravity-time/reports/gt-e5a-reflection.md` — OTR competing explanations, architecture implications, future alternatives.
8. `gravity-time/provenance/execution-GT-P009.md` — full commit/time/hash chronology, pre-freeze exposure and deviations.
9. Updated GT finding/question ledger, relations, readable coherence views, hypothesis register, roadmap, README, and **append-only** `gravity-time/docs/foundational-bridge-map.md` revision. Preserve all previous evidence and distinguish GT-P009 from prior post hoc analysis.
10. Optional `gravity-time/docs/gt-e5a-cross-programme-transfer.md` containing **suggestions only**, with exact GT provenance for CL-Q03/CL-Q05. Do not change Constraint Laboratory research records on other branches.
11. A concise PR #6 progress update, maintaining draft status and **do not merge**.

Use source and file paths in reports so the next reviewer can audit every claim.

---

## 7. Scientific guardrails and the 8G gate

- Remain in the **ordinary order-2, binary pair-relation, single-toggle grammar**. This is a useful modelling representation, not a commitment that the underlying ontology consists of binary links.
- No new ontological primitives, mass, force, metric, continuum, external spatial coordinates, physical clock, source-labelled transition rule, history H>0, meta L>0 or third-order O=3 grammar.
- The selected hub, motif core and instance anchor are **analysis-defined** objects. They are not dynamical agents or labels privileged by the rules. No hidden source or preselected attractive centre.
- Reuse exact methods and preserve per-event versus continuous-time distinctions and finite-N symmetry.
- A result on a particular labelled motif's duration does not establish that an unlabelled, reconfiguring organisation has an identity.
- A lifetime relative to one comparator does not establish comparator-independent metastability. In particular, merely matching stationary density is **not** a matched dynamical null unless the transition rates are specified (ND addresses this partially).
- Do not assert a spontaneous symmetry-breaking phase from N=5–6; any size trend is only a finite-size observation.
- The 8G gate applies before a suggestion that new behaviour needs extra history or meta state: determine whether current-state rules with larger templates K, cardinality J, or explicit current-state representation compile it first. Motif matching by a *read-only analyser* creates no history ontology.
- Preserve the difference between proved mathematical capabilities, observed dynamics, RS interpretations, comparison to physics and theological/worldview premises. This round supplies no physical or theological evidence.
- Keep GT branch and draft PR #6 isolated from `main`, books, canonical CBO and CL branches. Do not alter prior frozen plans, published numerical results or canonical statements without separate authorisation. Record qualifications append-only.

---

## 8. Stop and reporting contract

**You are authorised to design, freeze and run E5A once.** You are **not** authorised to run E5B, a new rule search, N=7, multi-reference physics-like simulations, or another sequence of experiments simply because E5A is positive, negative or ambiguous.

If definitions or numerical validation fail irreparably, stop and provide the best evidence available plus the unresolved issue. Do not conceal failure or replace the question with a more favourable one.

At completion, commit and push all permitted work, run local tests and check CI, update the draft PR without merging, and give the human researcher a concise completion note with:

- frozen plan SHA/hash and result commit SHA;
- precise counts of completed, failed, qualified or unresolved analyses;
- what the data **establish**, what they **suggest**, and what remains **undefined**;
- the main unexpected or null finding;
- whether the existing grammar provides any evidence for an *endogenously persistent pattern beyond matched controls*, in which sense and clock;
- a recommended next prompt direction, **not executed**.

This is Open-Thetical Research: progress consists in a better map of mechanisms and possibilities, including the discovery that an appealing prerequisite might not be present in the current grammar.

