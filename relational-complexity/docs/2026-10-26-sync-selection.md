# OTR selection: compositional predictive descriptions

Selected 26 October 2026 under
`prompts/2026-10-26-relational-composition-and-dynamics/RESEARCH-PROMPT.md`,
introduced at `c2f71ca` and format-corrected at `ec6888c`.
Starting live branch: `2bda78f45d3032a2d3f923863390bba4f2eb3d89`.

## Live audit

The worktree was fast-forwarded from `a06a02c` without disturbing the local
Atlas-019/020 outputs. Starting CI is successful and all 193 existing RRC tests
pass. Atlas-018 remains accepted; its frozen records and the later XOR analysis
are not rerun or reclassified. The scientific atlas remains 218 complete cells,
excluding 15 historical failures. Both deferred rounds remain unadopted.

## Chosen question

Does equality of a component's aggregate Markov dynamics, or exact closure of
one of its observations, survive a typed event-synchronising composition?
What stronger component information suffices to make reduction commute with
composition, and can the resulting system be composed again?

This investigates an actual operation on systems and their subsequent dynamics,
not another XOR parameter variation or a static relabelling of a cover.

Use finite weighted labelled transition systems. Each component carries the
same explicitly declared handshake alphabet H. Shared-label events synchronise
in a pair with product weight; other events update one component while the
other holds its state. Output states are Cartesian pairs and output event
weights are kept unnormalised for possible further composition. Only the final
global one-event law is normalised; an empty row halts without creating an
event. This is a specified instrument, not a universal synchronization policy.

Investigate associativity at fixed H, the identity component, aggregate-kernel
counterexamples, and sufficient labelwise weighted quotient conditions. Compare
fixed and evolving omitted state, shared-only and private-clock contexts, and
halt completion versus a declared synchronising no-op. A sufficient condition
must not be presented as necessary for every fixed partner.

## Selection judgement and alternatives

| Vector | Assessment |
| --- | --- |
| Consequence | Can separate stand-alone predictive equivalence from interchangeability inside a relational interaction. |
| Readiness | Finite weighted events, explicit pairing and block-row sums admit short exact proofs and independent enumeration. |
| Leverage | Gives a well-typed reapplicable operator for Q12 and connects Q10/Q13/Q15 with event-level information lost by aggregation. |
| Cognitive/computation cost | Small components, exact fractions and bounded software domains; no new scientific worker type is required. |
| Research significance | Directly addresses relationships between systems and whether their useful effective descriptions survive composition. |

Alternatives considered but not selected: new changing-membership semantics
without a settled validity contract; a general nonlinear XOR-embedding classifier;
another frozen atlas recovery; and a new finite-horizon influence experiment.
These remain legitimate later choices, not cancelled obligations. The chosen
question has greater immediate leverage because it specifies the composition
operation and a meaningful preservation property together.

## Predeclared verification and stopping boundary

This is an analytic increment with validation fixtures, not a new atlas round.
Use `label-sync-analysis-0.1.0` without changing any existing engine or event-kernel
method. General claims require self-contained proofs; finite cases check code.

Two independent calculation paths will be compared: sparse enumeration of
matching event pairs and private events, and dense per-label matrix formulas.
The bounded basis menu contains the empty two-state component and every single
unit-weight transition on two states labelled shared or private. Check all
pairs and triples of that menu; do not select cases by their resulting fractions.
Include a nonbinary three-state cycle, duplicate-event aggregation and positive
weights beyond one as additional software controls.

For reduction, lift those components with a hidden binary coordinate whose
updates hold, flip or reset it while preserving each label's block weights.
Compare quotient-before-composition with composition-before-quotient against
the basis partners. Include a both-factors-reduced control, hidden-label
counterexample, private-clock scaling control, constant/identity observations,
all-halt rows, valid synchronising no-ops and invalid interface signatures.
Undefined quotient rows must remain absent.

Commit and push this choice before running new validation fixtures. Stop after
the operation, preservation theorem and informative counterexamples are proved,
independently checked, integrated and pushed. Do not add fixtures to the atlas
count, adopt deferred results, invent autonomous entities, or claim a complete
classification of all possible composition policies.
