# External review 008B — ChatGPT review of v0.8B

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.8b-information-calibration` at `66fc7f48ac776aec461553cfac06126ed6566626`.

The review is external to the v0.8B implementation. It is not a line-by-line audit of every table cell. Generation 8, Generation 8A, and Generation 8B remain historical evidence. This review does not rewrite their plans, reports, journey records, execution provenance, or published tables.

## What was inspected

The external review inspected:

- branch chronology;
- the frozen B0 analysis plan;
- the information-calibration report;
- the exact-kernel results;
- the permutation calibration;
- the structural zero-information controls;
- the numerical validation;
- the current-context weighting comparisons;
- commit `7eb63924c4c5484decd1ab5b7bee3a25b440ac68`;
- final-head CI.

## Provenance and execution

The branch is 11 commits ahead of the v0.8A head `b7b5d848d90b7d1824bcce9740c2faf966cbea54`.

Final head:

```text
66fc7f48ac776aec461553cfac06126ed6566626
```

Final-head GitHub Actions run:

```text
38326986030
```

successful, on that head. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38326986030`.

Frozen B0 analysis plan:

```text
466d54339738d315ed621ea4256a239cb026498a
```

Plan hash:

```text
279857bb2ee82eefd430ba56c9fa3758238ebea9e0b652c01b56b97dbc1bf618
```

B0 numerical result and tables commit:

```text
dc9f9b9eb6e4a36b4513d10b49e937c43b57b371
```

The result descends from the frozen plan. No new scientific trajectories were run.

B0 used 40 bounded analysis items:

```text
exact
permute-initial
permute-current
```

with two workers and a 120-second watchdog.

Approximate item wall:

```text
exact:              ~3.8 s
initial permutation: 30–32 s
current permutation: 14–16 s
```

Verification completed. The report-head constraint-lab suite reported 182 passed.

## Validation correction after the frozen plan

The first R03 exact command stopped because the implementation required an empirical

```text
I(current triad ; next slot | graph isomorphism class)
```

quantity to be zero on an unconditional pair rule. That identity is not guaranteed. A finite empirical sample can correlate the triad state with which labelled pair mask inside the same graph class was visited, while the local slot law varies across those labelled masks.

Commit `7eb63924c4c5484decd1ab5b7bee3a25b440ac68` corrected only the validation assertion. The structural zero identity remains

```text
I(current triad ; next pair slot | full labelled pair mask) = 0
```

for R00, R03, and R07. The frozen estimands did not change. This is a legitimate correction to a validation assumption, not a post-hoc change of scientific target.

## Plug-in bias

The Generation 8A plug-in mutual-information cells reproduce: 336 cells, maximum absolute reproduction gap `2.810e-16`.

For first destination, the permutation-null mean is approximately `0.03024–0.03127` nats. The Generation 8A values lived on that scale.

The largest plug-in cell, R03 star at `0.07021` nats, is a structural-zero system. Its exact-kernel first-destination information is below `1e-10`. The large-looking plug-in value was finite-sample estimator behaviour, not triad-dependent routing.

## Exact first destination

For R00, R03, and R07, exact first-destination mutual information is at the numerical floor. For every path source, exact first-destination mutual information is also at the floor, including the triad-conditioned systems.

For star and triangle the triad-conditioned systems have genuine but extremely small values:

```text
R01  5.699e-7 nats
R02  3.307e-7
R04  3.307e-7
R05  2.025e-5
R06  1.906e-7
```

The star and triangle values agree to numerical precision. The initial hidden triad has almost no effect on eventual first routing among the other 3-edge organisations in this grammar.

## Checkpoint memory

The persistent Generation 8A plug-in signal of about `0.12–0.14` nats through pair epoch 512 was estimator bias. Exact initial-context graph-class information is transient.

The largest exact value is R06 path at checkpoint 1, `0.02798` nats. By checkpoint 32 the largest exact class mutual information is about `1.29e-9` nats. By checkpoint 64 every exact class mutual information is below the `1e-10` floor. The labelled pair-mask information decays on the same schedule.

The visible pair process forgets the initial triadic context on this timescale. The old figure near `0.12` is not persistent information.

## Edge count versus shape

At checkpoint 1, for star and triangle, exact graph-class information equals exact edge-count information. Shape given edge count contributes 0 at that first pair event.

For path:

```text
R06:
I(T0; class)              = 0.02798
I(T0; edge count)         = 0.008801
I(T0; class | edge count) = 0.01918

R01:
I(T0; class)              = 0.01023
I(T0; edge count)         = 0.001393
I(T0; class | edge count) = 0.008838
```

This edge-count versus shape split is one of the primary mechanism questions left for Generation 8C.

## Exact finite-horizon occupancy

The Generation 8A raw-context occupancy spans of about `0.06–0.09` were mostly sampling variation. Exact 512-pair-epoch dense-minus-sparse context ranges:

```text
R00/R03/R07: numerical floor

R01: 0.001423
R02: 0.000395
R04: 0.000395
R05: 0.000347
R06: 0.001925
```

These are genuine finite-horizon path-integrated context effects. They are small compared with the grade-driven occupancy shifts of order `10^-1`.

## Genuine local current-context dependence

The exact local estimand is

```text
I(current triad ; next pair slot | full labelled pair mask)
```

where the six pair propensities are renormalised conditional on the next full event being a pair event.

R00, R03, and R07 are at the numerical floor under balanced-law, stationary pair-event, and A0 empirical-source weightings. The triad-conditioned systems are genuinely non-zero.

Balanced-law weighting:

```text
R01  0.009749
R02  0.009749
R04  0.009749
R05  0.010413
R06  0.023368
```

Stationary pair-event weighting:

```text
R01  0.012025
R02  0.012025
R04  0.012025
R05  0.013240
R06  0.016895
```

A0 empirical-source exact-law values lie close to the stationary values. This is the main genuine higher-order signal left for a mechanism reading.

## Projection

Under stationary pair-event weighting, exact next-slot conditional mutual information retained after replacing the full labelled pair mask with graph isomorphism class:

```text
R01  0.661 of the full-mask value
R02  0.661
R04  0.661
R05  0.710
R06  0.443
```

The remaining fraction is lost labelled alignment. Information in the next graph class given the current graph class is smaller still, about `0.001–0.0026` nats for the conditioned systems.

## What this review does not do

It does not rerun trajectories. It does not edit Generation 8, 8A, or 8B sentences in place. It does not select a mechanism. Pass and fail in this record refer to verification and CI. The scientific content that survives is the separation between a small exact local dependence, where a rule reads the triad, and the absence of a long-lived initial-context footprint in this grammar.
