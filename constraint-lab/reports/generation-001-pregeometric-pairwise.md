# Generation 001 — pre-geometric pairwise grammar

Engine `0.1.0`, commit `fd7758d0be29877b6a306455fd81ca3eca49df8b`.
Specification hash `620c776a6d13d7ad0bc9e0c5b8e6bc4c683694f19a1dfc41172bc52d58058dbe`.
Python 3.12.3, NumPy 2.5.3, platform `Linux-6.18.40.1-microsoft-standard-WSL2-x86_64-with-glibc2.39`.
Wall time 220.4 seconds. Seed policy: MT19937 via `random.Random.randrange` on integer weights; Generation 1 horizons 32 with seeds `{0,1,2,3,4}`; rise-then-release horizon 4 from the empty state, and only when the state space has at most 64 states.
Summary SHA-256 `4bb1e44ee1c8ded1c3335079f82fadbe4b688b680a72abbe8860348522bd0938`.

Singleton-table SHA-256:

| File | SHA-256 |
| --- | --- |
| `singles-n2-k3.csv` | `ec9b0c67563ea7cb35c4197088e5f40ced3bae64fc1db035ce11bebfa73fa1d8` |
| `singles-n3-k3.csv` | `f829dd600c047c550d62fbed7eeb56c78e910619718a772f7fe2ba7915ca6f15` |
| `singles-n4-k2.csv` | `eb98a5a1cf63a9ca6a0345611de80a61191b197957995a6606ceac063b0912d2` |
| `singles-n5-k2.csv` | `6463e61887cb6ecd8a05c1a8ed1888b482bc2c369ea73d5f19ed289ee588ccae` |

The review is `docs/review-log.md`. It did not produce a second census.

## A. Experiment definition

Graph semantics. Undirected pairwise relations. No geometry, no extra state channel, no history, no meta-constraint. Alphabet `W4` (factors `0, 1/4, 1/2, 2, 4`). Sensitivity alphabets `W3` and `W16` on every singleton. Baseline weight of every toggle is 1.

```text
E(N=2, A≤2, O=2, G=0, S=0, H=0, K≤3, L=0, graph, W4)  cards {1,2,3}
E(N=3, A≤3, O=2, G=0, S=0, H=0, K≤3, L=0, graph, W4)  cards {1,2,3}
E(N=4, A≤4, O=2, G=0, S=0, H=0, K≤2, L=0, graph, W4)  cards {1,2}
E(N=5, A≤4, O=2, G=0, S=0, H=0, K≤2, L=0, graph, W4)  card  {1}
```

`A_max` is the declared bound. Observed arity is the number of distinct endpoints a canonical set names. At `K ≤ 2` a constraint names at most four entities.

Measure scope, also stored on each cell:

- Light analysis on every canonical set: support, recurrent classes, period, deadlocks, dissolution shift, closing bias.
- Heavy analysis on every singleton, and on the first-seen member of each modal-and-support family: stationary occupancy from the empty state, entropy rate, total variation from uniform, reversibility defect, and the rise-then-release probability when the state count is at most 64.
- Stationary arithmetic is rational for at most 16 states, otherwise float64 with a recorded residual.

Six reference expressions were located inside the exhaustive grammar. They were not a filter. On `N = 3` all six are in the grammar. The three-literal ones are outside `K ≤ 2`, so they are absent at `N = 4` and `N = 5`. Edges `0-2` do not exist at `N = 2`.

## B. Coverage

| Cell | Raw templates | Syntax-invalid | Redundant | Outside K | Normal forms | Labelled | Canonical states | Labelled states |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| N=2, K≤3 | 6 | 2 | 2 | 0 | 2 | 10 | 2 | 2 |
| N=3, K≤3 | 162 | 54 | 54 | 0 | 54 | 270 | 4 | 8 |
| N=4, K≤2 | 2,916 | 972 | 972 | 2,784 | 132 | 660 | 11 | 64 |
| N=5, K≤2 | 1,180,980 | 393,660 | 393,660 | 393,280 | 380 | 1,900 | 34 | 1,024 |

The four raw columns sum to the raw template count in each row. Labelled constraints equal normal forms times 5.

