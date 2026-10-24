# atlas-002 observations

A map of the verified carrier cells, and of how their weight tables sit next to atlas-001. Not a conclusion. Not an instruction to investigate any row next.

Plan hash `937573af07c6d5b40e43802b4f32bac76b32c66eefbca7a68aaab8d15a8bb26e`. All 16 items completed. The report table is `reports/atlas-002.md`.

The placement rule, first listed edge as the event and second listed edge as the condition, is an instrument. Carrier component counts are instruments: 1 for the chain, the branch, and the cycle, and 2 for the disconnected pair.

## What the weight tables do

The chain and the branch are different lists of pairs. On each of the four grammars their weight hashes are equal. EQ-006.

| Grammar | Shared hash |
| --- | --- |
| baseline | `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7` |
| prohibit | `d65a9800e618e62c49e0199f0d5cac3ca201448067180dbbbe4139a641958007` |
| multiply | `a14bf1210fb719fbab5c6af3b0db7c597a24bf2419dc3e3caddd439686adcdde` |
| formation prohibit | `7931c712431e7da64ae3579542285a2196ad260992d59f4fe4265b94ca0433d8` |

Those four hashes are also the hashes of the N=3 complete-carrier cells with the same bit rule: baseline, pro-present, mul-present, and pro-form. EQ-007. Both objects are 3-bit tables. The listing has renamed the pairs and kept the bit positions of the rule.

Mean present-edge counts therefore match between the chain, the branch, and those N=3 cells when the occupation is the integer row-sum law. Mean component counts match between the chain and the branch. They do not match the N=3 cells, because the node count is 4 rather than 3. The baseline means are 5/2 on the chain and the branch, and 13/8 on N=3.

The 4-cycle and the disconnected pair have their own hashes. All 16 occupations are unique. None of these cells is the both-polarity construction, so the round does not say whether that non-uniqueness survives a carrier change. ATLAS-Q05 stays open.

## What the common core does not see

Component count agrees on every one of the 8 masks of a 3-edge chain and a 3-edge star. The non-increasing degree sequence agrees on masks 0, 1, 2, 3, 4 and 6, and differs on two. Mask 5 (bits 0 and 2) is (1, 1, 1, 1) on the chain and (2, 1, 1, 0) on the branch. Mask 7 (all three edges) is (2, 2, 1, 1) on the chain and (3, 1, 1, 1) on the branch. These tuples are sorted, not indexed by node. That comparison reads the carrier lists. It is not a cell, and degree sequence is not in the common core. PAT-004. ATLAS-Q07 asks whether a later core should carry an observable that sees this. It does not schedule that core.
