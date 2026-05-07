# Claude Review Prompt: Relational Substrate Progress and Drift Audit

You are reviewing the current progress of the Relational Substrate research sandbox.

Your task is not to endorse the theory. Your task is to audit whether the work has remained aligned with its stated intent, whether the confidence language is calibrated, whether the evidence is being counted honestly, and what the next validation step should be.

Apply a skeptical but constructive standard. Penalize proof-framing, overclaiming, self-referential validation, hidden tuning, weak comparators, excessive confidence from qualitative wins, and benchmark proliferation that does not increase independent evidence. Credit explicit non-claims, ontology boundaries, source anchoring, held-out checks, quantified limitations, and restraint.

## Project Intent

The Relational Substrate sandbox tests whether a small unified grammar of route, closure, phase, charge, and continuity can reproduce, with reasonable equivalence, outputs and orderings that established domain models already produce, while providing one ontological framework across phenomena those models usually treat separately.

The point is not to prove an invisible substrate exists. The point is not to replace quantum chemistry, molecular dynamics, electromagnetism, optics, glass science, or any domain solver.

The standard is equivalence-with-unification:

- Can one grammar generate equivalent qualitative or quantitative outcomes across independent domains?
- Does that convergence justify stricter validation?
- Is the unification thesis becoming more evidentially grounded without being overstated?

The confidence metric is inferential convergence confidence, not proof-of-substrate confidence.

## Ontology Boundary

Use this T0/T1/T2 separation as a hard review standard:

- T0: proposed substrate level. It is not directly simulated or observed in this sandbox.
- T1: intermediate topology/coupling grammar level. Vorton language belongs here as a possible route from substrate to observable regimes.
- T2: secondary observable regimes such as molecules, lattices, materials, optical boundaries, and electromagnetic field behavior. These are pressure tests, not substrate objects.

The sandbox must not:

- Treat molecules, atoms, lattices, surfaces, field vectors, or rendered curves as substrate objects.
- Claim derivation of atoms or molecules from vortons.
- Insert a material middle layer between T0 substrate and T1 vortons.
- Treat passing T2 benchmarks as direct proof of T0.

## Current Repository State

Repository:

`https://github.com/gellsmore-svg/Relational-Substrate`

Local review artifacts:

- `docs/sandbox-closure-summary.md`
- `docs/external-ai-review-prompt.md`
- `docs/claude-progress-review-prompt.md`

Sandbox closure tag:

`sandbox-closure-v0.1`

Recent progression:

- `bce88d4 Rename sandbox to Relational Substrate`
- `466d9ec Add EM superposition comparator`
- `fd96b31 Add EM three-source comparator`

CI status at last update:

- Build passed.
- Full report regeneration passed.
- GitHub Actions passed.

## Current Reported Metrics

These are the project's current self-reported metrics. Do not assume they are correct; audit whether the evidence supports them.

| Metric | Current value |
|---|---:|
| Sandbox completion | 99.2% |
| Benchmark entries | 13/13 passing |
| Checks | 52/52 passing |
| Independent evidence lines | 7 |
| Grammar internal coherence | 7.5/10 |
| Inferential convergence confidence | 5.9/10 |
| Cross-domain equivalence demonstrated | 5.5/10 |
| Unification thesis support | 4.7/10 |

The current milestone summary deliberately keeps inferential convergence below 6/10 despite the recent EM passes, because the EM checks are still finite static vector comparators and do not yet include continuous field-line topology, equipotential geometry, calibrated magnitudes, or Maxwell-equation dynamics.

## Benchmark Inventory

