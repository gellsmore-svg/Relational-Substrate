# Generation 004a — reconfiguration sensitivity

Engine `0.4.0` on this cell. Semantic version `0.4.0`. Analysis version `0.5.0`. Grammar `independent-hypergraph-v1`. Normalisation `structural-unique-v1`.
Specification hash `9ec57d9ffa21c83a824650b4397f541daee40aed3eb327b4c304571ff4075fec`.
Python 3.12.3, NumPy 2.5.3, platform `linux`.
Summary SHA-256 `2fb9601c2968c54781384f98ae34e3e549c397c9d4af4ad5bfc526244bd1561c`.
Row table SHA-256 `c201f540597fbd4e7063e6be437abf0804c510cfa98407701bbfe8934ee50c9f` (`reports/tables/generation-004a-reconfiguration-sensitivity-singles-n4-k2.csv`, 161 lines including the header, 269,098 bytes).
Plan git commit `1c7726f8d431ea54baeb478bf2171d0703046ea2`. The summary field `git_commit` is that commit. The plan was written before this report.

This is a reanalysis of the 160 canonical weighted singletons from Generation 4. It does not replace Generation 4, and it does not edit that report, that specification, or those artifacts. The Generation 4 horizon-16 stationary passage and the structurally zero one-step flux stay as they were published.

Stationary distributions and committors in this reanalysis are float64. The largest primary stationary residual across the 160 rows is `3.531246475785288e-15`. These solutions are numerical.

## A. Why this reanalysis

Generation 4 fixed two observables before its census. The one-step same-edge-count flux is identically zero, because one pair event toggles one pair bit and the edge count changes by one. The horizon-16 hit-before-return between the two-edge path (`e2-deg2110-tri0-comp2`) and the two-edge matching (`e2-deg1111-tri0-comp2`) does move. The Generation 4 sensitivity probes recomputed the clocks, the jump boolean, the support, the modal toggle, and the one-step flux. They did not recompute the horizon-16 passage. That missing recomputation is the first job of this cell.

The second job is to separate two effects that the Generation 4 passage mixes. The historical quantity starts from each kernel's own stationary pair-event distribution conditioned on the source class. A constraint can change which full states are occupied when that class is seen, and it can change the future transitions from a given full state. Both are real. They are now recorded separately.

The third job is a horizon-independent eventual hit-before-return committor on the pair-event epoch kernel. Horizon 16 stays as the historical comparator. It is not replaced, and it is not retuned.

```text
N=4  O=3  G=0  S=0  H=0  L=0
cardinality 1
160 canonical weighted singletons
independent hypergraph
```

## B. Measures

`STATIONARY_SOURCE_PASSAGE` is the Generation 4 quantity. For a constrained kernel `C` it uses `C`'s own pair-event stationary distribution, conditioned on the source class. Its definition is unchanged.

`CONTROLLED_SOURCE_PASSAGE` uses one reference distribution `mu_ref`: the unconstrained baseline's pair-event stationary distribution, conditioned on the full states whose visible pairwise graph is the source class. The same `mu_ref` is used for the baseline and for the constrained kernel. The constrained stationary source is not substituted, and it is not used as a renormalisation of `mu_ref`.

The occupancy contribution is the descriptive difference

```text
Q_stationary(C) - Q_controlled(C)
```

on a shared target and source class. It is a difference of two defined quantities. It is not a unique causal split.

For each full source state `s` in the source class, `delta_q(s) = q_C(s) - q_0(s)` on the eventual committor. Each durable shard row stores, for the primary alphabet and `rho3 = 1`, the baseline-source-weighted mean, the maximum positive and maximum negative values, the full states and triadic configurations that attain them, and the range across the 16 triadic configurations. The published CSV stores the class-level aggregates. The full length-1,024 committor array is not written for these 160 rows.

The eventual committor is the probability of reaching the target class before returning to the source class, after at least one pair event. It is solved on the pair-event epoch kernel by `numpy.linalg.solve` on the transient block. Float64 solutions are not called exact. The solver name, dimension, and residual are stored on the primary direction. Horizon 16 remains the finite comparator. No other horizon is used.

