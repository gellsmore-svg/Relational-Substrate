# RRC — Next Open-Thetical Research Cycle: Structural Composition and Changing Relationships

**Created:** 26 October 2026  
**Research programme:** Recursive Relational Complexity and Structural Composition (RRC)  
**Repository:** `gellsmore-svg/Relational-Substrate`  
**Research branch:** `research/recursive-relational-complexity`  
**Working subtree:** `relational-complexity/`  
**Status:** Research handoff and independent selection charter — **not** a frozen experimental plan, completed increment, claim of emergence, or prescribed scientific result  
**Authority:** RRC charter, `research-methods/open-thetical-research.md` and `relational-complexity/AGENTS.md`

## Mission

Continue the **open-thetical** investigation into what follows mathematically when relational systems are composed, participate in further relationships, and change their internal or external relationships over time.

The latest accepted investigation defined one **identified shared-port product** with a port value that can change, an inherited boundary that supports further composition, exact consistency conditions, and useful distinctions between keeping two copies, identifying one shared value, and obtaining a predictively closed observation.

Our new task is **not** to replay that construction with larger state spaces, or to prove that changing memberships, new relational degrees of freedom, levels, autonomous entities or complexity growth must occur.

It is to select and answer **one genuinely worthwhile mathematical question** from the still-open programme. Information-rich reductions, exact equivalences, negative results, counterexamples, impossibility under explicit assumptions, or valid new constructions are equally welcome. Novelty is not required where established mathematics already resolves an important RRC ambiguity.

**The next model chooses the question on its merits.** The candidate directions below are not mandatory tasks, staged milestones or an instruction to find a desired result.

---

## 1. Audit the live repository and current research

The verified research and default branch heads at creation were identical:

`47e9cbeb71034b6f2791a2c6fb7ec24538f365a3`  
`Merge verified shared changing-port research (#15)`.

This SHA is a **checkpoint, not a reset target**. Fetch remote branches; inspect local worktree(s), pending commits, untracked/ignored material, open PRs, CI and newer reports. Do not discard, overwrite, reexecute or relabel unpublished work simply because it is absent from the remote view. If another agent has already completed the candidate question, do not duplicate it.

Read at least:

- `PROGRESS.md`, RRC `README.md` and `charter.md`, the OTR method, `AGENTS.md`, `docs/atlas-charter.md`, `docs/atlas-crosswalk.md`, and current append-only `atlas/` and `coherence/` registers.
- `reports/2026-10-26-shared-changing-port.md`, `docs/shared-changing-port.md`, `docs/2026-10-26-shared-port-selection.md`, `provenance/2026-10-26-shared-port-verification.json`, and its checker/tests.
- `reports/2026-10-26-contextual-preservation.md`, `docs/contextual-preservation.md`; `reports/2026-10-26-sync-composition.md`, `docs/labelled-sync-composition.md`; earlier XOR and Atlas-018 material.
- The living definitions in `docs/composition-taxonomy.md`, `docs/composition-operators.md`, `docs/state-event-families.md`, `docs/coupled-models.md`, `docs/event-semantics.md`, `docs/representations.md`, `docs/cover-observations.md` and `docs/compilation-gate.md`, as applicable.
- Current `src/rrc/` methods, the scientific worker, independent validators, test suite and documented frozen-experiment contract.
- `prompts/2026-10-26-otr-handoff/FROZEN-PLAN-DISPOSITION.md`, plus the recent `provenance/2026-10-26-adaptive-local-audit.md`, for protected historical outputs.

At this checkpoint:

- The accepted scientific atlas contains **218 independently verified adopted cells**; **15 historical failed Atlas-007 items** remain excluded. The latest accepted shared-port increment is **analytical**: zero new worker runs and zero additional atlas cells.
- The reported RRC test suite passed **247 tests**, and the research, PR and post-merge CI completed successfully.
- The last analysis method is `shared-port-analysis-0.1.0`. Earlier analysis identifiers, `rrc-0.4.0`, `event-kernel-0.1.0` and `event-kernel-0.2.0` retain their declared historical meanings.
- **Atlas-019 and Atlas-020** are frozen, **deferred and unadopted**; original local output bytes and their hashes are protected. They are not failed, owed, secretly accepted or automatically scheduled. The two old generated files are also preserved.
- Broad RRC questions remain open. A few bounded analytical coverage entries do not close an entire programme.

