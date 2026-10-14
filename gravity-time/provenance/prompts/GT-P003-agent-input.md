
# GT-P003 — E1 Observable Scaling and Pre-Freeze Research Review

**Programme:** Gravity, Temporality and Emergent Spatiality (GT)  
**Repository:** `gellsmore-svg/Relational-Substrate`  
**Working branch:** `research/gravity-time-admissibility`  
**Existing draft PR:** #6  
**Research method:** Open-Thetical Research (OTR 1.0), `research-methods/open-thetical-research.md`  
**Agent:** Claude Opus 5.5  
**Kind of work:** Bounded engineering, calibration, conceptual audit, and a *reviewable draft* of the next scientific experiment  
**Hard stopping boundary:** **Do not freeze or execute E1. Do not begin G2 or a substitute scientific round.**

## 1. Immediate instruction

**Proceed with scaling and validating the E1 observables, but stop before freezing the E1 scientific plan.**

The immediate purpose is to ensure that a scientifically informative seven-entity experiment can be designed *without confounding changes in system size with changes in effective constraint strength*, and without allowing a desired basin outcome to determine the rules or criteria.

Complete the necessary engineering, analyse the design alternatives, and present a concise plain-English proposal for review. Commit and push that work. **Do not execute the proposed E1 scientific cells; do not freeze/push an E1 scientific plan; do not treat this prompt as authorisation to do so.**

The broader research remains **gravity-motivated, coherence-guided, recursively adaptive discovery**, rather than an exercise in confirming a preferred mechanism. The E0 discoveries must remain open to qualification and surprise.

## 2. Context: what has been established

Read the repository first and check this account against the live records; these are orientation notes, not substitute evidence.

- GT-G0/G1 studied basin-like occupancy and relative event activity in existing relational grammars, distinguishing formation, retention, hard capture and clock convention.
- GT-E0A and E0B were successfully completed under OTR 1.0: 48 and 36 exact cells respectively. E0B was selected after observing E0A, not prewritten as a confirmatory continuation.
- The E0 audit established that the single-witness, label-covariant rule family is reversible with a relational Gibbs stationary law. Non-gradient, two-witness rules can support stationary probability currents and asymmetric event order.
- E0 found an asymmetric *handover* cycle, behaviour visible relative to a source or emergent hub, kinetic effects not determined by a stationary potential, and local activity without an attractive basin.
- A basin-with-arrow coexisted only narrowly in CSPH: a density-controlled attachment advantage of approximately **+0.047** at N=5 and **+0.009** at N=6. This is selectivity among present relations, **not** evidence that probes accumulate near the source; probe detachment remained substantial.
- There was no genuinely emergent, persistent centre at N≤6. The HELD triangle is an explicit instrument; FREE is a different experimental mode.
- E0C was deliberately stopped because the next useful scale question requires new machinery.
- The first E1 engineering step already exists: `constraint-lab/src/rs_constraint_lab/gtkernel.py`, with tests and `gravity-time/docs/e1-kernel.md`. The vectorised kernel reproduces the prior full kernel's reachable states, targets and weights for the documented E0 cells at N=4–6; preliminary N=7 NULL timing and an N=7 PATHF kernel *build-only* exposure are disclosed. This work does **not** amount to an E1 scientific experiment.

Primary materials include:

- `gravity-time/reports/gt-e0-report.md`
- `gravity-time/reports/gt-e0a-reflection.md`
- `gravity-time/reports/gt-e0-atlas.md`
- `gravity-time/docs/e0-coverage-and-selection.md`
- `gravity-time/docs/e1-kernel.md`
- `gravity-time/docs/roadmap.md`
- `gravity-time/hypotheses.md`
- `gravity-time/coherence/`
- `gravity-time/provenance/execution-GT-P002.md`
- `constraint-lab/formal/` and `constraint-lab/docs/scientific-plan-discipline.md`
- `research-methods/open-thetical-research.md`

Read these before making substantive decisions; do not rewrite historical findings.

## 3. Validate the live starting point

1. Inspect the latest remote branch head, PR #6 state, relevant commits and current CI.
2. Confirm the vectorised kernel's code, test coverage, benchmark evidence and limitations against the repository rather than trusting narrative summaries.
3. Confirm that the OTR method has a canonical home on `main` and identify how this branch references it. Do not create another divergent copy.
4. Confirm that no E1 scientific plan has been frozen and no actual E1 scientific cell has already been computed; if this assumption is false, document the exact state and preserve its provenance rather than overwriting it.
5. Keep separate which operations are **engineering validation**, which are **mathematical analysis**, which are **pilot exposures**, and which would be **scientific E1 execution**.

