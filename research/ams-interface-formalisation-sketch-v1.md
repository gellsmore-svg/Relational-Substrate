# AMS Interface Formalisation Sketch v1

## Purpose

This document begins the first compact formalisation pass over the now-stabilised AMS interface framework.

It does **not** attempt full mathematics.

Its purpose is narrower:

- define a compact notation layer
- reduce repeated prose load
- make the framework easier to reuse across cases
- preserve explicit distinctions without pretending the programme is already fully quantified

This is therefore a formalisation sketch, not a completed formal theory.

## Scope

The sketch covers:

- primitive variables
- derived terms
- geometric descriptors
- local zone types
- loop families
- route classes
- obstruction classes
- dominance modes
- transition-flow notation
- route-reality grades

## Formalisation Principles

### 1. Keep primitives few

Do not multiply primitive symbols unnecessarily.

### 2. Keep descriptors explicit

Some terms are useful but not yet primitive. They should remain tagged as descriptors.

### 3. Separate state, structure, and outcome

The notation should distinguish:

- what is locally present
- how it is organised
- what it tends to do

### 4. Avoid false precision

No symbolic expression here should imply a settled equation where none exists yet.

## Symbol Set

## Primitive Interface Variables

- `B_in`
  - admission capacity into a receiving whole
- `B_out`
  - release capacity out of a source whole
- `J_bound`
  - immediate boundary-face coupling
- `J_trans`
  - through-layer transition continuity
- `Q_coh`
  - coherence preservation / compatibility
- `D`
  - defect burden / defect-sensitive obstruction field

## Derived Interface Term

- `I_comp`
  - interface compatibility as a higher-order descriptor of viable joint handoff

This should currently be treated as:

- derived
- comparative
- not primitive

## Geometric Descriptors

- `L_depth`
  - penetration depth of the active event into the layer
- `L_span`
  - lateral spread of the active event
- `L_loop`
  - dominant loop geometry class
- `L_escape`
  - viability of completion routes still available to the event

These remain:

- descriptors
- not primitives

## Local Zone Notation

The current mixed-interface zone set is:

- `Z_A`
  - route-dominant zone
- `Z_B`
  - pocket-dominant zone
- `Z_C`
  - diffusing fringe

## Informal Zone Signatures

### `Z_A`

Typical profile:

- real route leverage present
- `L_escape` real
- `J_trans` at least moderate

### `Z_B`

Typical profile:

- strong local event capture
- bounded local reseating
- pseudo-progressive behaviour likely

### `Z_C`

Typical profile:

- broad weak continuation
- reduced route dominance
- drift toward diffuse outcome

## Loop Family Notation

- `L1`
  - face loop
- `L2`
  - shallow pocket loop
- `L3`
  - elongated stall loop
- `L4`
  - broken multi-loop field

### Current strongest role

- `L3` is the main recurring stall family

## Route Class Notation

- `R1`
  - narrow viable route
- `R2`
  - distributed weak routes
- `R3`
  - blocked apparent route
- `R4`
  - inward-biased route
- `R5`
  - loop-dominated pseudo-route
- `R6`
  - fragmenting route field

### Current strongest frontier pair

- `R3`
- `R5`

## Obstruction Class Notation

- `O1`
  - funnelling obstruction
- `O2`
  - late-gate obstruction
- `O3`
  - pocketing obstruction
- `O4`
  - biasing obstruction
- `O5`
  - diffusing obstruction
- `O6`
  - fragmenting obstruction

### Current strongest frontier pair

- `O2`
- `O3`

## Dominance Mode Notation

- `D1`
  - route-dominant interface
- `D2`
  - pocket-dominant interface
- `D3`
  - diffusion-dominant interface
- `D4`
  - mixed competitive interface

## Route-Reality Grade Notation

- `G_A`
  - strongly real route
- `G_B`
  - weak but real route
- `G_C`
  - apparent but unreliable route
- `G_D`
  - pseudo-route

These map to the prose grades:

- `A`
- `B`
- `C`
- `D`

## Compact Case Notation

A case can now be written in compressed form using:

```text
Case := <pairing> : {zones} ; {dominance} ; {route classes} ; {obstruction classes} ; {route-reality grades}
```

### Example Form

```text
glass->air : {Z_A, Z_B, Z_C} ; D4->D2 ; {R3, R5, R2} ; {O2, O3, O5} ; {G_B, G_C, G_D}
```

Meaning:

- the case contains:
  - route zone
  - pocket zone
  - diffuse fringe
- it is mainly mixed competitive, often drifting toward pocket-dominant
- the dominant route logics are:
  - blocked apparent route
  - pseudo-route
  - weak distributed continuation
- the dominant obstruction characters are:
  - late-gate
  - pocketing
  - diffusing