| Benchmark | Evidence line | Domain | Status | Checks | Limitation |
|---|---|---|---|---:|---|
| H2O2 torsion profile | H2O2 molecular torsion | molecular conformational ordering | qualitative pass | 3/3 | cis/trans barrier ratio directionally right but compressed |
| H2O2 quantitative torsion angle | H2O2 molecular torsion | molecular conformational ordering | quantitative angle pass | 3/3 | angle passes; barrier contrast still compressed |
| Ethane torsion profile | ethane molecular torsion | molecular conformational ordering | qualitative pass | 4/4 | normalized score is not an energy model |
| Ethane quantitative torsion tolerance | ethane molecular torsion | molecular conformational ordering | quantitative tolerance pass | 3/3 | endpoint is scale-anchored and intermediate points are high |
| Ionic lattice order | ionic lattice ordering | ionic solid structure | qualitative pass | 3/3 | not full 6:6 coordination or lattice energy |
| Boundary phase prediction | optical/interface boundary ordering | optical/electromagnetic boundary behavior | documented blind-style qualitative pass | 3/3 | not independently timestamped; not an optics simulator |
| Electromagnetic ordering | electromagnetic field ordering | qualitative EM behavior | qualitative EM ordering pass | 4/4 | not Maxwell, Coulomb calculation, or derivation of c |
| EM-02 Coulomb comparator | electromagnetic field ordering | static-charge equation comparator | equation-level Coulomb ordering pass | 5/5 | relative comparator only; no absolute force model |
| EM-03 superposition comparator | electromagnetic field ordering | static two-source field geometry | held-out superposition comparator pass | 5/5 | finite two-source vector comparator |
| EM-04 three-source comparator | electromagnetic field ordering | asymmetric static field geometry | non-symmetric three-source comparator pass | 6/6 | finite asymmetric vector fixture; not field-line/potential/Maxwell |
| Silicate held-out network order | silicate network topology | network solid/material structure | held-out qualitative pass | 5/5 | graph-level order, not glass-property prediction |
| Roughness held-out interface order | optical/interface boundary ordering | rough optical/material interface behavior | held-out interface pass | 5/5 | qualitative roughness ordering, not scatter calibration |
| Material NBO/T quantitative accounting | aluminosilicate NBO/T accounting | glass composition accounting | quantitative material pass | 3/3 | composition accounting, not measured property prediction |

Important breadth caveat:

The project has 13 benchmark entries, but only about 7 independent evidence lines. H2O2 and ethane each have qualitative and quantitative sub-checks; they should not be counted as separate domains.

## Known Weaknesses and Drift Risks

Audit these carefully.

### 1. H2O2 Compression

The H2O2 cis/trans barrier-ratio discrepancy is quantified:

| Measure | Value |
|---|---:|
| Model cis/trans ratio | 3.3273 |
| External cis/trans ratio | 6.621 |
| Compression factor | 1.9899 |
| Ratio shortfall | 49.75% |

This is currently accepted as a bounded limitation. It is not resolved. It should remain one of the strongest reasons not to overstate confidence.

Review question:

Is this limitation stated strongly enough, or does the current document make the H2O2 result sound cleaner than it is?

### 2. Boundary Benchmark Status

The boundary benchmark is documented in-script and reproducible, but it was not independently timestamped before the diagnostic cases existed.

Review question:

Is it fair to retain it as a documented qualitative pass with reduced inferential weight, or should it be downgraded further?

### 3. EM Benchmark Proliferation

The EM sequence now includes:

- EM-01: qualitative charge/magnetic/EM-wave ordering.
- EM-02: pairwise Coulomb direction and inverse-square/product ratios.
- EM-03: symmetric two-source electric-field superposition geometry.
- EM-04: non-symmetric three-source electric-field vector fixture.

This is meaningful domain broadening, but EM-03 and EM-04 are still finite static vector comparators built from the same superposition law. They improve depth within EM, but they may not add a fully independent evidence line.

Review questions:

- Are EM-03 and EM-04 real progress or mostly implementation of standard vector arithmetic?
- Is it honest to raise inferential convergence from 5.5 to 5.9 on this basis?
- Should inferential convergence remain below 6/10 until continuous field-line topology, equipotential geometry, calibrated magnitude, or time-dependent propagation is tested?

### 4. Confidence Ceiling

Current confidence is intentionally capped below 6/10:

- Many checks are qualitative.
- Several quantitative checks are narrow.
- EM checks are static finite fixtures.
- H2O2 absolute barrier scale is not solved.
- Material checks do not predict measured viscosity, durability, conductivity, or density.
- Interface checks do not predict calibrated scatter curves.

