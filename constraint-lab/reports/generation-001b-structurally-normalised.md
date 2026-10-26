# Generation 001b — structurally normalised reanalysis

Engine `0.2.0`, semantic version `0.2.0`, normalisation `structural-unique-v1`, grammar `pairwise-edge-v1`.
Census commit `112b6b11d0f5b901a755b6ba5c9e740032006536`.
Specification hash `c6ee7765142472162a6d210c45d54f3ab1e8398cdec571b05c553ed68ac5cc74`.
Python 3.12.3, NumPy 2.5.3, platform `linux`.
Wall clock 1117.1 seconds. Shard-work sum 1522.8 seconds. Workers 2. Shards 883. `DEFAULT_SHARD_ITEMS` 4000.
Summary SHA-256 `46a4316f5c1d6c71c9c405b1d361a34a4e26d55dbad0cc27fad657152587e797`.

This generation does not replace Generation 1. The committed Generation 1 manifests, report, catalogue, and exemplars stay as engine `0.1.0` at `fd7758d0be29877b6a306455fd81ca3eca49df8b` wrote them. Generation 1 searched labelled constraint sets that could stack two weights on one structural rule. Generation 1b analyses the same substrate and the same `W4` alphabet after those stacks are removed from the primary census.

Singleton-table SHA-256:

| File | SHA-256 |
| --- | --- |
| `generation-001b-structurally-normalised-singles-n2-k3.csv` | `2677493663799c9ea83b1fca36954145a4166b05711c850806b61ecfd27618c8` |
| `generation-001b-structurally-normalised-singles-n3-k3.csv` | `fd1372797e8706efba23910cca80e98f8c1bb1fc086b4dfbf0fe2ea147eb02cd` |
| `generation-001b-structurally-normalised-singles-n4-k2.csv` | `77dfcb548008f5a87bbcd1d4296c7759965a945afff540bdda8c19fa3fa82adc` |
| `generation-001b-structurally-normalised-singles-n5-k2.csv` | `216ed623d3729bcda080ab32bb5b8f58169c1af976338ad81b76a556bcf20c01` |

The `N = 3` family index (247 MB) and kernel index (25 MB), and the `N = 4` family index (15 MB), stay under `generated/generation-001b-structurally-normalised/`. Their SHA-256 values are in the summary. Indexes at most 2 MB are under `catalogue/`.

## A. What changed in the instrument, not in the coordinate

The coordinate is the Generation 1 coordinate. Graph semantics. `G = S = H = L = 0`, `O = 2`, alphabet `W4`, sensitivity alphabets `W3` and `W16`.

```text
E(N=2, A≤2, O=2, G=0, S=0, H=0, K≤3, L=0, graph, W4)  cards {1,2,3}
E(N=3, A≤3, O=2, G=0, S=0, H=0, K≤3, L=0, graph, W4)  cards {1,2,3}
E(N=4, A≤4, O=2, G=0, S=0, H=0, K≤2, L=0, graph, W4)  cards {1,2}
E(N=5, A≤4, O=2, G=0, S=0, H=0, K≤2, L=0, graph, W4)  card  {1}
```

`A_max` is now a grammar filter. In these cells it removed nothing (`outside_a_bound` is 0). A declared `G`, `S`, `H`, `L`, or `O` other than the values above is refused. Composition is `structural-simple`: a set may contain one weighted instance of a structural identity. The structural identity is polarity, action, conditions, and count literals. The weight is an attribute. Stacked-weight composition remains available as a named mode and was not run.

Heavy analysis runs on every canonical structurally-simple set. For `N ≤ 3` the stationary distribution and the rational observables stay as exact fractions. Entropy stays a float. At `N = 4` and `N = 5` the stationary solve is float64. Dissolution shift is an exact fraction of the kernel rows at every `N`.

Family identity is no longer the Generation 1 16-hex hash of the labelled modal and support maps. The identifiers below are 64-hex digests of `S_N`-canonical tokens. Counts can be compared with Generation 1. Identifier strings cannot.

## B. Coverage

`canonical` is the structurally-simple canonical count, the primary census. `including stacked` is that count plus the canonical stacked sets. `including stacked` equals the Generation 1 canonical count in every cell.

