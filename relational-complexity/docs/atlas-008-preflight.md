# atlas-008 preflight

Status: timing only. `scientific` is false. Observables from these runs were not retained.

The item is `composition_observation` on an empty constraint list. Each of the fifteen carriers and label maps was timed. The clock was the wall time of `execute_composition_observation`. The definitions commit is `6778da8`. That commit fills a missing `round_id` from the plan. It does not change the weight compiler.

The heaviest call was `A8-path4-degree`, the four-edge path degree sequence, 16 states, measured at 0.000801 seconds. The plan records 0.001 seconds. The watchdog is 120 seconds. The hard ceiling is 300 seconds.

No constrained table was timed. The static line graph and the cover operators were not timed as cells. `results/atlas-007` was not opened.
