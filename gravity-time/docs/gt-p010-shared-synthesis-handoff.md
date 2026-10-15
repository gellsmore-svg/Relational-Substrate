# GT-P010 handoff to the shared synthesis hub

*For a future, separately reviewed hub milestone cycle. **The central synthesis (`research-synthesis/` on `main`) was not modified by GT-P010.** Nothing here is accepted. Every candidate below has `review_status=proposed`.*

## A. Provenance

| Item | Value |
| --- | --- |
| Programme branch | `research/gravity-time-admissibility` |
| GT-P010 close commit | the provenance-close commit that follows this file (recorded in `provenance/ledger.jsonl` and PR #6) |
| Frozen plan | `fc3ec7d06618a1b7ca1fb5ccdacf241ef8056c9f`, plan_hash `c35bc3bbe590fecdceb49e022aff0b99dde15d4d05e3084ccae7c0ef1db0d944` |
| Results | `fcb17ae`, payload `0d307350d1acb16a2a3a39bc638c000a6176dce8b6f4993b68d435648a0bc2d1` |
| Reports | `reports/gt-e5b-report.md`, `gt-e5b-reflection.md`, `gt-e5b-atlas.md`, `round-e5b-tables.json` |
| GT snapshot | `coherence/snapshots/through-gt-e5b.md` |
| Consulted hub commit | `38c2501bbab22ca1eb2288ea76a962ac0170d5e6` (read with `git show`; frozen into the plan) |
| Hub pins at consultation | GT `79fa6b0` (GT-P009, unreviewed); CL `e650d71` (008N, unreviewed); SC `aa06213` catalogued only |
| Hub pin state after this close | GT pin `79fa6b0` will report `behind_branch_head`. Expected; it moves only through a reviewed pin update |
| New GT records | findings GT-F83 to GT-F90; questions GT-Q23, GT-Q24; relations GT-R143 to GT-R155 |
| Review status | GT-P010 (E5B) is closed and **unreviewed**. CL 008N remains unreviewed. GT-P009 remains unreviewed |

## B. Shared questions: what to report back

| Shared question | Report |
| --- | --- |
| **XQ::01** (kinetic comparators) | NK (layer-traffic matched) and the anchor-local count materially discriminate E5A's signals. PCOMP's ×25 persistence against ND disappears; CLOSEW's shrinks to a few percent; PATHF centres survive (NK = ND for PATHF). **Differences from CL's matched-source passage:** GT projects onto edge count, with no hidden history coordinate, a CT clock and a uniform within-layer lift; CL projects (P, h1, h2) onto (P, h1) at event epochs. **Still unmatched:** within-layer arrangement and anchor-neighbourhood kinetics (GT-Q24). |
| **XQ::04** (identity through replacement) | Complete renewal is a hitting probability observed by a read-only observer: no rule reads it, and no dynamical history axis enters (8G gate not engaged). **What it proves:** an operational property of a fixed labelled anchor survives replacement of all initial partners. **What it cannot prove:** identity of a moving or unlabelled structure; F_STAR renewal at N ≤ 6 (structurally impossible, T10). **Flicker:** for single-participant entry sets, renewal equals departure and a single toggle can satisfy it, so weaker replacement measures can be mimicked by flicker. Durability is untested (GT-Q23). |
| **XQ::07** (common operator or common question) | Both programmes now use hitting and stopping-set functionals of a finite generator (CL: first return, MFPT, committors; GT: exit-before-renewal, departures). That is a shared *kind* of quantity under a shared generator vocabulary. **No common theorem is shown**, and none is claimed. |
| XQ::03 (time change versus projection) | CT lifetime, global jump count and anchor-local count are three functionals of the same full process. No events are hidden, so they differ by time change and selection, not by projection. This contrasts with CL's pair epoch, which hides triad events. |

## C. Candidate cross-programme connections (proposed only)

### C-1. NK as the GT analogue of CL's stationary-conditional projection

- **Ends:** `GT::GT-F88-NK-LAYER-TRAFFIC-COMPARATOR` ↔ `CL::F8N-H1-MATCHED-PASSAGE-BOUNDARY` (CL-T89).
- **Proposed type:** `untested_hypothesis`. The map has been checked on the GT side only.
- **Eight dimensions:**

  | Dimension | Verdict |
  | --- | --- |
  | State | differs: FREE graph versus (P, h1, h2) |
  | Transition law | differs: W4 templates versus 8M controllers |
  | Support | differs: full hypercube versus recurrent augmented class |
  | Clock | differs: CT versus event epochs |
  | Projection | analogous role: edge count k versus (P, h1) |
  | Intervention | not applicable: both compare kernels |
  | Horizon | differs: entrance episodes versus first return and MFPT |
  | Conditioning | analogous: stationary conditional rates on the projection |

- **Lineage:** shared 8G kernel and validator lineage, so not independent.
- **Falsifier:** show that, among first-order CT kernels on K lifted uniformly, NK is *not* the unique one matching the stationary adjacent-layer joint flux. That would break the CL-T89 analogy.
- **Limits:** GT-P010 and CL 008N are unreviewed.
- **Recommended decision category:** `candidate`.

### C-2. Matching the adjacent joint removes a lifetime residual in GT but not a passage residual in CL

- **Ends:** `GT::GT-F83-PCOMP-PERSISTENCE-IS-BETWEEN-LAYER-TRAFFIC` ↔ `CL::F8N-MFPT-RESIDUAL`.
- **Proposed type:** `explicit_contrast`.
- **The contrast:**
  - In CL, Kpi matches the full stationary adjacent joint on (P, h1), yet sibling MFPTs still differ (446 slower, 274 faster).
  - In GT, NK matches the adjacent-layer flux on k, and PCOMP's apparent persistence disappears.
  - The difference lies in what the projection discards: a history coordinate that carries routing (CL), versus within-layer arrangement that, for PCOMP, does not lengthen episodes (GT).
- **Eight dimensions:** as C-1; the horizon differs (MFPT versus entrance episode).
- **Counterexamples and confounds:** in GT, residuals do survive NK for PATHF, PATHH and CSPH. The contrast is family-specific, not universal.
- **Falsifiers:**
  - a GT family whose lifetime residual against NK is as large as its residual against ND would weaken the GT side;
  - a CL system where Kpi removes all passage residuals would weaken the CL side.
- **Limits:** both rounds are unreviewed.
- **Recommended decision category:** `candidate`.

Existing hub links X::0001, X::0002 and X::0009 are not restated, and E5B is not an independent confirmation of them.

## D. Review questions, disagreements and nulls to preserve

- **Disagreement:** NK is not uniformly stricter than ND. 28/90 classifications change, in both directions, so "survives a stricter control" must name the control.
- **Nulls:**
  - PCOMP and PATHH F_2PATH, and PCOMP F_STAR, are below NK at both sizes;
  - PATHF F_TRI is below every comparator on renewal;
  - CLOSEW F_2PATH is below NK at N=6.
- **Structural:** F_STAR complete renewal is impossible at N ≤ 6 (not a negative).
- **Other sources:**
  - `SC::` stays catalogued only; no SC findings are cited;
  - `HIST::` stays private and pending; no archive material is used or committed;
  - no metaphor is needed or proposed.

## E. Hub intake instruction (a future workflow, not executed)

After the human researcher reviews this GT close, a **separate hub milestone cycle**, from a hub checkout and under its own review and permissions, may run:

```bash
python3 research-synthesis/synth audit
python3 research-synthesis/synth propose-pin --source GT --commit <GT-P010-CLOSE-SHA>
# HUMAN REVIEW of the pin proposal and of candidates C-1 and C-2
python3 research-synthesis/synth apply-pin --source GT --commit <GT-P010-CLOSE-SHA> --reviewed-by "<named human researcher>"
python3 research-synthesis/synth generate
python3 research-synthesis/synth check
python3 research-synthesis/synth generate   # confirm byte-identical output
python3 research-synthesis/synth snapshot --name <approved-milestone> --title "<approved title>"
# then round-close, PR, and later ratification under docs/cadence.md
```

**Not done by GT-P010:**
- `apply-pin`, `round-close`, `ratify`, or any other hub write;
- creating a machine-readable seed file. Candidates C-1 and C-2 are given here as text; a hub cycle can stage them with `synth intake-seeds` after checking that command's schema at the hub head.

A future author instruction does not by itself grant historical publication consent, acceptance of these proposals, or scientific review of CL 008N or GT-P009/GT-P010.
