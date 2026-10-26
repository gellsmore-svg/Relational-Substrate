# Inquiry modes

Two modes of inquiry are legitimate in this laboratory. Generation 007B uses one of them. It documents the other and does not execute it.

## MODE A — discriminating experiment

This is the current mode.

Question form:

```text
What specific ambiguity remains?
What is the smallest controlled experiment that distinguishes the live explanations?
```

It emphasises:

```text
matched controls
predeclared observables
confound removal
bounded inference
```

A discriminating experiment freezes the ontology, the observable, the tolerance, and the selection rule before the comparison it is meant to inform. Representation, composition, state shape, selectivity, and complexity stay separate reports. They are not collapsed into one pass/fail judgement.

Pass and fail remain available for software tests, CI, verification, and explicit engineering requirements.

## MODE B — open relational exploration

This is a future mode. It is not executed in 007B.

Question form:

```text
What happens if we introduce this relation/constraint/process?
What structures emerge?
What changes when another element is added?
What recurrent patterns or transitions appear?
What does the accumulated trajectory suggest?
```

In this mode there is no scientific failure in the ordinary sense.

Unexpected outcomes are observations that redirect exploration.

The intellectual loop is:

```text
exploration
→ observation
→ inference
→ coherence comparison
→ revised exploration
```

This is compatible with the broader Relational Substrate methodology.

Generation 007B does not switch into Mode B. Mode B stays a future research fork.

## Reproducibility requirement for Mode B

When Mode B is eventually used, it must still be reproducible.

Any exploratory stochastic journey must preserve:

```text
initial state
random seed(s)
proposal sequence
accepted/rejected events
constraint additions/removals
parameter changes
intermediate states
observables
branch decisions
agent rationale / research question at each branch
```

The entire exploration should be replayable.

A stochastic exploratory path may be contingent.

It must not be opaque.

## Epistemic principle for a future exploratory run

When that mode is used:

```text
The absence of an expected phenomenon is an observation, not a failed experiment.
```

```text
Multiple causes are not automatically a defect; they are part of the relational structure to be disentangled later if useful.
```

```text
The purpose is directional information and coherence accumulation, not repeated binary hypothesis verdicts.
```

This does not weaken reproducibility. It changes the question being asked.

## Event-sourced exploratory journey

A future exploratory engine must make the entire journey reconstructible:

```text
experiment version
initial state
constraints at each step
proposal source
random seed
random draw
chosen event
state transition
observables before/after
agent-selected next perturbation
reason for perturbation
```

The final output should be analysable as a path, not merely as an endpoint.

Generation 007B documents this requirement. It does not implement the exploratory engine.

## Fork, not a change of the current question

If the discriminating-control programme reaches diminishing returns, a later branch may ask "What happens if...?" rather than "Does X pass this test?"

A possible future experiment should:

1. Begin from a minimal state/constraint grammar.
2. Allow bounded additions, removals, and modifications of relational constraints.
3. Run replayable stochastic trajectories.
4. Record every change and every random choice.
5. Observe emergent organisation, dissolution, transition, memory, boundary, routing, and repair. Those outcomes are not hard-coded.
6. Let observations determine the next exploratory perturbation.
7. Compare accumulated patterns for global coherence. A pass/fail status is not assigned at each step.

That fork is not part of the 007B execution.

## Generation 8 executes Mode B

Generation 8 is the first laboratory execution of Mode B. Generations 1 through 7B remain Mode A records. Their reports are historical evidence and are not reinterpreted by editing them.

Generation 8 asks:

```text
What happens when higher-order relational context is allowed to participate in an evolving stochastic relational system, and what recurrent structures, routes, transformations, and context dependencies actually appear?
```

The governing loop is:

```text
exploration
→ observation
→ inference
→ coherence comparison
→ revised exploration
```

A completed trajectory has no scientific pass or fail. Unexpected behaviour is an observation.

Scientific language for Generation 8 is:

```text
observed
not observed
common
rare
context-dependent
context-insensitive
recurrent
transient
robust
sensitive
suggestive
unresolved
```

Pass and fail remain appropriate for software, CI, validation, and execution contracts. They are not the vocabulary of a trajectory atlas.

The unconstrained system in Round 0 is baseline relational dynamics. It is not called a null hypothesis in this generation.

The model contains state, possible events, constraint weights, and stochastic event selection. Organisation, persistence, dissolution, reorganisation, return, recurrence, routing, context dependence, repair-like return, and boundary-like persistence may be observed afterwards. They are not encoded as a reward, a target, or a semantic goal.

Exploration decisions happen between rounds. No stochastic trajectory is rewarded for reaching a desired state. There is no optimisation against maximum routing divergence, entropy, organisation, or persistence.

Open exploration still requires a frozen round plan, bounded work, deterministic seeds, complete event provenance, replay, durable outputs, explicit branch decisions, and separate observation and inference. The difference from Mode A is the question, not the engineering.

A crisp distinction found here may later be isolated by a Mode A experiment on another branch. Generation 8 does not turn that isolation into an unbounded discriminating census inside this prompt. At most four rounds are executed: Round 0, Round 1, Round 2, and Round 3. The charter is `constraint-lab/exploration/generation-008/charter.md`.

## Information calibration

Whenever a descriptive information statistic is estimated from finite trajectories, first identify structural zero-information controls or exact-kernel comparators. Do not interpret the plug-in value directly when the estimator has a non-negligible finite-sample bias. Where the state space permits, prefer exact transition-law information to bias-corrected trajectory estimates.

This applies to later Mode A work and to later Mode B work.

A plug-in mutual information computed from a finite contingency table is one layer of the observation. A permutation of the labels, with the outcome marginals held fixed, estimates the finite-table bias of that same plug-in. An exact-kernel quantity, computed from the known transition law, is a third layer. The three layers answer different questions. A table names its layer.

Structural zero-information controls are part of the model. A system whose pair-event law does not read the triad is a calibration instrument for any statistic that claims triad-context information on the pair-event clock. If that statistic is large on the control, it is describing the estimator before it is describing the dynamics. The control is not a null hypothesis, and the comparison is not a pass/fail test.

Negative values of `observed plug-in − null mean` stay in the stored tables. They say the finite sample landed below the estimated null mean. Only an exact mutual information is mathematically non-negative. A float64 kernel result is a deterministic kernel result. It is not called a mathematical identity unless the arithmetic is exact.

## Mechanistic representation

After exploratory statistics identify a stable non-zero structure, search for a minimal mechanistic representation before expanding the experiment. Prefer a small exact causal geometry inside the explicit model transition law over repeated measurement of the same effect. The phrase "causal geometry" here means a dependence in that declared law. It is not, without a further qualification, a claim about a system outside the model.

## Finding dimensions

A finding has several dimensions. Magnitude, robustness, persistence, explanatory reach, and structural role must not be collapsed into a single strength score. A small or fragile phenomenon may be structurally essential. A large robust phenomenon may be mechanistically generic. Preserve the literal observation and let later relational evidence establish significance.

The coherence ledger is `constraint-lab/coherence/`. `findings.jsonl` and `relations.jsonl` are the record. The Markdown and Mermaid views are generated. A substantive generation appends findings and relations, regenerates the views, and writes an immutable snapshot under `constraint-lab/coherence/snapshots/`. The snapshot hash belongs in that generation's provenance. Future prompts name the coherence nodes that motivated them.
