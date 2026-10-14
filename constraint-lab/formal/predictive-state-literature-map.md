# Predictive-state literature placement

Primary public sources inspected 2026-10-14. This is a terminology map, not a
systematic review, priority claim or import of new laboratory results.

| Object | Placement | Precise relationship |
| --- | --- | --- |
| Strong lumpability | Exact match in the declared finite homogeneous setting | Equal aggregate rows into partition blocks; arbitrary initial laws |
| Label-respecting probabilistic bisimulation | Exact match for finite state-labelled chains | A strong partition refining Pi_Y is a label-respecting bisimulation equivalence; coarsest strong refinement is its coarsest observation-respecting quotient |
| Trace / probabilistic language equivalence | Different, weaker object | Known hidden states agree on all finite observed words; branching structure can differ |
| Computational-mechanics causal states / epsilon-machines | Partial analogue, not identification | Classes of observed PASTS with equal conditional future laws, not partitions of a pre-given hidden Z subject to strong lumpability |
| Predictive state representations (PSRs) | Different construction with shared predictive aim | State is a vector of multi-step action-conditional test predictions; its dimension is not a count of strong-partition blocks |
| HMM minimisation | Different optimisation problem | May change latent representation, encoding and number of hidden states; 8I optimises none of these globally |
| Nerode-style equivalence | Analogue requiring declared domain | Residual future/language laws motivate equivalence of histories; that does not turn hidden-state strong refinement into causal-state minimisation |

## Sources and scoped claims

Bian and Abate define labelled-chain probabilistic bisimulation by equal labels
and equal probabilities of relation-closed sets; for finite equivalence classes
this is the block-sum condition. They distinguish linear trace behaviour from
branching equivalence and give strict separation. The mapping above is an
identification only under the explicitly finite, deterministic-label setup.
[Bian and Abate, extended version, 2017, definitions 1/3/6 and figure 1](https://arxiv.org/html/1701.04547v3).

Kiefer and Tang's 2024 paper explicitly distinguishes language/trace equivalence
from probabilistic bisimilarity, with the latter finer. Its MDP strategy and
approximate-distance problems are outside 8K; none of its complexity bounds
are attributed to the laboratory's exact partition utility.
[Kiefer and Tang, CONCUR 2024, introduction](https://drops.dagstuhl.de/storage/00lipics/lipics-vol311-concur2024/LIPIcs.CONCUR.2024.32/LIPIcs.CONCUR.2024.32.pdf).

Shalizi and Crutchfield define causal states through equality of conditional
future distributions given observed histories. That input domain differs from
known represented states. Their optimality language must not be transferred to
the laboratory's coarsest strong partition, nor read as unrestricted minimum
hidden-model cardinality. The source also discusses connections to formal
language theory, supporting analogy rather than terminological identity.
[Shalizi and Crutchfield, 2001, section IV.1 and appendices B/G.4](https://arxiv.org/html/cond-mat/9907176v2).

Littman, Sutton and Singh formulate PSRs using probabilities of selected
action-observation tests, contrasted with hidden-state and bounded-history
representations. A PSR's prediction-vector dimension and a finite quotient's
block count are not interchangeable. 8K does not implement or estimate PSRs.
[Littman, Sutton and Singh, NIPS 2001, paper PDF](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf).

## Terminology decision

Use **strong predictive refinement** only with its fixed-state,
observation-preserving, strong-lumping definition. Use **trace equivalence**
for all-word equality from known states and **stationary process equivalence**
for equality under declared stationary priors. Reserve **weak lumpability**
for actual first-order projected dynamics under a specified law.
Do not brand widehat-Pi_Y a causal state, epsilon-machine or PSR.
