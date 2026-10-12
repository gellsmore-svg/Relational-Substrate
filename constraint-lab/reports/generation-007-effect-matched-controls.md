# Generation 007 — effect-matched controls

Experiment `generation-007-effect-matched-controls`. Analysis version `0.7.0`. Calibration version `0.7.0`. Semantic version `0.4.0`. Specification `experiments/specs/generation-007.json`, sha256 `3bd1164efde699e57784d22ea24c9026e724e134939ff9d4743566cb23e6cf0d`.

The scientific generation is Generation 7. Prompt 007 did not produce a completed generation. This result was produced under Prompt 007R on `research/constraint-lab-v0.7-resumable`, by the micro-batch supervisor, from the reviewed v0.6 head `4deef3aa272a3ceadb5c610fcc95eaa24fde3901`.

The merged summary is gitignored at `constraint-lab/generated/generation-007/merge/summary.json`. It has 28 rows and an index of 3,880 item hashes. Schema `rs-constraint-lab.generation-007-merge/v1`. Verify on 2026-10-12, with `--require-complete`: `ok` true, `complete` true, items 3,880, receipts 238, `missing_completed` empty, orphans empty, quarantined empty, problems empty, 104 calibrations `converged`, spec hash unchanged.

Medians below are the average of the two central stored values. The summary holds the cell values.

## A. Aborted attempt and execution lesson

Prompt 007 ran on `research/constraint-lab-v0.7`. The record is `provenance/executions/007-attempt-1-aborted.md`. Known facts:

- Prompt 007 was executed.
- The run continued for many hours.
- The foreground terminal stopped providing useful visible progress.
- The machine remained computationally active.
- The user could not tell whether the experiment was progressing or hung.
- The run was manually terminated.
- Completion was not established.
- Partial outputs are not accepted as a completed generation without validation.

The established failure is lack of bounded execution and observability. No solver root cause is claimed.

Observed on 2026-10-12, with no `rs_constraint_lab` process running: `progress.json` was `IN_PROGRESS`, started `2026-10-05T10:02:35Z`, last heartbeat `2026-10-05T16:50:14Z`, two shards, two workers, the same spec hash as this generation. Shard `aca9c6ed43cdbb71cb432732` had a running file and no result. Shard `40f54eebb0d913327d887418` had a receipt of 294 seconds and 14 cells, and no per-evaluation item id. Those files stay at `constraint-lab/generated/forensic/generation-007-attempt-1/`. They are not Generation 7 results.

The permanent rule, recorded in the laboratory architecture and in `EXECUTION_BOUNDS`, is that no expensive computation may depend on one long-lived process, that the largest unit of work is the completed computation we are willing to lose, and that another terminal must be able to tell running, progressing, stalled, failed, stopped, complete, and safely resumable apart.

## B. External Review 006

Review 006 is `provenance/reviews/006-chatgpt-review-v0.6.md`. It reads v0.6 at `4deef3aa272a3ceadb5c610fcc95eaa24fde3901` and records Actions run `37193089700` on that head. It is not a review of this generation.

It keeps three v0.6 effects separate: hard deletion is the magnitude peak; generic composition accounts for interaction magnitude at matched nominal weights; the higher-order gate accounts for hidden-state selectivity. It also records the confound this generation is built to test. A condition-erased rule is active in more states than a gated rule, so equal nominal weights are not equal effective singleton strength.

## C. Recursive Pass 1

Two Pass 1 notes are in `docs/generation-007-design-passes.md`, and both are unchanged.

The scientific Pass 1, written before implementation, selected effect-matched erasure, then the adjacent face, then the disjoint face where v0.6 marks it live. Grok's vector for that design was CI 5, CF 4, CB 5, IN 5, IG 5, CR 4, PR 5. CF stayed 4 because an aggregate singleton match is not a state-shape match. CR stayed 4 because forward and reverse multipliers might differ.

The 007R Pass 1, written after the abort and before the supervisor, scored execution architectures. Resume-the-shard was CI 4, CF 4, CB 1, IN 2, IG 4, CR 3, PR 1, and was rejected. The micro-batch supervisor was CI 5, CF 4, CB 5, IN 4, IG 5, CR 4, PR 5. A two-parameter control before the scalar census was CI 3, CF 4, CB 3, IN 3, IG 3, CR 3, PR 4, and was not started. The execution-health expectation was B 5, O 5, R 5, F 5, D 5, T 4.

## D. Resumable execution architecture

The coding agent schedules. The supervisor owns progress. A worker owns one batch and exits.

```text
Grok / user
    |
    v
supervisor
    |
    +-- bounded worker batch
```

