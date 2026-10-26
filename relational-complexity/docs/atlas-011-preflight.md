# atlas-011 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables from these runs were not retained.

Seventeen `composition_observation` items. The triangle carries three singleton blocks, one overlapping cover, and three partial covers. The four-cycle carries the opposite-edge cover. The laws are the empty list and one multiply by 3.

The heaviest call was `A11-cyc-opp-mul-active`, 16 states, measured at 0.001236 seconds. The plan records 0.002 seconds. The watchdog is 120 seconds. The hard ceiling is 300 seconds.

Every timed call returned status `complete`. That status is a runner check, not a scientific result. No hash was retained.

The same seventeen items were then passed through the real worker into a disposable directory. The receipt hashes matched the result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. A separate worker pass verified with an empty problem list. Those files were discarded.

The four-edge path was not in the plan. The path-fixture bit covers were not timed. `results/atlas-008` and `results/atlas-010` were not opened.
