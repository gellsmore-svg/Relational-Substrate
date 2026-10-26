# RRC — Open-Thetical Research: Adaptive Relational Interfaces
**Created:** 26 October 2026
**Target:** `gellsmore-svg/Relational-Substrate`, branch `research/recursive-relational-complexity`
**Workspace:** `relational-complexity/`
**Authority:** `research-methods/open-thetical-research.md`, the RRC charter, and the live research journal
**Type:** Autonomous next-cycle research prompt. **Not** a frozen experiment, preset theorem, or compulsory task list.

## Governing purpose

Continue Recursive Relational Complexity (RRC) as **open-thetical mathematical exploration**.

The accepted research has progressed from exact representations and XOR-update recodings to a typed, reapplicable composition of weighted labelled transition systems, and then to an exact characterization of what a component abstraction must preserve to remain predictive under **every allowed partner in one fixed interaction class**.

The latest result shows that, with a **fixed handshake alphabet H**, product-of-weights synchronization, private interleaving, final-only normalization, full partner-state observation and allowed private calibration events, the following are equivalent:

- Shared-label raw weight-to-observation-block vectors plus the single aggregate private-weight vector are constant inside each observed source block.
- The product observation remains strongly lumpable for every finite partner in that specified class.
- A particular finite family of at most three-state calibrated partners distinguishes every failure.

This is valid mathematics within a declared formalism, not a physical result, a classification of all possible interactions, or an assertion that every interface must behave that way.

**Our open question is deeper: what happens when relationships between relational systems can themselves change, and how do we know whether such changes are substantive rather than new descriptions of familiar state?**

Treat that as a research motivation, not an outcome to force.

A changing interface, new structural coordinate, recursive composition, dynamical influence, new primitive, emergence or irreducibility must be *defined* before it can be claimed. Reductions to known representations are valuable. A genuine counterexample is valuable. An impossibility under explicit assumptions is valuable. No universal result is required.

**Choose one coherent, valuable increment after auditing the evidence.** Do not run every optional line of inquiry merely because it appears here.

---

## 1. Audit the actual checkpoint before choosing

Last verified pushed branch HEAD at prompt creation:
`24df50cf50d3ee07c41689bdea402680ce16b3a1`
(`research: record the published contextual-preservation handoff`).

**Resolve live HEAD.** Check branch, worktree, current remote state, local uncommitted files, newer reports and CI. This SHA is a historical checkpoint, not permission to reset, rewrite or force-push.

Read at least:

- `PROGRESS.md`, `charter.md`, `README.md`, `docs/atlas-charter.md`, `docs/atlas-crosswalk.md`.
- The governing Open-Thetical Research method and live idea, question, coverage, pattern, equivalence, finding and relation registers in `atlas/` and `coherence/`.
- `reports/2026-10-26-contextual-preservation.md`, `docs/contextual-preservation.md`, `docs/2026-10-26-context-selection.md`, and the saved independent proof checks.
- `reports/2026-10-26-sync-composition.md`, `docs/labelled-sync-composition.md`, plus the earlier XOR and Atlas-018 analyses.
- `docs/composition-taxonomy.md`, `docs/composition-operators.md`, `docs/state-event-families.md`, `docs/coupled-models.md`, `docs/event-semantics.md`, `docs/representations.md`, `docs/cover-observations.md`, `docs/compilation-gate.md`.
- The relevant `src/rrc/` engine and verification implementation, tests, and the existing deferred-plan decision log at `prompts/2026-10-26-otr-handoff/FROZEN-PLAN-DISPOSITION.md`.

