# Synchronising composition and sufficient effective descriptions

**Status:** Analytic increment, 26 October 2026.
**Method:** `label-sync-analysis-0.1.0`, analysis only.
**Question:** When can component descriptions be substituted inside a typed
interaction without changing the resulting dynamics?

## 1. Typed inputs, output and clock

A component is a finite nonempty state set S, a fixed handshake alphabet H,
and nonnegative integer matrices W_label on S for finitely many labels.
An entry is the aggregate weight of events with that label, source and target.
Distinct parallel event identities are not preserved by this representation;
their weights add within a label. Labelled self-loops are permitted.

| Feature | Contract |
| --- | --- |
| Constituent state | An arbitrary finite state, not necessarily a bit mask |
| Composition input | Two weighted labelled components with the same H |
| Composed state | Cartesian pair `(s,t)`; no extra state beyond the inputs |
| Shared event | Same label in H, both components update, weights multiply |
| Private event | Label outside H, one component updates while the other holds |
| Unmatched shared event | Blocked; an absent matrix is zero |
| Composition output | Another weighted labelled component with the same H |
| Clock | One global composed event, then row normalisation |
| Empty row | Halt self-loop, not an event available to synchronise |
| Reapplication | Defined using the unnormalised output and the same fixed H |

This is synchronization of action labels, not identification of equal interface
states or a changing block-membership operation. The product-of-weights choice
is a declared instrument. It is not asserted to be the canonical policy for
all stochastic systems or a law of physical interaction.

Write the two inputs' label matrices as W_label and V_label. The output is:

```text
label in H:       U_label = W_label tensor V_label
label outside H:  U_label = W_label tensor I + I tensor V_label
```

The label alphabet is the finite union of input labels and H; missing weights
are zero. Sum all U_label matrices and normalise each positive row. A zero row
gets probability one on its own state. Do not insert that completion into the
event matrices before another composition. Private self-loops, in contrast,
are real weighted events and affect the composed event clock.

Raw weights and H are part of the input contract. A component's normalised
Markov kernel is not sufficient input data for this operator. A different
normalisation or synchronization policy would be a different declared operator.

## 2. Iteration and identity

**Associativity at fixed H.** After reassociating Cartesian triples, the two
parenthesisations have equal label matrices before normalisation. For a shared
label, both give `W_label tensor V_label tensor Z_label`. For a private label,
both give the sum of three matrices: that factor's label matrix and identities
in the other two positions. Distributivity proves the equality, including zero
and self-loop matrices. The final normalised kernels therefore also agree.

This proves an iteration property of the specified dynamical operation, not
merely a repeated naming of a tuple. A handshake event of the composed component
can participate in a further joint event with a third component. It requires
all participants under the same H; it is not a model of arbitrary bilateral or
changing synchronization topology. Normalising intermediate outputs and then
reinterpreting probabilities as weights is outside this associativity statement.

**Identity.** The one-state component with one weight-one self-loop for every
label in H, and no private event, is a left and right identity. Its shared
matrices are `[1]` and private matrices `[0]`, giving exactly the other input's
weights. When H is empty, the empty one-state component serves this role.

The all-halt one-state component and this identity both have standalone kernel
`[1]`. For nonempty H they are not interchangeable in composition. A two-state
partner that toggles on a shared label moves with the identity, but halts with
the empty component. Halt completion cannot be promoted to a synchronising event.

## 3. Exact standalone prediction is not a congruence

Let A have states `(z,d)`, with `z,d` each 0 or 1. The hidden coordinate d holds.
The only event flips z, with weight one. Its label is a when d=0 and b when d=1.
Take H={a,b}. Both hidden states give the same aggregate raw weights and the
same normalised law on z: a deterministic flip. The observation dropping d is
strongly lumpable for A, for every starting distribution.

Let B be a two-state component toggling on a with weight one and offering no b.
Retain the observation `(z,B-state)` after composition. From `(z=0,d=0,B=0)`
the composed law moves to observed `(1,1)` with probability one. From
`(z=0,d=1,B=0)` the shared b is blocked and the row halts at observed `(0,0)`.
These sources share their observation but have different outgoing block rows.
There is no exact first-order quotient under that product observation.

