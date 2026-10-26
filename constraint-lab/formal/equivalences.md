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
