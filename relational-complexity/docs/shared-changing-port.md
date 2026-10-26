# A shared port that changes: dynamics, consistency and later participation

**Status:** Analytical increment, 26 October 2026.
**Method:** `shared-port-analysis-0.1.0`, analysis-only.

A changing interface can be shared state without being an additional independent
coordinate. Here components identify a port value already read from their own
states. Their composite retains that boundary and supports further composition.
Agreement is a transition constraint: synchronizing equal labels alone does not
guarantee it. This is one declared operator, not a canonical rule for all gluing.

## 1. Typed objects and event clock

Fix a finite nonempty port set P and a finite handshake alphabet H, possibly
empty. A component consists of finite nonempty states S, an onto boundary map
`b:S -> P`, and finite nonnegative integer label matrices W_l. Positive entries
are aggregate event weights; duplicate events of one label add. Individual
event identities are not recovered from these matrices.

Require **private port preservation**: for l outside H, `W_l(s,u)>0` implies
`b(s)=b(u)`. Shared events may change the port. A zero-weight entry is not a
positive write; invalid endpoints are still invalid. Surjectivity is a typing
choice ensuring nonempty compatible fibres, not a reachability assertion.

| Aspect | Declared contract |
| --- | --- |
| Identified composite state | `(s,t)` with `b_A(s)=b_B(t)` |
| Port value | Their common value; no extra coordinate is appended |
| Shared label h | Pair two h events with product weight; keep only compatible targets |
| Private label | One component updates and the other holds; private writes preserve the port |
| Output boundary | The inherited common port, with the same P and H |
| Normalisation | Only the final admitted event row; keep intermediate weights raw |
| Empty admitted row | Implicit halt self-loop, not a real event |
| Reapplication | The output is another component of this same type |

The value of the interface can change. The port type P, ownership rule and H
remain fixed. This is not evolving membership, changing handshake topology,
independently added controller state or identification of all constituent states.

## 2. Definition and well-typed output

For components A and B write `S times_P T` for their compatible pairs. For
compatible source `(s,t)` and target `(u,v)`, define raw output matrices:

```text
h in H:       U_h((s,t),(u,v)) = W_h(s,u) * V_h(t,v)
l outside H: U_l((s,t),(u,v)) = W_l(s,u) * indicator(t=v)
                                + indicator(s=u) * V_l(t,v)
```

Absent matrices are zero. These are the previous Cartesian weighted-label
formulas restricted to compatible sources **and targets**. Filtering before
normalisation is part of the new instrument. It must not be mistaken for a
proof that agreement was invariant in the unconstrained copy system.

Each port fibre is nonempty in both inputs, so their fibre product is nonempty
and its boundary onto P. A positive private output event changes only one
input, whose port is preserved. Thus the output satisfies the private contract
and can participate in another shared-port product. No engine method is changed.

## 3. Reapplication, associativity and unit

**Associativity theorem.** For three such components at fixed P and H, the
canonical reassociation `((s,t),r) <-> (s,(t,r))` is a boundary-preserving equality
of raw labelled weights on triples whose three source ports agree.

For a shared h, either parenthesization keeps precisely target triples whose
three ports agree, with weight `W_h(s,u)*V_h(t,v)*Z_h(r,w)`. An incompatible
intermediate pair could not be part of a compatible final triple. For a private
label, the result is the sum of the three single-factor updates, with the other
two states held fixed. Each private write preserves the common port. This is
the same sum under both parenthesizations; no fibre-size factor appears.
These equalities prove the raw dynamical claim, not only a set identity.
The final normalized kernels also agree. Intermediate normalisation followed
by interpreting probabilities as weights is outside this theorem.

