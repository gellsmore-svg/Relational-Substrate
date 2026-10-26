# Recursive Relational Complexity — Next Open-Thetical Research Cycle
**Created:** 26 October 2026  
**Audience:** Any research-capable CLI agent/model continuing RRC  
**Status:** Research handoff and selection framework — **not** a frozen scientific plan or a prescribed list of experiments.  
**Repository:** `gellsmore-svg/Relational-Substrate`  
**Branch:** `research/recursive-relational-complexity`  
**RRC root:** `relational-complexity/`  
**Research method:** `research-methods/open-thetical-research.md`

## Mission

Continue the **Recursive Relational Complexity and Structural Composition (RRC)** programme through independently selected, mathematically rigorous, recoverable increments. Seek a better understanding of what relational composition and interaction **can and cannot** preserve, change, encode or generate.

The accepted Atlas-018 result supplies a particularly useful point of departure: two copies of a shared interface can preserve the identified dynamics under a coupled update, yet fail to preserve them under independent updates. In the tested coupled model, an exact invertible XOR recoding changes the apparent two-coordinate joint event into ordinary toggles plus a frozen disagreement coordinate.

This is **a concrete result about a finite declared transition law**, not proof that all higher-order dynamics reduce, that other couplings cannot generate new capabilities, or that the Relational Substrate (RS) ontology is verified.

**Your task is not to disprove that recoding or prove emergence.** Investigate independently worthwhile questions across the mathematical possibility space. Contradictions to a conjecture, reductions to existing constructions, inability to form a quotient, and null effects are useful findings. No preferred hierarchy, level count, state size, event form or complexity trajectory is assumed.

This prompt governs the **next useful research increment**, not completion of the entire programme. Do not treat its candidate avenues as checkboxes or any number of completed atlas cells as a success target.

---

## 1. First action: audit the live repository, recover actual status

The last reviewed remote branch HEAD before this prompt was
`84135b589c4cfd85191c91afbb2d806cc29b3fbb`
(26 October 2026, recording the published Atlas-018 recovery handoff).

**Checkpoint only.** Resolve current HEAD, local uncommitted files, active branches and any newer published results. Do not reset, force-push, overwrite another agent's work or presume the above SHA remains the latest.

At that checkpoint:

- **Atlas-018** was accepted as a **completed recovered research increment**, with three original results independently checked and committed; it was **not** rerun in the recovery session.
- **218 verified scientific atlas cells** were committed cumulatively. The 15 historical failed Atlas-007 items remain excluded.
- The independent Atlas-018 checker examined **576 exact probability entries** and stored input/result/receipt evidence. The recorded RRC test suite passed **177 tests**, and CI for the substantive research commit completed successfully.
- Method `event-kernel-0.2.0` provided strict labelled event semantics. Frozen Atlas-017 remains on `event-kernel-0.1.0`; do not rewrite or implicitly upgrade historical results.
- **Atlas-019** (finite-horizon observations) and **Atlas-020** (elementary form/dissolve grammar) were frozen and preflighted by the prior session. Their local outputs were found but intentionally **left unadopted and uncommitted**. They remain **deferred**, not failed, cancelled, scientifically unimportant or required next. Retain them unchanged until an independent OTR selection makes their value clear.
- All fifteen broad atlas questions and major uncovered regions remain open; `COV-INTERFACE-INVARIANCE-SAMPLE` records only a **partial** sample.

Confirm all of this against the **live** repository rather than treating this text as authoritative.

Read at least:

- `PROGRESS.md`, `charter.md`, `README.md`, `docs/atlas-charter.md`, `docs/atlas-crosswalk.md`.
- `research-methods/open-thetical-research.md` and the living RRC registers under `atlas/` and `coherence/`.
- `reports/atlas-018-observations.md`, `reports/atlas-018.md`, `provenance/atlas-018-execution.md`, `provenance/atlas-018-independent-verification.json`, and `docs/2026-10-26-otr-selection.md`.
- `docs/compilation-gate.md`, `docs/composition-taxonomy.md`, `docs/composition-operators.md`, `docs/representations.md`, `docs/cover-observations.md`, `docs/state-event-families.md`, `docs/event-semantics.md`, `docs/event-kernel.md`, `docs/coupled-models.md`.
- `src/rrc/event_kernel.py`, `src/rrc/coupled_models.py`, `src/rrc/composition.py`, `src/rrc/items.py`, `src/rrc/cli.py`, the scientific-runner and verification code and tests.
- `prompts/2026-10-26-otr-handoff/README.md` and its `FROZEN-PLAN-DISPOSITION.md` for the binding **historical disposition**, not as instructions requiring deferred experiments.

