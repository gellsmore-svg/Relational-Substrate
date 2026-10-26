# atlas-012 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables from these runs were not retained.

Seven `atlas_core` items. One three-edge chain. The lists are the empty baseline, a present/absent pair at factor 3, two further single multiplies, two guards on one event, and two events sharing a condition.

The heaviest call was `A12-base`, 8 states, measured at 0.000809 seconds. The plan records 0.001 seconds. The first call carries the import overhead. The watchdog is 120 seconds. The hard ceiling is 300 seconds.

Every timed call returned status `complete`. That status is a runner check, not a scientific result. No hash was retained.

The same seven items were then passed through the real worker into a disposable directory. The receipt hashes matched the result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. A separate worker pass verified with an empty problem list. Those files were discarded.

The atlas-009 factor-2 grid was not in the plan. `results/atlas-009` was not opened.
