# Validation record

## Calculator

Python 3.12.3, Linux/WSL, 2026-09-10. The engine requires only Python's standard
library; plotting dependencies are recorded in `requirements-research.txt`.

`python3 -m unittest discover -s tests -v`: **15 tests passed**. This includes:

- 2,850 signed arithmetic grid cases across two seeds, checked independently.
- 242 decimal carry/borrow/sign combinations, plus forced-replay gate ablation.
- Conservation, state validity, zero, erasure failure, local collision dynamics.
- Identical-seed trajectory reproduction and distinct-seed structural diversity.
- Operator precedence, relational chaining, `ans`, and explicit remainder selection.
- Invalid syntax, division by zero, resource limits, and negative CLI expressions.
- JSONL logging, source archives, no-overwrite behavior, and one/two-worker parity.
- Source audit and observer-blocked relational addition.
- Noisy divisor destruction recorded as a failure instead of crashing a batch.
- Censored trials retained with an incomplete-state snapshot in the final harness.

Direct installed CLI check: `rs-calc '17 + 28' --seed 48271 --verbose` returned 45,
204 counted events and trajectory
`73a513ba6125acb5e995cbbcddfe7500de319c3c577050ff6a223964e0347791`.
This includes independent literal normalization by the expression interpreter;
direct-operation experiment event counts exclude that extra orchestration.

A supplemental 1,000-case signed radix stress check also passed: operands sampled
uniformly from [-1000000, 1000000] with operand seed 9182, transition seeds 0-999.
This is software verification, not a new logged research experiment. A scripted
REPL session returned 45, 90, `4 remainder 1`, and 5 for the documented chaining
workflow. All 93,800 retained JSONL rows parsed and had internally consistent
correctness/convergence flags.

## Experimental reproduction

- SC-001 rerun: all 30 summary cells exactly matched the initial experiment,
  including event statistics, structural diversity and outcomes. Same seeds were
  reused; the extra 6,000 trials are not independent evidence.
- Restored `reliability-holdout-v1/source.tar.gz` in an isolated directory; seed
  1200000 reproduced initial/final states, result, counts and trajectory with **no
  source changes**. Trajectory:
  `63eb317fe46d0ed50388e5fcfb89f4dc2ee8f82ee28d63b2d35ac0afb9ae988b`.
- The current implementation also reproduced that historical trial, explicitly
  reporting evolved source files rather than hiding the version difference.
- Censored seed 170000 in `censoring-v2` replayed exactly, including its incomplete
  population; only a later CLI-only source change was reported.
- 87,800 primary/supplemental trial records plus the 6,000 same-seed foundational
  rerun are retained. The original programme and follow-up definitions are archived.
- Analysis reads raw compressed logs. Eight PNG/PDF figure pairs were generated;
  constraint, survival-comparator, covariance and trajectory figures were visually
  inspected for labels, data and framing.

The early SC-001 run predates automatic code archiving. Its manifest preserves
source hashes and its final-code rerun provides an archived reconstruction. The
SC-018 v1 timeout rows do not contain a partial population; this historical gap is
explicitly preserved, and `censoring-v2` demonstrates the corrected logging path.

## Profile

`python3 -m cProfile -s cumulative -m rs_calc '500+500' --seed 1` returned 1000.
On this run, total profiled time was about 0.989 seconds, normalization 0.808 seconds
cumulative, list removal 0.383 seconds cumulative, and 1,272,590 relation equality
comparisons consumed 0.256 seconds. Trace event serialization was about 0.044 seconds
cumulative. These nested times must not be summed. List scans/removals dominate,
supporting an indexed-population optimization as future engineering work. No
performance claim is generalized from this machine-specific profile.

## Existing repository checks

`npm run guardrails`: **passed** in the working repository, including the existing
predeclaration gate self-test. The standalone calculator has its own manifest and
oracle separation rather than using a physical-property descriptor registry.

`npm ci` and `npm run build`: **passed** in an isolated native-Linux worktree of
the unchanged repository baseline `06cb0dc`. The Windows-mounted checkout initially
produced truncated JavaScript/generated JSON during npm operations, including with
a fresh npm cache; the native worktree avoided that failure. No application source
or dependency versions were changed as part of the calculator work.

`npm run reports` on the clean baseline reaches an existing ordering problem:
`model:external-roadmap` requests `analysis/out/model-frontier-report.json` before
the runner reaches `model:frontier` (runner entries 33 and 66). The prerequisite can
be generated with `npm run model:frontier`; a follow-up run is recorded separately
below. This is outside the new calculator modules.

After generating that missing prerequisite, **the full `npm run reports` completed
successfully** in the native worktree. The clean-checkout ordering defect remains
documented; no unrelated report-runner source change was included in this project.
