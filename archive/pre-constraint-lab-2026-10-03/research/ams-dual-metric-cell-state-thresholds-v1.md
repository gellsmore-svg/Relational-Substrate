# AMS Dual-Metric Cell-State Thresholds v1

## Purpose

This file maps the new dual burden metrics into whole-cell state thresholds.

The previous file established two distinct machine-export outputs:

```text
A_burden = acute collapse pressure
C_burden = cumulative architecture-decay pressure
```

The present question is:

```text
how should different combinations of acute and cumulative burden map into cell-state change?
```

This matters because the earlier cell-state bridge used three broad whole-cell states:

- coherent state
- stress compensation state
- failure state

The dual-metric model can now sharpen how the system moves between them.

## Central Claim

The central claim is:

> Whole-cell state is now best read through the interaction of acute and cumulative burden rather than by a single generic stress axis: high acute burden drives rapid instability, high cumulative burden drives progressive decay of recoverable order, and the most dangerous cell states arise when both are elevated strongly enough that compensation can neither stabilise the present nor preserve the future.

More briefly:

```text
Cells can fail quickly, slowly, or by both at once.
```

## Why the Dual Threshold Model Is Needed

The older bridge file already improved the ontology by showing that cell failure emerges when local machine burdens become globally owning.

But it still treated cell-state progression too much like one burden curve.

That was enough for a first bridge, but not enough after the weighting work.

The new dual-metric model matters because:

- some cells face rapid destabilisation before long-term decay matters;
- some cells remain active while cumulative decay quietly worsens;
- some cells experience both together and become much harder to recover.

One threshold axis is not enough to represent those cases cleanly.

## The Two Axes

The cell-state model should now be read on two axes:

## Axis 1: Acute Burden

```text
A_burden
```

This tracks:

- rapid destabilisation pressure;
- immediate threshold-crossing risk;
- collapse-prone burden in energy, boundary, and severe damage channels.

## Axis 2: Cumulative Burden

```text
C_burden
```

This tracks:

- architecture decay over time;
- renewal and coordination burden;
- slower erosion of recoverable order.

Together these give a cell-state plane rather than a single line.

## Four Main Cell-State Regions

The dual model implies four main regions.

## Region I: Low Acute / Low Cumulative

Interpretation:

```text
coherent cell state
```

This means:

- present stability remains strong;
- future recoverability remains strong;
- local burden exists only as bounded margin.

This is the ordinary viable state.

## Region II: High Acute / Low Cumulative

Interpretation:

```text
acute stress state
```

This means:

- immediate destabilisation risk is high;
- long-run decay is not yet the dominant problem;
- the cell may recover if rapid stabilisation succeeds.

This is the classic respiratory-crisis style region.

## Region III: Low Acute / High Cumulative

Interpretation:

```text
chronic degradation state
```

This means:

- the cell is not yet collapsing rapidly;
- architecture, coordination, and renewal are being worn down;
- recoverability is narrowing with time.

This is the classic translation-drift or slow proteostatic burden region.

## Region IV: High Acute / High Cumulative

Interpretation:

```text
compound failure state
```

This means:

- present stability is badly threatened;
- future recoverability is also badly eroded;
- the cell is under both collapse pressure and architecture-decay pressure at once.

This is the most dangerous region and usually the hardest to reverse.

## Mapping Back to the Earlier Three-State Model

The dual-region model does not abolish the earlier three-state model.

It refines it.

## Coherent State

Earlier category:

```text
coherent state
```

Dual reading:

```text
low A_burden
low C_burden
```

## Stress Compensation State

Earlier category:

```text
stress compensation state
```

Dual reading:

```text
either high A_burden with still-manageable C_burden
or high C_burden with still-manageable A_burden
```

This means stress compensation now has two major forms:

- acute compensation
- chronic compensation

That is a real improvement.

## Failure State

Earlier category:

```text
failure state
```

Dual reading:

```text
very high A_burden
or very high C_burden with recoverability collapse
or both together
```

This is better than using one generic failure threshold.

## First Threshold Bands

The dual metrics are still comparative outputs, so the threshold bands should remain banded rather than over-precise.

Use:

```text
low = lower third of current comparative burden range
moderate = middle third
high = upper third
very high = upper edge with strong cross-channel reinforcement
```

For current internal use, the simplest working bands are:

## Acute Burden Bands

```text
low A_burden      = < 110
moderate A_burden = 110-150
high A_burden     = 150-185
very high         = > 185
```

## Cumulative Burden Bands

```text
low C_burden      = < 105
moderate C_burden = 105-125
high C_burden     = 125-145
very high         = > 145
```

