# Generation 007B design passes

These vectors are ordinal design-selection scores on a `0–5` scale. Higher is better. They are not empirical facts, probabilities, or a confidence score. They are not summed. The external vector and the Grok vector are not averaged.

Dimensions:

```text
CI  causal isolation
CF  control fairness / comparability
CB  computational boundedness
IN  interpretability
IG  expected information gain
CR  resistance to confounding
PR  provenance / reproducibility clarity
```

The question being designed for is the gap left by Generation 7. A one-parameter pair-face rule matched each passage direction and matched none of them jointly. The question is the smallest explicit lower-order transition law that can reproduce the higher-order singleton's two-direction aggregate effect, how stable and unique that representation is, and what remains different after it is achieved.

Ontology stays fixed: `N = 4`, `O = 3`, `G = S = H = L = 0`, independent hypergraph. No second passage, no simplicial semantics, no history, no geometry, and no larger system in this round.

Generation 007 design passes are not edited. This file is the 007B record.

## Pass 1 — before implementation

Written before the two-level executor and before any composed-system margin is read. Costs below are counts from the existing Generation 6 catalogue view, not kernel timings.

### Catalogue check

The live pair-face set was recomputed from `graded_catalogue` through `_catalogue_view` and `_live_controls`. It was not taken from prose.

```text
target cells                         28
logical pair-face problems           42
unique two-level control structures   4
unique target singleton keys         20
```

The 42 problems are the live, non-duplicate pair faces on the 28 predeclared cells. `contains_t_action_edge` contributes adjacent faces only. `contains_p_companion_edge` contributes adjacent and disjoint faces. Both polarities occur. The four structures are the distinct `(action, face, on-bit)` identities after canonicalisation. Named grades do not change the control structure. They do change `Delta_T`, so the 42 residual problems stay distinct.

Each live face condition is one pair slot. Each target gate is one condition on a three-entity slot, one dissolve action, and one named weight. The complement of `present(f)` is `absent(f)` on that same pair slot, and the reverse. Exactly one of those two literals holds in any state where the action edge is admissible, because a condition on the action edge is not a live face.

### Complexity vectors

Checked against that catalogue and frozen. The coordinates are not added.

```text
[
  maximum predicate order,
  rule count,
  free scalar weights,
  condition partition size,
  action-edge count,
  history depth,
  geometry requirement
]
```

The third coordinate is the number of free scalar action weights in the law. For the target that weight is the named grade. For the two-level control both weights are fitted. It is not a fitted-versus-named score, and it is not a sum.

Higher-order singleton:

```text
[3, 1, 1, 2, 1, 0, 0]
```

Two-level pair-face control:

```text
[2, 2, 2, 2, 1, 0, 0]
```

The target predicate order is 3 because the condition names a triad. The control predicate order is 2 because both complementary literals name a pair. Partition size is 2 in both laws: the conditioned bit and its complement. History depth and geometry requirement are 0.

### External vector

The externally selected candidate is A, the two-level complementary pair-face control.

```text
CI 4
CF 4
CB 4
IN 4
IG 5
CR 4
PR 5
```

External rationale, recorded and not rescored by averaging:

- CI 4: the control changes only lower-order representational capacity and adds one degree of freedom.
- CF 4: it is a fairer two-direction lower-order comparator, and it is more parameter-rich than the target.
- CB 4: 2-D calibration is more expensive, and the supervisor bounds it.
- IN 4: two fitted parameters and possibly multiple solutions remain interpretable, and less simple.
- IG 5: it directly addresses the measured scalar representability failure.
- CR 4: extra flexibility can overfit the two aggregate observables. State shape and robustness are required.
- PR 5: the micro-batch platform can make every evaluation durable.

### Grok vector

Assigned independently, before implementation. The A row matches the external vector coordinate by coordinate. That match is agreement. It is not an average.

