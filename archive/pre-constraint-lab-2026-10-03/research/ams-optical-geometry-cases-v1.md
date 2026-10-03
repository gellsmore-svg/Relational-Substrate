# AMS Optical Geometry Cases v1

## Purpose

This document provides the first explicit geometry sketches for the AMS optical modelling programme.

The goal is not yet full mathematics. The goal is to move from:

- verbal family descriptions
- variable clusters

to:

- a small number of explicit geometric cases

These cases should give later mathematical work something sharper to formalise.

## Governing Rule

Each geometry case should:

- define a whole type
- define the key local-to-whole arrangement
- define what incoming propagation meets
- define what kind of outcome the geometry is supposed to support

The point is not to prove that one case is correct already. The point is to create a disciplined geometry space for comparison.

## Shared Geometric Primitives

The cases below are built from five primitives already established in the programme:

- local closure cell
- ring or loop path
- nested region
- boundary layer
- defect site

## Case G1: Regular Nested Transmissive Order

### Intended target

- crystal transmission

### Whole type

- ordered nested whole

### Geometric picture

- local closure cells are arranged in a regular nested pattern
- adjacency is highly structured
- admissible propagation paths recur in a stable, repeated order
- the boundary is real, but the bulk remains strongly ordered

### Main spatial properties

- high pathway regularity
- strong nested coherence
- relatively low ambiguity of local-to-local transition
- defect sites are local disruptions inside an otherwise regular field

### Expected optical behaviour

- coherent transmission
- lower scattering in ordered regions
- strong sensitivity to defects as local breaks in regular path continuity

### Main relevant variables

- high `R`
- high `J`
- structured moderate `S`
- moderate `B`
- low bulk `D`, high local `D` at defects

### Main model-family links

- `C`
- `G`
- `F`

### Pressure question

- can a regular nested order explain transmission without requiring perfect ideality?

## Case G2: Distributed Permissive Transmissive Order

### Intended target

- glass transmission

### Whole type

- disordered but real transmissive whole

### Geometric picture

- local closure cells remain viable
- adjacency is not regularly nested in the crystal sense
- propagation depends on distributed permissive routes rather than one repeated lattice grammar
- the whole remains coherent enough to transmit, but with greater sensitivity to defect and impurity conditions

### Main spatial properties

- lower long-range regularity
- higher pathway variability
- local viability without strict lattice repetition
- defect sites more easily redirect or degrade propagation quality

### Expected optical behaviour

- transmission remains possible
- clarity depends strongly on pathway continuity across a disordered whole
- scattering rises when local permissive continuity drops

### Main relevant variables

- moderate to high `R`
- moderate `J`
- moderate to high `S`
- moderate `B`
- high `D`

### Main model-family links

- `G`
- `D`
- `F`

### Pressure question

- what minimum distributed permissibility is needed for coherent transmission through disorder?

## Case G3: Collective Reflective Boundary Order

### Intended target

- metal reflection

### Whole type

- highly coupled whole with strong surface response

### Geometric picture

- local cells in the bulk are strongly coupled
- the surface region is not merely a line at the edge, but a boundary layer that participates collectively
- incoming disturbance is met by a coherent response from a strongly linked near-surface region

### Main spatial properties

- strong near-surface coupling
- very high boundary significance
- bulk order supports, but does not alone determine, the optical response
- surface defects alter collective response quality

### Expected optical behaviour

- strong reflection
- strong sensitivity to surface quality
- degraded or altered response when oxidation, roughness, or defect density changes the boundary layer

### Main relevant variables

- high `J`
- high `Q`
- very high `B`
- moderate to high `D`
- moderate `R`

### Main model-family links

- `H`
- `E`
- `F`

### Pressure question

- what exactly distinguishes a collective surface response from many local reflections happening in parallel?

## Case G4: Defect-Disrupted Pathway Order

### Intended target

- defect-sensitive scattering

### Whole type

- otherwise transmissive or responsive whole with local disruption sites

### Geometric picture

- a viable propagation or response field exists
- one or more defect sites locally alter adjacency, coupling, or pathway continuity
- the defect does not necessarily destroy the whole, but redirects or degrades the local passage of disturbance

### Main spatial properties

- local discontinuity inside a still-real whole
- redirection rather than full collapse in weaker cases
- propagation breakdown in stronger defect regimes

### Expected optical behaviour

- weak scattering
- strong scattering
- partial degradation of clarity
- localised optical distortion

### Main relevant variables

- very high `D`
- moderate `R`
- moderate `S`
- moderate `B`

### Main model-family links

- `F`
- `G`

### Pressure question

- when does a defect merely perturb propagation, and when does it destroy coherent pathway continuity?

## Case G5: Boundary Entry Transition Order

### Intended target

- entry into or exit from a transmissive medium

### Whole type

- interface between two admissibility fields

### Geometric picture

- one propagation-supporting region meets another region with different pathway grammar
- the boundary is thin enough to be an interface, but thick enough to matter as a layer
- incoming propagation must reconfigure its relation to the new medium

### Main spatial properties

- strong interface dependence
- not purely bulk, not purely point-like
- possible partial redirection or phase-like change without full reflection

### Expected optical behaviour

- modified entry
- partial redirection
- altered coherence conditions

### Main relevant variables

- high `B`
- moderate `R`
- moderate `S`
- moderate `Q`

### Main model-family links

- `E`
- `G`
- `D`

### Pressure question

- what geometric condition determines whether a boundary crossing remains transmissive or becomes more reflective or scattering?

## Case G6: Surface-Degraded Reflective Order

### Intended target

- loss or weakening of metallic reflection through oxidation or surface damage

### Whole type

- reflective boundary whole with degraded surface coherence

### Geometric picture

- the bulk whole remains strongly coupled
- the surface layer becomes mixed, rough, oxidised, or defect-heavy
- the collective response at the interface loses coherence even though metallic identity remains in the bulk

### Main spatial properties

- split between bulk persistence and surface degradation
- strong role for defect density
- strong role for changed boundary grammar

### Expected optical behaviour

- reduced reflectivity
- diffuse reflection
- mixed scattering

### Main relevant variables

- high `B`
- high `D`
- reduced effective `J` at boundary
- reduced effective `Q` at boundary

### Main model-family links

- `H`
- `E`
- `F`

### Pressure question

- how much surface degradation can occur before a reflective whole behaves optically like a different class of whole?

## Cross-Case Geometry Results

### 1. Transmission and reflection already require different geometric emphases

Current contrast:

- transmission cases emphasise:
  - pathway continuity
  - admissibility through the bulk
  - defect disruption
- reflection cases emphasise:
  - boundary-layer organisation
  - collective surface response
  - surface degradation

This is a good early sign that the optical programme is not forcing one geometry everywhere.

### 2. Disorder is not the same as incoherence

The glass case is important because it distinguishes:

- distributed permissive order

from:

- total random incoherence

That is one of the most important AMS optical claims now on the table.

### 3. Defects are geometrically central

The defect case is no longer a side issue. It is now part of the main geometry space for:

- transmission
- scattering
- reflection quality

### 4. Boundary layers need sharper mathematical treatment

The weakest current geometry remains:

- boundary entry / exit
- collective surface response

Those are now the main bottlenecks before stronger mathematics.

## Recommended Next Move

The next correct artifact should be:

- `ams-optical-parameter-sweep-v1.md`

That document should take the current geometry cases and ask:

- what happens when `R`, `S`, `B`, `D`, `J`, and `Q` are varied across low / medium / high regimes?

That will be the first real bridge from geometry sketches toward structured mathematical exploration.
