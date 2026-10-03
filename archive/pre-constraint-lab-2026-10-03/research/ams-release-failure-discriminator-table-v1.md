# AMS Release Failure Discriminator Table v1

## Purpose

This document turns the release-side failure space into a direct side-by-side comparison.

The goal is to discriminate cleanly between:

- diffuse release
- trapped release
- inward return
- scattering at exit

This is the release-side counterpart to the earlier interface discriminator work. The aim is to stop using near-overlapping prose categories and force the current variable set to show where each failure mode actually differs.

## Active Variable Set

Primitive variables:

- `B_out`
- `J_bound`
- `J_trans`
- `Q_coh`
- `D`

Derived term:

- `I_comp` where relevant, though it is less central here than in cross-whole handoff

Supporting context:

- `R`
- `S`
- `J_dist`

## Outcome Definitions

### Diffuse Release

The event still leaves the source whole, but it spreads, loosens, or degrades during terminal release. Outward continuation remains real but not clean.

### Trapped Release

The event reaches the terminal region and forms a local release event, but outward continuation does not dominate. Local reseating or shallow retention dominates instead.

### Inward Return

The event reaches the terminal boundary and is redirected inward with more structured boundary response than trapped release preserves.

### Scattering at Exit

The event reaches the terminal region but loses enough coherence and continuity that no strong outward release, local retention, or inward redirection dominates.

## Discriminator Table

| Failure mode | `B_out` | `J_bound` | `J_trans` | `Q_coh` | `D` | Dominant character |
|---|---:|---:|---:|---:|---:|---|
| Diffuse release | medium | medium | low/medium | medium | medium/high | outward continuation survives, but spreads |
| Trapped release | low/medium | medium/high | low/medium | medium | medium/high | local release event forms, but stalls |
| Inward return | low/medium | high | low | medium/high | low/medium | boundary response redirects inward |
| Scattering at exit | low/medium | low/medium | low | low/medium | high | organisation collapses into dispersed exit failure |

## Failure-Mode Analysis

## 1. Diffuse Release

### Signature

- `B_out`: medium
- `J_bound`: medium
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium/high

### What Makes It Distinct

Diffuse release still resolves outward.

That is the decisive point.

The release is degraded, broadened, or loosened, but the event does not remain locally retained and is not cleanly turned inward.

### Best Current Benchmark

- `glass -> air`

especially where the terminal layer spreads the event rather than fully blocking it.

### Strongest Discriminator

- outward continuation remains dominant despite degraded continuity

## 2. Trapped Release

### Signature

- `B_out`: low/medium
- `J_bound`: medium/high
- `J_trans`: low/medium
- `Q_coh`: medium
- `D`: medium/high

### What Makes It Distinct

Trapped release forms a local interface event but does not complete outward continuation.

Unlike diffuse release:

- outward resolution does not dominate

Unlike inward return:

- local organisation is insufficient for strong structured redirection

Unlike scattering:

- too much local organisation remains for immediate dispersion to dominate

### Best Current Benchmark

- `glass -> air`

in a shallow retention regime.

### Strongest Discriminator

- active local release attempt plus failed continuation

## 3. Inward Return

### Signature

- `B_out`: low/medium
- `J_bound`: high
- `J_trans`: low
- `Q_coh`: medium/high
- `D`: low/medium

### What Makes It Distinct

This is the most structured non-release case.

The event does not merely stall. It is actively redirected inward by strong boundary-face response.

That means:

- the boundary remains highly organised
- through-layer release continuity is weak
- coherence is preserved strongly enough for directional return rather than local retention

### Best Current Benchmark

- crystal-like exits
- polished but non-releasing boundaries

### Strongest Discriminator

- high `J_bound` plus relatively high `Q_coh`

## 4. Scattering at Exit

### Signature

- `B_out`: low/medium
- `J_bound`: low/medium
- `J_trans`: low
- `Q_coh`: low/medium
- `D`: high

### What Makes It Distinct

This is the least organised release failure.

The terminal event does not preserve:

- strong outward continuation
- strong local retention
- strong inward redirection

Instead:

- defect burden and weak continuity dominate

### Best Current Benchmark

- highly degraded exit layers
- rough or contaminated surfaces

### Strongest Discriminator

- high `D` with low `Q_coh` and weak local mediation

## Strongest Pairwise Distinctions

## Diffuse Release vs Trapped Release

Main separator:

- whether outward continuation still dominates

Diffuse release:

- degraded outward continuation

Trapped release:

- stalled continuation with local retention

## Trapped Release vs Inward Return

Main separator:

- structured redirection

Trapped release:

- local activity without strong directional return

Inward return:

- strong boundary-face response plus preserved coherence

## Trapped Release vs Scattering

Main separator:

- local organisation

Trapped release:

- local reseating remains

Scattering:

- local organisation is too weak to dominate

## Diffuse Release vs Scattering

Main separator:

- whether outward release still remains the dominant outcome

Diffuse release:

- yes

Scattering:

- no

## Which Variables Matter Most

## 1. `B_out`

This remains the main discriminator of whether release is actually completing or failing.

It does not separate all failure modes by itself, but it is the primary release-side gate variable.

## 2. `J_bound`

This is the strongest separator between:

- trapping
- inward return
- weakly organised scattering

It tells us whether the boundary is actively shaping the event or only weakly mediating it.

## 3. `J_trans`

This is the strongest separator between:

- release that continues outward
- release that stalls locally

It is especially important for distinguishing:

- diffuse release
- trapped release

## 4. `Q_coh`

This is the strongest separator between:

- structured return
- incoherent or weakly coherent failure

It is less dominant in diffuse release, more decisive in return.

## 5. `D`

`D` still drives the system toward scattering, but not all high-`D` cases scatter.

Trapping appears strongest where `D` is elevated enough to block completion but not so high that local organisation collapses completely.

## Current Best Release-Side Interpretation

The release-side failure space now looks genuinely structured.

It is no longer best described as:

- release succeeds
- or release fails

It is better described as:

- release succeeds cleanly
- release succeeds diffusely
- release stalls and traps
- release turns inward
- release collapses into scattering

That is a major gain for the programme.

## Remaining Weak Point

The weakest remaining area is not the variable set itself.

It is the geometry of:

- local reseating depth
- shallow retention loops
- how far a trapped event penetrates into the terminal layer before stalling

Those are still only partly specified.

## Confidence

- confidence that the four release-side failure modes are genuinely distinct: `9/10`
- confidence that trapped release is now clearly separable from diffuse release: `9/10`
- confidence that trapped release is now clearly separable from inward return: `8/10`
- confidence that scattering at exit is no longer being used as a catch-all: `8/10`
- confidence that the current variable set is sufficient for the next step: `8/10`

## Recommendation

Keep the current refined variable set unchanged.

The next gain should come from geometry, not from more variable splitting.

## Next Move

The best next artifact is:

- `ams-terminal-layer-depth-and-loop-geometry-v1.md`

That should focus on:

- local reseating depth
- shallow retention loops
- terminal-layer penetration before stall
- when a trapped event remains near-surface and when it becomes a deeper terminal-layer stall
