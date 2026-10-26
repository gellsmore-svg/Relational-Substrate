# atlas-018 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables were not retained.

Three `strict_event_comparison` items. Method `event-kernel-0.2.0`. Clock one declared event. Engine string `rrc-0.4.0`. The item list was fixed before the timing call.

The identified item is three bits with every toggle weight equal to 1. The free item is four bits with every toggle weight equal to 1, and it carries the map `(e0, e1, e2) → (e0, e1, e1, e2)` plus a copy of the identified catalogue. The coupled item uses the same map and the same reference. Its events toggle bit 0, toggle bit 3, and jointly flip bits 1 and 2. No occupation is requested. No horizon is requested.

The question is ATLAS-Q10. The round does not close it. ATLAS-Q15 is not the question of this round.

Excluded: the atlas-017 six cells, weights other than 1, the two-bit support constraint, a horizon, occupation, an intervention operator, N=6, form and dissolve, and reruns of `results/atlas-016` and `results/atlas-017`.

Heaviest call `A18-identified`, measured at 0.001014 seconds. The plan records 0.002 seconds. The item list was not changed. Watchdog 120. Hard ceiling 300. Every timed call returned status complete. That status is a runner check, not a scientific result. No probability row was retained.

The same three items then passed through the real worker into a disposable directory. Receipt hashes matched result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. The first run completed 3 items in 0.536091 seconds. The resume completed 1 item in 0.166337 seconds. Verify was not required for the problem list: the exercise problem list was empty. Those files were discarded. `results/atlas-017` was not opened.
