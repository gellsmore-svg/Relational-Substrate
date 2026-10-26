# External review 008A — ChatGPT review of v0.8A

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.8a-context-repair` at `b7b5d848d90b7d1824bcce9740c2faf966cbea54`.

The review is external to the v0.8A implementation. It is not a line-by-line audit of every durable item. Generation 8 and Generation 8A remain historical evidence. This review does not rewrite their plans, reports, journey records, execution provenance, or published tables. Generation 8A repaired the context-execution basis. This review does not invalidate that repair. It identifies the statistics that still need calibration.

## What was inspected

The external review inspected:

- branch chronology;
- Round A0 frozen-plan ancestry;
- the rule-aware symmetry implementation;
- raw-context execution;
- trajectory and replay execution;
- the Round A0 report and the synthesis;
- the mutual-information implementation;
- the current-context event counters;
- CI history;
- final-head CI.

## Operational conclusions

The micro-batch trajectory platform remained accepted. Round A0 executed the raw-context repair palette.

```text
6,144 primary trajectories
6,759 durable items
58 batches
2 workers
615 / 615 durable replay checks exact
5,314,418 full events
3,145,728 pair events
3,145,728 transition markers
0 timeouts
0 retries
0 quarantines
all 6,144 episodes reached pair_horizon
disk after merge 678,150,248 bytes (~678 MB)
```

Batch wall, median at index `n // 2` and p90 at nearest-rank index `min(n - 1, ceil(0.9 n) - 1)`:

```text
median 17.716329 s
p90    18.062894 s
max    19.428333 s
```

A0 frozen plan:

```text
61ed53075238284850e792aff5743f0a8a7b6695
```

A0 atlas result:

```text
4897d9e02b2942670bafc52bc966ef6709167b64
```

The result descends from the frozen plan. Journey step 2 records that ancestry. Journey step 1 still has a null result commit and was not rewritten.

Final-head GitHub Actions run:

```text
38312376920
```

on:

```text
b7b5d848d90b7d1824bcce9740c2faf966cbea54
```

The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38312376920`. Jobs `constraint-lab` and `books` both completed.

Earlier CI failures were caused by a shallow checkout. `merge-base` could not see Generation 8 plan commits, so `test_generation8_frozen_plans_are_ancestors_of_their_results` raised `ChronologyError`. Runs `38308019051` on `439d5545560b62e7e8d4eeea86683c38c3ef0f9a` and `38311458058` on `6a8060b0a336a9a140eee9816c0db68cf72fefd2` failed that way. Job `books` succeeded on both. Commit `bf821c771e4ed86e24688ed44ab6035b7e9af785` set `fetch-depth: 0` on the constraint-lab checkout. After that, Actions run `38311563660` succeeded on that commit, and the constraint-lab job reported 167 passed. The final-head run above is a later success on the close-out commit.

## Context repair succeeded

Generation 8A executed all 16 raw triad configurations for each source graph and system. It did not quotient them before execution.

```text
3 source graph classes
× 16 raw triad configurations
= 48 starts per system
```

Rule-aware symmetry was calculated after every start was defined. The analysis group is `Aut(source graph, constraint system)`, which preserves the labelled source pair graph and the labelled constraint multiset. It is not merely `Aut(source graph)`.

On the A0 palette, 86 old graph-only orbits split once a labelled rule is required to stay invariant. That formal correction stands. The engine, RNG, event logging, replay, and constraint semantics were not the flaw Generation 8A repaired, and this review does not reopen them.

## Robust observations that survive

The finite-grade edge-count axis survived exhaustive context starts. Round A0 dense minus sparse:

```text
R05 composite suppress              +0.2378
R03 unconditional dissolve suppress +0.1728
R01 conditional dissolve suppress   +0.0723
R04 off-edge conditional suppress   +0.0691
R00 baseline                        +0.0033
R02 conditional form suppress       -0.0711
R06 conditional dissolve favour     -0.0854
R07 unconditional dissolve favour   -0.1448
```

The 3-edge layer stayed near 0.314, except the composite at 0.3072.

Visible first-route structure remained: path splits between star and triangle; star and triangle route mostly through path.

The composite retained a non-zero residual on the 11-class occupancy vector, L1 0.0640. The same residual on the one-dimensional dense-minus-sparse coordinate was about −0.0008. These observations are not the object of the Generation 8B correction.

## Information values that require calibration

Generation 8A reported ordinary plug-in mutual information and conditional mutual information from finite contingency tables. The implementation matches the empirical table. It has no finite-sample bias correction, no permutation-null calibration, and no exact-kernel replacement.

The model supplies exact negative controls. R00 has no rule. R03 is `dissolve(0-1) => strong_suppress`. R07 is `dissolve(0-1) => strong_favour`. The review concludes that these pair-event rules do not read the triad, so the exact quantities

```text
I(initial triad ; first other 3-edge destination)
I(initial triad ; pair state or class at any pair-event checkpoint)
I(current triad ; next pair slot | full pair mask)
```

must be zero for R00, R03, and R07, under a uniform raw initial-triad prior and under any state weighting that does not alter the transition law. Generation 8B must prove that from the implemented transition semantics and must stop if the kernel result is not numerical zero.

Generation 8A's baseline first-destination plug-in values were about 0.031, 0.032, and 0.043 nats by source. With 16 context categories, 2 destination categories, and 256 episodes, the leading independence-bias scale is `((16 - 1) * (2 - 1)) / (2 * 256) ≈ 0.0293` nats. That scale is already close to the observed baseline. It is a sanity check, not the correction.

The largest A0 uniform-raw first-destination plug-in value was R03 star, about 0.0702 nats. R03 is an unconditional rule. If the exact value is zero, 0.0702 nats is a finite-sample tail of an exact-null system, not evidence of an initial-triad routing effect.

The plug-in checkpoint pair-class information stayed near 0.12–0.14 nats through pair event 512. For R00, R03, and R07 the exact value must be zero at every checkpoint. Persistence of the plug-in number is not, by itself, persistence of information.

Current-context plug-in `I(current triad ; next pair slot | full pair mask)` was about 0.018–0.019 nats on baseline and the unconditional rules, and about 0.030–0.036 nats on rules that name a triad. The exact baseline and unconditional values must be zero. The excess on triad-conditioned rules may be genuine. It is not to be recovered by subtracting 0.018 from the plug-in. Generation 8B must use the exact transition law.

## What this review does not do

It does not rerun trajectories. It does not edit Generation 8A sentences in place. It does not select a scientific outcome for the calibration. Pass and fail in this record refer to replay, verification, and CI.
