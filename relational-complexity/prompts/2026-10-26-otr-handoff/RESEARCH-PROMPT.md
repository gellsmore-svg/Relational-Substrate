# RRC — Open-Thetical Research continuation for a new model
**Created:** 26 October 2026  
**Working mode:** Autonomous, focused, recoverable research.  
**Status:** Guidance for selecting the next research direction, **not** a frozen experimental plan or a required sequence of experiments.  
**Repo:** `gellsmore-svg/Relational-Substrate`  
**Branch:** `research/recursive-relational-complexity`  
**Working directory:** `relational-complexity/`  
**Method:** `research-methods/open-thetical-research.md`

## Read this first

You are continuing the RRC programme **after a previous Grok CLI session exhausted its available credits**. Do not infer an unresolved scientific question must be solved, or an unexecuted plan run, merely because a predecessor prepared it.

Begin with a fresh audit of current branch HEAD, local working tree, historical and prospective results, status ledger and actual available compute. The last checked GitHub HEAD before this handoff was `8923de6565937a99a185f817526816ba50690def`. The preceding complete scientific round was **Atlas-017**, with **215 cumulative verified cells** at that checkpoint, plus 15 historical Atlas-007 failures excluded from the verified tally.

**Read `FROZEN-PLAN-DISPOSITION.md` in this folder.** Atlas-018, -019 and -020 were already frozen and preflighted but had **no committed scientific executions** at that checkpoint. Their disposition is **deferred, not required next**. They are not scientific negatives and have not been cancelled for lack of value. You may execute them *unchanged* if, after a fresh OTR selection, they are the best inquiry. You may also pursue a different direction. Do not modify or "unfreeze" them. Log a reasoned `retired-unexecuted` decision separately only if you actually make one.

## 1. Mission — build understanding, not a quota

Investigate the mathematical possibilities of **how relational configurations can compose, constrain, participate in further relations and affect dynamical behaviour**, including when effective descriptions preserve what matters and when they do not.

The central issue is the **relationship between a relational system and the further relationships in which it participates**. Do not reduce the programme to repetitions of bit-flip tables or to forced demonstrations of hierarchy or complexity. Equally, do not dismiss bounded exact finite systems merely because they are simple: their scope and independent significance determine their value.

The Relational Substrate ontology and its Transmit–Carry–Receive (TCR) motivation guide what questions matter but are **not** targets to be proven or outcomes to encode. No particular number of links, levels, cycles or constraints is preferred. Negative, null, reducible and known-theorem outcomes are legitimate.

Use the RRC charter's OTR inquiry loop:
**orient → select for information value → freeze → calculate → observe → challenge → integrate → reflect → choose next**.

**You have scientific discretion.** This prompt gives a selection framework, not a homework assignment. Do not commit an experiment solely because it was named in a previous prompt. Conversely, if you choose and freeze an experiment and still have resources, complete its run and report instead of mistakenly presenting the frozen plan as a verified result.

## 2. Mandatory repository orientation and scientific bookkeeping

Review at minimum:
- `PROGRESS.md`, `charter.md`, `README.md`, `docs/atlas-charter.md`, `docs/atlas-crosswalk.md`.
- `atlas/` question, idea, coverage, pattern and equivalence registers.
- `docs/compilation-gate.md`, `docs/composition-taxonomy.md`, `docs/representations.md`, `docs/composition-operators.md`, `docs/cover-observations.md`.
- `docs/state-event-families.md`, `docs/event-semantics.md`, `docs/event-kernel.md`, `docs/coupled-models.md`.
- `src/rrc/event_kernel.py`, `src/rrc/coupled_models.py`, `src/rrc/composition.py`, `src/rrc/items.py`, runner, validation and tests.
- The latest completed Atlas-014–017 result reports and frozen plans, and Atlas-018–020's *plans and preflights* with the separate disposition record.
- `research-methods/open-thetical-research.md` and existing cross-programme reuse boundaries.

First determine **what has actually been calculated**, versus what is a typed fixture, proof sketch, method extension, immutable unexecuted plan, or experimental result.

