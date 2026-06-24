# AMS Mixed Interface Event-Flow Scenarios v1

## Purpose

This document makes the mixed-interface model explicitly dynamic.

The previous weighting study established that one interface can contain multiple local zones and that those zones do not matter equally. But weighting alone is not enough. The programme now needs to model:

- how an event actually moves between local zones
- when it stays in one zone
- when it drifts into another
- when one local logic takes over from another

This document addresses that problem.

## Context

From:

- `ams-mixed-subregion-interface-model-v1.md`
- `ams-subregion-dominance-and-weighting-v1.md`

the active mixed-interface template includes:

- Zone A: late-gate route zone
- Zone B: pocketing pseudo-route zone
- Zone C: diffusing fringe

and the main dominance modes include:

- `D1` route-dominant
- `D2` pocket-dominant
- `D3` diffusion-dominant
- `D4` mixed competitive

The missing layer is now:

- event flow

## Core Claim

An event in a mixed interface is not statically located.

It may:

- begin under one local logic
- continue under another
- resolve under a third

That means whole-interface outcomes may depend not only on:

- which zones exist
- which zones are weighted strongly

but also on:

- the order in which the event encounters them
- whether continuity survives those transitions
- whether one zone captures the event before a rival zone can do so

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

Geometric descriptors:

- `L_depth`
- `L_span`
- `L_loop`
- `L_escape`

## Event-Flow Principle

The current programme suggests a simple first principle:

- event outcome depends on the strongest sequence of local control, not just the strongest single zone in the abstract

This matters because:

- a route zone may dominate if it captures the event early enough
- a pocket zone may dominate if it captures the event before a viable route stabilises
- a diffusing fringe may dominate if coherence weakens before either route or pocket logic can win decisively

## First-Pass Event-Flow Scenarios

## Scenario F1: Route-Led Completion

### Sequence

1. event enters a route-dominant zone
2. route leverage stays ahead of pocket capture
3. `J_trans` remains strong enough for continuation
4. event avoids strong diffusion spill
5. completion occurs

### Dominant Mode

- `D1`

### Main Route Logic

- `R1`
- or weakened `R3` that recovers before failure

### Main Variable Conditions

- medium/high `J_trans`
- medium/high `Q_coh`
- high enough `L_escape`
- limited competitive suppression from neighboring zones

### Best Current Cases

- selective `glass -> crystal`
- stronger `crystal -> air`

## Scenario F2: Route-Then-Block

### Sequence

1. event enters a route zone
2. genuine progression begins
3. late-gate obstruction becomes decisive
4. completion route collapses near the end
5. event resolves as blocked apparent route

### Dominant Mode

- `D1` drifting into `D4`

### Main Route Logic

- `O2 -> R3`

### Main Variable Conditions

- medium `J_trans`
- medium/high early `Q_coh`
- weakening `L_escape`
- strong enough late obstruction to defeat completion

### Best Current Cases

- glass late blocked release
- glass late compatibility failure
- failed ordered crystal release

## Scenario F3: Route-Then-Pocket Capture

### Sequence

1. event begins in a route zone
2. route progression weakens locally
3. event enters or is captured by a pocketing zone
4. local reseating begins to dominate
5. pseudo-route or trapped release takes over

### Dominant Mode

- `D4` shifting toward `D2`

### Main Route Logic

- `R3` drifting into `R5`

### Main Variable Conditions

- medium `J_trans` falling to low/medium
- medium `Q_coh`
- local event capture by pocket zone exceeds route leverage
- `L_escape` was real initially, then becomes mostly apparent

### Best Current Cases

- frontier `glass -> air`
- frontier `glass -> crystal`

### Importance

This is one of the most important dynamic scenarios in the entire programme.

It explains how an event that genuinely began with route logic can end in pseudo-progressive looping.

## Scenario F4: Pocket-Led Retention

### Sequence

1. event enters a pocketing zone early
2. local activity becomes intense quickly
3. no robust completion route ever stabilises
4. local reseating dominates
5. trapped release or pseudo-compatibility persists

### Dominant Mode

- `D2`

### Main Route Logic

- `O3 -> R5`

### Main Variable Conditions

- medium/high `J_bound`
- low/medium `J_trans`
- medium `Q_coh`
- low real `L_escape`
- high event capture by pocket zone

### Best Current Cases

- pocketed glass release
- pseudo-compatibility local zones

## Scenario F5: Pocket-to-Diffuse Bleed

### Sequence

1. event is captured in a pocketing zone
2. bounded local activity persists briefly
3. local coherence weakens
4. event spills into diffusing fringe
5. diffuse release or fragmentation dominates