| Cell | Cardinality | Combinations | Canonical | Removed by symmetry | Families in the cell |
| --- | ---: | ---: | ---: | ---: | ---: |
| N=2 | 1 | 10 | 10 | 0 | 4 |
| N=2 | 2 | 45 | 45 | 0 | (running) |
| N=2 | 3 | 120 | 120 | 0 | 4 |
| N=3 | 1 | 270 | 60 | 210 | (running) |
| N=3 | 2 | 36,315 | 6,330 | 29,985 | (running) |
| N=3 | 3 | 3,244,140 | 544,550 | 2,699,590 | 80,155 |
| N=4 | 1 | 660 | 50 | 610 | (running) |
| N=4 | 2 | 217,470 | 9,845 | 207,625 | 4,018 |
| N=5 | 1 | 1,900 | 50 | 1,850 | 30 |

`S_2` fixes the single edge, so every `N = 2` combination is already canonical.

Not searched, and not described as searched:

- `N = 4` cardinality 3. `C(660,3) = 47,574,540` labelled triples.
- `N = 5` cardinalities 2 and 3.
- `N > 5`.
- Templates above the per-cell `K` bound: 0 at `N = 3` (`K ≤ 3` exhausts the pairwise normal forms on three edges), 2,784 at `N = 4`, 393,280 at `N = 5`.
- Repeated copies of one constraint.
- Hypergraph semantics, simplicial semantics, `G > 0`, `S > 0`, `H > 0`, `L > 0`, `O > 2`.
- Any composition other than the product of weights.
- Rise-then-release on the 1,024-state chain.

Singleton sensitivity was exhaustive. It was not run on pairs or triples.

Family indexes committed: `N = 2` (4,042 bytes) and `N = 5` (33,679 bytes). The `N = 3` index is 108,324,385 bytes and the `N = 4` index is 4,911,258 bytes. Both are under `generated/generation-001/` and are gitignored. Their histograms, counts, and selected motifs are in the summary and in `catalogue/motifs/`. Regenerating them is the `rs-lab run` command in the README. On this machine the `N = 3` cell took 169.8 seconds and the `N = 4` cell 35.0 seconds.

## C. Observed results

### Baseline

The unconstrained kernel matched the hypercube walk at every `N`.

| N | Edges | Entropy rate (bits) | Density | Period | Triangle or matching mass | Rise-then-release from empty |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| 2 | 1 | 0 | 1/2 | 2 | — | 0 (a rise of 2 is impossible) |
| 3 | 3 | log2(3) ≈ 1.58496 | 1/2 | 2 | triangle 1/8 | 2/3 |
| 4 | 6 | log2(6) ≈ 2.58496 | 1/2 | 2 | three matchings 3/64 | 0.5556 |
| 5 | 10 | log2(10) ≈ 3.32193 | 1/2 | 2 | not computed | not computed (`1024 > 64`) |

Total variation from the uniform measure is 0 in rational arithmetic and at most `2e-15` in the float64 solves. `N = 5` residuals on the baseline and on all 50 singletons stay at most `2.3e-15`. No Cesàro fallback occurred.

### What a single constraint does

Across `N = 3, 4, 5`, the canonical singletons group by pattern and by sign class. `weak_favour` and `strong_favour` on the same pattern share a modal map. The two suppress grades share a different modal map. `prohibit` is a third family, and it is the one that changes the support. At `N = 5` this accounts for the whole cell: 10 canonical patterns times `{prohibit, suppress, favour}` is 30 families, and the manifest has 30 families, 10 of them structural, 20 with full support, and none equivalent to the baseline.

No singleton at `N > 2` is the baseline kernel. Every enumerated weight differs from 1, and with more than one toggle a non-unit factor changes the normalised row.

At `N = 2` there is only one toggle. Every strictly positive weight normalises to the baseline. The 175 canonical sets (10 + 45 + 120) fall into four families:

| Family | Exemplar | Count | Deadlocks | Period |
| --- | --- | ---: | ---: | --- |
| baseline-equivalent | `form(0-1) => strong_suppress` | 92 | 0 | 2 |
| form prohibited | `form(0-1) => prohibit` | 37 | 1 | 1 |
| dissolve prohibited | `dissolve(0-1) => prohibit` | 37 | 1 | 1 |
| both prohibited | both of the above | 9 | 2 | 1 |

Dissolution shift on all four is 0: with one edge, the only non-halt move is determined, so its probability cannot differ from the baseline. The halt families differ by having an empty admissible set, not by a changed probability on a live toggle. Screened families at `N = 2`: 0. Sensitivity checks: 20 of 20 modal, 20 of 20 support.

### `N = 3` reference rows

Rational stationary values from the same engine, on the canonical labelling.