| Cell | Card | Labelled | Simple labelled | Stacked labelled | Canonical simple | Stacked canonical | Including stacked | Generation 1 canonical |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| N=2 | 1 | 10 | 10 | 0 | 10 | 0 | 10 | 10 |
| N=2 | 2 | 45 | 25 | 20 | 25 | 20 | 45 | 45 |
| N=2 | 3 | 120 | 0 | 120 | 0 | 120 | 120 | 120 |
| N=3 | 1 | 270 | 270 | 0 | 60 | 0 | 60 | 60 |
| N=3 | 2 | 36,315 | 35,775 | 540 | 6,210 | 120 | 6,330 | 6,330 |
| N=3 | 3 | 3,244,140 | 3,100,500 | 143,640 | 519,830 | 24,720 | 544,550 | 544,550 |
| N=4 | 1 | 660 | 660 | 0 | 50 | 0 | 50 | 50 |
| N=4 | 2 | 217,470 | 216,150 | 1,320 | 9,745 | 100 | 9,845 | 9,845 |
| N=5 | 1 | 1,900 | 1,900 | 0 | 50 | 0 | 50 | 50 |

In every cell, analysed + stacked canonical + removed by symmetry equals the labelled combination count. Edge-template partitions: `N = 3` has 54 structural normal forms and 270 labelled constraints; `N = 4`, `K ≤ 2` has 132 and 660; `N = 5`, `K ≤ 2` has 380 and 1,900. Those labelled sizes match Generation 1.

| Cell | Qualitative families | Generation 1 families | Exact kernels | Observable signatures | Structural | Screened | Baseline-equivalent families |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| N=2 | 4 | 4 | 4 | 4 | 3 | 0 | 1 |
| N=3 | 61,929 | 80,155 | 391,991 | 379,177 | 47,342 | 61,757 | 1 |
| N=4 | 3,929 | 4,018 | 9,595 | 7,019 | 1,887 | 3,858 | 0 |
| N=5 | 30 | 30 | 50 | 30 | 10 | 16 | 0 |

Sensitivity on every analysed singleton, `W3` and `W16`: modal map unchanged and support map unchanged on 20, 120, 100, and 100 checks.

## C. Unchanged findings

- The six reference expressions that sit inside a cell reproduce the Generation 1 fractions. The canonical form of `form(0-2) | present(0-1) & present(1-2) => strong_favour` is `form(0-1) | present(0-2) & present(1-2) => strong_favour`. Density `13/24`, triangle mass `11/64`, closing bias `1/9`, dissolution shift `1/3`. The strong-suppress row is density `17/36`, triangle `3/32`. The prohibit row is density `11/24`, triangle `5/64`. `dissolve(0-1) | present(0-2) & present(1-2) => strong_favour` has density `1/2` and triangle `1/8`, baseline triangle mass and not the baseline kernel. `form(0-2) | present(0-1) => strong_suppress` is density `19/42`, triangle `1/12`. The strong-favour form of that pair is density `21/38`, triangle `13/76`.
- `N = 2` still has four families and four kernels. Any strictly positive weight on the single edge matches the baseline. The two prohibits, and the pair of both prohibits, do not. Three families are period 1 and one is period 2. One family has no deadlock, two have one deadlock state, and one has both states halted.
- At `N = 3` the period-1 count is still 104, and all 104 families are cardinality 3. Deadlock families are 104. The other 61,825 families are period 2 with no deadlock.
- Endpoint magnitudes that Generation 1 reported are unchanged. Rise-then-release excess at `N = 3` still runs from `−2/3` to `+1/3`. Closing bias still runs from `−1/3` to `+2/3`. Dissolution shift still reaches `2/3`. At `N = 4`, `K ≤ 2`, cards `{1, 2}`, there is still no halt and every family is period 2. At `N = 5` the 30 qualitative families, 10 structural and 20 full-support, are still the singleton census, and sensitivity is still 100/100.
- The soft three-literal closing favour still moves triangle mass from `1/8` to `11/64` and does not move the 4-step rise-then-release excess off 0. That row is the reference above.

