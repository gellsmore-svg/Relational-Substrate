# RRC — Context, interfaces, and dynamically consequential relationships
**Created:** 26 October 2026  
**Audience:** A research-capable CLI model or agent continuing Recursive Relational Complexity (RRC)  
**Status:** Autonomous Open-Thetical Research (OTR) **guidance**, not a frozen plan, scientific result, compulsory experimental menu, or requirement to produce a particular conclusion  
**Repository:** `gellsmore-svg/Relational-Substrate`  
**Branch:** `research/recursive-relational-complexity`  
**Working directory:** `relational-complexity/`  
**Research method:** `research-methods/open-thetical-research.md`

## 0. Core purpose

Continue investigating **how relationships between relational systems alter what can happen, what can be predicted, and which distinctions need to be retained**.

The last accepted RRC increment gave us something more than another state recoding: a **typed, reapplicable event-synchronisation composition**. It showed that a description that perfectly predicts a component in isolation may fail when that component interacts with another system. The missing information can be **event-label distinctions or raw relative weights**. A stronger labelwise weighted block-sum condition is sufficient for reduction and this particular composition to commute, but it is not necessary for one fixed interacting partner.

The question now is **which further mathematical distinctions deserve investigation**, without making the previous example into a universal mechanism or the next result into a confirmation exercise.

Explore possibilities in which a relation between two relational systems actually participates in determining transitions, where interfaces or memberships evolve, or where a system's effective dynamics depend on context. A precise negative, reduction, limited congruence theorem, alternate composition instrument, or formal type boundary may be as important as a positive construction.

**Do not pursue a preferred hierarchy, number of levels, emergence claim, recursion depth, cascade, ontology or physical parameter.** Relational Substrate (RS) and Transmit–Carry–Receive (TCR) are upstream motivations, **not** conclusions to be established by exact finite-state mathematical models.

**You have discretion to select the next worthwhile research inquiry.** Not all choices below are required. Avoid padding research with model variations that merely repeat established examples.

---

## 1. Mandatory live orientation and provenance

Check the **current GitHub branch HEAD and actual worktree** before acting. At prompt creation the last reviewed pushed HEAD is:

`3a0af2269e7efb296a3bfec97d66a66026f40aa0`  
`research: record the published synchronization-analysis handoff`

This is a provenance checkpoint, **not a reset or checkout target**. Inspect for newer commits, untracked outputs and local work. Do not overwrite, reset or force-push another session's changes. If the intended inquiry has already been completed, choose a different one.

Read and cross-check:

- `PROGRESS.md`, `charter.md`, `README.md`, `docs/atlas-charter.md`, `docs/atlas-crosswalk.md`, OTR research-method instructions, and all relevant living `atlas/` and `coherence/` registers.
- **Latest completed research:** `reports/2026-10-26-sync-composition.md`, `docs/labelled-sync-composition.md`, `docs/2026-10-26-sync-selection.md`, `provenance/2026-10-26-sync-verification.json`, `provenance/label-sync-analysis-check.py`, and tests.
- Earlier foundation: `reports/2026-10-26-xor-recoding.md`, `docs/xor-mask-recoding.md`, `reports/atlas-018-observations.md`, independent verification, method/version notes, and composition taxonomy.
- Implementation boundaries in `src/rrc/` and tests; `docs/event-semantics.md`, `docs/coupled-models.md`, `docs/state-event-families.md`, `docs/composition-operators.md`, `docs/representations.md`, `docs/cover-observations.md`, and `docs/compilation-gate.md`.
- The previous `prompts/2026-10-26-otr-handoff/FROZEN-PLAN-DISPOSITION.md` and newer journal sections for the frozen but deferred Atlas-019 and Atlas-020.

At the checked checkpoint:

- **218 committed, verified atlas cells** through accepted Atlas-018, with 15 historical failed Atlas-007 items **excluded**.
- Two following analytical increments (XOR recoding/predictive closure and labelled synchronising composition) were accepted as coherent mathematical research, **not** frozen atlas experiment rounds. Do not inflate the scientific count with proof checks or software fixtures.
- The reported complete RRC test suite passed **204 tests** at the latest research commit, and CI subsequently completed successfully.
- `label-sync-analysis-0.1.0` is **analysis-only**, and the original `rrc-0.4.0`, `event-kernel-0.1.0`, and `event-kernel-0.2.0` semantics remain unchanged.
- Atlas-019 and Atlas-020 have immutable frozen plans and previously found uncommitted local output. **They are deferred and unadopted**, not failed or required as the next experiment. Preserve bytes and decision history; no automatic reexecution, adoption or cancellation.
- Broad atlas questions and large coverage areas remain open. Any new statement about closure requires evidence beyond one tractable constructed example.

