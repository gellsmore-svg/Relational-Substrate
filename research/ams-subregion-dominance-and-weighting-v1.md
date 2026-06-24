# AMS Subregion Dominance and Weighting v1

## Purpose

This document develops the next necessary layer after:

- `ams-mixed-subregion-interface-model-v1.md`

The mixed-subregion model established that one real interface can contain several local zones at once, for example:

- Zone A: late-gate route zone
- Zone B: pocketing pseudo-route zone
- Zone C: diffusing fringe

That was useful, but incomplete.

The next problem is:

- how much does each zone have to matter before it changes the whole-interface outcome?

In other words:

- when is an interface mostly `R3`?
- when is it mostly `R5`?
- when is it mostly diffuse?
- when is it genuinely mixed without one dominant logic?

This document addresses that problem.

## Core Claim

Local zones do not matter equally.

The whole-interface outcome depends not only on:

- which zones are present

but also on:

- how much of the active event they control
- how strongly they preserve or degrade route reality
- how effectively they compete with one another

So the programme now needs a first-pass dominance logic rather than only a spatial template.

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

## Dominance Is Not the Same as Area

This is the first key point.

A zone does not dominate simply because it occupies the largest geometric area.

A smaller local zone may dominate the outcome if it:

- controls the most viable completion route
- captures the active event early
- or suppresses the stronger route options of other zones

So dominance must include:

- geometric extent
- route leverage
- event capture
- competitive suppression

## First-Pass Weighting Factors

The current model suggests four main weighting factors.

## 1. Event Capture Weight

Meaning:

- how much of the active event is drawn into or retained by the zone

Why it matters:

- a small zone can dominate if it captures the event early and strongly

Most relevant to:

- pocketing zones
- return-biased zones
- strong boundary-face zones

## 2. Route Leverage Weight

Meaning:

- how much the zone controls the most viable route or suppresses it

Why it matters:

- a narrow route zone may dominate the entire outcome if it carries the only real completion path

Most relevant to:

- `O1`
- `O2`
- strong `R1` / `R3` conditions

## 3. Persistence Weight

Meaning:

- how long the zone can keep shaping the event before completion, dissipation, or transition to another zone occurs

Why it matters:

- some zones act briefly
- others keep the event stalled long enough to become decisive

Most relevant to:

- `L3`
- `R5`
- trapped-release conditions

## 4. Competitive Suppression Weight

Meaning:

- how strongly one zone reduces the influence of rival zones

Why it matters:

- a diffusing fringe may be present but weakly suppressive
- a pocketing zone may actively prevent access to a narrow viable route

Most relevant to:

- mixed interfaces
- obstruction competition
- route-field instability

## First-Pass Dominance Modes

Using those weights, the current programme can now define four dominance modes.

## Mode D1: Route-Dominant Interface

### Description

One zone controls the genuinely viable completion route strongly enough that the whole-interface outcome is mostly set by that route.

### Typical Profile

- strong route leverage
- medium or high event capture
- sufficient persistence
- rival zones do not suppress the route fully

### Typical Outcome

- mostly `R1`
- or mostly `R3` if the route fails late

### Best Current Cases

- selective `glass -> crystal`
- stronger `crystal -> air`

## Mode D2: Pocket-Dominant Interface

### Description

A local retention or pseudo-route zone captures enough of the event that pseudo-progressive looping becomes the dominant whole-interface logic.

### Typical Profile

- high event capture
- high persistence
- medium competitive suppression
- weak real route leverage elsewhere

### Typical Outcome

- mostly `R5`
- trapped release

### Best Current Cases

- glass release under pocketing terminal layers
- pseudo-compatibility subregions

## Mode D3: Diffusion-Dominant Interface

### Description

No strongly viable route or strong local pocket dominates. The event broadens, weakens, or spreads across low-quality continuation.

### Typical Profile

- low route leverage
- low/medium event capture by any one zone
- low strong persistence of bounded local structure
- weak but broad suppression of route dominance

### Typical Outcome

- mostly diffuse release
- weak distributed continuation
- or drift toward fragmentation

### Best Current Cases

- degraded `glass -> air`
- fringe-dominated exit surfaces

## Mode D4: Mixed Competitive Interface

### Description

No one zone dominates strongly enough to define the whole-interface outcome on its own. Several zones compete and the result depends on which local logic gains temporary advantage.

### Typical Profile

- medium event capture by multiple zones
- medium route leverage in one zone but not enough to dominate
- persistent competition between local route, pocket, and fringe behaviours

### Typical Outcome

