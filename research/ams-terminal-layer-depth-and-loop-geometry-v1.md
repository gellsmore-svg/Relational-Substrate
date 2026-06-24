# AMS Terminal-Layer Depth and Loop Geometry v1

## Purpose

This document develops the main remaining weak point in the current release-side programme:

- the geometry of trapped release inside the terminal layer

The previous discriminator work established that release-side failure modes are now distinct:

- diffuse release
- trapped release
- inward return
- scattering at exit

But the current model still lacks a strong geometric account of:

- how deep a trapped event penetrates into the terminal layer
- what kind of local reseating loop it falls into
- when retention is shallow
- when retention becomes a deeper terminal-layer stall

This document addresses that gap.

## Core Claim

Trapped release is not one geometry.

It likely comes in at least two spatial forms:

- shallow retention near the boundary face
- deeper terminal-layer stall after partial inward progression through the release zone

That means “local retention” should not be treated as a single event shape.

## Active Variable Set

Primitive variables:

- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

Supporting context:

- `R`
- `S`
- `J_dist`

## New Geometric Descriptors

These are not yet new formal variables. They are geometric descriptors to sharpen the current model.

### `L_depth`

Meaning:

- approximate penetration depth of a release-failing event into the terminal layer before dominant stall, retention, return, or diffusion

### `L_span`

Meaning:

- lateral spread of local reseating within the terminal zone

### `L_loop`

Meaning:

- the dominant local reseating pattern of the trapped event

Current candidate loop classes:

- face loop
- shallow pocket loop
- elongated stall loop
- broken multi-loop field

### `L_escape`

Meaning:

- degree to which the local retained event still has viable outward continuation options available

These descriptors are being introduced as modelling aids, not yet as permanent primitives.

## Two Main Depth Regimes

## Regime D1: Shallow Retention

### Description

The event reaches the boundary face or immediate near-surface region and becomes locally retained there.

It does not penetrate deeply into the terminal layer before stalling.

### Typical Characteristics

- low `L_depth`
- low/medium `L_span`
- medium/high `J_bound`
- low `J_trans`
- low/medium `L_escape`

### Interpretation

This is the most surface-concentrated trapped-release case.

The boundary forms an active local event, but the terminal layer does not support deeper continuation or clean outward emergence.

### Best Fit

- shallow roughness cases
- weakly contaminated release faces
- near-surface pathway crowding

## Regime D2: Terminal-Layer Stall

### Description

The event enters the terminal layer beyond the immediate face, but the continuity required for outward completion fails before release resolves.

### Typical Characteristics

- medium `L_depth`
- medium `L_span`
- medium/high `J_bound`
- medium `J_trans`
- medium `L_escape`

### Interpretation

This is the more interesting trapped-release case.

The event does not fail immediately at the boundary face. Instead:

- release begins
- the event progresses inward through part of the terminal zone
- local reseating continues
- final emergence fails

This is the release-side analogue of a partially successful transition that never completes.

### Best Fit

- terminal-layer mismatch
- structured but incomplete release zones
- glass exit where continuity weakens late rather than immediately

## Candidate Loop Geometries

## Loop Type L1: Face Loop

### Description

The event cycles in a very shallow path near the boundary face itself.

### Geometry

- very low `L_depth`
- low `L_span`
- dominant boundary-face interaction

### Variable Pattern

- high `J_bound`
- low `J_trans`
- medium `Q_coh`
- medium/high `D`

### Likely Outcome

- shallow trapped release
- weak outward leakage possible
- little deep terminal-layer participation

### Interpretation

This is the simplest trapped-release loop.

It behaves more like repeated shallow boundary reseating than like a true through-layer stall.

## Loop Type L2: Shallow Pocket Loop

### Description

The event falls into a local near-surface pocket in the terminal layer and circulates within a bounded release region.

### Geometry

- low/medium `L_depth`
- medium `L_span`
- more finite local volume than L1

### Variable Pattern

- medium/high `J_bound`
- low/medium `J_trans`
- medium `Q_coh`
- medium `D`

### Likely Outcome

- persistent local trapping
- stronger local retention than a simple face loop
- release completion repeatedly attempted and not achieved

### Interpretation

This is a stronger trapped-release geometry than L1 because the event is not merely kissing the face. It occupies a bounded local release volume.

## Loop Type L3: Elongated Stall Loop

### Description

The event penetrates farther into the terminal layer and moves through an elongated local continuity path before stalling and reseating.

### Geometry