| Candidate | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A. Two-level complementary pair-face | 4 | 4 | 4 | 4 | 5 | 4 | 5 |
| B. Two live pair-face predicates, one multiplier each | 3 | 3 | 3 | 3 | 3 | 3 | 4 |
| C. Unconditional base multiplier plus one pair-face modifier | 3 | 3 | 4 | 2 | 4 | 2 | 4 |
| D. Skip richer controls and move to graph-class routing | 2 | 3 | 4 | 3 | 2 | 2 | 4 |
| E. Stop discriminating tests and enter open exploration | 5 | 4 | 5 | 4 | 2 | 4 | 5 |

### Why these scores

Candidate A keeps the failed scalar's predicate, action edge, and action direction, and replaces the single conditional level plus neutral complement with two complementary levels. The added object is one scalar degree of freedom. CI stays 4 because that degree of freedom is real. CF stays 4 because the control can now aim at both aggregate directions, while it has more free weights than the target. CB stays 4 because every `(m_off, m_on)` evaluation is a scheduler item and the adaptive cap is finite, and a two-dimensional search is still more work than Generation 7. IN stays 4 because `m_off` and `m_on` are identifiable if exactly one rule is active, and multiple basins would make the reading less simple. IG is 5 because Generation 7 already measured `0 / 42` joint pair-face matches. CR stays 4 because two aggregate numbers can be fit without reproducing state shape or selectivity. PR is 5 only if the DiskBook rule is kept: a missing point requests an item and returns.

Candidate B adds a second predicate as well as a second multiplier. That is a larger representational change than the failed control needs. CI, CF, IN, IG, and CR are all 3. CB is 3 because two predicates do not share one complementary partition and the search is less local to the measured gap. PR is 4.

Candidate C can be rewritten as `(m_off, m_on)`, in which case it is candidate A with a less direct parameterisation. Left as an overlapping product, the two factors are not separately identifiable. IN is 2 and CR is 2. IG is 4 because it still targets the joint gap. It is not executed. If a product form appears in the engine, the scientific report must still publish `m_off` and `m_on`.

Candidate D leaves the measured `0 / 42` joint gap untested. IG is 2. CI and CR are 2 because the passage changes before this representation question is answered. Graph-class routing remains the later fork already named in Generation 7 Pass 4. It is not executed here.

Candidate E is a coherent future mode, documented in `docs/inquiry-modes.md`. CI, CB, and PR are high because it would not pretend to answer the pair-face gap. IG is 2 on the question this round is for, because the joint representability gap would stay open. Mode B is not started.

### What drove the selection

The selected design remains candidate A. No coordinate of A was changed to follow the external vector. The alternatives are scored and not executed.

Rejected for this round:

- A second pair predicate.
- An overlapping unconditional-times-conditional product, unless rewritten into `(m_off, m_on)` and reported that way.
- Graph-class routing before the two-level census.
- Open exploration as the 007B execution.

### Frozen rules before any census

These are selection and accounting rules. They are not results.

```text
positive domain          1e-4 <= m_off, m_on <= 1e4
zero boundary            m_off = 0, m_on = 0, and the corner (0, 0), where a basin reaches the positive edge
coarse positive axis     1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000, 10000
coarse points            9 x 9 = 81 per unique structure
initial atomic items     81 * 4 + 20 = 344
match tolerance          1e-8, kept only if the two-level numerical reference stays below 1e-10
adaptive cap             250 new points per logical problem
unresolved status        unresolved_at_cap
cluster rule             max(|log10(m_off ratio)|, |log10(m_on ratio)|) <= 0.02
max initial basins       12, smallest joint-distance components kept, truncation recorded
newton entry             both log10 widths <= 0.05
stencil                  at most 5 new points in one basin wave
poor conditioning        condition number > 1e6, or Jacobian not estimated
small solution family    at most 8; above that, composition uses nearest nominal, nearest neutral, and most distant finite solution
primary selection        both components inside tolerance; then smallest max(|ln(m/nominal)|); then smallest Euclidean ln distance to (nominal, nominal); then parameter text
D_neutral                sqrt(ln(m_off)^2 + ln(m_on)^2), descriptive, not a selector
log in the selector      natural logarithm; the argmin is unchanged by a change of base
```

