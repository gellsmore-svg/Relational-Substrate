# E5 coverage and definition audit (GT-P009)

*Written 2026-10-15, **before** any E5 computation. Deliverable 1 of GT-P009.*
- *No E5A motif lifetime, turnover, matched-density comparator or lagged-hub value for any N=5 or N=6 cell had been computed when this file was committed.*
- *The definitions note is `docs/e5-definitions-and-null-construction.md`.*

## 1. Starting state (verified, not assumed)

| Item | Value |
| --- | --- |
| Branch | `research/gravity-time-admissibility`; local = remote = `a73cd0260f38885121a89a607efa73e98732e59f` (the expected GT-P008 head); worktree clean |
| PR #6 | open, **draft**; base `research/constraint-lab-v0.8g-formal-integration` (head `22e252e`), head `a73cd02` |
| CI on `a73cd02` | success: push run 38696273921, pull_request run 38696281378 |
| `main` | `05b15b0d903d46070b99ac84f9cab1bd898046ba` |
| OTR | `research-methods/open-thetical-research.md` sha256 `2d9023955ddfaf269131033589c547cea7090c72caf2577ab28f7138dfb388dd` on the GT branch **and** on `main` (identical) |
| Prompt | `provenance/prompts/GT-P009-agent-input.md`, an agent transcription (35,221 bytes, sha256 `058c120d…456c`), committed in `2bd18c6` before any analysis; no byte identity with an external file is claimed |
| Concurrent work | none: the branch had not moved since GT-P008, and no E5 plan, table or report exists |
| Interpreter | Python 3.12.3, numpy 2.5.3; **scipy is not installed** (consequence: §5, D-9) |
| Test baseline | `constraint-lab` full suite: **796 passed** (163 s) on `a73cd02` |
| Reference payloads | E0B tables payload `f02c7c95…cb80`, frozen plan `50c4b2c` |

## 2. Prior boundaries (checked against the records)

1. **GT-P008 added no E5 data.** Its execution record (`provenance/execution-GT-P008.md`) states that no E5 round was opened, frozen or executed and no scientific cell was computed. Confirmed.
2. **Its witness-floor odds factorisation (S1–S2) and first-order index (S4b) are theorems about the finite grammar.** They say nothing about FREE motif persistence. They enter E5 only as context.
3. **The 16/16 agreement of the first-order index with E4 orderings is post hoc** (GT-F71). It is not E5 evidence.
4. **Reference regimes are distinct.** GT-P008 (`docs/reference-architecture-review.md`) separates held, instantaneously selected, metastable and identity-tracked reference regimes. It established no emergent persistent reference. Its R1–R3 show that at finite N, in a label-covariant irreducible chain, no labelled structure persists indefinitely. So E5 can at most measure *metastable* longevity relative to comparators.
5. **E4's raw gathering was mostly density composition.** Its positive raw gathering largely disappeared under null-density standardisation (GT-F64/F71). The same caution applies here: a long-lived motif in a dense law may only reflect density, which is why the ND comparator exists.

## 3. Exposure: what is already published about the 12 E5A kernels

**All 12 E5A kernels (6 family-grades × N = 5, 6) are published FREE cells.** E5A recomputes their kernels and stationary laws. It **does not** independently replicate them, and the recomputed laws are labelled replications.

| Family-grade (exact spelling) | Components | Published FREE cells at N=5, 6 (cell ID as in the tables) |
| --- | --- | --- |
| NULL `none` | — | G0, E0A, E0B: `FREE-N5-NULL-none`, `FREE-N6-NULL-none`; E2A N=5; E3A `FREE-N5-W4-NULL-none` |
| PATHF `weak_suppress` | `path_form weak_suppress` | E0A, E0B: `FREE-N{5,6}-PATHF-weak_suppress`; E2A N=5 |
| PATHH `weak_favour` | `path_dissolve weak_favour` | E0A, E0B: `FREE-N{5,6}-PATHH-weak_favour`; E2A N=5 |
| CSPH `strong_favour+weak_favour` | `close_form strong_favour`, `path_dissolve weak_favour` | E0B: `FREE-N{5,6}-CSPH-strong_favour+weak_favour` |
| CLOSEW `weak_favour` | `close_form weak_favour` | E0B: `FREE-N{5,6}-CLOSEW-weak_favour`; E2A N=5. The same rule is G0's `FREE-N{5,6}-CLOSE-weak_favour` |
| PCOMP `weak_favour+weak_favour` | `path_form weak_favour`, `path_dissolve weak_favour` | E0B: `FREE-N{5,6}-PCOMP-weak_favour+weak_favour` |