The effect floor is `1e-8`. It was written into the specification before this census. On the reference kernels used to choose it, the largest block-versus-dense landing gap was `5.55e-17`, the largest stationary residual was `8.40e-16`, the largest committor residual was `1.78e-15`, and the largest statewise committor gap was `4.44e-16`. Committor condition numbers on those kernels were between 10 and 14. The floor is the existing float total-variation floor, about four orders of magnitude above a pessimistic thousand-fold amplification of the measured committor residual.

The one-step scalar `max_abs_stationary_pair_event_class_flux_delta` is not a success criterion here. Under the independent-hypergraph event model, one pair event toggles exactly one pair bit, so the pairwise edge count changes by exactly one, at every constraint cardinality. The same-edge-count one-step flux stays a structural invariant.

## C. Execution

Analysis `n4-reconfiguration-sensitivity`. Specification `experiments/specs/generation-004a.json`.

| Item | Value |
| --- | --- |
| Rows | 160 |
| Classes | `P->P` 50, `P->T` 40, `T->P` 40, `T->T` 30 |
| Shards | 10 |
| Shard items | 200 |
| Workers | 2 |
| Failed | 0 |
| Quarantined | 0 |
| Status | COMPLETE |
| Wall | 132.8163948400179 s |
| Shard work | 236.631408 s |
| Epoch solver | block |
| Largest stationary residual | 3.531246475785288e-15 |

Probes, each against the unconstrained baseline at the same alphabet and the same `rho3`:

```text
primary:  W4, rho3 = 1
rho:      rho3 = 1/2 and rho3 = 2, alphabet W4
alphabet: W3 and W16, rho3 = 1
```

The horizon-16 probes recompute the stationary passage and the controlled passage. They do not recompute the eventual committor. Robustness is claimed only for the quantities those probes recompute.

Every row shares one primary baseline hit: path to matching `0.18311749702578972`, matching to path `0.7324699881031586`. The same pair of values, to about `1e-15`, is the matched baseline at `rho3 = 1/2`, `rho3 = 2`, `W3`, and `W16`. On the unconstrained kernel the focused pair-event passage is insensitive to these rate and alphabet changes at the recorded precision. Constrained deltas still use the matched baseline of that probe.

Unresolved mass at horizon 16, over both directions and all 160 primary rows, stays between `0.002468396086067202` and `0.08738005930475529`. No row is a finite mean first-passage time.

## D. Horizon-16 sensitivity

Counts of rows with absolute delta above `1e-8`. The same counts hold for the stationary passage, the controlled passage, and the triadic-spread flag, on both directions, at primary, `rho3 = 1/2`, `rho3 = 2`, `W3`, and `W16`.

| Class | Rows | Nonzero passage | Triad changes the hit |
| --- | ---: | ---: | ---: |
| `P->P` | 50 | 50 | 0 |
| `T->P` | 40 | 40 | 40 |
| `P->T` | 40 | 0 | 0 |
| `T->T` | 30 | 0 | 0 |

The Generation 4 qualitative pattern survives every predeclared probe: every `P->P` and every `T->P` singleton moves the focused passage relative to the matched baseline, every `T->P` singleton makes that passage depend on the hidden triadic configuration, and `P->T` and `T->T` stay inside the floor.

Primary signs of the stationary horizon-16 delta reproduce Generation 4. Path to matching: `P->P` 29 negative and 21 positive; `T->P` 24 negative and 16 positive. Matching to path: `P->P` 31 negative and 19 positive; `T->P` 24 negative and 16 positive.

The sign is stable across all five probes on 48 of 50 `P->P` rows in each direction, and on 36 of 40 `T->P` rows in each direction. The nonzero status and the triad flag do not change on any row. The four `T->P` rows whose horizon-16 sign moves are the `weak_favour` dissolutions

