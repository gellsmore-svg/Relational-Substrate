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