- unstable mixture of `R3`, `R5`, and diffuse tendencies

### Best Current Cases

- frontier `glass -> air`
- frontier `glass -> crystal`

## What Makes a Zone Dominant?

Current best answer:

A zone dominates when it wins two tests at once:

1. it controls the event strongly enough
2. it controls the highest-leverage route logic strongly enough

This means:

- area alone is not enough
- intensity alone is not enough
- route reality alone is not enough

Dominance requires both:

- event control
- outcome leverage

## Interaction with `L_escape`

This is one of the most important parts of the document.

## High `L_escape`

If a zone preserves the strongest viable completion route, it can dominate even if it is not the largest zone.

This is why narrow route zones matter so much.

## Intermediate `L_escape`

This is the most unstable regime.

Why:

- route completion remains possible
- but local pocketing or diffusion may still capture the event

This is where mixed competitive interfaces are most likely.

## Low `L_escape`

If no zone preserves meaningful route viability, then:

- pocketing
- diffusion
- or fragmentation

will tend to dominate.

## Interaction with `Q_coh`

`Q_coh` affects dominance by shaping how much organisation a zone can preserve.

### High `Q_coh`

Favors:

- route-dominant interfaces
- ordered return
- strong bounded local structures

### Medium `Q_coh`

Favors:

- elongated stall
- trapped release
- mixed competitive zones

### Low/Falling `Q_coh`

Favors:

- diffusion-dominant interfaces
- fragmentation drift

## Interaction with `J_trans`

`J_trans` affects whether route-dominant zones can remain outcome-relevant.

### High `J_trans`

Supports:

- viable route continuation
- route-dominant outcomes

### Medium `J_trans`

Supports:

- `L3`
- `R3`
- `R5`
- unstable mixed zones

### Low `J_trans`

Supports:

- shallow retention
- diffusion
- failure of route leverage

## Best Current Benchmark Readings

## 1. Glass -> Air

Best current reading:

- usually `D2` or `D4`

Why:

- pocketing can dominate
- but blocked routes and diffusing fringes often coexist

This is the strongest mixed-interface benchmark.

## 2. Glass -> Crystal

Best current reading:

- `D1` in more successful selective regions
- `D4` in the frontier cases

Why:

- a narrow viable route can dominate if it survives
- but pseudo-compatibility and blocked routes can still compete strongly

## 3. Crystal -> Air

Best current reading:

- mostly `D1`

Why:

- ordered release more often preserves route leverage
- return bias may compete, but pseudo-pocketing is less central

## 4. Air -> Oxidised Metal

Best current reading:

- `D3`

Why:

- route leverage weakens
- fragmentation pressure rises
- no one clean route or pocket usually governs the whole surface strongly enough

## Strongest Current Consequences

## 1. Whole-Interface Outcome Can Now Be Weighted Rather Than Assumed

This is the main result.

The programme can now say:

- which zone matters most
- and why

instead of only naming which zones are present.

## 2. Mixed Cases Are Now More Modelable

This is crucial for the frontier material.

The strongest frontier cases were difficult partly because they looked internally inconsistent.

Now they can be read as:

- mixed competitive interfaces

rather than as:

- conceptually confused cases

## 3. `L_escape`, `Q_coh`, and `J_trans` Now Look Like the Strongest Dominance Modulators

These three appear to do the most work in deciding whether:

- route zones dominate
- pocket zones dominate
- diffuse fringes dominate

## 4. No New Primitive Variable Is Needed

Again this matters.

The current gains are still coming from:

- better weighting logic
- not from multiplying primitives

## Current Weak Point

The weighting logic is now good enough to use, but it still needs one more hardening step:

- explicit event-flow scenarios through the mixed interface

That is the obvious next move if the weighting scheme is going to become genuinely dynamic.

## Confidence

- confidence that subregion dominance must be modelled explicitly: `9/10`
- confidence that the four dominance modes are useful: `8/10`
- confidence that `glass -> air` and `glass -> crystal` are still the best mixed-interface benchmarks: `9/10`
- confidence that no new primitive split is needed yet: `8/10`

## Recommendation

Keep the current variable, loop, route, and obstruction frameworks unchanged.

Use dominance weighting as the next modelling layer.

## Next Move

The best next artifact is:

- `ams-mixed-interface-event-flow-scenarios-v1.md`

That should trace how one event may move:

- from route-dominant zone
- into pocket-dominant zone
- into diffusing fringe

or the reverse, so the mixed-interface model becomes explicitly dynamic rather than only weighted.*** End Patch