An atomic item is one target or control structure, one multiplier `m`, and one rho/alphabet context. It stores the singleton controlled committor in both passage directions, with solver residuals, epoch residuals, and the triad-spread check. Calibrating a whole target is not an item. Root finding reads persisted points and requests a few new evaluations. A worker does not walk a multiplier grid inside one item.

Durable layout, gitignored:

```text
constraint-lab/generated/generation-007/
    plan/  items/  batches/  receipts/  calibration/
    progress/  cache/points/  merge/
```

Each item is written to a temporary file, validated, fsynced, and replaced. A batch receipt is immutable and is written by the supervisor after the worker exits. The receipt proves execution. The item file is the scientific result.

The supervisor heartbeats every 10 seconds, including while a worker is inside a solve, and writes `status.json` before the first heartbeat interval. The lock is an in-place `flock` on `progress/supervisor.lock`. A second live supervisor is refused. A lock whose process is gone is recovered and logged. `stop` finishes the current batch, writes `STOPPED`, and releases the lock. A hard kill is recovered by the next start: valid items remain, and a batch without a receipt is scheduled again only for the items that were not published.

Workers start in a new session. A timeout kills the process group, keeps published items, and splits the unfinished items. A single item that times out twice after the first attempt is quarantined. Other work continues. Default concurrency is 2 workers. Numeric libraries are pinned to one thread. There is no nested multiprocessing.

The old `rs-lab run` path and `execute_7_shard` refuse this experiment and point at `generation007`.

Commands and the measured batch policy are in `docs/generation-007-execution.md`.

## E. Fault-injection tests

The platform tests in `tests/test_platform.py` ran before the census, in the suite that was green at `32bf3652d78d97ef441dfad1dd264e0d0b5b4867` (109 passed). They cover:

- a partial write is not a completed item
- a completed item is not recomputed
- a receipt verifies
- a timeout kills the worker process tree and splits the batch
- a repeated one-item timeout quarantines that item
- a killed worker is rescheduled, and completed items remain
- `status.json` is visible before the first heartbeat interval
- the heartbeat moves while a worker is busy
- the progress log records the batch lifecycle
- `status --watch` prints
- graceful stop
- a second live supervisor is refused
- a stale lock is recovered
- merge is restartable
- verify detects a missing item and a duplicate id

The census itself injected no fault. Resume events in the census operational block are 0. The injected-failure result from the platform test is that a killed worker lost no completed atomic item.

## F. Batch benchmark

Measured on this machine on 2026-10-12, three repeats, numeric threads pinned to 1. The count is `floor(45 / p90)`, then reduced while `count * p90 > 60` or `count * max > 100`. The watchdog stays 120 seconds. The policy file copied into the census plan is `plan/batch-policy.json`.

| Kind | p50 | p90 | max | items per batch |
| --- | --- | --- | --- | --- |
| multiplier | 0.301s | 0.315s | 0.316s | 142 |
| target singleton | 0.307s | 0.307s | 0.307s | 146 |
| target composition | 0.531s | 0.533s | 0.533s | 84 |
| control composition | 0.532s | 0.545s | 0.545s | 82 |

The smoke root is `generated/generation-007-smoke/`. It is an execution proof. Launcher pid 35071 started at `2026-10-12T08:51:31Z` in its own session. Status moved from the start at `08:51:32Z` to `COMPLETE` at `08:51:48Z`. A stop request at `08:51:55Z` found the process already gone. The plan opened at 72 items and closed at 76. Five receipts. The slowest smoke batch was 68 items in 13.386 seconds. The other four were 2 items and between 1.026 and 1.533 seconds. Timeouts, splits, retries, and quarantines were 0. Cache hits 70, misses 76. Both calibrations are `smoke_capped`. The smoke merge, written at close-out from those completed items, has 2 rows. Every strategy has `used_as_matched` false. The joint text on both controls is `m = 1`, which is the cap marker. It is not a scientific match. Smoke verify `--require-complete`: `ok` true, `complete` true, items 76, receipts 5, problems empty.

The in-process five-cell sample in the scientific Pass 2 remains a preflight note. It is not this generation's result. Its tolerances were kept: the effect floor, the match tolerance, and the joint scale are each `1e-8`. The worst numerical gap in that preflight was `1.52e-14`. The floors were not moved after the census.

## G. Execution-health vector

Scored from the census and the fault tests. Not summed. O, R, and F below 4 would reject the executor.

```text
B batch boundedness        5
O observability            5
R resumability             5
F fault isolation          5
D durability               5
T token efficiency         4
```