**Unit.** Take states P with identity boundary, one weight-one shared h event
`p -> q` for every h and every pair of port values, and no private events.
The bijection `(s,b(s)) -> s` (or its left-sided version) preserves all raw
labels and weights. For each shared event there is exactly one unit transition
with the required source and target port, of weight one. Private events pair
with the fixed matching unit state and preserve its value. This proves both
identity laws. The unit relays arbitrary shared port changes; it is not a
one-state halt component, and its standalone normalised law need not be inert.
Its identity property is for the identified operator. With unconstrained
Cartesian copies, its different possible target ports can leak out of agreement;
being this operator's unit does not imply that separate copies stay consistent.

The private-write contract matters. If an input could privately change p to q,
the other unit state would hold p; filtering would suppress that write, so this
unit would not preserve the input. Other ownership/update rules may admit such
writes, but they define other operators. When P is a singleton this construction
reduces exactly to the previously declared Cartesian product and its unit.

These are finite weighted-automaton facts under a common boundary, not a claim
that every adaptive interface is associative or that a hierarchy must emerge.

## 4. When do synchronized copies already agree?

Let F be the **unfiltered Cartesian** synchronization product with the same raw
input weights and H. Let I be its agreement image `b_A(s)=b_B(t)`.

**Invariance criterion.** I is invariant under F's final kernel if and only if,
for every shared h and every compatible source `(s,t)`, every positive pair of
h events `s -> u`, `t -> v` has `b_A(u)=b_B(v)`.

Private events cannot leave I by their contract. A shared event leaves I exactly
when its two positive target ports disagree. Nonnegative weights cannot cancel
such a contribution; normalization preserves positivity. An empty Cartesian
row halts within I. These observations prove both directions.

When the criterion holds, the inclusion of identified states into I preserves
raw labelled weights and is a kernel conjugacy onto an invariant image. It is
an **injective image comparison**, not a noninjective lumpability claim or a
carrier automorphism. Outside I, the copy system can have other states/dynamics.

Without invariance, identified raw matrices still equal the I-by-I restriction,
but their normalized rows need not be the original kernel's restricted rows:

| Raw row | Relationship to the Cartesian kernel |
| --- | --- |
| Some admitted weight remains | The identified row is its one-step law conditioned on the next state lying in I |
| Original raw total is zero | Both systems halt at the valid source |
| Original total positive, admitted total zero | Conditioning has zero probability and is undefined; the new operator halts by its declared completion |

For the first case, if total raw mass is T and admitted mass R>0, retained
Cartesian probabilities are admitted weights divided by T. Dividing again by
`R/T` gives weights divided by R, exactly the identified row. This is a rowwise
conditioning identity, not a claim about conditioning an entire future path.

An h write `0 -> 1` of weight 2 paired with an h hold `0 -> 0` of weight 3
leaves agreement with weight 6. A private unit hold provides admitted weight 1.
The copy kernel leaks `6/7`; the identified row holds with probability 1. Remove
that private event and conditioning is undefined, while the identified row
halts. Undefined restricted/conditional laws are left absent in the evidence.

### Equal marginals are not a shared random choice

Give each two-port component one h event into port 0 of weight 1 and into port
1 of weight 2, from either source. Both have the same port kernel `[1/3,2/3]`.
Their Cartesian pairing has weights 1,2,2,4 on target pairs 00,01,10,11. It
leaks `4/9` from each agreement state. Enforcing agreement leaves weights 1 and
4, so the identified port law is `[1/5,4/5]`, not either original marginal.
Identical marginal laws did not provide a common random draw. A different
correlated coupling would require a different declared matching/weight rule.

The clock policy is consequential. If rejected Cartesian attempts are counted
as holds at their source instead of discarded, the port rows in this example
become `[5/9,4/9]` and `[1/9,8/9]`. The checker reports this as an explicit
alternate-clock control. It is not the shared-port operator or an observation
of physical duration. No inequivalence caused by this policy is attributed to
spontaneously discovered relational structure.

## 5. A dynamic, consequential and reducible interface

Let A have states `(x,p)`, B have `(p,y)`, with all three variables binary.
Each shared h event flips its local p copy with weight one. A privately flips
x with weight `1+p`; B privately flips y with weight one. In the composite the
single identified p changes on h and affects the x rate. No new independent
interface variable is appended: there are eight `(x,p,y)` states, rather than
sixteen Cartesian states storing both copies.

