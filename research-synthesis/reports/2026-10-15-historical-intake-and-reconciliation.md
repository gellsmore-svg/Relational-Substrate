# Historical intake and reconciliation (2026-10-15)

**Epistemic status:** a dated report by an AI research assistant (Claude Opus 5.5). It is not experiment evidence. It changes no programme record.

**Outcome in one line:** the historical intake stopped at the custody gate. Neither private archive was available, so **no historical source was read and nothing historical was integrated.** This round delivered the safe, independent parts:
- the implicit round-trip acceptance rule;
- a historical source adapter with its tests;
- a coverage view;
- a source-specific re-evaluation of every record blocked on historical sources.

## 1. Custody gate

| Archive | Required sha256 | Found |
| --- | --- | --- |
| `RS_Work_Research.zip` (403 members) | `3ecfd22f…1e46` | **No** |
| `RS_Work_Round46_Supplement.zip` (9 members) | `630da2d9…4b5e` | **No** |

**Where I searched (by name), with nothing found:**
- the Linux home directory;
- the whole Windows user profile, including Downloads, Documents, Desktop and OneDrive;
- the member list of `chatgpt-history.zip` (5,184 entries, read without extraction).

**What arrived and what did not:**
- The optional integrity manifest (`RS_Historical_Archive_Integrity_Manifest_2026-10-15.json`) was not present either.
- The intake prompt itself was in Downloads.
- The pack's controlled-intake procedure, `05_HISTORICAL_INTAKE.md`, was available inside the author pack ZIP and was read.

As the instruction requires, nothing was reconstructed from:
- the earlier external synthesis;
- model memory;
- semantic search.

`HIST` remains `pending_intake`.

## 2. What the archives contain, and what they establish

**Unknown.** Nothing here has been inventoried. The figures in the pack are:
- 403 and 9 ZIP members;
- report and ledger material through historical Experiment 507;
- a v1.7 baseline through 464.

They are the earlier synthesis's own observations, recorded as unverified reference metadata. 403 members are not 403 experiments. The 600-plus experiment corpus is not established as complete or even present.

## 3. Coverage and numbering map

All ten landmarks are at **not inventoried**. The full matrix is in [`generated/historical-coverage.md`](../generated/historical-coverage.md). No link between the v1.7 numbering, the 505–507 line and the Work 1–48 sequence is source-proven yet.

## 4. Relationship table

| Category | Count | Records |
| --- | ---: | --- |
| Admitted historical relations | 0 | — |
| Proposed historical relations | 0 | — (new proposals wait for source-attested findings) |
| Still blocked on historical sources | 11 + 1 question | P::0005; SYN-C001, C005, C008; EXT-C01, C03, C04, C07, C11, C13, C18; XQ::05 |
| Contradicted or rejected by primary sources | 0 | — (no primary source read) |

Each blocked record now carries its **specific missing anchors**, plus an agent decision-history entry (`reassessment: HIST-INTAKE-2026-10-15`). For example:
- SYN-C001 needs `rs_work_round11/findings.md`.
- EXT-C13 needs the 507 integrated ledger and `RS_507_Negatives_And_Corrections.md`. The second is named only by the external synthesis and is not in the pack's list of verified paths.
- `HIST::505-507` (P::0005, XQ::05) is a range, not a file. It needs mapping to primary reports at intake.

## 5. Questions A–F: what each needs before any comparison

| Question | Primary sources | CL/GT side, already public | Discriminator to apply at intake |
| --- | --- | --- | --- |
| A. Predictive sufficiency | Work 11; Work 46–48 reports | CL 8H/8K/8M/8N (H1-vs-H2 matching) | Is the failure information loss under a *specified* intervention, or a compilation choice? State the operators; do not assume they are identical. |
| B. Retention and reconstruction | 505/506 ledger; 507 integrated ledger | GT E5A (intact vs flexible lifetimes; PCOMP rate heterogeneity) | Survival of a selected predicate ≠ identity through replacement; reconstruction ≠ occupation; check the activity-heterogeneity confound. |
| C. Higher-order effects | 505–507 interaction/context findings | CL roles, gates and composition; GT witness floors and site sorting | The strongest formal comparison and the strongest counterexample; shared vocabulary is not shared mechanism. |
| D. Stable outputs | (to be located) | SC, catalogued only | A methodological analogy at most; SC stays `catalogued_only` until a structured ledger exists. |
| E. Ontology versus model | 507 canonical baseline | CL/GT formal claims | Keep interpretation, mathematics, physics and theology apart; no primitive is added. |
| F. v1.7 baseline to 464 | (to be located) | — | Future-equivalence and representation-cost discipline (from 05). |

