# GT milestone (GT-P010 and GT-P011): PROVISIONAL / UNREVIEWED

*Dated 2026-10-15. Prepared by an AI research assistant (Claude Opus 5.5) on hub branch `hub/gt-p010-p011-milestone`.*

**Status: STAGED, PENDING NAMED-HUMAN REVIEW.**
- The hub's GT pin is **not** moved. `main`, the generated index and the manifest still report GT-P009 (`79fa6b0`) until a named human reviews the pin proposal and runs `synth apply-pin`.
- Nothing here is accepted or scientifically reviewed, and none of it is evidence beyond the GT programme's own records.

## 0. Pin proposal and provenance chain

| Item | Value |
| --- | --- |
| Current hub GT pin | `79fa6b0119449bd56359acf4436015df27855f43` (GT-P009; unreviewed) |
| GT-P010 close (E5B) | `4aaf04c0601b4232fc9fa24f6aa5d5ce6390c7e2` |
| GT-P011 close (E5C), proposed pin | `a81c505a08ac5c4c83359234915bec65bb1f60c3` |
| Ancestry | `79fa6b0` → `4aaf04c` → `a81c505` (each an ancestor of the next; verified) |
| Pin proposal | `proposals/pin-updates/GT-a81c505a08ac.json` (`synth propose-pin`): descends from current = true; no warnings |
| Delta | `findings.jsonl` +18 rows (10 GT-P010, 8 GT-P011), 0 removed, **0 rewritten**; `relations.jsonl` +24 rows (13 + 11), 0 removed, 0 rewritten; validator `coherence.py` unchanged |
| Dry run (throwaway worktree, discarded) | Repinning GT to `a81c505` with `unreviewed_generations` += GT-P010, GT-P011: `synth pin`, `validate` (valid), `generate`, `check --no-git` (ok); 433 → 451 source nodes. The staged candidates (§4) also validate there |
| CL pin | unchanged at `e650d71` (008N). CL 8O closed at `99565d1` and is outside this milestone |
| SC | catalogued only; no SC findings used |
| HIST | pending intake / private; nothing used |

**Artifact-list decision for the reviewer.** The hub's pinned GT artifacts (`pin-spec.json`) predate E5B. Adoption may also add `coherence/snapshots/through-gt-e5b.md`, `through-gt-e5c.md`, the E5B/E5C reports, and the transfer notes `gt-e5b-cross-programme-transfer.md` and `gt-e5c-cross-programme-transfer.md`. `pin-spec.json` was **not** edited by hand.

## 1. GT-P010 intake (E5B)

- **Round:** frozen plan `fc3ec7d` (plan_hash `c35bc3bb…d944`); results `fcb17ae` (payload `0d307350d1ac…`); 12/12 laws, 36/36 analyses; all frozen checks pass.
- **Hub question consulted:** `38c2501`.
- **New records:** GT-F83 to GT-F90, GT-Q23, GT-Q24, GT-R143 to GT-R155.