The primary solution is the least departure from the named scalar pair-face law. It is not the solution with the most favourable later `M_I`.

Representation labels, not grades:

```text
R0  no representation in the domain
R1  boundary-only representation
R2  unique well-conditioned finite interior representation
R3  multiple finite representations
R4  finite but poorly conditioned, or Jacobian not estimated
```

Exclusive assignment: R0 if the search finishes with no point inside tolerance; otherwise R1 if every solution is on the positive domain edge or at zero; otherwise R3 if two or more clustered solutions remain; otherwise R4 if the selected solution has condition number above `1e6` or no Jacobian; otherwise R2.

Preflight, representability and cost only, before the 42-problem census:

```text
polarity absent, all live faces, grades
  prohibit/prohibit
  strong_suppress/strong_suppress
  strong_favour/strong_favour
  strong_suppress/strong_favour
polarity present, all live faces, grade prohibit/prohibit
```

That set touches both geometries and all four control structures. It does not read `M_I` or `M_G`.

Robustness, after representation is frozen, not during preflight:

```text
rho3 = 1/2 and rho3 = 2
fixed selected parameters, and a separate recalibration
no W3 or W16 alphabet probe
```

The robustness rows are one structurally distinct face from each of the four control structures, plus the strong grade anchors on the absent adjacent and absent disjoint faces. The exact row list is frozen in the specification before the census.

### Factual uncertainties that can change a coordinate

- The number of sign-enclosing cells is not yet measured. A large number of basins would lower IN and CR. The cap of 12 initial basins records truncation rather than hiding it.
- A two-parameter fit of two aggregate numbers can succeed while state shape stays poor. That would lower CR of any later magnitude claim. It is an expected observation to report, not a reason to add a third parameter in advance.
- Jacobian conditioning is not yet measured. A nearly singular solution is R4, not a strong representation.
- Numerical noise of the two-rule kernel is not yet measured. The tolerance stays `1e-8` only if the reference gap remains below `1e-10`. It is not loosened because the search is two-dimensional.
- Batch size is not yet measured. Generation 7's 142-item multiplier batch is not reused.

Pass 1 is not rewritten by later passes.

## Pass 2 — after the 2-D preflight

Written after the representability preflight. No `M_I` or `M_G` was read. The preflight scheduled 1,361 pair-point items and 8 target singletons. It scheduled no composition item.

The vector is unchanged. The evidence below is why it did not move.

```text
CI 4
CF 4
CB 4
IN 4
IG 5
CR 4
PR 5
```

Candidate A remains the selected design. No third parameter is added. Mode B is not started.

### What the preflight did

Root `generated/generation-007b-preflight`. Fifteen logical problems, four structures, both geometries, both polarities on the prohibit anchor, and the absent-polarity grades named in Pass 1.

Two planner corrections were required before this reading, and both are in the code the census will run.

- A nominal of zero has no logarithm. Selection now uses Generation 7's `log_distance`: deletion ranks ahead of every positive multiplier, and positive candidates are then ordered by the multiplier itself. The smoke cell is the prohibit grade. It closed as one represented calibration. That cell is not part of this preflight score.
- Newton starts only when both log10 widths are at most 0.05. An empty subdivision stencil stays in subdivision. A missing Jacobian sample is requested. It is not treated as an exhausted basin.

The first preflight supervisor, `2026-10-12T12:34:12Z` to `2026-10-12T12:37:47Z`, left two adjacent `strong_favour` / `strong_favour` problems unrepresented. Their best stored point was `m_off = m_on = 2.539650767410e+0`, with component mismatches about `1.82e-8` and `7.29e-8`, outside `1e-8`. The basin exhausted with `jacobian = null` because the finite-difference sample around the current best was missing. Those two calibration files were removed. The stored points were kept. The second supervisor, `2026-10-12T12:42:10Z` to `2026-10-12T12:42:35Z`, evaluated 54 new shared pair points and represented both. The corrected preflight is the record used here. The first label was a solver stop.

