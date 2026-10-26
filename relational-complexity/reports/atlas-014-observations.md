# atlas-014 observations

A map of one verified sample. Not a conclusion. Not an instruction to choose a map.

Plan hash `c8f63dc8054478c71467db630aee633b4f39f884b5f2331cc76ec180a5715790`. Definitions commit `d82d23a`. Freeze `a09ba2c`. All 8 items completed in one invocation, 1.290584 seconds. Verify printed `verified`. The generated table is `reports/atlas-014.md`. Its Hash column is a 12-character prefix. The fractions below are the stored numerators and denominators. Engine `rrc-0.4.0`. Both laws use grammar `opening-prohibit-multiply-v1`. `results/atlas-008`, `results/atlas-010`, and `results/atlas-013` were not rerun.

Every item has 16 states and 4 edges. The carrier is the four-cycle `(0,1)`, `(1,2)`, `(2,3)`, `(0,3)`. The kernel hash equals the weight hash. No map adds a coordinate. `new_state` is false. Conditional exactness and a history-dependent kernel are `not_computed`. A sequential row is stored only when that stage is strongly lumpable. The seven prohibit items are one weight table.

## The empty list

`A14-base-orbit-count` is the constant-1 four-edge table, hash `5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3`. That is the EQ-016 weight table. The structure hash is `5747f684d10b1fc3f48c38b0a9b4176e5c1aa137469d113d0caa3126c12f7a51`, the structure hash stored on the atlas-008 four-cycle cells. The carrier orbit has 6 labels and defect `0/1`. The edge count has 5 labels and defect `0/1`. The count is a function of the orbit: a carrier automorphism preserves the number of edges, so each orbit has one count. Both stages are exact, the exact prefix is 2, and `agreement` is `exact`. The sequential count kernel and the direct count kernel are the same rows.

That agreement is the compatibility of strong lumpability. EQ-023 gives the baseline orbit. EQ-021 gives the baseline count. The second stage is a function of the first. The equality of the two kernels is that definition applied to this chain. It is not a new lumpability theorem.

## The prohibit

The other seven items share hash `b6ab427edcb7b603d898e81a3286efa03802664ccdd6b33152b8716d0ee35d79`. The list is one prohibit, action `either`, of `(0,1)` when `(2,3)` is present. Those edges do not meet. Eight weight cells are 0, all in the column of `(0,1)` and all in states where `(2,3)` is present. The other 56 cells are 1. The law changes support. It does not rescale a positive weight. The structure hash is the same four-cycle hash as the empty list. The carrier did not change.

No prohibit item has exact prefix 2. `agreement` is `undefined` on each of them, and `kernels_agree` is null. No sequential kernel is compared with a direct kernel, because no prohibit sequence has two exact stages.

On this edge list the carrier orbit and the degree sequence are the same partition: empty, one edge, an adjacent pair, an opposite pair, three edges, and the full cycle. A three-edge chain does not give those two maps the same blocks. The equality is this cycle. Under the prohibit the shared partition has defect `11/24`. The edge count is a coarser partition, five labels, and its defect is also `11/24`. The witness pair in both checks is states 7 and 14. State 7 is `(0,1)`, `(1,2)`, `(2,3)`. State 14 is `(1,2)`, `(2,3)`, `(0,3)`. Their pairwise L1 distance is `2/3`.

The count defect has a direct reading. The four states with three edges are one block. State 14 cannot add the missing edge `(0,1)`, because `(2,3)` is present, so every allowed toggle removes an edge. State 7 can still add `(0,3)`. The mean law of the four states puts probability `11/48` on the full cycle. State 14 puts probability 0 there. The L1 distance to that mean is `11/24`. The same four states are one orbit block. State 14's distance to the mean law of that block is again `11/24`, now split across the adjacent-pair block, the opposite-pair block, and the full cycle. One number is doing both jobs because the triple states are a block of both partitions. It is not a general identity of the two defects.

## What each sequence did

`A14-pro-orbit-count`. The orbit does not have a quotient. The edge count is a function of the orbit and its direct law is also not exact, defect `11/24`. The sequential stage is undefined because the orbit is not strongly lumpable. Its rows are absent.

`A14-pro-degree-count`. The edge count is a function of the degree sequence on this cycle: each of the six degree sequences has one edge count. The degree stage is not exact, so the sequential count has no rows. The direct count is the same failed law as above.

`A14-pro-count-degree`. The degree sequence is not a function of the edge count. States with two edges split into an adjacent pair and an opposite pair. The stored reason is that failure to factor. The sequential defect is null, not zero. The direct degree law is the orbit law above and is not exact. The count stage is not exact either, so a factored second map would still have had no sequential kernel.

`A14-pro-line-count`. The position-indexed line graph has 8 labels and defect `5/8`. The largest distance to a block mean is state 9 in the block of states 3, 6, 9, and 12. The witness pair is states 3 and 9, pairwise L1 `1/2`. The result file does not store that pair. It is the lumpability witness of the stored weight table. State 3 is `(0,1)`, `(1,2)`. State 9 is `(0,1)`, `(0,3)`. The edge count is a function of this line graph, because the line graph's vertex count is the number of present edges. The sequential count is undefined because the line graph is not strongly lumpable. The direct count remains defect `11/24`.

`A14-pro-orbit-constant`. The orbit stage is the failed orbit above. The one-block label has 1 label, direct defect `0/1`, and a self-loop of probability 1. That direct law is EQ-029. The sequential stage is undefined because the orbit is not strongly lumpable. A coarser direct law can be exact while the intermediate quotient is absent. The constant exactness is the one-block definition. It is not evidence that the prohibit has a closed two-stage quotient.

`A14-pro-injective-degree`. The relationship-labelled line graph has 16 labels and defect `0/1`. EQ-022 is the reason: the labels are the states. The degree sequence factors through it. The second stage is typed and not exact, defect `11/24`, and its rows are absent. The exact prefix is 1. This is a first exact stage and a second stage that is not exact. The first map does not compress the chain, so the second defect repeats the direct degree defect.

`A14-pro-overlap-count`. The blocks are `[(0,1),(1,2)]` and `[(1,2),(2,3)]`. Their only shared edge is `(1,2)`, and the family misses `(0,3)`. The realised-overlap count is the presence of that shared edge: 2 labels. It is not strongly lumpable. The defect is `1/12`. In the block where `(1,2)` is absent, the probability of toggling `(1,2)` is `1/4` when `(2,3)` is absent, because all four weights are 1, and `1/3` when `(2,3)` is present, because the prohibit removes the weight of `(0,1)` and the shared-edge weight stays 1. Each of those eight states is at L1 distance `1/12` from the mean of the block. The witness pair is states 0 and 4. The edge count is not a function of this two-label map. The stored sequential reason is that failure to factor, and the sequential defect is null.

## What the slice does not say

ATLAS-Q13 stays open. The round asked how a second map behaves after a first map, on one carrier and two laws. The empty list gives one exact pair, explained by EQ-021 and EQ-023. The prohibit gives no exact pair. One second map fails to factor. One first map is exact and its second map is not. One first map fails while the direct one-block map stays exact. Those are the outcomes on this list. They are not a classification of every sequence.

The baseline line-graph defect `1/2` is the atlas-008 cell. It was not recomputed. The parity fixture was not an item. No third map was added. The overlap count here is not the path or triangle fixture, and it is not the later chain sample. No pattern is opened from `11/24`, `5/8`, or `1/12`.
