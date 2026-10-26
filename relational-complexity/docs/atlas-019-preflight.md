# atlas-019 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables were not retained.

Three `event_horizon` items. Method `event-kernel-0.2.0`. Clock one declared event. Horizon 2. Initial state 0. Engine string `rrc-0.4.0`. The item list was fixed before the timing call.

The free item toggles each of four bits. The coupled item toggles bit 0 and bit 3 and jointly flips bits 1 and 2. The frozen-copy item toggles only bit 0 and bit 3. The label is 1 when bit 1 equals bit 2. The subset is those states. The laws are written in this plan. They are not read from another round. No intervention operator is defined. No stationary distribution is requested.

The question is ATLAS-Q13. The round does not close it. One partition is not a two-stage quotient.

Excluded: reading `results/atlas-018`, weights other than 1, a horizon other than 2, occupation, a stationary distribution, an intervention operator, a second label map, N=6, and a rerun of `results/atlas-017`.

Heaviest call `A19-free`, measured at 0.000960 seconds. The plan records 0.002 seconds. The item list was not changed. Watchdog 120. Hard ceiling 300. Every timed call returned status complete. That status is a runner check, not a scientific result. No probability row was retained.

The same three items then passed through the real worker into a disposable directory. Receipt hashes matched result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. The first run completed 3 items in 0.491817 seconds. The resume completed 1 item in 0.175904 seconds. The exercise problem list was empty. Those files were discarded. `results/atlas-017` and `results/atlas-018` were not opened.