- medium `L_depth`
- medium/high `L_span`
- recognisable terminal-layer path rather than surface-only looping

### Variable Pattern

- medium/high `J_bound`
- medium `J_trans`
- medium `Q_coh`
- medium `D`

### Likely Outcome

- terminal-layer stall
- partial progression without full release
- more structured trapping than L1 or L2

### Interpretation

This is the most likely geometry behind the stronger trapped-release cases.

It is also the one most likely to connect with:

- glass-to-crystal funnel stall
- deeper transition-layer compatibility failures

## Loop Type L4: Broken Multi-Loop Field

### Description

The event does not remain in one clean local loop. Instead it fragments into several weakly connected local reseating zones.

### Geometry

- variable `L_depth`
- higher `L_span`
- weak loop coherence

### Variable Pattern

- low/medium `J_bound`
- low `J_trans`
- low/medium `Q_coh`
- high `D`

### Likely Outcome

- transition from trapped release toward scattering

### Interpretation

This is the edge case where local organisation is beginning to break down.

It is useful because it marks the boundary between:

- true trapped release
- and exit-side scattering

## Shallow Retention vs Deeper Stall

This is the central distinction the document is trying to stabilise.

## Shallow Retention

Main signs:

- very low `L_depth`
- strong boundary-face dependence
- weak through-layer continuity
- mostly local face or pocket looping

Best loop types:

- L1
- L2

## Deeper Terminal-Layer Stall

Main signs:

- medium `L_depth`
- non-trivial `J_trans`
- partial progression before failure
- elongated local continuity path before stall

Best loop type:

- L3

### Main Difference

Shallow retention fails almost immediately.

Deeper stall fails after partial release progression.

That is the most important spatial distinction to preserve.

## Trapped Release vs Scattering Boundary

The new loop geometry helps here.

Trapped release remains dominant when:

- one loop or one bounded local path still carries the event
- local organisation still dominates over random dispersion

Scattering begins to dominate when:

- loop coherence degrades
- local reseating fragments into a broken field
- `L4` behaviour replaces `L1-L3`

This is one of the clearest gains in the document.

## Trapped Release vs Inward Return Boundary

Loop geometry also helps here.

In trapped release:

- the event remains locally cycling or stalling
- it does not resolve into a clean inward direction

In inward return:

- the event keeps enough organised boundary response to be redirected rather than trapped

So the key difference is:

- looping versus directional return

not merely “how much coherence is present.”

## Best Current Glass Exit Reading

The strongest current reading for `glass -> air` is now:

- bulk transmission remains viable
- the terminal layer may support either:
  - clean release
  - diffuse release
  - shallow trapped release
  - deeper terminal-layer stall

Most plausible trapped-release forms in glass:

- L2 shallow pocket loop
- L3 elongated stall loop

That is stronger than the earlier looser phrase:

- local retention near the boundary

## Programme-Level Consequences

## 1. Trapped Release Is Now Spatially Differentiated

That is the main result.

The model can now distinguish:

- where the event stalls
- how far it progresses
- what kind of local loop or retention field it enters

## 2. Terminal Layers Are Clearly Finite Active Regions

The work now supports the claim that:

- the release zone is not a mathematical face only
- it is a finite region with internal spatial structure

## 3. No Immediate New Primitive Variable Is Needed

The new descriptors help, but they do not yet justify adding more primitives.

The current variable set still seems sufficient if the geometry is described more explicitly.

## 4. The Best Next Refinement Is Comparative, Not Primitive

The next gain should come from testing these loop classes against:

- real glass exit cases
- crystal exit cases
- compatibility stalls

rather than introducing another variable split too early.

## Confidence

- confidence that trapped release has at least two spatial regimes: `9/10`
- confidence that loop geometry improves the model materially: `8/10`
- confidence that L1-L4 is a useful first loop classification: `8/10`
- confidence that no immediate primitive-variable split is needed: `8/10`

## Recommendation

Keep the current refined variable set.

Use:

- `L_depth`
- `L_span`
- `L_loop`
- `L_escape`

as geometric modelling aids for now rather than formal primitives.

## Next Move

The best next artifact is:

- `ams-trapped-release-loop-comparison-v1.md`

That should compare:

- L1 face loop
- L2 shallow pocket loop
- L3 elongated stall loop
- L4 broken multi-loop field

against:

- glass exit
- crystal exit
- glass-to-crystal compatibility stall

to see which loop families recur and which are release-specific.*** End Patch
