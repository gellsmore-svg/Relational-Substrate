# External review 007 — ChatGPT review of v0.7R

This file records the scope and conclusions of an external ChatGPT review of `research/constraint-lab-v0.7-resumable` at `91079cbd5a545702887d48bdd67ad16273de9a55`.

The review is external to the v0.7R implementation. It is not a line-by-line audit of every durable item. Generation 7 files are historical evidence and are not rewritten by this review.

## What was inspected

- Branch history.
- The Generation 7 report.
- The Generation 7 specification.
- The recursive design passes.
- Execution 007R.
- The aborted Execution 007 attempt.
- The supervisor implementation.
- The work store.
- The batch CLI.
- The Generation 7 execution adapter.
- The fault-injection tests.
- The calibration logic.
- Final-head CI.

## Operational conclusions

Generation 7R completed on the micro-batch platform:

```text
3,880 durable atomic items
238 batches
2 workers
~26 minutes total wall clock
median batch wall ~4.303 s
p90 batch wall ~5.601 s
maximum batch wall ~27.500 s
0 timeouts
0 retries
0 quarantines
104 / 104 calibrations converged
28 merged scientific rows
```

The local census status at `constraint-lab/generated/generation-007/progress/status.json` agrees with that record: phase `COMPLETE`, 3,880 completed items, 238 completed batches, 104 / 104 calibrations, 0 failed items, 0 retried batches, 0 timed-out batches, 0 quarantined items. The run started at `2026-10-12T09:08:33Z` and the last activity is `2026-10-12T09:34:28Z`.

Local batch receipts, 238 files, agree with the wall-clock summary under the same definitions used for Generation 7. The operational median is the upper of the two central receipt walls, index `len//2`: `4.303464` seconds. The p90 is the nearest-rank ceiling index: `5.600972` seconds. The maximum is `27.500368` seconds. Receipt timeouts are 0.

The final branch head has successful GitHub Actions run `38233719248` on `91079cbd5a545702887d48bdd67ad16273de9a55`. The run completed with conclusion `success`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38233719248`.

That run was viewed from this checkout. It is a run of the reviewed head. It is not a run id for a later commit that merely cites it.

The preceding report commit `107c7ab30fb0a36ed992e78b637ba3fda7ec5d16` has Actions run `38233390592`, recorded in Execution 007R. Execution 007R says that line is not a run id for the close-out commit. This review is the record of the final-head run. Do not create an infinite provenance chain of commits whose only purpose is recording the CI run of the previous commit.

The micro-batch execution architecture is accepted as permanent Constraint Laboratory infrastructure. Do not return to opaque shard-scale execution.

## Aborted-attempt lesson

The earlier Prompt 007 attempt had one 14-cell shard finish in about five minutes while another remained marked running for many hours without item-level durable outputs.

The root cause inside that process was not established.

The established engineering failure was:

```text
insufficient work granularity
insufficient visibility
insufficient fault isolation
```

Generation 7R fixed that. Do not reopen that architecture. The attempt remains `research/constraint-lab-v0.7` at `5787f2c0f2664d2daa3125997aaa5267a3059ac0`. It is not a Generation 7 result.

## Scientific conclusions

### Condition-erased scalar control

For all 28 target cells:

```text
forward match: 28 / 28
reverse match: 28 / 28
joint match:   28 / 28
```

All are finite positive multipliers.

Even the prohibit anchor is matched at approximately:

```text
m ≈ 0.309
```

rather than requiring:

```text
m = 0.
```

The higher-order singleton's aggregate two-direction passage vector is representable by an unconditional lower-order scalar rule.

The statewise effect is not reproduced.

For the 48 finite joint state-shape reports:

```text
48 / 48 poorly state-shape matched
median max_abs ≈ 0.01125
maximum max_abs ≈ 0.03914
```

with mixed signs across source states and triadic buckets.

Thus:

```text
aggregate representability
!=
state-resolved representability.
```

### Pair-face scalar control

The pair-face scalar control can match either direction separately:

```text
42 / 42 forward
42 / 42 reverse
```

and:

```text
0 / 42 joint
```

The best joint normalised distance lies approximately in:

```text
1.28066 to 1.34209.
```

Forward/reverse required multiplier ratios range approximately:

```text
0.114 to 1.338.
```

One pair-conditioned scalar multiplier is not a two-direction representation of the higher-order singleton on this control family.

That representability gap is what Generation 7B addresses. This review does not start Generation 7B.

### Composition magnitude

For one-direction effect-matched condition erasure:

```text
M_I < 0
M_G < 0
```

on all finite cells in the direction being matched.

Under the joint erasure selector:

```text
16 / 24 finite cells retain negative M_I
8 / 24 become positive M_I
```

because a different valid root is selected on those eight cells.

Composition magnitude is not a stable discriminator of relational order under the current scalar matching.

Do not summarise Generation 7 as:

```text
lower-order is always stronger
```

or:

```text
higher-order is stronger.
```

The sign is selector-dependent on part of the finite set.

### Higher-order selectivity

Matched lower-order controls remain triad-flat to numerical noise.

The target retains hidden-triad-conditioned selectivity across almost all cells.

This remains the more robust higher-order signature.

## Prompt 007R authored provenance

The externally verified authored Prompt 007R metadata is:

```text
bytes:
33,005

sha256:
c0413890748a7e0956f570dbba469d225ef6e228ef23fb980abf371cbea14e38
```

The stored Grok agent-input representation is:

```text
bytes:
33,191

sha256:
10e893b0734f74b55adf94e070aa713329d79c1cc4f3ae01d7e61c5e72f34c61
```

The local file `constraint-lab/provenance/prompts/007R-v0.7-resumable-agent-input.md` was measured again for this review: 33,191 bytes, sha256 `10e893b0734f74b55adf94e070aa713329d79c1cc4f3ae01d7e61c5e72f34c61`.

The authored artifact is not present locally. `authored_prompt_status` is `externally_verified_pending_import`. The relationship is `unknown`. The two byte strings differ. This review does not claim equality and does not assign the authored hash to the agent-input file. The agent-input file is not rewritten. The Prompt 007R ledger line is left unchanged. A later ledger line records this metadata.
