# GT-P012 starting audit

*15 October 2026. Written before any E5D computation. No NL comparator or E5D value of any N=5 or N=6 cell has been computed.*

## 1. Live state (verified by `git fetch`)

| Resource | Checkpoint | Observed |
| --- | --- | --- |
| GT branch / PR #6 | `a81c505` (GT-P011 close) | same; clean; draft; CI green (run 38802920114) |
| GT-P010 close | `4aaf04c` | ancestor of the GT head |
| GT-P011 freeze / results | `469ee28` / `5080199` | present |
| Hub `main` | `38c2501` | same (no commits since) |
| Canonical hub GT pin | `79fa6b0` (GT-P009) | same: the hub is **not** updated through GT-P010/P011 |
| Hub PR #9 | `hub/gt-p010-p011-milestone` at `42a474a`, draft, staged | same; CI green; no human review recorded; pin not adopted |

**Other activity.**
- A CL branch `research/constraint-lab-v0.8p-stopping-sufficiency` exists, presumably another agent's. It is outside GT-P012 and is not touched.
- No competing hub branch or PR exists.

**Charters.**
- No `AGENTS.md`, `CLAUDE.md`, cross-agent charter or federated-cycle policy exists on `main`, the GT branch or the hub branch.
- The governing hub documents are the runbook, branch-integration contract, cadence (with AD-0004) and epistemic policy at `38c2501`. They are unchanged.
- The `apply-pin` gate still requires a named human reviewer.

**Hub commit consulted (read-only, frozen into the E5D plan): `38c2501`.**

## 2. Exposure

- E5D uses the 12 published laws, whose E5A–E5C values are exposed.
- The choice of the PATHH and PCOMP questions was motivated by E5C (GT-F93, GT-F95, GT-Q25), so E5D is an adaptive follow-up, not a blind confirmation.
- The NL comparator is new. No NL value exists before the freeze.
- All six families and both sizes stay in the F_TRI matrix, including NULL, CLOSEW, CSPH and PATHF controls and negatives.

## 3. Known qualifications carried forward

- **E5A:** intact count 2/30 (GT-F90).
- **E5A:** two numerically qualified CT hub-lag channels, outside E5D.
- **E5B/E5C:** no failed frozen checks.
- **Structural:**
  - F_STAR complete renewal is impossible at N ≤ 6 (T10);
  - F_2PATH at N=5 cannot survive renewal (T14), so N5 F_2PATH is not in the E5D matrix;
  - size-1 F_TRI renewal equals a departure (GT-F87).

## 4. Research question and scope

**GT-Q25.** Are PATHH's triangle durability and PCOMP's within-class durability explained by where transition traffic sits around the anchor? Matching local and remote edge-count traffic (NL) tests this; a residual beyond NL would point to within-cell arrangement or organisation.

**Matrix (subject to the pre-freeze cost audit):**
- F_TRI({0,1}) for all 12 laws;
- F_2PATH(0) at N=6 for all six families.

That is 18 analyses. Comparators are N0, ND, NK and NL, each with its own entrance and first-renewal law.

**Stop conditions.**
- A failed NL identity on synthetic fixtures stops the freeze until the construction is fixed.
- After the freeze: no retuning and no substitute statistic; a failed check is recorded.
- After E5D: no E5E.
- The hub: no fabricated review; the canonical pin moves only through `apply-pin` by a named human.