At this historical checkpoint:
- **218 committed verified atlas cells** (through Atlas-018), excluding 15 old Atlas-007 failures.
- Latest increment was **analytical**, with **zero new scientific atlas cells** and **223 passing local tests**; subsequent CI for the research and handoff commits was successful.
- Established analyses have separate identifiers (including `label-sync-analysis-0.1.0`, `context-probe-analysis-0.1.0`); engine `rrc-0.4.0` and legacy event-kernel methods retain their original semantics.
- **Atlas-019 and Atlas-020** remain **frozen, deferred and unadopted**. Previously generated local results may exist but are not automatically adopted or scheduled. Preserve plans and output bytes without alteration; reselect independently only if scientifically worthwhile.
- Broad coverage questions remain open, despite several exact analytic findings.

Use the *current* facts from Git, not these potentially stale counts, if anything has moved.

---

## 2. Meaningful distinctions not to collapse

Keep these categories separate for any new work.

**Relational structure:** the objects, typed constituent relationships, boundary ports/interfaces, constraints and which systems can be composed.

**Declared dynamic state:** configurations that the model allows to vary independently. An "interface-state" variable is not a new entity merely because it has a different name.

**Derived description:** an interface label, graph, cover, relation-count or grouping calculated as a function of constituent state; this may add no independent state.

**Interaction operator:** what new valid state space and event law results when constituents are connected, identified, synchronized, constrained or jointly updated.

**Evolving interface:** a *specified state-changing rule* for an interface, attachment, shared label set, membership relation or coupling constraint, with a precise event clock and valid transition law.

**Observations and equivalences:** original constituent states, shared/duplicated ports, labelled events, raw weights, kernel conjugacies, graph/carrier isomorphisms, strong lumpability, observational/contextual equivalence and changing-clock equivalence are **not interchangeable**.

**Consequentiality:** retaining a distinction matters *relative to a declared prediction or interaction*, not because a new symbol has appeared. Determine which changes survive relabelling, coordinate recoding, state augmentation or quotienting, at a specified clock and allowed model class.

**Ontological interpretation:** Relational Substrate and Transmit–Carry–Receive motivate the investigation. Finite mathematical examples do not confirm them or disconfirm them.

If comparing systems, state the permitted mappings and what meaning those mappings preserve. If the current engine grammar simply encodes a new model as an extra bit, report that representation and its limits rather than automatically calling it "irreducible".

---

## 3. Candidate investigative directions — choose freely

### A. A genuinely stateful interface between relational systems

Investigate whether a *typed* interface that changes can be constructed so the result is a valid transition system and can participate in further composition.

Potential alternatives:

- **State identification versus synchronization:** a common interface variable shared by two components, contrasted with independently stored copies that are synchronized or conditionally constrained. Explicitly define admissible pairs, consistency restrictions and transitions.
- **Changing link or membership:** a relation or constituent moves between composites; an interface connection is formed, dissolved or reassigned; a block-family is part of state rather than a static cover.
- **Dynamic handshake permissions:** the allowed shared labels depend on current interface/membership state. Distinguish an actual changing handshake relation from fixed H with state-dependent zero event weights.
- **Interface-mediated dynamics:** an interface has its own transitions or affects which component events can occur. Include fixed-interface, independent-interface and reducible-label controls.
- **Iterated composition:** a composed system interacts again, with explicit boundary inheritance, event ownership and reapplication rules. Associativity may fail for a chosen dynamic interface; do not assert it without proof, nor manufacture failure by silently changing clocks.

For every construction, specify:
1. Input and output types and state spaces;
2. Valid states/compatibility constraints;
3. Whether interface state is derived or independently selectable;
4. Allowed event kinds, labels, updates and ordering;
5. Raw weights and zero/halt semantics;
6. Time/observation clock;
7. Projections and intended measurable distinctions;
8. Whether and how output is legitimately recomposed.

Merely drawing relations between boxes, renaming a transition, or assuming a bit is autonomous does not meet this standard. Conversely, a precise demonstration that a proposed mechanism reduces to a conventional product automaton may settle an important ambiguity.

### B. Contextual equivalence when interaction assumptions change

The last theorem assumes **fixed H**, a partner state visible in full, state-only observation, raw weighted handshake products and private calibration availability.

