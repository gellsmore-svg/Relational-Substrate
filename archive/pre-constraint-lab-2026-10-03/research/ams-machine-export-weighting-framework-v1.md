# AMS Machine Export Weighting Framework v1

## Purpose

This file introduces a first weighting framework for the main export channels by which local machine stress becomes whole-cell burden.

The earlier bridge file established the key channels:

- energy-order
- renewal
- boundary
- damage / repair
- coordination

The present file does one thing further:

```text
it gives them comparative weighting logic
```

The goal is not precision theatre. The goal is to move from:

```text
these channels matter
```

to:

```text
these channels matter in different magnitudes, at different speeds, and with different propagation leverage
```

## Central Claim

The central claim is:

> Machine-export burden is best analysed not as one undifferentiated stress output but as a weighted channel system in which some exports act quickly but locally, some act slowly but broadly, and some become especially dangerous because they amplify other channels rather than only contributing direct burden.

More briefly:

```text
Some burdens are heavy, some are fast, and some are contagious.
```

## Why Weighting Is Needed

The bridge from machine stress to cell state is now real, but still broad.

Without weighting, the ontology risks treating all export channels as if they:

- matter equally;
- propagate equally quickly;
- damage equally broadly;
- recover equally easily.

That is not true.

For example:

- ATP shortfall can spread quickly across many functions;
- mistranslation burden may accumulate more slowly but reshape architecture deeply;
- boundary leak can convert local problems into system-wide problems abruptly;
- oxidative burden can be both direct damage and amplifier;
- coordination loss often acts as a multiplier rather than an initial insult.

These differences need formal comparative handling.

## The Five Export Channels

The current framework keeps the same five channels:

1. `E_energy`
2. `E_renew`
3. `E_bound`
4. `E_damage`
5. `E_coord`

These should now be interpreted as weighted export burdens rather than simple presence labels.

## Three Weight Dimensions

Each channel should be weighted across three dimensions:

1. direct burden magnitude
2. propagation speed
3. amplification leverage

This gives a simple but useful matrix.

## 1. Direct Burden Magnitude

This means:

```text
how much immediate whole-cell load the channel contributes when elevated
```

Examples:

- ATP shortage often has high direct burden magnitude;
- mild signalling distortion may have lower immediate burden magnitude.

## 2. Propagation Speed

This means:

```text
how quickly the burden spreads from local machine stress into wider cell-state consequences
```

Examples:

- proton-field collapse may propagate quickly;
- gradual proteostatic burden may propagate more slowly.

## 3. Amplification Leverage

This means:

```text
how strongly a burden in one channel tends to worsen other channels rather than remaining isolated
```

Examples:

- damage / repair burden often has high amplification leverage;
- some local renewal problems may initially have lower leverage.

This third dimension is especially important.

Some burdens matter less because they are large in themselves than because they rewrite the rest of the system.

## Weight Scale

The simplest useful scale is:

```text
1 = low
2 = moderate
3 = high
```

This is enough for comparative control without pretending to precision.

Later versions could refine this numerically, but `1-3` is sufficient for a first framework.

## Baseline Channel Weights

The best current baseline weighting is:

| Channel | Direct burden | Propagation speed | Amplification leverage |
|---|---:|---:|---:|
| `E_energy` | `3` | `3` | `3` |
| `E_renew` | `3` | `2` | `3` |
| `E_bound` | `3` | `3` | `3` |
| `E_damage` | `2` | `2` | `3` |
| `E_coord` | `2` | `2` | `3` |

This is the best current baseline, not a final measured truth.

## Why These Weights Make Sense

## 1. `E_energy`

Energy-order burden is weighted:

```text
direct burden = 3
speed = 3
leverage = 3
```

because ATP shortage and related ordered-energy deficits rapidly affect:

- transport;
- repair;
- renewal;
- signalling;
- retention.

This is one of the most cell-owning channels.

## 2. `E_renew`

Renewal burden is weighted:

```text
direct burden = 3
speed = 2
leverage = 3
```

because architecture-renewal failure may not always collapse the cell instantly, but it has:

- deep medium-term burden;
- broad dependence across systems;
- strong secondary effects on maintenance and repair.

Translation and turnover failure often work this way.

## 3. `E_bound`

Boundary burden is weighted:

```text
direct burden = 3
speed = 3
leverage = 3
```

because retention failure can quickly destabilise:

- gradients;
- ionic control;
- compartmentation;
- selective transport;
- environmental buffering.

Boundary burden is one of the clearest routes from local defect to system-wide risk.

## 4. `E_damage`

Damage / repair burden is weighted:

```text
direct burden = 2
speed = 2
leverage = 3
```

because moderate damage does not always collapse the cell directly, but it strongly amplifies:

- energy demand;
- renewal demand;
- coordination cost;
- further machine weakening.

This channel often matters most through feedback.

## 5. `E_coord`

Coordination burden is weighted:

```text
direct burden = 2
speed = 2
leverage = 3
```

because coordination loss may initially appear abstract, but once it rises it tends to:

- reduce compensation quality;
- multiply local mismatches;
- worsen all other export channels.

It is usually more multiplier than first insult.

## Machine-Specific Weight Profiles

The baseline weights should be modified by machine type.