Always prefer live evidence over this historical text.

## 2. What the previous increment actually established

A component is a finite weighted *labelled* transition system with nonnegative integer raw event weights and a fixed handshake alphabet `H`.

One explicitly declared **composition instrument**:

- Shared-label events synchronize; their raw event weights multiply.
- Private-label events interleave with the other component's state held fixed.
- The composed state is a Cartesian pair.
- Only the **final global-event row** is normalized into transition probabilities.
- An empty event row halts as an implicit self-loop **without adding an event**.
- The composed weighted-labelled output may be composed again under the **same fixed `H`**.

For this specified operation, the published work proves associativity after Cartesian reassociation, a one-state shared-loop identity (not the same as halt), failure of isolated Markov equivalence to guarantee equivalence under interaction, and a **sufficient** preservation contract: equal raw labelled outgoing block weights across each observed source block.

The important distinction is:

> **Having a correct closed description in isolation is weaker than having a description that remains valid when the system participates in another relationship.**

**Do not re-prove the same theorem with larger or differently numbered fixtures.** Do not turn this one fixed product-weight/global-clock synchronisation policy into a universal law about composition. The published condition is not necessary for one *particular* partner; whether it becomes necessary under an appropriately rich class of contexts is a different, quantifier-sensitive question.

Preserve at least these distinct meanings:

1. Equality of standalone **normalised unlabelled kernels**.
2. Equality of normalised **labelled** transition probabilities.
3. Equality of raw **labelwise block weights** (with event identities aggregated only where justified).
4. Exact Markov lumpability of an observation of a system in isolation.
5. Preservation of the observation **in one fixed context**.
6. Preservation **uniformly for a declared class of contexts**.
7. Typed interchangeability/congruence of components under composition.
8. Identity of original constituent states/interfaces versus their Cartesian copies, quotient representations or state encodings.

The strongest of these is not automatically necessary or sufficient for the others without assumptions on contexts, clock, labels, weights, halt and observation.

---

## 3. Research portfolios — alternatives, not deliverables

### A. Contextual distinguishability and the information that composition exposes

One mathematically promising direction is to distinguish **one-context** equivalence from equivalence **under every admissible interaction**.

Potential precise questions:

- Given two states or two observations with equal standalone transition kernels, **which context labels and rates can distinguish them**, and by which observed behaviour?
- Under a stated class of partner systems, are there necessary as well as sufficient conditions for observational interchangeability?
- Can a finite family of deliberately selected *separating contexts* witness failures without enumerating every conceivable partner?
- How do restrictions on partners (only shared events; private events allowed; labels permitted; bounded state sizes) alter contextual equivalence?
- Does preserving raw labelled weights remain stronger than needed because a declared context class cannot observe some distinctions?
- When do quotient and composition commute for **a particular context**, but fail for another?

Don't assume a uniform-context theorem exists in the chosen model. State quantifiers carefully: "every finite allowed partner" is much stronger than "one selected partner" or "all partners in a bounded fixture menu".

Inspect established notions from weighted bisimulation, process algebra, observational congruence and probabilistic testing equivalence; do not rebrand classical results as new universal discoveries. A direct finite proof, valid separator or precise impossibility of a proposed equivalence can be a useful result.

A private-event "clock" in the accepted example means **an additional competing declared event**, not an experimentally observed duration or independent physical time.

### B. Relational interfaces whose identities or memberships genuinely change

The previous synchronisation product **does not** identify component interface states, revise the shared handshake alphabet, or maintain a changing relational block family.

A different next inquiry may be more valuable: define a *typed* relationship itself that can evolve while participating in the dynamics.

Candidate alternatives:

- **Interface identification:** two constituent systems possess ports/states/relations that become **one identified interface** rather than two Cartesian copies. State exactly how valid combined states, events, incompatible port values and projected observations are constructed.
- **Coupled-but-not-identified copies:** separate interface states with agreement constraints or joint updates. Compare to identified versions under matched clock and observable semantics.
- **Changing membership:** constituent relation `e` moves between named composites, or the block-family/attachment graph changes. Distinguish a static observation of existing constituents from an **additional independent membership state**.
- **Adaptive interface constraints:** admissible handshakes/transition weights depend on current interface or membership state; contrast with a fixed handshake alphabet and state-dependent zero rates.
- **Reapplicable composition:** once an interface has been formed, can it legitimately participate in the next interaction? What does associativity mean when the interface itself can change?

