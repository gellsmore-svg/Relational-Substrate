# AMS Trapped Release Study v1

## Purpose

This document isolates one of the most important remaining release-side frontier modes:

- trapped release

The need for this study emerged from:

- `ams-exit-geometry-study-v1.md`
- `ams-glass-release-study-v1.md`

The current programme can now distinguish:

- clean release
- diffuse release
- inward return

reasonably well.

What remains less sharp is:

- how a release event can fail by becoming locally retained near the terminal boundary without simply turning into scattering or structured return

That is the problem of trapped release.

## Core Claim

Trapped release is a real interface mode, not just “poor exit.”

It should be treated as:

- a bounded local failure of release
- in which the event remains organised enough to avoid immediate scatter
- but not release-capable enough to leave cleanly
- and not boundary-coherent enough to become a strong inward-return event

So trapped release is best understood as:

- shallow boundary retention under failed terminal continuity

## Active Variable Set

Primitive variables:

- `B_in`
- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

Derived term:

- `I_comp`

Supporting bulk variables:

- `R`
- `S`
- `J_dist`

## Why Trapped Release Matters

If trapped release is not modelled clearly, then the programme risks collapsing multiple distinct failures into one vague category:

- poor release
- diffuse loss
- retained interface activity
- inward redirection

That would weaken the whole interface programme.

Trapped release matters because it implies:

- the interface is active
- the event remains partially organised
- the failure happens in the release process itself

That makes it a stronger and more informative case than generic “degraded exit.”

## Working Definition

Trapped release occurs when:

- an internally propagated event reaches the terminal boundary
- a local release event forms
- the event cannot sustain viable outward continuation
- the event also does not collapse immediately into diffuse scattering
- local reseating or shallow retention therefore dominates

## Baseline Variable Signature

Current best first-pass signature:

- `B_out`: low/medium
- `J_bound`: medium/high
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium/high

Interpretation:

- the boundary does enough to form a local event
- but the terminal layer does not carry that event through into outward release
- some organisation persists, preventing immediate randomisation

## Two Main Trapped Release Geometries

## Geometry TR1: Shallow Boundary Retention

### Description

The event reaches the boundary face and remains near it. Local reseating occurs in a shallow region, but deeper outward continuation fails quickly.

### Variable Pattern

- `B_out`: low/medium
- `J_bound`: high
- `J_trans`: low
- `Q_coh`: low/medium
- `D`: medium/high

### Likely Behaviour

- repeated local boundary activity
- weak outward leakage at most
- no clean outward release
- no strong inward redirection

### Interpretation

This is the more surface-concentrated trapping case.

The interface can form a release event, but it cannot sustain it through the terminal layer.

## Geometry TR2: Terminal Continuity Stall

### Description

The event enters the terminal layer and begins release progression, but the continuity needed to complete outward emergence degrades before the event leaves the whole.

### Variable Pattern

- `B_out`: low/medium
- `J_bound`: medium/high
- `J_trans`: medium
- `Q_coh`: medium
- `D`: medium

### Likely Behaviour

- release begins
- local reseating persists
- the event neither escapes cleanly nor collapses immediately
- shallow retention occupies a finite release region

### Interpretation

This is the more interesting case, because it implies:

- the release process is active
- some through-layer mediation is present
- but not enough to finish the transition

This is the closest release-side analogue to the earlier:

- glass -> crystal funnel stall

## How Trapped Release Differs from Diffuse Release

This is the first major distinction the study needs to secure.

## Diffuse Release

In diffuse release:

- outward continuation still occurs
- the event spreads or loosens too much
- release remains real, but degraded

Typical signature:

- medium `B_out`
- medium `J_bound`
- low/medium `J_trans`
- medium `Q_coh`
- medium/high `D`

## Trapped Release

In trapped release:

- outward continuation does not dominate
- local reseating dominates instead
- the event remains near the boundary or terminal layer

Typical signature:

- lower `B_out`
- non-low `J_bound`
- low/medium `J_trans`
- medium `Q_coh`

## Main Difference

Diffuse release still resolves outward.

Trapped release does not.

That is the core distinction.

## How Trapped Release Differs from Inward Return

This is the second major distinction.

## Inward Return

In inward return:

- the boundary responds strongly and coherently
- the event is redirected inward rather than released outward

Typical signature:

- low/medium `B_out`
- high `J_bound`
- low `J_trans`
- medium/high `Q_coh`
- low/medium `D`