Do not rewrite the frozen plans, preflights, completed results or historic failures. Keep other research programmes, central synthesis and books outside direct modification unless the established integration process authorises it.

---

## 2. Research question: what is an actual dynamical distinction?

Atlas-018 demonstrated a mathematically precise change of coordinate:

`F(y0, a, b, y3) = (y0, a, y3, d)`, where `d = a XOR b`.

Under the **specific frozen coupled transition law**, `d` stays fixed while the other three recoded coordinates toggle with the stated probabilities. The original coupled law is conjugate to three ordinary toggles together with a frozen disagreement bit. There is an exact eight-state quotient that drops `d`.

This result motivates—not dictates—several distinct mathematical questions:

1. Which *specified* properties of an event grammar survive an **invertible state recoding**, and which depend on the chosen coordinate system?
2. Under what assumptions does a **global state transformation** turn a purported joint update into independent or conditionally coupled single-coordinate updates?
3. When do the **observable effective dynamics** close under a noninjective projection, and when does hidden state or past history remain consequential?
4. How does a **shared relational interface** compare with two copies under independent, constrained, synchronised and state-dependent updates?
5. Can changing relational membership or relations between composites be modelled with a semantically meaningful typed operator beyond simply relabelling listed bits?
6. Does a candidate distinction persist after allowing alternative state encodings, event labels, clocks and intermediate states—or does it reduce under a precisely scoped equivalence?
7. Which behaviours are captured by known mathematical structures and theorems (e.g. finite Markov-chain conjugacy, strong lumpability, stochastic bisimulation, product automata and graph/hypergraph transformation)?

Do **not** turn these into claims about primitive physical ontology. Also do **not** define a universal impossibility claim just because a transition fails the current one-bit, one-step compilation gate. The scope of every representability statement must specify the permitted state mappings, number of states, clock, event syntax and observable semantics.

An analytic theorem for a clearly bounded family, an exact counterexample, an impossibility under explicit assumptions, and a positive construction all have potential value.

---

## 3. Independent portfolio choices (examples, not required stages)

### Portfolio A — When exact recoding succeeds, fails or changes what is observable

Study a **principled** set of small finite transition systems, ideally with several independently selected structural families rather than a single formula tuned until the Atlas-018 recoding fails.

Possible dimensions include:
- State-dependent rates or prohibitions that couple disagreement with constituent updates.
- A copy-update rule whose event support is state-dependent rather than globally uniform.
- A genuinely simultaneous update and its relation to any allowed recoding under fixed clock/state size.
- An invariant disagreement coordinate versus an evolving one.
- Invariant agreement images versus images from which transition mass leaks.
- Similar aggregate Markov kernels with different event identities.

Compare **multiple equivalence notions**, never conflating them:

- Same integer event-weight table (where defined).
- Same normalised Markov kernel on the same named states.
- Kernel conjugacy by a named bijection.
- Coordinate **permutation** versus non-coordinate state recoding (such as XOR).
- Carrier automorphism preserving the original relational semantics.
- Exact projection/strong lumpability by an observation.
- Event-labelled equivalence, which requires a correspondence of event identities/kinds.
- Equality after changing the observation clock or adding intermediate states, with that change disclosed.

A failure under one equivalence notion does not establish failure under all of them. A recoding that removes a simultaneous step at kernel level may still change original relational and event semantics.

Do not choose parameter values to engineer a desired counterexample to EQ-033; choose meaningful contrasting model families and retain reducible, exact, null and nonexact outcomes.

### Portfolio B — Compositional descriptions that retain or lose causal-relevant information

Explore relational systems composed from components or overlapping subcollections. Distinguish:

- A fixed descriptive graph/cover of relations.
- A realised overlap dependent on currently present constituents.
- A block family or interface that **changes as part of the state**.
- An additional independently selectable state coordinate.
- A derived label or count `H=f(X)` that adds no state.
- A quotient process with exact closed Markov dynamics.
- An observed process without first-order Markov closure.

