# RRC next-cycle research prompt — Relational events and compositional dynamics
**Date:** 25 October 2026
**Audience:** Grok / command-line research agent
**Status:** Working research handoff prompt. **Not a frozen plan, calculation, result, or alteration of the charter.**
**Repository:** https://github.com/gellsmore-svg/Relational-Substrate
**Branch:** `research/recursive-relational-complexity`
**Directory:** `relational-complexity/`
**Method:** `research-methods/open-thetical-research.md`

## 0. Execute autonomously, but preserve the science

Continue the existing **Recursive Relational Complexity and Structural Composition** (RRC) programme under Open-Thetical Research (OTR). Start from the latest remote and local repository state, not from an assumed commit. Verify the working tree and any parallel work before changing files. Commit and push small independently recoverable increments. Finish with a truthful handoff in `PROGRESS.md`.

This is a directive to **investigate**, not to demonstrate that autonomous higher-order relations, recursion, emergence, or any particular ontology must occur. Mathematically trivial, reducible, undefined and negative results remain valuable. Do not contrive transition rules or cherry-pick cases to force an interesting outcome.

The last independently reviewed HEAD was `611dfc8a20c55a8a85ad8fdb7ec2b7418f0ff5e2` (verified Atlas-016); 209 verified atlas cells, excluding 15 historical failed Atlas-007 items, were known at that checkpoint. The known engine was `rrc-0.4.0`. These are **checkpoints only**. The first task is to confirm the actual current facts. Do not reset or overwrite newer work.

## 1. Read authoritative context and prevent duplicate work

Read:

- `PROGRESS.md`, `charter.md`, `README.md`, `docs/atlas-charter.md`, `docs/atlas-crosswalk.md`, and OTR.
- The living `atlas/` idea, question, equivalence, coverage and pattern registers.
- `docs/compilation-gate.md`, `docs/composition-taxonomy.md`, `docs/composition-operators.md`, `docs/representations.md`, `docs/cover-observations.md`, and `docs/state-event-families.md`.
- `src/rrc/state_families.py`, `src/rrc/coordinate_examples.py`, `src/rrc/composition.py`, `src/rrc/items.py`, transition and weight compilers, runner and tests.
- Frozen plans and completed results for Atlas-014, Atlas-015 and Atlas-016, and relevant prior rounds.
- The previous next-cycle handoff in `prompts/2026-10-25-rrc-dynamical-composition-next-cycle.md` to distinguish **completed stages** from work that is still open.

Respect all existing scientific freezes. Never rewrite historical plans or result directories, including failures.

**What was completed by Atlas-016:** bounded successive Markov descriptions, fixed potential-versus-realised block overlap observations, typed state/event/interface examples, and a separate eight-cell elementary sample on one carrier comprising an incident pair plus a disjoint edge. The last sample distinguished hard prohibitions, positive-weight multipliers and combinations; several rules matched old bit-position tables despite different carrier geometry. These are scoped findings, not laws about arbitrary carriers.

**What remains open:** nontrivial composition with independent state/event semantics, experimentally evaluated joint events, changing block-family dynamics, genuine model comparisons across clocks/representations, and well-defined dynamical propagation or intervention. Do not keep rediscovering the same single-toggle weight-table identities simply because they are easy to compute.

## 2. The mathematical frontier: events are not merely edge weights

So far the central engine has largely used a finite state of present/absent carrier edges, one bit toggle per step, with nonnegative integer weights that determine the next event. A zero row has the declared halt/self-loop completion. This is an effective experimental grammar; it is not assumed ontologically universal.

The next cycle should examine **mathematically distinct transition structures** without presupposing that a new structure is necessary. The crucial distinctions are:

1. **Observation:** H=f(X). No independent state beyond X.
2. **Extended state:** (X,H), where multiple H values can coexist with one X. Coupling may or may not be present.
3. **Alternative one-step event:** a transition of Hamming distance two or more under an explicitly fixed state representation.
4. **Shared-interface composition:** two relational systems with an identified interface, compared with independently duplicated interface coordinates.
5. **Changing relational family:** block membership or overlap may be part of the evolving state, not merely a fixed external instrument.
6. **Dynamics of an effective description:** a quotient Markov law exists only when justified; a state-derived label is not an autonomous higher-order entity.