These are provisional internal bands based on the current respiration/translation calibration set, not universal biological constants.

## Cell-State Threshold Rules

The best current bridge rules are:

## Rule 1

```text
Low A_burden and low C_burden = coherent cell state.
```

## Rule 2

```text
High A_burden with only moderate C_burden = acute stress compensation state.
```

This is the cell trying to stabilise the present before long-run decay has fully set in.

## Rule 3

```text
High C_burden with only moderate A_burden = chronic degradation state within stress compensation.
```

This is the cell remaining present-tense viable while future recoverability narrows.

## Rule 4

```text
High A_burden and high C_burden together = compound failure trajectory.
```

This is the clearest sign that both present stability and future recoverability are being lost together.

## Rule 5

```text
Very high A_burden can force rapid failure even before cumulative burden becomes dominant.
```

This preserves the reality of acute collapse.

## Rule 6

```text
Very high C_burden can force unrecoverable decline even without dramatic acute collapse if architecture, coordination, and renewal erosion become too severe.
```

This preserves the reality of slow ontological failure.

## The Two Main Stress Styles

The dual-threshold model now gives two main stress styles.

## 1. Acute-Dominant Stress

Characteristics:

- destabilisation is the main immediate problem;
- energy, boundary, and severe damage channels dominate;
- time to collapse is short if compensation fails.

Best machine analogue:

```text
respiration crisis
```

## 2. Cumulative-Dominant Stress

Characteristics:

- present function may continue for some time;
- renewal and coordination burden dominate;
- recoverability decays before outright collapse becomes obvious.

Best machine analogue:

```text
translation drift crisis
```

These styles should now be built into cell-state interpretation rather than treated as secondary nuance.

## Compound Failure Logic

The dual model becomes most useful when both metrics rise together.

This is the strongest current reading:

```text
compound failure begins when high acute burden prevents stable compensation while high cumulative burden simultaneously removes the reserve needed for future recovery
```

This is worse than either burden alone.

It means:

- the cell cannot secure the present;
- the cell cannot rebuild the future.

That is the clearest whole-cell approach to death in the current framework.

## Mapping the Core Machines onto the Cell-State Plane

Using the current dual scores:

## Respiration

```text
A_burden = 183.5
C_burden = 134.5
```

Respiration therefore sits in:

```text
high acute
high cumulative
```

but with stronger emphasis on the acute side.

Interpretation:

```text
acute-dominant compound threat
```

## Translation

```text
A_burden = 124.1
C_burden = 124.3
```

Translation therefore sits in:

```text
moderate acute
moderate-high cumulative
```

Interpretation:

```text
chronic-degradation dominant threat
```

This is a much clearer reading than the earlier one-score model could give.

## What This Clarifies About the Life Boundary

The life boundary now becomes more precise.

A living cell remains living while:

- acute burden has not irreversibly destabilised present coherence;
- cumulative burden has not irreversibly eroded recoverable order;
- the machine-remaking loop still belongs to the bounded system strongly enough to recover.

That means life is not lost merely because:

- acute burden rises;
- or cumulative burden rises.

Life is lost when these burdens cross far enough that recoverable machine-remaking coherence is no longer owned by the cell.

This is one of the strongest gains in the ontology so far.

## Best Current Result

The best current compressed result is:

```text
Cell states should now be read on two axes: one for how hard the cell is being pushed toward collapse now, and one for how strongly its recoverable order is being eroded over time.
```

That is the main gain of this file.

## What This File Now Constrains

This file materially constrains:

1. the bridge from dual machine metrics to whole-cell state;
2. the distinction between acute stress and chronic degradation;
3. the interpretation of compound failure;
4. the life-boundary relation to machine burden;
5. the next stage of machine-to-cell formal refinement.

## Immediate Follow-On

The best next file is:

```text
ams-machine-burden-to-life-boundary-integration-v1.md
```

Reason:

The dual metrics now exist and have been mapped to cell-state regions.

The next step is to integrate this directly into the living-state ontology so that:

- recoverability;
- viability;
- latency;
- failure

can all be discussed with the stronger burden grammar rather than older looser language.

## Compact Grammar

The best compression is:

```text
Cells do not just have one way to fail: they can be driven over, worn down, or both.
```

## Provisional Conclusion

The cell-state model is now materially better than before.

AMS dual-threshold summary:

```text
Whole-cell state should now be read on a dual burden plane: acute burden tracks pressure toward rapid instability, cumulative burden tracks erosion of recoverable order, and the most dangerous states arise when both are elevated strongly enough that the cell can neither stabilise the present nor preserve the future.
```

Score:

```text
dual metric cell-state thresholds: 9.3/10
```