B is 5 because the slowest census batch was 27.500 seconds, no batch exceeded 60 seconds, and the 120-second watchdog did not fire. O is 5 because `status.json` was readable from the first seconds of the run, the heartbeat continued, and `progress.log` can be tailed from another terminal. The progress log records the batch lifecycle. Phase changes during the run are on `status.json`. The log writes `phase=` at start (`04_INITIAL_GRID`) and at completion (`COMPLETE`). R is 5 from the restart tests. The census itself has `resume_events` 0, so this score is the tested recovery, not a recovery the census had to use. F is 5 because a timed-out or killed item cannot hold the other work, and the census quarantined nothing. D is 5 because verify accepted 3,880 item hashes and 238 receipts. T stays 4. Status and the log tail are concise. This report still reads the merged summary.

## H. Scientific target cells

Ontology: `N = 4`, `O = 3`, `G = S = H = L = 0`, independent hypergraph. No geometry channel, explicit history, state channel, meta-constraint, simplicial semantics, larger `N`, or cardinality 3.

Twenty-eight cells. Both passage directions. The seven weight pairs, each on `contains_p_companion_edge` and `contains_t_action_edge`, and on polarity present and absent:

```text
prohibit / prohibit
strong_suppress / strong_suppress
weak_suppress / weak_suppress
weak_favour / weak_favour
strong_favour / strong_favour
strong_suppress / strong_favour
strong_favour / strong_suppress
```

Twenty-four cells are finite: neither weight is prohibit. Four cells are the prohibit/prohibit anchors.

Controls:

- Condition-erased: `dissolve(e_B) => m`. Twenty-eight calibrations, relation `unconditional`.
- Pair-face: `dissolve(e_B) | L(face) => m`, polarity and action preserved. Twenty-eight adjacent and fourteen disjoint, forty-two calibrations.

`m = 1` is neutral, `0 < m < 1` suppresses, `m > 1` favours, and `m = 0` is the deletion boundary. The continuous multiplier is analysis semantics. The named weight alphabets are unchanged.

Coverage recorded in the plan: 28 target cells, 20 unique target singletons, 20 unique erased problems, 30 unique face problems, 5 unique control structures, 140 one-direction root solves, 70 joint minimisations, 170 grid kernel evaluations. The census stores 70 primary calibration problems because each target keeps its own calibration, including faces that share a structure. Robustness adds the calibrations that bring the total to 104.

## I. Calibration grid

The positive grid is 33 points, `log10(m) = -4 + i/4` for `i = 0..32`, so the domain is `1e-4 <= m <= 1e4`. Grid sha256 `076d0ad2498359546e350433f089fa37e25f04a1ef1f12266c2bd135d62a04d4`. `m = 0` is stored beside that grid and is outside the positive domain. Five structures times 34 points is the 170 initial grid evaluations.

Initial planned items: 218, which is 170 grid evaluations, 20 target singletons, and 28 target compositions. The progress log records `planned=218` at start. Adaptive refinement, joint requests, control compositions, and robustness added 3,662 items. The closed plan is 3,880.

Search classification uses finite solution, zero-boundary solution, lower-bound optimum, upper-bound optimum, no solution, and unresolved. Every one-direction block in the census is a finite solution. `zero_matches` is false on all 140 one-direction blocks. `only_exact_solution_is_zero` is false on all of them. No selected solution is the deletion boundary.

Monotonicity, over the stored direction curves:

- Erasure: 56 of 56 curves are non-monotone and sign-changing.
- Pair-face: 84 curves, all sign-changing. Forty-two are monotone and forty-two are non-monotone. Each direction contributes 21 of each.

Root counts, retained rather than collapsed:

- Erasure, each direction: 12 curves with one root, 16 with two roots.
- Pair-face, path to matching: 42 curves with one root.
- Pair-face, matching to path: 28 with one root, 14 with two.

## J. One-direction matches

Forward matching solves `Delta_C(m*) = Delta_T` on path to matching. Reverse matching solves it on matching to path. The other direction is stored with the composition and is not a match claim. On pair-face, that unmatched direction has singleton mismatch from `8.75e-5` to `0.00705` (forward strategy, reverse direction) and from `4.78e-5` to `0.00867` (reverse strategy, forward direction). Those gaps sit above the `1e-8` floor.

All 70 forward calibrations and all 70 reverse calibrations are finite solutions and are used as matches: 28 erasure, 28 adjacent, 14 disjoint.

Forward and reverse multipliers:

| Control | n | ratio forward/reverse, min | median | max |
| --- | --- | --- | --- | --- |
| erasure | 28 | 0.999997342 | 1 | 1.000000000000324 |
| pair-face | 42 | 0.11403975 | 0.98480885 | 1.33813975 |

Erasure roots agree across the two directions to a relative gap of about `2.66e-6` at the widest cell (`weak_favour / weak_favour`). Pair-face roots do not. The widest pair-face cell is `strong_favour / strong_favour`, `contains_p_companion_edge`, polarity absent: forward `m = 1.355519025646e+0`, reverse `m = 1.188637321371e+1`.