Current methodological boundary:
- `event-kernel-0.1.0` supplied frozen Atlas-017 and did **not** semantically validate toggle/joint Hamming distance.
- `event-kernel-0.2.0` is a separate strict method, with declared width distinguishing toggle (distance one), joint (distance at least two), noop and generic transition. Do not change old semantics under the same ID.
- Strict event comparisons and finite-horizon event kernels were added in the prior session, but as of the handoff had no scientific execution for Atlas-018–020.
- One-step single-toggle compilation, a new event **representation**, a new event **support**, an independently selectable state coordinate and an autonomous dynamical higher-order entity are **five different claims**.

Maintain the distinction among facts proved in the model, frozen computational observations, model inferences, representation artefacts, external mathematical precedents, RS-level interpretation and theological ontology. Do not promote the latter two to numerical evidence.

## 3. Choose research by information value: several portfolios

Select an interesting **small set of complementary alternatives**, not the largest number of easily generated cells. The following are invitations, not all mandatory.

### A. Genuine composition and interaction of relational systems

Explore mathematically typed products, interface identification, duplicated interfaces, joint updates, changing relationships among blocks, and recursive participation of a composite in another interaction.

Useful discriminations:
- Identified shared interface versus two coupled copies versus freely independent copies.
- Static overlay / observed overlap versus an actually stateful, evolving interface.
- Extra state H not determined by X versus a derived label H=f(X).
- One-step joint event versus sequential single events under **matched observation clocks**.
- Invariant interface subspaces with exact conjugacy versus leaking/nonconjugate images.
- Higher-level descriptions that close dynamically versus ones that depend on hidden state or past history.

The prior two-bit `coupled_models.py` readings are good typed controls but several are ordinary re-encodings of existing current-state single-toggle laws. Investigate genuinely different mathematical capabilities *only when a precise type or invariant distinguishes them*. A different label or number is not discovery.

### B. Effective dynamics and observational closure

Explore exact strong lumpability, valid successive Markov quotients and failures of closure under interacting systems. Choose maps and constraints **before** seeing the desired outcome; do not hunt until a success is found.

Possible questions:
- Does coupling change whether a small noninjective observation preserves the Markov property?
- Can a direct coarse observation be exact when an intermediate one is non-Markovian?
- Can a genuinely nontrivial two-stage quotient be exact at both stages, and with which scope?
- Under what conditions does retaining an additional relational coordinate restore sufficient memory?
- When do event-labelled dynamics differ although their aggregate kernels are identical?

An inexact Markov observation has no exact first-order quotient in the declared class. Do not silently fill undefined quotient rows.

### C. Temporal effects / propagation without a predetermined cascade

If informative, define exact finite-horizon contrasts or an explicit intervention on event rules **before computing them**. Distinguish:
- Perturbing an initial state;
- Conditioning on another coordinate;
- Comparing two specified transition laws;
- Performing a defined causal intervention;
- Merely following a path in a dependency diagram.

Compute bounded P^k or equivalent exact rational distributions, with informative controls, and record zero effects, timing conventions, leakage, and hidden-state confounds. Do not claim a causal mechanism from correlation, a static rule graph or reachability.

### D. Independent elementary constraint / representation exploration

Keep an independent avenue for elementary constraints, carrier geometry, constraint composition and equivalence classes, selected on its own information value. Possible variations include form versus dissolve, positive weights versus prohibited support, higher declared/effective rule cardinality and families not sampled earlier.

Do not rerun Atlas-016's incident-plus-disjoint carrier simply to reproduce its values, Atlas-017's half-probability rows, previous atlas defects, or repeated known permutation identities.

### E. Mathematical synthesis

Seek **scoped** identities, counterexamples and connections with established Markov-lumpability theory, products and restricted products, group symmetries, stochastic bisimulation, event-labelled transition systems and graph/hypergraph composition. Existing theorems are precedents, not novel laws. A clear analytical counterexample may be more informative than a numerically larger atlas.

## 4. Genuine OTR selection — permission to pivot or stop

After orientation, record a brief qualitative choice, considering:
**Consequence, Readiness, Leverage, Cognitive/computation cost, Personal research significance.**

