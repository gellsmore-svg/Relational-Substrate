# GT milestone (GT-P010, GT-P011, GT-P012): PROVISIONAL / UNREVIEWED

*Dated 2026-10-15. Prepared by an AI research assistant (Claude Opus 5.5) on hub branch `hub/gt-p010-p011-milestone` (draft PR #9). It extends `2026-10-15-gt-p010-p011-milestone-provisional.md`, which is retained unchanged.*

**Status: HUB STAGED THROUGH GT-P012, CANONICAL PIN STILL `79fa6b0119449bd56359acf4436015df27855f43`.**
- No named-human review of this pin proposal exists (PR #9: 0 reviews, 0 comments). `apply-pin` was not run, and `sources/pin-spec.json` and `manifest.json` are unchanged.
- Nothing here is accepted or scientifically reviewed.

## 0. Provenance chain and pin proposal

| Round | Freeze / results / close | Plan hash | New GT records |
| --- | --- | --- | --- |
| GT-P009 (current pin) | — / — / `79fa6b0` | `31202d70…97a8` | (pinned) |
| **GT-P010** (E5B) | `fc3ec7d` / `fcb17ae` / `4aaf04c` | `c35bc3bb…d944` | GT-F83–F90, GT-Q23, GT-Q24; GT-R143–R155 |
| **GT-P011** (E5C) | `469ee28` / `5080199` / `a81c505` | `bab7a59d…6e47` | GT-F91–F97, GT-Q25; GT-R156–R166 |
| **GT-P012** (E5D) | `c74d896` / `6749346` / `e2b5dc4` | `6a83dbb7…1fe7` | GT-F98–F103, GT-Q26; GT-R167–R178 |

- **Ancestry:** `79fa6b0` → `4aaf04c` → `a81c505` → `e2b5dc4`, verified.
- **Pin proposal (target):** `proposals/pin-updates/GT-e2b5dc4cb65b.json` (`synth propose-pin`; descends from the current pin; no warnings).
  - findings and questions: 25 added (10 + 8 + 7), 0 removed, **0 rewritten**;
  - relations: 36 added (13 + 11 + 12), 0 removed, 0 rewritten;
  - validator unchanged.
- **Earlier proposal:** `GT-a81c505a08ac.json` (through GT-P011) is retained as the audit trail. The new proposal includes all of its rows, so a single reviewed pin to `e2b5dc4` loses nothing.
- **Pin-spec entry (artifact-list gap closed as a proposal):** `proposals/pin-updates/GT-e2b5dc4cb65b-pin-spec-entry.json` gives the current and proposed GT entries.
  - **Commit:** `e2b5dc4`.
  - **`unreviewed_generations`:** GT-P009 to GT-P012.
  - **Nine new artifacts:**
    - snapshots `through-gt-e5b.md`, `through-gt-e5c.md`, `through-gt-e5d.md`;
    - transfer notes `gt-e5b-`, `gt-e5c-` and `gt-e5d-cross-programme-transfer.md`;
    - reports `gt-e5b-`, `gt-e5c-` and `gt-e5d-report.md`.
  - All ten original artifacts are retained unchanged. `pin-spec.json` was not edited.
- **Dry run** (throwaway worktree, discarded):
  - applying the proposed entry and the four staged candidates, `synth pin` → `validate` (valid) → `generate` → `check --no-git` (ok);
  - 433 → 458 source nodes, 50 → 54 proposals;
  - all 19 GT artifacts verify at the new pin;
  - the would-be generated index shows GT at `e2b5dc4` with 129 nodes.
- **Unchanged:** CL pin `e650d71` (CL 8O and 8P are separate milestones); SC catalogued only; HIST private and pending.

## 1. GT-P010 (E5B)

See the retained report §1 (NK comparator T11, PCOMP and CLOSEW corrections, PATHF/PATHH/CSPH qualifiers, T10, and the 2/30 E5A correction). Unchanged.

## 2. GT-P011 (E5C)

See the retained report §2 (first-hit law T12, transient renewal, CSPH flicker, PATHH durability beyond NK, T13/T14). Unchanged.

## 3. GT-P012 (E5D): new

- **Instrument (GT-F98, T16–T19).** NL lifts the target's *ordered* stationary fluxes on the (local, remote) edge-count projection around the anchor.
  - It is stationary by macro-flux conservation alone, with no detailed balance.
  - It matches every ordered macro flux, and therefore everything NK matches.
  - It is unique among pool-exchangeable lifts, and reversible iff no macro current exists.
- **Circulation (GT-F99).** PATHF, PATHH and CSPH carry projected net currents of 0.43–0.98, so NL is non-reversible for them. CLOSEW and PCOMP carry none.
- **Results:**

| Finding | Content |
| --- | --- |
| GT-F100 | PATHH triangle post-renewal survival exceeds NL at both sizes and in both entry classes (C_4 ×1.99 at N5, 0.055 against 0.028; ×1.44 at N6, 0.077 against 0.053); original returns at NL's level |
| GT-F101 | PATHF's centre effect is local/remote traffic: R0 ×1.32 → ×1.00, C_1 ×1.27 → ×1.01 against NL |
| GT-F102 | PCOMP size-≥2 triangle class residual survives NL (×2.2–2.4; small absolute values); no circulation; large within-cell rate dispersion |
| GT-F103 | CSPH triangle renewal remains flicker-assisted under NL (returns 2.1–2.4× NL) |

- **Negatives kept:** PATHF triangle below every comparator; CLOSEW near control; PCOMP pooled near control.
- **Open (GT-Q26):** is PATHH's residual within-cell arrangement or organisation? A completer-resolved projection would partly read the predicate.

## 4. Cross-programme coherence (interpretation only)

| Question | Contribution | Boundary |
| --- | --- | --- |
| XQ::01 | Refining the projection (k → (ℓ,r)) explained PATHF but not PATHH or PCOMP-class: comparator adequacy is family-specific and projection-relative | NL is not CL's Kpi |
| XQ::03 | Anchor-local counts integrate inert remote events (T13); NL's circulation is a projection property, not hidden events | — |
| XQ::04 | Durability with a return/exit split separates flicker (CSPH) from durable renewal (PATHH), which also survives NL | fixed analyst anchor |
| XQ::07 | GT now uses first-hit laws, local-event kernels and stationary-flow lifts on projections. CL 8O (not pinned) reports a stopping–Markovization factorization | shared vocabulary only; no common theorem; requires the CL 8O pin and an eight-dimension comparison |

**Eight-dimension scope against CL controlled passage:**

| Dimension | GT | CL |
| --- | --- | --- |
| State | graph | (P, h1, h2) |
| Transition law | W4 | 8M |
| Support | full | recurrent class |
| Clock | CT, jump count, local count | epochs |
| Projection | k (NK) and (ℓ, r) (NL) | (P, h1) |
| Intervention | none | none |
| Horizon | episode, renewal, survival | return, MFPT |
| Conditioning | Palm and first-hit | stationary class sources |

**Lineage:** 8G (no independence).

## 5. Staged candidates (`proposals/staged/`, agent_drafted, proposed, candidate)

| Id | Ends | Type | From |
| --- | --- | --- | --- |
| P::GT-C1 | GT-F88 ↔ CL::F8N-H1-MATCHED-PASSAGE-BOUNDARY | untested_hypothesis | GT-P010 |
| P::GT-C2 | GT-F83 ↔ CL::F8N-MFPT-RESIDUAL | explicit_contrast | GT-P010 |
| P::GT-C3 | GT-F97 ↔ CL::F8N-MATCHED-SOURCE-PASSAGE | epistemic_compatibility | GT-P011 |
| **P::GT-C4** | GT-F98 ↔ CL::F8N-H1-MATCHED-PASSAGE-BOUNDARY | requires_scope_alignment | GT-P012 (new) |

- C-1 to C-3 keep identical content; only their `staged_pending` note now names both pins.
- No duplicates. C-2 shares a CL endpoint with X::0001 but is a different, contrastive relation.
- All four validate at the proposed pin.

## 6. Required named-human action

1. Review this report, `GT-e2b5dc4cb65b.json` and `GT-e2b5dc4cb65b-pin-spec-entry.json`.
2. If approved:
   ```bash
   python3 research-synthesis/synth apply-pin --source GT --commit e2b5dc4cb65bafc423047f78468a63c9d6ceb218 --reviewed-by "<your name>"
   ```
   Then make the GT entry in `sources/pin-spec.json` equal `proposed_entry` (artifacts and `unreviewed_generations`), and run `synth pin`.
3. Run `synth generate`; `synth check`; `generate` again (byte identity); the hub tests.
4. Append the four staged candidates to `proposals/candidate-relations.jsonl`, then `synth validate`.
5. `synth snapshot --name 2026-10-15-gt-p012-milestone --title "..."`, then `synth round-close` (AD-0004).

The pin's presence is not acceptance of GT claims; the GT rounds remain closed and scientifically unreviewed.
