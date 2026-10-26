# atlas-006 preflight

Measured on this machine before `plans/atlas-006.json` was frozen. Each timed call was one `atlas_core` item with the common core and the tolerances in the plan. The heaviest call was the 5-node cycle with five uniform `eq 1` multiplies, 32 states. Wall time 0.007 seconds. The measured call was 0.007215 seconds.

The other fourteen calls were timed only to find that maximum. The 5-node cycle with five `ge 2` multiplies took 0.007 seconds. The three-edge carriers took under 0.002 seconds.

Every call returned status `complete`. That word here means the engine's internal class counts agreed. It is not a scientific observation. No weight hash, kernel hash, class count, occupation, support count, or other observable was retained. `scientific` is false.

State enumeration inside a cell is exhaustive. Ablation at five constraints stays under the cap of 16. The fifteen lists are one matched menu, not every count. `ge 1` was not timed. The 120-second watchdog is far above this shape.