## K. Joint matches

The joint objective is the predeclared normalised distance between `(Delta_T forward, Delta_T reverse)` and `(Delta_C forward, Delta_C reverse)`.

| Control | class | n | valleys | distance min | median | max |
| --- | --- | --- | --- | --- | --- | --- |
| erasure | finite solution | 28 | 16 with 2, 12 with 1 | 1.593e-10 | 1.949e-8 | 3.771e-7 |
| pair-face | no finite solution | 42 | 42 with 1 | 1.28066 | 1.29415 | 1.34209 |

Erasure joint matches are inside the calibration tolerance. Pair-face joint distances stay near 1.3. Each pair-face joint has one valley, `locally_minimal` true, and `boundary_status` empty. The stored multiplier is a valley of a curve that does not meet the target vector. It is not reported as a match. `used_as_matched` is false on all 42 pair-face joint strategies.

No joint solution is a zero-boundary solution, a lower-bound optimum, or an upper-bound optimum.

## L. Condition-erased controls

Erasure can be effect-matched in each direction and jointly, on all 28 cells, as a positive finite `m`.

On the matched direction, finite erasure margins (`n = 24`):

| Strategy | direction | `M_I` sign | `M_I` min | median | max | `M_G` sign |
| --- | --- | --- | --- | --- | --- | --- |
| forward | path to matching | 24 negative | -0.00936418 | -0.00372898 | -0.000734485 | 24 negative |
| reverse | matching to path | 24 negative | -0.0115125 | -0.00478801 | -0.00105755 | 24 negative |
| joint | path to matching | 16 negative, 8 positive | -0.00402283 | -0.00172526 | 0.0167612 | 16 negative, 8 positive |
| joint | matching to path | 16 negative, 8 positive | -0.00505922 | -0.00268030 | 0.0208289 | 20 negative, 4 positive |

`delta_S` of the erasure control is numerical noise. The largest absolute value on a used erasure composition in these blocks is `3.33e-16`. Singleton mismatch on the claimed direction is at most `3.00e-9` for one-direction erasure and `6.60e-11` for joint erasure.

The eight finite cells where joint `M_I` is positive on both directions share one joint multiplier, `m = 1.102086401766e+0`. Their one-direction roots are about `m = 4.62306941706e-1`. The joint selector has taken a different root. The eight cells are:

- `strong_suppress / strong_suppress` on both geometries and both polarities
- `strong_favour / strong_suppress` on both geometries and both polarities

On those eight, path-to-matching `M_G` is positive as well. On matching to path, `M_G` is positive on the four `strong_suppress / strong_suppress` cells (about `0.0228`) and negative on the four `strong_favour / strong_suppress` cells (`M_I` about `0.010587`, `M_G` about `-0.011285`).

The other 16 finite erasure cells stay negative on `M_I` and `M_G` in both directions under the joint match.

The four prohibit/prohibit anchors, under erasure, agree with each other at the printed precision. Forward, reverse, and joint all select `m = 3.090231902056e-1` up to the last stored digits of the one-direction roots. Path to matching: `M_I = M_G = -0.0277486`, target `delta_S = 0.0214318`. Matching to path: `M_I = M_G = -0.0334299`, target `delta_S = 0.0369089`. Control `delta_S` is at most a few times `1e-16`. The prohibit margin is larger than the finite median, and it is negative at the primary rho. The anchor does not require `m = 0`.

## M. Pair-face controls

Pair-face controls match each direction separately: 42 finite solutions forward and 42 reverse. They do not jointly match: 42 of 42 are `no finite solution`.

Finite pair-face margins on the matched direction only (`n = 36`):

| Strategy | direction | `M_I` | `M_I` min | median | max | `M_G` |
| --- | --- | --- | --- | --- | --- | --- |
| forward | path to matching | 36 positive | 0.00357825 | 0.00986520 | 0.0197188 | 36 positive |
| reverse | matching to path | 32 positive, 4 negative | -0.0105969 | 0.0112649 | 0.0245452 | 26 positive, 10 negative |

Control `delta_S` on those matched directions is at most `4.44e-16`. Matched-direction singleton mismatch is at most `7.72e-9`.

The four finite reverse rows with negative `M_I` are adjacent faces: `strong_favour / strong_favour` and `strong_suppress / strong_favour`, each on `contains_p_companion_edge` absent and `contains_t_action_edge` absent. `M_I` and `M_G` are about `-0.01060` and `-0.00558` respectively. Six further reverse rows, all `strong_favour / strong_suppress`, have positive `M_I` (about `0.0126` to `0.0130`) and negative `M_G` (about `-0.0084` to `-0.0090`).