### Dominant Mode

- `D2` drifting into `D3`

### Main Route Logic

- `R5` drifting toward `R2` or `R6`

### Main Variable Conditions

- `Q_coh` falling
- `J_trans` weak
- increasing diffusive suppression
- weakening bounded loop coherence

### Best Current Cases

- degraded glass release
- poor compatibility regions near fragmentation edge

## Scenario F6: Route-to-Diffuse Collapse

### Sequence

1. event begins with genuine route logic
2. route leverage weakens before pocket capture can stabilise
3. event broadens into diffusing fringe
4. route dominance is lost without a stable local pocket taking over

### Dominant Mode

- `D4` drifting into `D3`

### Main Route Logic

- weakened `R3` drifting toward `R2` or `R6`

### Main Variable Conditions

- `J_trans` weakening
- `Q_coh` falling
- route continuity breaks broadly rather than locally

### Best Current Cases

- degraded `glass -> air`
- degraded `air -> oxidised metal`

## Scenario F7: Mixed Competitive Oscillation

### Sequence

1. no single zone captures the event decisively
2. route leverage, pocket capture, and fringe spread compete
3. the event shifts locally between partial progression and local reseating
4. outcome remains unstable until one logic eventually dominates

### Dominant Mode

- `D4`

### Main Route Logic

- mixed `R3` / `R5` with possible `R2` fringe participation

### Main Variable Conditions

- medium event capture across multiple zones
- medium route leverage without decisive advantage
- medium persistence of local pockets
- unstable `L_escape`

### Best Current Cases

- strongest frontier `glass -> air`
- strongest frontier `glass -> crystal`

### Importance

This may be the most realistic frontier picture for the hardest mixed interfaces.

## What Controls Zone Transitions?

The current first-pass answer suggests four transition controls.

## 1. Route Leverage Decay

If the route zone loses leverage, the event may be captured by:

- a pocket zone
- or a diffusing fringe

This is crucial in:

- `R3 -> R5`
- `R3 -> R2/R6`

## 2. Pocket Capture Strength

If local retention gains control early enough, a route may never stabilise fully.

This is the key to:

- early `R5`
- trapped release

## 3. Coherence Retention

If `Q_coh` remains high enough, the event may:

- keep route logic
- or even resolve into ordered return

If `Q_coh` falls, the event may:

- drift toward diffuse or fragmented outcomes

## 4. Escape Viability Decay

If `L_escape` weakens:

- route-led completion becomes less likely
- pocket or diffuse capture becomes more likely

This is one of the clearest dynamic roles for `L_escape` so far.

## Strongest Current Dynamic Findings

## 1. Frontier Cases Are Best Explained as Event Flows, Not Static Labels

This is the main result.

Especially in:

- `glass -> air`
- `glass -> crystal`

the event is best understood as moving through a mixed local field rather than simply “being” one route class or one obstruction class.

## 2. `R3 -> R5` Is a Real Dynamic Possibility

This is a major gain.

The model can now say:

- a real route can begin
- lose leverage
- fall into local pocket capture
- and become a pseudo-route regime

That is much stronger than just saying the event “failed.”

## 3. Mixed Interfaces Need Sequencing, Not Only Weighting

Weighting remains important, but flow order matters too.

Early pocket capture and late route blockage are not the same event history, even if the final whole-interface label looks similar.

## 4. The Programme Still Does Not Need New Primitives

This should be said clearly.

The new gains still come from:

- event sequencing
- zone competition
- route viability tracking

not from adding more primitive variables.

## Current Weak Point

The current model now has:

- variables
- loops
- routes
- obstruction classes
- zone weights
- flow scenarios

But it still lacks a compact way to score transition likelihoods between zones.

That is now the obvious next step.

## Confidence

- confidence that mixed-interface behaviour is fundamentally dynamic: `9/10`
- confidence that the event-flow scenarios are useful: `8/10`
- confidence that `R3 -> R5` is a real dynamic path: `8/10`
- confidence that no new primitive split is needed yet: `8/10`

## Recommendation

Keep the current frameworks unchanged.

The next gains should come from:

- scoring transition likelihoods between local zones

## Next Move

The best next artifact is:

- `ams-zone-transition-likelihoods-v1.md`

That should estimate, in structured qualitative form:

- how likely Route Zone -> Pocket Zone is
- how likely Pocket Zone -> Diffusing Fringe is
- how likely Route Zone -> Completion remains
- how likely Mixed Competitive -> one-zone dominance becomes

under the current frontier benchmarks.*** End Patch
