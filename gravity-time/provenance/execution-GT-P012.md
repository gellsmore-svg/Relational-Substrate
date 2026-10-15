# Execution record: GT-P012 (anchor-local kinetics, durable renewal, federated synthesis closure)

- **Prompt.** `provenance/prompts/GT-P012-agent-input.md`: the author's file, copied byte for byte (36,555 bytes, sha256 `336f19c5…9384`).
- **Agent.** Claude Opus 5.5, assisting one human researcher.
- **Branch.** `research/gravity-time-admissibility`; draft PR #6, not merged.
- **Mandate.** One frozen E5D round, then extend the hub milestone to GT-P010, GT-P011 and GT-P012, respecting the named-human pin gate.

## Starting state (verified)

- GT `a81c505` (= GT-P011 close), clean, CI green.
- Hub `main` `38c2501`; canonical GT pin `79fa6b0` (GT-P009).
- Hub PR #9 at `42a474a` (staged, not adopted).
- No charter files. A CL 8P branch exists (out of scope).
- Baseline suite 883.

## Chronology

| Commit | Content |
| --- | --- |
| `666a9b9` | Prompt (verbatim) and `docs/gt-p012-starting-audit.md`. **Before any E5D computation** |
| `3746ef1` | `docs/e5d-local-traffic-comparator.md` (T16–T19); `gtlocalcontrol.py`, `gte5d.py`; tests `test_gtlocalcontrol.py` (8) and `test_gte5d.py` (6). 897 passed; CI 38808827539 |
| `c74d896` | **Freeze:** `plans/round-e5d-plan.json`, plan_hash `6a83dbb7…1fe7`, source `3746ef1`, hub `38c2501`; committed and local bytes identical |
| `5246cce` | Journey step 30, pushed before execution |
| (run) | 2026-10-15 21:23:52Z to 21:30:23Z; 12/12 complete; 18/18 analyses |
| `6749346` | **Results:** `round-e5d-tables.json` (payload `228b7bb9d313…8def`), `gt-e5d-atlas.md` |
| this commit | Report, reflection, coverage/integrity audit, ledger GT-F98–F103, GT-Q26, GT-R167–R178; map; snapshot `through-gt-e5d.md`; hypotheses (E5D columns); bridge-map section 14; ontology note; transfer T-25–T-26; GT-side handoff; README; roadmap; journey step 31; this record |
| close | Provenance ledger row with the CI result of the synthesis commit |

## Pre-freeze computations (no NL value or E5D readout of an N=5 or N=6 scientific cell)

| Fixture | Purpose |
| --- | --- |
| N = 4 NULL, both partitions | NL = NULL |
| Synthetic N = 4 circulating, non-reversible chain, both partitions | T16/T17 with real circulation; NL non-reversible; independent stationary solve |
| Synthetic count-dependent chain | NL = NK = target |
| N = 4 PCOMP | relabelling |
| Synthetic N = 6 neighbourhood rule | timing only (NL for four anchor sets about 25 s; 357 MB) |

## Execution and checks

- 12/12 items and 18/18 analyses; every frozen check passes:
  - E5C replication for target, ND and NK;
  - NL global balance and ordered-flux identities;
  - target macro conservation;
  - durability checks;
  - the NULL fixed point at both sizes.
- No unresolved channel.

## Deviations

None from the frozen plan.

## Hub

No `research-synthesis/` file is on the GT branch. The hub milestone follows this close, on the existing hub branch `hub/gt-p010-p011-milestone` (PR #9). Its status is recorded in the PR #6 description and the final report.
