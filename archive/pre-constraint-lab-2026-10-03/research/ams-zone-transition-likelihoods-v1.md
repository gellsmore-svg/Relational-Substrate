# AMS Zone Transition Likelihoods v1

## Purpose

This document turns the mixed-interface event-flow scenarios into a structured transition-likelihood model.

The previous document established that frontier interfaces are best understood dynamically, with events moving between:

- route-dominant zones
- pocket-dominant zones
- diffusing fringes

The next problem is:

- how likely are those transitions under the current benchmark conditions?

This document answers that in a first-pass qualitative way.

## Context

From:

- `ams-mixed-interface-event-flow-scenarios-v1.md`

the main event-flow paths included:

- route-led completion
- route-then-block
- route-then-pocket capture
- pocket-led retention
- pocket-to-diffuse bleed
- route-to-diffuse collapse
- mixed competitive oscillation

The present document turns those into transition-likelihood judgments.

## Scope

This is not a mathematical transition matrix.

It is a structured qualitative likelihood model using:

- very low
- low
- medium
- high
- very high

The aim is to determine:

- which transitions are stable tendencies
- which are frontier-sensitive
- which are relatively rare edge cases

## Active Mixed-Interface Zones

### Zone A

- route-dominant zone
- strongest associations:
  - `O2`
  - `R3`
  - `R1`

### Zone B

- pocket-dominant zone
- strongest associations:
  - `O3`
  - `R5`

### Zone C

- diffusing fringe
- strongest associations:
  - `O5`
  - `R2`
  - sometimes drift toward `R6`

## Transition Classes in Scope

- `A -> completion`
- `A -> B`
- `A -> C`
- `B -> B` persistence
- `B -> C`
- `B -> completion`
- `C -> completion`
- `D4 mixed competitive -> A`
- `D4 mixed competitive -> B`
- `D4 mixed competitive -> C`

## Baseline Transition Table

| Transition | Baseline likelihood | Current interpretation |
|---|---|---|
| `A -> completion` | medium/high | real route zones often remain completion-capable if leverage holds |
| `A -> B` | medium/high | one of the strongest frontier transitions; route can lose leverage into pocket capture |
| `A -> C` | medium | route can collapse into diffusing fringe if coherence weakens broadly |
| `B -> B` persistence | high | pocket zones are good at retaining events once capture occurs |
| `B -> C` | medium/high | pocket logic often degrades outward into diffuse spill if coherence weakens |
| `B -> completion` | low/medium | possible, but not the dominant behaviour of pocket zones |
| `C -> completion` | low | weak distributed continuation rarely sharpens into robust completion on its own |
| `D4 -> A` | medium | route leverage can still win in mixed interfaces if completion logic strengthens |
| `D4 -> B` | medium/high | pocket capture is often the easiest local winner in frontier conditions |
| `D4 -> C` | medium | fringe drift is plausible when neither route nor pocket dominates |

## Transition-by-Transition Analysis

## 1. `A -> completion`

### Likelihood

- medium/high

### Why

If a route-dominant zone already controls the strongest viable path, completion remains one of the most natural outcomes.

What prevents this from being “very high” is that frontier route zones often still face:

- late-gate blockage
- local pocket capture
- route leverage decay

### Best Cases

- stronger `crystal -> air`
- selective `glass -> crystal`

## 2. `A -> B`

### Likelihood

- medium/high

### Why

This is one of the most important transitions in the whole programme.

It captures:

- route-then-pocket capture

The path begins as genuinely completion-directed, but local pocketing overtakes route leverage before completion occurs.

### Best Cases

- frontier `glass -> air`
- frontier `glass -> crystal`

### Importance

This is one of the clearest dynamic routes into:

- `R3 -> R5`

## 3. `A -> C`

### Likelihood

- medium

### Why

This transition happens when route logic weakens broadly rather than being captured by one bounded pocket.

It appears less central than `A -> B`, because many frontier cases preserve local activity strongly enough that pocket capture is more likely than pure diffusion collapse.

### Best Cases

- degraded `glass -> air`
- degraded compatibility zones

## 4. `B -> B` Persistence

### Likelihood

- high

### Why

Pocket zones are locally self-maintaining once event capture occurs.

They preserve:

- local activity
- local coherence
- pseudo-progressive looping

without needing strong outward completion logic.

### Best Cases

- trapped glass release
- pseudo-compatibility local cycling

## 5. `B -> C`

### Likelihood

- medium/high

### Why

Pocket persistence is strong, but not indefinitely stable.

If:

- `Q_coh` falls
- `J_trans` weakens further
- local boundedness degrades

then the pocket may bleed into diffusing fringe behaviour.

### Best Cases

- degraded `glass -> air`
- pocket-to-diffuse release transitions

## 6. `B -> completion`

### Likelihood

- low/medium

### Why

Pocket zones are not built for completion.

Completion from a pocket is possible only if:

- local reseating reorganises into a genuine route
- route leverage rises enough to overcome local loop dominance

That can happen, but it is not the normal direction of travel.

