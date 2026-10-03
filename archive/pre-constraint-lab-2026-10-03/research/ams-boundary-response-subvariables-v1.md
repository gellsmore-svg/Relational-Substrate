# AMS Boundary Response Subvariables v1

## Purpose

This document refines the current optical variable set by decomposing the three most overloaded variables:

- `B` boundary sensitivity
- `J` coupling strength
- `Q` resonance compatibility

The parameter sweep showed that these variables are central, especially for:

- metal reflection
- transmissive boundary entry and exit
- degraded reflective surfaces

But it also showed that each variable is currently doing too much work at once.

This document therefore introduces subvariables so the next modelling round can distinguish more carefully between:

- different kinds of boundary behaviour
- different kinds of coupling
- different kinds of resonance

## Governing Rule

The goal is not to multiply variables without discipline.

The goal is to split only where the current variables are clearly conflating distinct behaviours.

Each subvariable therefore has to earn its place by helping discriminate:

- reflection from transmission
- bulk coherence from surface coherence
- transmissive entry from reflective return
- stable resonance from destabilising resonance

## Refining `B`: Boundary Sensitivity

The current variable `B` is too coarse.

It now needs to be split into at least four subvariables.

## `B_in` = Boundary Entry Sensitivity

### Meaning

How strongly incoming propagation is altered when it first enters a new medium or whole.

### Why it matters

This is distinct from reflection. A medium may strongly alter entry conditions without becoming strongly reflective.

### Main use cases

- transparent boundary entry
- crystal entry
- glass entry
- membrane transport analogies

### Early interpretive range

- low `B_in`: entry changes little
- high `B_in`: entry strongly reshapes propagation

## `B_out` = Boundary Exit Sensitivity

### Meaning

How strongly propagation is altered when it exits a whole or medium.

### Why it matters

Exit conditions are not always equivalent to entry conditions.

### Main use cases

- transmission out of glass
- transmission out of crystal
- boundary-mediated loss of coherence

### Early interpretive range

- low `B_out`: exit is comparatively smooth
- high `B_out`: exit strongly reshapes or degrades propagation

## `B_ref` = Reflective Boundary Sensitivity

### Meaning

How strongly a boundary favours reflective rather than transmissive response.

### Why it matters

This is one of the most important new subvariables. Reflection cannot be modelled well if it stays buried inside generic boundary sensitivity.

### Main use cases

- metal reflection
- degraded metallic surfaces
- reflective vs transmissive interface comparison

### Early interpretive range

- low `B_ref`: boundary not strongly reflective
- high `B_ref`: boundary strongly favours reflective response

## `B_coh` = Boundary Coherence Dependence

### Meaning

How strongly the optical or functional behaviour depends on preserving coherent order specifically in the boundary layer.

### Why it matters

This distinguishes:

- surfaces that still function under roughness or mild disorder

from:

- surfaces whose behaviour collapses quickly when boundary coherence is lost

### Main use cases

- metal surface quality
- catalytic surfaces
- membrane integrity

### Early interpretive range

- low `B_coh`: surface behaviour tolerates disorder
- high `B_coh`: surface behaviour requires strong coherence

## Refining `J`: Coupling Strength

The current variable `J` is too broad because it mixes:

- local neighbour coupling
- distributed whole coupling
- surface-layer coupling

These are not always the same thing.

## `J_loc` = Local Coupling Strength

### Meaning

How strongly one local closure cell constrains its immediate neighbours.

### Why it matters

This is the baseline coupling variable for grouped micro-organisation.

### Main use cases

- T1B local stability
- local propagation continuity
- local defect impact

## `J_dist` = Distributed Whole Coupling

### Meaning

How strongly the larger whole redistributes disturbance or maintains coherence beyond local neighbours.

### Why it matters

This is essential for distinguishing:

- a real higher-order whole

from:

- many only-locally coupled units

### Main use cases

- crystals
- glasses
- metals
- membranes
- organismal wholes

## `J_surf` = Surface-Layer Coupling

### Meaning

How strongly the near-surface region behaves as a linked response zone rather than as loosely related local sites.

### Why it matters

This is probably central for metal reflection.

### Main use cases

- reflective boundaries
- catalytic surfaces
- surface degradation

## Refining `Q`: Resonance Compatibility

The current variable `Q` also needs splitting because it currently mixes:

- stable coherent resonance
- collective response readiness
- destabilising amplification