```text
dissolve(0-1) | absent(0-1-2)
dissolve(0-1) | present(0-1-2)
dissolve(0-1) | absent(0-2-3)
dissolve(0-1) | present(0-2-3)
```

They are positive at `W4` for `rho3` in `{1/2, 1, 2}` and negative at `W3` and `W16`, in both directions. Two `P->P` rows change sign on path to matching, and two other `P->P` rows change sign on matching to path. In each of those cases the move is an alphabet probe, not a `rho3` probe.

Prohibit weights are invariant across `W3`, `W4`, and `W16`: the largest absolute difference of horizon-16 deltas among those three alphabets, over the 32 prohibit rows and both directions, is 0. A nonzero grade moves. For `dissolve(0-1) => strong_suppress`, class `P->P`, the path-to-matching horizon-16 delta is `-0.011019450183154339` at `W4`, `-0.01885405704943849` at `W3`, and `-0.022950880605566937` at `W16`. The matching-to-path deltas are `-0.044077800732617134`, `-0.0754162281977534`, and `-0.09180352242226708`. Of the 128 non-prohibit rows, 72 move the path-to-matching horizon-16 delta by more than the floor under `W3` or `W16`.

`rho3` does not move the largest `P->P` controlled horizon-16 magnitudes at the recorded digits. It does move the largest `T->P` controlled magnitudes by a small amount. Path to matching, maximum absolute controlled delta: `P->P` stays `0.0320331982177209` at all three rates; `T->P` is `0.003352397200209134` at `rho3 = 1`, `0.003441149210169525` at `rho3 = 1/2`, and `0.003416466935476953` at `rho3 = 2`. On every probe the largest `P->P` controlled movement remains larger than the largest `T->P` controlled movement, in both directions. At `W16` the gap is narrower than at `W4` and is still in the same direction: matching to path, `0.06755368449471777` against `0.034917186231842146`.

The Generation 4 reference row `dissolve(0-1) | present(0-2-3) => prohibit`, class `T->P`, is unchanged on the historical stationary passage: path to matching delta `-0.006258155390793857`, triad spread `0.008995800253034175`; matching to path delta `-0.025032621563174984`, triad spread `0.03598320101213692`. Under the controlled source those horizon-16 deltas are `-0.003094193977446036` and `-0.0123767759097837`.

The largest stationary horizon-16 movements remain the Generation 4 `P->P` prohibit rows. Path to matching: `dissolve(0-1) | absent(2-3) => prohibit`, delta `-0.03593449303098292`. Matching to path: `dissolve(0-1) => prohibit`, delta `-0.11970449038888031`. The controlled horizon-16 deltas on those two rows are `-0.02772918657233331` and `-0.03537210026399895`. The second of these is the clearest occupancy example in the historical measure: the stationary delta is `-0.11970449038888031` and the controlled delta is `-0.03537210026399895`, so the descriptive occupancy contribution is about `-0.08433`, roughly seven tenths of the stationary figure.

## E. Controlled source and the eventual committor

The eventual committor is reported at `W4`, `rho3 = 1` only. It was not recomputed on the sensitivity probes.

| Class | Direction | Controlled nonzero | Triad changes eventual | Max abs controlled | Max abs stationary |
| --- | --- | ---: | ---: | ---: | ---: |
| `P->P` | path to matching | 50 | 0 | 0.03065683868166208 | 0.034622761093342586 |
| `T->P` | path to matching | 40 | 40 | 0.0011971123165731568 | 0.0034892884240540767 |
| `P->P` | matching to path | 50 | 0 | 0.041220483357880866 | 0.07027450980392103 |
| `T->P` | matching to path | 40 | 40 | 0.004788449266292405 | 0.013957153696216085 |

`P->T` and `T->T` stay at most a few times `1e-16` on both the controlled and the stationary eventual deltas, in both directions. Their triad-conditioned eventual spread is on that same numerical scale.