The input state declarations already allow p to vary independently of x and y:
all `(x,p)` and `(p,y)` combinations are specified. That independence enters in
the inputs. Identification removes one redundant copy; it does not create p
from an overlap, grouping or a name assigned to a collection.

The copy agreement image is invariant here. The identified dynamics are exactly
ordinary current-state single-coordinate flips on the three-bit encoding:
`x` has weight `1+p`, `p` weight 1 and `y` weight 1. The x rate is a literal
factor-2 multiply when p is present. This **particular construction** therefore
reduces to the existing positive single-toggle grammar; it is not a new engine
primitive. Arbitrary shared-port components need not admit this bit encoding.

Observe only `(x,y)`. At x=y=0, p=0 gives block row
`[1/3,1/3,1/3,0]`; p=1 gives `[1/4,1/4,1/2,0]`, in observed order 00,01,10,11.
The observation is not strongly lumpable. The interface evolves and is
predictively consequential under this rate choice, rather than merely renamed.

As a null, set the x weight to one at both p values, keeping h and y events.
The same observation becomes exact even though p still changes. Thus a changing
shared port does not automatically matter for every predictive task.

## 6. Closed prediction versus an inherited interface

For any surjective observation `pi:S -> Q`, an inherited boundary `b_hat:Q -> P`
with `b=b_hat compose pi` exists **if and only if** b is constant on pi blocks.
Necessity follows by evaluating b_hat on one observed value. For sufficiency,
define b_hat(q) using any state in that block; constancy makes it well-defined.
It is unique and onto because pi and b are onto. This is elementary map
factorization, not an additional stochastic theorem.

In the no-feedback null above, `(x,y)` has a closed Markov law but merges p=0
with p=1. It therefore has no inherited port map to the original P and cannot
be substituted as the same port-typed component just from that kernel.
Appending a fresh port or changing its meaning would be an explicit new model
choice. Conversely, preserving b alone does not ensure a closed law: hidden
rates inside one port fibre can still destroy lumpability.

This is a type boundary, separate from the earlier all-partner criterion for
unconstrained Cartesian states. That theorem cannot silently be imported into
this identified-state context class. No minimal abstraction for all interfaces,
histories, observations or policies is classified here.

## 7. Verification, precedents and limits

The state set is a conventional fibre product of finite sets; weighted
synchronization, support invariance, conditioning and map factorization are
established mathematics. The RRC-specific increment specifies one compatible
dynamical gluing rule, proves its reapplication laws and exposes the distinction
between prediction and retaining a usable boundary.

Related precedent includes Baez, Fong and Pollard,
[*A Compositional Framework for Markov Processes*](https://arxiv.org/abs/1508.06448),
which composes open continuous-time processes through inputs/outputs, and Baez
and Courser, [*Coarse-Graining Open Markov Processes*](https://arxiv.org/abs/1710.11343),
which studies coarse-graining with that composition. Those boundary-state,
continuous-time and steady-state constructions are different from the present
port-value fibre product and row-normalized event rule. Their categorical
results are not claimed as a proof of this operator's laws or an identification
with our process. No universal mathematical novelty is asserted.

`provenance/shared-port-analysis-check.py` compares sparse event matching with
dense Cartesian label matrices restricted by an explicit image, checks exact
Fraction rows against the support criterion, and compares the feedback model
with a separate bit-table construction. Tests add hand fractions and previous
sparse-Cartesian compatibility. The bounded domain was predeclared separately;
general claims follow from the proofs, not its fixture counts. Software caps
(64 Cartesian validation states, 4096 event records) are not theorem bounds.

The port type and handshake alphabet do not evolve, and no independent
membership/controller state, causal intervention, autonomous entity, physical
clock or RS ontology is derived. Frozen history and old methods remain intact;
this analytical increment adds zero scientific workers or adopted atlas cells.
