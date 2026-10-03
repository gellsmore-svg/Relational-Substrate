# AMS Vorton Species Discrimination Framework v1

## Purpose

This note defines a first-pass framework for discriminating vorton species without turning vortons into particles, substrate cells, or hidden material pellets.

The aim is not to catalogue finished vorton species. The aim is to define what would have to differ for two stable vorton candidates to count as different species.

## Governing Rule

A vorton species is not defined by appearance, size, analogy, or narrative role.

A vorton species is defined by a stable and discriminable invariant profile:

```text
species(V) depends on I_profile(V)
```

where `I_profile` includes:

- closure class
- winding or return signature
- handedness or orientation signature
- return-path map
- boundedness envelope
- coherence tolerance band
- leakage tolerance band
- stability envelope
- coupling behaviour
- permitted reseating modes
- characteristic failure modes

## Species, State, and Context

AMS must distinguish three things.

### Species

A species-level difference changes the identity class of the vorton.

Examples of possible species-level differences:

- different closure class
- incompatible return signature
- different invariant orientation structure
- different coupling grammar
- different permitted reseating family
- different characteristic failure modes

### State

A state-level difference changes current condition without changing species.

Examples:

- stressed vs relaxed
- rotated vs unrotated
- coupled vs isolated
- high route load vs low route load
- near-threshold vs comfortably stable

### Context

A context-level difference comes from the surrounding regime rather than the vorton species itself.

Examples:

- neighbouring support
- boundary pressure
- route load
- secondary material arrangement
- external perturbation

The same species may behave differently in different contexts. That is not automatically a species difference.

## Minimal Discrimination Test

Two stable vorton candidates `V_a` and `V_b` count as different species only if at least one core profile component differs outside identity-preserving tolerance.

First-pass rule:

```text
species(V_a) != species(V_b)
iff
D_profile(I_profile(V_a), I_profile(V_b)) > D_species
```

Where `D_profile` is a structured difference measure, not a single finished equation.

## Core Difference Axes

### 1. Closure-Class Difference

Ask:

```text
Do the candidates close in the same way?
```

Possible differences:

- local closure vs distributed closure
- single return vs multiple return
- nested closure vs simple closure
- braided closure vs unbraided closure
- externally supported closure vs self-supported closure

Closure-class difference is a strong species discriminator.

### 2. Return-Signature Difference

Ask:

```text
Does the pattern return to itself with the same recurrence structure?
```

Possible differences:

- different return count
- different recurrence order
- different path dependency
- different tolerance under perturbation

Return-signature difference is a strong species discriminator if it persists when context changes.

### 3. Orientation or Handedness Difference

Ask:

```text
Does the candidate preserve a different orientation signature?
```

Possible outcomes:

- same species, opposite handed state
- paired species
- genuinely different species

This requires care. Opposite handedness might be a state, a counterpart, or a species distinction depending on whether coupling, reseating, and failure modes also change.

### 4. Stability-Envelope Difference

Ask:

```text
Do the candidates persist under different condition ranges?
```

Possible differences:

- different perturbation tolerance
- different leakage tolerance
- different boundary pressure tolerance
- different route-load tolerance

Stability-envelope difference alone is not always enough for species distinction. It may be a state or context effect unless tied to invariant profile difference.

### 5. Coupling-Grammar Difference

Ask:

```text
Do the candidates couple differently to other stable closures?
```

Possible differences:

- align vs counter-align
- bind vs repel
- transmit vs block
- store vs release
- support route continuity vs fragment routes

Coupling behaviour is a major species discriminator because it is the main bridge from primary topology to secondary material regimes.

### 6. Reseating-Mode Difference

Ask:

```text
Can the candidates adjust in the same identity-preserving ways?
```

Possible differences:

- one can slip, the other cannot
- one can rotate without identity loss, the other fragments
- one tolerates boundary reseating, the other collapses
- one can shift coupling mode, the other is locked

Different permitted reseating modes often indicate different species or at least different families.

### 7. Failure-Mode Difference

Ask:

```text
How do the candidates fail?
```

Possible differences:

- diffuse failure
- collapse failure
- fragmentation failure
- overconstraint failure
- underreturn failure
- incompatible-adjacency failure

Failure modes are not secondary detail. They reveal what kind of closure the candidate actually has.

## Species Family

A vorton family is a group of species that share a higher-order profile pattern.

Example family criteria:

```text
same broad closure class
similar return-path grammar
similar coupling role
different detailed stability envelopes or reseating modes
```

Families are useful only if they help explain material regimes. They should not become loose metaphorical groups.

## Species Versus Material Element

Vorton species are not chemical elements.

Chemical elements are `T2` material regimes built from stable primary topology and secondary organisation.

A chemical element may depend on:

- multiple vorton species
- repeated coupling patterns
- route-bearing secondary topology
- boundary and interaction behaviour

Therefore:

```text
vorton species != element
```

The relation should be:

```text
vorton species and coupling grammar
-> secondary regimes
-> material families
-> elements and compounds
```

## Species Versus Particle

Vorton species are not ordinary particle species.

If AMS later maps some vorton species or coupled regimes onto conventional particle descriptions, that mapping must be treated as a correspondence problem, not as an immediate identity claim.

Do not write:

```text
this vorton species is simply electron/proton/neutron
```

Write:

```text
this vorton species or coupled regime may correspond to part of the behaviour conventionally described as ...
```

until stronger mapping work exists.

## Discrimination Matrix

Use this table when evaluating candidates.

| Axis | Same species if | Different species if | Caution |
|---|---|---|---|
| Closure class | same closure grammar | closure relation differs outside tolerance | context can distort closure |
| Return signature | same recurrence structure | return structure changes identity | transient loops can imitate return |
| Handedness/orientation | reversible state difference | orientation changes coupling/failure class | may define counterpart rather than species |
| Boundedness envelope | same tolerance family | different retention regime | stress state can mimic difference |
| Coherence band | same recovery behaviour | different conflict tolerance | environment can degrade coherence |
| Leakage band | same loss tolerance family | different leakage identity | boundary pressure matters |
| Stability envelope | same persistence range type | different stability class | state vs species must be separated |
| Coupling grammar | same relation behaviour | bind/block/align roles differ | `T2` context can mask identity |
| Reseating modes | same identity-preserving moves | different allowable moves | locked state is not always species |
| Failure modes | same failure family | distinct characteristic failure | failure test may require perturbation |

## Candidate Naming Rule

Do not name a vorton species until the profile is filled.

Temporary labels may be used:

```text
candidate A
candidate B
closure class 1
return-family 2
proto-family X
```

Avoid:

```text
electron-vorton
magnet-vorton
light-vorton
wood-vorton
spirit-vorton
```

until a controlled correspondence framework exists.

## Mechanism Preservation

Species discrimination must preserve the substrate-to-matter mechanism:

```text
continuous substrate
-> stable primary topology/vorton species
-> coupling grammar
-> secondary material regimes
-> perceived matter
```

If a proposed species does not help explain how stable primary topology can couple into material regimes, its role in AMS is unclear.

## Current Status

This framework defines what vorton species discrimination requires.

It does not yet provide:

- a finished species catalogue
- exact numerical thresholds
- a substrate metric
- a particle correspondence map
- a chemical element mapping

The next useful step is a coupling-family matrix: how candidate vorton profile differences could generate locked, slip-tolerant, route-bearing, alignment, and boundary regimes.