| Canonical expression | Support | Closing bias | Triangle mass | Density | Entropy (bits) | Rise excess | Reversibility defect |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | full | 0 | 1/8 | 1/2 | 1.585 | 0 | 0 |
| `form(0-1) \| present(0-2) & present(1-2) => strong_favour` | full | +1/9 | 11/64 | 13/24 | 1.543 | 0 | 0.02604 |
| same pattern, `strong_suppress` | full | −2/27 | 3/32 | 17/36 | 1.561 | 0 | 0.01736 |
| same pattern, `prohibit` | cut | −1/9 | 5/64 | 11/24 | 1.512 | 0 | 0.02604 |
| `dissolve(0-1) \| present(0-2) & present(1-2) => strong_favour` | full | 0 | 1/8 | 1/2 | 1.543 | 0 | 0.02604 |
| `form(0-1) \| present(0-2) => strong_favour` | full | +1/9 | 0.17105 | 0.5526 | 1.515 | +0.0556 | 0.01316 |
| same pattern, `strong_suppress` | full | −2/27 | 0.08333 | 0.4524 | 1.530 | −0.0370 | 0.01190 |

The closing probability on the one wedge the three-literal rule matches is `2/3` under `strong_favour` (weights `1, 4, 1`) and `0` under `prohibit`. The bias is the mean over all three wedges, minus `1/3`, so the untouched wedges pull it back to `+1/9` and `−1/9`.

The dissolution rule that fires only on the completed triangle leaves density, triangle mass, closing bias, and the 4-step rise-then-release probability exactly at their baseline values. Total variation from uniform is `1/16`. The entropy rate and the reversibility defect move. Edge-count summaries do not see this rule. The transition measure does.

None of the six reference rules produces a halt. All six keep period 2.

### Cell-wide shape

| Cell | Families | Full support | Structural | Baseline-equivalent | Period 2 only | A halt class | Screened at 0.1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| N=2, K≤3 | 4 | 1 | 3 | 1 | 1 | 3 | 0 |
| N=3, K≤3 | 80,155 | 22,355 | 57,800 | 1 | 80,051 | 104 | 79,731 |
| N=4, K≤2 | 4,018 | 2,103 | 1,915 | 1 | 4,018 | 0 | 3,942 |
| N=5, K≤2, singles | 30 | 20 | 10 | 0 | 30 | 0 | 16 |

The one baseline-equivalent family at `N = 3` contains 64 grammars. Its exemplar is the pair `form(0-1) => strong_favour` together with `form(0-1) => strong_suppress`. The factors are `4` and `1/4`. At `N = 4` the same pair is the exemplar of the null family (20 grammars). The recorded dissolution shift there is `1.1e-16`, float dust on an exactly uniform kernel; see the review log.

At `N = 3` the 104 families whose recurrent classes are all halts are cardinality 3. The extremes are the two uniform prohibitions: `dissolve` on every edge (the completed triangle halts, and nothing can dissolve on the way there; closing bias `+2/3`), and `form` on every edge (the empty state halts; closing bias `−1/3`). `N = 4` at `K ≤ 2` and cardinality at most 2 produced no halt.

Closing bias at `N = 3`, over families, runs from `−1/3` to `+2/3`. The median is about `+0.009`. Dissolution-shift maxima have median `1/3`. Rise-then-release excess has median `0`, minimum `−2/3` (probability 0 against a baseline of `2/3`), maximum `+1/3` (probability 1).

The grammars at that maximum are structural triples of prohibits. One exemplar is `form(0-1) => prohibit`, `form(0-2) | absent(1-2) => prohibit`, `dissolve(1-2) => prohibit`. The grammars at the minimum include the pair `form(0-1) => prohibit` and `form(0-2) => prohibit`, which leaves only one edge free to toggle, so occupation cannot rise by 2. At `N = 4` the rise excess is smaller: median about `+0.004`, maximum `+0.101`, and that maximum is again a pair of formation prohibits.

## D. Behavioural families

The family id is the modal map together with the support map. Inside this census the modal map of a single constraint is fixed by its pattern and its sign class. Grade magnitude changes entropy, density, total variation, and defects, and it does not change the family.

Tags, as counts in the table above:

- `baseline-equivalent` — successor list equal to the baseline, including reciprocal grades whose product is 1.
- `structural` — at least one toggle removed. In this grammar that means a `prohibit` that actually matches some state.
- `measure` — full support, kernel not the baseline. Soft weights live here.
- `screened` — a predeclared flag fired. At `N = 3` and `N = 4` this is nearly the whole cell, because a weak grade already moves some toggle probability by more than 0.1. The flag is not a rare-event marker. Quantiles are in the summary under `family_histogram`.