## Trapped Release

In trapped release:

- the event is locally retained, not cleanly returned
- boundary organisation exists, but not enough for strong structured inward redirection

Typical signature:

- low/medium `B_out`
- medium/high `J_bound`
- low/medium `J_trans`
- medium `Q_coh`
- medium/high `D`

## Main Difference

Inward return preserves stronger organised boundary response.

Trapped release preserves local activity without achieving strong redirection.

## How Trapped Release Differs from Glass-to-Crystal Funnel Stall

This is the third key distinction.

## Funnel Stall

In `glass -> crystal` funnel stall:

- the event is already inside a transition layer between two transmissive grammars
- narrowing begins
- final admission into the receiving whole fails

Typical signature:

- medium/high `J_bound`
- medium `J_trans`
- medium `Q_coh`
- medium `I_comp`

## Trapped Release

In trapped release:

- there is no second structured transmissive whole waiting to admit the event
- the failure happens at outward terminal emergence
- local retention dominates because the event cannot complete release itself

Typical signature:

- lower `B_out`
- lower or absent genuine `I_comp`
- stronger dependence on terminal-layer continuity failure

## Main Difference

Funnel stall is:

- failed compatibility between transmissive orders

Trapped release is:

- failed completion of terminal outward emergence

## Terminal-Layer Conditions That Favour Trapped Release

The current study suggests four main contributors.

## 1. Local Pathway Crowding Near the Surface

The event reaches the boundary, but too many local reseating options remain shallow and lateral rather than outward.

## 2. Weak Outward Continuity Despite Active Boundary Response

The release event forms, but its onward path is poor.

This is one of the clearest signatures of:

- high enough `J_bound`
- insufficient `J_trans`

## 3. Medium Defect Burden Rather Than Total Disorder

If defect burden is too low, the event may release or return coherently.

If defect burden is too high, the event may scatter.

Trapping seems most plausible in the middle:

- enough burden to block completion
- not enough to destroy local organisation immediately

## 4. Terminal Geometry That Supports Local Cycling

The surface region may allow:

- repeated shallow reseating
- bounded persistence
- stalled continuity

without clean outward escape.

## Strongest Current Trapping Benchmark

At present the best benchmark remains:

- `glass -> air`

Reason:

- the bulk whole is already a good transmissive anchor
- terminal fragility is plausible
- release failure need not imply either strong reflection or total incoherence

So glass remains the best release-side place to stabilise trapped-release modelling.

## Cross-Programme Importance

This study matters beyond glass.

It strengthens:

### 1. Exit modelling in general

The programme can now distinguish:

- release
- diffuse release
- trapped release
- inward return

more sharply.

### 2. The transition-layer picture

Trapping supports the claim that a terminal interface is a finite active region, not just a mathematical surface.

### 3. Compatibility comparisons

Trapped release can now be compared to:

- glass -> crystal funnel stall
- oxide-layer interface degradation
- other partial-handoff failures

without collapsing them into one undifferentiated class.

## Current Weak Points

## 1. No Fully Explicit Cycling Geometry Yet

The study supports local reseating and shallow retention, but the geometry is still not formal enough to specify:

- loop depth
- repetition count
- local residence conditions

## 2. Trapped Release Still Uses Broad `D`

The current variable set is sufficient for now, but trapping does strengthen the longer-term possibility that `D` may eventually need splitting into:

- defect burden
- defect tolerance

This is not required yet, but the pressure is visible.

## 3. Return vs Trapping Boundary Profiles Still Need Direct Side-by-Side Testing

The distinction is clearer conceptually now, but it would still benefit from direct comparative tabulation.

## Confidence

- confidence that trapped release is a real interface mode: `9/10`
- confidence that it differs clearly from diffuse release: `8/10`
- confidence that it differs clearly from inward return: `8/10`
- confidence that glass remains the best trapped-release benchmark: `8/10`
- confidence that another variable split is needed immediately: `4/10`

## Recommendation

Keep the current refined variable set.

Do not split `D` yet.

Instead, strengthen the geometry and comparative testing first.

## Next Move

The best next artifact is:

- `ams-release-failure-discriminator-table-v1.md`

That should compare directly:

- diffuse release
- trapped release
- inward return
- scattering at exit

using the current refined variables so the release-side failure space becomes fully explicit rather than partly narrative.
