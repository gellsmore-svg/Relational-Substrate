# AMS Topological Geometry Toolchain and Vorton Simulator Plan v1

## Purpose

This note answers the current practical question:

```text
can existing topology, origami, or geometry software help model AMS vortons,
or do we need to write our own topological geometry simulator?
```

The short answer is:

```text
use existing software for pieces of the problem,
but build a custom AMS topology sandbox for the actual admissibility model.
```

Existing tools can help with knots, links, folds, persistence, triangulations, and visual intuition. They do not model AMS directly because AMS needs a special combination:

- stable closed topology
- non-closed transient propagation
- admissibility conditions
- pass / return / store / scatter / convert outcomes
- coupling into secondary material regimes
- no hidden material layer between substrate and vortons

## Guardrail

No software model should imply:

```text
T0 is made of cells, mesh elements, graph nodes, or material pellets.
```

Any mesh, graph, point cloud, curve sample, crease pattern, or triangulation is representation only.

The corrected AMS chain remains:

```text
continuous substrate
-> local organised disturbance
-> torsion/tension/alignment expression
-> candidate closure-pattern
-> stable primary topology/vorton
-> coupled vorton regimes
-> secondary material regimes
-> perceived matter
```

## Existing Software Categories

## 1. Knot and Link Software

### SageMath Knot Theory

Use for:

- knot objects
- braid construction
- Alexander and Jones polynomials
- determinants
- signatures
- basic invariant discipline

AMS value:

```text
helps discipline the idea that stable closed form needs invariants
```

Limit:

```text
does not simulate transient propagation, admissibility, or matter formation
```

### SnapPy

Use for:

- topology and geometry of 3-manifolds
- links
- hyperbolic structures
- command-line Python exploration

AMS value:

```text
useful for serious topology reference and link/manifold intuition
```

Limit:

```text
too specialised for the immediate AMS interaction sandbox
```

### Regina

Use for:

- low-dimensional topology
- 3- and 4-manifold triangulations
- knots and links
- normal surfaces
- Python bindings and GUI exploration

AMS value:

```text
useful for rigorous topology experiments and triangulated representations
```

Limit:

```text
triangulation must not be confused with substrate ontology
```

## 2. Persistent Topology Software

### GUDHI

Use for:

- persistent homology
- distinguishing persistent features from noise
- point-cloud topology
- filtration-based feature birth/death

AMS value:

```text
very useful analogue for the question:
when is a feature persistent enough to count?
```

Limit:

```text
persistent homology does not define vorton identity by itself
```

## 3. Origami and Folding Software

### Origami Simulator

Use for:

- interactive folding
- crease-pattern simulation
- strain visualisation
- fold percentage
- SVG/FOLD import and OBJ/STL export

AMS value:

```text
excellent analogy for admissible deformation, stored fold tension, and reseating
```

Limit:

```text
it models sheets and creases, not volumetric vorton closure
```

### ORIPA

Use for:

- crease-pattern drawing
- local flat-foldability checks
- folded-shape calculation from patterns
- FOLD/OPX/CP file workflows

AMS value:

```text
useful for rule-governed fold constraints and visual grammar
```

Limit:

```text
2D crease patterns are not AMS vortons
```

## What Existing Tools Cannot Do

Existing tools do not directly model:

- light-like open transients encountering closed topology
- admissibility as an AMS concept
- partial route split into admission, return, storage, scattering, and conversion
- vorton persistence as `I_profile` preservation
- coupling families becoming secondary material regimes
- perceived matter as interaction-bearing presentation

Therefore, existing tools are supporting tools, not the core modelling environment.

## Recommended Next Step

Build a custom browser-based AMS topology sandbox.

Why browser-based:

- fast visual feedback
- easy screenshots and demos
- Three.js handles 3D curves/tubes well
- easier to share with readers or reviewers
- can later export images for books

Working title:

```text
AMS Topology Sandbox
```

## Sandbox Aim

The first version should not try to be a physics engine.

It should model:

```text
closed stable form + open transient + admissibility outcome
```

This is the visual leap the books currently need.

## Core Objects

