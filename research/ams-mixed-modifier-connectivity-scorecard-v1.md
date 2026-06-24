# AMS Mixed Modifier Connectivity Scorecard v1

## Purpose

This scorecard tests the six connectivity regimes from the mixed Na/Mg silicate percolation study against five explanatory targets:

- ion mobility
- chemical durability
- viscosity / softening
- interface release behavior
- explanatory distinctiveness over a simple composition-average model

The goal is not to claim direct observation of vortons. The goal is to test whether the AMS subregion and connectivity model gives a sharper account of mixed modifier behavior than a flat average of sodium and magnesium effects.

## Scoring Scale

Scores use a 1-10 comparative confidence scale.

```text
1-3  weak fit; mostly speculative or redundant
4-5  plausible but underconstrained
6    useful directional model
7    good fit with clear comparative advantage
8    strong fit across multiple property classes
9    very strong fit with repeated explanatory success
10   reserved for direct, mature, highly constrained modelling
```

At this stage, scores above 8 should be rare. Mixed modifier modelling is still indirect and comparative.

## Regime Summary

| Regime | Connectivity condition | Dominance | Short description |
|---:|---|---|---|
| 1 | isolated `M2` islands | `D1/D4` | sodium-rich loosening remains local |
| 2 | connected `M2` pathways | `D3` | sodium-rich weak paths dominate |
| 3 | interrupted `M2` pathways | `D4` | sodium routes begin but are gated |
| 4 | connected `M1/M3` backbone | `D1/D4` | constraint network remains dominant |
| 5 | frequent `M4` junctions | `D4` | mixed competition controls handoff |
| 6 | fragmented high-disorder field | `D3/R6` | disorder overwhelms route coherence |

## Score Matrix

| Regime | Ion mobility | Durability | Viscosity / softening | Interface release | Distinctiveness vs average model | Mean |
|---:|---:|---:|---:|---:|---:|---:|
| 1 isolated `M2` islands | 6 | 6 | 5 | 5 | 6 | 5.6 |
| 2 connected `M2` pathways | 8 | 8 | 7 | 6 | 7 | 7.2 |
| 3 interrupted `M2` pathways | 8 | 7 | 7 | 7 | 8 | 7.4 |
| 4 connected `M1/M3` backbone | 7 | 8 | 7 | 7 | 7 | 7.2 |
| 5 frequent `M4` junctions | 7 | 7 | 8 | 7 | 9 | 7.6 |
| 6 fragmented high-disorder field | 7 | 6 | 6 | 7 | 6 | 6.4 |

## Regime Notes

### Regime 1: Isolated `M2` Islands

Score profile:

```text
mean: 5.6
```

This regime is useful but not decisive. It explains why sodium-rich loosening may exist locally without dominating the whole material.

Its strongest use is negative: it prevents over-reading sodium presence as automatic material-scale diffusion.

AMS interpretation:

```text
M2 present but not connected
=> local D3 pockets
=> whole field remains D1/D4
```

This is a necessary guardrail, but it does not strongly distinguish AMS from conventional composition-plus-structure reasoning.

### Regime 2: Connected `M2` Pathways

Score profile:

```text
mean: 7.2
```

This regime is strong for ion mobility and durability.

If sodium-rich weak paths connect, then the material should show a step-change in mobility and degradation vulnerability relative to isolated sodium-rich pockets.

AMS interpretation:

```text
M2 connected
=> R2/O5/D3
=> mobility and degradation become pathway-controlled
```

This is one of the clearest AMS predictions because it distinguishes local modifier chemistry from whole-field route continuity.

Weakness:

Interface release remains less certain unless the connected `M2` path reaches a boundary in a specific geometry.

### Regime 3: Interrupted `M2` Pathways

Score profile:

```text
mean: 7.4
```

This is the strongest ordinary mixed-modifier regime.

It explains why a material can show sodium-like mobility pressure without fully behaving like a sodium-dominated glass. The route begins as distributed diffusion but repeatedly encounters selective gates.

AMS interpretation:

```text
M2 nearly connected
but interrupted by M1/M3
=> R2 -> R3
=> O5 -> O2
=> D4
```

This has strong explanatory value because a simple average model struggles to represent route initiation and route termination as different events.

It also explains non-linear behavior without requiring every local region to behave anomalously.

