# Candidate methods

Methods are chosen per question. Listing a method here does not mean RRC-001 implements it.

| Method | Questions it might serve | RRC-001 decision |
| --- | --- | --- |
| Exact enumeration of the single-toggle chain | Q01–Q07 | Selected. State spaces: N=3 (8), N=4 (64), N=5 (1,024), N=6 (32,768). N=7 (2,097,152) is not selected |
| Strong lumpability defect, exact rational | Q02, Q04, Q05, Q07 | Selected. Defect zero is the exactness test. The reported magnitude is the maximum L1 distance to the block-mean row |
| Lumpable closure by repeated splitting | Q02, Q04, Q07, Q09 | Selected only for items whose state count the preflight shows can finish inside the watchdog. The closure size is the number of current-state blocks needed so that the refined process is Markov and still reports the original interface |
| Declared augmentations (edge count, parity, wedge profile) | Q07 | Selected. These are instruments. Failure is a result |
| Stationary distribution by power iteration, cross-checked by a dense solve when the dense matrix fits | Q06 | Selected for propagation items. Two independent starts when the dense solve does not fit. A residual above the frozen tolerance leaves the item unresolved |
| Analytical identities for state-independent rates | Q04, Q06, Q08 | Selected as checks, not as discoveries. Uniform stationary measure. Exact marginal lumpability. Toggle rate r_e / sum(r) |
| Graph isomorphism census | Q01 | Not selected. Interface questions at fixed labels do not need orbit counts |
| Monte Carlo | — | Not selected. Nothing in RRC-001 is reported as exhaustive if it was sampled |
| Mean-field, branching process, renormalisation | Q08, Q09 at large N | Not selected. No large-network claim is open |
| Bounded treewidth / cut decomposition | Q08 | Candidate for a later round if exact cells show a sparse sufficient statistic. Not implemented now |
| Weak lumpability | Q04 | Not selected. It depends on the initial law. Using it would blur the exactness claim |

## Exactness conditions the engine must enforce

For a partition of the finite state space, strong lumpability holds if and only if every state in a block has the same total probability of moving into each block. The one-step interface process is then Markov for every initial distribution, and its transition row is that common row.

The test depends on the original transition and on the partition. It does not depend on a stationary distribution. A stationary distance can be small while lumpability fails, and the engine must not substitute one for the other.

Weights in RRC-001 are non-negative integers. Transition probabilities on a non-halt state are those integers over their sum, as rational numbers. Halt states contribute a self-loop of probability 1 on their own block. Two signatures are equal only when those rationals are equal. There is no rounding in the exactness bit.

Float arithmetic is confined to stationary iteration, where the plan states a tolerance and a second method.