The spellings and components were checked against `gte0b.FAMILIES` (`constraint-lab/src/rs_constraint_lab/gte0b.py:38–45`). They are identical to the E4 family-grades (`gte4a.FAMILY_GRADES`). The factors are W4 (weak = 2^±1, strong = 2^±2).

**Published channels for these cells** (`reports/round-e0b-tables.json` and the others named above):

| Channel | Where | Relevance to E5 |
| --- | --- | --- |
| Full stationary law by isomorphism class, in CT and JT (`class_table`), and `mean_rate_ct` | E0B, all 12 | **Every E5 prevalence π(A), ν(A) and the CT density profile p_k is a deterministic function of these published tables.** The ND comparator's inputs (p_k and E_π[q]) are therefore pre-exposed (see below) |
| Integrated autocorrelation times (per unit time and per event) of edge count, triangle count, degree of vertex 0, and the indicator that vertex 0 is a full centre (degree N−1); `localisation_persistence_index` | E0B N=5 (all six); E0A N=5 | Persistence-*like*, but they are second-moment correlation times, not entrance-episode lifetimes. No episode, flux or turnover quantity was computed |
| Autocorrelation of a hub indicator; max-degree and tied-hub distributions (`hub_structure_ct`) | E2A N=5: NULL, PATHF, PATHH, CLOSEW | Instantaneous hub statistics (selection), not lagged follow-up of a once-selected vertex |
| `hub_frame` (event order and projected current on (edge count, max degree)) | E0B, all 12 | Hub-frame **projections at one time**. No lag channel |
| Partner frame, square affinities, irreversibility (σ), event order | E0A/E0B/E2A | Circulation context for path families |

**Channels never computed for any of these kernels:**
- entrance-episode boundary flux, lifetimes and recurrence for any motif;
- within-episode turnover Ω;
- edge present-episode lifetime;
- the ND process;
- lagged follow-up of a selected hub at a positive lag;
- neighbour-set retention;
- residual (occupation-sampled) lifetimes.

**Derived pre-exposure (stated explicitly).**
- The ND construction (prompt §2.5) is a fixed algorithm with no free choice. It is applied to inputs (p_k and E_π[q]) that can be derived from published tables.
- No one, including this agent, can tune ND after seeing its inputs: the algorithm and its scale were specified by the authorising prompt.
- Motif prevalences can likewise be derived from published class tables. E5A reports them as **re-expressions of published laws**, not as new evidence.

**What the agent saw during this audit.** To identify channels, the agent displayed published values for one cell, `FREE-N5-PATHF-weak_suppress`:
- its E0B `hub_frame` block and autocorrelation times;
- its E2A `hub_structure_ct`, `autocorrelation_extra` and partner-frame values;
- the first two class-table rows of `FREE-N6-CSPH`.

All were already-published values. None is an E5 quantity.

## 4. Allowed pre-freeze computations

| Use | Fixture | Status |
| --- | --- | --- |
| Episode-flux, Ω, edge-lifetime and residual-life identities | Two-state and small synthetic CTMCs, solved analytically or densely | Proof verification |
| NULL closed forms (independent unit-rate bits) | N=4 FREE NULL (not an E5 size), and the analytic formulas | Proof verification |
| ND construction | Synthetic, deliberately non-uniform p_k on N=4 | Proof verification |
| Family kernels | N=4 FREE kernels of the six family-grades (N=4 was used as a fixture size in E0A to E4; it is not an E5A size) | Engineering, PCOMP-uniformity and covariance checks |
| Stiff matrix exponential | N=4 kernels with synthetic factors (alphabet values not used in any round), and NULL N=6 with all rates multiplied by 2^24 (a synthetic chain whose values follow from the NULL closed forms by time rescaling) | Timing and accuracy only |

**Not allowed before freezing:** any E5A observable of any non-NULL family at N=5 or N=6. Its stationary law may be recomputed only inside the frozen run.

## 5. Definition decisions (refinements inside the authorised specification)

The prompt's §2 definitions are internally coherent. No decision changes the scientific question, so **there is no stop-before-freeze decision note.** The refinements below fix implementation details only.

- **D-1. Instances.**
  - Primary instances:
    - I_TRI(0,1,2);
    - I_STAR(0; 1,2,3);
    - I_2PATH(1,0,2), i.e. edges 01 and 02, middle vertex 0;
    - F_TRI(anchor {0,1});
    - F_STAR(0);
    - F_2PATH(0).
  - Every predicate is also computed on its image under the relabelling v ↦ N−1−v (the covariance check). Edge lifetime uses slot (0,1), with (N−2, N−1) as its relabelled check.
