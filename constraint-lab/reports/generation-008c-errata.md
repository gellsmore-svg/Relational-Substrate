# Generation 008C errata

This file corrects one exact-ratio sentence in the Generation 8C report. It does not replace that report. The historical report, its tables, and the historical coherence statement stay in place.

## Jensen–Shannon ratio

`constraint-lab/reports/generation-008c-mechanistic-decomposition.md` says that the favour/suppress total-variation ratio is `7/3` and that the same ratio appears in the Jensen–Shannon terms and in the balanced conditional mutual information.

The total-variation ratio is exact:

```text
(5/18) / (5/42) = 7/3
```

The one-gate edge-drift magnitude ratio is the same exact value:

```text
(5/72) / (5/168) = 7/3
```

The balanced-information ratio is not `7/3`. The verified closed forms divide as:

```text
0.023368444772049440 / 0.009748566529643857 = 2.397115996591876
```

Jensen–Shannon divergence is nonlinear in the slot probabilities. Equal total variation does not fix the divergence. Reciprocal multipliers `m = 4` and `m = 1/4` remain different distances from the uniform six-slot law, and that is why favour carries more local information than suppression. The information ratio is a separate number from the probability-displacement ratio and from the drift ratio.

`F8C-GRADE-ASYMMETRY` states the incorrect information-ratio clause. That statement is not rewritten. `F8D-CORRECT-GRADE-ASYMMETRY` records the distinction and is linked by `corrects`. The older node is marked `qualified`.

## Drift magnitude is not inherited

`F8C-DRIFT-DIRECTION` was stored with `magnitude_class = large` because the inference points at the Generation 8 occupancy axis. The inference itself is a local sign. The large magnitude belongs to `F010-OCCUPANCY-AXIS`. `F8D-DRIFT-MAGNITUDE-SCOPE` qualifies the older node. The older statement is not rewritten. Its status is `qualified`.
