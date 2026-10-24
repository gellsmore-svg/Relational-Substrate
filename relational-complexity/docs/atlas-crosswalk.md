# Cross-atlas index

A reading of records that already exist. Not a conclusion. Not a queue.

Rounds in view: RRC-001 (`rrc-0.1.0`), atlas-001 and atlas-002 (`rrc-0.2.0`), atlas-003, atlas-004, and atlas-005 (`rrc-0.3.0`), atlas-006 (`rrc-0.4.0`). Hashes are compared only when the integer tables have the same shape and the same declared edge order, or when a row states the bit rule that makes two shapes match. RRC-001 items are not `atlas_core` weight tables. Their lumpability numbers are not compared with these hashes.

## Weight tables

EQ-001 to EQ-003 are identities of the opening composer. They predate the type field.

EQ-004 and EQ-005 are atlas-001 cells whose lists differ and whose tables do not. EQ-006 and EQ-007 are the chain, the branch, and the N=3 bit rule. EQ-009 and EQ-011 are the same opening lists under `rrc-0.3.0`. EQ-010 is a dissolve prohibit sitting inside an either-prohibit. EQ-012 is an empty incident neighbourhood. EQ-013 is a one-neighbour incident rule that reads a single bit.

Equal hashes are equal integer tables in the declared order. They are not equal node sets. EQ-007 and EQ-013 record component means that differ because N differs.

## Kernels

EQ-008 is the method identity: baseline 1 and baseline 2, same kernel, different integers, under `halt_self_loop`. It is not a cell.

In atlas-003 and atlas-004, no two items shared a kernel without also sharing the integer table. Weight ablation and kernel ablation agreed on every cell of both rounds. A kernel hash that differs from its own weight hash means some positive row has gcd greater than 1. That is not an equivalence between two specifications.

ATLAS-Q08 stays open. No continuous-time rate was computed. Agreement under `halt_self_loop` is not agreement under every clock.

## Incident count

EQ-017 is a method identity of `rrc-0.4.0`. `ge 1` matches `incident_neighbour` present, and `eq 0` matches absent, including an empty neighbourhood. `eq 1` and `ge 2` differ from `ge 1` when a neighbourhood has two or more edges. The check is `tests/test_count.py`. Atlas-006 later used uniform `eq 1` and `ge 2` multiplies. Other count relations, and a common-neighbour count, have no cell. A common-neighbour count is not this predicate.

EQ-020 is the uniform `ge 2` cardinality identity. One multiply on every edge, factor at least 2, no other constraint. Weight-effective cardinality equals the number of edges with at least two incident carrier edges. Kernel-effective cardinality equals that number for `either` and for `form`. For `dissolve` it does too, except on a triangle and on a three-edge star, where the kernel is the baseline kernel and the integer table is not. A duplicate multiply, and a prohibit on the same guard, leave the family. The argument is `docs/incident-count-cardinality.md`. Atlas-006 was not rerun. The identity is not the next round.

## Relabelling

No frozen cell declares a node permutation. Hash equality without that mapping is not relabelling equivalence. IDEA-E03 and `COV-RELABEL` stay open.

The path-reversal check in `tests/test_kernel.py` is a compiler identity for one uniform template. The atlas-004 endpoint and middle-edge cells are designated instruments. They differ. That is not a covariance theorem.

## Contrasts

PAT-001 through PAT-007 are recorded. `schedules_follow_up` is false on each.

The designated-bit rules do not separate the atlas-002 chain from the atlas-002 branch. The incident-neighbour templates do. PAT-007. The structure hash stored on `rrc-0.3.0` results also differs for those carriers. Atlas-002 results were not rewritten to insert it. ATLAS-Q07 stays open.

An imposed syntax cycle occurs with one recurrent class and with more than one. PAT-006, and the same split on the incident templates. The flag is rule text.

In atlas-003 the two-event cell and the factor-4 cell share mean edges 5/3 and mean components 3/2 and do not share a hash. Those means do not identify the table.

## Line-graph total domination

For one rule, the uniform present-polarity incident prohibit on every edge, a state is a deadlock exactly when the present edges are a total dominating set of the carrier's line graph. The argument and the counterconditions are in `docs/line-graph-domination.md`. EQ-014. The atlas-004 deadlock counts agree. Recurrent classes on the three-edge chain outnumber those deadlocks. The identity is not a reason to centre the next round on domination.

## atlas-005

One generator, twelve lists, three carriers. State spaces have 8, 16 and 32 states, so weight hashes are compared only inside a shared shape.

EQ-015: `A5-N3-base` reproduces the 3-edge baseline hash `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`. Mean edges 3/2. Mean components 13/8.

EQ-016: `A5-P5-base`, the 5-node chain, matches the 4-cycle baseline hash `5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3`. Both are the constant-1 table on four edges. Mean edges 2/1 on both. Mean components are 3/1 on the chain and 33/16 on the cycle. The structure hashes differ.

PAT-008: length 12 of this generator has effective cardinality 9 on three edges and 12 on four edges and on five edges. PAT-009: length 9 has two recurrent classes on the chain and one on the cycle. `schedules_follow_up` is false on both. No two lists in the round share a weight hash or a kernel hash. Weight ablation and kernel ablation agreed on all 12 cells. ATLAS-Q01, ATLAS-Q05 and ATLAS-Q08 stay open.

## atlas-006

Fifteen cells. Five carriers, one designated-bit multiply by 3, and uniform `eq 1` and `ge 2` multiplies by 3. `ge 1` was not rerun.

