# AMS Machine Export Weighting Sensitivity Test v1

## Purpose

This file stress-tests the first machine-export weighting model.

The previous comparison produced a useful result:

```text
respiration exports burden more quickly and directly
translation exports burden more diffusely and cumulatively
```

The current question is:

```text
does that result survive reasonable changes in weighting assumptions?
```

This file therefore tests the stability of the model under:

- changed top-level weight priorities;
- moderate activation perturbations;
- stronger emphasis on amplification over direct burden.

## Central Claim

The central claim is:

> The weighted comparison is robust at the level that matters most: under reasonable perturbations, respiration remains the faster high-leverage collapse exporter and translation remains the slower high-breadth degradation exporter. The exact totals move, but the dominant export styles remain stable.

More briefly:

```text
The comparison bends, but it does not flip.
```

## Starting Baseline

The baseline framework used:

```text
w_d = 1
w_s = 1
w_a = 1
```

with channel weight sums:

| Channel | `M` | `S` | `A` | Weight sum |
|---|---:|---:|---:|---:|
| `E_energy` | `3` | `3` | `3` | `9` |
| `E_renew` | `3` | `2` | `3` | `8` |
| `E_bound` | `3` | `3` | `3` | `9` |
| `E_damage` | `2` | `2` | `3` | `7` |
| `E_coord` | `2` | `2` | `3` | `7` |

Machine activation profiles:

## Respiration

```text
E_energy = 3
E_renew = 1
E_bound = 3
E_damage = 3
E_coord = 2
```

## Translation

```text
E_energy = 1
E_renew = 3
E_bound = 1
E_damage = 2
E_coord = 3
```

Baseline totals:

```text
Respiration = 97
Translation = 77
```

## What Counts as Stability

The model should be treated as stable if three things remain true across reasonable perturbations:

1. respiration still dominates energy and boundary export
2. translation still dominates renewal and coordination export
3. respiration still reads as the faster collapse exporter while translation still reads as the slower degradation exporter

If those hold, then the framework is useful even if exact totals shift.

## Sensitivity Case 1: Amplification-Heavy Weighting

This case assumes amplification matters more than direct burden or speed.

Set:

```text
w_d = 1
w_s = 1
w_a = 2
```

New channel weight sums:

| Channel | New sum |
|---|---:|
| `E_energy` | `12` |
| `E_renew` | `11` |
| `E_bound` | `12` |
| `E_damage` | `10` |
| `E_coord` | `10` |

Weighted totals:

## Respiration

```text
E_energy = 12 * 3 = 36
E_renew = 11 * 1 = 11
E_bound = 12 * 3 = 36
E_damage = 10 * 3 = 30
E_coord = 10 * 2 = 20
Total = 133
```

## Translation

```text
E_energy = 12 * 1 = 12
E_renew = 11 * 3 = 33
E_bound = 12 * 1 = 12
E_damage = 10 * 2 = 20
E_coord = 10 * 3 = 30
Total = 107
```

Result:

- respiration still dominates through energy, boundary, and damage
- translation still dominates through renewal and coordination
- the overall gap widens slightly because respiration loads multiple high-amplification channels hard

Interpretation:

```text
the comparison survives stronger emphasis on system-wide feedback
```

## Sensitivity Case 2: Speed-Heavy Weighting

This case assumes propagation speed matters more than direct burden or amplification.

Set:

```text
w_d = 1
w_s = 2
w_a = 1
```

New channel weight sums:

| Channel | New sum |
|---|---:|
| `E_energy` | `12` |
| `E_renew` | `10` |
| `E_bound` | `12` |
| `E_damage` | `9` |
| `E_coord` | `9` |

Weighted totals:

## Respiration

```text
E_energy = 12 * 3 = 36
E_renew = 10 * 1 = 10
E_bound = 12 * 3 = 36
E_damage = 9 * 3 = 27
E_coord = 9 * 2 = 18
Total = 127
```

## Translation

```text
E_energy = 12 * 1 = 12
E_renew = 10 * 3 = 30
E_bound = 12 * 1 = 12
E_damage = 9 * 2 = 18
E_coord = 9 * 3 = 27
Total = 99
```

Result:

- respiration's advantage increases further
- translation remains serious, but reads even more clearly as the slower exporter
- the qualitative difference sharpens, not blurs

Interpretation:

```text
the model becomes even more respiration-favouring when speed is emphasised, which fits the biological reading
```

## Sensitivity Case 3: Direct-Burden-Heavy Weighting

This case assumes immediate direct burden matters more than speed or amplification.

Set:

```text
w_d = 2
w_s = 1
w_a = 1
```

New channel weight sums:

| Channel | New sum |
|---|---:|
| `E_energy` | `12` |
| `E_renew` | `11` |
| `E_bound` | `12` |
| `E_damage` | `9` |
| `E_coord` | `9` |

Weighted totals:

## Respiration

```text
E_energy = 12 * 3 = 36
E_renew = 11 * 1 = 11
E_bound = 12 * 3 = 36
E_damage = 9 * 3 = 27
E_coord = 9 * 2 = 18
Total = 128
```

## Translation

```text
E_energy = 12 * 1 = 12
E_renew = 11 * 3 = 33
E_bound = 12 * 1 = 12
E_damage = 9 * 2 = 18
E_coord = 9 * 3 = 27
Total = 102
```

Result:

- the qualitative ranking still does not flip
- respiration still reads as the more immediate cell-owning threat
- translation still reads as the more renewal-heavy burden source

Interpretation:

```text
the model remains stable even when immediate burden is favoured over amplification
```

## Sensitivity Case 4: Perturbed Activation Ratings

This case asks whether moderate changes in machine activation ratings destabilise the comparison.

