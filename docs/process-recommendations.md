# Process and Tooling Recommendations

**Date**: 2026-06-13  
**Source**: Detailed review of the research program, model, RI chain, tooling, and documentation.  
**Status**: Adopted as process expectations for new work (especially model forms and material-property validation).

These recommendations strengthen the project's existing emphasis on predeclaration, held-out validation, conventional comparators, provenance, and epistemic discipline. They do not relax any guardrails around claims or ontology boundaries.

## 1. Formal Predeclaration of Model Forms and Descriptors

**Recommendation**: Before scoring *any* new target (RI or otherwise), explicitly predeclare the allowed descriptor set and extraction rules.

- Use or extend `analysis/descriptor-registry.json` (started).
- The declaration should live in the script or a companion note for that diagnostic/chain step.
- Make predeclaration a hard gate in chain runners and reports.

**Why**: The RI work correctly moved from scalar composition terms to topology/packing/structural descriptors. Formalizing the declaration prevents post-hoc fitting and makes the "new model form" step auditable.

**Related files**: `analysis/descriptor-registry.json`, `analysis/ri-structural-descriptor-validation.mjs`, `analysis/ri-topology-volume-descriptor-diagnostic.mjs`.

## 2. Strengthen Conventional Baselines in Reports

**Recommendation**: Every material or optical report must include a clean, non-endpoint-fitted conventional predictor (e.g. fixed density + Lorentz-Lorenz style) reported side-by-side with any grammar-inspired terms.

- Show the delta (if any) on *held-out* rows only.
- Always label density, Lorentz-Lorenz, and similar terms as "conventional control evidence".
- Never count improvements on the conventional baseline as direct support for the substrate grammar.

**Why**: The RI chain already uses baseline comparisons. Making them explicit, non-fitted, and consistently reported increases the credibility of any claimed advantage.

## 3. Descriptor Registry and Provenance

**Recommendation**: Maintain a small machine-readable registry of descriptors.

Current starter (`analysis/descriptor-registry.json`) includes:
- id, name, units, extraction method, source requirement
- `conventional: true/false` flag
- High-level rules for predeclaration and conventional labelling

**Additional practices**:
- Lock primary source triples (CIF + measured refractive index + measured density) with clear provenance before any prediction is scored.
- Avoid broad/secondary aggregate sources (e.g. pooled WebMineral rows) for held-out targets.

## 4. Core Model Expressiveness vs. Transparency

**Recommendation**: If the `calculateOutcome` logic in `src/model.js` is extended (e.g., an explicit "constraint storage" accumulator or phase-continuity term derived from geometry), keep the implementation fully declarative and auditable.

- Prefer adding traceable intermediate values over burying logic in bias tables.
- The current model is a strength because it is simple and inspectable; any growth should preserve that property.

## 5. Statistical Characterization of the Toy Model

**Recommendation**: Complement existing molecule perturbation and coordinate sweeps with:

- Sensitivity analysis on the `identityPreserved` threshold (currently 0.62) and closureStress cutoff.
- Robustness checks on the bias tables and metric weighting.
- Threshold stability across scenario and form combinations.

This provides a better understanding of how "coherent" regions in the sandbox depend on modelling choices.

## 6. Tooling and Hygiene Improvements

- **Guardrails script**: `npm run guardrails` (implemented in `scripts/guardrails.mjs`). Runs syntax checks on key analysis files and basic validation of the descriptor registry. Run before reports or PRs when touching analysis code.
- **Generated file conventions**: Generated content under `analysis/out/` remains disposable. Only deliberately curated artifacts should be copied into `docs/` with explanation.
- **Data provenance**: Future improvement — introduce a `calibration/` or `data/` area with locked, versioned source rows (CIF + optical + density) and hashes or commit references.
- **Registry maintenance**: Keep `analysis/descriptor-registry.json` versioned. New descriptors require an entry (or PR to the registry) before use in scored work.

## 7. Cross-Track Evidence Accounting

**Recommendation**: Improve the auditability of the high-level metrics in `docs/research-task-map.md` (evidence lines, independence, cross-domain equivalence, unification support).

A lightweight, machine-readable or consistently formatted ledger across all tracks (molecule, material, EM, interface, torsion, etc.) would make the confidence numbers (currently 5.6/10 inferential convergence, below the 6.25 cap) easier to defend or challenge during reviews.

## 8. UI ↔ Analysis Round-Tripping

**Recommendation**: Add the ability in the browser sandbox to export the exact set of slider values + form/scenario choices as JSON that can be fed directly into analysis scripts or the chain runner.

This closes the loop between visual exploration and reproducible batch cases.

## Integration Notes

- See `CONTRIBUTING.md` for updated "Expected Changes" and the new "Process Improvements" section.
- See `.restart.md` for the same list in the project restart state (user may need to merge the section if `.restart.md` had root ownership at the time of this edit).
- New work that touches model forms, descriptors, or material validation should reference this document.

These changes are deliberately incremental and align with the project's long-standing preference for held-out checks, source locking, and quantified limitations.
