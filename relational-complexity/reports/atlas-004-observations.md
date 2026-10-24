# atlas-004 observations

A map of the verified incidence sample. Not a conclusion. Not an instruction to investigate any row next.

Plan hash `f6a9680feb02700b5dd8aa9fe024dfe1668d51bdfcbc8aaf5c64607d6c8391fe`. All 18 items completed. The report table is `reports/atlas-004.md`. Engine `rrc-0.3.0`.

The bit-prohibit placement is the atlas-002 instrument: the event is the first listed edge and the condition is the second. The incident templates put one present-polarity constraint on every carrier edge. The two chain cells that name one edge are instruments. They are not claimed to be label-covariant.

The report column `max K` is `max_positive_k`. That field counts designated-edge features only. On a pure incident list it is 0. The conjunction expansion is a different number and is quoted below.

## Bit controls

Baselines and bit prohibits reproduce the atlas-002 tables. EQ-011. The chain and the branch still share those two tables. The incident rules are not what produces that identity.

| Carrier | Grammar | Hash | Mean edges | Mean components |
| --- | --- | --- | --- | --- |
| chain and branch | baseline | `3f096c84d15f07449d954e22eb5abd7fb368a91b1912d5347b404e60d87e10a7` | 3/2 | 5/2 |
| chain and branch | bit prohibit | `d65a9800e618e62c49e0199f0d5cac3ca201448067180dbbbe4139a641958007` | 7/5 | 13/5 |
| cycle | baseline | `5c458ff162a1ba869c081c42a5160b03fab0df590b4f01e0a5977621177e86c3` | 2/1 | 33/16 |
| cycle | bit prohibit | `a5ec527229ef7b9ce77d9606eef8ab5c4fab52810d9d2dc651453a551fe2b924` | 27/14 | 17/8 |
| disconnected | baseline | `7d68b5c4119211a50d84f89b7f843e9ae6da04183d69ba4b542b04aeb2280273` | 1/1 | 3/1 |
| disconnected | bit prohibit | `45cb96ef4404d3f75d95c066173595b9e3c75fd15256ef6ed8d96b5842e88da9` | 5/6 | 19/6 |

All six occupations are unique. Method `integer_pi_proportional_to_total_weight`.

## Incident templates

The multiply template and the prohibit template each give a different table on the chain and on the branch. PAT-007. Full support on every multiply template. The prohibit templates do not have a unique occupation, so no means are reported.

| Carrier | Grammar | Weight hash | Kernel hash | Positive | Zero | Classes | Deadlocks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| chain | multiply | `e4e7608a0474f4cc74bfca854ebaca0322529ac83efa1a62b2f6351112d3e34f` | `68c3b01583d8ebed6be798c336a5d127a74a863f61b8d316c8a1eab44955bb40` | 24 | 0 | 1 | 0 |
| branch | multiply | `ebb9b42ba9d60338382547fe9bffb454c27e61e7a33fd8691a15f61b9b47e6ca` | `fbd6b25a09df6ba6bbb17c0018de00dd45ed6a1da98cf01a0072bfd1f321a285` | 24 | 0 | 1 | 0 |
| chain | prohibit | `ae907d329110008335dde73d2f9e2fad6b8785143b70da606a91fd0bc3834253` | same as the weight hash | 10 | 14 | 4 | 3 |
| branch | prohibit | `af814c24c82e010ae71530568157ddf588da9fcf8da64225cd6d3025d084c4fb` | same as the weight hash | 6 | 18 | 5 | 4 |
| cycle | multiply | `c5d14c7d98104500e36c4c261c299500c42befb860ad4a0f5d5895b358325186` | `86f04f1319654df773cf88fd3c477455b6e3d24433bdcb39a2c1c2ae1be90be2` | 64 | 0 | 1 | 0 |
| cycle | prohibit | `b572b2cbf5469ce2d3dde12a49022c184cc86c0b346ee9d5fddaf7ea41f95fa1` | same as the weight hash | 16 | 48 | 10 | 9 |

Chain multiply means: edges 45/26, components 59/26. Branch multiply means: edges 17/10, components 23/10. Cycle multiply means: edges 11/5, components 15/8.

Declared cardinality equals effective cardinality on these six cells, for the raw table and for the kernel. Where the kernel hash differs from the weight hash, a positive row has gcd greater than 1. Removing a constraint still changes both, on these cells.

Expansion, not declared K: the chain template has neighbourhood sizes 1, 2 and 1, expansion J total 5, max expansion K 3. The branch template has neighbourhood size 2 on every edge, expansion J total 9, max expansion K 3. The cycle template has neighbourhood size 2 on every edge, expansion J total 12, max expansion K 3. Declared J is the number of edges. `max_positive_k` stays 0.

The chain, branch, and cycle templates have `imposed_rule_dependency.has_cycle` true. The chain multiply has that flag and one recurrent class. The chain prohibit has the flag and four classes. The flag remains rule text. PAT-006 was the same split on the opening grammar.

## Empty neighbourhood

On the disconnected carrier each edge has no incident neighbour. Present polarity never matches. Both incident templates have effective cardinality 0 and the baseline hash. EQ-012. Expansion J is 0 and expansion K is 0. The bit prohibit on that carrier still changes the table, because it reads the other component by index. A static fact that the two edges do not meet is not this predicate. The predicate's failure to fire is the current empty neighbourhood.

## Named edges

`A4-chain-end-mul` multiplies the endpoint `(0,1)`. Its only incident neighbour is `(1,2)`, so the expansion is one conjunction, J 1 and K 2. The integer table equals atlas-003 `A3-03-mul-present-3`, hash `7b4f2c8ef26032e36f92000c69cc7c0fcf032e4f1353009ff490efa1f4b37be9`. EQ-013. Mean edges agree at 13/8. Mean components do not: 19/8 on the chain and 49/32 on the three-node cell. The node counts differ.

`A4-chain-mid-mul` multiplies `(1,2)`, which has two incident neighbours. Expansion J 3 and K 3. Hash `6e92a4e1ae6d3d7117da95e485c64c9f8a07f58de12cdfdb8bf47f9f1df062a2`. Mean edges 29/18. Mean components 43/18. The named edge changes the table. That is the instrument. It is not a covariance claim. The uniform template's permutation check remains the unit test in `tests/test_kernel.py`. ATLAS-Q11 stays open.

## Structure hashes

`structure_sha256` depends on the carrier, not on the constraint list. The four carriers store four hashes. Chain `e6f7386ece69cd8888eca2be7cbc621dc46a80b61c6ddebb9f0a18abfceea8cc`. Branch `6c959c90bc45976a55a7d874b0e0e4a6c4c31cf14f231e39417136e5ddf1e1d1`. Cycle `5747f684d10b1fc3f48c38b0a9b4176e5c1aa137469d113d0caa3126c12f7a51`. Disconnected `9dcbfc45a798a98c8c1d1597517b3e0cfc4e4f9192cbc70c45e00f07897b34e5`. The bit-rule tables do not separate chain from branch. This field does. ATLAS-Q07 asked whether a later core should carry such an observable. The field is now stored on `rrc-0.3.0` results. The question stays open. Atlas-002 results were not rewritten.

## What stays open

ATLAS-Q01 through ATLAS-Q11 stay open. One predicate separated these carriers. Other predicates were not run. N=5 was not run. These four listings are not every graph. Weight ablation and kernel ablation agreed on every cell in this round. That does not close ATLAS-Q08.