Consider one or more compositional operations **only if** input/output types are precise and the result allows further well-defined composition.

The programme seeks to understand how relations between relational systems **can matter dynamically**. Do not silently interpret state-labelled derived overlaps as independently existing higher-order agents. Conversely, do not exclude a new state grammar by definition: specify it and test whether its explanatory distinctions survive appropriate reductions.

A useful exact result could identify necessary/sufficient conditions for closure in a bounded family or a minimal counterexample to an assumed correspondence.

### Portfolio C — Successive observation, finite-horizon influence and memory

RRC has studied exact successive quotient conditions on a four-cycle. The deeper question remains open: how do relational interactions affect which descriptions retain enough state for predicting change?

Potentially useful independent tests:
- Strong lumpability under original law versus a separately specified coupled law.
- Two genuinely nontrivial exact quotient stages, if they arise under a fair selection scheme.
- A direct coarse quotient that exists despite a non-Markov intermediate observation.
- Hidden-state dependence of projected dynamics.
- Event-labelled differences even when aggregate kernels agree.
- Finite-horizon changes under **predeclared** initial-state perturbation or matched alteration of a transition rule.

For finite-horizon comparisons define the source state/distribution, observables, contrast, clock, horizon and null baseline **before** looking at resulting fractions. Report zero as zero; do not select a preferred propagation depth.

A dependency digraph, observational correlation or ability to reach a state does **not** establish an intervention or cascade. Causal language requires a genuinely specified intervention with transparent assumptions. No intervention is currently required.

Distinguish exact strong lumpability from weaker/initial-distribution-specific phenomena; a positive defect yields **no exact first-order quotient** under that definition.

### Portfolio D — Independent elementary constraints and structural representations

Keep an avenue for independent elementary constraint research when its expected value is high, especially if the coupled-system track becomes too close to confirming its own modelling choices.

Possible questions include formation versus dissolution, guard expressivity, support versus rate changes, constraint interaction/redundancy and carrier geometry; these are opportunities, not assignments.

Preserve comparisons of weight tables, normalised kernels, support, recurrence, occupation (including nonunique cases), and structural observables. In particular, an identical bit-position weight table need not imply equal carrier-based graph structure.

Atlas-020 is available as a **frozen, unadopted** form/dissolve sample. Select it only on information value. If reselected, verify the original local records independently and adopt them *unchanged* if valid; otherwise preserve status and decide according to the existing recovery contract. Never recalculate the same records merely to claim new execution.

### Portfolio E — Cross-atlas synthesis and mathematical precedents

Seek relationships among already verified results before generating more of the same kind. Identify:
- Exact mathematical identities and their assumptions.
- Counterexamples and failures of attempted equivalences.
- Already known mathematical principles that explain multiple atlas results.
- Representation-dependent artefacts and redundant experimental families.
- Genuine unexamined regions with independently stated selection criteria.

Do not label a known theorem a new mathematical discovery. Do not combine different equality notions into one vague measure of 'relational complexity'. Maintain separately the mathematical, numerical, interpretive, RS and theological layers required by the RRC charter.

---

## 4. OTR decision: what is worth doing *next*?

At the end of orientation, pick **one coherent next inquiry or a compact diverse combination** based on information value, not proximity to an old frozen plan.

Use the established qualitative evaluation vectors:
1. **Consequence:** Which important mathematical alternatives can the work separate?
2. **Readiness:** Are its objects, calculations and falsification tests actually defined?
3. **Leverage:** How does it inform other open inquiries without relying on a favoured result?
4. **Cognitive/computational cost:** Is the expected gain worth the effort and available model credits?
5. **Personal/research significance:** Does it serve the core relational composition inquiry?

No numerical score or forced rank is required. Record alternatives considered and the reason for selection.

**A completed increment can consist of rigorous analytic work plus independent checks, a verified frozen experimental round, or another coherent mathematical advance.** You need not run every portfolio. If an initially selected model proves reducible by inspection, log the reduction and either investigate a new information-rich question or stop with a clearly justified completed analytical increment.

