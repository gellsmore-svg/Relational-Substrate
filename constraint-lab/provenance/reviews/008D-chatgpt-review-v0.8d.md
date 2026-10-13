# External review 008D — ChatGPT review of v0.8D

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.8d-two-gate-composition` at `50e3f4dfeac19d8e075964c51560d4d3f08b85c8`.

The review is external to the v0.8D implementation. It is not a line-by-line audit of every table cell. Generations 1 through 8D remain historical evidence. This review does not rewrite their plans, reports, journey records, execution provenance, or published tables.

## What was inspected

The external review inspected:

- branch chronology;
- the Grok-to-Opus continuation record;
- the frozen D0 plan;
- the post-freeze validator correction;
- the structural census;
- the weighted census;
- the truth tables;
- reducibility;
- the information atlas;
- the ablations;
- the 8C errata;
- the coherence ledger and snapshot;
- final-head CI.

## Provenance and execution

The branch is 14 commits ahead of the v0.8C head `41ec34e72191f93647f28838f16296fa2c2880a3`.

Final head:

```text
50e3f4dfeac19d8e075964c51560d4d3f08b85c8
```

Final-head GitHub Actions run:

```text
38392825068
```

successful, on that head. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38392825068`.

Frozen D0 analysis plan:

```text
ac037f32df81271e04381c79efebf6f5b3d0b607
```

Plan hash:

```text
10a3114bcf7a1a914e9eff19e08f77a9fbcf71852bc4a22f14f04d723912ce07
```

Pre-result journey head `d3bf0f79b65f3d85e9a95e681b875c0f45b3a966`, with Actions run `38375394924` successful before execution.

D0 tables and result commit:

```text
093e460e9992e3ddc4fd24cdb43d6d5397de4e29
```

Report commit:

```text
7dc388352b30b87ced08abd67cead0dffa37dd82
```

Coherence snapshot commit:

```text
36cb89cbf1125cd5837afd9f02722671007c6832
```

Final close-out:

```text
50e3f4dfeac19d8e075964c51560d4d3f08b85c8
```

The snapshot-head suite reported 227 passed.

## Continuation

The execution record states that Grok 4.7 performed the implementation and the D0 work through the numerical tables commit `093e460e9992e3ddc4fd24cdb43d6d5397de4e29`, and that Claude Opus 5.5 continued from that exact repository commit to perform the interpretation, the report, the coherence update and the close-out. The second-session copy of the prompt was not byte-compared with the stored agent input.

```text
repository-state continuity:      established
second-session prompt byte identity: not established
```

The review does not claim more provenance certainty than that.

## D0 operational result

D0 used:

- 96 labelled one-gate `T->P` rules;
- 4,560 unordered labelled rule pairs;
- 236 S4 structural orbits;
- 3,584 W4 weighted canonical systems;
- 237 deterministic execution items;
- 3,670,016 full-state evaluations;
- 3,670,016 kernel-agreement evaluations;
- 86,016 S4 law images.

Execution used one worker. It ran no stochastic trajectories, no parameter fit and no new controls. The largest item wall was about 5.583 seconds, and the 120-second watchdog was not approached. Verify returned complete, and validation was ok.

## Post-freeze validator correction

Commit `cbfdae8a5ffb4118abcacc33a8285894f76435bf` lies after the plan freeze and before table publication, and it changes validation logic only. It fixes two false requirements:

1. Form and dissolve on the same pair slot with the same gate literal are distinct structural rules.
2. Two rules whose gate literals are mutually exclusive have no realised both-active state, so they must not be required to satisfy a both-active denominator check.

It did not change the frozen estimands, the analysis functions, the canonical census, the stored item contents, or the scientific work count. All item files predate it. The execution record reports that re-assembly with the published code reproduces the summary byte for byte, and that selected item re-executions reproduce the stored results, wall time excluded. The review treats the frozen D0 plan as intact.

## Core composition result

For the declared two-rule, one-condition-per-rule subgrammar:

```text
q(e | x) ∝ exp[ λ1 φ1(x,e) + λ2 φ2(x,e) ],    λi = ln(mi)
```

Each `φi` is one exactly where the action is admissible and one triad literal is true. Across all 3,584 systems the implementation/kernel weight gap is 0 and the log-weight residual is at most about `2.22e-16`. Primitive features add in event-logit space, and softmax normalisation couples the slot probabilities through the denominator.

## Exact collapses preserved

- **Complementary-gate elimination:** `A | G => m` with `A | NOT G => m` is exactly `A => m`. All 16 equal-weight complementary systems reproduce the unconditional full-event kernel.
- **Direction elimination:** equal-weight `form(A) | G => m` with `dissolve(A) | G => m` removes the action edge's state from the local law.
- **Reciprocal literal-flip twins:** different rule texts can give the same affine logit, and therefore the same labelled or S4-conjugate kernel. Syntactic complexity is not dynamical complexity.

## Effective gate dimension

16 systems have effective gate dimension 0, 960 have dimension 1, and 2,608 have dimension 2. Reducibility: R0 0, R1U 16, R1G 0, R1T 48, R2S 912, R2G 2608. Of the dimension-two systems, 256 are switched systems that never activate both rules at once: the pair mask selects which gate is read. Two effective gate bits do not necessarily mean simultaneous conjunction.

## Information is not dimension

Balanced current-triad slot information spans 0.0018455 to 0.0593653 nats at dimension 1 and 0.0050591 to 0.0478183 nats at dimension 2. The largest value is at dimension 1. In 64 systems the two-rule information is below the larger one-rule constituent. Information magnitude does not rank effective dimension, reducibility, coordinate count or structural significance.

## Scope of the no-gate-product result

Generation 8D correctly showed that two primitive one-condition rules on one action cannot create an independent gate×gate coefficient: `L(G1,G2) = c + λ1 l1(G1) + λ2 l2(G2)` and `L11 − L10 − L01 + L00 = 0`.

The report sometimes broadens this into statements that two conditions cannot be related without meta-constraints, or that `L > 0` is the first grammar that could create a gate×gate coefficient. That broader claim is not established. The ordinary `Constraint` representation already supports several conjunctive conditions in one rule. For the order-3 independent hypergraph, `Constraint.k() = 1 + len(conditions) + len(counts)`, and the parser accepts conditions joined by `&`. A legal ordinary rule can therefore have `K = 3` with two triad conditions, for example `dissolve(0-1) | present(0-1-2) & present(0-1-3) => strong_favour`, and no meta-constraint is involved.

The review asks for a scope erratum and a coherence qualification. It also identifies the next unexplored level of the existing grammar: one rule reading two triad literals conjunctively.

The review does not select an E0 result.