The lex-smallest grammar stored for an endpoint is the first grammar in lexicographic order that attains it, inside the structurally-simple census. For rise excess `−2/3` and closing bias `+2/3` that grammar is the three dissolve-prohibits. For closing bias `−1/3` it is the three form-prohibits. For rise excess `+1/3` it is two unconditional dissolve-prohibits plus `dissolve(1-2) | absent(0-1) & absent(0-2) => prohibit`. Generation 1 described the same endpoint values as coming from prohibit pairs or triples. The values are the finding. The stored exemplar is the lex-smallest simple grammar that hits the value.

## D. Changed findings

Qualitative-family counts fall where stacked sets had been families of their own, or had been the only members of a family: `N = 3` from 80,155 to 61,929, and `N = 4` from 4,018 to 3,929. `N = 2` and `N = 5` do not change, because a singleton has nothing to stack and the `N = 2` positive pairs that remain are structurally distinct (form against dissolve on the one edge).

The interior quantiles are a different population from Generation 1: canonical qualitative families after stacked sets are removed, not the old labelled modal/support families. They are not a revision of the Generation 1 quantiles. The endpoints above are the comparable part.

`N = 3` quantiles of the family-maximum dissolution shift: 0, `0.2222`, `1/3`, `1/3`, `0.4667`, `2/3`, `2/3`. Closing-bias maxima: `−1/3`, `−0.04444`, `0.009259`, `0.07407`, `0.1481`, `0.2667`, `2/3`. Rise-excess maxima: `−2/3`, `−0.08333`, 0, `0.07619`, `0.1455`, `0.25`, `1/3`.

`N = 4` rise excess now has exact endpoints `−397/4500` and `29/288`. The minimum is the pair `dissolve(0-1) => prohibit` and `dissolve(0-2) => prohibit`. The maximum is the pair `form(0-1) => prohibit` and `form(0-2) => prohibit`. Dissolution-shift maximum is `25/42`, from `dissolve(0-1) => strong_favour` together with `dissolve(0-1) | absent(0-2) => strong_favour`. Those two rules are structurally distinct. The Generation 1 float near `0.595` was this fraction seen through float arithmetic on a different, stacked, set. `N = 5` shift maximum is `27/130`, from the singleton `dissolve(0-1) => strong_favour`.

## E. Removed representational artifacts

Generation 1 treated `form(0-1) => strong_favour` together with `form(0-1) => strong_suppress` as two constraints. The factors are `4` and `1/4`. The product is 1, so the pair is the baseline kernel, and Generation 1 called it the smallest baseline-equivalent object at `N > 2`. Under structural identity that pair is one rule with two grades. It is excluded before analysis. The same exclusion removes the `N = 4` reciprocal pair whose recorded dissolution shift was one unit in the last place (`1.1e-16`) on an exactly uniform kernel. That float is not in this census. The shift column on the sets that remain is an exact fraction.

No cardinality-2 structurally-simple set in the searched cells has the baseline kernel.

At `N = 2` the sixteen positive form/dissolve pairs are `inherited_baseline`: each member is already the baseline on its own. They are not a cancellation. The baseline family there has 24 members: those 16 pairs and the 8 strictly positive singletons. Genuine global cancellations: 0. Local cancellations: 0.

## F. New findings made visible by exact-kernel analysis

### Global cancellation is a triple

At `N = 3` there are 40 genuine global cancellations. Every one is cardinality 3. The shard results stored all 40 examples; no shard truncated the example list below its count. All 40 share one exact kernel, the baseline kernel, and they are the entire baseline-equivalent family (count 40, one kernel, period 2, density `1/2`, triangle `1/8`, entropy `log2(3)`). Four of them were rebuilt from the expressions and matched the baseline successor table: the complementary dissolve partition, the three-edge dissolve wedge at `strong_favour`, a mixed form/dissolve triple at `weak_suppress`, and the three-edge form-when-absent triple at `strong_favour`.

The mechanisms, each present at strong and weak grade and in both reciprocal directions unless noted:

