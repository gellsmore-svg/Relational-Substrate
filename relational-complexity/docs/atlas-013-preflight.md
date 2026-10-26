# atlas-013 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables from these runs were not retained.

Five `atlas_core` items. One three-edge star. The lists are the empty baseline, uniform incident-count prohibits at `eq 1`, `eq 2`, and `ge 2`, and one `eq 2` prohibit on the first edge.

The heaviest item call on these five lists was `A13-eq2`, 8 states, measured at 0.001593 seconds. The plan records 0.002 seconds. The pass of the final plan stayed under that ceiling. The watchdog is 120 seconds. The hard ceiling is 300 seconds.

Every timed call returned status `complete`. That status is a runner check, not a scientific result. No hash was retained.

The same five items were then passed through the real worker into a disposable directory. The receipt hashes matched the result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. A separate worker pass verified with an empty problem list. Those files were discarded.

`results/atlas-006` and `results/atlas-012` were not opened.
