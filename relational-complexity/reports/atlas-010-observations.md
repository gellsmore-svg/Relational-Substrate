# atlas-010 observations

A map of one verified sample. Not a conclusion. Not an instruction to prefer a representation.

Plan hash `1d838e1e4a3c038ac08ca03816b67118442ceaf03d9466a072934a0ef5e5285a`. Definitions commit `2ecea77`. Freeze `73cc6c7`. All 15 items completed. Verify printed `verified`. The generated table is `reports/atlas-010.md`. Its Defect column is the tool float. The fractions below are the stored numerators and denominators. Engine `rrc-0.4.0`. Baseline is 1. A further label is undefined. `results/atlas-008` was not rerun.

No map adds state. No map is injective. Each label is a function of the current bitset. The three maps do not read the weights, so a carrier has one partition per map under both laws. The law decides whether that partition is strongly lumpable. Exact means strong lumpability. A positive defect rules out strong lumpability of that partition. It leaves other history-dependent descriptions untested. The quotient rows are stored only when the defect is zero. Each stored row sums to 1. When the defect is positive, the row field is null.

## Carriers and the one constraint

Triangle, edges `(0,1), (1,2), (0,2)`. Three-edge chain, edges `(0,1), (1,2), (2,3)`. Four-cycle, edges `(0,1), (1,2), (2,3), (0,3)`.

The empty list is stored for the canonical line graph and the carrier orbit. The position-indexed line graph of that empty list is the atlas-008 cell.

One multiply by 3, action `either`, polarity present, event `(0,1)`, condition `(1,2)`, is stored for all three maps. On each carrier those two edges are the first two listed edges. A comparison across carriers changes the carrier and the place of that pair together. It is joint.

## Shared tables

The triangle and the chain have three edges. Their empty lists are the same integer table, hash `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7`, the EQ-015 baseline. Their multiplies are the same integer table, hash `7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9`. That hash is the table stored on `A6-chain-bit` and `A6-branch-bit`. The four-cycle empty list is the EQ-016 baseline, hash `5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3`. The four-cycle multiply is a different table, hash `c7f6b804ebe70d93942121c4df693dd9ff27cd3c33b03c799eeb1d2aa1860aa7`. On every cell the kernel hash equals the weight hash. Grammar `opening-prohibit-multiply-v1`.

The shared table leaves the observation free. The triangle empty list has four labels and is exact. The chain empty list has five canonical labels, defect `4/9`, and six orbit labels that are exact.

## Partitions

The partition comparison uses the label functions on the stored edge lists.

On the triangle the three maps are one partition. Four labels. The empty list is exact, defect `0/1`, and the quotient is defined. The multiply has defect `4/9`, and the quotient is undefined. The three stored multiply cells share that law.

On the chain the position-indexed map and the canonical map are one partition. Five labels. The orbit is a different partition. Six labels. The empty-list canonical cell has defect `4/9`. The empty-list orbit cell is exact. The multiply canonical cell and the multiply position-indexed cell have defect `28/45`. The multiply orbit cell has defect `2/5`. The orbit partition that is exact under the empty list fails under the multiply. EQ-023 is the empty-list identity. This multiply lies outside it. The chain empty-list orbit cell is an instance of that identity.

On the four-cycle the canonical map and the orbit are one partition. Six labels. The position-indexed map is a different partition. Eight labels. The empty-list canonical and orbit cells are exact, and the quotient is defined. `A8-cycle4-line` stores the position-indexed map on the same empty-list hash: eight labels, defect `1/2`. That file was not rewritten. The multiply canonical and orbit cells have defect `11/24`. The multiply position-indexed cell has defect `19/24`. On this multiply the map with more labels has the larger defect. On the chain multiply the map with more labels has the smaller defect. Label count does not order the defect.

## What this sample does not say

It does not close ATLAS-Q10. The labelled line graph, the degree sequence, and a second label were not cells. ATLAS-Q11 was not in the round. It does not schedule defect `4/9`, `28/45`, `2/5`, `11/24`, or `19/24`. The triangle multiply and the chain empty-list canonical cell both store defect `4/9`. They are different tables and different carriers. It does not confirm EQ-022 or EQ-023. Those remain method identities. It does not rerun atlas-008. It does not observe a cover. It does not add a coordinate. A further label remains undefined.

PAT-013 records the separation of the weight table from the observation, with `schedules_follow_up` false.
