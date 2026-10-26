# Generation 007B work-count freeze

Frozen before the representability census. Counts come from `build_problems` on `experiments/specs/generation-007b.json`, not from prose. `tests/test_v07b.py` checks the primary row.

The census does not start until this file exists and `generation007b benchmark` has measured the two-level item. Batch size is chosen from that measurement. Generation 7's 142-item multiplier batch is not reused.

## Primary census

```text
logical calibration problems          42
unique two-level control structures    4
unique target singleton expressions   20
coarse-grid points per structure      81
initial atomic items                 344
```

`344 = 4 × 81 + 20`. The coarse axis is `1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000, 10000`. Zero-boundary points are not in this initial count. They are requested only when a basin's best stored point sits on a positive-domain edge.

The 42 problems share 4 control structures. A `(structure, m_off, m_on, rho, alphabet)` evaluation is stored once and reused. Named grades change `Delta_T`, so the 42 residual problems stay distinct.

## Adaptive cap

```text
maximum adaptive points per logical calibration    250
```

The cap counts points first requested by that calibration. A point already stored for the same structure is free. One scheduler step requests at most 9 new points. If the next stencil does not fit in the remaining cap, the step requests none of it and the calibration becomes `unresolved_at_cap`. Coarse-grid points do not count as adaptive.

```text
worst-case adaptive items, primary       42 × 250 = 10500
worst-case primary items, including grid          10844
```

The expected adaptive count is not known until the preflight. The planning range, if one or two basins converge, is about 20–80 new points per problem. That range is not a cap and not a measurement.

## Preflight

Representability and cost only. No composition and no `M_I` or `M_G`.

```text
logical preflight problems            15
unique structures in the preflight     4
unique preflight target expressions    8
initial preflight atomic items       332
```

`332 = 4 × 81 + 8`. The preflight uses its own root, `constraint-lab/generated/generation-007b-preflight/`. Items are not copied from the census root. Because all 4 structures are included, the preflight coarse grid is the census coarse grid.

The 15 problems are every live face at polarity `absent` for `prohibit/prohibit`, `strong_suppress/strong_suppress`, `strong_favour/strong_favour`, and `strong_suppress/strong_favour`, plus every live face at polarity `present` for `prohibit/prohibit`.

Preflight adaptive worst case is `15 × 250 = 3750` points, plus the 332 initial items.

## Robustness, after the primary census is terminal

Six represented primary problems, at `rho3 = 1/2` and `rho3 = 2`, in two modes: held parameters, and a separate recalibration. Alphabet sensitivity is not scheduled.

```text
robustness problems                         6
unique structures among those problems      3
unique target expressions                   5
recalibration logical problems        6 × 2 = 12
recalibration coarse pair points      3 × 2 × 81 = 486
recalibration target singletons       5 × 2 = 10
recalibration adaptive cap           12 × 250 = 3000
```

Held probes add one pair point, one target singleton, one target composition, and one control composition at each new rho for each represented robustness problem. Unrepresented and `unresolved_at_cap` primaries do not schedule composition or robustness.

## Measured batch

Measured on this machine on 2026-10-12. Nine two-level pair-point solves, three repeats of three multiplier pairs, numeric threads pinned to 1. The same samples are the target-singleton policy. Composition items stay at one per batch until they are timed on their own. The count is `floor(45 / p90)`, and this measurement did not need a further reduction.

```text
pair_point p50     0.290 s
pair_point p90     0.315 s
pair_point max     0.315 s
items per batch    142
```

`142 × 0.315 s ≈ 45 s` of kernel time. The watchdog remains 120 seconds.

The two-level numerical reference on the same run has maximum absolute passage-gap `0` against the scalar pair-face at `(m_off, m_on) = (1, m)` and against condition erasure at `(m, m)`. That is below `1e-10`. The singleton tolerance stays `1e-8`.

## Disk and wall clock

Generation 7 item files were about 110 KB because each one stores length-1024 committor vectors. A 007B pair point does the same. The worst-case primary grid, the adaptive caps, composition for a small solution family, and the robustness caps are on the order of 15,000 item files, or about 1.7 GB, if every cap is reached.

Kernel-time sketch at the measured p90 and two workers, excluding process start and the atomic write:

```text
census coarse grid, 344 items                 about 1 minute
census adaptive, 20–80 points × 42            about 2–9 minutes
census adaptive, cap on every problem         about 28 minutes
preflight coarse grid, 332 items              about 1 minute
preflight adaptive cap, 15 × 250              about 10 minutes
```

The 20–80 point range is still a planning range. The preflight replaces it with a measured adaptive count before the census is interpreted. Composition and robustness are scheduled only after the primary calibrations are terminal, so their wall clock is added after that, not hidden inside the coarse grid.
