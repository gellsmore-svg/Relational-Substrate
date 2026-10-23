# Computational feasibility

Estimates below are priors taken from `gravity-time/docs/feasibility.md` (commit `38e92015`, blob `d75151d2`) and from the shape of the RRC engine. They are not yet measurements of this engine. Stage D replaces the timing column with a preflight on calibration kernels before the scientific plan is frozen. Calibration kernels are not RRC-001 cells.

## State-space prior

| N | Pair bits | States | GT measured kernel build | RRC-001 stance |
| --- | --- | --- | --- | --- |
| 3 | 3 | 8 | trivial | inside |
| 4 | 6 | 64 | <0.01 s | inside |
| 5 | 10 | 1,024 | 0.04 s for a 30-instance template | inside, to be remeasured |
| 6 | 15 | 32,768 | 5.0 s for 120 instances in the fraction builder | eligible only if one RRC item, including every augmentation declared for it, finishes under 120 s in preflight |
| 7 | 21 | 2,097,152 | estimated 10–20 min | not in RRC-001 |
| ≥8 | ≥28 | ≥2^28 | infeasible for exhaustive kernels | not in RRC-001 |

Memory for an integer weight table at N=6 is 32,768 × 15 × 2 bytes, well under a megabyte. A dense float stationary matrix at N=6 is about 8 GB and is forbidden. Stationary work at N=6, if any, is iterative and is cross-checked by a second initial condition, not by a dense factorisation.

## Item shape

One item is one `(N, rule, partition)` lumpability task, or one `(N, base rule, perturbed rule)` propagation task.

Each item carries its own id, frozen spec, input hash, status, output and receipt. A crash discards only the open item. The watchdog is 120 seconds. The hard ceiling for an ordinary item is five minutes, and the plan must not contain an item whose preflight or estimate exceeds 120 seconds.

`run` accepts `--max-items` and `--budget-seconds` and exits normally when either limit is hit. A long queue is finished by repeated invocations.

## Information value of the first round, before any cell is run

The round is worth running if it can separate these possibilities at small N:

1. Interface reduction is exact for every rule in the grammar.
2. Interface reduction is exact precisely when weights ignore the hidden pairs, and fails as soon as a wedge can sit on a hidden pair (possibly already at N=3).
3. Some intermediate sufficient statistic (count, parity, wedge profile) restores exactness without the full hidden graph.
4. Some N, possibly six, is the first size at which one of these behaviours changes.
5. A local weight change propagates along the declared path index, or it only rescales every rate through the normalising constant.

Any of these, including a null for (4), answers a live question. The round is not justified by the chance that six is special.

## Stopping

If preflight puts every informative N=6 item over 120 seconds, RRC-001 freezes without those items and says so. It does not sample them. If the N≤5 contrasts already separate (1)–(5) as far as this grammar can, a second round still has to name a new question. It is not opened to enlarge N.

## Measured before RRC-001

The prior table above is not the decision. The decision is `docs/rrc-001-preflight.md`: a calibration bundle in the heaviest planned shape (N=6, three augmentations, closure) took 10.522 seconds. N=6 remains in the frozen plan. N=7 does not.

## Scored after RRC-001

The cells were executed from the frozen plan and verified: 29 complete, none failed, timed out, or left unresolved. Execution commit `cdc1de55c3e6e2f4e1b646d33d78859101a3348a`. The reading is `reports/rrc-001-interpretation.md`.

The five separations above, scored only on this grammar and these designated subsets:

1. Exact interface reduction for every rule. Closed against the round: every hard-wedge and soft-wedge cell has a positive rational defect.
2. Exact when the weights ignore the hidden pairs, and already failing at N=3 once a wedge can use a hidden pair. This is what the cells show. Unconstrained cells have defect 0/1. Both wedge families fail from N=3 upward.
3. An intermediate statistic restores exactness. Edge count and parity do so when they are the single hidden bit. The wedge-count profile does so in one cell only, the hard wedge at N=3 with one hidden pair. For every soft-wedge cell the lumpable closure is the full set of graphs.
4. A first change at some N, with six as one candidate. The qualitative split is present at N=3. Six nodes repeats neighbour verdicts, including the hard-wedge triangle defect 51/40 at N=4, 5 and 6.
5. A local weight change moves along the path index, or it rescales rates. Stationary toggle rates of the soft-wedge boost equal the state-independent orbit rates. Occupation moves between the star of node 0 and its complement. Depths greater than 0 repeat that complement because they are one symmetry orbit of the instrument.

N≤5 already separates these five as far as this grammar and these instruments go. N=6 repeats them. The stopping rule above therefore leaves N=7 closed and does not open a second round in order to enlarge N. A later round has to name a new question. The candidate is `docs/rrc-002-proposal.md`, and it is not frozen.
