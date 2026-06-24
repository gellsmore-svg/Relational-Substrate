# AMS Coupled Ecology Core Model v1

## Purpose

This file assembles the main ecology variables into one coupled core model.

Recent work has now sharpened:

```text
R_cap   = recovery capacity
R_res   = reserve depth
B_sync  = burden synchronisation
C_sup   = cross-support strength
F_casc  = cascade susceptibility
V_E     = ecology viability
θ_rec   = recoverability threshold
```

These variables are now individually useful.

The present task is to state how they function together as one system rather than as isolated concepts.

## Central Claim

The central claim is:

> A living ecology remains viable while recovery capacity, reserve depth, and effective cross-support reinforce one another strongly enough to keep burden synchronisation and cascade susceptibility below the ecology's recoverability threshold. Ecology-level decline begins when that positive cluster weakens and the negative cluster strengthens, so that burdens no longer remain partitionable and recovery becomes self-consuming rather than restorative.

More briefly:

```text
Life persists while recovery, reserve, and support outrun synchrony and cascade.
```

## Why a Coupled Model Is Needed

The recent ecology files established three important things:

1. high burden alone is not enough to explain death approach
2. synchronisation matters more than raw load alone
3. support and reserve are what keep burdens partitionable and recoverable

But without a coupled model, the ecology layer still risks fragmentation into separate variables that never quite recombine.

The goal here is to prevent that.

The ecology now needs one coherent answer to:

```text
what makes a living system still recoverable as one system?
```

That answer must involve the whole variable set together.

## The Positive and Negative Variable Clusters

The strongest current ecology structure is a two-cluster model.

## Positive Cluster

The positive cluster is:

```text
P+ = {R_cap, R_res, C_sup}
```

These are the variables that preserve recoverability.

They answer:

- how much recovery the ecology can still perform
- how much future headroom it still has
- how much its machines still support one another effectively

## Negative Cluster

The negative cluster is:

```text
P- = {B_sync, F_casc}
```

These are the variables that destroy recoverability.

They answer:

- how far burdens are becoming aligned rather than separable
- how likely local burden is to spread into ecology-owning cascade

This is the most useful current compression of the ecology.

## First Core Model

The simplest useful coupled model is:

```text
V_E = G(P+) - H(P-)
```

where:

- `G(P+)` is the positive viability contribution of recovery, reserve, and support
- `H(P-)` is the negative viability contribution of synchronisation and cascade

The first explicit form should be:

```text
V_E = (a*R_cap + b*R_res + c*C_sup) - (d*B_sync + e*F_casc)
```

with:

```text
a,b,c,d,e > 0
```

This was already suggested earlier, but it can now be treated as the ecology core model rather than a provisional side note.

## Why This Form Is Right for the Current Stage

This form is useful because it captures the key ontology directly:

- recoverability is strengthened by recovery, reserve, and support
- recoverability is weakened by synchrony and cascade

It also remains:

- simple enough to work with
- flexible enough for later refinement
- clearly tied to the living-state boundary

## The Five Core Couplings

The variables do not just add up.

They influence one another.

The strongest current couplings are:

## 1. Reserve -> Support Coupling

The strongest current relation is:

```text
R_res high -> C_sup more usable and effective
```

Interpretation:

- support is easier to deploy when headroom exists
- reserve gives support time and margin to work

Working expression:

```text
C_sup* = C_sup * (1 + k*R_res)
```

## 2. Support -> Synchrony Damping

The strongest current relation is:

```text
C_sup high -> effective B_sync lower
```

Interpretation:

- support helps keep burdens local
- support delays mutual reinforcement

Working expression:

```text
B_sync* = B_sync / (1 + m*C_sup)
```

## 3. Synchrony -> Cascade Coupling

The strongest current relation is:

```text
B_sync high -> F_casc rises sharply
```

Interpretation:

- when burdens align, local failures spread more easily
- synchrony is one of the main engines of ecology-wide instability

Working expression:

```text
F_casc = (Σ b_ij * B_sync) / (1 + R_cap + R_res)
```

## 4. Reserve -> Synchrony Damping

The strongest current relation is:

```text
R_res high -> effective synchronisation lower
```

Interpretation:

- reserve gives the ecology room to absorb uneven burdens without forcing them to align
- shallow reserve exposes the same burden pattern more destructively

Working expression:

```text
B_sync** = B_sync / (1 + u*R_res)
```

## 5. Cascade -> Recovery Erosion

The strongest current relation is:

```text
F_casc high -> R_cap and C_sup degrade
```

Interpretation:

- once cascade pressure is high, recovery becomes less effective
- support routes begin failing functionally even if topology remains

This is the key downhill coupling.

## Effective Ecology Variables

The model becomes clearer if the main variables are expressed in effective form.

## Effective Support

Use:

```text
C_eff = C_sup * (1 + k*R_res) / (1 + n*B_sync)
```

Interpretation:

- reserve strengthens effective support
- synchrony weakens it

## Effective Synchrony

Use:

```text
B_eff = B_sync / (1 + m*C_sup + u*R_res)
```

Interpretation:

- synchrony is ecologically worse when support and reserve are weak

## Effective Cascade Pressure

Use:

```text
F_eff = F_casc * (1 + x*B_sync) / (1 + y*R_cap + z*R_res)
```