These one-direction face margins are not a substitute for the joint comparison. The unmatched direction misses the singleton by up to `0.00867`.

## N. Composition margins

`M_I = |I_T| - |I_C|` and `M_G = G_T - G_C`. A negative margin means the lower-order composition has the larger absolute interaction, or the larger super-singleton gap.

On condition-erased controls, after a one-direction match, both margins are negative on every finite cell in the matched direction. After the joint match, both margins stay negative on 16 of 24 finite cells in the forward direction. In the reverse direction the joint match keeps `M_I` negative on 16 and `M_G` negative on 20. The eight sign changes are the root change in section L, from about `0.462` to about `1.102`.

On pair-face controls, the matched direction has positive finite `M_I` and `M_G` throughout the forward match. The reverse match is mostly positive on `M_I` and mixed on `M_G`. There is no pair-face joint composition, because there is no pair-face joint match.

Calibration strategy changes the sign conclusion for erasure. Reporting only the joint match, or only the one-direction match, would hide that split. The eight cells, and the four reverse rows where joint `M_I` and `M_G` disagree, are the split.

Support violations on every used composition are 0.

## O. Higher-order selectivity

Target `delta_S` from the merged question block:

| Direction | above the floor | finite targets | finite and above the floor |
| --- | --- | --- | --- |
| path to matching | 28 | 24 | 24 |
| matching to path | 24 | 24 | 20 |

The four finite cells below the floor on matching to path are negative, not flat. All four are `opposite_suppress_favour`, `strong_suppress / strong_favour`, one on each geometry and each polarity. The stored values are about `-0.004565708`. Path-to-matching `delta_S` on those same cells stays above the floor. The four prohibit anchors are above the floor in both directions (`0.0214318` and `0.0369089`).

Control `delta_S` on every used match is inside the floor. The controls stay triad-flat. The target's selectivity is not reproduced by the matched lower-order rule.

## P. State-shape mismatch

State shape is computed at merge from the stored `q` and `mu`. The predeclared bands are an absolute band of `1e-4` and a relative band of `0.05` of the target scale. A mixed sign pattern whose maximum absolute state error exceeds `1e-4` is classified `poorly state-shape matched`.

For the finite erasure joint matches, both directions, 48 reports:

- classification: 48 poorly state-shape matched
- sign pattern: 48 mixed
- triad-bucket sign pattern: 48 mixed
- `max_abs`: minimum `0.003177`, median `0.011246`, maximum `0.039137`
- the weighted mean of the state error stays near `1e-11`, which is the aggregate match

The largest `max_abs` is `0.03913748503339343`, on `strong_favour / strong_suppress`, `contains_p_companion_edge`, polarity present, matching to path. The aggregate mismatch on that report is about `1.35e-11`.

An aggregate singleton match leaves a statewise residual that changes sign across states and across triad buckets. The classification `aggregate + approximately state-shape matched` does not occur on these 48 reports.

## Q. Robustness

Robustness is six predeclared cells, at `rho3 = 1/2` and `rho3 = 2`, scheduled as ordinary atomic items after the primary calibrations were terminal. The frozen specification lists alphabets `W3` and `W16`. Those alphabets were not scheduled. The divergence is in the plan manifest and in `docs/generation-007-execution.md`.

The six cells are the `ROBUSTNESS_CELLS` tuple: three prohibit/prohibit anchors (`contains_p_companion_edge` absent, `contains_p_companion_edge` present, `contains_t_action_edge` absent), plus `strong_suppress / strong_suppress`, `strong_favour / strong_favour`, and `strong_suppress / strong_favour`, each on `contains_p_companion_edge` absent. `contains_t_action_edge` present at prohibit/prohibit is a primary cell and is not in this robustness set.

Probe inventory: 12 unconditional, 12 adjacent, 10 disjoint. The `contains_t_action_edge` absent prohibit cell has no disjoint face, which accounts for 10 rather than 12. Every adjacent and disjoint probe is `fixed_status = not_matched`, recalibrated class `no finite solution`, `recalibrated_matched` false. Pair-face joint non-representability survives both rhos.

Every unconditional probe is a finite solution and `fixed_status = matched_probe`. The held primary joint `m` is a probe. Its singleton mismatch is about `2e-4` to `5e-5`, above the `1e-8` floor, so the held multiplier is not a new joint match. Recalibration brings the mismatch back to about `1e-10` or smaller.

Signs at the two rhos, unconditional erasure:

- `strong_favour / strong_favour` and `strong_suppress / strong_favour` stay negative on `M_I` and `M_G` in both directions, for the held `m` and for the recalibrated `m`, at both rhos. Primary `m` is `2.539632711361e+0`. Recalibrated `m` is `2.594634533631e+0` at rho `1/2` and `2.483436833001e+0` at rho `2`.
- `strong_suppress / strong_suppress` stays positive on both margins, both directions, both probes, both rhos. Primary `m` is `1.102086401766e+0`. Recalibrated `m` is `1.156422022939e+0` at rho `1/2` and `1.037629546645e+0` at rho `2`.
- The three prohibit anchors agree. The held `m = 3.090231902056e-1` stays negative at both rhos. At rho `1/2` the fixed matching-to-path `M_I` is `-0.0218953`, and the recalibrated `m = 2.580951296213e-1` makes it `-0.0417572`. At rho `2` the held `m` still has matching-to-path `M_I = -0.0413913`. Recalibration moves `m` to `1.229236202726e+0` and the margins flip positive: matching-to-path `M_I = 0.0591645`, `M_G = 0.0646024`; path-to-matching `M_I = 0.0487337`, `M_G = 0.0473742`. Recalibrated mismatch is about `1e-12`.

The primary-rho prohibit margin is negative under the matched multiplier and under the held multiplier at both robustness rhos. It is positive after recalibration at `rho3 = 2`.

## R. Recursive Pass 3

007R Pass 3 is appended in `docs/generation-007-design-passes.md` after this census. The 007R vector does not move: CI 5, CF 4, CB 5, IN 4, IG 5, CR 4, PR 5.

CF stays 4 because the joint erasure match is aggregate. All 48 finite state-shape reports are poorly matched. CR stays 4 because the sign of `M_I` depends on whether the selector takes the one-direction root or the joint root, and because pair-face forward and reverse multipliers differ by up to an order of magnitude. IN stays 4 because a single quoted multiplier is not the result: two roots are retained on 16 erasure curves in each direction, and three strategies are required to see the sign split.

The execution-health vector in section G is the operational score. It is not averaged into this vector.

## S. Optional 007B

Not run. No secondary experiment id was executed.

The scalar pair-face control fails joint representability on 42 of 42 problems. Distances stay between `1.28066` and `1.34209`, each with one valley. That is the representability failure Prompt 007R named as the condition for a later two-parameter control. The scalar erasure control does not fail that test.

007B, a frozen two-parameter lower-order control for the pair-face gap, is the justified next experiment. It has to be specified, scored, and given a work count before any run, and it has to use this supervisor. It is not part of this execution. Graph-class routing among the 3-edge star, the triangle plus an isolated vertex, and the 3-edge path is documented as a later fork and is not run.

## T. Negative findings

- No census solution is `m = 0`. The deletion boundary is not required for the prohibit anchor.
- No pair-face joint calibration is a finite solution, a boundary optimum, or a zero-boundary solution.
- No finite erasure one-direction margin `M_I` or `M_G` is positive.
- The joint erasure match does not keep a single sign. Eight finite cells flip.
- Forward and reverse pair-face multipliers are not the same object. The ratio runs from `0.114` to `1.338`.
- No used control has `delta_S` above `1e-8`. None reproduces target selectivity.
- No finite erasure joint state-shape report is an approximate shape match.
- The smoke `m = 1` texts are cap markers. They are not matches.
- `W3` and `W16` were not run. Robustness is rho only, on six cells.
- The forensic shard was not imported.
- Cardinality 3, simplicial semantics, a larger `N`, graph-class routing, and `G`, `S`, `H`, `L` above 0 were not run.
- 007B was not run.

## U. Inferences

OBSERVED. Condition-erased controls match the higher-order singleton in each direction and jointly, on all 28 cells, at a positive finite multiplier. Joint distances run from `1.593e-10` to `3.771e-7`.

OBSERVED. Pair-face controls match one named direction and miss the two-direction vector. Joint distances run from `1.281` to `1.342`. One scalar face multiplier does not represent the singleton across both passages.

OBSERVED. After one-direction erasure matching, finite `M_I` and `M_G` are negative on all 24 finite cells. The lower-order composition is the larger interaction. The prohibit anchors are more negative (`M_I` about `-0.028` and `-0.033`) and use `m ≈ 0.309`, not `m = 0`.

OBSERVED. After joint erasure matching, 16 of 24 finite cells stay negative. Eight become positive because the joint selector uses `m ≈ 1.102` where the one-direction roots use `m ≈ 0.462`. On four of those eight, matching-to-path `M_G` stays negative while `M_I` is positive. Strategy changes the sign conclusion.

OBSERVED. Target `delta_S` stays above the floor on every path-to-matching cell, and on 20 of 24 finite matching-to-path cells. The four exceptions are `strong_suppress / strong_favour`, about `-0.004566`. Matched controls stay triad-flat.