Confirm these facts against **live evidence** before using the counts or claims.

## 2. Preserve exactly what the previous work taught us

The accepted shared-port analysis considered finite systems with boundary maps onto a fixed port set `P` and a fixed handshake alphabet `H`. Positive private events preserve the port. Shared events may update it, and paired shared transitions survive only when their target port values agree. Raw weights are combined before a single final normalization; an empty admitted event row halts without creating an extra event.

Within these assumptions:

- The identified-port composition is typed, associative under canonical reassociation, and has a port-relay identity; its result can be composed again.
- The agreement subset of the **unfiltered Cartesian copy product** is invariant exactly when **every positive paired shared event from agreeing source ports has agreeing target ports**. Otherwise the identified product filters transitions and renormalizes; with zero admitted mass the putative conditional distribution is undefined and a separate declared halt applies.
- Equal port marginals are insufficient for copy consistency. The observed `4/9` leakage and identified `[1/5,4/5]` law were **particular counterexample values**, not targets to reproduce.
- An eight-state changing-port example has real predictive dependence on its port in one observation, but reduces to ordinary current-state three-bit dynamics; it establishes **no new computational primitive**.
- A closed predictive abstraction need not retain the original boundary map needed for another composition. Port-map factorization and Markov closure are separate conditions.

The prior fixed-H contextual theorem likewise applies only to its declared Cartesian weighted synchronisation policy and observation class, not automatically to shared-port identification.

**Do not relabel any of these as an ontological result or universal theorem about all possible relational systems.** Preserve the mathematical/experimental/interpretive/RS layers separately.

## 3. Possible research avenues — independent alternatives, not required stages

### A. A relationship or membership that itself changes

The prior shared **port value** changes, but its type `P`, handshake alphabet `H` and private-write ownership stay fixed. This leaves a significant conceptual distinction unexamined: **changing the relationship itself**, rather than changing the value carried by a fixed interface.

Useful candidate questions include:

- A finite, typed **attachment or membership state** that connects or disconnects constituents, or moves a constituent between composites.
- A handshake relation whose admissible event pairings change with an attachment state, rather than a globally fixed H; is this truly different from a fixed larger label alphabet with guarded weights?
- A private writer handing off ownership of a port; what prevents incompatible simultaneous writes, and which event/clock convention governs the handoff?
- Composition with boundary/port interfaces of different types, via explicitly typed maps or spans; when can the output be composed again?
- An interface graph or hypergraph that changes alongside constituents; distinguish actual independently declared attachment choices from an observation computed from current constituent state.

For each selected candidate give precise state/event types, initial choice of independent state, transition semantics, constraints, event weights, port/membership compatibility, clock and output boundary. **If a conventional enlarged state-space model expresses everything exactly, record that reduction honestly.** It can still be a useful type/representation theorem; don't claim a new primitive just because there is a new kind of label.

This is one possible direction, not an obligation to create an independently evolving membership coordinate.

### B. Exact abstraction that remains suitable for *further* composition

The latest study demonstrates that first-order predictive closure and retaining a typed boundary are independent. A substantive new question could ask for the **joint information** required for a particular class of future interactions.

Possible directions:

- Conditions for a quotient map `pi` to be both a valid boundary-preserving map and an exact dynamic quotient under a given operator.
- When such quotients commute with shared-port gluing and when they fail, with meaningful positive, null and counterexample controls.
- Which changes if future partners may observe interface events or manipulate interface membership rather than only use a fixed port.
- Characterization of partner classes that can distinguish hidden port-dependent behaviour; careful quantifiers over **one context**, **all permitted contexts**, and **a bounded software menu**.
- Small separating contexts or a minimal sufficient signature, **only** if minimality is stated relative to a precise class and formally justified.

**Do not rerun the previous all-partner fixed-H Cartesian theorem** or assume its necessary-and-sufficient signature carries over to different identified interfaces. If an abstraction has no well-defined inherited boundary, report that as a type obstruction rather than quietly filling one in.

