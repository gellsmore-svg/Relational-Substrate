# AMS Vorton Coupling Family Matrix and Electrical Modelling Entry v1

## Purpose

This note does two jobs.

First, it defines a first-pass coupling-family matrix: how different vorton profile features could generate locked, slip-tolerant, route-bearing, alignment, and boundary regimes.

Second, it opens the practical modelling question raised in conversation: if the substrate cannot be seen directly, where might AMS materially change how we analyse a real system? The best first test case is high-frequency AC across mixed conductive and dielectric paths, because standard circuit language often collapses a composite route into lumped quantities while AMS pushes attention toward constraint location, route partition, storage, boundary stress, and frequency/amplitude-dependent evenness.

## Conversation Constraint

The recent supporting research failed where it inserted material-like things between substrate and vortons without explaining how those things came into being.

This note therefore obeys the corrected chain:

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

No hidden substrate cells, graph nodes, or material pellets are allowed between `T0` and vortons.

## Coupling-Family Matrix

Stable vorton identities may couple into secondary regimes through repeatable compatibility relations.

The first-pass matrix is:

| Coupling family | Dominant profile features | `T2` regime tendency | Electrical relevance | Optical relevance | Magnetic relevance | Main failure risk |
|---|---|---|---|---|---|---|
| Locked | high `B_env`, low `M_reseat`, narrow `Q_band` | rigid/solid-like regimes | low slip, high bottleneck stress | reflection/capture at hard boundaries | pinned alignment | brittleness, fracture, overconstraint |
| Slip-tolerant | moderate `B_env`, high `M_reseat`, recoverable `Q_band` | deformable/fluid-like regimes | route reseating, conduction support | absorption or adaptive delay | domain movement support | diffusion, incoherent slip |
| Route-bearing | high `J_trans`, repeatable `K_couple`, low route loss | conductive/transmissive regimes | low-barrier paths, AC routing | transmission, guided propagation | alignment propagation | overload, heating, route fragmentation |
| Storage-bearing | high lock capacity, delayed release, bounded leakage | dielectric/capacitive regimes | polarisation, charge storage, phase lag | capture/release, dispersion | weak or delayed alignment response | leakage, relaxation, breakdown |
| Alignment-bearing | strong orientation relation, stable `H_sig`, coherent group response | magnetic/polar regimes | induction-like coupling | polarisation-sensitive response | domains, remanence, hysteresis | depinning, reversal, incompatible adjacency |
| Boundary-bearing | strong boundary fit, high `J_bound`, asymmetric route partition | surfaces/interfaces | contact impedance, dielectric interfaces | reflection/refraction/scattering | domain walls, phase boundaries | interface stress, scattering, delamination-like failure |

These are not vorton species. They are coupling families: ways stable primary topology can organise into secondary material behaviour.

## Why This Matters For Electrical Modelling

Standard circuit modelling is powerful. AMS should not pretend otherwise.

The question is narrower:

```text
where does AMS change modelling emphasis enough to suggest a different experiment,
different variable, or different design heuristic?
```

For ordinary DC or low-frequency circuits, AMS may mostly restate known constraint logic:

- current is limited by the strongest bottleneck
- reducing non-bottleneck resistance can increase stress at the bottleneck
- composite resistance hides local constraints
- heating and failure concentrate at route weaknesses

That does not yet give AMS a distinctive modelling advantage.

The more promising case is high-frequency AC, especially where conductors, dielectrics, interfaces, geometry, and frequency-dependent response interact.

## AMS Electrical Reframe

Instead of treating electricity primarily as stuff flowing through wire, AMS should model electrical behaviour as:

```text
ordered route reseating under constraint
```

The useful variables are:

```text
R_route      ordinary route resistance or dissipation
K_store      storage/lock-up capacity
J_trans      transition quality along the route
J_bound      boundary/interface quality
Q_even       evenness of response across frequency/amplitude
L_leak       leakage tendency
X_frag       fragmentation or incoherence tendency
B_bottle     bottleneck severity
P_stress     local route pressure/stress at constraint points
Phi_lag      phase lag or delayed release
```

These are AMS-facing modelling variables, not new ontology.

## Constraint-First Circuit View

A composite electrical path should be read as:

```text
source drive
-> route admission
-> local reseating chain
-> bottleneck stress
-> storage/return/dissipation at interfaces
-> system relaxation or oscillation
```

The primary design question becomes:

```text
where does unresolved reconfiguration accumulate?
```

Not only:

```text
what is the total resistance or impedance?
```

The total value remains useful. It is just not the whole explanatory object.

## High-Frequency AC Entry Point

High-frequency AC is a good AMS test case because the system is repeatedly driven away from rest and asked to reseat in alternating directions.

Important questions:

1. Does the route respond evenly across frequency?
2. Does the route respond evenly across amplitude?
3. Where does phase lag concentrate?
4. Where does stored mismatch fail to release cleanly?
5. Where do interfaces dominate over bulk path properties?
6. Where does geometry matter more than lumped resistance?
7. Where does local heating or noise indicate route fragmentation?

AMS expects dielectric and boundary behaviour to be especially important because blocked slip and stored mismatch are not side effects. They are central route outcomes.

## Candidate AMS AC Variables

### 1. Route Evenness `Q_even`

`Q_even` measures how consistently a path responds across frequency and amplitude.

```text
high Q_even -> stable response across drive variation
low Q_even  -> frequency/amplitude-sensitive distortion, lag, or loss
```

Possible classical correlates:

- flat impedance response
- low phase distortion
- low dielectric loss variation
- low amplitude-dependent nonlinearity

### 2. Bottleneck Severity `B_bottle`

`B_bottle` measures the severity of the strongest local constraint in a composite route.

