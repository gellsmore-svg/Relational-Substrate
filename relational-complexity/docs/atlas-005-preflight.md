# atlas-005 preflight

Measured on this machine before `plans/atlas-005.json` was frozen. Each timed call was one `atlas_core` item with the common core and the tolerances in the plan. The heaviest call was the 5-node cycle, five edges, 32 states, 12 constraints. Wall time 0.857 seconds. The measured call was 0.856875 seconds.

The other eleven calls were timed only to find that maximum. The next heaviest was the 5-node chain with 12 constraints, 16 states, at 0.408 seconds. The N=3 complete carrier with 12 constraints, 8 states, took 0.202 seconds. Empty lists took under 0.001 seconds.

Every call returned status `complete`. That word here means the engine's internal class counts agreed. It is not a scientific observation. No weight hash, kernel hash, class count, occupation, support count, or other observable was retained. `scientific` is false.

State enumeration inside a cell is exhaustive. Ablation at 12 constraints stays under the cap of 16. The 12 lists are one generator, not every list. The 120-second watchdog is far above this shape. Complete N=5 was not timed and is not in this round.
