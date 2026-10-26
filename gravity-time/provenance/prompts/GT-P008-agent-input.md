
# GT-P008 — Relational Sorting, Reference Architecture, and the Foundational Bridge

**Research programme:** Gravity, Temporality and Emergent Spatiality (GT)  
**Repository:** `gellsmore-svg/Relational-Substrate`  
**Working branch:** `research/gravity-time-admissibility`  
**Pull request:** #6, open draft; **do not merge**  
**Method:** Open-Thetical Research (OTR 1.0)  
**Intended agent:** Claude Opus 5.5, operating in the existing repository  
**Prompt ID:** GT-P008  
**Mandate:** Mathematical and architectural **consolidation**, not a new E5 experimental round

---

## 0. Executive instruction and hard boundary

You are assisting **one human researcher** in an ongoing inquiry into a proposed relational substrate. The researcher uses gravity, temporality, spatiality and other globally coherent phenomena as *directions of inquiry*, while also following foundational discoveries wherever they lead. The work has two interacting lenses:

- **Lens A — ontological depth / top-down gap analysis:** What mechanisms, definitions and structural prerequisites might lie between stochastic relational actualisation under constraints and physically meaningful phenomena such as persistent objects, displacement, acceleration, clocks, spacetime and gravity? Which steps are necessary, possible, conjectural or perhaps unnecessary?
- **Lens B — mathematical possibility / bottom-up construction:** What can an explicitly specified, label-covariant stochastic relational grammar demonstrably produce without inserting the desired phenomenon as an assumed primitive?

**These lenses must remain in dialogue, but neither is evidence that a proposed physical ontology is correct.** Progress toward foundational understanding is welcome even if it moves away from gravity. Do not pursue gravitational resemblance as an optimisation target.

### The purpose of GT-P008

The E4 rounds discovered **floor-guided sorting**: some locations within an imposed held reference receive more attachments than others, associated with how many permanently held two-path witnesses support their incident attachment slots. E4 also found that native positive *raw* gathering around some held structures was mostly a composition effect associated with relational density, not a robust density-independent tendency.

Two activities are now most informative:

1. **Workstream A — explain and challenge the sorting mechanism mathematically**, identifying exactly what follows from the grammar, what requires a stationary distribution, what depends on topology and crowding, and what remains empirical.
2. **Workstream B — evaluate the architecture of relational reference, persistence and identity**, establishing what would need to be defined or demonstrated before a held structure could be replaced by a dynamically sustained or genuinely emergent reference.

Produce a decision-ready consolidation and a carefully reasoned **proposal for the next scientific round**. This prompt **does not authorise the execution of E5A/E5B or any other new scientific experiment**.

### Boundaries

- Work on the existing GT branch and draft PR #6. Verify remote head, branch, clean worktree, PR status and CI before doing substantive work; report if the baseline has moved unexpectedly.
- Do **not** edit, merge or redefine CBO, the canonical relational ontology, the books, Appendix E, `main`, or other research programmes' branches.
- Do not introduce a new ontology axis, new physical primitive, source-labelled constraint, compensating witness correction or arbitrary attraction rule.
- Do not silently mutate E0–E4 frozen plans, results, tables, reports or their provenance. Corrections/qualifications should be new, append-only records referring to previous findings.
- Keep the ordinary O=2 pair grammar, fixed weights, clock semantics and lab generation 8G compilation discipline intact.
- Do not run new N=7 cells, FREE N=7, expanded grade sweeps, new multi-source dynamics, or any prospective experimental cell.
- **Permitted without a new science plan:** reading published results, pure algebraic derivation, analysis of already-published E4 data (clearly labelled *secondary/post hoc*), proof-verification fixtures on synthetic or logically necessary small constructions, ordinary unit/CI testing, and a bounded architecture review. If you discover that a *new scientific search or enumeration* is necessary, document and propose a frozen plan for **human review**, but do not execute it.
- Preserve null, contrary and failed mathematical findings. An honest proof boundary or counterexample is preferable to an unwarranted theorem.
- Commit and push this consolidation, update draft PR #6, and **STOP** for human review. Do not initiate the next round autonomously.

---

