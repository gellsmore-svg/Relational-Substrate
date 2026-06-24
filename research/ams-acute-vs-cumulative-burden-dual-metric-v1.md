# AMS Acute vs Cumulative Burden Dual Metric v1

## Purpose

This file refines the machine-export weighting model by separating two kinds of whole-cell burden that the earlier single-score model compressed too tightly:

1. acute collapse pressure
2. cumulative architecture-decay pressure

The sensitivity test showed why this is necessary.

A single total burden score can be useful, but it hides an important distinction:

```text
a machine can be the sharper acute threat
without being the greater long-run burden source
```

This file therefore introduces a dual-metric framework.

## Central Claim

The central claim is:

> Whole-cell machine burden should now be read through two linked but distinct metrics: acute burden measures how strongly a machine pushes the cell toward rapid instability and collapse, while cumulative burden measures how strongly a machine erodes architecture, coordination, and recoverable order over time. Respiration dominates the first more often; translation can rival or exceed it in the second under amplification-heavy conditions.

More briefly:

```text
Some machines break the cell quickly; others wear out the conditions of living coherence.
```

## Why One Score Is Not Enough

The earlier weighting model already improved the machine-to-cell bridge.

But the sensitivity test exposed a structural problem:

- respiration often dominates through fast, direct, high-leverage burden;
- translation can dominate under some assumptions through slower but broader amplification.

If these are forced into one score, the ontology risks making one of two mistakes:

- treating slow degradation as if it were simply weaker collapse pressure;
- treating fast collapse as if it were simply a larger version of cumulative decay.

Both are wrong.

The model therefore needs two outputs.

## The Two Metrics

The dual-metric framework introduces:

```text
A_burden = acute collapse pressure
C_burden = cumulative architecture-decay pressure
```

These are related, but not identical.

## 1. Acute Collapse Pressure

`A_burden` asks:

```text
how strongly is the current machine state pushing the cell toward rapid instability, threshold crossing, and failure?
```

This metric should emphasise:

- direct burden magnitude;
- propagation speed;
- channels that destabilise essential retention and energetic support rapidly.

## 2. Cumulative Architecture-Decay Pressure

`C_burden` asks:

```text
how strongly is the current machine state eroding architecture, renewal quality, coordination, and recoverable order over time?
```

This metric should emphasise:

- amplification leverage;
- renewal strain;
- coordination strain;
- burdens that accumulate and widen system dependence over longer intervals.

## Channel Priorities by Metric

The five export channels remain:

- `E_energy`
- `E_renew`
- `E_bound`
- `E_damage`
- `E_coord`

But they should now be weighted differently for the two metrics.

## Acute Metric Priorities

For `A_burden`, the strongest current priority order is:

```text
E_energy
E_bound
E_damage
E_coord
E_renew
```

Why:

- energy failure quickly constrains almost everything;
- boundary loss rapidly destabilises retention and gradients;
- damage can become rapidly self-amplifying;
- coordination matters, but often after major destabilisation has begun;
- renewal burden is often serious, but slower in its whole-cell consequences.

## Cumulative Metric Priorities

For `C_burden`, the strongest current priority order is:

```text
E_renew
E_coord
E_damage
E_energy
E_bound
```

Why:

- renewal failure erodes architecture over time;
- coordination strain multiplies downstream mismatch;
- damage burden accumulates through repair and replacement cost;
- energy burden matters here too, but often as a secondary amplifier unless acutely severe;
- boundary burden can be cumulative, but in the strongest cases it often behaves more acutely.

## First Dual Weight Sets

The simplest useful dual weighting is:

## Acute Weights

```text
w_d = 2
w_s = 2
w_a = 1
```

This privileges:

- direct burden
- speed

over:

- longer-run amplification

## Cumulative Weights

```text
w_d = 1
w_s = 1
w_a = 2
```

This privileges:

- amplification

while still keeping:

- direct burden
- speed

in view.

## Channel Coefficients by Metric

To prevent the two metrics from differing only slightly, channel-specific emphasis should also change.

## Acute Channel Coefficients

Use:

| Channel | Coefficient |
|---|---:|
| `E_energy` | `1.3` |
| `E_renew` | `0.8` |
| `E_bound` | `1.3` |
| `E_damage` | `1.1` |
| `E_coord` | `0.9` |