The finite checker uses micro encoding `2*z+d` and product encoding `2*micro+B`.
Its witness sources are 0 and 2, both observed as 0. Their block rows are
`[0,0,0,1]` and `[1,0,0,0]`. Nonexact rows are reported as undefined, not filled
with zeros or approximated. This comparison changes label allocation, not the
standalone aggregate raw weights. Ordinary kernel equality and standalone
lumpability have erased information needed by this particular interaction.

## 4. A sufficient quotient rule that does compose

Let pi and rho be surjective observations of the two components. Require, for
every label and every target observation block, that the sum of outgoing label
weights into that block is the same at every source in one source block.
This defines a weighted labelled quotient for each component.

**Preservation theorem.** Under this condition on both inputs, reducing before
composition and composing before reduction have equal labelwise block weights
under `pi times rho`. After normalisation, the product observation is strongly
lumpable and its exact kernel is the kernel of the composed weighted quotients.

**Proof for shared labels.** Sum the product weight over a target product block.
The finite double sum factors into the W_label block sum times the V_label block
sum. Each is fixed by its source observation. Their product is exactly the
shared-label weight in the composition of the quotients.

**Proof for private labels.** The identity on the passive factor sums to one
when the target observation equals the passive source observation, and to zero
otherwise. Each term therefore gives the quotient's label block sum times the
appropriate observed identity. Adding the two private contributions yields the
private-label formula on the quotient product. No block-cardinality multiplier
appears.

**Normalisation and halt.** Summing the equal block weights gives equal row
totals within a source product block. Positive rows normalise identically.
If a total is zero, every source in that block halts at its own observation,
as does the quotient. Thus the exact normalised block rows agree in both cases.

The condition allows hidden state to hold, flip, reset or evolve in other ways.
It constrains labelwise flow into observed blocks, not transitions inside each
block. An event that becomes a quotient self-loop must retain its label and
weight: it can still synchronise with a partner and change that partner's state.
The condition concerns weighted label behaviour, not recovery of all microscopic
event identities or preservation of original carrier meanings.

This is a sufficient rule, not a necessary condition for every particular partner.
For example, if A's a-flip weights are 1 and 2 at the two hidden values, a shared-
only partner still yields a deterministic joint flip. Its product observation
is exact even though the labelwise weights of A differ within a block.

## 5. The private-clock boundary

Add a weight-one private self-loop at every partner state in that last example.
At hidden weight 1, the joint flip and the private event each have probability
`1/2`. At hidden weight 2, they have probabilities `2/3` and `1/3`. The retained
product observation is no longer strongly lumpable. Labels of A have not changed;
its raw weight scale, invisible to its standalone kernel, now matters relative
to the partner's private event.

The contrast follows from the declared product-weight/global-clock convention,
not an invariant assertion about every composition policy. It also shows why
normalised labelled probabilities alone do not generally replace the raw
weighted interface contract. No causal intervention or physical timescale is
inferred from this constructed comparison.

## 6. Verification, scope and precedents

`provenance/label-sync-analysis-check.py` compares sparse event-pair enumeration
with independent dense per-label matrix formulas. Exact Fraction aggregation
checks normalised observations; unit tests also use hand-derived rows. Its
bounded domains and the analytical selection are recorded separately. The
prototype caps itself at 32 states and 2048 event records for cost, not as a
mathematical limit of the proved operator.

Weighted labelled transition systems and the labelwise sum-to-class condition
are established mathematics: see Miculan and Peressotti, *Weak bisimulations for
labelled transition systems weighted over semirings*, Definitions 1–2,
[arXiv:1310.4106](https://arxiv.org/abs/1310.4106). We use the strong weighted
condition as a sufficient interface contract. Their weak/silent-transition
results are not imported, and the particular product/clock policy here is
explicitly specified rather than attributed to every process algebra.

The proofs are elementary matrix and block-sum consequences, not claims of new
universal theorems. Compared with the previous XOR analysis, the new question
changes the operation and the subsequent system dynamics, and the sufficient
condition permits evolving omitted state. Broad composition, higher-order-state
and ontology questions remain open.
