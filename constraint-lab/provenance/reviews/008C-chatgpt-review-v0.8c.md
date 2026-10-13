# External review 008C — ChatGPT review of v0.8C

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.8c-mechanism` at `41ec34e72191f93647f28838f16296fa2c2880a3`.

The review is external to the v0.8C implementation. It is not a line-by-line audit of every table cell. Generations 1 through 8C remain historical evidence. This review does not rewrite their plans, reports, journey records, execution provenance, or published tables.

## What was inspected

The external review inspected:

- branch chronology;
- the C0 frozen plan;
- the mechanism report;
- the mechanism tables;
- the local-law implementation;
- the topology atlas;
- the gate-memory analysis;
- the projection analysis;
- the drift analysis;
- the coherence ledger;
- the coherence generator;
- the coherence tests;
- final-head CI.

## Provenance and execution

The branch is 12 commits ahead of the v0.8B head `66fc7f48ac776aec461553cfac06126ed6566626`.

Final head:

```text
41ec34e72191f93647f28838f16296fa2c2880a3
```

Final-head GitHub Actions run:

```text
38356522671
```

successful, on that head. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38356522671`.

Frozen C0 analysis plan:

```text
3e783387cd2c8050559c29bac059beae03555ab7
```

Plan hash:

```text
febde3989a8b2f2461440e708897fe78c1fdac436375c0c628b393309932c897
```

C0 tables commit:

```text
f962000d7c6c750565843426d46bcd3fdbb43026
```

Report commit:

```text
479469f7b56277849f75080f5f8478e875d95ec7
```

Prompt close-out:

```text
41ec34e72191f93647f28838f16296fa2c2880a3
```

The tables commit descends from the frozen plan. The close-out commit is outside the inclusive analysis range that ends at the report commit.

The report-head constraint-lab suite reported 207 passed.

C0 used 60 deterministic mechanism items. It ran 0 new stochastic trajectories, 0 parameter fits, and 0 new controls. The largest item wall was about 1.413 seconds. The 120-second watchdog was not approached. Verification completed.

## Central mechanistic compression

Generation 8C supports this chain, and the review preserves it as the principal explanatory compression:

```text
triad gate state
→ one pair slot reweighted
→ six-slot law changes by normalisation
→ graph topology maps slot identity into edge-count / shape consequences
→ stochastic triad refresh erases the initial gate value
→ the current gate continues to modify the current transition law
→ long-run occupancy reflects persistent rule bias rather than persistent initial-context memory
```

## One-gate closed form

For one conditional pair rule with multiplier `m`, the inactive six-slot law is uniform, `q_0(e) = 1/6`. When the rule is active on one slot:

```text
q_m(action) = m / (m + 5)
q_m(other)  = 1 / (m + 5)
```

Balanced current-context information is `(1/2) JS(q_0, q_m)`.

Verified values:

```text
m = 1/4
I = 0.009748566529643857 nats

m = 4
I = 0.023368444772049440 nats
```

Enumeration gaps are of order `1e-15`. R01, R02, and R04 are locally equivalent under this balanced quantity. R05's additional local information is explained by shared denominator normalisation when two weighted pair slots coexist.

## Path topology

At one pair toggle, the star has one resulting isomorphism class per resulting edge count, and the triangle has one resulting isomorphism class per resulting edge count. The path has multiple resulting isomorphism classes inside edge count 2 and inside edge count 4.

On the canonical path:

```text
dissolve middle edge -> 2-edge matching
dissolve end edge    -> 2-edge path
form short chord     -> triangle + pendant
form long chord      -> 4-cycle
```

R01 and R06 reweight the path's middle edge. That is why path topology converts a one-slot bias into shape information conditional on edge count.

## Initial memory versus current efficacy

Generation 8C shows that `I(initial gate ; current pair mask)` is below `1e-10` by pair epoch 64, while `I(current triad ; next pair slot | current full pair mask)` remains at the one-gate closed-form scale.

Current relational efficacy and persistent memory of the initial relation are different properties.

## Edge-count drift

For the strong grades, one-gate rule-induced balanced edge drift includes:

```text
strong-suppress dissolve: +5/168
strong-suppress form:     -5/168
strong-favour dissolve:   -5/72
```

Unconditional versions double the one-gate balanced mean because the triad gate no longer switches the rule off on half of triad states. The signs agree with the Generation 8 sparse/dense occupancy axis. The stationary average expected edge-count drift is numerical zero. Stationary mass is not inferred from local mean drift.