OBSERVED. Aggregate agreement leaves a mixed statewise residual. Median `max_abs` on the finite erasure joint reports is `0.01125`. The largest is `0.03914`.

OBSERVED. At `rho3 = 1/2` and `rho3 = 2`, unconditional erasure remains jointly representable and pair-face remains jointly non-representable. The strong_suppress positive joint sign and the strong_favour negative sign survive fixed and recalibrated probes. The prohibit sign survives the held primary multiplier and survives recalibration at rho `1/2`. Recalibration at rho `2` flips it positive.

INFERRED. For a condition-erased control matched in one direction, and for the joint match on 16 of 24 finite cells, the higher-order gate does not add composition magnitude. The larger `|I|` and `G` belong to the lower-order composition. The gate's remaining contribution on those cells is selectivity, and a statewise pattern that the aggregate match does not flatten.

INFERRED. That magnitude claim is strategy-dependent on eight finite cells. A report that quoted only the joint root would say the higher-order target is larger there. A report that quoted only the one-direction root would say the opposite. Both roots are retained. The sign is a property of the selector.

INFERRED. A pair-face scalar is the wrong instrument for the two-direction question. Its positive one-direction margins answer a single passage. They do not show that a face-gated lower-order rule, once matched in both directions, overtakes or falls behind the target. The two-direction face comparison is blocked by representability.

INFERRED. Prohibit remains the large primary-rho case, and it remains a finite multiplier. The rho-2 recalibration shows that the prohibit sign is not invariant once the multiplier is refit. The held primary multiplier does not flip.

## V. RS / global-coherence interpretation

This census does not establish a globally coherent architecture, and it does not assign a meaning to a triad.

What it supports is a split that survived a fairer strength match on the erasure control. Composing two dissolution weights is non-additive with the gate removed. Matching the erased rule to the gated rule's singleton effect, one direction at a time, leaves the erased composition with the larger absolute interaction and leaves `delta_S` on the gated target. The same aggregate match does not make the statewise effect the same: the residual changes sign across states. So the higher-order relation, on this passage and this control, is doing selectivity and shape work more steadily than it is doing extra magnitude work.

The joint selector qualifies the magnitude half of that sentence. On eight finite cells a second root reverses `M_I`. The laboratory can say that lower-order dominance survives one-direction matching. It cannot say that every admissible scalar match preserves the sign.

The pair-face result qualifies the control. A face is a lower-order predicate with its own duty cycle. One multiplier cannot put that predicate on top of both passage effects at once. Until a second parameter is frozen and run, a face-gated control is evidence about one direction, not evidence about the two-direction singleton.

A calculated split of this kind is not a design conclusion. It is the reason the next experiment, if it is run, is a two-parameter face control rather than a new graph class.

## W. Recursive Pass 4

Pass 4 is in the design-pass note. The chosen next step is to specify 007B and not to run it in this branch. The pair-face joint failure is identified. The erasure scalar is representable and stays the comparison. Graph-class routing stays deferred, because the magnitude-versus-selectivity split is stable for one-direction erasure and not stable for the joint selector, and because the face control is not yet a two-direction object.

Stopping without 007B would leave the face question unanswered. Running graph classes now would change the graph before that control question is closed. Neither is the smallest next step.

## X. Operational commands

From `constraint-lab/`:

```bash
python -m rs_constraint_lab generation007 plan
scripts/start-generation-007.sh
python -m rs_constraint_lab generation007 status --watch 5
python -m rs_constraint_lab generation007 stop
python -m rs_constraint_lab generation007 verify --require-complete
python -m rs_constraint_lab generation007 merge
```

Linux / WSL:

```bash
tail -n 30 -f constraint-lab/generated/generation-007/progress/progress.log
```

PowerShell:

```powershell
Get-Content .\constraint-lab\generated\generation-007\progress\progress.log -Tail 30 -Wait
```

`scripts/stop-generation-007.sh` and `scripts/watch-generation-007.sh` are the other two shell entry points. The PowerShell twins were written and were not executed on this Linux host.

`run-next` and `run-batches --count 5` are the bounded foreground commands. The census was not run that way. It was started with `scripts/start-generation-007.sh`, which returns after the supervisor has its own session. Pid 45223, session leader, started `2026-10-12T09:08:33Z`, exited after `COMPLETE` at `2026-10-12T09:34:28Z`. Wall clock is about 26 minutes. No foreground scientific command ran for hours.

## Operational record