- **D-2. Clocks and starts.** CT quantities use the CT stationary law π. JT quantities use the jump-chain law ν = π q / E_π[q]. The lagged hub starts at x_0 ~ π for CT lags and x_0 ~ ν for JT lags.
- **D-3. JT episode length** is the number of jumps made from states in A per episode, including the exit jump, so L_JT = E_π[q 1_A]/J_A. Internal events per episode are then L_JT − 1 (an algebraic identity, checked).
- **D-4. Ω counts eligible toggles, not replacements.**
  - A witness that leaves and returns counts twice.
  - Whether an episode ever replaces *all* of its entry participants is an identity-tracking quantity. It is **not** defined in E5A.
  - Also reported: the eligible share Ω/(L_JT − 1).
- **D-5. F_TRI eligibility.** The toggled slot must be ac or bc for some c ∉ {a,b}, with the other leg (bc or ac) present, so that the toggle changes the completer set, and A must hold before and after. For F_STAR and F_2PATH, the toggled slot must be incident on c, with A holding before and after.
- **D-6. F_TRI exit causes** are split into anchor-edge dissolution and loss of the last completer. Intact-motif exits are always required-edge dissolutions; that is the structural theorem, and it is checked.
- **D-7. Comparison vertex** for the hub control is uniform over all N vertices, the selected one included. By stationarity its expected degree is then constant in the lag. The hub tie rule is uniform over the arg-max set (S_N-covariant).
- **D-8. ND rare bins.**
  - Flag every k with p_k < 10^−12 (the E4 rare threshold) and report its mass.
  - Report the conditioning: the range of log φ_k.
  - If any p_k = 0, the comparator is reported as unresolved for that cell. Nothing is smoothed.
- **D-9. Exact CT lags without scipy.**
  - path_dissolve weak_favour gives dissolution rates up to 2^24 on dense graphs at N=6. This is a structural property of the rule: 24 path witnesses on K6. Uniformisation would need about 10^7 steps.
  - CT lags are therefore computed exactly on the chain **lumped by the permutations fixing vertices 0 and 1**. Every covariant chain is strongly lumpable under them, which is checked.
  - The lumped chain has 240 states at N=5 and 1,992 at N=6. The computation is a scaling-and-squaring Padé-13 matrix exponential, with:
    - row-sum, non-negativity and stationarity checks;
    - a lumped-versus-full jump-chain cross-check;
    - a uniformisation cross-check where uniformisation is cheap (N0 and ND).
  - JT lags are exact full-space propagation.
- **D-10. Residual (occupation-sampled) lifetimes** are a secondary channel. They solve the killed jump chain on A by BiCGSTAB with a declared cap. The same solve yields an independent first-passage check of L = π(A)/J_A from the entrance distribution. If unresolved, they are recorded as unresolved.
- **D-11. Discovery matrix.**
  - Classification uses the signs of log(L_target/L_ND), log(ρ_target/ρ_ND) and Ω_target − Ω_ND per clock, and the same against N0.
  - A sign counts as a "tie at frozen precision" when |relative difference| < 10^−9.
  - No magnitude threshold is used anywhere.

## 6. Risks recorded before freezing

1. **Predicate breadth.** The F_* predicates are non-induced and broad. F_2PATH(0) can be nearly always true in dense laws, giving long but uninformative episodes. E5A reports prevalence beside lifetime for this reason.
2. **ND underdetermination.** ND is one reversible dynamics matching the CT density profile and the CT mean event rate. An effect relative to ND is a fact about that comparison only.
3. **ND is not JT density-matched.** JT comparisons against ND are kinetic diagnostics. The JT density discrepancy is reported.
4. **Pre-exposure.** Prevalences, density profiles and mean rates are functions of published tables (§3). Only flux-based, turnover and lag quantities are new.
5. **Stiffness.** Rates spanning about 10^7 could affect expm accuracy. This is mitigated by the D-9 checks; a failed check is recorded, not repaired.
6. **Killed-chain convergence** may fail for near-certain predicates. The channel is secondary and is recorded as unresolved if it does.
7. **Finite size.** N = 5, 6 only. Any trend is a finite-size observation, and no symmetry-breaking claim is possible (R3).
8. **Clock reading.** The model clocks are conventions, not physical time. A motif lifetime is not the duration of a body.

## 7. Cross-programme reading (read-only)

- `constraint-lab/formal/open-problems.md`:
  - CL-Q03 asks whether current-state dependence must be represented as extra state (the 8G compilation test);
  - CL-Q05 asks about fragility, passage and transition-enabling dissolution.
- E5A creates no history or meta state. Motif matching is done by a read-only analyser, so the 8G gate is not engaged.
- Any transfer is written as suggestions only (deliverable 10). No laboratory file or branch is changed.
