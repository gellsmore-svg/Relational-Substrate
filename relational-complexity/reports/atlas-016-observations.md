# atlas-016 observations

A map of one verified sample. The question stays open.

Plan hash `d933e17efe85ea998c3a81229e4bd3436d02a7cd42ccdb7d6d73d20e40688c1d`. Definitions commit `72ee4e5`. Freeze `269a0dd`. All 8 items completed in one invocation, 1.278385 seconds. Verify printed `verified`. The generated table is `reports/atlas-016.md`. Its Hash column is a 12-character prefix. The fractions below are the stored numerators and denominators. Engine `rrc-0.4.0`. Grammar `opening-prohibit-multiply-v1`. Occupation method `integer_pi_proportional_to_total_weight`. `results/atlas-012` and `results/atlas-015` were not rerun. The matrix comparisons below compile the named rules.

Every item has 8 states and 3 edges. The carrier is `(0,1)`, `(1,2)`, `(3,4)` on 5 vertices. The first two edges share vertex 1. The third edge is disjoint. The carrier has 2 components. The kernel hash equals the weight hash. The structure hash is `0963ca7e652f311e3382a80a52a2c8efe545700c1c793db7444f5140bb162fbd` on every cell. `new_primitive` is false. The composer is `prohibit_then_product`, and `order_independent` is true. The clock is `halt_self_loop`. Each cell has 1 recurrent class and 0 deadlocks. Occupation status is `unique` on all eight cells.

Every subset of these edges is a forest on the same five vertices, so the edge count plus the component count is 5 on every state. The stored means add to 5 on every cell. The baseline component mean `7/2` is this carrier.

## Eight tables

The empty list is the EQ-015 table, hash `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`. Every cell is 1. Mean edges `3/2`. Mean components `7/2`. Marginals `1/2`, `1/2`, `1/2`. Effective cardinality 0. The list changes neither support nor a positive weight. EQ-015 does not claim that the carrier geometry is the table.

`A16-pro-incident` prohibits `(1,2)` when `(0,1)` is present. Hash `fe1f4d4e5e5fcac700a7efc7ec32acb0dfcc1c21f5bb401f6b27738b527b2d7c`. That is the atlas-015 prohibit of the shared edge on the three-edge chain. Four cells are 0, all in the column of `(1,2)` and all in states where `(0,1)` is present: `(1,1)`, `(3,1)`, `(5,1)`, `(7,1)`. The other cells are 1. Mean edges `7/5`. Mean components `18/5`. Marginals `2/5`, `1/2`, `1/2`. Effective cardinality 1. This is a support change. The unread edge on this carrier is `(3,4)`. On the chain it is `(2,3)`.

`A16-mul-incident` multiplies `(1,2)` by 3 when `(0,1)` is present. Hash `badcbc1cecba75dbdb76f74ea9cc1368c0dc49c55eb52346b9575889e02dd84b`. Values `{1,3}`. No zero cell. Mean edges `13/8`. Mean components `27/8`. Marginals `5/8`, `1/2`, `1/2`. Effective cardinality 1. This is a rate change on a full support.

`A16-pro-across` prohibits `(0,1)` when `(3,4)` is present. Hash `866005248da1269bc32a3c62e3d391cae91e841b57fa180d634f832f11e67fc6`. Four cells are 0, all in the column of `(0,1)` and all in states where `(3,4)` is present: `(4,0)`, `(5,0)`, `(6,0)`, `(7,0)`. The other cells are 1. Mean edges `7/5`. Mean components `18/5`. Marginals `1/2`, `1/2`, `2/5`. The `2/5` is the condition edge `(3,4)`. Effective cardinality 1. This is a support change. The hash differs from the incident prohibit.

`A16-mul-across` multiplies `(0,1)` by 3 when `(3,4)` is present. Hash `35818e425b302f38df5d28715a61ec5e21b1a765ab3ceee5f81ee55c40156e82`. That is the atlas-012 far cell, which multiplies `(0,1)` when `(2,3)` is present. Values `{1,3}`. No zero cell. Mean edges `13/8`. Mean components `27/8`. Marginals `1/2`, `1/2`, `5/8`. The `5/8` is the condition edge. Effective cardinality 1. This is a rate change on a full support. The atlas-012 path has 4 vertices, so the same edge mean has component mean `19/8` there. The shared object is the matrix.