## 4. What “scaling the observables” means

The kernel determines possible transitions and their weights. Observables are the measurements derived from those transitions or the resulting stationary and transient processes. A faster kernel is necessary but not sufficient: the *measurement routines* must remain valid, comparable and computable as the state space increases.

Review every observable considered for E1 and assign one of four explicit statuses:

- **Already scalable and verified:** can run at N=7 without a substantial redesign.
- **Can be scaled now:** implement an array-based, sparse, symmetry-aware or analytically equivalent form and validate at N≤6.
- **Only approximate at N=7:** propose a defined estimator with declared uncertainty, convergence and validation checks; do not silently replace exact values with estimates.
- **Omitted/deferred:** explain why omission is scientifically acceptable or why it prevents a meaningful E1 experiment.

Consider at least these channels:

1. Source-relative attachment and **attachment controlled for total edge density**.
2. Probe-to-source relational distance, shell occupancy, distribution of detachment and relevant conditioning.
3. Local formation/dissolution activity and the near/far comparison, under separately declared jump and continuous-time conventions.
4. Stationary probability current, entropy production, cycle orientation and event-order asymmetry (especially the handover pattern).
5. Hub-relative or other *emergent* reference frames in FREE systems, with treatment of ties and fluctuating hubs.
6. Structural and class-conditional occupancy; distribution of network shapes, not only global means.
7. Relaxation spectra, gaps and autocorrelation where scientifically informative, with an explicit choice to implement a justified sparse estimator or defer them.
8. Symmetry, equivalence, conservation or persistence channels essential to interpreting any apparent emergent organisation.

**Keep complementary observables.** Do not limit measurement solely to the CSPH attachment margin, a handover score, or proximity to the hoped-for gravitational analogy. Unexpected and negative behaviours remain visible.

## 5. Engineering standards and tests

Reuse the existing Constraint Laboratory engine and GT implementation. Do not add a new ontological primitive, clock, particle, metric or constraint language merely to make scaling easier.

For each changed observable:

- Define mathematically what it measures, what it conditions on and whether it concerns occupancy, event activity, transition probabilities, stationarity, first-passage behaviour or temporal sequences.
- Document its computation under the two relevant clock conventions where applicable.
- Prove exact equivalence when feasible; otherwise use recorded tolerances and compare against the original N=5/N=6 implementation and committed E0 numerical results.
- Validate representative edge cases: disconnected graphs; empty and complete graphs; symmetric or tied hubs; absorbing states; unreachable states; sparse occupancy; zero denominators; null and density controls; non-gradient/gradient pairs.
- Check that the projection has not erased the pattern of interest. Class-free averaging and hub-frame measurements must not be confused.
- Record runtime, memory, numerical residual, convergence and failure modes. Plan durable/resumable execution if a scientific round later requires it.
- Preserve G0, G1, E0A and E0B data and provenance unchanged.

Engineering fixtures and reproduction of previously published N≤6 cells are authorised. **Do not calculate previously unopened N=7 E1 scientific observables during this work.** A scientific exposure for timing must be separately declared if unavoidable, but first prefer synthetic and theorem-fixed cases, as in the existing E1 kernel record.

## 6. The crucial model-size / effective-strength confound

This is a mandatory design review, **not** an instruction to normalise all rates.

The binary pair model has `N(N−1)/2` pair slots and `2^[N(N−1)/2]` possible FREE configurations. In HELD mode, the source triangle fixes three relations, giving `2^[N(N−1)/2−3]` candidate configurations before reachability restrictions.

These are consequences of the current representation, not an observation that physical reality has a binary relational substrate.

For current label-covariant templates, one rule factor `m` is multiplied **once per qualifying witness**. For a two-witness PATH component, the maximum per-pair witness count is `2(N−2)(N−3)`: **12 at N=5, 24 at N=6, 40 at N=7**. Some other motif counts also grow with N. Consequently the effective log-weight contribution is proportional to `w log(m)`; a fixed grade is not necessarily a fixed aggregate physical or relational influence at different N.

Other size-dependent confounds include:

- changing opportunities for pair formation/dissolution;
- changing density and entropic/combinatorial baselines;
- changes in the ratio of held-source entities to total entities;
- changes in shell sizes and conditional populations;
- saturation and near-absorbing regimes;
- per-event versus per-unit-continuous-time normalisation;
- finite-size symmetry effects, hub definition and network topology.