EQ-018: `A6-disc-eq1` and `A6-disc-ge2` match the disconnected baseline hash `7d68b5c4119211a50d84f89b7f843e9ae6da04183d69ba4b542b04aeb2280273`. Mean edges 1/1. Mean components 3/1. Each neighbourhood is empty. The bit instrument on that carrier has a different hash.

EQ-019: `A6-chain-bit` and `A6-branch-bit` match `A4-chain-end-mul` and `A3-03-mul-present-3`, hash `7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9`. Mean edges 13/8. Mean components 19/8 on the chain and the branch, and 49/32 on the N=3 cell. The structure hashes differ.

PAT-010: the `eq 1` template and the `ge 2` template each give different hashes on the three-edge chain and the three-edge branch. The bit instruments share a hash. PAT-011: on the five `ge 2` lists, effective cardinality equals the number of edges with at least two incident neighbours. `schedules_follow_up` is false on both. All 15 cells have one recurrent class and no deadlock. Four cells have a kernel hash different from their weight hash. Weight ablation and kernel ablation agreed on all 15. ATLAS-Q09 and ATLAS-Q08 stay open. EQ-014 does not apply.

## Regions not in the comparison

Complete N=5. Cardinalities other than the atlas-005 lengths, and every list the generator did not write. Absent-polarity incident rules. Count thresholds other than the atlas-006 `eq 1` and `ge 2` templates. Common-neighbour counts. History. Independent hyperedges. A search over graph isomorphism. Any clock other than `halt_self_loop`. A composition cell.

## Composition

`docs/composition-taxonomy.md` formulates C1 through C8 and keeps dependency, reach, composition, and recursion as four readings. `IDEA-L01`, `IDEA-L04`, `IDEA-L06`, `IDEA-L09`, `IDEA-L11`, `IDEA-L15`, and `IDEA-L17` stay `open`. `IDEA-L08`, `IDEA-L13`, `IDEA-L14`, and `IDEA-L16` are `partial`. The line graph, the intersection graph, and the nerve are implemented, and those operators are not frozen cells. `COV-COMPOSITION` and `COV-COMPOSITION-LIBRARY` stay `open`. Atlas-007 froze fifteen baseline label maps. Every item failed before a weight table was stored. That failure is not a lumpability result. Overlap is not stored as a tree. RRC-001's two-subset cut is not reopened as the definition of composition. The static line-graph operator is a unary operation on simple graphs. Its specification is `docs/composition-operators.md`. EQ-014 is not rerun and is not that operator's dynamics.

Atlas-008 stored the fifteen maps. Verify printed `verified`. The three-edge weight hash is the EQ-015 baseline `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`. The four-edge weight hash is the EQ-016 baseline `5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3`. On each carrier the kernel hash equals the weight hash, and the structure hash matches the earlier baseline cell with the same edge list. Those shared tables do not share the observation laws. Present edge count is exact on all five carriers. EQ-021 is the reason: under an empty list and a constant positive baseline, the next count depends only on the current count. On the triangle and the three-edge star the other two maps induce the same partition as the count, so they are exact there too. On the three-edge chain the line graph and the degree sequence share a partition that is not the count, with defect `4/9` and five labels. On the four-edge path the three partitions differ. The degree sequence and the line graph both have defect `1/3`, with seven and eight labels. On the four-cycle the degree sequence is exact, with six labels, and the line graph has defect `1/2`, with eight labels. No map is injective. No map adds state. A further label is undefined. The equal path defects are not an identity of the two maps. The chain partition agreement is that carrier. The four-cycle split is not scheduled. ATLAS-Q10 stays open. The detail is `reports/atlas-008-observations.md`.

ATLAS-Q01 through ATLAS-Q12 stay open. ATLAS-Q12 asks which named operators accept their own output. It is not scheduled.

Atlas-009 verified 16 of 16 on one four-edge path. The baseline hash is the EQ-016 table. The twelve factor-2 present multiplies have twelve weight hashes and one mean, `37/18`. Cells with the same condition edge share the four edge marginals and not the weight hash. The three cardinality-2 instruments have three further hashes. The path and mutual instruments share marginals `11/20`, `11/20`, `1/2`, `1/2` and not the weight hash. Their `has_cycle` flags are the imposed rule text. A comparison of cardinality 1 with cardinality 2 is joint. The detail is `reports/atlas-009-observations.md`. ATLAS-Q01 stays open. PAT-012 has `schedules_follow_up` false.

The line-graph label in the atlas-008 paragraph is the position-indexed bare line graph. `docs/representations.md` separates that map from the canonical unlabelled line graph and from the carrier-orbit label. Atlas-010 verified 15 of 15. The label is a function of the present edges. On the triangle the canonical line graph, the carrier orbit, and the position-indexed line graph are one partition. It is exact under the empty list and has defect `4/9` under one multiply by 3. On the three-edge chain the position-indexed map and the canonical map are one partition, and the orbit is another. The empty-list orbit is exact. The multiply orbit is not. On the four-cycle the canonical map and the orbit are one exact partition of six labels under the empty list. `A8-cycle4-line` remains the position-indexed cell on that hash, eight labels, defect `1/2`. The triangle and the chain share the EQ-015 empty list and share the multiply hash `7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9`, which is the `A6-chain-bit` table. They do not share the observation laws. A carrier comparison is joint with the designated pair `(0,1)` conditioned on `(1,2)`. No map adds state. The detail is `reports/atlas-010-observations.md`. ATLAS-Q10 stays open. PAT-013 has `schedules_follow_up` false. EQ-022 and EQ-023 stay method identities.
