
# GT-P004 — E1 Option B: Freeze, Execute, Interpret

## Research programme

**Repository:** `gellsmore-svg/Relational-Substrate`  
**Working branch:** `research/gravity-time-admissibility`  
**Existing draft PR:** [#6](https://github.com/gellsmore-svg/Relational-Substrate/pull/6)  
**Method:** [Open-Thetical Research (OTR) 1.0](research-methods/open-thetical-research.md)  
**Expected starting head at authoring:** `31620b6f6d0ccb1d381a95803c7552d506ae96e3` (verify; never reset newer legitimate work to this SHA)  
**New prompt ID:** `GT-P004`

## 0. Decision and mandate

The human researcher has reviewed GT-P003 and **authorises Option B** from `gravity-time/docs/e1-design-alternatives.md`: **the E1 HELD N=7 fixed-grade scale round plus the predeclared W3/W16 strength bracket at N=5 and N=6**.

**You are authorised to complete the scientific plan, freeze and push it, then execute the frozen E1 round and publish its findings.** This is not another pre-freeze consultation. Do not stop after preparing a plan unless a genuine safety, correctness, cost, or repository-state blocker prevents responsible execution.

**Not authorised:** the Option D / FREE N=7 tranche, any post-result grade optimisation, a new ontology primitive, a new scientific round after E1, editing G0/G1/E0A/E0B results, editing the CBO manuscripts, merging the PR, or changing other programmes' branches.

If the repository has advanced, inspect and reconcile its current state before proceeding. Preserve all legitimate existing work. Keep PR #6 a draft.

## 1. Why we are doing this

The E0 Open-Thetical rounds discovered a distinction between **relational occupancy**, **kinetic activity**, and **the preferred orientation of event sequences**. A source-relative *handover* circulation emerged under non-gradient constraints. One composite, **CSPH**, combined that circulation with weak source-selective attachment, but the apparent basin was fragile.

GT-P003 exposed consequential qualifications:

- At HELD N=5 → N=6, CSPH's **continuous-time raw attachment margin** decreases approximately **+0.046 → +0.009**, while its **jump-chain raw margin** remains approximately **+0.073 → +0.065**.
- Under **null-density standardisation**, the N=6 margin is **negative** in both clocks (continuous approximately −0.073; jump approximately −0.034). This is a conditional, counterfactual reweighting that can include configurations extremely rare under CSPH; it complements rather than supersedes ordinary occupancy.
- Per-rule factors are multiplied per qualifying witness. A fixed nominal grade does not imply constant total influence at larger N; path-witness maxima are 12, 24 and 40 for N=5, 6 and 7, while **engaged** witness loads in the actual N≤6 dynamics increase much less, or even fall for some components.
- HELD holds a three-entity triangle fixed. Increasing N changes the relative size of this imposed scaffold and the combinatorics of possible attachments. Neither is evidence of an emergent source.

The task is **not** to prove whether CSPH makes gravity. It is to understand how these behaviours reorganise with system scale, and whether witness amplification is a plausible partial explanation—while continuing to notice unexpected phenomena.

## 2. Source-of-truth preparation and audit

Before changing code or planning any scientific cells:

1. Verify the live remote branch, current head, PR state, worktree cleanliness, CI status and OTR method document.
2. Read: `gravity-time/reports/gt-e0-report.md`, `gravity-time/reports/gt-e0a-reflection.md`, `gravity-time/reports/gt-e1-prefreeze-review.md`, `gravity-time/docs/e1-design-alternatives.md`, `gravity-time/docs/e1-scale-confound-audit.md`, `gravity-time/docs/e1-held-free-feasibility.md`, `gravity-time/docs/e1-observables.md`, `gravity-time/docs/e1-kernel.md`, `gravity-time/provenance/execution-GT-P003.md`, plus the relevant plans, journey, ledger, and analysis code.
3. Check the verified GT-P003 observable implementation and its validation against all 84 prior E0 cells. Preserve GT-F34 and GT-F35 as qualifications of prior results; do not silently rewrite old outputs.
4. Confirm actual family, grade and alphabet identifiers from code rather than translating names by intuition.
5. Record all already-exposed fixtures, theorem-fixed quantities, partial kernel builds, published N≤6 results and post-hoc channels. Do not represent these as independently unopened observations.
6. Check the per-cell and full-round computational budget against the actual host before freezing. The previously reported figures are *estimates*, not guaranteed performance.

Use existing `gtkernel`, `gtobs`, `gtscale`, `gtobs_validate`, frozen-plan machinery, exact/sparse checks, and the programme's durable execution conventions. Do not invent parallel infrastructure or change the constraint grammar for this round.

## 3. Authorised Option B cells — exact scope

### Tranche I: native N=7 fixed-grade HELD comparison (8 cells)

Set **N=7**, mode **HELD**, the same permanently linked source triangle and start state as E0, the existing **W4** alphabet, and the exact grades below:

| Family | Grade |
| --- | --- |
| `CSPH` | `strong_favour+weak_favour` |
| `CSPF` | `strong_favour+weak_suppress` |
| `CWPH` | `weak_favour+weak_favour` |
| `CWPF` | `weak_favour+weak_suppress` |
| `PATHF` | `weak_suppress` |
| `PATHH` | `weak_favour` |
| `NULL` | `none` |
| `CLOSEW` | `weak_favour` |

The `NULL` N=7 identities were previously evaluated as theorem-fixed fixtures; declare this exposure. Do not count them as fully new observations. `CLOSEW` is the reversible gradient control. The six non-gradient families are substantive open cells.

### Tranche II: within-grammar strength-sensitivity bracket (24 cells)

For the **six non-NULL, non-CLOSEW families** listed above, use precisely their specified component combinations and grades, with each of the existing **W3** and **W16** sensitivity alphabets at **N=5 and N=6**, mode **HELD**:

6 families × 2 sizes × 2 alphabets = **24 cells**.

This varies the log-strength scale at fixed N, not the grammar, the scaffold, the rule ordering or the observable definitions. Use the actual W3/W16 definitions already supported by the repository. W3 and W16 may require tolerance-based rather than bit-exact float/rational comparison; declare tolerances in advance.

**Total authorised scientific/comparison cells: 32** (8 + 24), with identity fixtures and prior-published baselines distinctly labelled.

Do not silently add further grade sweeps, strength interpolation, compensatory parameter choices, or N=7 FREE cells. Any necessary revision to the scientific cell set must be justified, recorded and approved **before** opening the affected round; an issue discovered after freeze is handled by explicit amendment and new provenance, never quiet substitution.

## 4. What to observe — discovery first, not one-margin optimisation

Apply the validated scalable observable suite consistently across all available cells. Report **both the jump-chain and continuous-time conventions** wherever they produce distinguishable quantities.

At minimum preserve:

- Stationary occupancy, graph/relational density, reachable and recurrent-class diagnostics, detached-probe counts, and topology/class distributions.
- Source-relative attachment and relational-distance distributions, including shells with small probability mass and explicit rare-state warnings.
- **All attachment representations together**: raw margin versus size-specific NULL; null-density-standardised margin; ceiling-normalised margin; full attachment-by-free-edge-count profile. No single representation should be selected after observing E1.
- Local activity and shell profiles by clock, and their density/occupancy dependence.
- Probability currents, entropy production, non-gradient cycle or square affinities, event-order asymmetry, and especially the *handover* sequence **without** treating handover as the only phenomenon worth retaining.
- Hub-frame and source-frame comparisons, including ties and changing null hub rates.
- Autocorrelation and persistence indicators supported by `gtobs`.
- Per-component and event-engaged witness loads, to distinguish the nominal maximum witness count from the actual dynamical exposure.
- Equal-ratio kinetic comparisons and changes in the associated stationary distributions.
- Null, weak, counterintuitive, ambiguous, unexpectedly strong, saturated and numerically fragile effects.

The full relaxation spectrum may remain omitted at N=7 for the documented dense-algebra reason; mark it explicitly as unavailable, not zero. Distinguish a null observation from an unresolvable quantity.

Present measurements as a **multidimensional behaviour profile**, not a weighted score that rewards gravitational resemblance. Note unusual patterns beyond the original candidate questions.

## 5. Size and strength comparisons: methodological boundaries

Predefine the following comparisons in the frozen plan:

1. **Native size sequence:** published N=5 W4 and N=6 W4 against E1 N=7 W4, with consistent observable definitions and explicit numerical qualifications from GT-P003.
2. **Same-size strength response:** W4 → W3 → W16 at N=5 and N=6, for each of the six specified families. Do not presume monotonicity.
3. **Calibration on known size change:** contrast N=5 W16 with published N=6 W4, in particular for the single-component PATH families where interpretation is cleanest. Matching the path-witness *maximum* does not mean matching actual engaged loads, state-space combinatorics or transition laws. If the calibration does not work, report the strength bracket as a poor explanatory proxy rather than forcing an interpretation.
4. **Component-specific engagement:** distinguish closure and path contributions in CSPH/CSPF/CWPH/CWPF. Uniformly scaling the weights cannot independently hold their relative influences fixed as N changes.
5. **Changes in geometric reference:** as N grows, the HELD source triangle occupies a shrinking share of the entities, and the size-specific null attachment ceiling changes. Neither is separately identified by the N sequence alone.
6. **Clock and density sensitivity:** compare raw and standardised observations without elevating an artefact-prone rare-density conditional to a physical conclusion.

A margin crossing below null is an observation **for that family, N, clock and definition**. It does not, by itself, establish an intrinsic finite-size effect, witness-strength amplification, or a failure of the Relational Substrate ontology. Do not tune rule grades after the fact to preserve an attractive result.

There is no expectation that CSPH must retain a positive basin or that a handover must persist. If the system transitions into a new regime, characterise it without treating the deviation as failure.

## 6. Freeze protocol and numerical integrity

Finish necessary engineering, synthetic fixtures and dry-run plumbing **before** the scientific freeze. Use established GT plan conventions.

Create `gravity-time/plans/round-e1-plan.json` with:

- complete authorised 32-cell manifest; source/start policy, modes, alphabets, grades, grammar/kernel/observer versions;
- initial states, symmetries, named clock conventions, observations, estimands, comparison rules and baseline sources;
- frozen thresholds, tolerances, solver diagnostics, precision policies, symmetry checks, ref/array equivalence checks and handling of rare conditional probabilities;
- replay/durability, batching, memory and wall budgets, timeout strategy, partial/unresolved-cell handling, recovery policy and stop conditions;
- pre-freeze exposure declaration and exact links/hashes to the earlier documents/results;
- controls and structural expectations, separated from open scientific questions;
- deliberate omissions, particularly FREE N=7 and dense spectrum.

Keep structural identities distinct from scientific predictions. The proposed GT-P003 Z1–Z5 controls are a starting reference, not an invitation to claim every scientific cell must produce the hoped-for behaviour. In particular, a solver nonconvergence is **unresolved**, not a scientific counterexample; do not assert that every cell resolves merely because a draft expectation says so.

Commit **and push** the frozen plan before any E1 scientific cell is run. Verify the committed plan hash and remote ancestry in execution. Log the question/plan journey event before results, then publish result commit hashes afterward. If a solver-only correction is necessary after freeze, preserve plan, document precise effect on computation, validate independently, and mark affected results; if an estimand or cell set must change, stop and follow explicit amendment governance.

Guard against false precision: use dual starting distributions, stationary residual and symmetry checks, near-zero mass diagnostics, robust denominators and independent reference checks where computationally feasible. Numerically wrong values in old E0 results were identified in GT-P003: do not repeat the rare-state clipping or early-convergence problems.

## 7. Execution budgets and workflow

The GT-P003 design estimates roughly **15–50 minutes** for the eight HELD N=7 cells plus up to **30 minutes** for the 24 smaller strength-bracket cells. These are extrapolations from fixtures. The proposed full Option B round cap is **4 hours wall time**, with resumable items and sensible per-cell watchdogs. A historic 120-second watchdog should **not** be blindly inherited where N=7 scientific cells are expected to exceed it.

Run only as many workers as fit the available memory and solver characteristics; execution should be resumable without changing its scientific content. Record actual time and peak memory by cell.

Do not run the FREE N=7 tranche: current estimates are **30–80 minutes per scientific FREE cell** with roughly **3.2 GB peak per cell**. Preserve that opportunity as a separate future decision informed by E1 results. If the 4-hour cap is reached or a cell remains unresolved, publish complete and incomplete item records and stop rather than silently weakening tolerances or exceeding the budget.

Do not initiate an E2/G2/G3 or other new scientific round. One completed, audited E1 round is the mandate.

## 8. Recursive Open-Thetical reflection after E1

After completing or responsibly closing E1, perform a genuinely exploratory coherence reflection:

- What was directly observed? What was unexpected, especially outside the headline CSPH question?
- How did occupancy, transition kinetics, stationary circulation, recurrent activity and spatial reference relate at the larger scale? Which distinctions sharpened or blurred?
- Which behaviours were robust across clocks, definitions, rule-strength alphabets and size? Which were fragile or only apparent under a selected projection?
- Did source-selective attachment and handover remain coupled, separate, or take on another relationship? Avoid implying they are physical gravity or time dilation.
- How much of the observed N-dependence can the calibrated strength bracket plausibly illuminate, and what remains non-identifiable?
- Does the FREE-centre question become more or less informative given E1, or does another newly observed mechanism suggest a better direction?
- What new incomplete possibilities should be added to the hypothesis/open-question register?

Retain *all* relevant findings and ambiguities. Do not collapse their support into a scalar. Distinguish model observations [O], mathematical mechanisms [M], RS interpretation [RS], empirical physical comparison [P], and theological premise [T]. No physical corroboration is established by matching a toy effect to a verbal analogy.

Decide and **recommend, but do not execute**, the next investigation using the information-value logic of OTR. Candidates may include the FREE N=7 emergent-hub tranche, a narrower kinetic/handover mechanism investigation, component-specific scaling, source-size control, or something genuinely suggested by the observations. Do not select a follow-up merely because it is already on a roadmap.

## 9. Deliverables and GitHub close-out

Publish to the existing research branch:

1. The immutable frozen E1 plan and its chronology/hash/provenance records.
2. Reusable, tested E1 execution code if not already present, without duplicating prior engines.
3. Complete result tables for every authorised cell, including unresolved cases and numerical diagnostics.
4. A plain-language **E1 results report** explaining what changes with N and strength, and what still cannot be inferred.
5. A comparison/behaviour atlas covering all families and all observations, retaining negative and unusual outcomes. Include replayable exemplars if trajectories add independent insight; exact kernels remain the numerical authority.
6. The scale-versus-strength interpretation and its calibration limitations, with counterfactual density standardisation clearly labelled.
7. An Open-Thetical coherence reflection and justified next-round recommendation.
8. Updates to GT's hypothesis register, linked findings, relations, generated coherence map, and qualified ontology proposals where warranted.
9. A complete execution/provenance ledger and updated draft PR #6 summary. Preserve G0, G1, E0A, E0B and GT-P003 source records unchanged; qualify rather than rewrite.
10. Final unit tests, full relevant CI and checks on the actual final branch head. State any unverified checks explicitly.

A readable final agent summary must explain, without assuming the human researcher already knows the codebase:

- **What did you run, and why?**
- **What did you discover, including surprises and negative results?**
- **What is a model result versus a physical implication?**
- **What remained confounded or uncertain?**
- **What should we investigate next, and why is that the most informative option?**
- **Which commit, report and PR should be reviewed?**

## 10. Governing instruction

**We are pursuing coherent understanding of gravity-motivated relational dynamics, not optimising a model to resemble gravity.** E1 is a deliberately bounded, directed exploration chosen because it can clarify *multiple* live possibilities. The scientific rules, cells, comparison methods and numerical criteria must be frozen before observing new scientific results. The observations must be allowed to expand, narrow, complicate, or overturn our current thinking.

**Proceed to freeze, execute, analyse and publish Option B; stop before any additional scientific round or merger.**
