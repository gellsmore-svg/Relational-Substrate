# Which distinctions can every allowed partner expose?

**Status:** Analytical result, 26 October 2026.
**Method:** `context-probe-analysis-0.1.0`, analysis-only.

For the fixed-H product, an observation remains exact in every allowed context
if and only if it preserves each shared label's raw block weights and the
aggregate private block weights. Private labels need not remain distinct for
this state-only observer. A finite family of at most three-state partners
separates every failure, even though the allowed context class has no finite
state-size bound. This is a statement about a declared context class and clock.

## 1. Types, observation and quantifiers

Use the finite weighted labelled systems and operator in
`labelled-sync-composition.md`. A has nonempty finite state set S, finite
handshake alphabet H, and finite nonnegative integer label matrices W_l.
The private labels are those outside H. Parallel events of one label add.
No microscopic event identities are preserved by these matrices.

Every allowed partner B has a finite nonempty state set T, the same H, finite
nonnegative integer weights, and may offer private events, including a
unit-weight event. The label vocabulary permits a private label outside H.
Shared events pair with product weight; private events interleave; only the
final composed row is normalised. An empty raw row halts without adding an
event. A real self-loop contributes weight and competes in that final row.

Let pi: S -> Q be surjective. Retain `(pi(s),t)` in A composed with B. The
observer sees all partner states, but sees no event labels, identities or raw
weights directly. An exact description means strong lumpability of this
product observation, for every microstate and initial distribution, at one
final global-event step. It is not a stationary or selected-initial-state claim.

Define **uniform contextual preservation** of pi to mean this exactness for
**every finite allowed B**. In particular, the partner class includes branching
private calibration events. Restricting that class or observing fewer partner
states is a different question. No physical duration is being measured.

## 2. The necessary and sufficient signature

For s in S and observed target block C, define

```text
w_h(s,C) = sum over u with pi(u)=C of W_h(s,u), for each h in H
p(s,C)   = sum over private l and u with pi(u)=C of W_l(s,u)
```

Keep these shared-label vectors and the one private aggregate in separate
namespaces. The condition is equality of this entire signature for every pair
s,s' with pi(s)=pi(s'). It includes target C=pi(s): a private event internal to
one observation block can still compete with a partner event. Raw weight,
rather than a normalised component probability, is the quantity compared.

**Theorem.** The following are equivalent:

1. The signature is constant within every source observation block.
2. pi is uniformly contextually preserved for the context class in section 1.
3. pi times partner identity is strongly lumpable for every probe in section 3.

This is an exact iff within these quantifiers. It is not a necessary condition
for each particular partner, nor for every conceivable composition policy.

## 3. A finite separating family and necessity

Use one private label k outside H. Its spelling is immaterial: a private label
never synchronizes here, even if both components use that spelling.

| Probe | States | Only partner events | Purpose |
| --- | --- | --- | --- |
| B_0 | 0,1 | private k: 0 -> 1, weight 1 | Recovers private block weights |
| B_h, for each h in H | 0,1,2 | shared h: 0 -> 1 and private k: 0 -> 2, both weight 1 | Separates h and calibrates its raw scale |

Partner states 1 and 2 have no partner events. This does not prevent the
component's private events from interleaving there. The family has `1+|H|`
members, each of size at most three. It is an upper bound, not a minimality
claim. If H is empty, only B_0 is needed.

At source `(s,0)`, B_0 has denominator
`D_0(s)=1+sum_C p(s,C)`. Its probability into `(pi(s),1)` is exactly `1/D_0`.
Its probability into `(C,0)` is `p(s,C)/D_0`. Dividing the latter by the former
recovers every private block weight, including the internal-block weight.
All shared component events are blocked by this probe.

For B_h the denominator is
`D_h(s)=1+sum_C p(s,C)+sum_C w_h(s,C)`. The probability into `(pi(s),2)` is
`1/D_h`; into `(C,1)` it is `w_h(s,C)/D_h`; into `(C,0)` it is `p(s,C)/D_h`.
Other shared labels are blocked. Taking ratios to the calibration branch
recovers each w_h and also p. Every denominator is positive and finite even
when A has no event, because the partner offers its unit-weight private event.

If two sources with the same pi value have equal observed rows in these
probes, their calibration probabilities and all these ratios agree. Thus their
raw signatures agree. Contrapositively, any signature difference has a probe
with different observed rows at `(s,0)` and `(s',0)`. A nonexact quotient has no
rows; the differing rows are a failure witness, not a proposed approximate law.
This proves 3 -> 1. The implication 2 -> 3 holds because the probes are allowed.
No enumeration of arbitrary contexts is used to infer this necessity result.
These probes separate exact probability laws. They do not recover arbitrary
raw weights exactly from finitely many sampled trajectories.