That is necessary because different machines export burden differently.

## Respiration-Dominant Export Profile

For respiration, the strongest current weighting profile is:

| Channel | Relative emphasis |
|---|---:|
| `E_energy` | `3` |
| `E_renew` | `1` |
| `E_bound` | `3` |
| `E_damage` | `3` |
| `E_coord` | `2` |

Interpretation:

- respiration most strongly exports energy-order burden;
- boundary burden is also very strong because proton and membrane logic are central;
- damage burden is strong because oxidative stress amplifies the machine's failure;
- coordination effects matter, but usually follow the primary burdens.

## Translation-Dominant Export Profile

For translation, the strongest current weighting profile is:

| Channel | Relative emphasis |
|---|---:|
| `E_energy` | `1` |
| `E_renew` | `3` |
| `E_bound` | `1` |
| `E_damage` | `2` |
| `E_coord` | `3` |

Interpretation:

- translation most strongly exports renewal burden;
- coordination burden is also strong because readable-order drift spreads through many downstream dependencies;
- damage burden is meaningful through proteostatic load;
- boundary burden is usually indirect rather than primary.

## Why Machine Profiles Matter

These profiles prevent a major mistake:

```text
treating every machine as if it exports the same kind of burden in the same proportions
```

That would flatten the ontology.

The weighting framework should instead preserve two truths:

1. all core machines can eventually affect the whole cell
2. they do not do so by the same dominant route

## First Composite Burden Formula

The simplest useful composite formula is:

```text
B_export = Σ (w_d * M_d + w_s * S_d + w_a * A_d) * C_d
```

where:

- `d` indexes the export channel;
- `M_d` = direct burden magnitude weight;
- `S_d` = propagation speed weight;
- `A_d` = amplification leverage weight;
- `C_d` = current channel activation level for the machine under study;
- `w_d`, `w_s`, `w_a` are analyst-set importance weights.

For the current stage, a simple equal weighting is acceptable:

```text
w_d = w_s = w_a = 1
```

which gives:

```text
B_export = Σ (M_d + S_d + A_d) * C_d
```

This is enough for comparative scenario ranking.

## Threshold Reading of the Composite Burden

The composite burden should not replace the detailed channels.

It should serve as a control indicator.

The best current reading is:

```text
low B_export = local burden likely containable
moderate B_export = stress compensation likely required
high B_export = cell-owning burden likely emerging
very high B_export = failure trajectory likely
```

This is a discipline tool, not a substitute for case analysis.

## Channel Interaction Rules

The weighting framework becomes much more useful when paired with a few interaction rules.

## Rule 1

```text
High E_energy tends to raise effective E_coord and E_renew pressure even when those channels are not the primary original insult.
```

## Rule 2

```text
High E_bound tends to accelerate E_energy and E_damage simultaneously.
```

## Rule 3

```text
High E_damage tends to amplify all other channels through rising repair and replacement cost.
```

## Rule 4

```text
High E_renew tends to increase E_coord first and E_energy second.
```

## Rule 5

```text
High E_coord often marks the point at which multiple burdens have stopped remaining separable.
```

These rules are still broad, but they already improve the bridge materially.

## Worked Comparative Reading

The framework can be illustrated simply.

## Case A: Respiratory Leak Crisis

Likely activation pattern:

```text
E_energy = high
E_bound = high
E_damage = high
E_coord = moderate
E_renew = low-moderate
```

Interpretation:

- fast export;
- high direct burden;
- strong amplification;
- likely rapid approach to cell-owning stress.

## Case B: Translation Drift Crisis

Likely activation pattern:

```text
E_renew = high
E_coord = high
E_damage = moderate
E_energy = low-moderate
E_bound = low
```

Interpretation:

- slower export;
- broad downstream burden;
- high cumulative amplification;
- more metastable interval before overt collapse.

This contrast is exactly what the framework is meant to preserve.

## Best Current Result

The best current compressed result is:

```text
Respiration exports burden fast and hard through energy, boundary, and damage channels, while translation exports burden more gradually but more diffusely through renewal and coordination channels.
```

That is the main gain of the framework.

## What This File Now Constrains

This file materially constrains:

1. the bridge from local machine decline to whole-cell burden;
2. the distinction between fast and slow export styles;
3. the distinction between direct burden and amplification burden;
4. the comparison between respiration and translation as cell-owning risk sources;
5. the next step toward a more formal machine-to-cell propagation model.

## Immediate Follow-On

The best next file is:

```text
ams-machine-export-weighted-comparison-v1.md
```

Reason:

The framework now exists. The next step is to apply it comparatively across the two strongest machine cases and see whether the weighting logic materially sharpens the calibration layer.

## Compact Grammar

The best compression is:

```text
Some machine burdens hit harder, some spread faster, and some mainly make everything else worse.
```

## Provisional Conclusion

The machine-to-cell bridge is now more disciplined than before.

AMS weighting summary:

```text
Machine export should now be read as a weighted channel system in which energy-order and boundary burdens tend to spread quickly and directly, renewal burden tends to spread more gradually but deeply, and damage and coordination burdens often matter most because they amplify the rest of the system.
```

Score:

```text
machine export weighting framework: 9.0/10
```