Corrected terminal state: 1,369 / 1,369 items, 15 / 15 calibrations, 0 unresolved, 0 timeouts, 0 retries, 0 quarantines. Seventy-one batch receipts. Median batch wall, index `n // 2`, is 2.435 s. Nearest-rank p90 is 13.020 s. Maximum is 36.043 s. Two batches exceeded 30 s. None exceeded 60 s. Two starts, one stale-lock recovery, no supervisor error.

### Representability on these 15 problems

```text
R2  15
R0   0
R1   0
R3   0
R4   0
```

Every problem has `solution_count = 1`. Every selected solution is a finite interior point. None is on the zero boundary. No basin list was truncated. Each problem opened 12 search basins; that is the search cap, and it is not 12 solutions. Condition numbers of the selected solutions run from 2.227 to 41.661. All are estimated. The largest absolute component mismatch is `2.13e-9`, inside `1e-8`. The two-level numerical reference gap remains 0, so the tolerance stays `1e-8`.

On every one of these 15 problems the selected solution has `m_off = m_on`.

```text
prohibit / prohibit                         3.090231392163e-1
strong_suppress / strong_suppress           1.102087305612e+0
strong_suppress / strong_favour             1.102087305612e+0
strong_favour / strong_favour               2.539633224184e+0
```

The same value appears for every geometry, relation, and polarity in that grade inside this preflight. Prohibit does not select zero. The two-level search had a second free multiplier and the aggregate match did not use it. This is a preflight observation. It is not yet the 42-problem census.

Adaptive counts on the stored calibrations run from 54 to 172, against the cap of 250. The sum of those counts is 1,896. Unique adaptive pair items are 1,037 (`1,361 - 4 × 81`). Repeated requests across problems that share a control structure did not become repeated kernel items.

### Why the coordinates stay

- CB stays 4. The 2-D search is bounded: the preflight finished, the adaptive cap was not reached, and no batch approached the 120 s watchdog. It is not raised. Twelve search basins per problem, and the census still has composition and robustness ahead.
- IN stays 4. The in-tolerance solution is unique and the condition numbers are modest, which is simpler than a large equivalence family. The law still has two named multipliers, and the search still opens 12 basins. Equality of the selected multipliers is interpretable. It does not make the design a one-parameter experiment.
- CR stays 4. Local identification is present: the Jacobian is estimated and far from the `1e6` limit, and there is not a cloud of distinct in-tolerance roots. The aggregate match lying on `m_off = m_on` means these two observables did not require a pair-conditioned split. State shape is not part of preflight, so the concern that two aggregate numbers can be fit without the internal transition structure remains.
- CF stays 4. The control can represent both directions on this set, and the selected points do not spend the extra parameter. The target still has one named weight. The comparison remains more parameter-rich at the level of the law.
- PR stays 5. Both supervisor runs, the stale lock, the 54 resumed points, and the corrected calibrations are on disk. The first unrepresented label is recorded as a solver stop rather than overwritten without comment.
- CI stays 4 and IG stays 5. The preflight answers the cost and representability questions that Pass 1 left open. It does not change what the control is allowed to alter.

### What Pass 2 does not do

It does not rewrite Pass 1. It does not add a parameter. It does not move to graph-class routing or to open exploration. It does not treat the diagonal solutions as a census result. The census is the next measurement.

## Pass 3 — after the representability census

Written after the 42-problem census, the composition items, the state-shape join, and the robustness probes were durable. Pass 1 and Pass 2 are not rewritten.

The census represents every aggregate two-direction vector inside `1e-8`. Thirty-two calibrations have one in-tolerance solution. Ten disjoint calibrations have two. All 52 stored solutions are finite interior points with `m_off = m_on`, estimated Jacobians, and condition numbers from 2.227 to 90.73. None is poorly conditioned. None is zero. The adaptive cap was not reached.

