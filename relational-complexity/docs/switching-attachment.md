# A switching attachment: fixed-protocol reduction and required predictive state

**Status:** Analytical result, 26 October 2026.
**Method:** `switching-link-analysis-0.1.0`, analysis-only.

An independently changing link can alter which constituents update together
without requiring a new finite-state primitive. The link policy below compiles
exactly to a fixed four-label protocol with an explicit controller. Its mode
cannot generally be inferred from the actors' configuration. The coarsest exact
current-state refinement of that configuration keeps the mode precisely where
an actor can move, and forgets it where both actors are inactive.

The reduction preserves global raw labelled dynamics. It does not preserve a
literal interpretation of the original attachment graph or claim that joint
events become single-bit events. These representation contracts are distinct.

## 1. Types, independently declared state and clock

Let S and T be finite nonempty actor state sets. A(s,u) and B(t,v) are finite
nonnegative integer raw matrices with **zero diagonals**. They describe actor
moves, not their normalised kernels; parallel indistinguishable moves aggregate.
Actor self-loops are outside this grammar. The controller has states m=0,1 and
switch weights gamma_0,gamma_1, also nonnegative integers.

All states `(s,t,m)` are valid. The link relation is absent at m=0 and connects
the actors' update participation at m=1. At m=0, one actor moves at a time. At
m=1, both move together. A switch changes only m. The two modes are independently
selectable for the same `(s,t)` by the input declaration; they are not a derived
cover, grouping, shared-port value or emergent coordinate.

```mermaid
flowchart LR
  U["link off: left or right actor moves"] -->|"switch: gamma_0"| C["link on: actors move jointly"]
  C -->|"switch: gamma_1"| U
```

The four output labels are H={left,right,joint,switch}. For each source, the raw
events are:

| Mode | Label and update | Raw weight |
| --- | --- | --- |
| 0 | left: `(s,t,0) -> (u,t,0)` | A(s,u) |
| 0 | right: `(s,t,0) -> (s,v,0)` | B(t,v) |
| 1 | joint: `(s,t,1) -> (u,v,1)` | A(s,u) B(t,v) |
| Either m | switch: `(s,t,m) -> (s,t,1-m)` | gamma_m |

Zero weights enable no event. Sum all admitted weights and normalize **once**
for one global event; a zero raw row halts implicitly without adding an event.
One synchronized joint move and one switch each count as one event. These are
dimensionless weights, not physical transition rates. The product and scheduling
rules specify one link policy, not a universal meaning of attachment or
statistical independence of the actors' discrete-time trajectories.

The output is a finite weighted labelled system on S times T times {0,1}, with
the fixed protocol alphabet H. It can enter further existing same-H Cartesian
composition while its full state and raw matrices are retained. We do not claim
that recursively connecting independently controlled links is associative under
an unspecified network-ownership rule.

## 2. Exact compilation to a fixed shared protocol

Construct three finite components, all sharing every label in H:

| Component | Active transitions | Explicit weight-one passive transitions |
| --- | --- | --- |
| Actor S | A(s,u) under left and joint | self-loop under right and switch |
| Actor T | B(t,v) under right and joint | self-loop under left and switch |
| Controller | m=0 loops under left/right; m=1 loops under joint; switches with gamma_m | guard-loop weights are one |

The controller offers no joint event at m=0 and no left/right event at m=1.
Missing events block the corresponding all-shared synchronization. The passive
loops are real participation events; they are not substituted halt completions,
extra independent event attempts or zero-time transitions.

**Compilation theorem.** The all-shared raw product of these three components
has exactly the four global matrices in section 1 under the state bijection
`(s,t,m) <-> (s,t,m)`. Thus raw labelled weights and the final kernel agree,
including all-zero rows. No additional state beyond the already declared mode
is introduced, and no hidden intermediate clock step is inserted.

**Proof.** For left at mode 0, the matching weights are A(s,u), 1 and 1, and the
other actor/mode hold. At mode 1 the controller offers no left match. The right
case is symmetric. For joint at mode 1 the weights multiply to A(s,u)B(t,v),
with controller loop weight one; the mode-0 guard blocks it. For switch both
actors contribute their unit loops and the controller contributes gamma_m.
These exhaust the labels and reproduce every raw entry. If all four channels
are absent globally, both constructions have a zero row and apply the same
halt rule. Local passive loops alone never create a global event.

Because the correspondence preserves raw labels, it also survives subsequent
composition using the earlier fixed-H product, even when a later partner adds
private competing events. This follows by substituting equal matrices into that
operator; it is not a new classification of all contextual equivalences.

The compiler expands the actors' protocol catalogues. It does not assert that
their original standalone matrices equal these expanded component matrices,
preserve individual event identities, or establish physical communication
equivalence of the two declared interaction graphs. In particular, passive
module participation in a fixed protocol is an encoding of the changing global
update rule. Normalised-kernel agreement alone would be weaker than the raw
correspondence needed for later competing contexts.

## 3. Exactly what the actor-only observer loses

Let pi(s,t,m)=(s,t). Exactness means one common first-order quotient kernel for
every microstate and initial distribution: strong lumpability. This is not
closure under one selected initial mode or an assertion about finite histories.

Call `(s,t)` **active** when `a_s+b_t>0`, where `a_s=sum_u A(s,u)` and
`b_t=sum_v B(t,v)`. Call it inactive otherwise.

**Actor-view criterion.** The two modes at a fixed `(s,t)` have equal outgoing
pi-block rows iff that actor configuration is inactive. Consequently pi is
strongly lumpable on the full model iff every actor configuration is inactive.