```text
B_bottle = max(local constraint stress / local tolerance)
```

AMS design heuristic:

```text
optimising the average route may increase stress at the bottleneck
unless the bottleneck itself is relieved
```

### 3. Storage/Lock-Up Capacity `K_store`

`K_store` measures how much mismatch a region can store reversibly.

High `K_store` can be useful in capacitive behaviour, but harmful if release is delayed, lossy, or nonlinear.

### 4. Boundary Junction Quality `J_bound`

`J_bound` measures how cleanly a route crosses a material boundary or interface.

For high-frequency AC, this may matter more than bulk resistance because repeated reversals stress interfaces continuously.

### 5. Transition Quality `J_trans`

`J_trans` measures route continuity through the path.

In conductor-like paths:

```text
high J_trans -> smooth reseating
low J_trans  -> discontinuity, scattering, heating, lag, failure
```

### 6. Leakage and Fragmentation `L_leak`, `X_frag`

`L_leak` measures route loss.

`X_frag` measures incoherent route breakup.

In AC terms, these may appear as:

- heat
- noise
- dielectric loss
- harmonic distortion
- frequency-dependent attenuation
- phase instability

### 7. Phase Lag `Phi_lag`

`Phi_lag` measures delayed release or delayed reseating.

Classical impedance already includes phase, but AMS asks where the lag is physically concentrated and whether it arises from route storage, boundary lock-up, or distributed reseating delay.

## SPICE Question

SPICE is still useful, but not as a direct AMS simulator.

It can model:

- lumped resistance
- capacitance
- inductance
- transmission lines
- parasitics
- frequency response
- nonlinear components if specified

It does not automatically model:

- substrate-level route reseating
- vorton identity
- local admissibility mismatch
- hidden interface stress unless represented by circuit elements
- geometry/material microstructure unless abstracted into components

So the practical route is:

```text
use SPICE as a classical response engine
wrap it with AMS-derived variables and equivalent subcircuits
compare whether AMS-guided decompositions explain behaviour better
than simpler lumped models
```

## Modelling Strategy Without Lab Equipment

A useful no-lab modelling programme is:

### Phase 1: Equivalent-Circuit Decomposition

Start with simple SPICE models:

- resistor only
- resistor plus parasitic capacitance
- resistor plus parasitic inductance
- conductor-dielectric interface as RC element
- distributed RC ladder
- transmission line with loss
- nonlinear capacitor or voltage-dependent dielectric proxy

Then interpret each element through AMS variables:

```text
R  -> dissipative route loss
C  -> reversible storage/lock-up
L  -> reluctance to rapid route-rate change
RC ladder -> distributed storage and release
transmission line -> route delay and reflection
nonlinear C -> amplitude-dependent storage
```

### Phase 2: Frequency Sweep

Sweep frequency and record:

- impedance magnitude
- phase
- resonance
- attenuation
- bandwidth
- group delay where possible

AMS question:

```text
which model has higher Q_even across the intended range?
```

### Phase 3: Amplitude Sweep

Add nonlinear proxies and sweep amplitude.

AMS question:

```text
does the route remain even, or does storage/release become amplitude-dependent?
```

### Phase 4: Bottleneck Injection

Insert a single constraining element into an otherwise good route.

Examples:

- small series resistance
- lossy dielectric shunt
- poor contact model
- small nonlinear capacitance
- local inductive discontinuity

AMS question:

```text
does improving the rest of the route increase stress at the bottleneck?
```

### Phase 5: Interface-Dominant Comparison

Compare:

```text
same total impedance, different distribution
```

Example:

- one model has evenly distributed loss/storage
- another has the same total loss/storage concentrated at an interface

AMS prediction:

```text
the concentrated-interface model should show worse evenness,
more phase distortion, more local stress, or narrower tolerance
even when simple totals match
```

This is a place where AMS may generate a distinctive design heuristic.

## Where AMS Might Differ In Practice

AMS is unlikely to beat classical circuit theory by denying it.

It may differ by insisting on variables that lumped analysis can hide:

- location of constraint
- distribution of storage
- interface quality
- release timing
- amplitude dependence
- route evenness
- bottleneck stress
- failure mode

The practical claim would be:

```text
for high-frequency AC, the best path is not merely the lowest-resistance path
but the path with the most even, least fragmenting, least bottlenecked route response
across the relevant frequency and amplitude range
```

## Design Heuristics To Test

1. Do not optimise only total impedance. Optimise distribution of constraint.
2. Prefer distributed, low-stress storage over concentrated boundary lock-up.
3. Treat interfaces as active route regions, not passive joins.
4. Identify bottlenecks before lowering resistance elsewhere.
5. Optimise `Q_even` across the actual operating range, not only at a nominal frequency.
6. Compare same-total-impedance designs with different internal distributions.
7. Track phase lag as a route-location problem, not only a scalar circuit output.

## Relation Back To Vortons

This electrical modelling entry does not require naming vorton species yet.

The vorton relation is:

```text
stable primary topology
-> coupling family
-> route-bearing or storage-bearing secondary regime
-> electrical behaviour
```

The point is not that current is vorton motion.

The point is that a material path's electrical behaviour depends on how stable primary topology has coupled into secondary route regimes.

## Current Status

This note creates a bridge from vorton coupling families to practical high-frequency AC modelling.

It does not prove AMS.

It gives a way to start looking for AMS-relevant differences without laboratory equipment:

- build classical equivalent models
- introduce AMS variables as interpretive overlays
- compare distributed vs concentrated constraint
- focus on frequency/amplitude evenness
- treat dielectrics and interfaces as central

The next useful step is to create a SPICE-oriented experiment plan with specific circuits, sweep parameters, and expected AMS-relevant observations.

