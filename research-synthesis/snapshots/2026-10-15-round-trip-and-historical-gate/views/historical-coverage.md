# Historical coverage and source attestation

**HIST status:** `pending_intake`. Intake plan `HIST-INTAKE-2026-10-15`: **awaiting_archives**.

Historical archives are private and stay outside the repository. A `HIST::` reference resolves only to a registered finding that was source-verified at intake and approved for publication by a logged human decision. Everything else stays pending, and records citing it stay `blocked_missing_source`.

Verification levels are separate: **local source verified** (bytes hashed at intake), **public pointer attested** (record consistent, but CI cannot rebuild it), **numerically reproduced** (independently recomputed). Author acceptance is a review status, not a verification level.

## Archives

| Archive | Expected sha256 | Expected members | State |
| --- | --- | ---: | --- |
| `RS_Work_Research.zip` | `3ecfd22f9d4b64c1…` | 403 | inaccessible |
| `RS_Work_Round46_Supplement.zip` | `630da2d942b15247…` | 9 | inaccessible |

## Coverage matrix

Unknown means unknown, not false.

| Source (landmark) | Question | Expected role | Inventoried | Read | Source-attested | Structured findings | Cross-compared |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| `rs_work_round11/findings.md` | A | primary_report | no | no | no | 0 | no |
| `rs_work_round46_moments/REPORT.md` | A | primary_report | no | no | no | 0 | no |
| `rs_work_round47/REPORT.md` | A | primary_report | no | no | no | 0 | no |
| `rs_work_round48/REPORT.md` | A | primary_report | no | no | no | 0 | no |
| `rs_sources/RS_Baseline_Post_506Z/RS_Baseline_Post_506Z/02_EXPERIMENT_LEDGER_505_506.md` | B, C | run_ledger | no | no | no | 0 | no |
| `rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` | B, C | run_ledger | no | no | no | 0 | no |
| `rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_Post_507_Canonical_Baseline.md` | E | retrospective_baseline | no | no | no | 0 | no |
| `rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_508_Starting_Questions.md` (A question or plan unless a separate executed result is shown; 508 is not counted as run.) | plan | future_question | no | no | no | 0 | no |
| `rs_work_round32_to35/RECOVERED_CONVERSATION_RECORD.md` (Retrospective recovered content, not a contemporaneous execution report; may contain private conversation and must not be published.) | provenance | recovered_record | no | no | no | 0 | no |
| `rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Negatives_And_Corrections.md` (Named by the external synthesis (EXT-C13); not in the pack's list of verified entry paths.) | B, C | correction | no | no | no | 0 | no |

Registered historical findings: **0**.

## Records blocked on historical sources

| Record | Kind | Decision | Missing anchors |
| --- | --- | --- | --- |
| `P::0005` | proposal | blocked_missing_source | `HIST::505-507` (no_member_path_named) |
| `P::EXT-C01` | external_claim | blocked_missing_source | `HIST::rs_work_round11/findings.md` (archive_inaccessible)<br>`HIST::rs_work_round46_moments/REPORT.md` (archive_inaccessible)<br>`HIST::rs_work_round47/REPORT.md` (archive_inaccessible)<br>`HIST::rs_work_round48/REPORT.md` (archive_inaccessible) |
| `P::EXT-C03` | external_claim | blocked_missing_source | `HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` (archive_inaccessible) |
| `P::EXT-C04` | external_claim | blocked_missing_source | `HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` (archive_inaccessible) |
| `P::EXT-C07` | external_claim | blocked_missing_source | `HIST::rs_sources/RS_Baseline_Post_506Z/RS_Baseline_Post_506Z/02_EXPERIMENT_LEDGER_505_506.md` (archive_inaccessible)<br>`HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` (archive_inaccessible) |
| `P::EXT-C11` | external_claim | blocked_missing_source | `HIST::rs_work_round46_moments/REPORT.md` (archive_inaccessible)<br>`HIST::rs_work_round47/REPORT.md` (archive_inaccessible) |
| `P::EXT-C13` | external_claim | blocked_missing_source | `HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` (archive_inaccessible)<br>`HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Negatives_And_Corrections.md` (archive_inaccessible) |
| `P::EXT-C18` | external_claim | blocked_missing_source | `HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` (archive_inaccessible) |
| `P::SYN-C001` | seed_claim | blocked_missing_source | `HIST::rs_work_round11/findings.md` (archive_inaccessible) |
| `P::SYN-C005` | seed_claim | blocked_missing_source | `HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` (archive_inaccessible) |
| `P::SYN-C008` | seed_claim | blocked_missing_source | `HIST::rs_sources/RS_Baseline_Post_507/RS_Baseline_Post_507/RS_507_Integrated_Ledger.md` (archive_inaccessible) |
| `XQ::05` | shared question | pending_source | `HIST::505-507`<br>`HIST::work-11`<br>`HIST::46-48` |

## Cautions

- 403 ZIP entries are not 403 experiments; completeness of the 600+ experiment corpus is not established.
- The Round 46 supplement is not later authority because of its filename; compare versions.
- ZIP timestamps are metadata, not research dates.
- Separate the v1.7 baseline (through Experiment 464), the 505-507 line and the Work 1-48 sequence; link numbering systems only where a source proves it.
- Never execute .py, .pyc or serialised data from the archives.
