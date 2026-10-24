# atlas-003 observations

A map of the verified cardinality sample. Not a conclusion. Not an instruction to investigate any row next.

Plan hash `05de332578ff435f6e25eb2550db0a92ca576fdda187c99c8861fb9fdb77fc26`. All 13 items completed. The report table is `reports/atlas-003.md`. Engine `rrc-0.3.0`. The grammar is the opening composer. No incident predicate is in the plan.

The 13 lists are a declared sample. State enumeration inside each cell is exhaustive: 8 states and 3 edges. The sample is not every list of these cardinalities.

## Controls against atlas-001

Five lists reproduce atlas-001 integer tables. EQ-009. The engine string differs. The tables do not.

| atlas-003 | atlas-001 | Shared hash |
| --- | --- | --- |
| A3-01-base | A-N3-01-base | `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7` |
| A3-04-mul-present-4 | A-N3-03-mul-present | `a14bf1210fb719fbab5c6af3b0db7c597a24bf2419dc3e3caddd439686adcdde` |
| A3-06-pro-present | A-N3-02-pro-present | `d65a9800e618e62c49e0199f0d5cac3ca201448067180dbbbe4139a641958007` |
| A3-07-pro-form | A-N3-05-pro-form | `7931c712431e7da64ae3579542285a2196ad260992d59f4fe4265b94ca0433d8` |
| A3-08-pro-dissolve | A-N3-06-pro-dissolve | `e855bbd4fb6c12fd5ad974991496df8a76e016006389c881ba1825fe900e8dc3` |

The factor-2 absent multiply is not the atlas-001 factor-4 absent cell. Those hashes differ. That is a different factor, not a failed replication.

Form and dissolve occupations use `stationary_balanced`. Their stored means are float64 and are not quoted. The integer-method means below are fractions.

## Factors

Multiplying `(0,1)` by 2, by 3, and by 4 when `(0,2)` is present produces three tables and three `halt_self_loop` kernels. PAT-005. Each cell has 24 positive transitions and 0 zero cells. One recurrent class. The other columns stay at baseline 1, so a larger factor is not a pure scale of the row, and the row gcd does not identify the three kernels.

| Factor | Hash | Mean present edges | Mean components |
| --- | --- | --- | --- |
| 2 | `ff20a9324b668730f9fbe6f5ed12b6724c6440e8915c47fadab0baad424fd803` | 11/7 | 11/7 |
| 3 | `7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9` | 13/8 | 49/32 |
| 4 | `a14bf1210fb719fbab5c6af3b0db7c597a24bf2419dc3e3caddd439686adcdde` | 5/3 | 3/2 |

The factor-2 absent cell has hash `7367479acf60c51706dbd71d8a8bcc4293433d306194e9cf40ac250555b4ed88`, mean edges 10/7, mean components 47/28. Full support. It is not the present-polarity factor-2 table.

The two-event cell has the same integer means as the factor-4 cell, 5/3 edges and 3/2 components, and a different hash, `dae4059eba559216adfc8b9465b70d1d606eecc9cfd4f07aaed895d6ddf6b6c5`. Those means do not identify the table. The two-event cell has 20 positive transitions and 4 zero cells. The factor-4 cell has none zero.

## Longer lists

No two items in this round share a weight hash or a kernel hash.

Weight ablation and kernel ablation agreed on every cell. A removal that changes the integer table changes the kernel, and a removal that leaves the table leaves the kernel. ATLAS-Q08 stays open. This sample did not contain a constraint that changes the integers and leaves the kernel.

| Item | Declared | Effective | Kernel-effective | Positive | Zero | Classes | Deadlocks | Syntax cycle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A3-11-card4 | 4 | 4 | 4 | 16 | 8 | 1 | 0 | yes |
| A3-12-card6 | 6 | 6 | 6 | 12 | 12 | 2 | 1 | yes |
| A3-13-card8 | 8 | 7 | 7 | 12 | 12 | 2 | 1 | yes |

Card4 has a unique occupation. Mean present edges 29/22. Mean components 19/11. Method `integer_pi_proportional_to_total_weight`.

Card6 and card8 do not have a unique stationary law. No means are reported.

Card4 and card6 both have an imposed syntax cycle. Card4 has one recurrent class and card6 has two. The cycle flag is rule text. PAT-006. It is not a measured oscillation.

The length-8 table equals the same list without its last constraint. EQ-010. That constraint prohibits dissolution of `(0,2)` when `(1,2)` is present. The length-6 generator already prohibits either toggle of `(0,2)` on that guard. Leave-one-out on the frozen list finds only index 7 redundant, for the raw table and for the kernel. The seventh constraint, a factor-4 multiply of `(0,1)` when `(0,2)` is absent, is not redundant: card8 and card6 have different hashes. Their support counts still match, 12 and 12, so the support count does not identify the table either.

Card6 and card8 are the two cells whose kernel hash differs from their own weight hash. Some positive row has gcd greater than 1. That is not an equivalence between two specifications.

## Carrier structure

All 13 items store the same `structure_sha256`, `ff349bdce93ed13b62f03679c99fd48833989b4355d70f562056f7d3fa4f1447`. The carrier is the same complete graph on three nodes. The field does not read the constraint list.

## What stays open

ATLAS-Q01 through ATLAS-Q11 stay open. Cardinalities 5 and 10 were not in the sample. N=4 was not repeated. The incident predicate was not used. Nothing in these cells appoints the next round.