### 1. Closed Candidate

Represents a vorton candidate.

Visual form:

- torus knot
- loop
- braided loop
- nested loop
- deformable closed tube

State variables:

```text
C_class
W_sig
H_sig
R_map
B_env
Q_band
L_band
S_env
K_couple
M_reseat
F_modes
```

### 2. Open Transient

Represents light-like non-vorton propagation.

Visual form:

- open curve
- wave ribbon
- pulse tube
- phase-coloured path

State variables:

```text
coherence
frequency
amplitude
route direction
orientation/polarisation-like angle
fragmentation tendency
```

### 3. Boundary / Admissibility Region

Represents the region where the transient interacts with the closure-pattern.

Not a substrate cell.

State variables:

```text
J_bound
J_trans
K_store
Phi_lag
X_frag
L_leak
```

## First Interaction Outcomes

The sandbox should implement three canonical outcomes first:

### Option A: Admission

```text
open transient enters route
-> delays
-> exits coherently
```

Visual:

- path passes through or around the closed form
- colour shifts to show delay
- closure flexes but returns

### Option B: Return

```text
open transient reaches boundary
-> route incompatibility
-> reflected or redirected
```

Visual:

- incoming path bends away
- boundary flashes
- closed form remains stable

### Option C: Storage / Scattering / Conversion

```text
open transient partially admits
-> some stored
-> some scattered
-> some converted into local regime stress
```

Visual:

- part of path dims or fragments
- local stress glow appears
- closure may reseat or destabilise

## Minimal Metrics

First version metrics:

```text
admitted_fraction
returned_fraction
stored_fraction
scattered_fraction
closure_stress
coherence_loss
reseating_distance
identity_preserved
```

These map to AMS language:

```text
J_trans
J_bound
K_store
X_frag
B_env
Q_band
M_reseat
I_profile
```

## Minimal Versus Maximal

Minimal means:

```text
the smallest working rule set that distinguishes vorton,
non-vorton transient, admissibility, and failure.
```

Maximal would mean:

- exact substrate metric
- exact vorton species catalogue
- exact physical correspondence
- exact energy accounting
- exact mathematical topology solver
- full electromagnetic model

The sandbox should start minimal. Its job is to make conceptual distinctions visible.

## Suggested Technology

Use:

- Three.js for 3D rendering
- Vite for local app scaffolding if needed
- plain TypeScript or JavaScript
- simple curve and tube geometries
- GUI controls for admissibility variables

Avoid at first:

- full finite-element simulation
- full computational topology dependency
- heavy physics engine
- claims of physical proof

## Possible Later Tool Integration

Later, integrate external tools only where useful:

```text
SageMath -> knot invariant checks
GUDHI    -> persistence/noise experiments
ORIPA    -> fold/crease inspiration
Regina   -> topology reference checks
```

But do not block the first visual sandbox on these.

## First Build Scope

Build version `0.1` with:

1. A selectable closed form:
   - circle
   - trefoil-like torus knot
   - double loop

2. A selectable incoming transient:
   - straight pulse
   - sinusoidal pulse
   - ribbon pulse

3. Sliders:
   - boundary compatibility
   - route continuity
   - storage capacity
   - scattering tendency
   - reseating tolerance

4. Outputs:
   - admitted
   - returned
   - stored
   - scattered
   - identity preserved yes/no

5. Three scenario buttons:
   - Option A: admitted
   - Option B: returned
   - Option C: stored/scattered/converted

## Book Use

The sandbox can support the books by producing:

- screenshots
- explanatory diagrams
- clearer prose for admissibility
- examples of open vs closed order
- examples of stable matter as perceived interaction-bearing topology

The most important book-facing sentence remains:

```text
Light is open travelling order.
A vorton is closed stable order.
Matter is the perceived, interaction-bearing presentation of coupled stable order.
```

## Current Decision

Existing topology and origami tools are useful, but none is the right primary tool.

The next step should be:

```text
build a custom AMS topology sandbox v0.1
```

This is the most direct way to develop intuition, test rule language, and create book-ready visual explanations without smuggling material units into `T0`.