| Finding | Content (GT's words, abbreviated) |
| --- | --- |
| GT-F88 (T11) | NK: label-covariant, reversible; matches the CT edge-count profile, **every adjacent-layer stationary flux**, E[q\|k], the mean rate and the JT density; **not** within-layer rates, local activity or correlations |
| GT-F83 | PCOMP's ×25 persistence against ND disappears against NK (vertex patterns ×0.77–0.90 in all clocks): between-layer traffic |
| GT-F84 | PATHF centres survive NK (= ND for PATHF) and the anchor-local count, with more replacement (small) |
| GT-F85 | CLOSEW mostly prevalence and traffic (×1.02–1.07; F_2PATH reverses at N=6) |
| GT-F86 | PATHH triangle/star and CSPH triangle exceed NK; CSPH flicker about double |
| GT-F87 (T10) | Complete renewal from an entry set of size s needs K−s ≥ threshold; F_STAR impossible at N ≤ 6; size-1 F_TRI renewal equals a departure |
| GT-F89 | 28/90 classifications change ND→NK; 3/30 rows clock-mixed |
| GT-F90 | **Append-only correction** of GT-F74: intact motifs outlive ND in **2/30** rows (6/30 exact ties), not 1/30 |

## 2. GT-P011 intake (E5C)

- **Round:** frozen plan `469ee28` (plan_hash `bab7a59d…6e47`); results `5080199` (payload `582e845ba338…`); 12/12 laws, 24/24 analyses; all frozen checks pass (R0 replicates E5B; T13 zero violations; return + exit = 1; NULL fixed point).
- **New records:** GT-F91 to GT-F97, GT-Q25, GT-R156 to GT-R166.

| Finding | Content |
| --- | --- |
| GT-F91 | Renewal is transient in every law (C_4 ≲ 0.08): no self-maintaining renewed organisation at N ≤ 6 |
| GT-F92 | CSPH triangle renewal is **flicker-assisted**: R0 ×2.2–2.6 against NK but C_1 ×0.84–0.86; original return before exit 2.5–3× NK |
| GT-F93 | PATHH triangle survives renewal better than NK at both sizes and in both entry classes (size-1 C_4 0.055 against 0.026; 0.077 against 0.048); returns at NK's level |
| GT-F94 | PATHF's advantage fades after one anchor event; PATHF triangle below NK |
| GT-F95 | PCOMP size-≥2 triangles: within-class C_4 ×1.5–2.2 against NK (small absolute values), a within-layer effect hidden in pooled lifetimes |
| GT-F96 (T13, T14) | Remote toggles never leave the renewed set but change later rates (kernel (I − P_rem)⁻¹ P_loc); F_2PATH at N=5 cannot survive renewal |
| GT-F97 | The first-hit law differs from the stationary restriction (L1 0.3–1.7); all E5C values use first-hit conditioning |

**Negative rows kept:**
- PATHF triangle;
- PATHH F_2PATH;
- CLOSEW (at or below NK);
- CSPH conditional survival;
- F_STAR infeasibility;
- F_2PATH at N=5 structural zero.

## 3. Cross-programme coherence (interpretation; not evidence)

| Shared question | GT-P010 + GT-P011 contribution | Boundary |
| --- | --- | --- |
| **XQ::01** | NK controls layer traffic; residual effects (PATHF/PATHH durations, PATHH triangle durability, PCOMP size ≥ 2) sit in within-layer and anchor-local arrangement (GT-Q24, GT-Q25) | NK is not CL's Kpi; the CL matched-source control was not transplanted |
| **XQ::04** | Renewal and durability are trajectory observables without a history axis; the return/exit split separates flicker (CSPH) from durable renewal (PATHH) | Fixed analyst anchor; mobile identity undefined |
| **XQ::07** | GT quantities are hitting and resolvent functionals: first-hit laws and powers of a local-event kernel. CL 8O (not pinned here) reports a Markovization–stopping defect factorization | **Shared vocabulary only.** No common theorem; a proper comparison needs the CL 8O pin and an eight-dimension check |
| XQ::03 | Anchor-local counts integrate inert remote events exactly (T13): selection within one process, not a time change hiding events | CL's pair epoch does hide state-changing triad events |

**Scope comparison with CL controlled passage (CL `e650d71`):**

| Dimension | GT | CL |
| --- | --- | --- |
| State | FREE graph | (P, h1, h2) |
| Transition law | W4 templates | 8M controllers |
| Support | full hypercube | recurrent augmented class |
| Clock | CT, jump count, anchor-local count | pair-event epochs |
| Projection | edge count (NK) | (P, h1) (Kpi) |
| Intervention | none | none |
| Horizon | entrance episodes, renewal, survival | first return, MFPT, committors |
| Conditioning | Palm entry; first-hit law | stationary class-conditioned sources |

**Lineage:** shared 8G (`22e252e`); no independence.

## 4. Staged candidate connections (proposed; not in the live registry)

Staged in `proposals/staged/2026-10-15-gt-p010-p011-candidates.jsonl`, generated by `proposals/stage_gt_p010_p011.py`, with origin `agent_drafted`, status `proposed` and category `candidate`. They are appended to `candidate-relations.jsonl` only **after** pin adoption, because they cite GT findings absent from the current pin. They validate at the proposed pin (dry run).

| Id | Ends | Type | Note |
| --- | --- | --- | --- |
| P::GT-C1 | GT-F88 ↔ CL::F8N-H1-MATCHED-PASSAGE-BOUNDARY | untested_hypothesis | NK as a stationary-conditional lift on K; falsifier: non-uniqueness among uniform lifts |
| P::GT-C2 | GT-F83 ↔ CL::F8N-MFPT-RESIDUAL | explicit_contrast | Shares the CL endpoint with X::0001 but is a different, contrastive relation |
| P::GT-C3 | GT-F97 ↔ CL::F8N-MATCHED-SOURCE-PASSAGE | epistemic_compatibility | Explicit source laws for post-event functionals (methodological) |

No metaphor is proposed. No `X::` record, decision or acceptance is created.

## 5. Open questions and contradictions kept live

- Stationary occupancy, layer traffic, within-layer rate placement, lifetime, renewal, durability, controlled passage and predictive sufficiency are **different quantities**. NK changed 28/90 GT classifications, in both directions.
- PCOMP: no lifetime excess beyond NK, yet a within-class durability excess. Pooled and within-class views disagree.
- CSPH: strong renewal, weak survival.
- GT-Q24 and GT-Q25: is there a within-layer or anchor-local comparator that would explain the residuals?

## 6. Required human actions (in order)

1. **Review** this report and `proposals/pin-updates/GT-a81c505a08ac.json`, including the artifact-list decision in §0.
2. If approved, run from a hub checkout:
   ```bash
   python3 research-synthesis/synth apply-pin --source GT --commit a81c505a08ac5c4c83359234915bec65bb1f60c3 --reviewed-by "<your name>"
   ```
   Then set GT `unreviewed_generations` to include GT-P010 and GT-P011 if not already done, and decide the artifact list.
3. `synth generate`; `synth check`; run `generate` again to confirm byte identity; `python3 -m unittest discover -s research-synthesis/tests`.
4. Append the staged candidates (§4) to `proposals/candidate-relations.jsonl` and re-validate.
5. `synth snapshot --name <milestone> --title "..."`, then `synth round-close` under `docs/cadence.md` (AD-0004: the closing commit must display any recommendations).

The pin's presence is not acceptance of GT's claims. GT-P010 and GT-P011 stay *closed but scientifically unreviewed* until a separate scientific review.

---

*Addendum (later on 2026-10-15): superseded as the pin **target** by `2026-10-15-gt-p010-p012-milestone-provisional.md`, which proposes GT → `e2b5dc4` (GT-P012 close) and includes every row of this proposal. This report is unchanged above and kept as the audit trail.*
