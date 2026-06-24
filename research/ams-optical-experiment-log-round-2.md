# AMS Optical Experiment Log Round 2

## Purpose

This document reruns the first optical benchmarks using the initial geometry and state-variable sketch.

Round 1 identified promising family combinations. Round 2 asks a stricter question:

- what variables seem to be doing the real explanatory work?
- and where are the current models still too vague to trust?

This is still not final mathematics. It is a sharper experimental pass.

## Variable Set In Use

The current variables are:

- `T` = torsion magnitude
- `C` = closure tightness
- `R` = return-path strength
- `K` = knotting / linking complexity
- `J` = coupling strength
- `S` = slip tolerance
- `Q` = resonance compatibility
- `B` = boundary sensitivity
- `D` = defect sensitivity
- `M` = memory retention

## Round 2 Rule

Each benchmark now records:

- dominant family combination
- dominant variables
- weakly constrained variables
- current modelling judgment

## Experiment R2-001

- `Experiment ID`: `R2-001`
- `Target behaviour`: glass transmission
- `Dominant family combination`: `G + D + F`

### Current variable profile

- `T`: low to moderate
- `C`: moderate
- `R`: moderate to high
- `K`: low to moderate
- `J`: moderate
- `S`: moderate to high
- `Q`: moderate
- `B`: moderate
- `D`: high
- `M`: low

### Dominant variables

Current strongest candidates:

- `R`
- `S`
- `D`

Interpretive reading:

- glass transmission currently seems to require enough return-path strength and slip tolerance for propagation to remain coherent through a disordered whole
- defect sensitivity appears to explain why clarity degrades without requiring total loss of whole identity

### Weakly constrained variables

- `T`
- `K`
- exact role of `Q`

### Current modelling judgment

Promising.

The model is now more informative than in Round 1, because it can say:

- transmission through glass likely depends more on distributed pathway permissibility than on high knotting complexity or strong static closure

### Main unresolved point

We still lack a sharp geometric definition of:

- what counts as an admissible pathway in a disordered whole

## Experiment R2-002

- `Experiment ID`: `R2-002`
- `Target behaviour`: reflection from metal
- `Dominant family combination`: `H + E + F`

### Current variable profile

- `T`: low to moderate
- `C`: moderate
- `R`: moderate to high at whole level
- `K`: low
- `J`: high
- `S`: low to moderate
- `Q`: high
- `B`: very high
- `D`: moderate to high
- `M`: moderate

### Dominant variables

Current strongest candidates:

- `J`
- `Q`
- `B`

Interpretive reading:

- metal reflection currently looks most coherent when treated as a collective surface response of a highly coupled whole with very strong boundary sensitivity

### Weakly constrained variables

- exact role of `T`
- whether `M` matters only as a modifier or as a primary driver in real metals

### Current modelling judgment

Promising and stronger than in Round 1.

The variable picture now makes it clearer why metal reflection should not be reduced to:

- isolated local events

It appears to require:

- high whole-level coupling
- high resonance compatibility
- decisive surface response

### Main unresolved point

We still need a sharper distinction between:

- collective surface response
- and merely many local surface responses happening at once

## Experiment R2-003

- `Experiment ID`: `R2-003`
- `Target behaviour`: crystal transmission
- `Dominant family combination`: `C + G + F`

### Current variable profile

- `T`: low to moderate
- `C`: moderate to high
- `R`: high
- `K`: moderate
- `J`: high
- `S`: low to moderate
- `Q`: moderate
- `B`: moderate
- `D`: high at defect sites, low in ordered bulk
- `M`: low

### Dominant variables

Current strongest candidates:

- `R`
- `J`
- structured `S`

Interpretive reading:

- crystal transmission currently looks like propagation through a strongly nested whole with more regular admissibility than glass

### Weakly constrained variables

- exact role of `K`
- whether `Q` is central or only supportive

### Current modelling judgment

Coherent.

This is one of the stronger early optical modelings because it cleanly differs from glass without requiring a different ontology.

### Main unresolved point

We still need a better geometric distinction between:

- regular nested pathway order
- distributed permissive pathway order

## Experiment R2-004

- `Experiment ID`: `R2-004`
- `Target behaviour`: defect-sensitive scattering
- `Dominant family combination`: `F + G`

### Current variable profile

- `T`: low to moderate
- `C`: moderate
- `R`: moderate
- `K`: low
- `J`: moderate
- `S`: moderate
- `Q`: low to moderate
- `B`: moderate
- `D`: very high
- `M`: low to moderate

