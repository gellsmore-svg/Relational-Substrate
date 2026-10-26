# atlas-012 observations

A map of one verified sample. Not a conclusion. Not an instruction to choose a polarity or a list length.

Plan hash `1dffac3ff30ff7d6a37fbe0df4c63e90b1988cf454a9d8a7a4ba746515de5185`. Definitions commit `040bfab`. Freeze `4eb1f14`. All 7 items completed in one invocation, 1.159164 seconds. Verify printed `verified`. The generated table is `reports/atlas-012.md`. Its Hash column is a 12-character prefix. The fractions below are the stored numerators and denominators. Engine `rrc-0.4.0`. Grammar `opening-prohibit-multiply-v1`. Occupation method `integer_pi_proportional_to_total_weight`. `results/atlas-009`, `results/atlas-010`, and `results/atlas-011` were not rerun.

Every cell has 8 states, 3 edges, 0 zero-cells, 24 positive transitions, and 1 recurrent class. The kernel hash equals the weight hash. The compilation gate reports current-state single-toggle weights and `new_primitive` false. The carrier is the path `(0,1)`, `(1,2)`, `(2,3)`. Bits 0, 1, and 2 are those edges. A subgraph of this path is a forest, so the stored component count is `4` minus the stored edge count on every cell. That is the same reason as the four-edge path identity, at this node count.

## Tables

The empty list is the EQ-015 table, hash `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`. Mean edges `3/2`. Marginal `1/2` on each edge.

`A12-pol-present` is the EQ-019 table, hash `7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9`. That is the atlas-010 three-edge multiply and `A6-chain-bit`. Mean edges `13/8`. Marginals `1/2`, `5/8`, `1/2`.

`A12-pol-absent` has hash `a30d2af41e1b65601390615151522d627502825abba5d36195739e051a798cff`. Mean edges `11/8`. Marginals `1/2`, `3/8`, `1/2`.

`A12-single-far` multiplies `(0,1)` when `(2,3)` is present. Hash `35818e425b302f38df5d28715a61ec5e21b1a765ab3ceee5f81ee55c40156e82`. Mean edges `13/8`. Marginals `1/2`, `1/2`, `5/8`.

`A12-single-other` multiplies `(2,3)` when `(1,2)` is present. Hash `f4b5f62c8045ae02a0e81f3fde6202933c166f3c92862e0348b0f3382b3945ad`. Mean edges `13/8`. Marginals `1/2`, `5/8`, `1/2`.

`A12-one-event` puts both guards on `(0,1)`. Hash `4689196251660b2458b053cf65ecf08d19ca17a2182ac10f8f040495d6ff2328`. Declared cardinality 2. Effective cardinality 2. Kernel-effective cardinality 2. Mean edges `11/6`. Marginals `1/2`, `2/3`, `2/3`.

`A12-two-event` puts one guard on `(0,1)` and one on `(2,3)`, both conditioned on `(1,2)`. Hash `f1e515bd6d9dba119ac4ea8833c34d628796fb62f07736ea6951c787b88bacc5`. Declared cardinality 2. Effective cardinality 2. Kernel-effective cardinality 2. Mean edges `17/10`. Marginals `1/2`, `7/10`, `1/2`.

The seven hashes are distinct. Each length-2 hash differs from each stored single and from the empty list.

## Bit relabeling of the singles

The stored absent matrix is the stored present matrix with each row moved by flipping bit 1. Columns 1 and 2 are the constant 1. Column 0 depends on bit 1. Flipping that bit exchanges the present guard and the absent guard, and the translation commutes with every toggle. The condition marginals are `5/8` and `3/8`. The other two marginals stay `1/2`. EQ-024 records that matrix identity. The designated polarity remains the instrument that names which side of the bit is the guard.

The stored other-end matrix is the stored present matrix after swapping bits 0 and 2. That permutation is the path reversal. EQ-025 records it. The hashes differ because the edge order is fixed.

Swapping bits 1 and 2 carries the present matrix onto the far matrix. That permutation exchanges the middle edge with an end edge. The automorphism group of this path is the identity and the reversal, so the far cell is a different placement on the carrier. The three singles share mean edges `13/8` because each of those maps preserves the edge count. The ordered marginals of the far cell are `1/2`, `1/2`, `5/8`.

## Length 2

The baseline is 1 and the composer multiplies matching factors. The stored one-event matrix is the elementwise product of the present matrix and the far matrix. The stored two-event matrix is the elementwise product of the present matrix and the other-end matrix. Effective cardinality 2 means neither factor is idle.

The two length-2 matrices differ. An enumeration of the 48 automorphisms of the 3-bit toggle graph finds no map from one onto the other, and none from either onto a stored single or onto the empty list. The separation is a property of these weight tables. It is not a renaming of the three bits.

The matched comparison holds factor, action, polarity, cardinality, and carrier fixed, and changes the event arrangement. A comparison of either length-2 cell with a polarity cell changes cardinality and arrangement together. That comparison is joint.

## What this sample does not say

It does not close ATLAS-Q03. One carrier, one factor, and one action leave the question open. Support, recurrence, and effective cardinality agree on the two length-2 cells. The integer tables and the ordered marginals differ. ATLAS-Q01 and ATLAS-Q04 were not in the round. Formation and dissolution were not cells. The atlas-009 factor-2 path was not rerun. Mean `13/8` is not mean `37/18`. Marginal `5/8` is not marginal `5/9`.

It does not schedule `13/8`, `5/8`, `3/8`, `11/6`, `2/3`, `17/10`, or `7/10`. It does not schedule the atlas-010 defects, the atlas-011 defects, PAT-012, or PAT-014. PAT-015 records the bit relabeling and the length-2 separation, with `schedules_follow_up` false.

## Restart

The plan and the preflight stay as frozen. A later round needs its own freeze.
