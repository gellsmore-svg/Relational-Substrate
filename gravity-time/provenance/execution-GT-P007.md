# Execution record — GT-P007 (source structure and relational gathering)

- **Prompt.** `provenance/prompts/GT-P007-agent-input.md`, an agent transcription: 33,315 bytes, sha256 `f58b607118279e1716bf61fd514ebc4a00a500123f266e49d3b3f12890027d0e`. It has not been compared with the authored external file, and no byte identity is claimed.
- **Agent.** Claude Opus 5.5, assisting one human researcher.
- **Branch.** `research/gravity-time-admissibility`. Draft PR #6, not merged.
- **Starting commit.** `75754ec`, verified as the remote head, with a clean worktree, PR #6 an open draft and CI green. OTR is byte-identical to `main`. The test baseline is 638.

## Mandate kept

- **Rounds.** E4A, plus one E4B chosen because of E4A. No E4C, no N=7, no FREE N=7.
- **Grammar.** Unchanged. No source-labelled or compensating rule exists; the E3B instrument was not reused.
- **Records.** CBO, books, Appendix E, `main` and other branches untouched. All G0–E3 plans, tables and reports unchanged. Cross-programme items are suggestions only.

## Chronology

| Commit | Content |
| --- | --- |
| `289388c` | Prompt stored; ledger row |
| `3d33aa6` | **Engineering.**<br>• Configurable held scaffold (`gt0.Scaffold`, K2/P3/K3; held slots separated from source-internal slots; class C for free source chords; symmetry = automorphisms of the held graph), routed through `gte0a`, `gtkernel`, `gtobs`, `gte1`, `gte2a`.<br>• The `gte4a` runner.<br>• Scaffold tests: exhaustive rule-string kernel equality, relabelling covariance, automorphisms, NULL geometry, floor census.<br>• The coverage and scaffold documents.<br>Suite: 733 passed |
| `f5b3b50` | **E4A frozen plan.** Hash `61e3bef23d102e94fe46a62797d072d949dd910e1ec2ec858c403c8243a4b137`; file sha256 `a5954b77…`; pushed |
| `9974a92` | Journey step 19, pushed before execution |
| — | E4A executed 19:51:47–19:55:15 UTC |
| `06e5f36` | **E4A results.** Payload `f050380ac32e`, file sha256 `fd89e8db…`; atlas |
| `8127d24` | **E4A reflection and E4A → E4B selection,** committed before any E4B code |
| `e04da91` | S4 and P4 presets; `gt0.reference_probe`; `gte4a` assembly and atlas generalised (E4A assembly re-derived identically); the `gte4b` runner and tests. Suite: 748 passed |
| `9a1c539` | **E4B frozen plan.** Hash `82fce6f3ac5d3df5319b540f271d3931e47d42814180005c4c006c568643dd3e`; file sha256 `3394370c…`; pushed |
| `93b79fc` | Journey steps 20 and 21, pushed before execution |
| — | E4B executed 20:02:35–20:08:47 UTC |
| `64e183f` | **E4B results.** Payload `169e71c33b38`, file sha256 `cdd67927…`; atlas |
| (this commit) | Formal note on witness floors; synthesis; plain-English report; transfer note; bridge-map revision 2 (sections 1–8 unchanged); ledger GT-F60–F66, GT-Q16–Q17, GT-R100–R110; register (status after E4; H-SORT); OP-16/OP-17; README; roadmap; journey step 22; this record |

## Engineering validation before freezing

- **Rule strings.** Kernels for K2, P3 and K3 at N=4, 5 equal the independent `build_kernel(rules_for(...))` implementation, with scaffold prohibitions, for six families: states, targets and weights identical.
- **Relabelling.** Relabelling P3's middle permutes the kernel exactly.
- **Free and held slots.** Held edges never dissolve; free slots always toggle; the reachable NULL class has 2^M states.
- **Symmetry.** Automorphism group sizes are correct, and the class-table symmetry check passes under P3 and K2.
- **Reference implementation.** `gt0.held_observables` equals `gtobs.held_observables` under P3.
- **Legacy reproduction.** Published triangle cells reproduce with tolerance 0: E1 HELD-N5-W4-CSPH, E2A HELD-N5-PATHH-weak_favour, E3A HELD-N5-W4-PF-strong_suppress and E3B HELD-N5-CSPH. The only differences are bookkeeping keys.
- **Floor census.** It matches the analytic floor at every state for N=4, 5, 6.
- **Cost.** Synthetic-factor fixtures at N=6 took 4.5 s (K2, 16,384 states) and 2.4 s (P3) at 170 MB. No science observable was read.

## Execution

| | E4A | E4B |
| --- | --- | --- |
| Items | 36 complete (24 new, 12 K3 replications) | 12 complete |
| Wall | 208 s (4 workers); cells 0.1–123 s | 372 s; cells 118–126 s |
| Peak memory | ≤ 315 MB | ≤ 321 MB |
| Frozen checks | W 36/36, N 6/6, R 12/12, U 6/6, G 6/6, K3 replication 12/12, Z5 36/36 | W 12/12, N 2/2, R 4/4, U 2/2, G 2/2, Z5 12/12 |

**No frozen check failed in either round.**

## Deviations and notes

1. **Reference probe** (between E4A and E4B, before the E4B freeze).
   - `gtobs` single-probe channels used vertex 3, which is a source vertex under S4 and P4. `gt0.reference_probe` now uses vertex 3 when it is a probe, otherwise the lowest probe.
   - For every legacy and E4A scaffold this is vertex 3, so nothing changed: the E4A assembly was re-derived identically.
2. **Atlas header wording.** The `gte4a.render_atlas` header wording was generalised after E4A. The committed E4A atlas was **not** regenerated; it keeps its original header.
3. **Synthesis correction before commit.** The first draft called the P4 orbits "nearly level". Rechecked against the tables, they are level only for PATHF (PATHH 0.128 against 0.159; CSPH 0.092 against 0.151), and the text was corrected.
4. **Legacy modules unchanged.** `gtscale` (E1 census) and `gte3b` (E3B instrument) keep the triangle constant. Both are published, triangle-specific modules.
5. **Overlap caveat.** At N=6 the standardised margin is partly counterfactual (18–31% of the null weight on low-mass free-edge counts). It is flagged in the atlas.

## Results (summary)

See `reports/gt-e4-report.md` and `reports/gt-e4-synthesis.md`.
- **Floor-guided sorting** within references (GT-F60), with the chord switching a site off (GT-F64).
- **Native raw gathering** under floor-free references (GT-F61), which is mostly density composition (GT-F62).
- **Total floor is not predictive** across references (GT-F63).
- **Handover orientation is invariant** across five references (GT-F65).
- **Witness-floor theorems** F1, F2 and F4 (GT-F66).
- **Not shown.** No displacement, drift or acceleration; these remain undefined.
- **Recommended next, not run.** A derivation of the sorting (GT-Q16) and an architecture review of references (GT-Q17).
