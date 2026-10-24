# atlas-006 observations

A map of one verified menu. Not a conclusion. Not an instruction to investigate any row next.

Plan hash `9b551e3e24afb1bdf21c243f52e6a08cb4d287880ce14553d92170cd2ee3cdcb`. All 15 items completed. The report table is `reports/atlas-006.md`. Engine `rrc-0.4.0`. Each carrier has one designated-bit multiply by 3 and two uniform `incident_count` multiplies by 3, `eq 1` and `ge 2`. `ge 1` and `eq 0` are absent from the plan. EQ-017 already identifies them with the Boolean incident polarities.

State enumeration inside each cell is exhaustive. The menu is not every threshold and the five carriers are not every graph. Shapes are 8 by 3, 4 by 2, 16 by 4, and 32 by 5. A hash is compared only inside one shape.

Every action is `either`. Every cell has one recurrent class, no deadlock, a full support, and `empirical_bit_independent` true. The occupation method on every cell is `integer_pi_proportional_to_total_weight`. The means below are those integer fractions.

## Bit instruments

`A6-chain-bit` and `A6-branch-bit` are one integer table. EQ-019. Hash `7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9`. It is also the hash of `A4-chain-end-mul` and `A3-03-mul-present-3`. Mean present edges 13/8 on the chain, the branch, and the N=3 cell. Mean components are 19/8 on the chain and the branch, and 49/32 on the N=3 cell. Structure hashes differ: chain `e6f7386ece69cd8888eca2be7cbc621dc46a80b61c6ddebb9f0a18abfceea8cc`, branch `6c959c90bc45976a55a7d874b0e0e4a6c4c31cf14f231e39417136e5ddf1e1d1`.

The bit rule names the first listed edge and the second. On the chain the second edge is the only neighbour of the first, so the instrument matches the stored endpoint incident multiply. The branch listing has a different third edge. The bit rule does not read it.

`A6-disc-bit` is a different table, hash `8235855a769efbbae3d89067143567df057a419b792248d4d7f3aa2da7944e09`. Mean edges 7/6. Mean components 17/6. The two edges share no vertex. The designated bit still changes the weights.

`A6-path5-bit` hash `c7f6b804ebe70d93942121c4df693dd9ff27cd3c33b03c799eeb1d2aa1860aa7`. Mean edges 21/10. Mean components 29/10. `A6-cycle5-bit` hash `19fafa9f27b5c6bed66338346c07ec757b74718c04ec99222976dfda2be128c7`. Mean edges 31/12. Mean components 157/64. These two bit instruments do not share a hash. Their shapes differ, 16 by 4 and 32 by 5.

## Count templates

`A6-disc-eq1` and `A6-disc-ge2` are the constant-1 table on two edges. EQ-018. Hash `7d68b5c4119211a50d84f89b7f843e9ae6da04183d69ba4b542b04aeb2280273`, the disconnected baseline. Mean edges 1/1. Mean components 3/1. Each event has incident-neighbourhood size 0, so `expansion_j` is 0 on both constraints. Declared cardinality 2. Effective cardinality 0. The designated-bit instrument on the same carrier is the different hash above.

On the other four carriers the two templates have different hashes from each other and from the bit instrument.

| Item | Edges | Declared | Effective | Expansion J | Classes | Deadlocks | Kernel equals weight | Mean edges | Mean components |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A6-chain-eq1 | 3 | 3 | 3 | 4 | 1 | 0 | no | 5/3 | 7/3 |
| A6-chain-ge2 | 3 | 3 | 1 | 1 | 1 | 0 | yes | 23/14 | 33/14 |
| A6-branch-eq1 | 3 | 3 | 3 | 6 | 1 | 0 | yes | 3/2 | 5/2 |
| A6-branch-ge2 | 3 | 3 | 3 | 3 | 1 | 0 | no | 11/6 | 13/6 |
| A6-path5-eq1 | 4 | 4 | 4 | 6 | 1 | 0 | no | 17/8 | 23/8 |
| A6-path5-ge2 | 4 | 4 | 2 | 2 | 1 | 0 | yes | 11/5 | 14/5 |
| A6-cycle5-eq1 | 5 | 5 | 5 | 10 | 1 | 0 | yes | 5/2 | 161/64 |
| A6-cycle5-ge2 | 5 | 5 | 5 | 5 | 1 | 0 | no | 17/6 | 107/48 |

Kernel-effective cardinality equals effective cardinality on all 15 cells, and the kernel-removal count equals the removal-sensitive count. That agreement is not ATLAS-Q08. Four cells have a kernel hash different from their own weight hash: `A6-chain-eq1`, `A6-branch-ge2`, `A6-path5-eq1`, and `A6-cycle5-ge2`. Support is full on every cell, so the split is a row gcd above 1.

`A6-cycle5-eq1` has mean edges 5/2, the same fraction as the atlas-005 cycle baseline, and a different hash. Mean components are 161/64 on this cell and 81/32 on that baseline.

## Neighbourhood width and the ge-2 lists

The stored features already give `expansion_j` per constraint. For `ge 2`, an edge with fewer than two incident edges has `expansion_j` 0. On the three-edge chain the two ends are 0 and the middle edge is 1. Effective cardinality is 1. On the five-node chain the two ends are 0 and the two middle edges are 1 each. Effective cardinality is 2. On the branch and the five-node cycle every edge has neighbourhood size 2 and `expansion_j` 1, and effective cardinality equals the declared length. On two disjoint edges both expansions are 0 and effective cardinality is 0. PAT-011. Kernel-effective agrees. The round has no second `ge 2` constraint on an edge that can already meet the threshold, so it does not show whether a wide edge can be redundant.

## Chain and branch under the two templates

`A6-chain-eq1` hash `f72239651823600e4f856c64609c1be03f78301a877fea521a4933044c78f32d`. `A6-branch-eq1` hash `d8d45d4524bb5b541e2031d42038e296cb9802235bb9f53543f8388e59a4cb30`. `A6-chain-ge2` hash `807be7e941aa5edc9e24dcb4e30544c49bafb11f17e7995eb1a7ea5578be149b`. `A6-branch-ge2` hash `41ad64444b33b6bc58eff4144721ad322649c5495ae7b7e2ea47ebf4eba02382`. PAT-010. The bit instruments on those two carriers share a hash. The count templates do not. `schedules_follow_up` is false. ATLAS-Q09 stays open.

Every uniform template on a carrier with an incident edge has `imposed_rule_dependency.has_cycle` true. The disconnected templates have the flag false, because an empty neighbourhood adds no arc. The bit instruments have the flag false and a syntax path of one edge. The flag is rule text. It sits beside one recurrent class on every cell in the round. PAT-006 already records that pairing for another menu. That row is unchanged.

No cell in this round is a uniform present-polarity incident prohibit. EQ-014 does not apply.