Four adjacent `weak_favour` / `weak_favour` calibrations, both geometries and both polarities, are labeled R2. A second diagonal root near `1.544233607966e+0` is stored on the disjoint twin of the same `contains_p` target, inside tolerance, and Generation 7's joint erasure selected that magnitude. On the adjacent structures the coarse cell from `m = 1` to `m = 10` is sign-enclosing and shares a connected component with the cell that refined to `1.757429855532e-1`, because an off-diagonal coarse cell also encloses. Refinement followed the nearer corner. `basins_truncated` is false: the detector did not drop a thirteenth initial basin. The R2 label on those four cells means one solution among the basins the frozen rule opened.

Composition is a single number on the 32 single-solution calibrations. On the 10 dual calibrations it is a range. `I_C2` changes sign across the two roots in 8 of 20 direction-cases. `G_C2` changes sign in 2 of 20. Those signs are non-identifiable from the aggregate match.

State shape stays poorly matched on all 84 direction reports, for the two-level law and for the Generation 7 erasure baseline. Selected controls stay numerically triad-flat. Targets do not.

```text
CI 4
CF 4
CB 4
IN 3
IG 5
CR 3
PR 5
```

- CI stays 4. The control still changes only lower-order representational capacity.
- CF stays 4. The law still has two parameter slots. The fitted points set them equal, and the target still has one named weight.
- CB stays 4. The census finished inside the cap and inside the watchdog. It is not raised: twelve search basins and the connected-component merge left a known diagonal root unrefined on four cells.
- IN moves from 4 to 3. The diagonal reading is clear. Uniqueness is conditional on the searched component for four cells, and ten cells have two roots whose composition differs.
- IG stays 5. The census answers the two-direction representability question that Generation 7 left open for the pair face.
- CR moves from 4 to 3. The aggregate match does not identify composition sign on part of the dual set, and a coarse-cell merge can hide a second diagonal root.
- PR stays 5. The evaluations, the merged component, the disjoint twin, and the Generation 7 baseline are on disk.

No third parameter is added. The aggregate gap that justified candidate A is closed on the searched points, and the unused split is the reason to stop this parameter sequence rather than extend it. Mode B is not started.

## Pass 4 — after composition and state shape

Written after the same durable merge. The question is which fork the evidence supports. Scores are independent. They are not summed and not averaged.

| Fork | CI | CF | CB | IN | IG | CR | PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Stop this lower-order parameter sequence | 5 | 5 | 5 | 4 | 4 | 5 | 5 |
| A third lower-order parameter | 2 | 2 | 3 | 2 | 1 | 1 | 4 |
| Multi-destination graph routing | 3 | 3 | 4 | 3 | 3 | 3 | 4 |
| Open relational exploration | 5 | 4 | 5 | 4 | 3 | 4 | 5 |
| Simplicial semantics | 2 | 2 | 3 | 2 | 2 | 2 | 3 |
| Larger N or a new ontology | 2 | 2 | 2 | 2 | 1 | 2 | 3 |

Stop this sequence. Every in-tolerance solution found lies on `m_off = m_on`. The extra pair-conditioned level was searched and the aggregate match did not use an unequal split. State shape stays poorly matched. Triad selectivity stays on the target. A third scalar would be aimed at residuals the two aggregate numbers do not identify. That is interpolation. The complexity stopping rule in the report says to stop.

A later discriminating test would need a different predeclared observable, such as state shape or selectivity, with its own control and its own tolerance. It is not another multiplier on the same two passage numbers.

Graph routing, simplicial semantics, and a larger ontology are different questions. This census does not start them.

Open exploration remains the documented future mode in `docs/inquiry-modes.md`. Its score is high where it refuses to disguise itself as a pass/fail test. It is not executed in 007B. The exploratory engine is not implemented.