### Best Cases

- cleaner edge conditions in glass release
- recovered compatibility after local pocket instability

## 7. `C -> completion`

### Likelihood

- low

### Why

Diffusing fringe behaviour weakens route dominance rather than strengthening it.

So completion from Zone C usually requires a stronger restructuring than the current frontier cases normally preserve.

### Best Cases

- weak and rare

This should be treated as an edge case, not a main pathway.

## 8. `D4 Mixed Competitive -> A`

### Likelihood

- medium

### Why

Mixed interfaces can still resolve into route dominance if:

- one viable route persists
- route leverage rises
- `L_escape` remains more real than apparent

This is plausible, but not automatic.

### Best Cases

- selective `glass -> crystal`
- stronger mixed `crystal -> air`

## 9. `D4 Mixed Competitive -> B`

### Likelihood

- medium/high

### Why

Pocket capture is often the easiest way for a mixed interface to resolve locally.

This is especially true when:

- local activity is already strong
- one route is plausible but not dominant
- bounded local reseating offers a more stable immediate regime

### Best Cases

- frontier `glass -> air`
- frontier `glass -> crystal`

## 10. `D4 Mixed Competitive -> C`

### Likelihood

- medium

### Why

If no route and no pocket secures dominance, a mixed competitive interface may drift into diffuse broadening.

This is plausible, but often secondary to pocket capture in the strongest frontier glass cases.

## Benchmark-Specific Transition Patterns

## Glass -> Air

Strongest transitions:

- `A -> B`
- `B -> B`
- `B -> C`
- `D4 -> B`

Interpretation:

This remains the strongest benchmark for:

- route-to-pocket capture
- pocket persistence
- pocket-to-diffuse degradation

## Glass -> Crystal

Strongest transitions:

- `A -> completion`
- `A -> B`
- `D4 -> A`
- `D4 -> B`

Interpretation:

This remains the strongest benchmark for:

- selective viable handoff
- blocked route drift
- pseudo-compatibility pocketing

## Crystal -> Air

Strongest transitions:

- `A -> completion`
- `A -> A` persistence implied
- `D4 -> A`

Weaker transitions:

- `A -> B`
- `B -> B`

Interpretation:

Crystal-like cases preserve route dominance better and are less hospitable to persistent pocket logic.

## Air -> Oxidised Metal

Strongest transitions:

- `A -> C`
- `D4 -> C`

Interpretation:

This case remains the best benchmark for broad route degradation into fragmentation-adjacent behaviour rather than for stable pocket capture.

## Strongest Current Dynamic Conclusions

## 1. `A -> B` Is a Core Frontier Transition

This is one of the biggest results in the document.

It means:

- a genuinely real route can degrade into pocket-dominant pseudo-progression

That is a more precise dynamic statement than the programme could make earlier.

## 2. `B -> B` and `B -> C` Together Define Pocket Behaviour

Pocket zones:

- tend to retain events strongly
- but often eventually bleed into diffusion if coherence and boundedness weaken

This gives the programme a usable dynamic picture of trapped-release evolution.

## 3. `D4 -> B` Is Often More Likely Than `D4 -> A`

Especially in the frontier glass cases.

That means mixed interfaces often resolve locally into:

- pocket capture

before they resolve into:

- recovered route dominance

This is an important and somewhat sobering result.

## 4. `C -> completion` Is Rare

That is another stabilising result.

Diffuse fringe behaviour is not a common route back to strong completion.

Once the event has genuinely diffused, the programme should not overstate how easily it recovers.

## Programme-Level Significance

## 1. The Mixed-Interface Model Is Now Dynamically Usable

This is the main result.

The model can now say not just:

- what zones exist

but:

- which transitions are likely

That is a major step.

## 2. The Glass Frontiers Are Still the Best Dynamic Test Beds

Again this is reinforced.

The strongest mixed dynamic transitions all remain clearest in:

- `glass -> air`
- `glass -> crystal`

## 3. No New Variables Are Needed

The current dynamic gains still come from:

- sequencing
- weighting
- transition-likelihood logic

not from adding more primitives.

## Current Weak Point

The transition-likelihood model is now useful, but it still needs one final tightening step:

- a compact decision framework for diagnosing which mixed-interface flow is occurring in a given case

That is the obvious next move.

## Confidence

- confidence that the transition-likelihood model is useful: `8/10`
- confidence that `A -> B` is one of the key frontier transitions: `9/10`
- confidence that `B -> B` and `B -> C` now capture pocket dynamics well: `8/10`
- confidence that no new primitive split is needed yet: `8/10`

## Recommendation

Keep the current framework unchanged.

Use the likelihood model as the dynamic layer on top of the mixed-subregion model.

## Next Move

The best next artifact is:

- `ams-mixed-interface-diagnostic-framework-v1.md`

That should provide a compact decision framework for diagnosing:

- which zones are present
- which zone currently dominates
- which transitions are most likely
- whether the case is primarily:
  - route-dominant
  - pocket-dominant
  - diffuse
  - or genuinely mixed competitive