## 1. Read the actual current record before drawing conclusions

Begin with a short evidence and coverage audit identifying exact file paths, baseline commits, the source of every reused claim, whether it is a theorem or observation, and unresolved limitations. Read at least:

**Method, governance and programme:**

- `research-methods/open-thetical-research.md`
- `gravity-time/charter.md`
- `gravity-time/docs/roadmap.md`
- `gravity-time/coherence/current-map.md`, the canonical append-only coherence JSONL records, the latest snapshot and journey
- `gravity-time/hypotheses.md`, `hypotheses.jsonl`
- `constraint-lab/docs/scientific-plan-discipline.md`
- `constraint-lab/formal/open-problems.md` — in particular CL-Q04 and CL-Q05; read only

**Immediate evidence, GT-P006 and GT-P007:**

- `gravity-time/reports/gt-e3-report.md`
- `gravity-time/reports/gt-e3-synthesis.md`
- `gravity-time/docs/e3-formal-support-and-recovery.md` — especially T7 and T8
- `gravity-time/docs/foundational-bridge-map.md` — preserve previous versions as append-only revisions
- `gravity-time/docs/e4-configurable-scaffold.md`
- `gravity-time/docs/e4-formal-witness-floors.md` — F1–F6
- `gravity-time/docs/e4-coverage-and-selection.md`
- `gravity-time/plans/round-e4a-plan.json`
- `gravity-time/plans/round-e4b-plan.json`
- `gravity-time/reports/round-e4a-tables.json`
- `gravity-time/reports/round-e4b-tables.json`
- `gravity-time/reports/gt-e4a-reflection.md`
- `gravity-time/reports/gt-e4-report.md`
- `gravity-time/reports/gt-e4-synthesis.md`
- `gravity-time/provenance/execution-GT-P007.md`

**Relevant implementation:**

- `constraint-lab/src/rs_constraint_lab/gt0.py` — `Scaffold` and its held/source/free classification
- `constraint-lab/src/rs_constraint_lab/gte0a.py` — rule grammar and witness templates
- `constraint-lab/src/rs_constraint_lab/gtkernel.py` — rates/witness census
- `constraint-lab/src/rs_constraint_lab/gtobs.py` — stationary observables
- `constraint-lab/src/rs_constraint_lab/gte4a.py` and `gte4b.py`
- Relevant E4 tests and older numerical validation helpers

Use the **repository's current contents**, not the prose in this prompt, as the authoritative statement of file paths, actual outcomes and exact implementation details. If a prior statement and a computed table disagree, verify and record the discrepancy rather than choose the narrative-friendly version.

### Baseline facts to verify

E4A: 36 cells, K2/P3/K3 at N=5,6, frozen `f5b3b50`, results `06e5f36`; 12 K3 replications. E4B: 12 cells, star K1,3/P4 at N=6, selected after E4A reflection `8127d24`, frozen `9a1c539`, results `64e183f`. Latest reviewed GT-P007 head was `11f62df0c56a866e46c212fbb86f4dc5623fb2e6` and the recorded full test suite passed 748 tests. Verify what is current instead of assuming that is still the head.

Some E4 findings are **strong**: lower-floor sites of P3 and K1,3 have substantially higher attachment occupancy; a free P3 chord changes the internal witness environment; and the handover orientation persists across tested reference shapes. Other findings are **qualified**: K2 yields positive raw margins for tested σ>0 path families, but margins generally fade or turn negative after null-density standardisation; some N=6 standardised comparisons reweight low-support density strata. At P4, orbit differences persist in some families despite equal permanent floors.

**Do not conflate these categories.**

---

## 2. Open-thetical orientation: several live explanations, no answer selected

The motivating problem is not “prove that low floor causes attraction”. It is:

> How does a relational structure's internal organisation influence the distribution and history of its connections to other entities, and which parts of that influence are derivable from the rules rather than artefacts of support, conditioning, density, reference choice or stationary weighting?

Keep at least these rival and potentially complementary accounts live:

- **P1 — permanent witness-floor contribution:** path-rule rates contain known state-independent factors on attachments, which bias occupancy among source sites.
- **P2 — state-dependent witness interactions:** free chords, probe relations and other non-held paths create additional witnesses that can reinforce, cancel or dominate the floor.
- **P3 — topology and automorphism orbits:** source vertex position, orbit multiplicities and structural roles can generate differences even where floor counts match.
- **P4 — kinetic competition and the clock:** an attachment may be relatively prominent among events but short-lived in continuous time; equal affinities do not imply equal stationary occupancies or event-order magnitudes.
- **P5 — composition / null geometry:** global gathering margins may be dominated by which density strata are occupied, rather than an intrinsic conditional preference.
- **P6 — imposed-reference effects:** holding a structure fixed creates persistence exogenously and may determine much of the source/probe asymmetry.
- **P7 — unexpected or null mechanisms:** sorting might resist a universal sign theorem, break under reasonable conditioning, or reveal a mechanism not in this list.

For each explanation, say what existing results support, contradict or fail to distinguish, and what a new result *could* establish. Do not reduce these to one weighted coherence score.

---

## 3. Workstream A — mathematical mechanism of relational sorting

### A1. Establish the exactly proved local structure

Start with E4's theorem for any held graph H and source vertex s:

`floor_H(s) = sum_{c in N_H(s)} (deg_H(c) - 1)`

Check the hypotheses: source is the vertex set incident to held edges; attachment slots connect a source vertex and a probe; witnesses are the existing **ordered** path-template instances; the held subgraph is fixed; no rule reads source labels.

Derive the decomposition, for each component and every attachment slot, into:

- permanently held two-path witnesses;
- state-dependent witnesses entirely inside the source (for instance free chords);
- other witnesses involving probes/free relations.

Show explicitly how a path-formation or path-dissolution factor `m` contributes `m^floor_H(s)` on the relevant toggle, with its sign and interpretation. Re-derive F1, F2 and F4 independently, or give a precise dependency proof with reproducible checks.

Explain the orientation-neutrality theorem correctly: constants that multiply formation/dissolution rates of *specific slots* leave the affinities of **closed cycles** unchanged; they need not preserve stationary occupancy, per-event law, event ordering or current magnitudes. Do not infer an attraction or sorting theorem from the local factor alone.

### A2. Attempt the missing mathematical bridge: local floor → stationary orbit occupancy

Ask whether, **under explicitly stated assumptions**, the ordering of source vertices by permanent floor determines or bounds their attachment occupancy. Distinguish the following levels:

1. Exact statement about individual toggle rates at a fixed complete graph state.
2. Exact statement about rate ratios for matched alternative slots under a well-defined comparison, accounting for different non-floor witnesses and the availability of toggles.
3. Statement about conditional attachment rates/odds under a declared state or density conditioning.
4. Statement about stationary occupancy of source-vertex automorphism orbits, in the continuous-time chain.
5. Statement about stationary jump-chain occupancy and subsequent-event probability.
6. Statement about *overall* attachment preference versus a size- and scaffold-specific null.

**Do not leap from level 1 to level 4, 5 or 6.** A nonequilibrium stationary law depends on global flux, not only on one attachment's local rates. Use an appropriate analytic technique if beneficial: generator balance equations, conditional rate balance, Markov-chain tree theorem, coupling, comparison bounds, perturbation identities, exact symmetries or finite-state counterexample construction. If a method fails, explain exactly why.

Priority contrasts, all grounded in published E4:

- **P3:** floor-0 middle versus floor-1 ends. Can the factor and/or stationary orbit ratio be predicted, bounded or even signed independently of a full stationary solve? What changes when the free closing chord is present?
- **K1,3 star:** floor-0 centre versus floor-2 leaves. Does stronger floor contrast imply stronger sorting at matched rule strength? Is a monotonic claim valid or only contingent?
- **P4:** all source vertices have floor 1, yet PATHH and CSPH still have orbit differences. This is a **necessary negative control** for a floor-only explanation.
- **K2:** floor 0 everywhere, yet most positive raw gathering is density composition. A floor-free reference is not sufficient for density-independent gathering.
- **K3:** uniform positive floor and previous suppression of attachment. Does the theorem predict only a local rate effect, rather than the magnitude of stationary suppression?