Review question:

Is 5.9/10 too high, too low, or appropriate under an inferential-convergence framing?

### 5. Equivalence vs Displacement

The project should not require proving conventional models wrong. The correct standard is coherent equivalence across domains under one grammar, not displacement.

Review question:

Does the current documentation state equivalence-with-unification clearly enough, or does it still drift into either proof-framing or replacement-framing?

## Current Non-Claims

Check whether these are preserved consistently:

- This is not proof of the Relational Substrate theory.
- This is not direct simulation or observation of T0 substrate.
- This is not derivation of atoms or molecules from T1 vortons.
- This is not quantum chemistry, molecular dynamics, glass-property, BRDF, Fresnel, rough-surface scattering, Coulomb-force, field-line, potential, or Maxwell-equation solving.
- Passing order checks does not exclude conventional explanations.
- Mathematical equivalence is the floor before broader philosophical implications become defensible, not a shortcut to those implications.

## Specific Review Tasks

Please produce a structured review with these sections.

### 1. Executive Verdict

Choose one:

- Ready to proceed.
- Ready to proceed with revisions.
- Not ready to proceed.

Explain in 3-6 concise paragraphs.

### 2. Drift Audit

Audit whether the project has drifted in any of these directions:

- Proof of substrate existence.
- Replacement of established models.
- Overcounting benchmarks as independent evidence.
- Treating T2 objects as substrate objects.
- Raising confidence from implementation success rather than external evidence.
- Treating finite vector arithmetic as stronger EM validation than it is.

### 3. Evidence Audit

Identify:

- Strongest evidence line.
- Weakest evidence line.
- Most over-weighted benchmark.
- Most under-weighted benchmark.
- Any benchmark that should be downgraded or reframed.

### 4. Confidence Calibration

Give your own scores:

| Dimension | Your score |
|---|---:|
| Grammar internal coherence | ?/10 |
| Cross-domain equivalence demonstrated | ?/10 |
| Independence of evidence lines | ?/10 |
| Unification thesis support | ?/10 |
| Inferential convergence overall | ?/10 |

Briefly justify each score. If you think 5.9/10 is wrong, say what number should replace it and why.

### 5. EM Sequence Audit

Evaluate EM-01 through EM-04.

Questions to answer:

- Does EM-04 genuinely improve over EM-03?
- Does the EM sequence now justify calling electromagnetic behavior a substantiated domain in the unification map?
- What is the next EM test that would actually add inferential weight?
- Should the next EM test be continuous field-line topology, equipotential geometry, calibrated magnitude, or time-dependent propagation?

### 6. H2O2 and Chemistry Audit

Evaluate whether the H2O2 compression issue should now become the priority.

Questions to answer:

- Is H2O2 absolute torsional barrier calibration a better next target than more EM work?
- Does the current barrier-ratio compression suggest a grammar limitation or just a calibration limitation?
- What would count as a strong pass?
- What would count as a real failure?

### 7. Recommended Next Step

Choose exactly one next target:

1. EM-05 continuous electric-field-line topology comparator.
2. EM-05 equipotential-geometry comparator.
3. EM-05 calibrated field-magnitude comparator.
4. H2O2 absolute torsional barrier calibration.
5. Material measured-property correlation downstream of NBO/T.
6. Roughness calibrated scatter quantity.
7. Something else, but only if you can justify why it better tests the unification thesis.

Your recommendation should include:

- Why this target is the best next gate.
- What would be required to pass.
- What would be required to fail.
- Whether passing it should move inferential convergence above 6/10.

### 8. Required Revisions Before Proceeding

List any documentation, benchmark, confidence, or ontology revisions that should be made before the next implementation step.

If no revisions are required, say so explicitly.

## Suggested Reviewer Stance

Be skeptical of the theory, but fair to the sandbox.

The right question is not "is the Relational Substrate theory true?" The right question is:

> Does this work now contain enough externally anchored, non-circular, cross-domain equivalence to justify the next stricter validation target without inflating its claim?

Answer that question directly.