| Field | Value |
| --- | --- |
| atomic item | one structure, one `m`, one rho/alphabet, both passage directions |
| initial planned items | 218 |
| adaptive added items | 3,662 |
| closed plan | 3,880 |
| batch target | 45 seconds, from the measured p90 |
| hard timeout | 120 seconds |
| workers | 2 |
| heartbeat | 10 seconds |
| background mode | `scripts/start-generation-007.sh`, new session, pid 45223 |
| completed batches | 238 |
| timeouts | 0 |
| splits | 0 |
| retries | 0 |
| quarantines | 0 |
| resume events | 0 |
| median batch wall | 4.303464 seconds |
| p90 batch wall | 5.600972 seconds |
| maximum batch wall | 27.500368 seconds |
| batches over 60 seconds | 0 |
| batches over 120 seconds | 0 |
| largest batches | three multiplier batches of 142 items, at 27.500, 27.427, and 27.417 seconds |
| cache hits / misses | 3,346 / 3,936 |
| events | start 1, batch_start 238, batch_complete 238, advance 203, robustness_scheduled 1, supervisor_exit 1 |
| maximum lost completed work after an injected worker kill | 0, from the platform test |
| calibrations | 104 / 104 converged |
| merge | 28 rows from the durable item files |

The median, p90, and maximum are the values stored in the summary operational block. The median there is the upper of the two central receipt walls.

## Questions this generation was asked

1. Condition-erased controls can be effect-matched. All 28 are finite solutions in each direction and jointly.
2. Pair-face controls can be effect-matched in one named direction. All 42 forward and all 42 reverse are finite solutions. None of the 42 is a joint finite solution.
3. None require `m = 0`. Prohibit uses `m ≈ 0.309`.
4. Effect curves are sign-changing on every stored direction. Erasure curves are non-monotone on all 56. Pair-face curves are monotone on 42 and non-monotone on 42.
5. Multiple roots are present. Sixteen erasure curves in each direction have two roots. Sixteen erasure joints have two valleys. Fourteen pair-face matching-to-path curves have two roots. Pair-face joints have one valley each.
6. Erasure forward and reverse multipliers agree to a relative gap of at most about `2.66e-6`. Pair-face ratios run from `0.114` to `1.338`, median `0.985`.
7. The joint scalar match is good for erasure (median distance `1.95e-8`, maximum `3.77e-7`) and unavailable for pair-face (minimum distance `1.281`).
8. After one-direction erasure matching, finite `M_I` is negative. After joint erasure matching, finite `M_I` is negative on 16 cells and positive on 8, in each direction. After pair-face forward matching, finite `M_I` is positive on all 36. After pair-face reverse matching, it is positive on 32 and negative on 4.
9. `M_G` follows `M_I` on the one-direction erasure matches and on the joint forward direction. On joint matching to path, `M_G` is negative on 20 finite cells and positive on 4. Pair-face forward `M_G` is positive on all 36 finite matched directions. Pair-face reverse `M_G` is positive on 26 and negative on 10.
10. Yes. The erasure sign depends on the strategy for those eight cells. Pair-face has no joint composition to compare.
11. Yes. Control `delta_S` stays at numerical noise on every used match. Support violations are 0.
12. Target `delta_S` stays above the floor on all 28 path-to-matching cells and on 24 of 28 matching-to-path cells. Twenty of 24 finite matching-to-path cells are above the floor. Four finite `strong_suppress / strong_favour` cells are negative, about `-0.004566`.
13. The state-shape mismatch is large relative to the aggregate. All 48 finite erasure joint reports are poorly state-shape matched, mixed sign, mixed triad. Median `max_abs` is `0.01125`. The maximum is `0.03914`.
14. Prohibit stays exceptional in magnitude at the primary rho, and it stays a finite match. It is not an `m = 0` case. Recalibration at `rho3 = 2` can flip its sign.
15. v0.6 lower-order dominance of `|I|` survives one-direction erasure matching on every finite cell, and it survives the joint match on 16 of 24. It does not survive the joint match on the other eight. Pair-face one-direction margins mostly go the other way, and they are not a joint comparison.
16. One-parameter representation fails for the pair-face control across both directions. It does not fail for the erasure control. The failure mode is a single valley whose distance stays near 1.3, not a boundary pile-up.
17. A richer lower-order control is justified for that pair-face gap. It is not justified as a replacement for the erasure result.
18. The smallest justified next experiment is 007B: freeze a two-parameter pair-face control, score it, count the work, and run it through this supervisor. Graph-class routing waits.

## Execution success criteria

The census meets the v0.7R operational criteria. No unbounded foreground scientific command was used. Normal batches finished in at most 27.5 seconds, under the 60-second target. The hard timeout stayed 120 seconds and did not fire. Progress was visible from status and from the progress log. The platform kill test lost no completed item. Restart reuses completed receipts; the census did not have to resume. Quarantine exists so one stuck item cannot hold the rest; the census did not need it. Merge read the durable item files and wrote 28 rows. Verify accepted that merge.