If a proposed additional membership state is already reducible to an existing listed bit, report that exact reduction. If it is an extra independently selectable variable, say where that independence entered the model; it was **specified**, not conjured by a new name.

Potential pitfalls:

- A quotient that identifies interface states may not preserve the dynamics unless transition consistency is proved.
- A pushout, graph quotient or merge of carriers is a **static structural operation** until its transition semantics are declared.
- Two alternative event clocks can create an apparent inequivalence not caused by relational structure.
- Changing a label on an existing state does not establish a new independent relational degree of freedom.
- Reifying a derived edge-count/overlap/cover as a primitive is a modelling choice, not a mathematical discovery.

Do not impose an allegedly canonical rule for merging or updating interfaces; compare admissible rules with explicitly typed alternatives.

### C. Different composition policies and what remains invariant

If comparison of mathematical instruments is more informative than a new state grammar, consider independent policy alternatives:

- Shared event weights multiply, take another explicitly justified combination, or are normalized locally before synchronization.
- **Handshaking versus interleaving**, with transparent competing event clocks.
- Synchronization of multiple partners at once versus explicitly binary parenthesization; explain what exactly is held fixed.
- Fixed versus evolving handshake structure, with any required membership state explicitly represented.
- Label-preserving composition versus composition that aggregates labels before joining.
- Self-loops, halt, internal/silent moves and duplicate named events as separate semantic cases.

For each declared policy, test the same suitable inputs and matched clocks whenever feasible. If policy choice produces a different answer, that's an **instrument-dependence finding**, not proof that one policy is reality.

Compare applicable precedents from weighted transition systems, stochastic process algebra and Markov-interaction theory.

### D. Prediction, finite memory and higher-order participation

A compound system can need information that was irrelevant to its constituent standalone behaviours. Examine **how much information** suffices for effective prediction under a declared interaction, but only after defining what must be predicted and for whom.

Options include:

- Finding the coarsest exact observation compatible with a specified composition.
- Testing whether hidden state must be retained to predict a partner's observed evolution.
- Contextual distinguishability of histories or an observation process with finite additional memory.
- An extra state that evolves independently versus a derived label or a frozen coordinate.
- A second or third reapplication of the composition operator that is mathematically nontrivial and has a stated observable consequence.
- A defined intervention on a relation, interface or coupling law with matched null controls. Only then speak of intervention effects; reachability or a static dependency path is not causal propagation.

Do not chase a preferred depth, size or number of distinguishable states.

### E. Independent mathematical coverage and synthesis

Review the independent RRC coverage atlas for high-information gaps that may offer more leverage than developing the synchronisation model further. This may include elementary constraint families, geometry-sensitive composition, realised overlap, successive quotients or interface mappings.

**Atlas-019** and **Atlas-020** exist as frozen but unadopted plans and local outputs. They are not mandatory. Select them only after a fresh OTR assessment. If selected, verify and recover their **original** already computed bytes where valid; never pretend recovery is a new execution. If left unselected, leave them untouched and deferred.

Consolidate precise known mathematical equivalences, counterexamples and applicability of standard theorems before proposing new searches. An independently proved construction or failure can contribute more than another large fixture count.

---

## 4. OTR selection, stop and pivot

Make a reasoned choice **after** reading the live research. Do not choose solely because a portfolio is first in this document or because the previous model listed it as a next action.

Evaluate a few materially different proposals using the qualitative vectors:

- **Consequence:** Which competing mathematical explanations can this distinguish?
- **Readiness:** Are the types, operators, outcomes and validation methods clear?
- **Leverage:** How does it advance the central inquiry into systems participating in other relationships?
- **Cognitive/compute cost:** Can the work finish as a bounded, recoverable increment with available model credits?
- **Personal research significance:** Does the result connect to RRC's underlying questions rather than convenient test values?

Record one compact selection decision, alternative paths considered and why they were not selected. **No weighted/aggregate score, ranking metric, arbitrary research-cell quota or predetermined outcome.**

An acceptable completed increment may be:

- A scoped analytical theorem with direct proof and independent checks.
- An informative exact counterexample or obstruction to a stated claim.
- A mathematically consequential typed operation with demonstrated dynamics and negative/reducible controls.
- A selected, preflighted, independently verified and committed frozen experimental round.
- A synthesis that rigorously resolves confusion or redundant apparent findings, when it answers an explicit mathematical question.

**Method implementation, preliminary typing or freezing plans alone do not count as a finished scientific experiment.** Stop at a coherent, independently checked mathematical answer. If credit or tool resources run out before that point, mark **resource-blocked / incomplete**, preserve the precise restart point and never claim that omitted execution was a justified scientific stop.

---

## 5. Mathematical and implementation discipline

For every selected inquiry:

1. Define its **domain and quantifiers** before making a theorem claim: finite state sets, labels, interface and membership types, transition/event grammar, raw weights, normalization rule, halt/noop behaviour, observation clock and allowed equivalence operations.
2. Keep an explicit separation between **mathematical fact**, **computed software fixture**, **frozen scientific observation**, **model-level inference**, **representation dependence**, and **RS / ontological interpretation**.
3. Include a meaningful null, failure, reducible, and positive case when they sharpen the claim. Do not create examples solely to match an expected conclusion.
4. **Prove** a general claim by a general argument. Use exact rational software checks for independent verification and failure-mode tests, not to extrapolate broad claims from finite fixture enumeration.
5. When possible, use two distinct algorithms/representations (e.g. direct event enumeration and separate block/matrix algebra). Merely calling the main engine twice is not independent verification.
6. State whether equivalence preserves *only normalised kernels*, also *raw labelled weights*, *individual event identities*, *observations*, *interface meaning*, or *time*. Mark weaker statements honestly.
7. Avoid changing previously accepted method IDs. Any new research method or operator with different semantics receives its **own name/version and compatibility note**.
8. Record all local file/branch/CI provenance and preserve other research programmes and shared ontology/book projects outside the RRC work.

For **new scientific computations**, adhere to the existing mandatory freeze contract:

- Define selection scope, exact plan items, stopping and failure conditions, controls and costs.
- Conduct a disposable **end-to-end** preflight through the actual worker, serialization, receipts, hashes, interruption/resume and verification; discard scientific observables from the preflight.
- **Commit and push** the frozen experimental plan before executing its scientific cells.
- Use short independently recoverable tasks; ordinary watchdog **120 s**, hard per-item ceiling **300 s**. No uncontrolled monolithic enumerations.
- Execute only frozen items; preserve errors, timeout, pending, invalid and failed records without changing the planned inputs.
- Independently check mathematical outputs, publish a separate verified execution commit, append findings/coverage/crosswalk/journal updates and keep previous scientific records byte-for-byte intact.

For **analytical-only** increments, do not create an empty experimental freeze to satisfy a process ritual; clearly state that there are **zero newly adopted scientific atlas cells**.

No new experiment is required merely because one was mentioned in the prompt. No old uncommitted local output can be counted until verified and formally adopted.

---

## 6. Handoff requirements

Complete **one scientifically meaningful increment**, not the entire RRC programme.

Before finishing:

1. Confirm and report **starting live SHA**, all substantive and selection commits, **ending pushed SHA**, and status of the local worktree.
2. Give the precise mathematical question, independent OTR selection rationale and alternative families considered.
3. State the actual answer with quantified assumptions; include exact proofs/counterexamples and where the result is standard mathematics versus a new RRC-specific construction.
4. Separate software validations from scientific cells; state exact evidence paths, methods and counts.
5. Update `PROGRESS.md`, append-only coverage, equivalences, ideas, patterns, coherence findings/relations and the crosswalk as appropriate; **do not close broad questions on one example**.
6. Report local tests and CI outcomes **as observed**. Do not claim CI completion while jobs remain pending.
7. Explicitly preserve the disposition and any local output evidence of **Atlas-019 / Atlas-020**; do not cancel, adopt, rerun or modify them reflexively.
8. Include any blocker, missing evidence or exact restart instructions. Propose possible future directions but impose none.
9. Ensure a selected mathematical investigation is actually completed, independently challenged and committed before reporting **"research increment complete"**.

### Governing question

**When relational systems participate in further relationships, which constituent distinctions become consequential, which remain safely abstractable, and how does that depend on the form of the relationship itself?**

Investigate that question as open mathematics, not a conclusion that the research is obliged to confirm. Respect the difference between model specification, mathematical consequence and ontological interpretation.

**Audit live HEAD. Select for information value. Work to one coherent verified result. Commit, push and leave an honest handoff.**