- route-reality spans:
  - weak real
  - apparent/unreliable
  - pseudo-route

## Transition Notation

### Basic Transition Arrow

Use:

- `->`

for a likely transition.

Examples:

- `Z_A -> Z_B`
- `R3 -> R5`
- `L3 -> R1`

### Weighted or Tendency Arrow

Use:

- `=>`

for a stronger tendency or currently dominant drift.

Examples:

- `Z_B => Z_C`
- `O2 => R3`
- `O3 => R5`

### Competitive Coexistence

Use:

- `~`

for live competition or coexistence without decisive dominance.

Examples:

- `Z_A ~ Z_B`
- `R3 ~ R5`
- `D4 : Z_A ~ Z_B ~ Z_C`

### Resolution Set

Use:

- `{ ... }`

for bounded resolution options.

Example:

```text
L3 -> {R1, R3, R4, L4}
```

Meaning:

- the elongated stall family currently resolves toward:
  - successful handoff logic
  - blocked route logic
  - inward return logic
  - fragmented loop-field logic

## Subregion Weighting Sketch

For local zone weighting, use provisional comparative tags:

- `W_low`
- `W_med`
- `W_high`

Applied to:

- event capture
- route leverage
- persistence
- competitive suppression

### Example

```text
Z_B : capture=W_high ; leverage=W_med ; persistence=W_high ; suppression=W_med
```

This does not yet imply a formal score. It is a compact comparative profile.

## Minimal Diagnostic Expression

A full compact diagnostic can be written as:

```text
<pairing>
= Zones{...}
= Dom{...}
= Route{...}
= Obst{...}
= Grade{...}
= Flow{...}
```

### Example: Glass -> Crystal Frontier Region

```text
glass->crystal
= Zones{Z_A, Z_B}
= Dom{D4}
= Route{R1, R3, R5}
= Obst{O1, O2, O3}
= Grade{G_B/G_A, G_C, G_D}
= Flow{Z_A->completion, Z_A->Z_B, D4->Z_A, D4->Z_B}
```

### Example: Air -> Polished Metal

```text
air->polished_metal
= Zones{Z_A? return-biased boundary field}
= Dom{D1(return-biased)}
= Route{R4}
= Obst{O4}
= Grade{G_A inward / G_D outward}
= Flow{return dominance}
```

Note:

- this case does not fit the mixed-glass frontier template as directly
- the notation is still useful, but should be read with directional asymmetry in mind

## Current Stable Mappings

The following should now be treated as stable shorthand:

- `O2 => R3`
- `O3 => R5`
- `O4 => R4`
- `L3 -> {handoff, trapped release, ordered return, fragmentation}`

And at case level:

- `glass->air : {Z_A,Z_B,Z_C} ; D4->D2 ; {R2,R3,R5} ; {O2,O3,O5}`
- `glass->crystal : {Z_A,Z_B,(Z_C weak)} ; D1 or D4 ; {R1,R3,R5} ; {O1,O2,O3}`
- `air->oxidised_metal : {Z_A weak,Z_C strong} ; D3 ; {R3,R6} ; {O2,O6}`

## What This Formalisation Is Good For

It is now good for:

- compact case summaries
- comparing benchmark cases quickly
- tracking which layers are active in one case
- reducing repeated prose overhead
- preparing for later, more mathematical formalisation

## What It Is Not Yet Good For

It is not yet good for:

- quantitative prediction
- settled equations
- simulation-ready formal dynamics
- probabilistic calibration

That is fine. It should not pretend otherwise.

## Current Strongest Gains

## 1. The Framework Is Now Compressible

This is the main result.

The recent modelling sequence can now be written in a compact reusable notation rather than only in long prose.

## 2. Cross-Layer Relations Are Explicit

The formal sketch makes it easier to see:

- obstruction class
- route class
- zone type
- dominance mode

inside one expression.

## 3. It Preserves Honesty

This matters.

The notation is compact, but it does not pretend the programme already has finished mathematics.

## Current Weak Point

The biggest remaining weakness is:

- notation is now compact
- but not yet stress-tested in repeated use across a wider set of cases

So the next step should be application, not more notation growth.

## Confidence

- confidence that the framework is now compact enough for repeated use: `8/10`
- confidence that this level of formalisation is appropriate for the current stage: `9/10`
- confidence that more formal notation growth should wait until more application work is done: `9/10`

## Recommendation

Keep this notation layer small and stable for now.

Do not expand it aggressively yet.

Use it on more cases first.

## Next Move

The best next artifact is:

- `ams-formalised-case-library-v1.md`

That should apply this notation compactly to the strongest benchmark cases and build the first true mini-library of standardised interface-case expressions.*** End Patch