### Dominant variables

Current strongest candidates:

- `D`
- `S`
- `R`

Interpretive reading:

- scattering currently looks best understood as local disruption or redirection of otherwise viable propagation pathways

### Weakly constrained variables

- exact role of `M`
- whether higher `Q` sometimes turns scattering into resonant response instead of simple disruption

### Current modelling judgment

Strong relative to the other benchmarks.

This is one of the clearest current uses of `Family F`.

### Main unresolved point

We still need a sharper taxonomy of:

- weak scattering
- strong scattering
- propagation breakdown

## Experiment R2-005

- `Experiment ID`: `R2-005`
- `Target behaviour`: transparent boundary entry and exit
- `Dominant family combination`: `E + G + D`

### Current variable profile

- `T`: low
- `C`: moderate
- `R`: moderate
- `K`: low
- `J`: moderate
- `S`: moderate
- `Q`: moderate
- `B`: high
- `D`: moderate
- `M`: low

### Dominant variables

Current strongest candidates:

- `B`
- `S`
- `R`

Interpretive reading:

- entry and exit at transmissive boundaries probably depend on boundary conditions more strongly than the bulk-transmission model alone suggests

### Weakly constrained variables

- almost all except `B`

### Current modelling judgment

Underconstrained.

This remains an important benchmark, but it is currently the weakest of the set because the geometry of entry and exit has not yet been sharply specified.

### Main unresolved point

We need a better geometric account of:

- what happens when a propagating regime crosses from one admissibility field into another

## Experiment R2-006

- `Experiment ID`: `R2-006`
- `Target behaviour`: metal surface quality and reflection degradation
- `Dominant family combination`: `H + E + F`

### Current variable profile

- `T`: low
- `C`: moderate
- `R`: moderate to high
- `K`: low
- `J`: high
- `S`: low to moderate
- `Q`: high
- `B`: very high
- `D`: high
- `M`: moderate

### Dominant variables

Current strongest candidates:

- `B`
- `D`
- `J`
- `Q`

Interpretive reading:

- reflection quality appears to depend not only on metallic whole identity but on preserving a surface condition that can respond collectively without strong defect-induced incoherence

### Weakly constrained variables

- exact role of `M`
- how surface oxidation should be modelled in relation to bulk metallic order

### Current modelling judgment

Promising.

This benchmark strengthens the general idea that:

- reflection quality is a surface-coherence problem as much as a bulk-identity problem

## Round 2 Comparative Results

### 1. The key optical variable sets are beginning to separate

Current dominant variable clusters appear to be:

- glass transmission: `R + S + D`
- metal reflection: `J + Q + B`
- crystal transmission: `R + J + structured S`
- defect scattering: `D + S + R`

This is a useful result because it means the model space is starting to generate differentiable behaviour rather than one flat explanation.

### 2. Boundary sensitivity is central, but not always the same way

`B` appears:

- very high in metal reflection
- high but underconstrained in transmissive boundary entry
- moderate in glass transmission

That supports the current family separation between transmission and reflection.

### 3. Defect sensitivity is a cross-cutting optical variable

`D` now looks like one of the most important support variables across multiple optical behaviours.

This makes the defect-responsive family more central than it first appeared.

### 4. Slip tolerance is likely more important for transmission than for reflection

This is an early but useful discrimination:

- transmission cases currently seem to require more pathway flexibility
- reflection cases seem to depend more on collective boundary response and strong coupling

## Current Strongest Optical Hypotheses

### Glass transmission

Best current hypothesis:

- a disordered but real whole can remain transmissive when distributed admissible pathways support propagation strongly enough despite defect sensitivity

### Metal reflection

Best current hypothesis:

- a metal reflects when a highly coupled whole produces a collective boundary response to incoming disturbance, with surface coherence strongly shaping the outcome

### Crystal vs glass difference

Best current hypothesis:

- crystal propagation depends on more regular nested admissibility
- glass propagation depends on more distributed permissive admissibility

## Most Underconstrained Areas

The weakest current areas are:

- transparent boundary entry and exit
- exact meaning of collective response
- exact geometric meaning of pathway admissibility in a disordered whole

These are now the next modelling bottlenecks.

## Recommended Next Move

The next correct artifact should be:

- `ams-optical-geometry-cases-v1.md`

That document should define a small number of geometry sketches for:

- regular nested transmissive order
- disordered transmissive order
- collective reflective boundary order
- defect-disrupted pathway order

That will be the next step toward more explicit mathematics.