Do not call an extra named bit, alone, an expressive breakthrough. The established activity-bit construction `EQ-027` reduces to an existing listed-edge model. Do not rerun it as a novelty claim.

Do not call a joint event fundamentally irreducible: under a **fixed representation, state space and one-step clock**, a single-toggle chain has zero probability on Hamming-distance-two successors, whereas an explicitly allowed joint event may have positive probability. That is a precise scoped support distinction. Multi-step observations, augmented intermediate states or alternative clocks may reproduce some observable effects. Specify and test relevant reductions rather than denying them.

## 3. Portfolio A — Minimal general event kernel, with independent validation

Before authoring a scientific round, design the **smallest** typed extension needed to compare event grammars faithfully. Prefer a new, explicitly versioned mathematical method over changing the meaning of `rrc-0.4.0`. An isolated experimental module may be sufficient; do not refactor the entire historical engine.

Start from a finite set of states S and a declared catalogue of admissible events. For each event e, specify:

- Input state and event type, including coordinate types.
- Target state, or a declared deterministic state update.
- State-dependent nonnegative integer weight/rate.
- Whether two distinct events leading to one target must have their weights **summed** before transition normalisation.
- Row completion when no event is enabled.
- A discrete-event step clock and, if considered, a clearly separate physical-time or continuous-time semantics.
- Rules for identity, simultaneous updates, no-ops, invalid events and failure.

Produce the exact transition kernel P(s,t) using rational arithmetic on small examples. Keep events, target states, aggregate transition weights, normalised probabilities and clock interpretation distinguishable.

**Critical:** a self-loop arising from a declared no-op event is not automatically the same as a halt self-loop from a zero-weight row. Define both explicitly.

Suggested candidate grammars to compare (not mandatory, not all to be implemented):

- G0: ordinary single-bit toggles (existing control).
- G1: one simultaneous two-bit update plus selected single-bit events.
- G2: conditionally enabled joint event, without an assumed hierarchy.
- G3: event types acting on an additional activity/interface coordinate.
- G4: a constrained coupled update of two copies of a shared interface.
- G5: a block-family change as an event distinct from elementary relationship toggles.

Use small, state-labelled constructions where exact verification is tractable. Avoid arbitrary hard-coded examples designed only to produce an intended stationary mean, apparent cascade or new recurrent class.

**Tests:** transition rows sum to one exactly; invalid updates are rejected; duplicate event targets aggregate correctly; event-order invariance holds when promised; positive/zero-row cases are correct; full transition tables match independent hand enumeration on tiny systems; existing single-toggle law is recovered as an explicit embedding when assumptions match; support differences under fixed clock are demonstrable. Tests are not scientific cells.

## 4. Portfolio B — Interaction between relational levels and interfaces

Develop a small set of **comparable but non-equivalent model families**. The mathematical objects need not form a chain of higher and higher graphs.

### B1. Identified versus duplicated shared interface

Begin with two elementary relational subsystems sharing an edge or interface.

Compare:

- A single identified interface coordinate.
- Two independently evolving copies of the purported shared interface.
- A restricted product where the copies must agree.
- A coupled transition that updates both interface copies together.
- Optional explicit asynchronous updates under a separate semantics.

The mapping from identified state into the duplicated-state agreement subset must be explicit. Compare event support and exact transition laws **on the correctly mapped states**. Distinguish a bijection of state sets from equivalence of dynamical laws. Explain when the joint update is one bit toggle in an identified representation but two toggles in the duplicated representation.

The existing typed note provides definitions, not a frozen experimental result for these alternatives. Reuse its validated types and extend only as needed.

### B2. Additional state versus derived state

Use (X,H), with H not determined by X, but introduce a coupling with a clear mathematical role. A useful witness is two complete states with identical X, different H, and different probabilities for a specified X-event.

Then investigate whether an observation of X alone is Markovian, and whether including H restores exact closure. Distinguish this from automatically asserting that H is a new physical primitive.

