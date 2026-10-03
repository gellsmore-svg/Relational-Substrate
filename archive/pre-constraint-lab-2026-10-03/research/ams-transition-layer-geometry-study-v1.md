# AMS Transition-Layer Geometry Study v1

## Purpose

This document develops the missing geometric layer identified in:

- `ams-glass-to-crystal-compatibility-study-v1.md`

The central problem is:

- how an interface can transform one transmissive organisation into another

without reducing the transition to:

- vague compatibility language
- simple admission failure
- or crude defect burden

The current highest-pressure case remains:

- `glass -> crystal`

because it forces the model to explain how distributed permissive propagation can become structured nested admissibility.

## Core Claim

The interface should no longer be treated as a zero-thickness boundary.

The current working claim is:

- successful cross-transmissive handoff requires a transition layer with its own geometry

That geometry must account for:

- local release from the source whole
- local reseating into admissible transition pathways
- narrowing or ordering of those pathways
- final admission into the receiving whole

This implies that the interface is:

- not merely contact
- not merely disruption
- but a structured region with its own causal role

## Three Candidate Boundary Geometries

## Geometry A: Sharp Boundary

### Description

The source whole and receiving whole meet abruptly. There is little or no intermediate region. Pathway organisation changes almost immediately from one grammar to another.

### Expected Behaviour

- high mismatch sensitivity
- strong dependence on immediate `B_in` and `B_out`
- low tolerance for organisational differences

### Likely Outcomes

- selective handoff when the two sides are already well matched
- reflection, scattering, or trapping when they are not

### Strength

This geometry is simple and may fit some highly polished or strongly bounded interfaces.

### Weakness

It appears too brittle to explain the more graded compatibility behaviour suggested by `glass -> crystal`.

### Current Assessment

Useful limiting case, but probably not the general solution for the hardest transmissive-compatibility problems.

## Geometry B: Graded Transition Layer

### Description

The interface includes a finite region in which pathway organisation changes progressively rather than abruptly.

The layer does not yet fully behave like the receiving whole, but no longer behaves simply like the source whole either.

### Expected Behaviour

- reduced mismatch shock
- partial preservation of coherence across the transition
- better support for staged reseating and narrowing

### Likely Outcomes

- stronger successful handoff
- less dominant scattering
- lower likelihood of immediate structured reflection

### Strength

This geometry fits the current need for:

- progressive compatibility
- mediation rather than instant conversion

### Weakness

Still too general unless we specify how the gradient works.

### Current Assessment

Most plausible general candidate for `glass -> crystal`.

## Geometry C: Funnelled Transition Layer

### Description

The transition layer does not merely grade from one order to another. It actively narrows distributed permissive propagation into fewer, more structured onward routes.

This is more than a gradient. It is a local reorganisation of pathway availability.

### Expected Behaviour

- strong interface mediation
- selective but more successful handoff than a sharp boundary
- potential for local trapping if narrowing is incomplete or overloaded

### Likely Outcomes

- selective successful handoff
- partial handoff
- trapping when the funnel geometry is active but insufficient

### Strength

This geometry directly fits the hardest problem:

- turning distributed propagation into patterned admissibility

### Weakness

It introduces more structure than the current variable set may yet describe clearly.

### Current Assessment

This is the most fertile candidate for cross-transmissive compatibility, but also the one most likely to require variable refinement.

## Comparison of the Three Geometries

| Geometry | Best use case | Main strength | Main weakness | Current plausibility for `glass -> crystal` |
|---|---|---|---|---:|
| Sharp boundary | simple limiting case | clarity | too brittle | 4/10 |
| Graded transition layer | broad compatibility mediation | staged reseating | still abstract | 8/10 |
| Funnelled transition layer | hard cross-transmissive handoff | active ordering of transition | may require extra variables | 9/10 |

## What the Transition Layer Must Actually Do

The current studies suggest that a real transition layer has to perform four distinct roles:

### 1. Preserve Source-Side Release

It must allow propagation to leave the source whole without immediate destructive collapse.

This keeps `B_out` relevant.

### 2. Support Near-Interface Reseating

