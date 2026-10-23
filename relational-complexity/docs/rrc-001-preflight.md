# RRC-001 preflight

Measured on this machine before `plans/rrc-001.json` was frozen. The kernels are `calibration_weights` (every weight is `1 + ((state * 17 + edge * 13) % 5)`) or, for one propagation bundle, that rule against the unconstrained rule. No defect, exactness bit, closure size or stationary value from these runs is recorded. The output file `generated/preflight.json` is disposable and is not a result.

The bundle is the scientific item shape: interface lumpability, edge-count, parity and wedge-profile augmentations, lumpable closure, recurrent classes and the grammar classification. The propagation bundle is two parity-balanced solves (two starts each) and a dense solve when the state count is at most 1,024.

| N | States | Build (s) | One lumpability (s) | Closure (s) | Bundle (s) | Propagation bundle (s) |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 64 | 0.00007 | 0.0016 | 0.0017 | 0.009 | 0.006 |
| 5 | 1,024 | 0.0013 | 0.023 | 0.019 | 0.166 | 0.226 |
| 6 | 32,768 | 0.099 | 0.867 | 1.269 | 7.947 | 0.837 |

The N=4 and N=5 rows hide `N-1` nodes, so the interface is a star into one exterior node. A second N=6 timing used the heavier scientific shape, hiding only `{0,1,2}` (12 interface pairs, three augmentations, closure). Wall time 10.522 seconds. Still a calibration rule. The exactness bit was not read.

## Decision

Every planned item sits under the 120-second watchdog with a factor of about ten in the heaviest measured shape. N=6 stays in the round, including closure. N=7 is not opened: the GT prior at commit `38e92015` puts a fraction kernel there at 10–20 minutes, and this preflight did not remeasure it. Nothing is sampled.

Stationary iteration at N=6 converged on the calibration chain (the convergence bit is a solver check, not a relational finding). Dense solves stop at 1,024 states. N=6 propagation is two starts only.

Hard-wedge propagation is not in the round. A hard zero can make more than one recurrent class, so a single stationary law is not the right observable. The lumpability items still count recurrent classes.
