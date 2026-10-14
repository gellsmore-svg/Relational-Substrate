# State taxonomy and notation

Generation 8K is a formal synthesis. None of the categories below adds a new
executed ontology axis. See [predictive theory](predictive-state-theory.md),
[compilation classes](axis-compilation.md) and the historical
[notation audit](notation.md).

## 1. Process model and notation audit

Use a finite homogeneous process model mathcal-M=(Z,T,mu), with row-stochastic
T. For prior-free claims write just (Z,T). mu is an initial distribution;
stationarity is the additional condition mu T=mu, never a default assumption.
A state value is z in Z; time-indexed represented state is Z_t.

| Existing symbol | Retained meaning | Synthesis choice |
| --- | --- | --- |
| P / p | Pair mask in 8H/8I; older P also denoted full kernel | P_t remains the worked-example pair mask; use T for kernels |
| R / r | Parity in 8I; remembered-pair presence r; older receive descriptors | R_t parity, r presence; never R for predictive refinement |
| S | Programme entity-state axis, historically also state | Do not rename S; use Z for general represented state |
| H | History axis/depth; h last-pair register | H_t general historical summary; h_1,h_2 explicitly pair-clock slots |
| L | Meta-constraint depth; word length on an alternate branch | Retain axis L; use ell for a word length in new theory |
| K | Per-rule expression complexity; K_t count in 8I | Keep both scoped historical uses; k is a count value |
| J | Rule cardinality | Unchanged |
| C | Graph class or ordinary constraint collection | C_t graph class; compilation class is mathfrak-A |
| M | Information model label in earlier comparisons | mathcal-M process; a random comparison label is separately declared |
| T | Transition kernel in history/predictive theory | T throughout the synthesis |
| Z | Augmented state; earlier lower-case z had local roles | Z is full represented state space, z a value |
| Pi_Y | Fibres of current observation | widehat-Pi_Y is its coarsest strong refinement |

Formal formulas use Pi_Y, widehat-Pi_Y, rho_Y for its block map, and B_t for
the current refinement block. They do not repurpose P_Y as another pair mask.
Entropy, if mentioned, is Ent_mu(B), not an unqualified H.
The existing ordinary grammar and its K/J budgets are not redefined.

## 2. Ordinary/material state X

X is the declared ordinary relational representation. In the current N4/O3
independent hypergraph it is ten bits: six labelled pairs and four triads.
It answers which ordinary relations currently exist in that representation.
It is not asserted to be the complete metaphysical present.

The pair-epoch state reduction in 8H/8I uses P, the six pair bits, only after
proving the triad-excursion quotient. This does not erase triads from the
declared ordinary X or silently move a new variable into S.

## 3. Hidden current state

A coordinate can be hidden by an observation while still being determined by
complete current X. Triad bits are hidden when the observation is the pair
mask; the finer pair topology is hidden when the observation is edge count.
These are ordinary current distinctions, not H merely because they are unseen.

8B/8C's current triad efficacy versus loss of information about the initial
triads is the historical example (CL-I01, F018-LOCAL-VERSUS-INITIAL).
Time-indexed initial and current variables are different quantities.

## 4. Historical state H

H_t is a declared summary of prior process information, for example

    H_t=F(X_0,E_1,X_1,...,E_t,X_t),
    H_(t+1)=U_H(H_t,X_t,E_(t+1),X_(t+1)).

For genuinely additional historical state relative to X, it must not be a
function of X_t on the declared reachable domain. Historical origin alone does
not show this: a redundant past-derived variable might already be recoverable
from X_t. Nor does an arbitrarily initialised hidden variable establish a
common-start history witness.

8H supplies the stronger condition: one common programme and start, two legal
ordered paths, same complete X, different last-pair h and different futures.
Its h remembers the most recent PAIR event, including across triad-only events.
At the pair clock its depth is H_pair=1, alphabet size six after the sentinel.

A passive history register may record past information without affecting any
future ordinary row. Correlation with that register is not sufficient evidence
that the law reads it. Current efficacy need not imply permanent retention of
the initial register (CL-T32).

Finite alphabet, recursive update and bounded temporal window are distinct:
a one-bit cumulative event parity can summarise arbitrarily old events.
One-step recursive update does not by itself mean temporal depth one.

## 5. Augmented represented Markov state Z

Z_t=(X_t,H_t), or in a future design (X_t,H_t,eta_t,...), is first-order if the
conditional next joint law given the full past depends only on Z_t.
Every coordinate is represented at the current time; a coordinate's historical
origin does not make it absent from the augmented present.

Finite cardinality alone does not prove sufficiency. If the update reads
omitted history, an unrepresented external driver or an omitted clock phase,
the purported Z is not yet a closed homogeneous Markov representation.
See CL-T64/T65 for the precise conditional-law hypotheses.

