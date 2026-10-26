# atlas-010 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables from these runs were not retained.

Fifteen `composition_observation` items. The carriers are the triangle, the three-edge chain, and the four-cycle. The laws are the empty list and one multiply by 3. The maps are the canonical line graph, the carrier orbit, and, on the multiply only, the position-indexed line graph.

The heaviest call was `A10-cycle4-mul-line`, 16 states, measured at 0.001449 seconds. The plan records 0.002 seconds. The watchdog is 120 seconds. The hard ceiling is 300 seconds.

Every timed call returned status `complete`. That status is a runner check, not a scientific result. No hash was retained.

The same fifteen items were then passed through the real worker into a disposable directory. The receipt hashes matched the result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. The verify problem list was empty. Those files were discarded.

The baseline position-indexed map was not in the plan. Cover observations were not timed as cells. `results/atlas-008` was not opened.