## 6. The previous external synthesis after this round

The previous external synthesis (stored as EXT-SYNTH-20261015) is unchanged in standing:
- Its seven historical claims remain **unverified**.
- Its 15 checkable claims stay `under_review` as before.
- Its three cross-programme restatements (EXT-C08-R1, C09-R1, C20-R1) are unaffected.

Nothing in it survives, changes or fails on primary evidence yet, because no primary evidence was read.

## 7. What did change: implicit acceptance through the round trip

The author's rule, "human accept needs to be implicit in the round trip process", is now in the tooling (`docs/cadence.md`). It applies as follows:
- A round ends with `synth round-close`, which lists the agent's reported recommendations.
- The author's next instruction ratifies that list as a logged human decision (`synth ratify`), except for items the author objects to.
- Ratification accepts at the reported category and never upgrades it.

**Applied once, retrospectively.** RT-0001, the round that ended at `0dbc9d2`, was ratified by AD-0002, which made two changes:
- **X::0001–0009 are `human_accepted`.** X::0003, X::0004 and X::0005 are `accepted_bounded`; the rest are `qualified`. The six that rest on CL 008N or GT-P009 stay `qualified` under the unreviewed-round cap.
- **The six reviewed metaphors are `human_accepted`.** They are still non-evidentiary.

**Where it departs from the intake instruction.** The instruction said not to promote `agent_reviewed` relations to `human_accepted`. The author's message that came with it overrides this, and the override is recorded in AD-0002.

**What it leaves unchanged:**
- AD-0001 is preserved; SYN-C003's seed wording is untouched.
- CL 008N and GT-P009 remain unreviewed **rounds**. The round trip accepts synthesis records; it does not review a programme's scientific round.

## 8. Explicit non-claims

- No historical finding is integrated, and no historical claim is used as evidence.
- No physical gravity, time or quantum model is derived.
- No complete 600-plus experiment corpus is established.
- No ontology is promoted by metaphor.
- No independence is asserted where apparatus or proof ancestry overlaps.

## 9. Next bounded options (not run)

1. **Supply the archives** outside the repository and repeat this round from the gate. The code path is ready: `hist-inventory`, then findings, then `check` with `RS_HIST_ARCHIVE_DIR`. Trade-off: none beyond the author's time; this is the only route to real historical integration.
2. **Approve a publication policy first.** Decide whether member paths and short derived summaries may be public, so the first findings do not stall at the privacy check. Trade-off: one more decision before intake, fewer stops during it.
3. **Narrow the first intake to question A** (Work 11, 46–48: four files). This is the smallest set that tests the strongest external claim (EXT-C01) against CL's exact H1-vs-H2 results. Trade-off: B–F wait for a later round.

## Addendum (later on 2026-10-15): archives supplied; custody verified; publication awaits consent

The body above is unchanged; it was written while the archives were absent.

- **Custody passed.** The author's closeout transfer bundle supplied both archives. Whole-file sha256 and member counts match, every file member matches the bundle's integrity manifest, and no member is unsafe. Inner archives were not extracted and nothing was executed.
- **Sources read.** The priority sources (Work 11, 45, both Work 46 branches, 47, 48; the 505-507 ledgers, negatives, the post-507 baseline and the 508 plan) were read read-only from the ZIP members.
- **Nothing historical is public yet.** Derived findings, cross-programme candidates and the assessment of every blocked record are staged privately outside the repository. The closeout instruction requires an explicit, scoped `publication_consent` decision, and AD-0002 is not consent. HIST therefore stays `pending_intake`, and the 11 blocked records and XQ::05 stay blocked, each with an appended re-evaluation entry (`HIST-INTAKE-2026-10-15-B`).
- **Next.** The operational readiness report (`reports/2026-10-15-operational-readiness.md`) carries the release gates and the decision requested.