Every `T->P` eventual triad spread is above the floor. The smallest path-to-matching spread is `8.085985262007434e-05` and the largest is `0.0013548922071161817`. The smallest matching-to-path spread is `0.0003234394104806304` and the largest is `0.005419568828464727`. The largest spreads belong to `dissolve(0-1) | present(0-2-3) => strong_favour`. The Generation 4 prohibit reference on that same orbit has eventual spreads `0.00044178903709299333` and `0.0017671561483717513`, with controlled deltas `-0.00014811954486698697` and `-0.0005924781794679479`.

The ranking does not reverse. On the controlled eventual committor the strongest `P->P` movement is about 26 times the strongest `T->P` movement on path to matching, and about 8.6 times on matching to path. The same order holds for the stationary eventual committor.

Signs of the eventual controlled delta are not the signs of the horizon-16 stationary delta. Path to matching, eventual: `P->P` 30 negative and 20 positive; `T->P` 32 negative and 8 positive. Matching to path, eventual: `P->P` 30 negative and 20 positive; `T->P` 32 negative and 8 positive. The horizon-16 sign and the eventual sign disagree on 3 of 50 `P->P` rows for path to matching, on 11 of 50 for matching to path, and on 24 of 40 `T->P` rows in each direction. The horizon-16 stationary sign and the horizon-16 controlled sign disagree on 4 `P->P` and 4 `T->P` rows for path to matching, and on 5 `P->P` and 4 `T->P` rows for matching to path. A row can move the passage under every probe and still change sign when the source distribution or the horizon changes. That is a distinction between measures. It is not a loss of the nonzero effect.

## F. Occupancy against future dynamics

For the eventual committor, the median of `|occupancy contribution| / |stationary delta|` on the 40 `T->P` rows is `0.749762376955627` in both directions. The range is `0.5861778688217765` to `1.0402273551834786`. On a typical `T->P` row, most of the stationary eventual shift is the difference between the constrained source occupancy and the baseline source occupancy. The controlled delta remains above the floor on all 40.

On `P->P` the same median is `0.19005288054878527` for path to matching and `0.35235638417220017` for matching to path. Four matching-to-path rows have a ratio above 2. The largest, `20.58452277349036`, is `dissolve(0-1) | absent(0-2) => weak_favour`, whose stationary eventual delta is only `0.00015197905834229974`. A large ratio there is a small stationary denominator, not a large dynamical effect. The controlled delta on that row is `0.0032803954458829887`.

The Generation 4 headline `dissolve(0-1) => prohibit`, matching to path, is the occupancy extreme among the large stationary effects. Stationary eventual delta `-0.07027450980392103`, controlled eventual delta `-0.002332871195615871`, occupancy contribution `-0.06794163860830515`. The controlled eventual movement is above the floor and is about one thirtieth of the stationary eventual movement. The historical horizon-16 stationary delta on this row, `-0.11970449038888031`, was comparing kernels that do not share a source distribution.

For the horizon-16 passage the median occupancy ratio on `T->P` is lower, `0.4591464420893781` in both directions, with range about `0.172` to `5.210`. Occupancy is a substantial part of the historical `T->P` figure and is not the whole of it.

## G. Answers to the five singleton questions

1. All 40 `T->P` singletons alter the eventual path/matching committor in both directions, under the controlled source and under the stationary source. The absolute controlled deltas run up to `0.0011971123165731568` and `0.004788449266292405`. All 40 also alter the horizon-16 passage under every sensitivity probe.
2. Hidden triadic configuration alters the eventual committor on all 40 `T->P` rows, in both directions. The spread is over the 16 configurations in `{0,1}^4`, not over the popcount. The same flag is true for the horizon-16 hit on all 40, under every probe.
3. The ranking of `P->P` against `T->P` does not change when the source is controlled. The largest `P->P` controlled eventual movement remains larger than the largest `T->P` controlled eventual movement, in both directions. The same order holds for the controlled horizon-16 passage at every probe.
4. On the eventual committor, the median `T->P` occupancy share of the stationary delta is about three quarters. On the historical horizon-16 passage the median share is about `0.46`. Individual rows differ. The large matching-to-path stationary effect of `dissolve(0-1) => prohibit` is mostly occupancy. The controlled eventual remainder is small and above the floor.
5. No Generation 4 qualitative conclusion reverses. The passage still moves for every `P->P` and every `T->P` singleton. The hidden triad still conditions every `T->P` passage and no other class in this grammar. `P->P` remains the stronger singleton cause of this particular reconfiguration. `P->T` and `T->T` still sit on the floor. What changes is the size, and on many rows the sign, once occupancy is separated from future dynamics and the finite horizon is replaced by the eventual committor. Those are different quantities. Generation 4 did not claim that its horizon-16 signs were horizon-independent.