Explore one independently chosen alteration (or a compact family of meaningful contrasts):

- H itself varies as part of state or during composition.
- The observer sees emitted event labels as well as destination states.
- Partners have restricted capabilities, e.g. no private competing events; determine whether raw-weight calibration remains necessary.
- Some partner state is also hidden/quotiented rather than observed in full.
- Interfaces impose state compatibility constraints rather than synchronizing labels alone.
- Normalization/clock choices change; local normalization followed by composition need not equal final-only global normalization.
- Some event labels are converted between private and shared, changing which previous abstractions remain safe.

Ask whether a previous component abstraction is preserved, invalidated or can be repaired by retaining a **minimal declared addition** of information. If "minimal" is claimed, specify a partial order on observations/signatures and prove or bound minimality; don't assert it because an example uses one extra coordinate.

Avoid re-proving the existing `1+|H|` probe theorem or merely testing a longer fixture list. A different class must be formally different and the new result must explain something not settled in the prior work.

### C. Compositional memory and predictive closure

Consider dynamic interfaces or coupled hidden state where observation is not strongly lumpable. Carefully separate:

- First-order strong Markov closure (uniform across all microstates);
- Closure under a chosen initial distribution;
- Higher-order history-dependent description or belief state;
- A finite memory augmentation restoring exact prediction, if one exists;
- Event-label visibility, private clock events and raw-weight effects;
- Dependency, reachable effects and actual interventions.

Test whether *one extra relational coordinate* is meaningful or merely the original hidden state copied. A truly information-saving model must define a comparison to the full system and preserve the specified predictive observable.

If introducing a causal intervention, declare the operator and controls first; do not infer causal influence from a static dependency graph or transition reachability.

### D. Alternative operators and independent atlas coverage

If the most valuable inquiry is not stateful-interface construction, examine independent composition instruments or the unfinished elementary constraint programme. Examples: graph/hypergraph gluing, pushout-style carrier identification **with separately defined transition semantics**, disjoint/overlapping covers, constraint formation/dissolution, guarded event synchronizations, and relational systems with different classes of admissible partners.

Established mathematics — weighted automata, process algebra, synchronization networks, categorical composition, state-dependent Markov chains, bisimulation, lumpability and graph rewriting — should be used as **precedent and challenge**, not disguised as new universal theorems. Identify when a categorical or algebraic identity is *merely formal* and when it actually constrains dynamics.

Atlas-019 and Atlas-020 remain optional: a valid earlier local result can be independently verified and adopted unchanged if *reselected on research merit*. If unselected, leave both untouched and deferred.

### E. Cross-atlas synthesis / stopping

If the most informative next increment is analytical consolidation rather than a new model, derive or falsify a precise relationship among already verified facts, documenting the scope and any counterexample. A rigorous impossibility/representation boundary with independent checks can complete a coherent increment.

Do not schedule a computational experiment merely to create a new cell count or satisfy an arbitrary research quota.

---

## 4. OTR selection: choose for information value

Before implementation or experiment, briefly assess materially different candidate questions on the five independent vectors:

- **Consequence:** what meaningful mathematical alternatives would the inquiry separate?
- **Readiness:** are the types, mathematical checks, nulls, controls and failure conditions defined?
- **Leverage:** how does it change understanding of relationships participating in further relationships?
- **Cognitive/computational cost:** can it be finished in a bounded recoverable increment within available model credits?
- **Personal/research significance:** does it serve RRC rather than convenient numerical curiosities?

These are qualitative evaluation dimensions, **not a numeric score**. Record a concise rationale and alternatives deferred. Choose a question whose negative result is informative as well as its positive result.

No mandatory experimental portfolio. No preference for increasing recursion depth. No predetermined ratios, defects, invariants, number of nodes, "emergence" or integer. Preserve independence of scientific selection from measured outcomes.

