# Cross-atlas index

A reading of records that already exist. Not a conclusion. Not a queue.

Rounds in view: RRC-001 (`rrc-0.1.0`), atlas-001 and atlas-002 (`rrc-0.2.0`), atlas-003 and atlas-004 (`rrc-0.3.0`). Hashes are compared only when the integer tables have the same shape and the same declared edge order, or when a row states the bit rule that makes two shapes match. RRC-001 items are not `atlas_core` weight tables. Their lumpability numbers are not compared with these hashes.

## Weight tables

EQ-001 to EQ-003 are identities of the opening composer. They predate the type field.

EQ-004 and EQ-005 are atlas-001 cells whose lists differ and whose tables do not. EQ-006 and EQ-007 are the chain, the branch, and the N=3 bit rule. EQ-009 and EQ-011 are the same opening lists under `rrc-0.3.0`. EQ-010 is a dissolve prohibit sitting inside an either-prohibit. EQ-012 is an empty incident neighbourhood. EQ-013 is a one-neighbour incident rule that reads a single bit.

Equal hashes are equal integer tables in the declared order. They are not equal node sets. EQ-007 and EQ-013 record component means that differ because N differs.

## Kernels

EQ-008 is the method identity: baseline 1 and baseline 2, same kernel, different integers, under `halt_self_loop`. It is not a cell.

In atlas-003 and atlas-004, no two items shared a kernel without also sharing the integer table. Weight ablation and kernel ablation agreed on every cell of both rounds. A kernel hash that differs from its own weight hash means some positive row has gcd greater than 1. That is not an equivalence between two specifications.

ATLAS-Q08 stays open. No continuous-time rate was computed. Agreement under `halt_self_loop` is not agreement under every clock.

## Incident count

EQ-017 is a method identity of `rrc-0.4.0`. `ge 1` matches `incident_neighbour` present, and `eq 0` matches absent, including an empty neighbourhood. `eq 1` and `ge 2` differ from `ge 1` when a neighbourhood has two or more edges. The check is `tests/test_count.py`. No scientific cell uses the count. A common-neighbour count is not this predicate.

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

## Regions not in the comparison

Complete N=5. Cardinalities other than the atlas-005 lengths, and every list the generator did not write. Absent-polarity incident rules. Count predicates other than the compiler identities in EQ-017. No count cell. History. Independent hyperedges. A search over graph isomorphism. Any clock other than `halt_self_loop`. A composition cell.

## Composition

`docs/composition-taxonomy.md` formulates C1 through C8 and keeps dependency, reach, composition, and recursion as four readings. `IDEA-L01`, `IDEA-L04`, `IDEA-L06`, `IDEA-L08`, `IDEA-L09`, `IDEA-L11`, `IDEA-L13`, and `IDEA-L14` stay `open`. `IDEA-L15`, `IDEA-L16`, and `IDEA-L17` are the new open rows. `COV-COMPOSITION` and `COV-COMPOSITION-LIBRARY` stay `open`. No composition cell was run. A named map, with its defect or its failure, is not yet frozen. Overlap is not stored as a tree. RRC-001's two-subset cut is not reopened as the definition of composition. The static line-graph operator is recorded as a unary operation on simple graphs. EQ-014 is not rerun and is not that operator's dynamics.

ATLAS-Q01 through ATLAS-Q12 stay open. ATLAS-Q12 asks which named operators accept their own output. It is not scheduled.