### Regime 4: Connected `M1/M3` Backbone

Score profile:

```text
mean: 7.2
```

This regime explains retained constraint.

Even when sodium-rich regions exist, a connected silica-rich or magnesium-rich constraint network can prevent broad diffusion from dominating.

AMS interpretation:

```text
M1/M3 connected
=> R1/R3
=> O1/O2
=> D1/D4
```

This matters because it prevents the model from being sodium-centric. Magnesium and silica are not treated as merely reducing sodium effects; they impose route structure and gate behavior.

### Regime 5: Frequent `M4` Junctions

Score profile:

```text
mean: 7.6
```

This is the strongest distinctiveness case.

`M4` junctions explain non-linear mixed modifier behavior as a competition of handoff nodes rather than as a weighted average of two modifiers.

AMS interpretation:

```text
frequent M4
=> local route handoff instability
=> R1/R2/R3 with local R5
=> O1/O2/O5 with local O3
=> D4
```

This regime gives AMS a specific mechanism-facing advantage: the model can say where non-linearity enters. It enters at the junction between incompatible local route grammars.

Weakness:

This regime needs composition-specific cases before it can be scored higher. Without specific structural evidence, `M4` remains a powerful but abstract explanatory category.

### Regime 6: Fragmented High-Disorder Field

Score profile:

```text
mean: 6.4
```

This regime is plausible but less distinctive.

It explains cases where disorder becomes so high that route coherence breaks down, producing broad diffusion, irregular release, and durability weakness.

AMS interpretation:

```text
M2 abundant
M1 broken
M3 unable to impose coherent gates
=> R2/R6
=> O5/O6
=> D3/R6
```

The weakness is that conventional disorder language already explains much of this. AMS adds route and obstruction detail, but the comparative advantage is smaller than in regimes 3 and 5.

## Comparative Findings

### Strongest Regime

```text
Regime 5: frequent M4 junctions
mean 7.6
```

This is the strongest AMS-specific regime because it explains non-linear mixed modifier behavior through local route competition.

### Strongest Property Anchor

```text
ion mobility
```

Ion mobility remains the best property class for testing the connectivity model. It should respond sharply to whether weak sodium-rich regions are isolated, interrupted, or connected.

### Strongest Material-Scale Transition

```text
isolated M2 -> connected M2
```

This transition is the clearest percolation threshold.

AMS prediction:

```text
local sodium-rich loosening does not imply material-scale mobility
until M2 regions connect into through-going route fields.
```

### Strongest Mixed-Modifier Signature

```text
connected or nearly connected M2 repeatedly interrupted by M1/M3/M4
```

This produces:

- non-linear mobility
- uneven durability
- route initiation without route completion
- late-gate failures
- mixed `D4` dominance

This is more informative than saying that sodium lowers constraint and magnesium raises it.

## Score Implication for Mixed Na/Mg Silicate

Previous score:

```text
mixed Na/Mg silicate: 6.5/10, upward pressure
```

The scorecard supports a move to:

```text
mixed Na/Mg silicate: 7/10
```

Reason:

The model now has a clear, testable comparative structure. It does not only assert that mixed modifiers produce mixed effects. It specifies the route conditions under which sodium-rich diffusion dominates, fails, is interrupted, or becomes locally trapped in mixed handoff nodes.

The score should not move above 7 yet because:

- no specific composition has been fully mapped
- no quantitative percolation threshold has been assigned
- optical and interface behavior remain secondary anchors
- the model is still inferred from structural and property coherence

## Updated Score Entry

```text
Case: mixed Na/Mg silicate
Previous score: 6.5
Updated score: 7
Confidence: moderate
Reason: connectivity and regime scorecard provide clear comparative advantage over simple composition averaging.
Primary anchors: ion mobility, durability, viscosity / softening non-linearity.
Secondary anchors: interface release and surface behavior.
Next pressure: composition-specific mapping.
```

## Next Artifact

The next useful artifact should be:

```text
ams-specific-mixed-silicate-composition-template-v1.md
```

That template should define how to map a named composition into:

- approximate `M1/M2/M3/M4` proportions
- likely connectivity regime
- expected route class
- expected obstruction class
- predicted property behavior
- score adjustment pressure

This is the necessary step before scoring real compositions rather than the family-level mixed Na/Mg class.
