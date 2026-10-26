# External review 007B — ChatGPT review of v0.7b

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.7b` at `8f47bae7f773ec3b706b2c603667a31b9c69285b`.

The review is external to the v0.7b implementation. It is not a line-by-line audit of every durable item. Generations 1 through 7B remain historical evidence. This review does not rewrite their reports, design passes, execution records, or prompts.

## What was inspected

The external review inspected:

- branch history;
- the Generation 007B report;
- the Generation 007B machine-readable tables;
- the experiment specification;
- the design passes;
- the execution record;
- `v07b.py`;
- the Generation 007B execution adapter;
- the relevant tests;
- the supervisor multi-worker status changes, including `running_batches[]`;
- final-head CI.

## Operational conclusions

Generation 007B completed on the resumable micro-batch platform:

```text
4,539 durable items
196 batches
2 workers
~93 minutes elapsed
median batch wall ~24.346 s
p90 batch wall ~44.280 s
maximum batch wall ~53.949 s
0 timeouts
0 retries
0 quarantines
42 / 42 primary calibrations terminal
0 unresolved
verify --require-complete succeeds
```

The local census status at `constraint-lab/generated/generation-007b/progress/status.json` agrees: phase `COMPLETE`, 4,539 completed items, 196 completed batches, 42 / 42 calibrations, 0 unresolved, 0 timed-out batches, 0 retried batches, 0 quarantined items. The run started at `2026-10-12T12:45:38Z` and the last activity is `2026-10-12T14:19:04Z`, which is 93.4 minutes.

Local batch receipts, 196 files, agree under the same definitions used for Generation 7. The operational median is index `n//2`: `24.346407` seconds. The p90 is the nearest-rank ceiling index `min(n-1, ceil(0.9*n)-1)`: `44.279666` seconds. The maximum is `53.949035` seconds. Receipt timeouts are 0. Receipts with failed items are 0. 82 batches exceeded 30 seconds. None exceeded 60 seconds. None exceeded 120 seconds.

`running_batches[]` lists every live worker. A second terminal can see each worker independently. That status change is part of what this review inspected. The resumable micro-batch platform remains mandatory. Generation 8 does not bypass it.

Final-head GitHub Actions run:

```text
38266091871
```

on:

```text
8f47bae7f773ec3b706b2c603667a31b9c69285b
```

The run completed with conclusion `success`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38266091871`. Jobs `constraint-lab` and `books` both completed. This review is the record of that final-head run. The preceding analysis commit `6aa898aafbdd6bdd1cde715cc36022a16a5acaf1` has Actions run `38265662798`, recorded in Execution 007B. That line is not a run id for the close-out commit. Do not add a further commit whose only purpose is to restate `38266091871`.

## Central scientific observations

Generation 007B asked whether a two-level pair-conditioned lower-order control

```text
pair condition true  -> m_on
pair condition false -> m_off
```

could reproduce the higher-order singleton's two-direction aggregate passage vector.

Observed:

```text
42 / 42 logical controls have at least one finite representation
0 boundary-only
0 zero-boundary
0 unrepresented
0 unresolved
```

The search stored:

```text
52 in-tolerance solutions
```

and every stored solution satisfies:

```text
m_off = m_on
```

Every found representation therefore collapses dynamically to an unconditional scalar weight. The extra pairwise contextual degree of freedom was not used by the fitted representation.

## Aggregate passage versus internal structure

For the two aggregate passage observables alone, a one-rule one-scalar lower-order representation already exists. That is the Generation 7 result. The minimal lower-order representation of those two numbers is that unconditional rule and its fitted scalar.

This review does not say that the lower-order aggregate representation intrinsically requires two rules and two parameters. The two-level search had room for that representation. The solutions it stored did not use the extra degree of freedom.

Separately, the state-resolved reports stay poorly matched:

```text
84 / 84 two-level state-shape reports
```

The controls remain triad-flat to numerical noise:

```text
max |Delta_S_C2| ≈ 3.33e-16
```

The target retains non-zero triad-conditioned selectivity.

So an aggregate projection can be emulated while the state-resolved transition structure is not reproduced, and while the higher-order contextual selectivity is not reproduced. Those are different observations.

## Composition remains representation-dependent

Ten calibrations have two stored aggregate representations. Across their 20 passage-direction cases:

```text
I_C2 changes sign in 8
G_C2 changes sign in 2
```

Composition magnitude is not uniquely determined by aggregate singleton matching. A larger interaction magnitude is not a privileged higher-order signature. The more stable structural observation remains contextual selectivity.

## Search-completeness qualification

The declared basin search behaved according to its frozen rules.

Four adjacent `weak_favour / weak_favour` cases are labelled R2 only relative to the basins opened by that search. A disjoint structurally related case demonstrates a second diagonal root near:

```text
m ≈ 1.544
```

that the adjacent search did not directly evaluate.

Future language should say:

> solution multiplicity discovered by the declared search

rather than:

> mathematically exhaustive global uniqueness

unless a proof or an exhaustive root search exists.

This qualification does not undermine the diagonal-collapse observation. The additional known root is also diagonal.

## Complexity stopping rule

The lower-order coefficient-fitting sequence stops here.

A third fitted lower-order parameter is not added merely to chase the remaining statewise residuals. The two aggregate observables are already represented. Further free coefficients, without new independent structural predictions, would move the exercise toward interpolation.

Generation 8 changes the question. It does not extend the coefficient sequence.

## Prompt 007B authored metadata

The following metadata is externally verified and is not assigned to the stored agent input. The two byte strings are distinct. The authored file is not in this working environment, so no byte comparison was performed.

```text
authored bytes: 43,719
authored sha256: e343cdbd693edf5302d1518095ba2912e2254d801e068ccbdd87280f9b8defef
authored_prompt_status: externally_verified_pending_import
relationship: unknown

stored Grok agent input:
  path: constraint-lab/provenance/prompts/007B-v0.7b-agent-input.md
  bytes: 43,718
  sha256: 4bd7fc8a6463d948dde493ae91054738a66a30460f83edb8de25295238f16075
```

The original Prompt 007B ledger line is left unchanged, including its null authored hash. A later ledger line records this external verification. Prompt 007 and Prompt 007R are not overwritten.

## Provenance limitation carried forward

Generation 007B was committed in two commits. Its report says the specification and the work count were frozen before execution, and the execution hashes are internally consistent. Git history itself does not independently demonstrate that chronology.

Generation 8 is required to improve this. A round plan is committed and pushed before any scientific trajectory of that round. The plan commit is recorded as `frozen_exploration_plan_commit`. Scientific results are a later commit.
