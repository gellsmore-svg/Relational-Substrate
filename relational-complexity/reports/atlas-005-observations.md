# atlas-005 observations

A map of one verified generator. Not a conclusion. Not an instruction to investigate any row next.

Plan hash `2ab849ad8e43bd643685feea729533fcb3815d6f898a58aa19e236da57142f45`. All 12 items completed. The report table is `reports/atlas-005.md`. Engine `rrc-0.3.0`. The grammar is the opening composer. No incident predicate is in the plan.

The 12 lists are one menu of eight templates. State enumeration inside each cell is exhaustive. The sample is not every list of these lengths, and the three carriers are not every graph on three or five nodes. Shapes are 8 by 3, 16 by 4, and 32 by 5. A hash is compared only inside one shape.

Form and dissolve constraints make the integer occupation shortcut inapplicable. Where the stationary law is unique for those lists, the method is `stationary_balanced` and the stored means are float64. Those means are not quoted. Integer means below are the baseline fractions.

## Controls

`A5-N3-base` reproduces the 3-edge baseline. EQ-015. Hash `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`. Mean present edges 3/2. Mean components 13/8. Structure hash `ff349bdce93ed13b62f03679c99fd48833989b4355d70f562056f7d3fa4f1447`, the same carrier record as atlas-003.

`A5-P5-base` is the constant-1 table on four edges. EQ-016. It matches `A2-cycle-base` and `A4-cycle-base`, hash `5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3`. Mean present edges 2/1 on the chain and on the cycle. Mean components are 3/1 on the 5-node chain and 33/16 on the 4-cycle. The chain is a forest, so the component count is five minus the number of present edges, and the baseline marginal 1/2 gives mean components 3. The cycle is not a forest. Structure hashes differ: chain `84db59d996c291bfe5bafa71dbabc7abd162bee5c450306dfad834b498c10598`, 4-cycle `5747f684d10b1fc3f48c38b0a9b4176e5c1aa137469d113d0caa3126c12f7a51`.

The 5-node cycle baseline is a new table, hash `e8f5b72f4904e93a3666620d0e0e0578a318860207da155ec5a77842d05f7ccb`. Five edges. Mean present edges 5/2. Mean components 81/32. Structure hash `03dc4396f64c4cecad187d849a0da7aca48983941a72f7b73344398ab07e29f5`.

## Same declared length on different carriers

Declared cardinality, effective cardinality, and kernel-effective cardinality were computed separately. On these 12 cells the effective count equals the kernel-effective count, and the removal-sensitive count equals the kernel-removal count. That agreement is not ATLAS-Q08. Five cells have a kernel hash different from their own weight hash, so some positive row has gcd greater than 1, and removing a constraint still moves the table and the kernel together.

| Item | Edges | Declared | Effective | Positive | Zero | Classes | Deadlocks | Kernel equals weight |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A5-N3-card5 | 3 | 5 | 5 | 19 | 5 | 1 | 0 | yes |
| A5-N3-card12 | 3 | 12 | 9 | 10 | 14 | 2 | 1 | no |
| A5-P5-card5 | 4 | 5 | 5 | 52 | 12 | 1 | 0 | yes |
| A5-P5-card9 | 4 | 9 | 9 | 38 | 26 | 2 | 0 | no |
| A5-P5-card10 | 4 | 10 | 10 | 38 | 26 | 2 | 0 | no |
| A5-P5-card12 | 4 | 12 | 12 | 37 | 27 | 2 | 0 | no |
| A5-C5-card5 | 5 | 5 | 5 | 136 | 24 | 1 | 0 | yes |
| A5-C5-card9 | 5 | 9 | 9 | 104 | 56 | 1 | 0 | yes |
| A5-C5-card12 | 5 | 12 | 12 | 96 | 64 | 1 | 0 | no |

PAT-008. Length 12 has effective cardinality 9 on the 3-edge carrier and 12 on the 4-edge chain and the 5-edge cycle. The list bookkeeping is part of the generator: length 12 names 3, 4, or 5 distinct events, and the maximum number of constraints on one event is 4, 3, or 3. Those counts are properties of the list. The effective-cardinality gap is a property of the weight table.

PAT-009. Length 9 has two recurrent classes on the chain and one on the cycle. Both cells have effective cardinality 9. `schedules_follow_up` is false on both patterns.

`A5-P5-card9` and `A5-P5-card10` share the support counts 38 and 26 and do not share a hash. The support count does not identify the table. Length 12 on that chain is 37 and 27, so the eleventh and twelfth constraints, which ablation counts as effective, change the support as well as the integers.

The only deadlock in the round is `A5-N3-card12`, one deadlock and two recurrent classes. These lists are designated-edge rules. EQ-014 does not apply to them.

No two items share a weight hash or a kernel hash.

## Syntax flag

Every non-empty list stores `has_cycle` true. The longest simple dependency path is 2 edges on the complete carrier, 3 on the chain, and 4 on the cycle. The flag occurs with one recurrent class, including `A5-C5-card12`, and with two recurrent classes, including `A5-N3-card12`. That is the split already recorded as PAT-006. The flag remains rule text. This note does not widen PAT-006 into a law.

## What stays open

ATLAS-Q01 through ATLAS-Q12 stay open. The round shows one generator on which a longer list is redundant on three edges and not redundant on four or five edges. It does not say when a constraint is redundant. Complete N=5 was not run. Incident predicates, count predicates, history, hyperedges, and composition were not in the plan. Nothing in these cells appoints the next round.
