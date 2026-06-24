# AMS Vorton Geometry and Closure Formalism v1

## Purpose

This note is the first direct formalisation pass on the vorton model.

The immediate goal is not to produce a finished theory of everything. It is to define enough semi-formal structure that the current AMS language about:

- vortons;
- closure;
- route classes;
- coherence;
- reseating;
- fragmentation;

stops functioning as free narrative and starts functioning as constrained modelling language.

## Central Claim

The central claim is:

> A vorton is a bounded persistence pattern in a continuous substrate, maintained by closed or quasi-closed circulation of relational constraint such that local perturbations can be absorbed or reseated without immediate loss of identity. Vorton identity is therefore not primitive particle identity but closure-pattern identity.

## Formal Aim

The model needs to answer six questions.

```text
1. What counts as a vorton?
2. What counts as closure?
3. What counts as coherence?
4. What counts as a route through or between vortons?
5. What counts as a transition between route classes?
6. What counts as failure or fragmentation?
```

This file defines a first-pass answer to each.

## Primitive Objects

The current semi-formal model uses the following primitives.

### Substrate Region

Let:

```text
S
```

denote a continuous substrate domain.

Local regions are:

```text
R_i ⊂ S
```

The model does not assume that `S` is made of primitive pellets. It assumes continuity with structured local state.

### Local State Field

Let:

```text
X(x,t)
```

denote the local state of the substrate at position `x` and time `t`.

`X` is intentionally generic. It may later be decomposed into:

- density-like terms;
- circulation terms;
- torsion terms;
- phase or orientation terms;
- constraint-gradient terms.

For now, the only requirement is:

```text
X` must be rich enough to distinguish
diffusion,
circulation,
topological retention,
and breakup.
```

### Constraint Flow

Let:

```text
J(x,t)
```

denote local constraint flow.

This is not assumed to be identical to ordinary momentum or charge current, though it may correlate with such things in later model comparison.

The key point is:

```text
J describes how local organised strain or constraint is routed through the substrate.
```

### Boundary Surface

For any candidate persistent pattern `V`, define a boundary surface:

```text
∂V
```

This boundary need not be perfectly sharp. It is the operational surface across which inward retention and outward leakage are compared.

## Definition of a Vorton

A candidate vorton `V` is a bounded region of the substrate such that:

```text
V ⊂ S
```

and the following three conditions hold.

### Condition 1: Boundedness

There must be enough inward retention that the pattern does not immediately diffuse away.

Formally:

```text
B_in(V) > B_min
```

where:

- `B_in(V)` = inward-retentive closure strength;
- `B_min` = minimum threshold for persistence.

### Condition 2: Distributedness

The pattern must not collapse into singular local concentration that destroys route continuity.

Formally:

```text
D_spread(V) > D_min
```

where:

- `D_spread(V)` = distributedness of retained constraint across the region;
- `D_min` = minimum spread needed to avoid collapse into a non-propagating singularity.

### Condition 3: Returnability

The pattern must be able to route perturbation or strain through a return path rather than only radiating it outward.

Formally:

```text
R_return(V) > R_min
```

where:

- `R_return(V)` = existence and strength of closed or quasi-closed return paths.

### First Formal Definition

A vorton exists when:

```text
V exists iff
B_in(V) > B_min
and
D_spread(V) > D_min
and
R_return(V) > R_min
```

This is the minimum closure triad.

## Closure Function

Define the closure function:

```text
C(V) = f(B_in(V), D_spread(V), R_return(V))
```

For first-pass use, the simplest operational form is:

```text
C(V) = w1 * B_in(V) + w2 * D_spread(V) + w3 * R_return(V)
```

with positive weights:

```text
w1, w2, w3 > 0
```

This linear form is not meant to be final. It is a scaffold.

The important thing is:

```text
closure is not a single property
but a composite of retention, spread, and returnability
```

### Closure Thresholds

Use the following first-pass thresholds.

```text
C(V) < C_fail        -> no stable vorton
C_fail <= C(V) < C_weak  -> weak or metastable vorton
C_weak <= C(V) < C_strong -> viable vorton
C(V) >= C_strong     -> strongly retained vorton
```

This gives a formal basis for the earlier language:

- weak but real;
- strongly real;
- pseudo-route;
- fragmenting route field.

## Coherence

Closure alone is not enough. A pattern may be bounded but internally incoherent.

Define:

```text
Q_coh(V)
```

as coherence.

Operationally, coherence measures how well local state transitions within `V` remain mutually compatible under perturbation.

### First-Pass Coherence Form

Let:

```text
Q_coh(V) = 1 - N_conflict(V)
```

where `N_conflict(V)` is a normalised measure of incompatible local strain or route competition internal to `V`.

Interpretation:

```text
high Q_coh -> reseating remains lawful
low Q_coh  -> internal competition destroys retention
```

### Important Distinction

```text
C(V) answers: does it hold together at all?
Q_coh(V) answers: does it hold together cleanly enough to behave as one identity?
```

This distinction is needed for:

- metastable patterns;
- counterfeit continuities;
- fragmenting biological or machine states.

## Route Field

The current AMS work uses route language constantly. It now needs first-pass formal meaning.

For a given vorton or coupled system, define the route field:

```text
R_field(V)
```

as the set of dynamically admissible transition paths through or between closure regions.

Each path `p` in `R_field` has:

- entry cost;
- transit retention;
- exit cost;
- fragmentation risk.

Define route admissibility:

```text
A(p) = T_ret(p) - [L_diff(p) + X_frag(p)]
```

where:

- `T_ret(p)` = retained transmissibility along path `p`;
- `L_diff(p)` = diffusive loss;
- `X_frag(p)` = fragmentation penalty.

Then:

```text
p is viable iff A(p) > 0
```

This is the first-pass formal basis for route classes.

## Route-Class Mapping

The earlier route classes can now be tied to inequalities.

### R1: Narrow Viable Route

```text
A(p*) >> 0
for one dominant path p*
and
A(other paths) << A(p*)
```

Interpretation:

One narrow route dominates and remains strongly coherent.

### R2: Distributed Weak Routes

```text
multiple p_i with A(p_i) > 0
but none strongly dominant
```

Interpretation:

Transmission is real but spread across weaker pathways.

### R3: Blocked Apparent Route

```text
entry path appears open
but A(p) <= 0 after internal penalty
```

Interpretation:

The route looks viable locally but fails globally.

### R4: Inward-Biased Route

```text
A(p) > 0
with strong inward retention component
```

Interpretation:

The route deepens internal closure or inner reconfiguration rather than simple through-flow.

### R5: Loop-Dominated Pseudo-Route

```text
circulation persists
but net transmissible progress ~ 0
```

Interpretation:

The pattern loops constraint without productive route completion.

### R6: Fragmenting Route Field

```text
for most candidate paths p,
X_frag(p) dominates
```

Interpretation:

The region or coupled system can no longer maintain route coherence.

## Coupled Vorton Systems

Many important entities in the AMS work are not single vortons but coupled wholes.

Define a coupled system:

```text
W = {V1, V2, ..., Vn}
```

with coupling matrix:

```text
K_ij
```

where `K_ij` measures the strength and quality of route-compatible linkage between `Vi` and `Vj`.

### Higher-Order Wholeness Criterion

The coupled system counts as a real higher-order whole when:

```text
1. each Vi remains individually viable
2. K_ij exceeds minimum integration threshold for enough key pairs
3. the whole W has a coherence score Q_coh(W) not reducible to isolated Vi scores
```

That is:

```text
W is real iff
Vi viable
and
K-network integrated
and
Q_coh(W) > max individual-fragment risk
```

This is the formal scaffold behind the earlier claim:

```text
a genuine higher-order whole appears when coupled systems become more than adjacent parts
```

## Slip and Reseating

Earlier work used the phrase:

```text
slip as controlled relational reseating
```

This now needs formal meaning.

Define slip:

```text
S_slip(V, Δ)
```

as the ability of a vorton or coupled system to absorb perturbation `Δ` by redistributing local state while preserving global identity.

Operational condition:

```text
identity preserved iff
C(V after Δ) > C_fail
and
Q_coh(V after Δ) remains above coherence threshold
```

Interpretation:

```text
slip is good when local arrangement changes
but closure-pattern identity remains
```

This is essential for:

- glass behaviour;
- membrane behaviour;
- biological adaptation without identity loss;
- perturbation tolerance generally.

## Transition Criteria

The model needs formal criteria for state change.

### Persistence

```text
V persists if dC/dt and dQ_coh/dt remain bounded above failure thresholds
```

### Weakening

```text
V weakens if C(V) declines
while identity still remains above C_fail
```

### Fragmentation

```text
V fragments if
C(V) < C_fail
or
Q_coh(V) < Q_fail
or
R_field becomes predominantly R6
```

### Reconfiguration

```text
V reconfigures if local topology changes
but identity-class invariants remain
```

This last criterion is especially important because many AMS claims depend on:

```text
real continuity through lawful reconfiguration
```

## Identity-Class Invariants

A stronger model needs explicit invariants.

For now, define a vorton identity class by:

```text
I(V) = {topological class, closure range, coherence range, dominant route grammar}
```

Two states `V_a` and `V_b` count as the same identity-class if:

```text
Top(V_a) ~ Top(V_b)
and
C(V_a), C(V_b) lie within same viability band
and
Q_coh(V_a), Q_coh(V_b) lie within same coherence band
and
dominant route class remains equivalent
```

This is not yet a full invariant theory, but it is enough to stop identity from collapsing into raw visual similarity.

## Obstruction Classes

The earlier obstruction classes can also be formalised.

### O1: Funnelling

```text
entry and transit costs channel flow into one narrow viable path
```

### O2: Late-Gate

```text
route stays viable until a downstream threshold abruptly blocks completion
```

### O3: Pocketing

```text
constraint enters local retention zone but does not re-emerge productively
```

### O4: Biasing

```text
route field remains open but skewed toward inward, delayed, or selective completion
```

### O5: Diffusing

```text
loss terms dominate retention before coherent completion
```

### O6: Fragmenting

```text
internal incompatibility and breakup dominate all candidate route continuities
```

## First Formal Consequences

The current scaffold gives several real constraints.

### Consequence 1

Not every persistent swirl counts as a vorton.

It must satisfy:

```text
boundedness
distributedness
returnability
```

### Consequence 2

Closure and coherence are distinct.

This matters for:

- metastability;
- counterfeit order;
- corrupt continuation;
- pseudo-routes.

### Consequence 3

Higher-order systems require integration criteria, not proximity alone.

This matters for:

- molecules;
- membranes;
- machine systems;
- living cells.

### Consequence 4

Failure is formally describable as threshold crossing, not just narrative collapse.

This matters for:

- oxidative damage;
- membrane rupture;
- mistranslation overload;
- false persistence.

## What This Still Does Not Solve

This file is a scaffold, not a finished formal physics.

It still does not provide:

- exact equations of motion for `X`;
- exact geometry for specific vorton families;
- direct derivation of quantum or electromagnetic observables;
- a completed invariant theory;
- a proven mapping from AMS variables to standard measurable quantities.

Those remain next-phase tasks.

## Compact Formal Grammar

The best current compression is:

```text
A vorton is a bounded closure-pattern identity in a continuous substrate, defined by sufficient retention, sufficient spread, and sufficient returnability to preserve coherent route-bearing persistence through perturbation.
```

Expanded:

```text
Vorton identity is the persistence of a topologically and dynamically constrained closure pattern whose internal coherence and route admissibility remain above fragmentation thresholds, allowing lawful reseating without immediate loss of identity.
```

## Score Recalibration

### Constraint Gain

This file significantly increases constraint relative to earlier purely descriptive usage.

Score:

```text
8.5/10
```

### Formal Sufficiency

It is still only semi-formal, not yet a mathematically complete theory.

Score:

```text
7.5/10
```

### Programme Value

As a dependency-clearing scaffold, it is very high value.

Score:

```text
9.0/10
```

## Provisional Conclusion

The AMS programme now has its first serious closure formalism.

AMS summary:

```text
Vortons are closure-pattern identities in a continuous substrate, and their persistence depends on boundedness, distributedness, returnability, coherence, and route admissibility remaining above fragmentation thresholds.
```

Score:

```text
vorton geometry and closure formalism: 8.5/10 as scaffold
```

## Recommended Next Workstream

The best next artifact is:

```text
ams-route-variable-mathematical-framework-v1.md
```

Reason:

The present file defines the objects and thresholds. The next step is to formalise the variable system itself:

- `B_in`
- `B_out`
- `Q_coh`
- `J_bound`
- `J_trans`
- `D`
- `I_comp`

and relate them more explicitly.
