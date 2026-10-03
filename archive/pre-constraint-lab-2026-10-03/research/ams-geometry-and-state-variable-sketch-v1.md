# AMS Geometry and State-Variable Sketch v1

## Purpose

This document provides the first geometry and variable sketch for the AMS experimental modelling programme.

It is not yet a finished mathematical formalism.

Its purpose is to reduce vagueness by giving the current model families:

- a shared geometric vocabulary
- clearer variable meanings
- first distinctions for later mathematical experiments

## Governing Rule

At this stage, the variables should be:

- simple enough to use
- distinct enough to compare families
- revisable later

This sketch should therefore be treated as:

- disciplined scaffolding

not final mathematics.

## Geometric Primitives

The current programme needs a small set of geometric primitives.

### 1. Local Closure Cell

The smallest candidate region in which a closure can form and be evaluated for viability.

Questions:

- does local circulation close?
- does strain remain bounded?
- is return-path continuity present?

### 2. Ring Or Loop Path

A recurrent or distributed relation path capable of supporting closure across more than one local cell.

Questions:

- is the loop complete?
- is strain evenly or unevenly distributed?
- does the loop support distributed persistence?

### 3. Nested Region

A region in which smaller closures participate in a larger enclosing organisation.

Questions:

- is the whole more than many local closures side by side?
- does disturbance redistribute across the whole?

### 4. Boundary Layer

The transition region where a whole meets:

- another medium
- a surface
- an interface
- an external forcing condition

Questions:

- is the boundary constitutive or secondary?
- does it transmit, reflect, scatter, or destabilise?

### 5. Defect Site

A local disruption in otherwise viable ordered relation.

Questions:

- does the defect remain local?
- does it nucleate wider change?
- does it alter propagation or memory?

## State Variables

## `T` = Torsion Magnitude

### Meaning

How strongly local closure involves torsional deformation or twist.

### Early use

- low `T`: weakly twisted regime
- high `T`: strongly twisted regime

### Questions

- does higher `T` improve persistence?
- when does higher `T` become collapse-prone?

## `C` = Closure Tightness

### Meaning

How strongly a local or distributed regime closes upon itself.

### Early use

- low `C`: weak or leaky closure
- high `C`: tightly locked regime

### Questions

- when does low `C` produce diffusion?
- when does high `C` become overconstrained?

## `R` = Return-Path Strength

### Meaning

How strongly strain or circulation can return through a viable path rather than dissipating or collapsing.

### Early use

- low `R`: underreturned regime
- high `R`: strongly self-reseating regime

### Questions

- which families are most sensitive to `R`?
- does optical propagation require high `R` at the whole level or only locally?

## `K` = Knotting / Linking Complexity

### Meaning

How much the closure depends on non-trivial linking, looping, or topological entanglement rather than simple local circulation alone.

### Early use

- low `K`: simple loop or local closure
- moderate `K`: ring or distributed loop complexity
- high `K`: nested or strongly linked regimes

### Questions

- which cases genuinely need higher `K`?
- where does higher `K` improve stability and where does it introduce fragility?

## `J` = Coupling Strength

### Meaning

How strongly one closure cell or region constrains neighbouring regions.

### Early use

- low `J`: weakly coupled
- high `J`: strongly coupled

### Questions

- when does high `J` yield higher-order whole formation?
- when does low `J` leave only loose aggregation?

## `S` = Slip Tolerance

### Meaning

How much local reseating or relational adjustment can occur without destroying the identity of the regime.

### Early use

- low `S`: brittle regime
- high `S`: flexible regime

### Questions

- does glass require more `S` than crystal for transmission?
- does membrane function depend on high boundary `S`?

## `Q` = Resonance Compatibility

### Meaning

How readily a regime can participate in or sustain coherent dynamic response under repeated forcing or oscillatory relation.

### Early use

- low `Q`: weak resonant participation
- high `Q`: strong resonant coherence

### Questions

- when does high `Q` stabilise?
- when does high `Q` become unstable oscillation?

## `B` = Boundary Sensitivity

### Meaning

How strongly behaviour changes when the regime encounters an interface or surface.

### Early use

- low `B`: boundary-insensitive
- high `B`: boundary-critical

### Questions

- does metal reflection require very high `B`?
- does glass transmission require moderate boundary `B` but stronger bulk pathway permissibility?

## `D` = Defect Sensitivity

### Meaning

How strongly local defects or discontinuities alter the behaviour of the regime.

### Early use

- low `D`: defects remain local
- high `D`: defects strongly alter whole behaviour

### Questions

- which optical benchmarks depend most on `D`?
- which higher-order wholes remain robust despite high local defect presence?

## `M` = Memory Retention

### Meaning

How strongly prior alignment, strain, defect history, or forcing remains active in the current state.

### Early use

- low `M`: little retained history
- high `M`: strong path dependence or hysteresis

### Questions

- which material and biological cases require high `M`?
- how should `M` interact with `D` and `B`?

## First Family Sketches Using Variables

### Family G: Pathway-Selective Propagation Closure

Likely profile:

- moderate `T`
- moderate `C`
- moderate to high `R`
- moderate `J`
- moderate to high `S`
- moderate `Q`
- moderate `B`
- high `D`
- low to moderate `M`

Interpretive note:

- propagation depends on enough admissible pathway continuity for coherence without requiring crystal-like regularity

### Family H: Collective Surface-Response Closure

Likely profile:

- moderate `T`
- moderate `C`
- high whole-level `R`
- high `J`
- low to moderate `S`
- high `Q`
- very high `B`
- moderate to high `D`
- moderate `M`

Interpretive note:

- the whole responds collectively at the interface, making reflection a surface-whole event rather than only a local event

### Family F: Defect-Responsive Closure

Likely profile:

- variable `T`
- variable `C`
- moderate `R`
- moderate to high `J`
- low to moderate `S`
- variable `Q`
- high `B`
- very high `D`
- high `M`

Interpretive note:

- defect and history are not perturbations after the fact; they are part of the state description

## First Optical Variable Heuristics

These are not equations yet. They are first heuristics.

### Glass Transmission

Likely requires:

- adequate `R`
- moderate to high pathway `S`
- moderate `Q`
- high `D`
- medium `B`

Interpretive idea:

- propagation remains possible if the whole still supports distributed admissible pathways despite disorder

### Metal Reflection

Likely requires:

- high `J`
- high `Q`
- very high `B`
- moderate to high `D`

Interpretive idea:

- reflection emerges when the surface region of a strongly coupled whole responds collectively at the boundary

### Crystal Transmission

Likely requires:

- high `R`
- lower but more structured `S`
- lower disorder in pathway layout
- significant `D` at defect sites

Interpretive idea:

- propagation occurs through more regular and nested whole-order than in glass

## Immediate Use

This sketch is now enough to support the next cycle of work:

- the experiment log can start referencing variables explicitly
- the optical benchmarks can begin to compare family profiles rather than only verbal analogies
- later mathematical work can decide which of these variables need formal relationship, constraint, or elimination

## Recommended Next Move

The next correct artifact should be:

- `ams-optical-experiment-log-round-2.md`

That document should rerun the current optical benchmarks using:

- family combinations
- first variable profiles
- explicit statements of where the variables are still too vague