Period splits the structural families further. Most support cuts leave a period-2 recurrent class. A halt class appears when the cuts leave some state with no toggle, and the 104 `N = 3` families with only period 1 are those whose every recurrent component is a halt.

## E. Minimal constraint motifs

Recorded motifs are the deterministic selection in `catalogue/motifs/`, capped at 48 per cell. The following are minimal for the behaviour named, in the sense that the census did not show a smaller cardinality doing the same thing.

| Behaviour | Smallest grammar observed | Coordinate |
| --- | --- | --- |
| Identical to the baseline, despite non-unit weights | any strictly positive weight | `N=2`, cardinality 1 |
| Identical to the baseline at `N>2` | reciprocal grades on one action, e.g. strong favour with strong suppress | cardinality 2 |
| One halt, the empty state forced | `form(0-1) => prohibit` | `N=2`, cardinality 1. At `N=3` a single form-prohibit does not halt the empty state |
| Both states halted | form-prohibit and dissolve-prohibit on the only edge | `N=2`, cardinality 2 |
| Support no longer the full hypercube | any matching `prohibit` | cardinality 1 |
| Triangle mass moved to 11/64, chain still irreducible and period 2 | the three-literal strong favour of the missing edge | `N=3`, cardinality 1, `K=3` |
| Occupation statistics unchanged while entropy and reversibility move | strong favour of one dissolution, conditioned on the other two edges | `N=3`, cardinality 1, `K=3` |
| Every recurrent class is a halt | three formation prohibits, or three dissolution prohibits | `N=3`, cardinality 3 |
| Rise-then-release probability driven from 2/3 to 0 or to 1 | pairs or triples of prohibits that trap the walk | cardinality 2 or 3, structural |

Soft grades do not appear in the rows that create halts, change period, or push the short path probability to 0 or 1.

## F. Parameter robustness

On every singleton, changing the base from 2 to 3 or 4 left the modal map and the support unchanged. Checks and matches: `N=2` 20/20, `N=3` 120/120, `N=4` 100/100, `N=5` 100/100.

What does change with the base, and with the grade inside a sign, is the numerical kernel. The closing probability on the favoured wedge is `2/3` at base 2 with grade `+2` (factor 4). The same grades at base 4 use factor 16 and a larger probability. The sign of that one-wedge difference from `1/3` is stable for this isolated rule. The census does not claim that every probability difference from the baseline keeps its sign once several constraints share a row and the row is normalised.

The algebraic identity `strong_favour × strong_suppress = 1` is independent of any further parameter. It is why that pair is baseline-equivalent on every edge.

## G. Unexpected findings

- Reciprocal grades are an ordinary member of the grammar, and they are the entire baseline-equivalent family once `N > 2`. A constraint set can cancel.
- A rule supported only on the completed triangle is invisible to density, triangle mass, closing bias, and the 4-step rise-then-release probability, and visible to entropy rate, total variation (`1/16`), and the reversibility defect.
- The soft three-literal closing favour moves triangle mass from `1/8` to `11/64` and leaves the 4-step rise-then-release probability exactly at `2/3`. Stationary occupation and the short path predicate come apart.
- The extreme values of that path predicate are hard truncations of the hypercube: forbid two formations and the walk cannot gain two edges; forbid every dissolution and the walk cannot fall.
- `N = 4` with `K ≤ 2` and at most two constraints produced 9,845 canonical pairs, 4,018 families, and not a single halt.
- Canonical state counts reproduce the number of undirected graphs on `N` vertices (2, 4, 11, 34).

## H. Inferences

These are inferences about the formal system, from the observations above.

The multiplicative monoid is doing the work that a longer effect vocabulary would have named. Sign class and the zero element organise the modal catalogue. Magnitude is a knob inside a sign class. `prohibit` is not a sixth soft grade; it is the element that changes the support graph, the period, and the existence of halts.

Memoryless pairwise reweighting is enough to move stationary mass on a completed triangle, to break reversibility, and to lower the entropy rate, with the chain still irreducible and period 2. It is not enough, in the cells searched, to make the predeclared 4-step rise-then-release event more or less likely for the same three-literal closing rule. That event's large deviations are properties of the support, not of the soft weights.

Edge-count observables are a coarse projection. Two kernels can share them and differ as transition measures. Entropy rate and the reversibility defect distinguished a case that density and triangle mass did not.

A set of constraints is not a cumulative list. The smallest baseline-equivalent object at `N > 2` is a pair whose factors multiply to the identity.

