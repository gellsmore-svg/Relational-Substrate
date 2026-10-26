# atlas-016 preflight

Status: timing and a worker dry-run. `scientific` is false. Observables were not retained.

Eight `atlas_core` items. One carrier on vertices 0, 1, 2, 3, and 4. Edges `(0,1)`, `(1,2)`, and `(3,4)`. The first two edges share a vertex. The third edge is disjoint. Eight states. The item list was fixed before the timing call.

The empty list. Three matched pairs, each a prohibit and a multiply by 3 of the same event under the same present condition: `(1,2)` when `(0,1)` is present; `(0,1)` when `(3,4)` is present; `(3,4)` when `(0,1)` is present. One mixed list puts that incident prohibit and that disjoint multiply on one condition, `(0,1)`. Action `either`. Polarity present. Baseline 1. Grammar `opening-prohibit-multiply-v1`. No incident-count predicate. No form or dissolve.

The question is ATLAS-Q02: which changes are support changes, which are rate changes on a full support, and which are both. The round does not close it. The incident prohibit reads the second listed edge when the first is present. That is not the EQ-031 bit position. Atlas-006 stored count templates on two disjoint edges and on connected carriers. Atlas-009 stored factor-2 multiplies on the four-edge path. Atlas-012 stored factor-3 multiplies on the three-edge chain. Atlas-013 stored incident-count prohibits on the three-edge star. This carrier is none of those graphs.

Excluded: absent polarity, formation and dissolution, incident-count predicates, the three-edge star, the three-edge chain, two disjoint edges as the whole carrier, the four-edge path, factors other than 3, N=6, the EQ-031 bit-position prohibit, the atlas-012 length-2 lists, the atlas-015 overlap maps, successive quotients, and reruns of `results/atlas-006`, `results/atlas-009`, `results/atlas-012`, `results/atlas-013`, and `results/atlas-015`.

Heaviest call `A16-base`, 8 states, measured at 0.000781 seconds. A later pass was heaviest on `A16-mixed` at 0.000758 seconds. The plan records 0.002 seconds. The item list was not changed. Watchdog 120. Hard ceiling 300. Every timed call returned status complete. That status is a runner check, not a scientific result. No weight-table hash was retained.

The same eight items then passed through the real worker into a disposable directory. Receipt hashes matched result bytes. One completed item was removed and marked running. Resume recomputed that item and left the others in place. The first run completed 8 items in 1.303955 seconds. The resume completed 1 item in 0.161507 seconds. Verify printed `verified`, and the problem list was empty. Those files were discarded. `results/atlas-006`, `results/atlas-009`, `results/atlas-012`, `results/atlas-013`, and `results/atlas-015` were not opened.