Check whether the complete transition law compiles to an ordinary listed-bit grammar. If it does, record the reduction rather than hiding it.

### B3. Changing block families

Separate three readings:

- Fixed family B and changing present relationships S_t.
- A changing family B_t with a fixed underlying eligible carrier.
- Joint changes of a constituent and its membership/interface in one event.

Define block names, membership semantics, admissible updates and recoverability. Potential overlap and realised overlap remain different observables. Do not confuse dynamic activation of fixed blocks with actual change of block membership.

Pick more than one structural arrangement **if** it adds independent information; do not choose a favourite number of blocks or levels.

### B4. Several kinds of composition

Keep product state, interface identification, overlapping families, graph operations, quotient maps, and joint event structures as distinct types. Explore how one construction can participate in a further operation **only when types and transition laws make that meaningful**. An idempotent canonicalisation is not recursive dynamics.

## 5. Portfolio C — Exact dynamical descriptions, memory and propagation

Continue the Markov-quotient research with an emphasis on **nontrivial effective descriptions**.

Investigate at least a few independently selected examples across the new event structures if feasible:

- A non-injective observation with an exact closed Markov law.
- An observation that ceases to be exact after adding a coupling or joint event.
- A coarser direct observation that is exact despite a non-Markov intermediate description.
- An extra-state projection whose hidden coordinate matters to the next-event distribution.
- A valid two-stage quotient that actually reduces states at both stages, if mathematically available.

Use exact factorisation and lumpability criteria. If no suitable nontrivial two-stage example occurs in the declared sample, state that. Do not generate endless fixtures until one appears. Report direct and sequential kernels under meaningful label correspondences, not incidental integer class order.

**Propagation** requires a defined time-dependent stochastic or interventional contrast, not a directed line in a rule-dependency diagram. Possible candidates include:

- A finite-horizon difference in an observable's distribution following a declared initial-state perturbation.
- A matched comparison of two transition kernels differing in one predeclared event rule.
- A clearly defined intervention on an event rate or admissible support.
- A change propagating across a typed shared interface over several steps.

Define the contrast and its interpretive limits first. Distinguish stochastic conditioning, initial-state sensitivity and causal intervention. Compute P^k exactly for bounded k when suitable. No preferred cascade depth or form is assumed. A negative or zero propagation contrast is informative.

Do not silently describe a dependence observed under one selected initial distribution as strong lumpability, a universal causal law or emergence.

## 6. Portfolio D — Independent elementary constraints and atlas synthesis

Maintain an independent stream of elementary constraint research so that the higher-order programme does not become self-confirming.

Atlas-016 already covered the path-plus-disjoint-edge carrier with one prohibition, one multiplier and a mixed pair under factor three. Do **not** expand its exact stationary values or its bit-swapping identity merely because they appeared recently.

Choose a different informative slice if justified: mixed formation/dissolution, different guard expressivity, larger constraint cardinality with effective-cardinality controls, varied topology and event placement, or other bounded independent grammar coverage.

Preserve comparison among raw integer tables, normalised kernels, support, recurrence, stationary uniqueness, marginals, automorphisms, general bit permutations and structural observations. A table may match a former carrier while structural quantities differ. Equal means do not imply equal kernels.

Independently compare the new event/coupling results to relevant established mathematics, such as lumpability, group actions, stochastic transition systems, graph/hypergraph methods, compositional Markov processes and stochastic bisimulation—**only with explicit mathematically correct mappings and scope**.

Identify:
- established theorem applications;
- exact new-to-this-atlas identities;
- counterexamples and reducibilities;
- ordinary implementation consequences;
- genuinely open mathematical regions.

Do not call a familiar theorem original research, or infer relational ontology from finite mathematical compatibility.

## 7. Select, preflight, freeze and run without hindsight bias

Choose bounded investigations for **information value across several plausible alternatives**, not to force a preferred result. Record the scientific question and selection scheme before seeing experimental outputs.

For each frozen scientific round, specify:

1. State types and sizes, carrier/interface/block family and source definitions.
2. Event grammar, event semantics and fixed clock.
3. Rule list, action, polarity, normalisation and zero-row convention.
4. Chosen sample (exhaustive slice, stratification or predeclared illustrative controls).
5. Observables, equivalence relation and expected computational cost.
6. Controls and alternate explanations.
7. What would count as support, reduction, failure, unknown or undefined.
8. Exclusions, computational limits and stopping criteria.
9. Engine/method version, plan identifier and immutable plan hash.

Separate disposable implementation preflight from scientific observation. Preflight must exercise the **real worker path**, including schema validation, serialization, receipts/checksums, crash/resume and verification, and discard its scientific observables. Commit and push the frozen plan **before** executing any scientific cell. Execute small independent items; verify and commit results separately. Preserve failed cells rather than editing the plan to erase them.

**Runtime:** normal watchdog 120 seconds; no indivisible calculation expected to exceed five minutes; prefer approximately 1–3 minute or smaller independently recoverable items; short invocation budgets and persistent deterministic item records. Exact rational enumeration is preferred on small systems. If cost is excessive, keep a precise open question and stop rather than launching monolithic work.

Never modify frozen Atlas-001–016 plans/results or retroactively relabel `rrc-0.4.0` results. Do not edit other research programmes, books or shared-synthesis authority outside the defined integration process.

## 8. Completion strategy: diverse, recoverable increments

Suggested **sequence**, adjustable after the initial audit:

**Stage 1 — Verify, type, and test:** Inspect HEAD and previous prompt, complete a precise comparison matrix of event/interface model families. Identify reducible candidates and the minimum change of mathematical semantics. Implement tiny validation examples and tests. Commit and push.

**Stage 2 — New event grammar:** Build a minimal, explicitly versioned exact kernel for any justified multi-coordinate or typed-event update. Record event-to-target aggregation and clock semantics. Validate independently and commit.

**Stage 3 — First bounded scientific event/composition sample:** Select two or more genuinely different model families with matched controls; freeze separately from their scientific execution; run, verify, interpret and push. If all candidate models reduce to prior grammar, record the reduction and choose an alternative rather than pretending novelty.

**Stage 4 — Effective dynamics / interface propagation:** Explore mathematically valid quotient and finite-horizon comparisons under the new model families, retaining negative and undefined cases. Use a separate freeze for any scientific round.

**Stage 5 — Independent elementary inquiry:** Choose one unrelated, diverse and bounded elementary constraint region, only if it contributes new coverage. Freeze and verify separately.

**Stage 6 — Cross-atlas synthesis:** Update living idea, coverage, question, equivalence and crosswalk records; preserve strict distinctions between mathematical fact, experimental observation, implementation result, interpretation and ontology.

No minimum number of new rounds or cells is imposed. These stages are not permission to abandon the other research portfolios; balance breadth and depth. Stop at a coherent checkpoint when more work would be redundant or computationally unjustified.

## 9. Reporting and handoff

After each independently meaningful stage, update `PROGRESS.md`, commit and push. At the end report:

- Actual starting SHA, latest branch SHA and new commit identifiers.
- Implemented versus merely proposed state/event families.
- Which models reduce to the old single-toggle grammar and under what exact scope.
- New semantic version/method identifier, if introduced.
- Frozen plan(s), plan hashes, execution results and verified cell counts, if any.
- Numerical observations with exact fractions where practical, and explicit invalid/undefined cases.
- Mathematical identities, counterexamples, limitations and established-theorem connections.
- Correctly scoped coverage status, with broad unfinished questions still open.
- How to resume without repeating work; any pending worktree changes or unpushed commits.

Keep preflight tests, scientific cells and interpretive claims separate. Do not overstate completion or experimental novelty.

### Governing principle

**Investigate how relationships may participate in further relationships, including changing relational state, shared interfaces and non-elementary event structures, without predetermining whether any such process yields autonomous higher-order dynamics, recursion or complexity growth.**

Different mathematical constructions may be equivalent, independent, reducible, dynamically distinct, trivial or undefined. All these outcomes belong in the atlas.

**Begin with a fresh repository audit. Carry out the next justified, verified and recoverable research increments now.**
