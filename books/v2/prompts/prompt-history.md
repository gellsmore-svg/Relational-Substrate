# Prompt and process history

## 2026-10-03: initiating instruction

The full instruction is in [`rewrite-master-prompt.md`](rewrite-master-prompt.md), copied verbatim from the session. It asked for:

- a fundamental rewrite of CBO from the current research state;
- a reusable readability skill;
- a concept graph and human-context-load analysis;
- vector-scored architecture selection;
- an epistemic register;
- covers;
- a validated EPUB 2;
- full provenance.

No further instructions were given during the work. It was carried out in one autonomous session, in these stages, each committed separately on branch `book/coherent-biblical-ontology-v2`:

1. **Research baseline.** All branches, the GitHub organisation, the local workspace and the archived ChatGPT export were searched.
   - The stochastic calculator (branch `research/stochastic-calculator`, PR #2) and the constraint laboratory (branch `research/constraint-lab-v0.1`) were found to carry the September–October work.
   - Several programmes named in the brief (the 502-series, a relational stochastic ring, Navier–Stokes, spectral/Grassmannian work) were not found in any record. They were treated as unverified (`research-baseline.md`, D-3 and D-5).
   - The in-progress, uncommitted constraint-lab v0.2 working tree was left untouched and is not cited.
2. **Readability skill.** Literature citations were verified by web search before use. The skill was applied to the first edition first.
3. **Concept graph and architecture.** Five candidates were scored, and the selected one was revised once (D → D′) and red-teamed.
4. **Drafting.** Chapter by chapter, with factual corrections made during drafting:
   - molecule count in a tyre;
   - the subject of Einstein's 1905 paper;
   - the origin of nucleon mass;
   - the constraint-laboratory occupation statement;
   - the SC-024 reliability figure;
   - the status of the false-attractor observations.
5. **Review.** Metrics, voice pass, acceptance tests (added attractor and mathematical-determinism definitions; powers-ontology concession; quantum-interpretation flag), final vector review.
6. **Build.** Covers (seeded SVG), EPUB 2 build integrated into `scripts/build-epubs.sh`, epubcheck validation.

The brief's formulations that the research revised are recorded with reasons in `../analysis/research-baseline.md` §3.

## 2026-10-03: v2.1 follow-up review and correction

- **Instruction:** [`v2.1-follow-up-review-prompt.md`](v2.1-follow-up-review-prompt.md), verbatim.
- **Branch:** `book/coherent-biblical-ontology-v2`. Starting commit `11495e0`. Draft PR #3.
- **Purpose:** an independent review compared the v2 manuscript with a larger conversational research corpus not in GitHub, and found the v2 reconstruction good but incomplete. v2.1 is a correction and completion pass, not a rewrite.
- **Major corrections:**
  - T-C-R decoupled from the calculator carry protocol (Ch 7).
  - Identity as relational equivalence with provenance and future discriminability (Ch 6).
  - Joint-process coordination and mean versus fluctuation stability (Ch 8).
  - Global coherence beyond non-contradiction (Chs 2, 9).
  - Ch 9 argued against serious alternatives.
  - Constraint Lab v0.2 integrated: Generations 1b and 2, including the correction of v2's cancellation claim (Ch 4, App B).
  - Calibration of LLN, Bell, collapse theories, mass and fields.
  - Freedom, death and higher-alignment language made theologically neutral and calibrated.
  - T2 retired.
  - New identity figure.
- **Provenance handling:** conclusions supplied from conversational research are recorded in `../analysis/conversational-research-import-v1.md`. In the manuscript they are labelled as exploratory and never cited as experiments.
- **Divergences from the instruction:** none of substance. Nuances are recorded in the research baseline §7 (Generation 2's pairwise count cancellations; the roadmap candidates are not commitments).
- **Resulting commits:** `cf5a49d`, `150f69a`, `fc0da70`, and the final v2.1 commit that records this entry.

## 2026-10-03: v2.2 follow-up refinement

- **Instruction:** [`v2.2-follow-up-review-prompt.md`](v2.2-follow-up-review-prompt.md), verbatim.
- **Starting head:** `62eca7d`. Constraint Lab refs verified: v0.2 `0170189` unchanged. A new branch, v0.3 (`e04e0d4`, Generation 3), had appeared and was integrated.
- **Purpose:** refinement of Chapter 8 (aggregation versus coordination; dependence as an ontological, not mathematical, claim); negative and conditional 502 results; the endogenous carrier/lineage problem recorded as open; removal of stale baseline contradictions.
- **Files changed:**
  - manuscript: Chs 6, 7, 8 and Apps B, D;
  - analysis: research-baseline (restructured), conversational-research-import-v2 (new; v1 marked superseded), epistemic register, HCL map, concept-graph builder, chapter map, v2.2 review record, final reviews;
  - READMEs.
- **Divergence:** the instruction treated triadic relation and history as untested candidates. The repository had run Generation 3 (triadic), so its results are reported. Recorded in the baseline III.3.
- **Resulting commits:** `cbbe8c0` and the v2.2 audit commit that records this entry.

## 2026-10-03: v2.3 final surgical pass

- **Instruction:** [`v2.3-final-surgical-review-prompt.md`](v2.3-final-surgical-review-prompt.md), verbatim. **Starting head:** `f658254`. No ref movement.
- **Purpose:** eight residual issues (identity versus individual continuity; neutral stochasticity; Ch 4 structure; corruption; Genesis inference; Ch 9 target; interactional versus constitutive relation; unreceived transmission) and an optional Ch 8 midpoint reset.
- **Files:** manuscript Chs 1, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15 and Apps B, C; analysis (epistemic and terminology registers, research baseline, concept-graph builder and chapter map, v2.3 review record, final vector review); this history.
- **Divergences:** none.
- **Resulting commit:** the v2.3 commit that records this entry.

## 2026-10-03: v2.3.1 final cleanup

- **Instruction:** [`v2.3.1-final-cleanup-prompt.md`](v2.3.1-final-cleanup-prompt.md), verbatim. **Starting head:** `f5aef30`.
- **Purpose:** propagation of the v2.3 identity distinction; metadata cleanup.
- **Changes:** Chs 0 (preface), 5, 10, 11, 14, 15 and App B; research-baseline status and identity lines; concept-graph `equivalence` label. Details in `../analysis/v2.3.1-cleanup-record.md`.
- **Divergences:** none.