**Required analysis:**

A. **Preserve the native fixed-grade sequence.** Comparing the *same declared rules and grades* at N=5, 6 and 7 is a meaningful and necessary question. It tells us how that model behaves as it grows; do not alter this primary sequence.

B. **Quantify how the effective conditions change.** Derive or calculate the witness-count distributions and relevant scale relationships from definitions, analytical bounds and already-published small-system data. Do not use new N=7 scientific outcomes while preparing the plan.

C. **Design a distinct size-sensitivity comparison** that separates changed witness multiplicity from genuine changes in emergent organisation, to the extent identifiable. Consider prospective per-witness/log-weight normalisation or matched aggregate log-weight as a *separately labelled alternate model*, not an invisible rescaling of the original one. Assess whether such a comparison fits the established grammar/weight alphabet and compilation rules. If not, explain what change it would require and propose alternatives that remain within the existing grammar. Do not smuggle in new continuous grades just to rescue a desired outcome.

D. **Assess identifiability.** Say explicitly which effects can and cannot be disentangled at N=7. Some comparisons may not have a unique interpretation from seven entities alone.

E. **Predeclare controls rather than tune after observing E1.** Specify what would be compared under the native fixed-grade model and any separately legitimate sensitivity model. Do not use the observed sign of the N=7 basin margin to choose a new grade or an acceptable threshold.

The correct interpretation of a vanished CSPH margin might be finite-size behaviour, witness-amplification, occupancy/combinatorial effects, or an unresolved combination. **Do not pronounce a physical or ontological conclusion from one scalar crossing of the null.**

## 7. HELD and FREE remain different questions

- **HELD** has an explicitly fixed relational triangle; source-relative measurements can be computed without pretending the source emerged.
- **FREE** has no imposed centre. It may exhibit local hubs along individual histories even if the ensemble remains label-symmetric. Hub-based analysis should retain this distinction.
- Do not claim the disappearance of an imposed-source effect implies that unscaffolded organisation cannot emerge.
- Evaluate whether FREE N=7 is computationally practical with all proposed observables; distinguish mathematical possibility from realistic execution cost. The prior NULL benchmark is not automatically representative of non-gradient composite chains.
- If FREE must be deferred, explicitly state which emergence questions therefore remain unanswered and how they could be investigated later.

Do not insist on the same analyses for both modes if this would make the round infeasible, but do not treat one as evidence for the other.

## 8. Research design: an E1 *draft*, not an E1 commitment

Prepare a **reviewable scientific proposal** which compares multiple plausible E1 designs, for example:

- **Option A — Scale/robustness first:** exact N=7 HELD fixed-grade comparison across the key handover and coexistence families, with well-matched controls.
- **Option B — Scale plus explicit witness-strength sensitivity:** the same primary comparisons accompanied by a separately specified and justified scaling control, if legitimate in the current grammar.
- **Option C — Mechanism/discovery first:** a smaller but more information-rich comparison or reanalysis if the size confounds, unavailable observables or compute budget make a premature N=7 round weak.

These are options to evaluate, not outcomes selected in advance. An unforeseen superior design can be proposed.

For each option, explain in plain English:

1. **Why run it?** What uncertainty has E0 left us with?
2. **What would vary, and what would be held constant?** Include rules, grades, initial states, modes, clocks, projections and observables.
3. **What would we actually see?** Include all important distributions and failure/null channels, not simply a success metric.
4. **Which contrasting outcomes would be informative?** For example, handover persistence with vanishing attachment selectivity; stable selectivity but altered kinetics; source effects without a hub; an emergent hub with no stable source; no robust effect; or a new unanticipated pattern.
5. **What could still be artefact or underdetermined?** Include witness multiplicity, density, clock and projection controls.
6. **What is the cost?** Approximate work count, memory/CPU demands, convergence strategy and numerical tolerances; distinguish measured timings from extrapolations.
7. **What next?** Indicate how observations would inform the following OTR round without precommitting to it.

Avoid collapsing this comparison into a single numerical ranking or a binary test of gravitational resemblance. OTR favours the design that provides the most meaningful *discrimination and discovery opportunity* within the feasible budget.

The recommended plan should still be sufficiently explicit to freeze later, but **do not create, freeze or push the final E1 execution manifest** in this prompt. A clearly labelled review draft is welcome. Do not execute any proposed E1 cells.