- One action, three structurally distinct conditions whose factors multiply to 1 on every state. Example: `dissolve(0-1) => strong_favour`, `dissolve(0-1) | absent(0-2) => strong_suppress`, `dissolve(0-1) | present(0-2) => strong_suppress`. The same pattern occurs for `form`.
- A finer partition of one condition, plus the coarser rule at the reciprocal grade. Example: `dissolve(0-1) | absent(0-2) & absent(1-2) => strong_favour`, `dissolve(0-1) | absent(0-2) & present(1-2) => strong_favour`, `dissolve(0-1) | absent(0-2) => strong_suppress`.
- The same weight on the three symmetric wedges `dissolve(edge) | present(other) & present(other)`. Weighting every dissolve of the complete triangle equally leaves the kernel at the baseline, and each member alone does not.
- The same construction for `form(edge) | absent(other) & absent(other)`.
- Mixed form and dissolve triples, four grades each. One pattern is a dissolve of each of two edges under complementary conditions, plus a form of the third when both of those edges are present.

At `N = 4`, inside `K ≤ 2` and cards `{1, 2}`, genuine global cancellations are 0. Structurally distinct constraints do not cancel globally in that cell. Local cancellations are 112. The lex-smallest is `dissolve(0-1) => strong_favour` with `dissolve(0-1) | absent(0-2) => strong_suppress`: two structures co-match a toggle with reciprocal grades, and the kernel is not the baseline.

At `N = 3`, local cancellations are 20,352. The stored example list is capped, so it is not a complete catalogue. The lex-smallest examples are cardinality 3 and pair a prohibit with a second dissolve whose conditional grade is reciprocal on some states only.

### Within-family variation

A qualitative family is support plus modal map. Exact kernels inside one family are not the same object.

| Cell | Families with more than one kernel | Widest kernel count | Sets in that family | Lex-smallest member |
| --- | ---: | ---: | ---: | --- |
| N=2 | 0 | 1 | 1 | each family is one kernel |
| N=3 | 57,574 of 61,929 | 1,042 | 1,645 | `dissolve(0-1) => strong_favour` |
| N=4 | 3,002 of 3,929 | 38 | 50 | `dissolve(0-1) => strong_favour` |
| N=5 | 20 of 30 | 2 | 2 | `dissolve(0-1) | absent(0-2) => strong_favour` |

The widest `N = 3` family, exact fractions: density `3481/8610` to `299/615`, total variation `1/10` to `5/22`, triangle mass `167/2870` to `67/574`, closing bias `−4/21` to `−2/117`, rise excess `−7/33` to `−1/18`. Halt mass is `0/1` throughout. Entropy, which is not rational, runs from about 1.320 to 1.551 bits.

The widest entropy span at `N = 3` is a different family: 0.783 bits, 46 kernels, 98 sets. The lex-smallest member is `form(0-1) => strong_suppress` together with `form(0-2) | absent(0-1) => prohibit`. Entropy runs from about 0.553 to 1.336 bits.

At `N = 5` the widest family has two kernels and one observable signature. Entropy runs from about 3.287 to 3.313 bits while the signature, which does not contain entropy, does not split them. Observable equality is not kernel equality. At `N ≤ 3` an exact-kernel match does imply the same qualitative family and the same observable signature. The `N = 3` counts show the converse is false: 391,991 kernels, 61,929 qualitative families, 379,177 signatures.

At `N = 4` the stationary path is float64. The widest family entropy runs from about 2.423 to 2.562 bits, and the recorded density runs from about 0.451 to 0.488.

## G. What this reanalysis does not say

The screen is the predeclared Generation 1 threshold. It flags 61,757 of 61,929 families at `N = 3`. The histograms are the record. The screen is not a discovery.

`stationary_residual` is stored as `0.0` on the rational path. That value is a placeholder, not a measured residual of an independent solve.

Generation 1b did not search stacked-weight composition as its own mode, occupation counts, `N = 4` cardinality 3, `N = 5` cardinality above 1, `N > 5`, or any positive `G`, `S`, `H`, `L`.

## Commands

From `constraint-lab/`, engine 0.2:

```bash
.venv/bin/python -m rs_constraint_lab run experiments/specs/generation-001b.json \
  --out generated/generation-001b-structurally-normalised --workers 2 --publish .
.venv/bin/python -m rs_constraint_lab verify generated/generation-001b-structurally-normalised
```

Generation 1 is still:

```bash
python -m rs_constraint_lab run experiments/specs/generation-001.json \
  --out generated/generation-001 --publish .
```

at commit `fd7758d0be29877b6a306455fd81ca3eca49df8b`. Re-running that specification with engine 0.2 writes a different census and does not replace the committed Generation 1 files.