These must be distinguished.

## `Q_coh` = Coherent Resonance Compatibility

### Meaning

How readily a regime can sustain useful coherent dynamic participation without becoming unstable.

### Why it matters

This is the “good” side of resonance.

### Main use cases

- dynamic transmission support
- membrane-linked function
- organised living systems

## `Q_coll` = Collective Response Readiness

### Meaning

How readily many local regions can participate together in a whole-level dynamic response.

### Why it matters

This is likely more central to metal reflection than generic resonance compatibility.

### Main use cases

- metal reflection
- whole-surface response
- some whole-level dynamic effects

## `Q_dest` = Destabilising Resonance Susceptibility

### Meaning

How easily a regime enters instability, amplification, or destructive oscillation under repeated forcing.

### Why it matters

This is the “danger” side of resonance and should not remain hidden inside positive resonance language.

### Main use cases

- defect-driven scattering
- unstable oscillation
- degraded reflective surfaces
- metastable optical transitions

## First Rewritten Optical Profiles

The point of the subvariables is to rewrite the earlier benchmark profiles more precisely.

## Glass Transmission

Earlier profile:

- `R + S + D`

Now refined as:

- moderate to high `R`
- medium to high `S`
- medium `B_in`
- medium `B_out`
- low `B_ref`
- medium `J_loc`
- medium `J_dist`
- high `D`
- medium `Q_coh`
- low to medium `Q_dest`

Interpretive gain:

- glass can now be described as transmissive with meaningful entry/exit effects and high defect sensitivity without being forced into reflective boundary logic

## Crystal Transmission

Earlier profile:

- `R + J + structured S`

Now refined as:

- high `R`
- medium `S`
- medium `B_in`
- medium `B_out`
- low `B_ref`
- high `J_loc`
- high `J_dist`
- low bulk `D`, high defect-site `D`
- medium `Q_coh`
- low `Q_dest`

Interpretive gain:

- crystal transmission now looks more clearly like propagation through a highly distributed but still strongly ordered whole

## Metal Reflection

Earlier profile:

- `J + Q + B`

Now refined as:

- medium `R`
- low to medium `S`
- high `B_ref`
- very high `B_coh`
- high `J_surf`
- high `J_dist`
- moderate `D`
- high `Q_coll`
- medium `Q_dest`

Interpretive gain:

- metal reflection now looks less like “high boundary sensitivity” in general and more like a surface-coherent collective-response case

## Degraded Reflective Surface

Earlier profile:

- `B + D + J + Q`

Now refined as:

- reduced effective `B_coh`
- reduced effective `J_surf`
- reduced effective `Q_coll`
- increased effective `D`
- increased `Q_dest`

Interpretive gain:

- degradation can now be modelled as a loss of surface coherence and collective response, not only as a vague increase in disorder

## Main Gains From The Subvariable Split

### 1. Reflection is now more sharply distinguished from entry effects

This is one of the biggest improvements.

Earlier, generic `B` mixed:

- transmissive entry
- transmissive exit
- reflective response
- surface coherence dependence

That was too much.

### 2. Collective response is now distinguished from generic resonance

This also matters a great deal.

Metal reflection now looks less like “resonance somewhere” and more like:

- high collective response readiness in a surface-coherent boundary layer

### 3. Whole coupling is now separated from surface coupling

This helps prevent confusion between:

- a strongly coherent bulk whole

and:

- a surface that must respond as a linked layer for reflection to remain strong

## Current Most Useful Subvariables

At this stage, the most useful new subvariables appear to be:

- `B_ref`
- `B_coh`
- `J_surf`
- `Q_coll`
- `Q_dest`

These are likely the main variables that will sharpen the optical work fastest.

## Remaining Weaknesses

Even after the split, several areas remain underconstrained:

- the exact geometric meaning of `J_surf`
- the difference between medium and high `Q_coll`
- how `B_in` and `B_out` should vary across real transmissive media

These are now the next modelling bottlenecks.

## Recommended Next Move

The next correct artifact should be:

- `ams-optical-parameter-sweep-v2.md`

That document should rerun the main optical cases using the new subvariables:

- `B_in`
- `B_out`
- `B_ref`
- `B_coh`
- `J_loc`
- `J_dist`
- `J_surf`
- `Q_coh`
- `Q_coll`
- `Q_dest`

That will be the first genuinely sharper parameter pass in the optical sub-programme.