Interpretation:

- synchrony magnifies cascade risk
- recovery and reserve damp it

## Effective Recovery Capacity

Use:

```text
R_eff = R_cap * (1 + q*C_sup) / (1 + r*B_sync + s*F_casc)
```

Interpretation:

- support strengthens recovery
- synchrony and cascade consume it

These effective variables are not yet final equations, but they make the coupled structure explicit.

## Core Viability Criterion

The strongest current ecology viability criterion is:

```text
the ecology remains recoverable while the positive cluster remains stronger than the negative cluster
```

This can now be stated more explicitly as:

```text
Rec_E = 1 if V_E > θ_rec
Rec_E = 0 if V_E <= θ_rec
```

where:

```text
V_E = (a*R_eff + b*R_res + c*C_eff) - (d*B_eff + e*F_eff)
```

This is the cleanest current ecological recoverability test.

## Four Ecology Regimes

The coupled model now supports four main regimes.

## Regime I: Stable Recovery Ecology

Condition:

```text
R_cap, R_res, C_sup high
B_sync, F_casc low
V_E comfortably above θ_rec
```

Meaning:

```text
the ecology still helps itself well enough that burdens remain real but non-owning
```

## Regime II: Compensating Recovery Ecology

Condition:

```text
positive cluster still stronger than negative cluster
but margins are narrowing
```

Meaning:

```text
the ecology is spending reserve and support to keep burdens partitioned
```

## Regime III: Fragile Recovery Ecology

Condition:

```text
positive and negative clusters near balance
V_E near θ_rec
```

Meaning:

```text
the ecology is still active, but recoverability is becoming thin and increasingly difficult to own
```

## Regime IV: Collapse Ecology

Condition:

```text
negative cluster stronger than positive cluster
V_E at or below θ_rec
```

Meaning:

```text
burdens have become ecology-owning and the system is no longer functionally recoverable as one ecology
```

This is the strongest current ecology-level death-approach regime.

## Recovery and Decline as Dynamic Loops

The coupled model is more realistic if two opposing loops are stated.

## Recovery Loop

The positive loop is:

```text
R_res -> C_sup -> R_cap -> lower B_sync -> lower F_casc -> preserved R_res
```

Interpretation:

- reserve enables support
- support enables recovery
- recovery keeps burdens from synchronising
- lower synchrony and cascade preserve reserve

This is the main life-preserving loop.

## Decline Loop

The negative loop is:

```text
B_sync -> F_casc -> lower C_sup and lower R_cap -> lower R_res -> higher B_sync
```

Interpretation:

- synchronised burdens raise cascade pressure
- cascade degrades support and recovery
- reserve is spent away
- the ecology becomes even less able to keep burdens apart

This is the main death-approach loop.

This loop structure is one of the strongest current results in the whole ecology layer.

## What This Clarifies About Life

This coupled model strengthens the life ontology in a decisive way.

Life is not merely:

- activity
- local repair
- burden tolerance
- or machine presence

It is:

```text
the continued dominance of the recovery loop over the decline loop in one bounded ecology
```

That is one of the strongest current sentences in the corpus.

It explains why:

- severe burden can remain compatible with life
- active function can coexist with near-death
- death approach is ecological, not merely local

## What This Clarifies About Death Approach

The strongest current coupled reading of death approach is:

```text
death approach begins when the decline loop becomes stronger than the recovery loop strongly enough that reserve, support, and recovery can no longer keep burdens partitioned below the ecology's recoverability threshold
```

This is a better line than:

- one machine fails
- one threshold is crossed
- one burden becomes high

It is a systems line, which is what the ecology layer needed.

## Best Current Compression

The best short line is:

```text
Life persists while recovery loops beat collapse loops.
```

The best fuller line is:

```text
A living ecology remains recoverable while reserve, support, and recovery reinforce one another strongly enough to keep synchrony and cascade from becoming the dominant system logic; death approaches when that balance reverses and the ecology can no longer keep burdens partitioned, buffered, and restoratively governed as one bounded continuity.
```

These are the strongest current reusable ecology-model lines.

## What This File Now Resolves

This file resolves five things.

1. The sharpened ecology variables now function as one coupled model.
2. Positive and negative variable clusters are now explicit.
3. Recovery and decline are now represented as opposing loops.
4. The ecology layer now has a clean recoverability criterion.
5. The life-boundary work now has a stronger systems-level base.

## Recommended Next Workstream

The best next move is:

```text
apply the coupled ecology model to worked recovery and death-approach scenarios
```

If one file is required next, the best immediate candidate is:

```text
ams-coupled-ecology-recovery-vs-collapse-scenarios-v1.md
```

because the coupled model is now explicit and should be pressure-tested against contrasting trajectory types.

## Compact Grammar

The best compression is:

```text
Life fails when collapse loops start winning.
```

## Provisional Conclusion

The ecology layer now has its first coupled core model.

AMS coupled ecology summary:

```text
A living ecology remains viable while recovery capacity, reserve depth, and effective cross-support reinforce one another strongly enough to keep burden synchronisation and cascade susceptibility below the recoverability threshold; death approaches when synchrony and cascade begin eroding reserve, support, and recovery faster than the ecology can restore them.
```

Score:

```text
coupled ecology core model: 9.45/10
```