It must provide local paths for repeated reseating rather than forcing:

- immediate return
- immediate scattering
- or premature trapping

This is the part of the process most strongly implicating `J_surf`.

### 3. Narrow or Order the Propagation

In `glass -> crystal`, the transition layer must reduce distributed permissive spread into a more patterned onward event.

This is the point at which the idea of a pathway funnel becomes most important.

### 4. Present a Receivable Event to the Crystal

It must hand off a disturbance that the receiving whole can admit into structured nested order.

This keeps `B_in` and `Q_coh` relevant.

## Does `J_surf` Need Splitting?

Current answer:

- probably yes

Reason:

`J_surf` is currently being asked to cover at least three different functions:

- local surface coupling at the immediate boundary
- transition-layer mediation across finite depth
- capacity for repeated reseating within the interface region

That is too much for one variable if the geometry becomes more explicit.

## Provisional Split

### `J_bound`

Meaning:

- immediate coupling behaviour at the boundary face itself

This captures:

- how strongly the interface responds at first contact
- whether a structured boundary event forms at all

### `J_trans`

Meaning:

- coupling continuity within the transition layer beyond the first contact zone

This captures:

- whether local reseating can continue through the interface region
- whether narrowing and handoff are viable

### Why This Split Helps

It distinguishes:

- surface response
- through-interface mediation

That is exactly the distinction the current programme has started to need.

## Is Trapping a Real Interface Mode?

Current answer:

- yes, probably

But it is still underdefined.

The transition-layer picture strengthens the case for trapping because a finite layer can fail in more ways than a sharp boundary can.

A disturbance may:

- enter the transition layer
- fail to complete handoff
- fail to return cleanly
- remain locally re-seated within a bounded interface region

That is not just poor transmission. It is a distinct local mode.

## Two Candidate Trapping Geometries

## Trapping Geometry T1: Shallow Retention

### Description

The disturbance remains near the boundary face. Reseating occurs locally, but deeper progression into the transition layer fails.

### Likely Signature

- low `J_trans`
- medium/high `J_bound`
- low `B_in`
- low `B_out`

## Trapping Geometry T2: Funnel Stall

### Description

The disturbance enters the transition layer and is partially narrowed, but the final structured handoff fails. The event remains in a repeated local cycle inside the funnel region.

### Likely Signature

- medium/high `J_trans`
- medium/high `J_bound`
- medium `Q_coh`
- low/medium `B_in`
- low/medium `B_out`

### Importance

This is the more interesting trapping case because it would mean the interface is actively doing work, but not enough to complete compatibility.

## Current Best Geometric Reading of `glass -> crystal`

The current best reading is now:

- not a sharp boundary
- not a purely passive graded boundary
- but a graded transition layer with funnel tendencies

That means the most plausible geometric picture currently is:

1. source-side distributed release
2. local transition-layer reseating
3. narrowing or ordering of admissible paths
4. selective crystal admission

This is the first point in the programme where that sequence can be stated this explicitly.

## Main Consequences for the Variable Set

## Keep

- `B_in`
- `B_out`
- `Q_coh`
- `D`
- `I_comp`

## Refine

- replace or split `J_surf`

Preferred current move:

- `J_surf` -> `J_bound` + `J_trans`

## Do Not Add More Variables Yet

The current model does not yet justify adding a large new family of transition variables.

The best move is to split the one clearly overloaded variable first and see how much sharper the geometry becomes.

## Provisional Confidence

- confidence that a finite transition layer is needed: `9/10`
- confidence that the funnel picture is more useful than the sharp-boundary picture: `8/10`
- confidence that `J_surf` is overloaded: `9/10`
- confidence that the `J_bound` / `J_trans` split is the right next refinement: `8/10`
- confidence that trapping is a real interface mode: `7/10`

## Next Move

The best next artifact is:

- `ams-interface-variable-refinement-v1.md`

That should:

- formally replace `J_surf` with `J_bound` and `J_trans`
- rerun the key interface pairings with the refined variables
- test whether:
  - `glass -> crystal` becomes sharper
  - trapping becomes more distinguishable
  - `I_comp` becomes less overloaded