## H. Negative findings

- The eventual committor was not recomputed at `rho3 = 1/2`, `rho3 = 2`, `W3`, or `W16`. Whole-census robustness is not claimed for it.
- The one-step same-edge-count flux was not re-ranked. The structural zero stands for this event model at every cardinality.
- `P->T` and `T->T` do not move the focused passage or the eventual committor above the floor.
- No `P->P` row has a triad-conditioned spread above the floor. A pairwise rule moves the passage and does not make that passage depend on the hidden triad.
- Unresolved mass at horizon 16 remains on every row. Means inside the horizon stay truncated.
- The full per-state committor vector is not in the published table. The shard rows keep the state summary: weighted mean, both extrema, and the states and triads that attain them.
- Cardinality 2, simplicial semantics, and `H`, `S`, `G`, `L` above 0 were not introduced.
- Alphabet movement of non-prohibit grades is real. A claim that a `strong_favour` or `strong_suppress` magnitude is alphabet-invariant would be false on these rows.

## I. Inferences

OBSERVED. On these 160 kernels, and on all five horizon-16 probes, passage movement and triadic conditioning split by cross-order class exactly as in Generation 4: 50/50 and 40/40 above the floor, triad flag 0 and 40, and 0/40 plus 0/30 for the other two classes.

OBSERVED. Controlling the source distribution reduces the `T->P` effects and does not remove them. Removing the horizon reduces them further. The strongest singleton movements remain `P->P`.

OBSERVED. For a typical `T->P` row, the stationary eventual delta and the controlled eventual delta differ by more than the controlled delta itself. Source occupancy and future dynamics are both visible in the old number.

INFERRED. Generation 4's statement survives the missing sensitivity and the cleaner mechanistic quantity. A higher-order condition is not necessary for this reconfiguration, and it is not the strongest singleton cause. The hidden triadic configuration does condition the eventual passage on every searched `T->P` singleton. Hidden timing, hidden transition-law information, and hidden topology-conditioned passage information remain three observations. This reanalysis does not test a fourth, the interaction of a `T->P` rule with a `P->P` rule.

## J. RS / global-coherence interpretation

This cell does not establish a globally coherent architecture.

What it adds to Generation 4 is a separation. Part of the published horizon-16 shift was the constraint changing which hidden states carry the source class. Part was the constraint changing the later pair-event law. After that separation, an independent triadic literal still changes an eventual passage between two non-isomorphic pairwise graphs, and an ordinary pairwise literal still changes it more. That remains coherent with treating the higher-order relation as its own primitive, and it still tensions with reading the `T->P` delta as the selector of the lower-order organisation.

## K. Next smallest justified experiment

The singleton layer is now measured on the horizon-16 probes and on the controlled eventual committor. The open question is composition. Generation 5 asks whether one `T->P` rule and one `P->P` rule, canonicalised as a complete set under `S4`, produce an interaction residual on the controlled eventual committor beyond the sum of the two singleton effects, and whether that pair increases the triad-conditioned spread already present in the `T->P` member.

The pool is not the 85,175 canonical cardinality-2 sets, and it is not the label grid `8 × 10 × 2 × 2 = 320`. The exact canonical count is recorded with that census. `H`, `S`, `G`, and `L` stay 0. Simplicial face closure stays a later fork.