Aim for **the best justified result**, which might be a theorem with a small domain, a conditional sign result, upper/lower bounds, a counterexample to monotonicity, or a carefully explained non-identifiability. A proof of a false broad claim is not a deliverable.

### A3. Test the explanation against the published numbers—without a new round

You may analyse *existing E4A/E4B tables*, or write a modest, reproducible analysis script to compute **derived quantities using those same results**. Mark these analyses **post hoc / explanatory**, not a new preregistered experimental test or independent confirmation.

Useful (optional, subject to available table fields) comparisons include:

- Per eligible source–probe slot occupancy by source automorphism orbit, under the NULL, reversible and path-rule controls.
- Permanent floor; measured total engaged witnesses; and, where available, state-dependent witness counts by orbit.
- Continuous-time versus per-event conditional occupancy; formation activity versus dissolution activity; holding-time effects.
- Ratios and signed differences of orbit occupancies, with uncertainty/conditioning flags if appropriate (exact finite chains have numerical error, not Monte Carlo sampling error, unless trajectories are used).
- Overall raw, ceiling-normalised and null-density-standardised margins; density support overlap and effective reweighting of rarely visited strata.
- Within-cell matched comparisons versus cross-scaffold contrasts, explicitly noting which dimensions change (source-vertex count, held-edge count, probe count, free chords, orbit sizes, NULL denominator).

Do **not** call within-cell orbit differences an intervention on floor. They control global N and the common stationary environment, but different orbits also have different topology and state-dependent witnesses. Likewise, **conditioning on a free chord's presence is observational**: a difference in conditioned occupancies is not proof that toggling that chord alone caused the whole difference.

Prefer showing a few transparent, interpretable contrasts over a large new metric collection. If an estimator is undefined, numerically unstable or rests on poor support overlap, say so and do not assign it a flattering sign.

### A4. Formal record and falsifiability

Create a formal note distinguishing:

- **Theorem** — complete statement, assumptions, proof, scope and references.
- **Verified identity** — analytic relation checked with fixtures; if proof incomplete, do not call it a theorem.
- **Exact finite-model observation** — computed from published stationary laws, with method, clock and domain.
- **Mechanistic explanation** — evidence and alternative accounts.
- **Conjecture** — a general statement not yet proved.
- **Disproved or underdetermined claim** — counterexample, missing assumption or identifiability gap.

Challenge any proposed general sorting sign law with the existing P4, dynamic-chord and counter-circulation observations before publishing it.

---

## 4. Workstream B — architecture of reference, persistence and identity

Write a substantial but focused architectural inquiry, not a speculative ontology expansion. We need to understand the conceptual distance between a *held reference* and an *emergent reference* and decide which missing capabilities actually require new dynamical machinery.

### B1. Four different reference regimes

Compare these **as distinct architectures**, each with explicit assumptions, observable conditions, risks and potential value:

1. **Externally held reference:** present scaffold H with forbidden dissolution. Useful experimental boundary; persistence is imposed.
2. **Conditioned or instantaneously selected reference:** choose a hub, motif or other configuration-relative frame from a FREE state. This is a method of observing a system, not evidence that the reference persists.
3. **Dynamically maintained / metastable reference:** a relational structure persists over many events or a declared clock interval through endogenous transitions, despite every relation being allowed to change.
4. **Identifiable emergent reference:** an intrinsically defined pattern can be tracked through reconfiguration, perhaps in a quotient under vertex relabellings, with a declared and non-circular identity/matching rule.

An emergent reference does not require you to assume a new **primitive**. It may be built from existing graph states, histories or derived observables. Equally, do not claim it exists merely because a hub can be named at each instant.

### B2. Identify the minimum necessary definitions and discrimination tests

Examine:

- **Existence and recognition:** what constitutes a source-like motif? Which motif definitions are arbitrary, induced by the analyst or generated by the grammar?
- **Persistence:** lifetime, recurrence, metastable retention, survival through partial edge replacement, and finite-state mixing; what thresholds would be predeclared in a future experiment?
- **Identity through change:** when is a motif at event t the same structure at event t+1? How should ties, splitting, merging, relabelling, extinction and reappearance be handled? Is a history register truly necessary, or does a current-state description suffice?
- **Relative frame:** how can attachments, distance or separation be measured when the reference itself changes, without making the measurement dependent on the desired gathering result?
- **Symmetry and labels:** in a label-covariant finite FREE model with symmetric prior, named entities are exchangeable. Explain the distinction between a labelled persistent centre, a symmetry-invariant motif, a trajectory-conditioned frame and a spontaneous symmetry-breaking claim. Do not turn frame selection into evidence for permanent localisation.
- **Kinetics versus clock:** event count and continuous time are separate model conventions; any persistence or recovery claim must state which is used.
- **Support versus propensity:** hard gates, soft kinetics, conditional occupancy and persistence do not imply physical motion.
- **Mutual interaction:** what would it mean for two persistent, endogenous structures to influence each other, distinct from the analyst holding one fixed?
- **Operational displacement:** what could change *relative to what*, and what non-circular identity and metric would be required? Do **not** define or claim acceleration by renaming attachment/density gradients.
- **Compilation / ontology gate:** could candidate extra machinery be represented by additional relations, finite current state, K/J budget or explicit history H under the 8G compilation test? Do not recommend a new ontology axis without an exact expressivity question and failure of the applicable compilation alternative.

### B3. Build a prerequisite map rather than a predetermined staircase

Separate:

- **Logically required within an operational definition** (e.g. identity and a reference for displacement of a tracked object);
- **Potentially sufficient under stated assumptions** (e.g. a long-lived motif could provide a temporary frame, but not automatically a metric or attraction);
- **One candidate implementation among several**;
- **Speculative RS interpretation**;
- **Unknown/possibly unnecessary**;
- **Blocked by current data or architecture**.

Allow branches and alternate routes. A gravitational description need not emerge from the specific path-template families currently tested; and foundational organisation may be informative independently of gravity.

Keep the original **two-lens bridge map**: from bottom-up demonstrated capability toward larger phenomena, and from top-down phenomena toward missing prerequisites. Update it as an append-only new revision, retaining past claims and explicit supersession links rather than silently rewriting research history.

### B4. Concrete next-round design choices, without execution

Propose **at least three genuinely different bounded next-step candidates**. Candidate examples (refine or replace based on your review):

- **Mechanism discrimination at fixed small N:** a carefully frozen derived-measurement or control round separating floor, state-dependent witnesses, topology and density composition; avoid re-running published cells without an independent reason.
- **FREE persistence and reference feasibility:** predeclare motif identity, symmetry-invariant persistence metrics, conditioning controls and a finite-N kernel budget before probing for endogenous frames. A dynamically selected instantaneous hub is a negative/control baseline, not proof of emergence.
- **Dynamic source transformation:** investigate how a non-held source-like motif reorganises and how its attachment profile changes, distinguishing conditioning from causation. Requires an operational motif identity and a proper experiment freeze.
- **Mathematical theorem/counterexample:** attack aggregate sorting or stationary orientation sign using a rigorous finite-N symbolic argument or a separately frozen bounded search.
- **Larger-N scaling:** only if a specific mechanism and discriminating observable justify the additional cost; not as the default next round.

For each candidate give expected information value, plausible alternative outcomes (including null/negative), mechanism novelty, artefact discrimination, interpretability, cost/memory/risk, cross-programme relevance and impact on the two-lens gap map. **No aggregate ranking score.** Recommend one principal candidate and a fall-back, with concrete reasons and a clearly defined human decision gate.

Do not draft an apparently frozen E5 plan that has already been influenced by new E5 data: **there must be no new E5 data in this task**.

---

## 5. Open-theoretical and mathematical integrity checks

The conclusions must explicitly address:

1. **Does the witness-floor formula imply the observed sorting direction, or only a local rate factor?** Give the strongest defensible answer, with counterexamples/boundaries.
2. **What is the explanatory residue?** Account for P4's equal floor but unequal occupancy, P3's dynamic chord, and the difference between star and P4 despite total floor ordering.
3. **What do the clocks do?** Distinguish stationary CT time, jump-chain event weighting, one-step transition probabilities and cycle affinities.
4. **How much of native raw gathering is composition?** Show the relevant published E4 evidence and support-overlap limitations. Never claim density-independent attraction from raw margins alone.
5. **What is the status of the E3B counterfactual?** It is an instrument, not a native label-covariant rule. E4 partially vindicates the scaffold-confound diagnosis without reproducing every E3B standardised result.
6. **What does 'emergent' mean operationally?** Distinguish instant selection, conditioned frame, stationary symmetry, genuine persistence and identity across events.
7. **Which mathematical capabilities are now present and which prerequisites remain undefined?** Do not silently equate event order, drift, displacement, acceleration, metric, or physical time.
8. **Where are plausible explanations independent of gravity?** Report structural and mathematical findings for their own information value.
9. **What did this consolidation fail to resolve?** An explicit list of proof gaps, counterexamples and observability limits is required.

Maintain evidence layers throughout:

- `[O]` computed observation in a declared finite model;
- `[M]` derivation, theorem, formal property or conjecture (identify which);
- `[RS]` provisional relational-ontological interpretation;
- `[P]` physical comparison, only if independently warranted—otherwise none;
- `[T]` theological/worldview premise, not part of the calculation.

No toy result establishes actual spacetime, gravity, physical entropy production or a real physical substrate.

---

## 6. Cross-programme coherence, without merging records

Read `gravity-time/docs/e3-cross-programme-transfer.md`, `gravity-time/docs/e4-cross-programme-transfer.md` and the Constraint Laboratory open-problem/theorem catalogues **read only**.

Identify candidate transferable insights for:

- **CL-Q04:** incidence-sensitive coupling, witness support, possible factorisation and stationary consequences;
- **CL-Q05:** dissolution, recovery, persistence, passage/committors and dependence on source structure;
- **CL-Q03 / compilation discipline:** if identity-through-change appears to require memory/history, distinguish expressivity from a convenient derived register.

The GT grammar here is O=2 with single pair toggles; CL has different O=3 questions and its own baseline. Do not upgrade GT evidence to a CL theorem without an explicit proof transfer. Do not edit CL branches or canonical findings. Put proposals in a **GT transfer note** only.

---

## 7. Implementation, verification, and provenance rules

The main output is analysis and reasoning; code changes are optional and should be modest.

- Before computing secondary derived quantities, write down their definitions, conditioning, denominator, clock and null interpretation in a dated audit note. This does not make the analysis independently preregistered: E4 data are already exposed.
- For proofs, provide a paper-traceable derivation. Use independently written symbolic/synthetic proof fixtures to check indexing, ordered witness multiplicity and small constructions. Distinguish proof from finite verification.
- If reusing published numerical tables, test extraction/aggregation against selected published values and the known NULL/CLOSEW controls. Report mismatches.
- Do not rerun original E4 science as though it were an unopened confirmatory replication. A diagnostic reproduction must be explicitly labelled.
- If a new large computation, exhaustive parameter search, or novel scientific design becomes needed, **stop that strand** and specify what a separate, frozen and human-authorised plan would require.
- Preserve the 8G scientific-plan discipline, deterministic code paths and provenance of existing results.
- Add only necessary, backward-compatible tooling; do not refactor shared GT/CL machinery for aesthetic reasons.
- Run the relevant tests and, where feasible, the full suite; record counts and any failures. Verify GitHub Actions after push. Do not claim a green run unless it is reported green.
- Keep significant mathematical failures and numerical qualifications visible in the report; never revise previous frozen thresholds retroactively.

---

## 8. Required durable deliverables

Create meaningful, reviewed Markdown artifacts on the current GT branch (adapt names only if repo conventions require it):

1. **`gravity-time/docs/gt-p008-coverage-and-integrity-audit.md`**  
  Baseline, current head, published E4 evidence, exact theorem/observation boundaries, residual confounds, exposure and permitted analyses.
  
2. **`gravity-time/docs/e4-sorting-mechanism-derivation.md`**  
  A real mathematical investigation: local witness factors; possible orbit-level theorems/bounds; proofs, counterexamples or non-identifiability; chord and uniform-floor controls; links to source tables and code. Include statements explicitly marked theorem, conjecture, observed or disproved.
  