## I. RS / global-coherence interpretation

Under the working premises, the split just observed is coherent with a distinction between admissibility and tendency. Hard zeros decide which relational transitions exist. Positive grades decide their relative weight. The laboratory did not derive that distinction from the premises. The grammar exhibited it, and the distinction is one a designed runtime could reuse. That is an interpretation of a formal fact, not a certificate of the premises.

The rise in stationary mass on the three-edge state, from `1/8` to `11/64` under one soft rule, is a local increase in occupation of a completed relational pattern. It sits comfortably beside the older word "closure" only as a gloss. The chain did not become absorbing, the period stayed 2, and the empty state remained able to reach the triangle. Nothing in the run warrants treating that mass shift as closure in the sense used by the archived programme.

The same rule did not produce a short-horizon excess of rise-then-fall. The dissolution rule aimed at the completed triangle preserved occupation and still rearranged the leaving edge. Neither observation is the sequence "organisation, completion, dissolution, released possibility, reorganisation." That sequence was not isolated in this grammar. The hope that constructive dissolution would already be the generic behaviour of the smallest memoryless pairwise rules is in tension with this census. The tension is local to this coordinate. It does not reach the working premises.

No operational boundary was measured. Component count is in the heavy record. A partition score was not defined, and none is inferred here.

Cross-substrate recurrence was not tested. Hypergraph and simplicial runs were refused rather than simulated with pairs.

## J. Tensions and negative findings

- The 0.1 screens flag almost every non-null family at `N = 3` and `N = 4`. They do not pick out a special subset. The histograms do.
- Soft path-closing leaves the rise-then-release probability exactly where the baseline put it.
- The path predicate's dramatic values are produced by deleting transitions, which is the behaviour one would expect from a smaller graph, not a new kind of trajectory inside the full graph.
- Cancelling pairs undo a constraint. Reading a set as "more constraints, more effect" is not supported.
- `K ≤ 2` and cardinality ≤ 2 do not halt the 64-state chain. Freezing that chain needs a larger cardinality, a larger `K`, or a different literal.
- There is no baseline-equivalent singleton at `N = 5`. Pairs were not searched there, so the cancelling-pair family was not given a chance to appear. That is a limit of the cell, not evidence against the identity.
- Float dust of one ulp appears on the `N = 4` cancel pair's shift column.
- The bulk family indexes are not in the git object store. A reader who clones the branch has the counts, the histograms, the singleton tables, and the motifs, and regenerates the indexes from the specification.

## K. Next bounded experiment

The smallest justified increase is one new condition literal, still at `N = 3`, `H = 0`, `L = 0`, `G = 0`, graph semantics, exact rational arithmetic.

The literal is an occupation threshold, schematically `count_at_least(2)`, allowed as a condition on `form` or `dissolve`. The current grammar can name "the other two specific edges are present," which fires only on the completed triangle. It cannot say "at least two edges are present," which would also fire on the two-edge states. The triangle-only dissolution rule left the rise-then-release probability and the triangle mass unmoved. A threshold that fires one step earlier is the smallest expression the present census cannot already say.

Bound the cell to cardinalities `{1, 2}`, a small `K`, and the same weight alphabet, and compare each new rule with the six reference rows already measured. Do not retune Generation 1. If the threshold cell is searched, record it as Generation 2.

The following stay larger than that step, and wait:

- `H = 1` at `N = 3`, which enlarges the state the kernel reads.
- One irreducible triadic hyperrelation, as its own semantics.
- `N = 4` triples, after a fresh size calculation.
- Any geometric embedding.

## Commands

From `constraint-lab/`, with the package installed:

```bash
rs-lab inspect-space experiments/specs/generation-001.json
rs-lab enumerate states experiments/specs/generation-001.json --n 3
rs-lab enumerate constraints experiments/specs/generation-001.json --n 3
rs-lab run experiments/specs/generation-001.json --out generated/generation-001 --publish .
rs-lab report experiments/manifests/generation-001-pregeometric-pairwise-summary.json
rs-lab replay exemplars/01fce7a65bc87c75.json
rs-lab compare experiments/manifests/generation-001-pregeometric-pairwise-summary.json 075e55aaad9f376b
```

The compare id is the family id of the canonical three-literal strong-favour rule. The replay file is a Generation 0 trace: `dissolve(0-1) => prohibit`, `N = 3`, complete initial state, horizon 16, seed 0. Replaying it reproduced 16 events and final state 7. Generation 1 traces in the same directory use horizon 32.
