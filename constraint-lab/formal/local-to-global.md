# Local-to-global mechanisms

## Pipeline

~~~mermaid
flowchart TD
  SY["Constraint syntax"] --> FV["Active feature vector"]
  FV --> LG["Unnormalised event log weights"]
  LG --> Q["Normalised event probabilities"]
  Q --> P["Full transition kernel"]
  P --> CLK["Full-event or next-pair-epoch dynamics"]
  CLK --> DIST["Finite-horizon or stationary distribution"]
  DIST --> PROJ["Declared projection / coarse-graining"]
  PROJ --> STAT["Observable statistic"]
~~~

| Arrow | What is specified or lost | Mechanism |
| --- | --- | --- |
| Syntax -> features | Satisfiability, direction and gate placement; neutral/redundant syntax may collapse | Boolean evaluation |
| Features -> log weights | Coefficients compose; different feature decompositions can yield the same function | Linear sum |
| Log weights -> probabilities | Common statewise shifts disappear; all slots become coupled | Exponentiation and shared denominator |
| Probabilities -> kernel | Event support and successor map are fixed; event labels can be lost if successors coincide | State update; injective toggles here |
| Kernel -> clocked dynamics | Hidden-only excursions are integrated out in E, not in immediate pair conditioning | Resolvent, products and path sums |
| Dynamics -> distribution | Initial priors/time horizon matter; stationarity removes source information but periodic limits need parity | Linear propagation; spectral/balance structure |
| Distribution -> projection | Labels, raw hidden coordinates or graph shape can be erased; a quotient need not be Markov | Deterministic many-to-one map |
| Projection -> statistic | Chosen summaries discard distinctions; equal statistics do not prove process equivalence | Information, passage or occupancy functional |

No downstream operation can reconstruct a distinction already erased without additional information. Nonlinear operations can redistribute existing distinctions among observables; they do not create a missing primitive gate coefficient in the original log-weight function.

## Normalisation is distinct from feature interaction

R05's denominator effect and 8D's probability-level interaction coexist with additive logits. In 8F, PROJECTION removes constant and first-order log-weight components under **uniform corners**, not under nonlinear probability or stationary weighting. Thus a centered interaction can still alter mean probability and occupancy.

ENDPOINT fixes two corners, PROJECTION fixes lower-order log components, and DRIFT fixes one balanced probability moment. None universally dominates; retain separate comparison vectors.

## Topology routes visibility

The same affected slot has different shape consequences in different visible graphs. In the canonical path, dissolving the middle edge and an end edge produces different unlabelled two-edge shapes. Formation when the action is already present is initially inadmissible. Star/triangle sources and their labelled action positions differ.

8C and 8F show this routing at committed finite horizons; they do not prove the path always dominates. 8F explicitly records path-not-universal. Edge count, shape conditional on edges, and labels conditional on class remain separate channels.

## Nested projection information

For mask X, class Y and edge count Z, CL-T16 gives
I(M;X)=I(M;Z)+I(M;Y|Z)+I(M;X|Y).
Each term answers a different question. Equal-prior JS measures law discrimination, not a scalar global interaction strength. Graph-class projection is finer than edge count, coarser than labelled mask.

## Clocks and current information

P takes one full toggle. Immediate pair q conditions the current slot law on a pair event. E waits through arbitrarily many hidden-only toggles before the next pair arrival. Pair-event stationary arrival occupancy differs from full-event occupancy and from event-weighted pre-pair context.

A current triad can predict the next pair slot even when the initial triad is forgotten in visible state. Current CMI is not historical memory. The 8F suppression case has lower stationary current CMI but greater K3/PROJECTION pair JS than favouring; no monotone prediction law follows.

## Stationary mechanism and limits

CL-T18 proves action-bit occupancy times uniform other pairs when action rates depend only on action and hidden bits. CL-T19 then proves stationary shape-given-edge invariance. The numerical 8F factorisation gap (~2.6e-15) verifies that palette; the new general proof is a distinct formal result with stricter stated assumptions.

At stationarity tiny edge and labelled residues can remain while shape disappears. At even checkpoints a fixed-parity source approaches a parity-conditioned stationary vector, not full stationary occupancy. Source forgetting does not erase all model discrimination.

## Evidential vector

Magnitude, robustness, temporal character, structural role, projection sensitivity and epistemic layer are not summed. The tiny 8F PROJECTION residue is persistent within tolerance, structurally diagnostic of a centered interaction comparison, and projection-dependent. Its size does not prove ontological importance. Conversely a large ENDPOINT difference may reflect unmatched lower-order bias.

Finite-model observations, mechanism inferences and RS/global-coherence interpretations must remain separate. The formal system explains model behaviour without establishing physical spacetime, receiver, design or theology.
