# atlas-014 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables from these runs were not retained.

Eight `successive_observation` items. One four-cycle. The laws are the empty list and one prohibit of `(0,1)` when `(2,3)` is present. Each item names two maps.

The heaviest item call on these eight lists was `A14-pro-injective-degree`, 16 states, measured at 0.003644 seconds. The plan records 0.004 seconds. A later call on the final plan measured 0.003583 seconds and stayed under that ceiling. The watchdog is 120 seconds. The hard ceiling is 300 seconds.

Every timed call returned status `complete`. That status is a runner check, not a scientific result. No hash was retained.

The same eight items were then passed through the real worker into a disposable directory. The receipt hashes matched the result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. A separate check of the stored files found an empty problem list. Those files were discarded.

`results/atlas-008`, `results/atlas-010`, and `results/atlas-013` were not opened.
