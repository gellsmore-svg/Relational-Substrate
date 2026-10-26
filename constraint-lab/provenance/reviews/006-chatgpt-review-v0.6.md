# External review 006 — ChatGPT review of v0.6

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.6` at `4deef3aa272a3ceadb5c610fcc95eaa24fde3901`.

The review is external to the v0.6 implementation. It is not a line-by-line audit of every shard or numerical matrix. Shard directories and individual numerical matrices under `generated/` were not re-derived one by one in that review.

## What was inspected

- The v0.6 commit history.
- The Generation 6 report.
- The Generation 6 specification.
- The recursive design passes.
- The Generation 6 row table and graded surface.
- Provenance Review 005 and Execution 006.
- `v06.py`.
- The v0.6 tests.
- Target and control canonicalisation.
- The final CI state.

## Conclusions recorded from that review

### Execution state

Generation 6 completed:

```text
100 canonical target systems
1,200 labelled target systems
15 canonical condition-erased controls
100 canonical pair-face controls
10 shards
2 workers
0 failed
0 quarantined
```

The run took approximately 96.0 seconds of wall clock. Execution 006 records the summary field `runtime_seconds` as 96.00385372998426.

The final v0.6 head itself has successful GitHub Actions run `37193089700` on `4deef3aa272a3ceadb5c610fcc95eaa24fde3901`. Jobs `constraint-lab` and `books` both completed. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/37193089700`.

The preceding run `37192986304` belongs to the earlier report commit `a359af33e396d7f5325145f2b51ee3262dca7fe6`. Jobs on that run also completed. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/37192986304`. Execution 006 records `37192986304` and says that line is not a run id for the commit that adds it.

This review is the record of the final-head run. Final-head CI is recorded by the later external review. Do not create an infinite provenance chain of commits whose only purpose is recording the CI run of the previous commit.

### Three effects, kept separate

v0.6 cleanly separated three effects. They are not one claim.

#### A. Hard deletion

The prohibit/prohibit cell is the magnitude peak. Finite grades retain interaction, but typically only a fraction of the prohibit anchor.

For the 64 finite/finite target systems, median continuity ratios relative to the prohibit/prohibit anchor are approximately:

```text
R_I:
0.121 path -> matching
0.135 matching -> path

R_G:
0.097
0.100

R_S:
0.144
0.134
```

No finite row retains at least half of the prohibit-anchor `|I|`.

Hard prohibition strongly amplifies the interaction magnitude. Finite interaction does not collapse to zero.

#### B. Generic nonlinear composition

For every one of the 100 target rows in both directions:

```text
I_abs_margin < 0
```

relative to the strongest matched lower-order control.

Thus the target exceeds every matched lower-order control in `|I|` on 0 / 100 rows in each direction.

The condition-erased prohibit/prohibit control produces larger absolute interaction and larger `G` than the higher-order prohibit anchor.

Non-additive committor interaction and large super-singleton effects are not specifically higher-order phenomena in this experiment.

#### C. Higher-order selectivity

The matched lower-order controls are triad-flat to numerical tolerance. The maximum measured lower-order triadic spread is approximately `1.39e-15`, with 0 controls above the `1e-8` floor.

The genuine higher-order target retains positive `Delta_S` on 64 / 64 finite path-to-matching rows and 56 / 64 finite matching-to-path rows.

The distinctive role of the higher-order gate in this experiment is that the lower-order passage becomes conditional on hidden higher-order relational configuration.

The decomposition to keep is:

```text
constraint composition -> non-additivity
hard deletion -> magnitude peak
higher-order gating -> hidden-state selectivity
```

Do not collapse those back into one claim.

### Unresolved confound

v0.6 preserved nominal weights. It did not necessarily preserve effective singleton strength.

A condition-erased rule is active in more states than a gated rule. The same nominal weight is therefore not the same effective dynamical strength.

Example:

```text
dissolve(e_B) | present(tau) => strong_suppress
```

is active only when the triadic predicate holds. The condition-erased control:

```text
dissolve(e_B) => strong_suppress
```

is active everywhere the event itself is admissible. The erased control can be dynamically stronger even with the same nominal grade.

v0.6 therefore does not answer whether a lower-order control, calibrated so that its singleton-level effect equals the higher-order singleton effect, still produces as large a composed interaction. That question is not answered by this review.
