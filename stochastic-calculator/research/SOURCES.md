# Sources and methodological boundaries

Accessed 2026-09-10. These are conventional comparators, not empirical RS evidence.

1. Chen, Doty and Soloveichik, *Deterministic function computation with chemical
   reaction networks*, Natural Computing 13 (2014), 517-534.
   [Author-hosted paper](https://www.dna.caltech.edu/Papers/Chen-Doty-Soloveichik-2014-deterministic-CRNs.pdf).
   Establishes exact stable function computation in a specified CRN model and
   characterizes its functions via semilinearity. The paper distinguishes stable
   reaction-count outputs from equilibrium concentration approximations and warns
   about composition and completion detection. Our model is not a fixed finite
   CRN: it uses labelled pair registries, variable structures, and global checks.
   Its multiplication result is therefore not a counterexample to that theorem.

2. Angluin, Aspnes, Eisenstat and Ruppert, *The computational power of population
   protocols*. [Primary manuscript](https://arxiv.org/abs/cs/0608084).
   Provides the conventional setting in which local interaction rules yield stable
   global outputs, with explicit computational limits. Anonymous finite-state agents
   are materially different from our labelled and extensible data structures.

3. Tao, *Finite time blowup for an averaged three-dimensional Navier-Stokes
   equation*. [Primary manuscript](https://arxiv.org/abs/1402.0290).
   Methodological comparison only: conservation properties alone do not specify
   all relevant nonlinear dynamics. This is the averaged equation, not the
   unmodified Navier-Stokes equation or the user-mentioned 2026 construction.

## 2026 Navier-Stokes boundary

The request's 2026 construction was not supplied as a specific primary manuscript.
Contemporary search results were not sufficient here to audit its mathematical
claims, forcing assumptions, or proof status. No conclusion in this project relies
on its validity. The requested analogy is used only to motivate separate tests of
conservation, cancellation, covariance, local coupling, and amplification. We make
no claim of equivalence to a PDE, fluid energy landscape, or physical blowup.

## Repository context

- [CONTRIBUTING.md](../../CONTRIBUTING.md) requires epistemic discipline and conventional baselines.
- [Validation status](../../docs/relational-substrate-validation-status.md) distinguishes a conceptual
  lens from a quantitative physical predictor.
- [State of model](../../docs/state-of-model-2026-07-12.md) distinguishes internal consistency from
  empirical correctness. The calculator does not raise the latter.