`A16-pro-disjoint` prohibits `(3,4)` when `(0,1)` is present. Hash `b54fee3ce4ed5f19f4843249d82b4217eb004fba882f25d8894b2b5d08fe7eb3`. Four cells are 0, all in the column of `(3,4)` and all in states where `(0,1)` is present: `(1,2)`, `(3,2)`, `(5,2)`, `(7,2)`. The other cells are 1. Mean edges `7/5`. Mean components `18/5`. Marginals `2/5`, `1/2`, `1/2`. Effective cardinality 1. This is a support change. The means and the marginals match the incident prohibit. The hash does not.

`A16-mul-disjoint` multiplies `(3,4)` by 3 when `(0,1)` is present. Hash `92189689622ad7ebd818c01b8ab01236265258c1cacdf43adf9de5c3f124311c`. That is the atlas-015 multiply of `(2,3)` by 3 when `(0,1)` is present. Values `{1,3}`. No zero cell. Mean edges `13/8`. Mean components `27/8`. Marginals `5/8`, `1/2`, `1/2`. Effective cardinality 1. This is a rate change on a full support. The means and the marginals match the incident multiply. The hash does not.

`A16-mixed` is the incident prohibit together with the disjoint multiply, both conditioned on `(0,1)`. Hash `f83fd2d4e2aeb937143f26dceae8a06363691ad470e2570e5d16dc6c4b64219b`. Values `{0,1,3}`. The four zero cells are the incident-prohibit cells `(1,1)`, `(3,1)`, `(5,1)`, `(7,1)`. Declared cardinality 2. Effective cardinality 2. Removal-sensitive count 2. Maximum positive `K` is 2. Mean edges `11/7`. Mean components `24/7`. Marginals `4/7`, `1/2`, `1/2`. The list is both a support change and a rate change. One recurrent class. No deadlock.

The eight hashes are distinct. The three prohibits share mean edges `7/5` and have three hashes. The three multiplies share mean edges `13/8` and have three hashes. Equal means are unequal tables.

## Where the marginal moves

On each of the six single-rule cells, the marginal that moves is the condition edge. The event edge and the unread edge stay at `1/2`. Each prohibit moves the condition marginal to `2/5`. Each multiply moves it to `5/8`. That is what these six cells show.

## Bit positions

The incident prohibit, the disjoint multiply, and the across multiply each match a stored chain matrix. Both listings put the named edges on the same bit positions, and the rule does not read the remaining edge. EQ-032 records those three identities. The carriers differ. The unread edge is a different pair. The incident prohibit is the second listed edge when the first is present. EQ-031 is the other bit order, the first listed edge when the second is present.

Swapping bits 1 and 2 carries the incident-prohibit table onto the disjoint-prohibit table, and the incident-multiply table onto the disjoint-multiply table. The carrier automorphisms are `(0,1,2,3,4)`, `(0,1,2,4,3)`, `(2,1,0,3,4)`, and `(2,1,0,4,3)`. That is the identity, the flip of vertices 3 and 4, the flip of vertices 0 and 2, and both. None of them swaps `(1,2)` with `(3,4)`, because `(1,2)` meets `(0,1)` and `(3,4)` does not. The bit swap is a different map from a carrier automorphism.

The mixed table is the elementwise product of the incident-prohibit table and the disjoint-multiply table. That is the existing composer.

## What the slice does not say

ATLAS-Q02 stays open. These eight cells separate support, rate, and both for this carrier, factor 3, and polarity present. The carrier is one five-vertex graph. No intervention operator is defined. No pattern is opened from `3/2`, `7/5`, `13/8`, `11/7`, `7/2`, `18/5`, `27/8`, `24/7`, `2/5`, `5/8`, or `4/7`. Atlas-012 and atlas-015 were not rerun.