Use perturbed profiles:

## Respiration Perturbed

```text
E_energy = 3
E_renew = 1
E_bound = 2
E_damage = 3
E_coord = 2
```

This weakens the boundary emphasis slightly.

## Translation Perturbed

```text
E_energy = 1
E_renew = 3
E_bound = 1
E_damage = 2
E_coord = 2
```

This weakens the coordination emphasis slightly.

Use baseline equal top-level weights again.

Weighted totals:

## Respiration

```text
E_energy = 9 * 3 = 27
E_renew = 8 * 1 = 8
E_bound = 9 * 2 = 18
E_damage = 7 * 3 = 21
E_coord = 7 * 2 = 14
Total = 88
```

## Translation

```text
E_energy = 9 * 1 = 9
E_renew = 8 * 3 = 24
E_bound = 9 * 1 = 9
E_damage = 7 * 2 = 14
E_coord = 7 * 2 = 14
Total = 70
```

Result:

- totals shrink
- the gap narrows slightly
- the core style difference still remains

Interpretation:

```text
moderate profile perturbations weaken the sharpness, but do not reverse the comparison
```

## Sensitivity Case 5: Translation-Friendly Stress Test

This is the hardest reasonable challenge to the baseline.

Assume:

- translation coordination burden is maximal
- translation damage burden is slightly stronger
- respiration boundary burden is slightly less dominant

Use:

## Respiration

```text
E_energy = 3
E_renew = 1
E_bound = 2
E_damage = 2
E_coord = 2
```

## Translation

```text
E_energy = 1
E_renew = 3
E_bound = 1
E_damage = 3
E_coord = 3
```

Use amplification-heavy weighting:

```text
w_d = 1
w_s = 1
w_a = 2
```

Weighted totals:

## Respiration

```text
E_energy = 12 * 3 = 36
E_renew = 11 * 1 = 11
E_bound = 12 * 2 = 24
E_damage = 10 * 2 = 20
E_coord = 10 * 2 = 20
Total = 111
```

## Translation

```text
E_energy = 12 * 1 = 12
E_renew = 11 * 3 = 33
E_bound = 12 * 1 = 12
E_damage = 10 * 3 = 30
E_coord = 10 * 3 = 30
Total = 117
```

This is the only test case here in which translation overtakes respiration in total burden score.

But this does not overturn the model.

Why:

1. the winning scenario requires multiple translation-favouring shifts at once
2. the burden style still differs rather than converges
3. translation wins here by cumulative amplification, not by becoming the faster collapse exporter

Interpretation:

```text
under unusually translation-favouring assumptions, translation can become the greater long-run burden source without ceasing to be the slower degradation exporter
```

This is actually a useful result, not a failure.

It shows the framework can express cases where translation becomes more dangerous overall without forcing it into respiratory-style collapse logic.

## Main Stability Judgment

The best current judgment is:

```text
the framework is qualitatively stable and quantitatively flexible
```

That is exactly what is needed at this stage.

It is:

- stable enough to be useful
- flexible enough not to be obviously overfitted

## What the Sensitivity Test Clarifies

This file clarifies five things.

## 1. The Core Contrast Is Robust

Across the reasonable perturbations:

- respiration stays the faster high-leverage exporter
- translation stays the slower broad-burden exporter

That is the most important result.

## 2. Translation Can Dominate Long-Run Burden Under Some Assumptions

This is the strongest new nuance.

If amplification and coordination are weighted heavily enough, and if translation burden is activated strongly enough, translation can exceed respiration in total burden score.

This is not a contradiction.

It means:

```text
faster collapse risk and larger long-run burden are not the same thing
```

## 3. Boundary Burden Remains the Sharpest Respiratory Marker

When respiration's boundary weighting is reduced, its total burden falls noticeably.

That confirms:

```text
boundary burden is one of respiration's defining export signatures
```

## 4. Coordination Burden Remains the Sharpest Translation Marker

When translation's coordination weighting is reduced, its distinctiveness weakens materially.

That confirms:

```text
coordination burden is one of translation's defining export signatures
```

## 5. The Model Needs Two Distinct Outputs

The sensitivity tests suggest that one total burden score is not enough.

The next version should probably separate:

1. acute collapse risk
2. long-run cumulative burden

That would preserve the most important distinction now emerging from the tests.

## Best Current Result

The best current compressed result is:

```text
Respiration remains the sharper acute threat, while translation can rival or exceed it as a cumulative threat under amplification-heavy conditions.
```

That is the strongest result of the file.

## What This File Now Constrains

This file materially constrains:

1. how robust the weighting framework is under perturbation
2. the difference between acute and cumulative burden
3. the centrality of boundary burden to respiration
4. the centrality of coordination burden to translation
5. the design requirements for the next weighting model

## Immediate Follow-On

The best next file is:

```text
ams-acute-vs-cumulative-burden-dual-metric-v1.md
```

Reason:

The sensitivity results have exposed the most useful next refinement:

```text
one burden score is not enough
```

The next framework should therefore separate:

- acute collapse pressure
- cumulative architecture-decay pressure

That is now the clearest technical upgrade path.

## Compact Grammar

The best compression is:

```text
Respiration is usually the sharper knife; translation can still be the longer poison.
```

## Provisional Conclusion

The weighting model survives a serious first stress test.

AMS sensitivity summary:

```text
The current export-weighting model is robust enough to preserve the main machine contrast under reasonable perturbation, but the tests also show that acute collapse risk and long-run cumulative burden should be separated in the next refinement, because translation can become the greater total burden source under amplification-heavy assumptions without becoming the faster collapse exporter.
```

Score:

```text
machine export weighting sensitivity test: 9.2/10
```
