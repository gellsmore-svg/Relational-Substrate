# Starting audit: shared research-coherence infrastructure (2026-10-15)

*Written before any implementation on branch `infra/shared-research-coherence-v1`. All refs were fetched from `origin` (`gellsmore-svg/Relational-Substrate`) on 2026-10-15 and checked, not assumed.*

## 1. Inputs supplied with the task

| Input | Status |
| --- | --- |
| `01_AGENT_IMPLEMENTATION_PROMPT.md` | **Present.** Pasted in the session, with an identical copy at `C:\Users\cello\Downloads\RS_Federated_Coherence_Implementation_Prompt.md` (14,789 bytes) |
| Start message | Present (`RS_Claude_Code_Start_Message.md`, 1,261 bytes) |
| `02_ARCHITECTURE_CONTRACT.md` | **Missing.** Not found in the session, the Downloads folder, the Windows user profile (depth 6) or any recent zip |
| `03_DISCOVERY_RUBRIC.md` | **Missing** |
| `04_ACCEPTANCE_AND_REVIEW.md` | **Missing.** The acceptance list used here is Stage H of the 01 prompt, recorded in `docs/acceptance.md` |
| `05_HISTORICAL_INTAKE.md` | **Missing.** Historical intake is therefore limited to registering pending pointers |
| `seeds/source-manifest.json`, `seeds/candidate-relations.jsonl`, `seeds/metaphors.jsonl` | **Missing.** The agent drafts replacement proposals from the 01 prompt's named themes and labels them `origin: agent_drafted`. They are not the author's seeds. The `intake-seeds` command validates and stages the author's seeds when supplied |
| `background/2026-10-15-cross-research-synthesis.md` | **Missing.** Registered as a missing external source (`EXT::2026-10-15-cross-research-synthesis`) |

## 2. Repository state

| Ref | Head | Notes |
| --- | --- | --- |
| `origin/main` (default branch) | `05b15b0d903d46070b99ac84f9cab1bd898046ba` | Unchanged from the prompt's observation. Carries `research-methods/` (OTR 1.0, sha256 `2d902395…88dd`). **It holds no programme coherence ledger** |
| CL active: `research/constraint-lab-v0.8n-h2-controlled-passage` | `e650d71bda7203c8018d8bd134c5496a03d74a11` | Head commit "provenance: close Prompt 008N…". The 8N generation is **closed**; snapshot `through-generation-008n.md` was published in `cc9678b` |
| GT: `research/gravity-time-admissibility` | `79fa6b0119449bd56359acf4436015df27855f43` | GT-P009 (E5A) closed; draft PR #6 (base 8G); CI green |
| SC: `research/stochastic-calculator` | `aa06213ce42e5166ae2a0d21846a2a7c218f6b50` | Draft PR #2; last commit 2026-09-10 |
| CL 8G: `research/constraint-lab-v0.8g-formal-integration` | `22e252e560cc711d337b6ae506b0fb76728247d6` | Base of GT |

**Pull requests:**
- open drafts: #6 (GT) and #2 (SC);
- merged: #7 (OTR), #5, #4, #3.

**Ancestry:**

| Pair | Common ancestor |
| --- | --- |
| CL 8N and GT | `22e252e` (CL 8G) |
| CL 8N, GT and SC with `main` | `06cb0dc` |
| SC with 8G | none (SC does not contain 8G) |

So GT and CL share the 8G constraint-lab code, kernel and coherence validator. Agreement between them on anything inherited from 8G is **not independent evidence**.

## 3. Coherence schemas and validators

| Item | CL @ `e650d71` | GT @ `79fa6b0` | Notes |
| --- | --- | --- | --- |
| `coherence.py` blob | `1fc80911d9` | `1fc80911d9` | Identical (also at 8G) |
| findings / relations | 216 / 331 | 104 / 142 | |
| Finding fields | common core + `formal_refs` | common core + `dependence` (some rows) | Core: finding_id, statement, epistemic_layer, status, scope, evidence_refs, created_commit, created_generation, observable, magnitude_class, robustness_vector, structural_roles, temporal_character, literal_value, notes |
| Relation fields | identical | identical | |
| ID pattern | `F001-…`, `F8D-…` | `GT-F01-…`, `GT-Q…` | No collisions inside a programme. Namespacing separates programmes |
| Layers | 117 OBS, 20 INF, 45 METH, 23 OQ, 11 RS | 55 OBS, 18 INF, 7 METH, 22 OQ, 2 RS | |
| Formal catalogue | `constraint-lab/formal/theorem-catalog.jsonl` (108 rows, CL-T01 onwards); `open-problems.md` (CL-Q01–Q06) | GT theorems are in prose notes (T1–T8, S1–S7, R1–R3); no catalogue | |
| Snapshots | `constraint-lab/coherence/snapshots/` through 008n | `gravity-time/coherence/snapshots/` through E5A | Immutable; read only |

**Inherited duplicate.** The GT branch also carries `constraint-lab/coherence/{findings,relations}.jsonl` frozen at 8G (blobs identical to 8G). The federation reads CL **only** from the CL pin and never from the GT branch, so those 105 rows are not counted twice.

**SC.** There is no structured findings ledger. There are prose findings (`stochastic-calculator/RS_FINDINGS.md`, `DISCOVERIES.md`, `HYPOTHESES.md`) and run manifests. SC is registered at document level as a separate, non-equivalent test apparatus. No SC finding is ingested.

## 4. Source access, tests and limits

- **Historical archives** (505–507, Work 11, 46–48): **not found** in the repository or the local workspace. Name searches matched only unrelated files. Status: pending intake. No historical claim is promoted.
- **CI on `main`:** Node build plus report generation (`.github/workflows/ci.yml`). The shared layer adds its own path-filtered Python workflow that uses only the standard library and never runs research suites.
- **Environment:** Python 3.12.3 is available; no new dependency is introduced.
- **Ongoing experiments:** none open at the pinned heads. Both pinned heads are closed round boundaries. Later commits on either branch need a fresh pin review.
- **Non-mutation boundary:** the shared layer writes only under `research-synthesis/` and adds one workflow file. Programme ledgers, plans, results, snapshots, books and other branches are read through git objects at pinned commits.
