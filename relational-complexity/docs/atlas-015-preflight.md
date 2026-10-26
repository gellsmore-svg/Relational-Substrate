# atlas-015 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables were not retained.

Twenty `composition_observation` items. One three-edge chain, edges `(0,1)`, `(1,2)`, `(2,3)`, eight states. The block family is `[(0,1),(1,2)]` and `[(1,2),(2,3)]`. The blocks share `(1,2)`, and every carrier edge sits in a block. The family is an overlapping cover. It is not a partition.

Five laws. The empty list. A prohibit of the shared edge `(1,2)` when `(0,1)` is present. A prohibit of `(0,1)` when `(1,2)` is present. A multiply by 3 of `(1,2)` when `(2,3)` is present. A multiply by 3 of `(2,3)` when `(0,1)` is present. Those last two edges lie in different blocks. None of the four lists is an atlas-012 multiply. Four maps on every law: `active_intersection`, `realised_intersection`, `labelled_realised_blocks`, and `realised_overlap_count`. The item list was fixed before the timing call.

The question is ATLAS-Q14: which observations of a fixed block family depend only on the block definitions, and which change when a shared constituent is present or absent. The round does not close it. Atlas-011 observed covers under one multiply on a triangle and a four-cycle. Atlas-012 stored weight tables on this chain and no block family. Atlas-014 used a partial family on the four-cycle as one successive map. This round places the potential map and the realised maps on one chain cover, and separates a constraint on the shared edge from a constraint on an unshared edge.

The observables are the label partition, strong lumpability of that partition, and the weight table. No item declares a second map, so a further label stays undefined. The state space is eight states, enumerated exhaustively. After execution, items that share a constraint list can be compared by weight hash, and the kernel hash can be compared with the weight hash. The empty list may be the constant-1 three-edge table. Potential and realised maps are not assumed to be the same partition. A prohibit can change support while a multiply changes positive weights. Those comparisons are not a reason to drop a cell.

Excluded: the atlas-012 multiply list, the atlas-014 four-cycle overlap item, the path and triangle realised-overlap fixtures, a third block, a block family that changes over time, parity, incident-count thresholds, the three-edge star, N=6, and reruns of `results/atlas-012` and `results/atlas-014`.

Heaviest call `A15-base-active`, 8 states, measured at 0.000933 seconds. A later call on the written plan measured 0.001045 seconds. The plan records 0.002 seconds. The item list was not changed. Watchdog 120. Hard ceiling 300. Every timed call returned status complete. That status is a runner check, not a scientific result. No weight-table hash was retained.

The same twenty items then passed through the real worker into a disposable directory. Receipt hashes matched result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. The first run completed 20 items in 3.283861 seconds. The resume completed 1 item in 0.172573 seconds. A separate check of the stored files found an empty problem list. Those files were discarded. `results/atlas-012` and `results/atlas-014` were not opened.
