# Generation 8 charter — Mode B, open relational exploration

Generation 8 is the first execution of Mode B. The inquiry note is `constraint-lab/docs/inquiry-modes.md`. Generations 1 through 7B stay Mode A evidence. Their files are not rewritten.

## Question

What happens when higher-order relational context participates in an evolving stochastic relational system, and which recurrent structures, routes, transformations, and context dependencies appear?

A completed trajectory has no scientific pass or fail. Unexpected behaviour is an observation.

## What the runtime contains

The process contains only:

```text
state
possible events
constraint weights
stochastic event selection
```

Derived records may later describe organisation, persistence, dissolution, reorganisation, return, recurrence, routing, context dependence, repair-like return, or boundary-like persistence. Those words are not rewards, targets, or semantic goals. The engine does not seek a destination class.

The unconstrained system is baseline relational dynamics. This charter does not call it a null hypothesis.

Exploration choices are made between rounds, after observations. No trajectory is trained or scored so that a larger divergence, entropy, or residence becomes a reward.

## Fixed ontology

```text
N = 4
O = 3
G = 0
S = 0
H = 0
L = 0
independent hypergraph
```

The state is 6 pair bits and 4 independent triad bits: 10 bits, 1024 full states. Geometry, explicit memory, entity state, meta-constraints, simplicial face closure, and a larger N are outside this generation.

## Clocks

The full-event clock counts every toggle, including triad-only events. The pair-event epoch counts toggles of the six pair slots. Routing summaries may use the pair-event epoch. Triad-only timing stays in the event stream.

## Rounds

At most four rounds:

```text
Round 0
Round 1
Round 2
Round 3
```

Round 0 is a starter atlas:

```text
baseline
the canonical structural T->P singleton archetypes from Generation 4, at strong_suppress
one Generation 5 disjoint-action T->P + P->P anchor, both rules at strong_suppress
```

`prohibit` is absent from Round 0 so the first atlas keeps finite stochastic support. A later round may introduce `prohibit` only when an observation gives a concrete reason to inspect a hard-support boundary, written in the journey before that round runs.

Adaptive rounds contain at most four new systems. Extra seeds, a narrower context scope, or a different finite grade on a system already run counts as one of the four when it adds substantive compute. The default replicate count is 16. A later round may use 32 or 64 on a narrower set when the journey says the allocation is for trajectory resolution. That is not a power calculation and it is not a significance test.

Allowed perturbation operators, unless a committed plan amends the list:

```text
weight_shift among strong_suppress, weak_suppress, weak_favour, strong_favour
condition_polarity_flip present <-> absent
structural_tp_neighbour among the known canonical T->P orbits
add_pp_companion from the Generation 4 P->P canonical set, total rules at most 2
remove_rule from a two-rule system
```

Ontology axes stay fixed. Adaptive rounds ordinarily reuse the Round 0 source and context-orbit basis. A narrower scope keeps the Round 0 context ids and says why.

## Frozen plans

Every round executes only after its plan commit exists on the remote. The plan hash covers the palette, the horizon, the seed schedule, the context basis, the replicate count, and the work count. The commit SHA is `frozen_exploration_plan_commit`. The plan file does not contain that SHA. The runner refuses to start without a 40-hex commit whose committed plan hash matches the plan being executed. Result artifacts record the SHA. Scientific results are a later commit.

## Horizon preflight

The primary horizon is 512 pair-event epochs, with a safety cap of 16,384 full events. Before Round 0, a cost benchmark may reduce the horizon. The reduction rule is operational and is applied before any atlas is interpreted:

```text
If the estimated Round 0 wall at 2 workers exceeds 3 hours,
or the estimated compressed event storage exceeds 2 GiB,
or one replay exceeds 5 seconds,
freeze 256 pair events instead of 512.
If that reduced horizon still exceeds either budget, freeze 128.
If 128 still exceeds either budget, stop and record the estimate.
Do not read route outcomes in order to choose the horizon.
```

Termination reasons `pair_horizon`, `full_event_cap`, and `no_admissible_event` are observations. The episode record remains valid.

## Attention

When a later round is chosen, each candidate carries an unsummed attention vector. The coordinates are ordinal 0–5:

```text
CN contextual novelty
RD routing diversity
RC recurrence / return structure
EC explanatory-compression potential
CG coherence relevance
CB computational boundedness
```

The coordinates are not a confidence score and not a pass/fail score. They are not added together.

## Interpretation boundary

Simulation, observation, and structural inference may contribute to a coherence assessment. They do not establish a Designer, a Christian ontology, or an ultimate receiver. Those remain upstream or broader premises.

Each round report separates observations, inferences, the coherence reading, and the next options. Causal wording stays out of the observation tables.

## Journey

`journey.jsonl` is append-only. A decision record is not rewritten after it is written.
