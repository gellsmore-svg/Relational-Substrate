# atlas-020 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables were not retained.

Four `atlas_core` items. Grammar `opening-prohibit-multiply-v1`. Engine string `rrc-0.4.0`. The item list was fixed before the timing call.

The carrier is edges `(0,1)` and `(1,2)` on N=4. Vertex 3 is isolated. The empty list is the control. The other three items are one prohibit of `(0,1)` when `(1,2)` is present, with action either, form, or dissolve. Baseline 1. No multiply. No event-kernel cell.

The question is ATLAS-Q04. The round does not close it. The atlas-002 form cells use other carriers. The atlas-016 edges are not this carrier.

Excluded: a multiply, absent polarity, the atlas-002 carriers, the atlas-016 edges, incident-count predicates, N=6, event-kernel cells, and reruns of `results/atlas-002` and `results/atlas-016`.

Heaviest call `A20-form`, measured at 0.000871 seconds. The plan records 0.002 seconds. The item list was not changed. Watchdog 120. Hard ceiling 300. Every timed call returned status complete. That status is a runner check, not a scientific result. No weight table was retained.

The same four items then passed through the real worker into a disposable directory. Receipt hashes matched result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. The first run completed 4 items in 0.668173 seconds. The resume completed 1 item in 0.172512 seconds. The exercise problem list was empty. Those files were discarded. `results/atlas-016` was not opened.