However, distinguish:
- **Method preparation complete** (implementation / tests / typed fixtures).
- **Research increment complete** (a defined question answered and verified; interpretation and register updated).
- **Frozen experimental round complete** (selected immutable items *actually* executed or valid earlier results explicitly recovered, checked and adopted).
- **Programme complete** (not asserted by this task).

If credits or tool access end, preserve the checkpoint and state **resource-blocked / incomplete** rather than invoking scientific optionality as an explanation for work that simply did not finish.

---

## 5. Validation, freeze, recovery and publication

For each **selected scientific calculation**, and only when scientific computation is warranted:

1. State formal objects and types, state space, laws and event semantics, event weights, clock, observation maps and candidate equivalences.
2. Declare a bounded selection/contrast with positive, negative, null and reducible possibilities; keep controls independent of output values.
3. Prefer exact rational enumeration where tractable; use an independent validator, hand derivation or separate code path. Challenge your own expected interpretation.
4. Preflight the **actual worker and verifier** in a disposable workspace, including schema, receipts, hashes, crash/resume behaviour and result status. Discard preflight scientific observables.
5. **Freeze, commit and push** the immutable plan before any selected scientific item runs. Do not add/remove cells, broaden tolerances, rewrite weights or change semantics after seeing results.
6. Run deterministic independent items with the ordinary **120-second watchdog**, hard ceiling **300 seconds per indivisible task**, and short recoverable invocation budgets; do not launch long monolithic calculations.
7. Persist exact pass/fail/timeout/invalid/unrun states, verify scientific results, interpret alternative explanations, and **commit/push execution records** separately from the freeze.
8. Record independent verification and result provenance. Existing uncommitted local results are **not new executions**: verify input/plan compatibility, origin, bytes, and full mathematical contents before adopting them. Preserve valid evidence rather than rerunning reflexively.
9. Update `PROGRESS.md`, coverage/ideas/patterns/equivalences and crosswalk accurately; keep broad questions open unless supported by genuinely comprehensive grounds.

Do not edit or replace historical Atlas-001–020 frozen plans, preflight files or completed result bytes, including the original failed Atlas-007 items. If a prior frozen plan becomes scientifically unhelpful, record `retired-unexecuted` or `superseded-unexecuted` in a **separate append-only disposition record** with mathematical reasons. Credit exhaustion is not such a reason.

If selecting one of the deferred Atlas-019/020 plans, **preserve and reassess** any existing local results and provenance; do not relabel preflight as science or commit unverified files. The RRC charter's model/experiment distinction and immutable freezes still apply.

Restrict code changes to the authorised RRC programme. New representations or method semantics require a different method identifier and explicit compatibility boundary. Do not silently change the existing `rrc-0.4.0` or `event-kernel-0.1.0` historical interpretation.

---

## 6. Final report and restart

When a coherent increment is finished:

- Report **actual starting HEAD and ending pushed SHA**, with commit subjects and evidence paths.
- State the **question chosen** and a short information-value rationale, plus important alternatives deliberately not selected.
- Distinguish analytic proof, independently checked fixture, preflight, frozen-plan execution, verified scientific cell, and interpretive inference.
- State exact numerical/structural findings **within scope** and which claims reduce under explicit changes of representation or clock.
- Provide the status and provenance of **Atlas-019 and Atlas-020** (still deferred unless independently reselected), without inventing results or clearing their historical freezes.
- Report result hashes/plan hashes/counts for any newly adopted experiment, test suite and CI status when available.
- Update the journal and relevant living registers, keeping all unresolved broad questions honest.
- Identify **one or several possible next mathematical inquiries**, without imposing them on the next model. Name the exact restart location.

A clear, verified increment with one substantive result is better than many redundant cells or a long list of unfinished plans. A credible mathematical limitation is as valuable as a compatible construction when it distinguishes possible explanations.

### Final research principle

**Relations can be described, grouped, carried across interfaces, made conditional on other relations and composed into further dynamical systems. The question is what these constructions actually entail under stated mathematical assumptions—not what the programme hopes they will entail.**

Stay curious about possibilities the current grammar does not represent; stay rigorous about reductions the grammar already admits. Treat ontology and design as research motivations, not evidence manufactured by finite computation.

**Audit the live repo. Select for information. Complete and verify a worthwhile increment. Commit, push and leave a precise recovery point.**