These are independent assessment vectors, not numeric scores. Explain why the selected contrast distinguishes meaningful possibilities, including null and negative alternatives.

Pick the **next smallest informative mathematical step**, not a fixed number of steps. An acceptable cycle may produce one frozen and verified new round, a strong analytical result with independent checks, several genuinely diverse short rounds, or a reasoned non-experimental conclusion. Do not invent experiments to justify further consumption of credits.

Do **not** interpret a token/credit cap or tool interruption as a reason that an unrun scientific plan has low scientific value. If resources end, record `resource-blocked / not executed`, the exact restart point and uncommitted work; do not announce the mathematical work done when it was merely prepared.

If you select Atlas-018/019/020, use their **original frozen items unchanged**. If you select something else, those three remain deferred and require no replacement ritual. If you conclude one of the frozen rounds is redundant or ill-posed, record a reasoned `retired-unexecuted` / `superseded-unexecuted` note separately, never modify the original plan.

## 5. Strong technical and experimental requirements (only for work actually chosen)

For any new scientific computation:
1. Declare state space/type, event/constraint grammar, clock, transition law, observation maps, inference target, nulls, controls and reproducible selection.
2. Define criteria for representation equivalence, kernel equivalence, labelled-event equivalence and structural/conjugacy equivalence distinctly.
3. Preserve exact arithmetic where tractable. Use independent hand-enumerated or separately implemented checks on small cases. Assert both positive and negative fixtures.
4. Bound state enumeration and other expensive operations. Use <=120 second ordinary watchdog and no indivisible task expected above 300 seconds; prefer small resumable items with short budgets.
5. Preflight the **real worker path** in disposable files, verify serialisation, receipts, hashes, interruption/resume and schema. Keep test/dry-run observables outside scientific results.
6. **Commit and push the immutable new plan before running scientific cells**, then execute only that frozen plan, verify, persist, report, integrate and commit/push the results separately. Do not post-select or revise plan items after observations.
7. Keep failed, timed-out, nonunique-stationary, undefined-quotient and unrun results explicit.
8. Do not alter frozen plans/results through Atlas-020, historical failures or other independent research programmes. Shared synthesis and `books/` are outside scope without the established process.

A method change must be versioned. A new type of event support may require a new method; do not mislabel it as a new fundamental law. If no new computation is justified, supply a rigorously supported analytical assessment rather than a fabricated frozen plan.

## 6. Deliver a finished **increment**, not pretend the programme is finished

The incoming model should make useful progress and create a clean handoff. A **completed increment** requires:
- A mathematically precise question/construction or bounded investigation actually answered;
- Its evidence/verification (proof with independent checks, or valid frozen scientific execution);
- Honest observations and alternatives, including negative/reduction results;
- Updated research registers / `PROGRESS.md` showing exactly what changed and what remains open;
- Committed and pushed records (except clearly disclosed failures);
- A next research choice or explanation that none is justified yet.

If the increment is only implementation support or mathematical preparation, call it that. Do not claim it is a completed scientific experiment.

**Do not require the new model to finish every option in this prompt. Do not require execution of three old frozen plans.** Seek useful mathematical discovery with disciplined decisions, not compliance theatre.

## 7. Final handoff format

In `PROGRESS.md` and a final concise response, provide:

- Starting/ending branch SHAs and every new substantive commit.
- Research question(s) selected, with reasons and alternatives explicitly rejected or deferred.
- Mathematical facts, computations and checks actually completed; plan hashes and verified/failed/unrun counts for any round.
- What reduces to the original single-toggle grammar, what genuinely differs at the declared state/clock/event level, and what remains merely an untested possibility.
- Exact status of Atlas-018, -019 and -020: **deferred unless independently reselected**; no invented results or silent cancellation.
- Cross-atlas correspondences and negative cases with scope limitations.
- Current blockers, remaining open atlas questions, possible next useful inquiry and exact restart point.

**Begin from live HEAD. Choose for understanding. Execute and verify the work you actually select. Stop at a coherent checkpoint rather than chasing a quota.**
