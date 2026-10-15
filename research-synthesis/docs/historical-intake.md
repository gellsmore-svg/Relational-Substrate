# Historical intake

The old mathematical programme lives in two private archives. This page sets out how they enter the shared layer without the public repository becoming a mirror of them.

**Current state (2026-10-15, later):** archives supplied in the author's closeout bundle and verified (whole-file and member hashes); priority sources read locally. `HIST` stays `pending_intake` because no `publication_consent` decision has been recorded: derived findings are staged privately outside the repository. See [`generated/historical-coverage.md`](../generated/historical-coverage.md).

## Sources of this procedure

- The pack's controlled-intake procedure, `05_HISTORICAL_INTAKE.md`, in `RS_Shared_Coherence_Implementation_Pack_2026-10-15.zip` (sha256 `e1f7d94d…cdbd`).
- The author's instruction of 2026-10-15, *Historical Corpus Intake and Cross-Programme Reconciliation*.
- The machine-readable plan: [`sources/historical/intake-plan.json`](../sources/historical/intake-plan.json).

## 1. Custody gate (mandatory)

| Archive | Required sha256 | Members |
| --- | --- | ---: |
| `RS_Work_Research.zip` | `3ecfd22f9d4b64c17c2a2c9c198615ee1e1c6e3d08512e6971ae7b4090261e46` | 403 |
| `RS_Work_Round46_Supplement.zip` | `630da2d942b15247a164d5e1fd262f759483941210f38a9ab29b12c1a6ce4b5e` | 9 |

- Keep the archives **outside the Git working tree**, for example `../rs-private-historical-inputs/`.
- Inventory them with `synth hist-inventory`, writing to a directory outside the repository:

  ```
  python3 research-synthesis/synth hist-inventory \
    --archive ../rs-private-historical-inputs/RS_Work_Research.zip \
    --archive ../rs-private-historical-inputs/RS_Work_Round46_Supplement.zip \
    --out ../rs-private-historical-inputs/inventory
  ```

- The inventory never extracts anything. It hashes the whole file and every member, and flags:
  - absolute paths, parent-directory traversal, backslashes;
  - duplicate (and case-folded duplicate) paths;
  - symbolic links and encrypted members;
  - nested archives (inventoried as bytes, never opened);
  - members over the decompression limits;
  - code and serialised data (`never_execute`).
- **A whole-file hash mismatch or a wrong member count stops intake.** A file with the right name but the wrong bytes is not used.

## 2. Inventory, chronology and coverage

- The inventory records path, size, ZIP timestamp (metadata only), media type, member sha256, privacy review state and source role.
- Distinguish executed experiment, round, report, derived statement, theory proposal and roadmap item. **403 ZIP entries are not 403 experiments.**
- Map experiment ids to primary reports and correction lineage. Lexical order is not chronology.
- Keep the v1.7 baseline (through 464), the 505–507 line and the Work 1–48 sequence apart, linking numbering systems only where a source proves it.
- 508 stays an unverified boundary unless an executed primary record shows otherwise. The 32–35 recovered conversation record is retrospective, not a contemporaneous report.

## 3. Public derived records

Records live in `sources/historical/findings.jsonl` as `HIST::<id>`. Each one carries:
- the archive id, archive sha256, member path, member sha256 and a section or line anchor;
- the experiment or round id, evidence layer and source role;
- a short derived summary and a precisely scoped claim, with no invented wording;
- the model, state, parameters, clock, projection, intervention, comparison and horizon, where known;
- outcome and limitations (failed controls, fragility, numerical status, correction, supersession);
- the verification level, privacy disposition, provenance, review status and decision history.

`synth check` enforces the following rules:

| Rule | Check |
| --- | --- |
| No findings while `pending_intake` | A finding cannot exist before intake. |
| `included_partial` needs a usable finding | At least one finding must be source-verified and approved, and the verified archive hashes must match. |
| Evidence layers | One of: observation, exact_result, simulation_result, inference, interpretation, negative_null, question, plan. |
| Verification levels are kept apart | `local_source_verified` and `numerically_reproduced` need the intake inventory digest. `numerically_reproduced` needs a reproduction record. Author acceptance is not a level. |
| Privacy | A public record needs `public_summary_approved`, given by a logged **human** decision. Summaries are short. Quotes over 160 characters need quote approval. |
| Conflicts | Two findings for one experiment citing different files must declare supersession or conflict. |
| Gaps stay pending | A `HIST::` reference that is not a usable finding stays pending, and any record citing it stays `blocked_missing_source`. |

## 4. What CI can and cannot check

- **Without the archives**, CI checks the public records and their internal consistency (level 2, *public pointer attested*). It reports the private checks as `requires_private_input`, never as passed.
- **With the archives**, set `RS_HIST_ARCHIVE_DIR` (or run `synth hist-verify --archive-dir <dir>`) to re-hash every cited member. A mismatch is an error.

## 5. Then, and only then

- Propose cross-programme edges through the normal proposal and review workflow, comparing:
  - model and state;
  - transition law and support;
  - clock, projection and intervention;
  - horizon and conditioning;
  - lineage, controls and alternatives.
- Re-evaluate the blocked records in [`historical-coverage.md`](../generated/historical-coverage.md) from the primary sources.
- Acceptance follows the round trip (`docs/cadence.md`). It never upgrades a category.

## Publication consent (AD-0004)

Source integrity and publication permission are separate. A public `HIST::` record needs an explicit human decision of kind `publication_consent` in `proposals/author-decisions.jsonl`. It may carry `limits` (maximum characters per field) and `excluded_members`; the validator enforces both. Round-trip acceptance is never consent. Until consent exists, findings are kept in a private review packet outside the repository with disposition `awaiting_publication_approval`.