### C. Different composition instruments and comparison clocks

One operator is not a universal law. Independent high-information comparisons may vary:

- Filtering incompatible paired transitions versus rejecting attempted transitions as holds, blocking the whole operation, or defining a separately justified correlated coupling.
- Whether component-level normalization before composition, unnormalized products with final normalization, and an explicit attempt/retry clock preserve the same observables.
- Genuine state identification versus constraint-enforced duplicated state; determine which embeddings, quotients and invariants apply under matched event semantics.
- Two-component versus three-component construction when interface types or ownership differ; identify exact conditions for associativity or a concrete well-typed counterexample.
- Event identity, private/self-loop semantics, halt and emitted label observations.

Keep policy dependence distinct from a genuine structural distinction. Changing clocks is a **declared modeling choice**; it cannot silently be counted as new dynamics generated by relationality.

### D. Recursive participation, history and limits of reduction

Another direction is to consider whether further relationships alter what can be predicted from a compressed state. Candidate questions include finite observation memory, exact strong lumpability of a typed composite, hidden-rate dependence, or bounded nontrivial repeated composition.

A changing graph of relationships is not automatically a causally significant hierarchy. If you claim influence or an intervention, declare a matched intervention operator and observable before computing results. Do not call simple reachability a causal cascade.

State-space expansion is ordinary mathematics. When claiming that some behaviour cannot be represented in an existing grammar, **quantify the allowed state mappings, extra coordinates, event labels, clock, carrier meaning and intermediate transitions**. A failure of the original one-bit compiler or one coordinate system is not a general impossibility.

### E. Independent atlas inquiry and synthesis

RRC also has open elementary constraint, form/dissolve, carrier geometry, composition taxonomy and successive-quotient questions. Choose one of those instead if its consequence/readiness/leverage profile is stronger than continuing the shared-port track.

Atlas-019 and Atlas-020 may be reselected **only after a fresh OTR decision**, with their original frozen inputs and local results independently audited before any adoption. Do not rerun valid old results merely to produce a new scientific worker invocation. If not chosen, leave their evidence untouched and deferred.

A direct comparison with established mathematics (finite weighted automata, graph/hypergraph rewriting, labelled transition systems, Markov lumpability, probabilistic bisimulation, fibre products and open-system composition) may expose redundancy or a missing assumption. A rigorous synthesis answering a precise question can be a complete analytical increment.

## 4. OTR choice: favour information, not activity

After orientation, evaluate at least a few **materially different** possible inquiries using the existing qualitative vectors:

1. **Consequence:** What mathematical alternatives can the work distinguish?
2. **Readiness:** Can a meaningful question, typed objects, failure cases and verification actually be defined?
3. **Leverage:** How will the result inform other open RRC questions?
4. **Cognitive and compute cost:** Is this a bounded, resumable and worthwhile use of resources?
5. **Personal/research significance:** Does it illuminate relationships among relational systems, rather than merely generate more fixtures?

Do not turn this into an arbitrary weighted numeric ranking. Record an explicit selection rationale and alternatives not selected. Seek a question for which **both a positive and a negative/reducible outcome have information value**.

Only **one coherent, independently validated research increment** is required. Do not treat sections A–E as checkboxes, a mandatory progression or a request to prove emergence.

It is acceptable to stop after a valid analytical theorem, exact counterexample, proven representational reduction or a completed frozen/verified experiment, if it genuinely answers the selected question. It is **not** acceptable to claim completion after method scaffolding, unexecuted selected scientific items or a list of ideas. If compute/model credits interrupt work, record **resource-blocked/incomplete** and preserve a precise restart point.

## 5. Scientific rigor and provenance

For any selected inquiry:

- Define exact finite domains, input/output types, observations, state and interface variables, validity constraints, event grammar, raw weights, zero/halt semantics and the relevant clock.
- Name explicit equivalence notions: representation/coordinate recoding, labelled/raw-weight equality, one-step Markov kernels, full-state conjugacy, invariant image, strong lumpability, boundary-preserving morphism and contextual substitution are different.
- Prove general claims by argument, not by extrapolating a small enumeration. Keep necessity separate from sufficiency and preserve undefined/failed cases.
- Use predeclared positive, negative, null and reducible controls, not a search for the desired result.
- Validate with independent exact rational calculations, hand proofs or algorithmically different checker implementations; do not merely call production code twice.
- Identify relevant established theorems and precisely what RRC-specific construction or limitation they explain. Do not claim standard algebra, fibre products or probability identities as new universal mathematics.
- Give genuinely new semantics a **new versioned method identifier**. Preserve old engine, event-kernel and analysis interpretations.
- Distinguish software fixtures and proofs from **formally frozen scientific atlas cells**. No new scientific-cell count merely because more tests passed.

For an **experimental scientific round**, follow the immutable freeze contract: predeclare exact items, outcomes and resource budgets; complete disposable worker/schema/receipt/hash/interruption/resume preflight; **commit and push the immutable plan BEFORE any selected scientific execution**; run independently recoverable items with ordinary 120-second watchdog and hard 300-second per-task maximum; preserve complete/fail/timeout/invalid/unrun statuses; independently verify exact results; publish a separate execution/verification commit; and update registers accurately. Do not edit a frozen item after observing its output.

For a **purely analytical increment**, no fake experimental freeze is necessary. Preserve proofs, independent mathematical challenge, validation bounds, source versions, deterministic evidence and explicitly **zero** newly adopted scientific cells.

Protect historical Atlas-001–020 plans/results, old Atlas-007 failures, Atlas-019/020 untracked output bytes, existing `generated/` evidence and other programmes. Keep books, central synthesis and ontology outside direct RRC modifications except through an independently authorised integration.

## 6. Publish, automatically integrate, and hand off

When substantive research has **actually completed and passed independent verification**:

1. Publish a clear report under `reports/`; formal analysis and proofs under `docs/`; verification/evidence under `provenance/`; and tests as appropriate.
2. Add precise append-only findings, ideas, equivalences, patterns, relations, coverage, crosswalk and journal entries **only where warranted**. Preserve historical prefixes and unique IDs; do not close broad atlas questions from one narrow result.
3. Push selection and actual substantive research commits separately as needed, with an honest publication timeline and observed CI status.
4. Under the standing user instruction in `relational-complexity/AGENTS.md`, **open/update the PR and automatically merge validated RRC research into `main` without requesting another permission**. Preserve newer changes to unrelated code, other research, ontology, books, synthesis, dependency snapshots and lockfiles. Require the actually configured application/reports, laboratory, RRC and book CI checks to pass.
5. Verify the merged `main` SHA and safely synchronise the continuing research branch. Preserve local untracked deferred outputs and their audit hashes. If blocked by branch protection, failing checks or a conflict, report **research complete / integration blocked** and the exact blocker; never invent a successful merge.
6. Do **not** treat this prompt's own upload or merge as scientific completion. Automatic merge authority covers **validated completed RRC work**, not future speculation.

Final handoff must give:

- Actual starting SHA/worktree, selected question, OTR vectors and alternatives considered.
- Exact assumptions, proof/counterexample, new understanding, reduction/equivalence boundaries and the status of relevant known mathematics.
- Independent validation evidence paths/hashes and exact test/CI outcomes, keeping analytical fixtures separate from adopted scientific cells.
- Any new frozen plan and verified scientific-cell statuses, or an explicit analytical-only declaration.
- Selection, substantive, verification, PR and final merge SHAs/URLs, plus the continuing research branch HEAD.
- Preserved Atlas-019/020 hashes/status and protection of frozen history.
- An exact restart location and some **optional**, not mandated, future inquiry directions.
- One honest conclusion: **research complete and merged**, **research complete but integration blocked**, or **research incomplete/resource-blocked**.

### Governing principle

**Relationships can participate in further relationships; what this entails depends on the precise state, interface, event and observation contracts. Investigate their mathematical consequences without treating a hoped-for ontological account as either evidence or an answer.**

Start from the live branch, select for information value, complete one independently challenged result, publish it and automatically integrate it when valid.