## 9. Specific interpretation and stop-rule corrections

The current roadmap says, in effect, that if the CSPH selectivity margin crosses the null at N=7 it should be called a finite-size effect and grades should not be tuned. Preserve the anti-tuning intention, but propose a more epistemically precise interpretation:

- A null crossing is a valid observation **for that fixed-grade, finite-N model**.
- It does *not*, by itself, distinguish intrinsic size dependence from growing witness multiplicity or changing occupancy baselines.
- It must not be repaired by post-hoc grade tuning.
- Follow-up sensitivity tests must be separately designed and frozen if justified.
- Fragile effects and failed outcomes are retained as meaningful findings, not labelled failures of the wider RS ontology.

Record any suggested changes as **proposed roadmap clarifications** or a new review note. Do not retroactively edit historical plans or observations.

## 10. Record the limitations of binary state counting

A brief explanatory note is useful for clarity:

- `2^[N(N−1)/2]` arises because this specific finite model has one present/absent bit for each unordered pair.
- More expressive relation types, directed relations, triadic relations or multivalued states would have different configuration counts.
- The combinatorics place a strong practical constraint on exact exploration.
- **No physical or ontological claim about binary reality follows from this representational choice alone.**

Do not turn the E1 engineering prompt into a separate research project about fundamental discreteness; simply record the distinction accurately.

## 11. Reproducibility, performance, and preservation

- Keep the existing `gtkernel` validation as the baseline and rerun appropriate tests on any changed code.
- Check numerical comparability to committed E0A/E0B values, with appropriately declared residuals, especially for stationary currents and event-order statistics.
- Avoid large test cases in routine CI if they are too costly; keep a documented, reproducible opt-in validation for larger N≤6 cases.
- Capture real measured memory and execution costs for engineering fixtures, clearly labelling extrapolations for unexecuted scientific E1 cells.
- Respect the frozen-plan-before-science discipline of the Constraint Laboratory.
- Preserve legacy files, all G0/G1/E0 results, and the provenance chain.
- Do not edit CBO, Appendix E or the canonical RS research baseline.
- Do not merge PR #6 or change independent Constraint Laboratory research branches.
- No cherry-picks into other branches without a separately justified integration.

## 12. Deliverables

Commit and push the following on the GT research branch (choose clear filenames consistent with its layout):

1. **Scalable observable implementation**, tests and explicit omissions/deferred methods.
2. **Observable validation matrix**: old and new definitions, available N, exact/approximate status, reproduction gaps, edge cases and numerical limitations.
3. **Scale/confound audit** including witness-count derivations, density/entropy/source-ratio effects and the limits of inference.
4. **HELD versus FREE feasibility note** including time/memory assumptions and which questions each mode can answer.
5. **E1 design alternatives** with a recommended option, reproducible budget estimate and a plain-English rationale.
6. **E1 pre-freeze review note**, written for a human reader with no assumed familiarity with internal jargon.
7. **Engineering provenance**, changed-code commit(s), test results and final-head CI status.
8. A brief update to PR #6 describing what has been done and explicitly stating **E1 scientific plan is not frozen; E1 scientific execution has not begun**.

For the plain-English note, give a compact explanation of:

- what E0 found;
- what is still ambiguous;
- what scaling the observables accomplished;
- the role of effective rule strength as N grows;
- what experiment is now being proposed and why;
- the principal competing interpretations of likely outcomes;
- what decision is being requested from the human researcher.

## 13. Mandatory stopping point and final response

Once the engineering and pre-freeze research review are committed and pushed, **stop**.

Do not treat “the user asked for the next prompt” as authorisation to run E1. Do not silently freeze the plan when engineering finishes. Do not start E1, E0C, G2 or a new research round.

Conclude in ordinary language, answering:

1. Are the observables ready for N=7, and which remain unavailable?
2. Have you accounted for the system-size/witness-strength confound?
3. What exactly would the recommended E1 run do?
4. Why is that run more informative than the alternatives under OTR?
5. How much memory and computation is estimated, with which uncertainties?
6. What are the risks of an uninterpretable result?
7. Is the work ready for the **human researcher to review and authorise freezing E1**?

If some prerequisites remain incomplete, report that explicitly. Do not compensate with unfounded assurances or quietly weakened standards.

**Governing principle:** Improve the system's capacity to *observe and discriminate*, not its capacity to reproduce a desired gravitational result. Preserve understanding gained from nulls and surprises. Freeze the scientific experiment only after a separate human review.