3. **`gravity-time/reports/gt-p008-secondary-analyses.md`** (only if new derived views of published data are useful)  
  Reproducible post-hoc comparisons, exact cell references, clock/null/overlap diagnostics, and an explicit statement that they are *not* new E5 evidence. Omit the file if no useful secondary analysis is justified, explaining why.
  
4. **`gravity-time/docs/reference-architecture-review.md`**  
  Comparison of held/conditioned/metastable/identifiable references; definitions and measurement criteria; symmetry, clocks, false emergence, identity-through-change and 8G compilation questions; concrete boundaries on what can presently be inferred.
  
5. **`gravity-time/docs/gt-p008-next-round-options.md`**  
  At least three bounded designs, multifactor comparison without a combined score, primary and fallback recommendation, explicit stop/human-authorisation gates. These are proposals, **not executed** or already frozen E5 experiments.
  
6. **`gravity-time/reports/gt-p008-consolidation-report.md`**  
  A plain-English explanation addressed to the sole human researcher. Open with “what did we actually learn?”, not an index of files. Explain the sorting observation, what was/was not proved, the density issue, implications of imposed references, implications for the foundational bridge, and next recommendation. State all significant negative, inconclusive or counterintuitive results.
  
7. **Append-only coherence and bridge-map updates:**
  
  - `gravity-time/docs/foundational-bridge-map.md` — add a new clearly marked GT-P008 revision; retain previous sections and evidence states.
  - Coherence ledger, relation entries, current map/snapshot and hypotheses as justified by the actual work. Do not inflate a restated observation into multiple new findings. New open questions should have discriminators and dependencies. The established ontology remains unchanged; candidates belong in the proposal file only.
  - `gravity-time/docs/gt-p008-cross-programme-transfer.md` — suggestions only, if substantive.
8. **`gravity-time/provenance/execution-GT-P008.md`**, prompt transcription/ledger row, and the journey record. Record start head, commit sequence, whether any proof fixtures or secondary scripts were run, all data exposure, test outcomes, CI status, and confirmation that no E5 cells were executed. Update `gravity-time/README.md`, roadmap status and PR #6 description with an accurate concise summary.
  

Include one or more compact **Mermaid dependency or mechanism diagrams embedded directly in Markdown**, where they improve comprehension; no separate images are required. The diagrams must distinguish established, observed, conjectural and undefined connections. Avoid excessive diagrammatic decoration.

---

## 9. Completion gates and exact stopping instruction

Before finishing, independently verify:

- The distinction between *permanent witness floor* and *stationary attachment sorting* has not been erased.
- E4's P4 residual differences and E4's mainly density-composition gathering remain visible negative/qualifying evidence.
- No result has been described as a physical force, gravitational acceleration, real clock dilation or proof of a substrate.
- The architectural distinctions between **externally held**, **instantaneously selected**, **metastably maintained** and **identifiable through change** have been preserved.
- New mathematical derivations either have proofs or explicit unresolved assumptions/counterexamples.
- Previously published E0–E4 plans, results and historic evidence have not been altered.
- No new science experiment/parameter sweep has been silently undertaken; E5 is **not** opened, frozen or executed.
- The current branch and PR remain GT-specific and the PR remains **draft and unmerged**.
- The final report and options support an informed human decision about the **next experiment**, including the possibility that no experiment is justified until a definition is improved.

Commit and push the deliverables to `research/gravity-time-admissibility`. Run tests, check remote head and CI, and update PR #6 with clear provenance. If CI is unresolved, report that fact instead of declaring success.

**Then STOP.** Do not begin E5A, modify the canonical ontology or work on another programme's branch. Return a concise, understandable summary of the mathematical results (including failed theorem attempts), the architecture conclusions, the recommended next scientific design, its unresolved risks and links to the committed documents.

---

### Governing question

> **How far can the observed organisation of relational attachment be explained by the existing constraints—and what must a relational system actually be capable of before an externally held reference can be replaced by an identifiable, dynamically maintained structure?**

The objective is *greater coherence of understanding*, not confirmation of gravity or of any predetermined ontology.