## Cumulative Channel Coefficients

Use:

| Channel | Coefficient |
|---|---:|
| `E_energy` | `0.9` |
| `E_renew` | `1.3` |
| `E_bound` | `0.8` |
| `E_damage` | `1.1` |
| `E_coord` | `1.3` |

These are not measurements. They are a first disciplined way of encoding what the sensitivity test already implied.

## Dual-Metric Formulae

The simplest useful formulae are:

```text
A_burden = Σ ((2M + 2S + A) * K_A(d) * C_d)
C_burden = Σ ((M + S + 2A) * K_C(d) * C_d)
```

where:

- `d` indexes channels;
- `K_A(d)` is the acute channel coefficient;
- `K_C(d)` is the cumulative channel coefficient;
- `C_d` is the machine-specific activation level.

This is enough for a first dual-metric comparison.

## Baseline Channel Scores Under the Dual Model

Using the earlier baseline channel values:

| Channel | `M` | `S` | `A` |
|---|---:|---:|---:|
| `E_energy` | `3` | `3` | `3` |
| `E_renew` | `3` | `2` | `3` |
| `E_bound` | `3` | `3` | `3` |
| `E_damage` | `2` | `2` | `3` |
| `E_coord` | `2` | `2` | `3` |

The raw metric sums become:

## Acute Raw Sums

| Channel | Raw acute sum |
|---|---:|
| `E_energy` | `15` |
| `E_renew` | `13` |
| `E_bound` | `15` |
| `E_damage` | `11` |
| `E_coord` | `11` |

## Cumulative Raw Sums

| Channel | Raw cumulative sum |
|---|---:|
| `E_energy` | `12` |
| `E_renew` | `11` |
| `E_bound` | `12` |
| `E_damage` | `10` |
| `E_coord` | `10` |

After applying coefficients:

## Acute Effective Channel Weights

| Channel | Effective acute weight |
|---|---:|
| `E_energy` | `19.5` |
| `E_renew` | `10.4` |
| `E_bound` | `19.5` |
| `E_damage` | `12.1` |
| `E_coord` | `9.9` |

## Cumulative Effective Channel Weights

| Channel | Effective cumulative weight |
|---|---:|
| `E_energy` | `10.8` |
| `E_renew` | `14.3` |
| `E_bound` | `9.6` |
| `E_damage` | `11.0` |
| `E_coord` | `13.0` |

This already encodes the core distinction:

```text
acute burden privileges energy and boundary
cumulative burden privileges renewal and coordination
```

## Machine Application: Respiration

Respiration activation profile remains:

```text
E_energy = 3
E_renew = 1
E_bound = 3
E_damage = 3
E_coord = 2
```

## Respiration Acute Score

```text
(19.5 * 3) + (10.4 * 1) + (19.5 * 3) + (12.1 * 3) + (9.9 * 2)
= 58.5 + 10.4 + 58.5 + 36.3 + 19.8
= 183.5
```

## Respiration Cumulative Score

```text
(10.8 * 3) + (14.3 * 1) + (9.6 * 3) + (11.0 * 3) + (13.0 * 2)
= 32.4 + 14.3 + 28.8 + 33.0 + 26.0
= 134.5
```

Interpretation:

- respiration is extremely strong in acute burden;
- it is still serious in cumulative burden;
- but its sharpest distinctiveness lies in collapse pressure.

## Machine Application: Translation

Translation activation profile remains:

```text
E_energy = 1
E_renew = 3
E_bound = 1
E_damage = 2
E_coord = 3
```

## Translation Acute Score

```text
(19.5 * 1) + (10.4 * 3) + (19.5 * 1) + (12.1 * 2) + (9.9 * 3)
= 19.5 + 31.2 + 19.5 + 24.2 + 29.7
= 124.1
```

## Translation Cumulative Score

```text
(10.8 * 1) + (14.3 * 3) + (9.6 * 1) + (11.0 * 2) + (13.0 * 3)
= 10.8 + 42.9 + 9.6 + 22.0 + 39.0
= 124.3
```

Interpretation:

- translation is materially lower than respiration on acute burden;
- translation is nearly equal to respiration on cumulative burden;
- this matches the sensitivity test far better than the earlier single-score model.

## First Dual-Metric Result

The dual-metric model produces the clearest current comparison:

| Machine | Acute burden | Cumulative burden |
|---|---:|---:|
| Respiration | `183.5` | `134.5` |
| Translation | `124.1` | `124.3` |

The exact numbers are comparative outputs, not measurements.

The real result is structural:

```text
respiration dominates acute burden
translation approaches respiration much more closely in cumulative burden
```

That is exactly the distinction the sensitivity test said the model needed.

## What the Dual Model Clarifies

The dual model materially improves the ontology in five ways.

## 1. It Separates Collapse Pressure from Decay Pressure

This is the biggest gain.

The ontology can now say clearly:

- respiration is the sharper acute destabiliser;
- translation is the more competitive long-run architecture eroder.

Those are not the same kind of threat.

## 2. It Preserves the Machine Contrast Better

The earlier one-score model risked over-compressing the two machines.

The dual model preserves their different burden styles without denying that both can become cell-owning.

## 3. It Explains the Sensitivity Results More Cleanly

The earlier sensitivity test showed that translation could exceed respiration under amplification-heavy assumptions.

The dual model explains why:

```text
translation is not usually the stronger acute threat,
but it can be a nearly equal or greater cumulative threat
```

That is a much cleaner interpretation.

## 4. It Improves the Machine-to-Cell Bridge

Cell-state transition can now be read more precisely:

- acute failure risk is dominated by high `A_burden`
- chronic decline risk is dominated by high `C_burden`

This is better than treating all cell-state risk as one axis.

## 5. It Creates a Better Basis for Multi-Machine Comparison

Other machines can now be compared on two outputs instead of one.

That will likely be much more informative for:

- repair systems;
- membrane traffic systems;
- cell-cycle systems;
- dormancy and recovery scenarios.

## Best Current Interpretive Categories

The two machines can now be classified more sharply.

## Respiration

Best category:

```text
acute-collapse dominant exporter
```

## Translation

Best category:

```text
cumulative-decay dominant exporter
```

This is a better classification than the earlier single-score language.

## What Still Needs Caution

The dual model is better, but still provisional.

## 1. Coefficients Are Still Analyst-Chosen

The coefficients:

- `1.3`
- `1.1`
- `0.9`
- `0.8`

are currently disciplined choices, not measured constants.

## 2. Other Channel Orderings May Emerge in New Systems

Repair-heavy or signalling-heavy machines may produce different coefficient needs.

The model should stay open to that.

## 3. Acute and Cumulative Burden Are Still Not the Whole Cell Story

The cell still has:

- compensation reserves;
- adaptive remodelling;
- latency states;
- contextual differences in what counts as fatal.

The dual metric improves the bridge, but does not finish it.

## Best Current Result

The best current compressed result is:

```text
Respiration is the stronger acute burden source; translation is the stronger rival in cumulative burden.
```

That is the main gain of this file.

## What This File Now Constrains

This file materially constrains:

1. the distinction between acute and cumulative machine burden;
2. the interpretation of the sensitivity test;
3. the comparative position of respiration and translation;
4. the next refinement of the machine-to-cell bridge;
5. the form future multi-machine comparisons should probably take.

## Immediate Follow-On

The best next file is:

```text
ams-dual-metric-cell-state-thresholds-v1.md
```

Reason:

The dual metrics now exist. The next step is to define how:

- high acute burden;
- high cumulative burden;
- or both together

map into:

- coherent state;
- stress compensation;
- failure trajectory.

That is the clearest next control point.

## Compact Grammar

The best compression is:

```text
Respiration pushes the cell toward collapse faster; translation can age the cell into failure almost as hard.
```

## Provisional Conclusion

The burden model is materially better than before.

AMS dual-metric summary:

```text
The machine-export model should now be treated as dual rather than singular: respiration is the dominant acute burden exporter, while translation becomes much more competitive as a cumulative burden exporter once architecture decay, coordination strain, and amplification are treated explicitly rather than collapsed into one score.
```

Score:

```text
acute vs cumulative burden dual metric: 9.3/10
```
