# atlas-017 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables were not retained.

Six `event_kernel` items. Method `event-kernel-0.1.0`. Clock one declared event. Engine string `rrc-0.4.0`. The item list was fixed before the timing call.

The control is the two-bit catalogue with every toggle weight equal to 1. That catalogue is also the free product of two copy toggles, so the free product is not a second cell. The joint cell uses the same four states and names, from each state, a toggle of bit 0 and a joint step by xor 3. The identified cell is one bit, toggled both ways. The coupled cell names only the joint step between states 0 and 3. States 1 and 2 of that cell have no event. The declared image sends identified state 0 to duplicated state 0 and identified state 1 to duplicated state 3. The halt cell is one state and an empty event list. The noop cell is that state with one noop of weight 1. No item adds a coordinate. No carrier weight table is compiled. No stationary distribution is requested.

The question is ATLAS-Q06: which of these catalogues fail the one-step single-toggle compilation gate, and what coordinate they would add. The round does not close it. ATLAS-Q15 is not the question of this round.

Excluded: a second cell for the free product, the three-state summed-target witness, carrier weight tables, occupation, stationary means, the atlas-016 carriers, the atlas-016 bit swap, EQ-027, a changing block family, successive quotients, an intervention operator, N=6, prohibit and multiply constraints, and reruns of `results/atlas-012`, `results/atlas-015`, and `results/atlas-016`.

Heaviest call `A17-g0`, 4 states, measured at 0.000154 seconds. The plan records 0.002 seconds. The item list was not changed. Watchdog 120. Hard ceiling 300. Every timed call returned status complete. That status is a runner check, not a scientific result. No probability row was retained.

The same six items then passed through the real worker into a disposable directory. Receipt hashes matched result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. The first run completed 6 items in 0.947979 seconds. The resume completed 1 item in 0.163956 seconds. Verify printed `verified`, and the problem list was empty. Those files were discarded. `results/atlas-012`, `results/atlas-015`, and `results/atlas-016` were not opened.