A research increment is **complete** when it provides a precise answer, scoped limitation, theorem, verified construction or counterexample; challenges it independently; integrates the findings and leaves a reproducible record. Method scaffolding, untested fixtures or frozen-but-unrun experiments alone are not a completed scientific round.

If resources or credits interrupt before completion, record that **resource blocker** and a restart point; do not claim that scientific optionality explains the interruption.

---

## 5. Evidence, scientific freeze, provenance and verification

For any chosen **analytic** investigation:
- Write formal objects, quantifiers, clocks, observational equivalences and assumptions.
- Supply direct reasoning/proof for claimed generality. Finite computational examples are **software validation and controls**, not evidence for an unproved universal claim.
- Test meaningful positive, negative, null and reducible boundaries with an independent algorithm or exact rational calculation, ideally not importing the RRC production implementation.
- If a classical theorem handles the situation, cite it accurately and explain RRC's specific construction or limitation without announcing mathematical novelty.
- Give any changed operator or analysis method a new clearly scoped identifier, leaving existing method semantics untouched.
- Preserve exact reported failure cases and never fill undefined quotient rows.

For any chosen **scientific experimental** round:
1. Declare state grammar, event rules, controls, initial distributions where relevant, clock, observations, success/failure definitions, selection/stopping rule and resource bounds *before results*.
2. Use a disposable **end-to-end worker preflight** with actual schema, serialization, hash/receipt checks, interruption and recovery. Discard preflight scientific observables.
3. **Commit and push an immutable new plan** before executing any scientific cell. Never alter its items, weights, exclusions or interpretation after seeing results.
4. Use independent recoverable tasks, ordinary watchdog **120 s**, hard per-indivisible-work ceiling **300 s**, and short bounded invocation budgets. Prefer exact small systems.
5. Run frozen items only; preserve failed, timed-out, invalid and pending records honestly.
6. Independently check mathematical outputs, challenge conclusions, publish separate execution/verification commits, and update the registers and journal accurately.

Do not alter frozen plans/preflights/results through Atlas-020, historical failure records, old method identifiers, or other research programmes. Use the established shared-coherence integration process before touching cross-programme authority, books or ontology documents.

Existing Atlas-019/020 **local untracked outputs** are not newly run science. If reselected, audit original input, plan, freeze-first chronology, manifest, receipts, bytes, execution provenance and exact mathematical content before adoption. Preserve valid evidence instead of rerunning reflexively. If no such selection is made, don't promote those outputs to committed scientific findings.

---

## 6. Handoff and acceptance contract

On completing one independently chosen meaningful increment:

- Identify starting live SHA, selected mathematical question, OTR rationale, alternatives considered and exact result scope.
- Supply an actual proof or logically adequate independently checked evidence — not simply a proposal, method type or preflight.
- Separate established mathematics, this programme's constructed result, software fixtures, formally frozen scientific outputs, interpretive inferences and ontological motivation.
- Specify under which model/clock/observer/interface mapping any distinctions survive or collapse.
- Show independent verification, tests and CI **as actually observed**, disclosing pending or failed runs accurately.
- Commit/push completed artifacts, update `PROGRESS.md`, crosswalk and appropriate append-only idea/coverage/equivalence/pattern/finding/relation records without falsifying the old history.
- Preserve and explicitly describe deferred Atlas-019/020 status and any local evidence, or justify an independent new disposition without editing frozen files.
- Give ending pushed SHA and a precise next restart point. Name possible future inquiries without making them mandatory.
- Do not claim all RRC questions are closed because one defined mathematical model has a theorem.

**Governing question:** *When the relationship between relational systems can itself change, what is genuinely new about the resulting dynamics, what is representationally reducible, and what information must remain available for later interactions?*

Treat this as an open mathematical investigation, not a result to be manufactured.

**Audit live HEAD. Select the next question independently. Complete a coherent and verified increment. Commit, push and leave a truthful handoff.**