## 4. Sufficiency for every finite partner

Write V_h for the partner's shared matrices and R for the sum of its private
matrices. Before normalisation, the outgoing weight from `(s,t)` into observed
target `(C,v)` is

```text
F(s,t; C,v) = sum over h in H of w_h(s,C) * V_h(t,v)
             + p(s,C) * indicator(v=t)
             + indicator(C=pi(s)) * R(t,v).
```

This follows by factoring the finite shared target sum. For a private event,
the passive identity sums to a Kronecker delta, with no target-block size
multiplier. Thus F depends only on pi(s) and t under condition 1. Its total
also does. Positive rows normalise identically; an all-zero row halts at its
source observation for every source in that product block. Therefore the
product observation is strongly lumpable for any allowed B. This proves 1 -> 2.
No assumption requires the omitted component state to remain fixed.

## 5. What can be safely merged, and what cannot

Replace every private label by one new private name, adding weights. Keep each
shared label. Call this relabelling c_H. It is not a weak/silent-transition
construction: private transitions still consume one event, retain self-loops
and weights, and are not removed or replaced by multi-step paths.

At weighted matrix level, c_H commutes with this product:

```text
c_H(A compose_H B) = c_H(A) compose_H c_H(B).
```

For shared matrices nothing changes. For the private matrix both sides give
`P_A tensor I + I tensor P_B`. This equality uses common Cartesian state
indexing and compares the collapsed weighted labels, not the original private
labels. The signature condition is precisely the familiar labelwise weighted
block-sum condition applied **after** c_H. Its weighted quotient has the same
normalised observed law in every allowed context. The operation can be
reapplied under the same H; retaining original private names is unnecessary
for these state observations, including after further same-H compositions.

Consequently, the previous full-label sufficient condition is **not necessary
even for every context in this class**. Example: states `(z,d)` each flip z and
d with weight 1, using private p when d=0 and private q when d=1. H={a,b}.
Dropping d preserves p(s,C): one unit into the opposite z block. Full separate
p/q block weights differ, but the theorem guarantees exactness for all allowed
partners. This is a general guarantee from the proof, not an extrapolation
from three probes or a bounded partner menu.

Limits are consequential:

- If H changes to include p and q, a partner can synchronize selectively and
  distinguish the same states. Fixed-H substitutability does not license an
  interface change that promotes previously private labels.
- If emitted labels are observed, the example's p versus q distinction is
  already visible. The label-blind theorem does not preserve that observation.
- If partners cannot offer competing private events, raw scaling may cancel.
  An a-only joint flip at hidden weights 1 and 2 is exact with a shared-only
  toggle partner. A calibrated a probe distinguishes it. The theorem's
  necessity must not be exported to that restricted partner class.
- A private self-loop of weight 1 versus no event is visible to B_0 even when
  the component observation is constant: the partner moves with probability
  1/2 versus 1. Implicit halt is not an event and cannot supply that weight.

This result neither identifies original constituent states nor adds membership
state, autonomous entities, a new engine primitive, a causal intervention or a
physical timescale. Label and raw-weight distinctions become consequential
relative to the operator, allowed contexts and observation chosen here.

## 6. Established mathematics and independent challenge

The raw sum-to-class criterion is established strong weighted bisimulation;
see Miculan and Peressotti, *Weak bisimulations for labelled transition systems
weighted over semirings*, Definitions 1-2,
[arXiv:1310.4106](https://arxiv.org/abs/1310.4106). We use the strong criterion
after an explicit private-label relabelling. No weak-transition or continuous-
time semantics is imported. The RRC-specific contribution is the exact context
class, observer, calibration/separation construction and its policy boundaries.
The elementary proof is not claimed as a new universal process-algebra theorem.

The broader precedent of characterizing processes by tests includes Larsen and
Skou, [*Bisimulation through probabilistic testing*](https://doi.org/10.1016/0890-5401(91)90030-6).
Their abstract concerns a different testing language and equivalences; that
paper is not the source of this product, raw-weight calibration or iff claim.
No equivalence with its testing theory is asserted.

`provenance/context-probe-analysis-check.py` independently compares direct raw
event signatures with dense labelled-matrix composition, Fraction normalisation
and observed row sums. It recovers each signature from probe probabilities.
The validation domain was selected before execution. Generality follows from
the proofs, not the finite case count. Hand fractions and the existing sparse
event implementation provide additional independent checks in the tests.
Software caps of 16 constituent states, 64 product states and 2048 input events
bound this checker, not the theorem. There are no new scientific atlas cells.