## 6. Observation Y

A deterministic map phi:Z->Y defines Y_t=phi(Z_t). It can omit current ordinary
coordinates, historical coordinates and constraint state. Examples are labelled
pair mask, graph class, edge count and parity.

An observation is a mathematical projection, not an observer, cause or ontology
axis. It need not preserve Markovity. Fine-state history, projection-induced
memory and history-specific process differences must be distinguished.

## 7. Strong predictive refinement

Pi_Y groups states with the same current Y. widehat-Pi_Y is the unique
coarsest strongly lumpable refinement of Pi_Y on the fixed (Z,T).
B_t=rho_Y(Z_t) is its Markov quotient state and Y_t is determined by B_t.
This is the named strong predictive refinement, not an unqualified claim of
globally minimal predictive state or minimal hidden-model realisation.

It can retain hidden CURRENT structure, historical information or both.
Predictive sufficiency is a role relative to process, observation and equivalence
criterion, not a new ontology category. A refinement block need not be known
from a finite observation suffix; synchronization is a separate property.

8I's model-specific non-neutral path is 384 labelled-history states -> 28
marked-pair graph roles -> 12 count/direction states -> 2 parity states.
The maximum extra categories per current observation are 6,4,2,1, respectively;
the last is trivial, meaning zero extra historical information.
This is not a universal identity->role->direction->nothing law.

## 8. Constraint state eta and fixed meta-programme

Candidate eta_t is represented state whose interpreted value configures how
ordinary constraint expressions are instantiated, enabled, parameterised,
scoped, composed or interpreted. A decoder might map eta to an active rule set
or coefficients. The common meta-programme specifies that decoder AND its
update law. Selecting two static rule sets in different experiments is not
dynamic constraint state under one programme.

No eta dynamics or L-positive controller is implemented in 8K. Finite closed
constraint dynamics can flatten to a kernel (CL-T65). A stronger L claim needs
declared semantic/compiler restrictions, not merely proof that eta matters.

| Boundary case | Historical origin? | Constraint-configuring role? | Consequence |
| --- | --- | --- | --- |
| Unobserved triad bit already in X | Not required | May influence ordinary weights | Hidden current state, not automatically H or L |
| Last pair slot used by fixed reversal law | Yes | Fixed law reads h directly | Executed H example; not evidence of dynamic constraint architecture |
| eta stores exactly the last pair under another name | Yes | Only claimed by renaming | No additional capability established |
| Past-derived eta enables an explicit rule object | Yes | Yes, if decoder/update declared | H origin and L-style role may overlap; raw kernels do not separate them |
| H controls a coefficient in one fixed expression | Yes | Ambiguous architectural reading | Coefficient dependence alone does not establish a new L axis |
| Autonomous rule-enable eta | Not necessarily ordinary-path-derived | Yes | Candidate dynamic constraint state; flattening still applies if closed |
| Unrepresented evolving rule interpreter | Unknown | Claimed | Augmented state may be incomplete; no flattening theorem yet |

Origin, update semantics, grammatical role and interpretation are separate axes
of description. H and eta are neither presumed independent nor mutually exclusive.

## 9. Belief/filter state

For declared mu, b_t(z)=Pr_mu(Z_t=z | Y_0,...,Y_t) is a posterior distribution,
not another physical material coordinate. Its predictions depend on T and mu.
There can be infinitely many reachable beliefs even for finite Z.
Two beliefs may have equal future-word predictions without identical support
or identical hidden configurations.

History-state H is part of the generative representation. A filter is an
inferential distribution over represented states. Causal states partition
observed histories by future law, not necessarily the original hidden states;
see the [literature map](predictive-state-literature-map.md).

## 10. What is not being claimed

No category here denotes minimal physical memory, an ontology hierarchy,
irreducible time, observer-created history, purpose, design or theology.
All ontology/global-coherence readings remain separate from algebraic,
finite exact, numerical, model-inference and methodological claims.

## Generation 8L: semantic temporal depth two

Verified SECOND-RECENT retains (h1,h2), the two most recent PAIR slots.
The alphabet has 36 recurrent values; its temporal depth is two, regardless of
whether it is encoded in two variables, one 36-valued variable or several bits.
The strict H1 class preserves h1's last-pair meaning, not arbitrary recoding.
At identical complete X and h1, different reachable h2 gives different ordinary
rows. The augmented (X,h1,h2) is nevertheless first-order Markov.
At labelled pair resolution its strong predictive refinement has 2304 blocks,
while its observed order is three: neither number defines depth.
See [history depth](history-depth.md); no L-positive state is introduced.
