# Execution 007B — two-level pair-face control

This is the execution record for prompt 007B. It closes that prompt. It does not close prompt 007 or prompt 007R.

## Prompt

| Field | Value |
| --- | --- |
| prompt_id | 007B |
| agent_input_path | `constraint-lab/provenance/prompts/007B-v0.7b-agent-input.md` |
| agent_input_sha256 | `4bd7fc8a6463d948dde493ae91054738a66a30460f83edb8de25295238f16075` |
| agent_input_bytes | 43718 |
| authored_prompt_path | null |
| authored_prompt_sha256 | null |
| authored_prompt_bytes | null |
| authored_prompt_status | `pending_verbatim_import` |
| relationship of authored to agent input | `unknown` |
| date | 2026-10-12 |
| authoring source | user instruction to the implementing agent |
| target | Grok 4.7 |
| repository | gellsmore-svg/Relational-Substrate |
| starting_branch | `research/constraint-lab-v0.7-resumable` |
| starting_commit | `91079cbd5a545702887d48bdd67ad16273de9a55` |

The stored file is the agent input. It includes one leading newline and one trailing newline. It does not contain its own sha256. No separate authored Markdown was byte-compared. Prompt 007 and Prompt 007R are not overwritten.

Prompt 007R authored metadata stays externally verified and pending import: 33,005 bytes, sha256 `c0413890748a7e0956f570dbba469d225ef6e228ef23fb980abf371cbea14e38`. That hash is not assigned to the stored 007R agent-input file. The two byte strings differ.

## Result

Branch `research/constraint-lab-v0.7b`.

The inclusive commit range produced by prompt 007B, through the analysis report, is:

```text
6aa898aafbdd6bdd1cde715cc36022a16a5acaf1
```

The parent of that commit is `91079cbd5a545702887d48bdd67ad16273de9a55`. The commit that adds this execution file is outside that range. The ledger line that points at this record is that same close-out commit. It is not inside the analysis range above.

Experiment id:

- `generation-007b-two-level-pair-face`

There is no secondary experiment id. Mode B was not executed. Graph-class routing was not executed.

Report:

- `constraint-lab/reports/generation-007b-two-level-pair-face-control.md`

Tables:

- `constraint-lab/reports/generation-007b-tables.json`

Design passes:

- `constraint-lab/docs/generation-007b-design-passes.md`

## What ran

The census root is `constraint-lab/generated/generation-007b/`. The supervisor started at `2026-10-12T12:45:38Z`. Last activity is `2026-10-12T14:19:04Z`. Status `COMPLETE`. Workers 2. Heartbeat 10 seconds. Watchdog 120 seconds. Items 4,539 / 4,539. Batches 196. Timeouts 0. Retries 0. Quarantines 0. Resume events 0. Stale-lock events 0. Median batch wall, index `n // 2`, is 24.346407 seconds. Nearest-rank p90 is 44.279666 seconds. Maximum is 53.949035 seconds. Calibrations 42 / 42 represented. Unresolved 0.

`cache_hits` and `cache_misses` in the status file are 0 because the 007B counter returns those fields as zero. They are not a kernel-cache measurement.

Local verify `--require-complete` on the census root: `ok` true, `complete` true, items 4,539, receipts 196, problems empty, spec hash `7ea4ff15146e50f18f2683a5567d1a7d2644735d13d625c812464f22de6370f0`.

`constraint-lab/generated/` is gitignored. CI does not re-run the census. The published numerical record is the report and the tables file.

The corrected preflight root and the smoke root remain local. They are not the census.

## Divergences from the prompt

- Four adjacent `weak_favour` / `weak_favour` calibrations are labeled R2. A second diagonal root is stored on the disjoint twin of the same target and was absorbed into the nearer coarse component on the adjacent structures. The census was not rerun. The report states the search limit.
- Alphabet sensitivity was not scheduled. `sensitivity_alphabets` is empty. W3 and W16 were not run.
- Pair-source-orbit pattern is not a field of the stored state-shape report and was not recomputed.
- PowerShell start, stop, and watch scripts were written and were not executed on this Linux host.
- The 007B status counter does not report kernel cache hits.
- Review of Generation 007B is not written here. Review 007 is the external reading of v0.7R.

## Local checks

Before the report commit, `python -m pytest -q` in `constraint-lab` reported 129 passed in 190.72 seconds. That suite includes the 007B planner tests, the 007B verify-row test, and the platform fault tests. It does not include the Generation 007B census.

## CI

Actions run `38265662798` is the push of `6aa898aafbdd6bdd1cde715cc36022a16a5acaf1`. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38265662798`.

`gh run view 38265662798` reported conclusion success on `6aa898aafbdd6bdd1cde715cc36022a16a5acaf1`. Jobs `constraint-lab` and `books` both completed. The URL is `https://github.com/gellsmore-svg/Relational-Substrate/actions/runs/38265662798`.

This execution file is a later commit. The run id is not a run id for the commit that adds this file.
