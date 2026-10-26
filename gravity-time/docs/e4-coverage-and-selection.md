# GT-P007 coverage audit and selection (before E4A)

*Deliverable 1. Written before the E4A plan was frozen and before any K2 or P3 scientific cell was computed.*

## 1. Starting state

- **Repository.** Branch at `75754ec` (GT-P006 close). Clean worktree; CI green on both events; PR #6 an open draft. OTR 1.0 is byte-identical to `main`. The test baseline is 638.
- **Materials read:**
  - the charter, roadmap, hypotheses, journey and coherence map;
  - the E3 report, synthesis and reflection;
  - the E3 formal note (T7, T8, §7.6–7.7);
  - the bridge map;
  - the E3B plan, tables and atlas, and the GT-P006 provenance;
  - the E1 report (clock and density qualifications);
  - the E2 formal note;
  - the laboratory's plan discipline and 8G gate;
  - the code of `gtkernel`, `gtobs`, `gt0`, `gte0a`, `gte1`, `gte2a` and the batch wiring.

## 2. What was executed before, and what exposure exists

| Material | Cells | Exposure for E4A |
| --- | --- | --- |
| E0B HELD N=5/6 (triangle) | NULL, PATHF ws, PATHH wf, CLOSEW wf, PCOMP, CSPH | All standard channels published. The 12 K3 cells of E4A are **replications** |
| E1 HELD N=5–7 (triangle) | CSPH, CSPF, CWPH, CWPF, PATHF, PATHH, NULL, CLOSEW | N=7 is cited only |
| E3B HELD N=5/6 (triangle, neutralised instrument) | The same families plus PATHF wf, PATHH ws, CWPH | Neutralised margins are known. They are cited beside native results and never pooled |
| K2 and P3 | — | **Never computed before GT-P007.** Engineering tests used N=4/5 kernels (rule-string equality, covariance, symmetry, NULL geometry) and one P3 N=5 PATHF ws attachment-fraction equality between two implementations (the value was not inspected). Timing used synthetic factors at N=6 |

## 3. What is supported, and what is not

| Supported (with domain) | Not supported |
| --- | --- |
| T7/T8 (proved): the K3 floor of 2 internal witnesses per attachment; a constant class factor is orientation-neutral | That a native, covariant reference without that floor gathers |
| E3B (instrument): with the floor divided out of K3, σ > 0 path families gather while keeping their arrow | That the neutralised K3 law resembles any native scaffold's law |
| E1: the CSPH coexistence lost at N=7 with K3 | Anything about K2/P3 at any N |
| Square identity A = σ·Δdeg on intact squares (proved) | The sign of aggregate handovers under new scaffolds |

## 4. Possibilities in play (from GT-P007 §2; no outcome required)

- **P1, triangle-specific inhibition:** K2 and perhaps P3 gather for σ > 0 path families.
- **P2, source size and combinatorics:** differences track k, M, r0 and the number of probes, not witness topology. K2 against K3 confounds k; P3 against K3 does not.
- **P3, topology beyond the floor:** state-dependent witnesses (P3's chord) and kinetic competition matter.
- **P4, clock or density artefact:** gathering appears only in one clock, at sparse densities, or in rare conditionals. Overlap diagnostics and rare flags guard against this.
- **P5, structure-sensitive dynamics:** handover orientation or magnitude changes with scaffold.
- **P6, no general gathering:** native scaffolds stay non-gathering.
- **P7, something unexpected.**

Alternatives to the E3B explanation that E4A can expose:
- **Source size:** K2 has a lower r0 and more probes.
- **The chord:** P3 can become triangle-like by forming its chord.
- **Density:** different free-slot counts change the occupied density.
- **Frame:** source-orbit measures normalise per eligible slot.

## 5. Selection

**Matrix.** 3 scaffolds (K2, P3, K3) × N ∈ {5, 6} × 6 families: NULL, PATHF weak_suppress, PATHH weak_favour, CSPH strong_favour+weak_favour, PCOMP weak_favour+weak_favour, CLOSEW weak_favour. That is 36 cells, of which 12 are K3 replications and 24 are new.

It meets every condition in GT-P007 §4.1:
- formation- and dissolution-acting σ > 0 path families;
- a NULL per scaffold and size;
- σ = 0 (PCOMP) and reversible gradient (CLOSEW) comparators;
- P3 against K3 at equal source count;
- K2 without the floor;
- two sizes.

**Not included (E4B candidates only):** other scaffolds (a star, a held 4-path, larger sources), opposite-σ families, N=7.

## 6. Cost ceiling

- **Measured on synthetic-factor fixtures** (CSPH-like rule with non-alphabet factors) at N=6, full pipeline including checks:
  - K2 (16,384 states): 4.5 s at 170 MB;
  - P3 (8,192 states): 2.4 s.
- **Frozen limits:** 4 workers, a watchdog of 900 s at N=5 and 1,800 s at N=6, a round wall cap of 3 h, and a memory ceiling of 2.5 GB per worker.
- **Numerics:** the dense GTH referee is used up to 4,096 states, with a third-start referee above (K2/P3 at N=6), as in E1.

## 7. Cross-programme relevance

The source-as-witness bias is a methodological point for any laboratory contrast that holds or conditions on a source class (E3 transfer note T-4). E4A results would sharpen it. Any note goes to `docs/e4-cross-programme-transfer.md`, as suggestions only.
