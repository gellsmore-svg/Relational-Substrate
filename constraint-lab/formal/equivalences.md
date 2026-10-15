# Equivalence, symmetry and quotienting

## Declared hierarchy

| Notion | Required agreement | Qualification |
| --- | --- | --- |
| Canonical syntax | Same canonical rule collection and factor interpretation | Vertex-relabelling canonicalisation is declared; duplicate multiplicity is not erased |
| Unnormalised law | Same event weights at every full current state | Sufficient but not necessary for q equality |
| Local full-event law | Same normalised event distribution at every state | Positive weights may differ by a common state-dependent scale |
| Full-kernel equality | Same P on the same labelled state space | Equivalent to full-event law equality here because each toggle has a distinct successor |
| Conjugacy | P'(f(x),f(x'))=P(x,x') for an explicit bijection f | Initial distributions and event projections must map too |
| Projected process equality | Same declared projected finite-dimensional distributions | Specify clock, initial prior, projection and horizon family; projection need not be Markov |
| Statistic equality | Same chosen occupancy, passage or information statistic | Strictly weaker than process equality |

Immediate pair-conditioned slot equality is not full-event equality: multiplying every pair weight by 2 preserves conditional pair probabilities but changes pair-versus-hidden-event hazard. Nor does it automatically preserve the next-pair epoch kernel.

Generation 7B's fitted aggregate collapse is not a proof of projected-process equivalence. Once its equal complementary factors are specified, CL-T04 proves equality to an unconditional local/full kernel, which is a different claim. Generation 8D provides several full-state eliminations and distinct law-coordinate patterns. Generation 8F provides explicit hidden-state conjugacies fixing visible pair labels.

## Vertex covariance versus automorphism

A vertex permutation maps both relation coordinates and rules. This covariance is available to the labelled model. Keeping rules fixed generally leaves only a stabiliser subgroup as automorphisms. Quotienting by all S4 graph isomorphisms while ignoring a labelled law can destroy transition semantics; 8A repaired exactly that error.

For partition blocks, strong lumpability requires equal total transition probability from any two states in one block into every destination block. Automorphism orbit partitions satisfy this condition. Isomorphic visible pair graphs with different raw hidden configurations need not.

## Independent hidden-bit symmetries

At N=4 the four independent hidden triad bits have symmetric baseline flips. A coordinate permutation need not arise from a vertex permutation to conjugate a selected one-action law. Complement maps can also work when literal polarity and priors map.

The BOTH/ONE/NEITHER placements are structurally distinct under S4 but dynamically conjugate in the 8F grammar, with pair projection fixed. This is exact projected-process equality for mapped uniform-hidden priors, not an assertion that all triad-conditioned kernels are exchangeable.

## Incidence boundary

Independent hypergraph state coordinates do not automatically impose face coupling. 'Pair is a face of triad' is metadata until used by the law. Independence of coordinates does not imply statistical independence of paths: normalisation couples slot probabilities.

Incidence can become dynamically consequential within an existing ordinary grammar by choosing correlated face-action templates, several coupled pair actions, or pair-dependent gate behaviour. Alternatives include simplicial closure, geometry or shared-state coupling, but no such extension is selected in 8G. L or H is not required merely to consult incidence when constructing fixed rules.

## Observable-preserving Markov refinement (predictive-state 8I)

A raw projection merely groups equal current observations and may fail strong
lumpability. A strong-lumping refinement splits those groups until every member
has the same aggregate transition row into every refined block. The coarsest
such refinement is obtained by exact partition iteration (CL-T52), and works
for arbitrary augmented initial distributions. This is stronger than stationary
weak lumpability under one prior.

Full future-word equivalence requires equal laws for every finite observed
future, preserving the current observation. Strong lumping is sufficient for
that equality but need not be necessary in arbitrary hidden models. In this
RECENT-REVERSAL N4 instance, distinct stable blocks sharing a current observation
already have different next-observation rows, so the two notions coincide on
the fixed declared state set. Neither notion claims globally smallest hidden
Markov realisation under arbitrary re-encoding.

The 28 marked-graph, 12 count/direction and 2 parity reductions are exact strong
lumpings, not kernel conjugacies or mere statistic equalities. Their nested
quotient maps commute (CL-T59). Matching stationary one-step rows with H0 is
strictly weaker than projected-process equality; only parity has the separate
all-order equality proof for all m.

## Generation 8K implication map

This is not a single linear hierarchy: some notions concern two models,
others a partition of one model, and others a chosen prior or statistic.
See [general theory](predictive-state-theory.md) and
[exact false-converse fixtures](predictive-state-counterexamples.md).

| Notion | What is preserved | Implication and caution |
| --- | --- | --- |
| Typed state-space isomorphism | Declared coordinate/observation meaning under a bijection | A bare bijection says nothing about T |
| Kernel equality | Same T on identical state labels | Path equality also needs the same initial law and observation |
| Kernel conjugacy | T'(f(z),f(u))=T(z,u) for a bijection | Transport mu and phi too for model/process isomorphism |
| Strong lumpability | Equal block sums for arbitrary starting states | Gives an exact quotient for every mu, with transported observation |
| Observation-preserving strong refinement | Coarsest eligible partition of fixed Z | CL-T52/T60/T61; not minimum latent-model realisation |
| Future-word / trace equivalence | Every finite future observation law from known states, plus current output | Strong blocks imply it; converse fails in CE-TRACE |
| Weak lumpability | Projected first-order law for a specified mu | Does not imply strong lumpability; CE-WEAK is fully positive |
| Stationary observed-process equivalence | All observed finite-dimensional laws under declared stationary priors | Does not identify hidden kernels or require a Markov output |
| Stationary one-step equivalence | One-time and adjacent two-time joint laws | Does not imply weak lumpability or longer-word equality; CL-T67 |
| Statistic equality | One declared distribution/statistic/projection | Weaker than the corresponding full observed path equality |

Strong block equality implies trace equivalence by induction on words.
For two initial mixtures, equal weights on trace-equivalence classes suffice
for equality of observed finite-dimensional laws. No converse about hidden
state identities follows. A chosen stationary pair matching is weaker still.
Do not confuse the existence of Q_mu with a weak-lumping theorem.

The non-neutral 8H/8I mask/class/count processes are examples of stationary
ONE-STEP equality without weak lumpability, not examples of stationary Markov
projection. Parity has the separate all-order process proof. CE-WEAK shows
that actual stationary weak lumpability can occur without strong lumpability.

## Generation 8M: Comparator And Alphabet Scope

KU-H1 uniformly averages already-normalised rows in older history and has its
own stationary law. Kpi-H1 conditionally averages using the actual stationary
law and matches adjacent (P,h1) joints, not all paths. Exact equal stationary
joint laws can coexist with unequal kernels: M0 R00/R09 direction partners.
STAR/TRIANGLE instead have opposite-pair kernel conjugacy, not same-labelled
kernel equality. Transporting the class alphabet exchanges star and triangle
while leaving count fixed. Equal scalar information under that bijection is
weaker than identical raw class laws.

## Generation 8N: Passage Equality

Equality of selected return, MFPT or committor functionals is weaker than
full path equality. Different path laws can give equal selected functionals;
same occupancy and stationary adjacency do not force passage equality.
Kernel conjugacy transports stopping sets, starts and passage alphabets, not
necessarily identical raw labelled outputs. A one-return class kernel under
stationary conditional starts is not automatically a strong Markov quotient.
See [history-controlled passage](history-controlled-passage.md).

## Generation 8O: Equality After A Stopping Readout

For matched stationary sources, [route equality](markovization-stopping-factorization.md)
is exactly U W=0 for the declared killed/reset/readout operators. Nonzero
factors can annihilate in a product. This criterion is neither strong lumpability
nor equality of every future word; changing source, route or target changes the
criterion. Kernel conjugacy transports the criterion to a renamed task.

## 8P Stopping Equivalences

Eventual target equality, all-length terminal equality and full coarse path equality are different equivalences. [Exact rational counterexamples](stopping-sufficiency-counterexamples.md) disprove the tempting converses. Source/target linear spans are algebraic testing spaces, not arbitrary admissible stochastic priors.