**Proof.** At an active configuration, mode 0 has positive probability of
changing exactly one actor. Its total raw row is a_s+b_t+gamma_0, hence positive.
Mode 1 changes both actors or neither: actor diagonals are zero, so joint moves
cannot have the same observed target as any mode-0 local move. If its raw row
is zero it halts, which still changes neither actor. Thus the observed rows
differ. At an inactive configuration both actor rows are zero, so only switches
or halt are possible; every such event stays in that pi block. Both rows are
the same point mass there. This proves both directions, including zero gamma.

The off-diagonal actor assumption is essential to this disjoint-support proof.
The formula is not asserted for actors with genuine self-loop moves. A passive
loop introduced by the compiler does not change the original actor grammar.

## 4. Coarsest exact refinement retaining the actor configuration

Order deterministic observations by partition refinement, requiring the actor
view pi to factor through them. Each pi block has two states. A refinement can
either keep that pair together or separate its two modes; it cannot merge
different actor configurations.

Define pi_star by splitting every active pair and leaving each inactive pair
together. Its state count is

```text
|S| |T| + number of active actor configurations.
```

**Minimal-refinement theorem.** pi_star is the unique coarsest strongly lumpable
refinement of pi, for every model in section 1.

**Necessity.** If an exact refinement left an active pair together, equality of
its outgoing refined-block probabilities would imply equality after aggregating
them back to pi blocks. Section 3 shows those pi rows differ. Therefore every
exact refinement must separate every active pair.

**Sufficiency.** Active refined blocks are singletons. An inactive block has no
actor move in either mode, so all switches or halts stay in that same block.
Both sources give its point-mass block row. The partition is strongly lumpable.
Every exact refinement refines this one, which proves coarseness and uniqueness.

If all actor configurations are active, the full state is required among these
refinements. If all are inactive, pi itself suffices even while the link changes.
For binary actors with only their 0-to-1 moves enabled, (1,1) is inactive and the
coarsest refinement has seven states instead of eight. These are consequences
of the support rule, not preferred state counts.

Minimality is **not** over all observations: the constant observation is always
Markov but discards the required actor configuration. Nor is it a lower bound
on special-initial-state or history-based models. Even an exact pi_star quotient
need not preserve raw labels or be safe for every later partner. With inactive
actors and gamma_0=1,gamma_1=2, actor-only prediction is constant, but a partner
that synchronizes on switch and offers a private unit competitor sees move
probabilities 1/2 versus 2/3. This applies the previously established calibration
lesson; it is not another universal contextual theorem.

## 5. Fixed finite protocol does not imply single-bit support

Consider binary toggle actors with all four off-diagonal weights strictly
positive and gamma_0,gamma_1>0. The global support contains the directed cycle

```text
(0,0,0) --left--> (1,0,0) --right--> (1,1,0)
        --switch--> (1,1,1) --joint--> (0,0,1)
        --switch--> (0,0,0).
```

Each edge has positive weight under these assumptions; no probability threshold
or enumeration is needed to establish the five-cycle.

**Same-clock support obstruction.** There is no injective encoding of these
full states into a binary hypercube of any dimension that maps every positive
off-diagonal transition to one bit flip at the same one-event clock.

Every one-bit edge changes Hamming parity. Five such edges cannot return to
the same encoded state, proving the obstruction. This is elementary
bipartiteness, not a new universal expressivity theorem.

Controls matter. When both switch weights are zero, each fixed-mode image is
invariant. In mode 0, the actor coordinates themselves give one-bit moves.
In mode 1, `(a,b) -> (a,a xor b)` turns the joint toggle into a one-bit move with
the other coordinate fixed. These encodings do not combine into one permitted
encoding of the genuinely switching model. Special initial-mode laws are
different from a common quotient over both full modes.

The fixed-protocol compilation remains valid: it permits joint global updates.
It therefore does not compile this full positive switching support into the
single-toggle support of rrc-0.4.0. Extra intermediate steps, a changed clock,
noninjective/distributional encodings or a different primitive event class lie
outside the obstruction. Ordinary finite-state representation is already
available; no new computational power, physical mechanism or ontology follows.

## 6. Verification and established precedents

Guarded synchronization and passive weight-one participation are established
finite-state modelling techniques; see the official
[PRISM synchronization documentation](https://www.prismmodelchecker.org/manual/ThePRISMLanguage/Synchronisation).
PRISM also explains that its
[parallel scheduling depends on the model type](https://www.prismmodelchecker.org/manual/ThePRISMLanguage/ParallelComposition).
Our dimensionless raw-product/final-normalization convention is explicitly
specified here, not asserted to be PRISM's default DTMC scheduler or a
continuous-time physical rate law. The paper's reductions and refinement proof
are self-contained consequences of this RRC-specific link policy.

Strong lumpability uses the standard equality-of-probability-to-block criterion.
The coarsest-refinement formula is proved for this grammar by its separated
local/joint supports; it is not generalized from a finite parameter menu.

`provenance/switching-link-analysis-check.py` compares direct guarded global
matrices with independent n-ary matching of the compiled event catalogues.
It enumerates all deterministic actor-view refinements in the predeclared
binary menu and checks their minima without assuming the proposed formula.
Tests add hand fractions, the previous binary sparse product, a later private
context, and a separate support-colouring algorithm. Generality is mathematical;
finite enumeration is software verification, not new scientific cells.

The implementation limits global states to 32, actors to four states each,
and exhaustive refinement to eight actor blocks. These are validation cost
caps, not bounds on the finite theorems. Existing methods and frozen history
retain their meanings; this analytical increment invokes no scientific worker.
