# RRC-002 proposal

Status: proposed, not frozen, not executed.

RRC-001 is closed. The stopping rule in `docs/feasibility.md` says that once the N≤5 contrasts have separated the five pre-registered possibilities, a further round has to name a new question. It is not opened in order to enlarge N. Those five possibilities are scored in that file. N=6 repeated the N≤5 verdicts. N=7 stays closed.

## Why a second computational round is not opened now

The exact outside description, for the next-step law of a designated interface, is settled on this grammar:

- Unconstrained weights: the interface itself is exact, and the outside grammar stays `unconstrained_lazy`, including the one two-triangle composition.
- Soft wedge: the lumpable closure is the full set of graphs in every frozen cell. No coarser exact description that still reports the interface exists there.
- Hard wedge: the closure omits only a thin, N-dependent set of graphs, and the unique lasting pattern is the empty graph.

Another size, another designated subset of the same kind, or another run of the same items would repeat this split. An approximate reduction is a different question. It is not opened here, because an approximation after an exact negative result needs its own error metric and its own freeze, and it is not required to understand the exact result.

## Leftovers worth understanding

Two exact patterns in the results do not yet have a general proof.

1. The hard-wedge defect on a hidden triangle is 51/40 at N=4, N=5 and N=6. The soft-wedge defect on a hidden triangle is 486/935 at N=5 and N=6. The witnesses are local, but the equality of the defects is an observation. A proof that either fraction is stable for every larger N would be an analytical result. It does not need a 2,097,152-state kernel.
2. At N=4, multiplying the soft-wedge weights of the star of node 0 by 2, 5 or 7 leaves every pair's stationary presence at 43/74. The same cancellation appeared, in a post-round check of the weight table, for several other positive weight pairs. It fails at N=3 and at N=5 for the frozen weights. A proof or a counterexample pair at N=4 is the right next step. The frozen plan itself used only the multiplier 5.

The ledger row for these leftovers is `RRC-001-OPEN-ANALYTIC`.

## A computational round, if one is later justified

The path-index instrument cannot see transmission inside a symmetry orbit. Depths greater than 0 were equal because every pair not touching node 0 is one orbit under relabeling of the remaining nodes. A later round that wants propagation along successive relations has to break that symmetry. One candidate is a carrier that is not the complete set of potential pairs, or a weight that treats the far pairs unequally, on N≤5, with an exact small case beside it.

That round is not designed here. If it is opened, it needs its own preflight, its own frozen plan, and its own item budget. It does not edit `plans/rrc-001.json`. It does not sample and then describe the sample as exhaustive.

## Synthesis

No intake into the shared synthesis is prepared beyond the existing unread proposal in `docs/synthesis-proposal.md`. A closed mathematical round can be offered for review later. This proposal does not make that offer.
