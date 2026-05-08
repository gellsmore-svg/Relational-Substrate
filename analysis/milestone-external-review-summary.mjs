import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

async function readOptionalJson(name) {
  try {
    return await readJson(name);
  } catch {
    return null;
  }
}

const summary = await readJson('external-benchmark-summary.json');
const assumptions = await readJson('model-assumptions.json');
const frontier = await readJson('model-frontier-report.json');

const benchmarkFiles = [
  'external-h2o2-benchmark.json',
  'external-h2o2-quantitative-benchmark.json',
  'external-h2o2-absolute-barrier-benchmark.json',
  'external-hydrazine-cation-torsion-benchmark.json',
  'external-ethane-benchmark.json',
  'external-ethane-quantitative-benchmark.json',
  'external-ionic-benchmark.json',
  'external-boundary-blind-benchmark.json',
  'external-em-ordering-benchmark.json',
  'external-em-coulomb-comparator.json',
  'external-em-superposition-comparator.json',
  'external-em-three-source-comparator.json',
  'external-em-field-line-topology-comparator.json',
  'external-em-equipotential-comparator.json',
  'external-em-field-magnitude-comparator.json',
  'external-em-dielectric-media-comparator.json',
  'external-em-wave-propagation-comparator.json',
  'external-silicate-heldout-benchmark.json',
  'external-roughness-heldout-benchmark.json',
  'external-material-nbo-quantitative-benchmark.json',
];

const benchmarkArtifacts = (await Promise.all(benchmarkFiles.map((file) => readOptionalJson(file)))).filter(Boolean);
const h2o2Quant = benchmarkArtifacts.find((artifact) => artifact.source === 'external-h2o2-quantitative-benchmark.mjs');
const h2o2Absolute = benchmarkArtifacts.find((artifact) => artifact.source === 'external-h2o2-absolute-barrier-benchmark.mjs');
const hydrazineCation = benchmarkArtifacts.find((artifact) => artifact.source === 'external-hydrazine-cation-torsion-benchmark.mjs');
const boundaryBenchmark = benchmarkArtifacts.find((artifact) => artifact.source === 'external-boundary-blind-benchmark.mjs');
const h2o2AbsolutePass = h2o2Absolute?.status === 'absolute barrier pass';
const hydrazineOrderingPass = hydrazineCation?.status === 'held-out torsion ordering pass with quantitative miss';
const hydrazineTransferPass = hydrazineCation?.status === 'held-out torsion transfer pass';

const intent = {
  primary:
    'The Relational Substrate sandbox is an external-review test bench for a proposed substrate/topology grammar. Its purpose is to test whether a small unified grammar of route, closure, phase, charge, and continuity variables can reproduce, with reasonable equivalence, outputs and orderings that established domain models already produce while providing one ontological framework across phenomena those models usually treat separately.',
  ontologyBoundary:
    'The sandbox does not simulate T0 directly. It does not treat atoms, molecules, lattices, surfaces, curves, rendered meshes, or graph nodes as substrate objects. Molecules and materials are T2 secondary regimes used as pressure tests for a possible T1 coupling grammar.',
  equivalenceStandard:
    'The standard is equivalence-with-unification, not displacement. The sandbox does not need to prove conventional models wrong or outperform them. It needs to show that the grammar can produce equivalent qualitative or quantitative outputs across enough independent domains that stricter validation of a unified generative foundation is justified.',
  inferenceStandard:
    'The inference target is not proof of an invisible substrate. The target is increasing independent, non-circular evidential convergence, analogous in structure to how unobservable theoretical entities gain standing through convergent explanatory and predictive success.',
  reviewQuestion:
    'The correct review question is not "has the Relational Substrate theory been proven?" The correct question is "does this sandbox now contain enough externally anchored, non-circular checks to justify the next stage of stricter quantitative and held-out validation?"',
};

const glossary = [
  {
    term: 'T0',
    definition:
      'Proposed substrate level. It is not directly simulated or observed in this sandbox.',
  },
  {
    term: 'T1',
    definition:
      'Intermediate topology/coupling grammar level. Vorton language belongs here as a possible route from substrate to observable regimes.',
  },
  {
    term: 'T2',
    definition:
      'Secondary observable regimes such as molecules, lattices, materials, optical boundaries, and interfaces. These are pressure tests, not substrate objects.',
  },
  {
    term: 'Vorton',
    definition:
      'A proposed T1 topological unit or coupling motif. The sandbox does not claim to derive atoms or molecules from vortons.',
  },
  {
    term: 'Route',
    definition:
      'The path or transition ordering by which a state is reached.',
  },
  {
    term: 'Closure',
    definition:
      'The degree to which a topology or transition forms a stable completed loop, lock, or constraint pattern.',
  },
  {
    term: 'Phase',
    definition:
      'Continuity, memory, and alignment of oscillatory or state-order information across a transition.',
  },
  {
    term: 'Charge',
    definition:
      'Signed or directional constraint imbalance used by the grammar; it is compared against electrical/ionic behavior only at the T2 pressure-test level.',
  },
  {
    term: 'Continuity',
    definition:
      'Persistence of ordering across boundaries or transformations.',
  },
];

const unificationMap = [
  {
    benchmarkFamily: 'Molecular torsion: H2O2 and ethane',
    conventionalDomain: 'molecular conformational chemistry',
    grammarVariables: 'route, closure, phase',
    currentReading:
      hydrazineTransferPass
        ? 'Shows torsion-order and transferred barrier equivalence after anti-planar release, with a held-out hydrazine cation transfer pass.'
        : hydrazineOrderingPass
        ? 'Shows torsion-order and H2O2 transferred barrier equivalence after anti-planar release. Hydrazine cation gives a held-out qualitative/ratiometric pass but misses absolute barrier magnitudes, so calibration remains limited.'
        : h2o2AbsolutePass
        ? 'Shows torsion-order and transferred barrier equivalence after anti-planar release. This reduces the prior H2O2 limitation, but the revision needs a fresh held-out torsion check to guard against overfitting.'
        : 'Shows torsion-order equivalence but remains limited by H2O2 barrier-ratio compression. The absolute transfer check localizes the issue: cis is near scale, trans is overpredicted, so the relative barrier floor remains the strongest current grammar limitation.',
  },
  {
    benchmarkFamily: 'Ionic lattice order',
    conventionalDomain: 'solid-state ionic structure',
    grammarVariables: 'charge, closure, continuity',
    currentReading: 'Shows qualitative ordering against standard ionic coordination expectations.',
  },
  {
    benchmarkFamily: 'Boundary phase and roughness/interface checks',
    conventionalDomain: 'optical/electromagnetic boundary behavior',
    grammarVariables: 'phase, continuity, route',
    currentReading: 'Roughness/interface ordering is a qualitative evidence line. The boundary phase prediction is orientation evidence only because it is documented but not independently timestamped.',
  },
  {
    benchmarkFamily: 'Electromagnetic ordering',
    conventionalDomain: 'charge, magnetic-field, and EM-wave behavior',
    grammarVariables: 'charge, phase, closure, continuity, route',
    currentReading:
      'Opens the EM domain with one electromagnetic evidence line containing Coulomb direction/ratio, two-source superposition geometry, asymmetric three-source field implementation checks, continuous field-line topology, scalar equipotential geometry, calibrated point-charge field magnitude, ideal conductor/dielectric media behavior, and plane-wave propagation relations. This still imports conventional constants and ideal constraints and is not a material-response derivation, radiation-generation model, or full electromagnetic solver.',
  },
  {
    benchmarkFamily: 'Network/material structure: silicate network and NBO/T accounting',
    conventionalDomain: 'network solids and glass chemistry',
    grammarVariables: 'closure, charge, continuity',
    currentReading: 'Shows held-out material ordering and exact composition accounting, but not measured property prediction.',
  },
];

const completion = {
  milestoneStatus: 'complete for external review',
  reason:
    'The milestone now has broad internal diagnostics, external benchmarks spanning multiple domains, held-out material/interface checks, and quantitative accounting/torsion checks. Remaining work is validation beyond the sandbox, not more same-layer exploratory extension.',
  sandboxCompletionPct: summary.confidence.updatedSandboxCompletionPct,
  benchmarkPasses: summary.benchmarkPasses,
  totalBenchmarks: summary.benchmarks.length,
  checksPassed: summary.passedChecks,
  totalChecks: summary.totalChecks,
};

const confidence = {
  internalCoherenceOutOf10: summary.confidence.updatedInternalCoherenceOutOf10,
  inferentialConvergenceOutOf10: summary.confidence.updatedInferentialConvergenceOutOf10,
  crossDomainEquivalenceOutOf10: summary.confidence.crossDomainEquivalenceOutOf10,
  evidenceIndependenceOutOf10: summary.confidence.evidenceIndependenceOutOf10,
  unificationThesisSupportOutOf10: summary.confidence.unificationThesisSupportOutOf10,
  reading:
    h2o2AbsolutePass
      ? 'Internal coherence is sufficient for external review but still below final-theory confidence because the H2O2 improvement came from a post-failure grammar refinement, boundary verification remains non-timestamped, benchmark breadth is compressed, hydrazine absolute magnitudes remain low, and EM propagation/media checks still import conventional constants and ideal constraints rather than deriving electrodynamics.'
      : 'Internal coherence is sufficient for external review but lower than the prior 8.5/10 closure draft because H2O2 compression, boundary-verification limits, benchmark-breadth compression, and qualitative EM topology limits remain known issues. Inferential convergence has crossed 6/10 only because EM now includes continuous field-line topology; it remains moderate because the topology check is not calibrated physical property prediction or Maxwell-equation dynamics.',
};

const nonClaims = [
  'This is not proof of the Relational Substrate theory.',
  'This is not a direct simulation or observation of T0 substrate.',
  'This is not a derivation of atoms or molecules from T1 vortons.',
  'This is not a quantum chemistry, molecular dynamics, glass-property, BRDF, Fresnel, rough-surface scattering, conductor, capacitance, Coulomb-constant derivation, or Maxwell-equation solver.',
  'This does not yet solve absolute H2O2 barrier structure, material viscosity/durability/conductivity/density, or calibrated scatter curves.',
  'Passing benchmark order checks does not by itself exclude conventional explanations.',
];

const reviewPackage = {
  source: 'milestone-external-review-summary.mjs',
  status: 'Relational Substrate sandbox milestone summary for external review',
  intent,
  completion,
  confidence,
  glossary,
  equivalenceStandard: intent.equivalenceStandard,
  inferenceStandard: intent.inferenceStandard,
  unificationMap,
  h2o2Compression: h2o2Quant?.metrics ?? null,
  h2o2AbsoluteTransfer: h2o2Absolute?.metrics ?? null,
  hydrazineCationTransfer: hydrazineCation?.metrics ?? null,
  boundaryVerification: boundaryBenchmark?.predictionManifest?.verificationStatus ?? null,
  independentEvidenceLines: summary.independentEvidenceLines,
  orientationEvidenceLines: summary.orientationEvidenceLines,
  externalStatus: {
    status: summary.status,
    externalCompletionPct: summary.externalCompletionPct,
    remainingGates: summary.remainingExternalGates,
  },
  benchmarks: summary.benchmarks,
  nextFrontier: frontier.nextTarget,
  nonClaims,
  reviewerQuestions: [
    'Are the ontology boundaries clear enough to prevent overclaiming?',
    'Are the external benchmarks independent enough to reduce circularity?',
    'Which benchmark is most vulnerable to hidden tuning or overly permissive tolerances?',
    'What quantitative target should be required before inferential convergence can responsibly rise above 6/10?',
    'Which conventional model should be used as the strongest comparator in the next validation round?',
  ],
};

await writeFile(new URL('milestone-external-review-summary.json', outDir), JSON.stringify(reviewPackage, null, 2));

const benchmarkRows = summary.benchmarks
  .map(
    (benchmark) =>
      `| ${benchmark.label} | ${benchmark.evidenceLine ?? 'n/a'} | ${benchmark.domain ?? 'n/a'} | ${benchmark.conventionalComparator ?? 'n/a'} | ${benchmark.status} | ${benchmark.checksPassed}/${benchmark.checksTotal} | ${benchmark.score} | ${benchmark.limitation} |`
  )
  .join('\n');

const uniqueSources = benchmarkArtifacts
  .flatMap((artifact) => [...(artifact.external?.sources ?? []), ...(artifact.external?.source ? [artifact.external.source] : [])])
  .reduce((sources, source) => {
    const key = source.url ?? source.label;
    if (!sources.has(key)) sources.set(key, source);
    return sources;
  }, new Map());

const sourceRows = Array.from(uniqueSources.values())
  .map((source) => `- ${source.label}: ${source.url}. ${source.note}`)
  .join('\n');

const assumptionRows = assumptions.assumptions
  .map(
    (group) =>
      `### ${group.category}\n\n${group.items
        .map((item) => `- ${item.assumption} Status: ${item.status}. Risk: ${item.risk}`)
        .join('\n')}`
  )
  .join('\n\n');

const glossaryRows = glossary.map((item) => `- ${item.term}: ${item.definition}`).join('\n');

const unificationRows = unificationMap
  .map(
    (item) =>
      `| ${item.benchmarkFamily} | ${item.conventionalDomain} | ${item.grammarVariables} | ${item.currentReading} |`
  )
  .join('\n');

const h2o2CompressionRows = h2o2Quant
  ? `| Model cis/trans ratio | ${h2o2Quant.metrics.modelCisToTransRatio} |
| External cis/trans ratio | ${h2o2Quant.metrics.externalCisToTransRatio} |
| Compression factor | ${h2o2Quant.metrics.barrierRatioCompressionFactor} |
| Ratio shortfall | ${h2o2Quant.metrics.barrierRatioShortfallPct}% |`
  : '| H2O2 compression data | unavailable |';

const h2o2AbsoluteRows = h2o2Absolute
  ? `| Trans model barrier | ${h2o2Absolute.metrics.trans.modelCm1} cm-1 |
| Trans external barrier | ${h2o2Absolute.metrics.trans.externalCm1} cm-1 |
| Trans error | ${h2o2Absolute.metrics.trans.errorPct}% |
| Cis model barrier | ${h2o2Absolute.metrics.cis.modelCm1} cm-1 |
| Cis external barrier | ${h2o2Absolute.metrics.cis.externalCm1} cm-1 |
| Cis error | ${h2o2Absolute.metrics.cis.errorPct}% |
| Transfer-scale status | ${h2o2Absolute.status} |`
  : '| H2O2 absolute transfer data | unavailable |';

const hydrazineRows = hydrazineCation
  ? `| Status | ${hydrazineCation.status} |
| Model 0/180 ratio | ${hydrazineCation.metrics.modelBarrierRatio0To180} |
| External 0/180 ratio | ${hydrazineCation.metrics.externalBarrierRatio0To180} |
| Ratio error | ${hydrazineCation.metrics.ratioErrorPct}% |
| Ordering pass | ${hydrazineCation.metrics.orderingPass ? 'yes' : 'no'} |
| Absolute barrier pass | ${hydrazineCation.metrics.absolutePass ? 'yes' : 'no'} |
| 0 degree required scale multiplier | ${hydrazineCation.metrics.calibrationGap?.requiredScaleMultipliers?.find((row) => row.angle === 0)?.multiplier ?? 'n/a'}x |
| 180 degree required scale multiplier | ${hydrazineCation.metrics.calibrationGap?.requiredScaleMultipliers?.find((row) => row.angle === 180)?.multiplier ?? 'n/a'}x |
| Best single multiplier | ${hydrazineCation.metrics.calibrationGap?.leastSquaresScaleMultiplier ?? 'n/a'}x |`
  : '| Hydrazine cation transfer data | unavailable |';

const milestoneSummaryPath = new URL('milestone-external-review-summary.md', outDir).pathname;
const aiReviewPromptPath = new URL('milestone-external-review-ai-prompt.md', outDir).pathname;

const markdown = `# Relational Substrate Sandbox Milestone Summary for External Review

## Executive Status

Milestone status: ${completion.milestoneStatus}.

Sandbox completion reported by benchmark summary: ${completion.sandboxCompletionPct}%.

Benchmark passes: ${completion.benchmarkPasses}/${completion.totalBenchmarks}.

Checks passed: ${completion.checksPassed}/${completion.totalChecks}.

Grammar internal coherence: ${confidence.internalCoherenceOutOf10}/10.

Inferential convergence confidence: ${confidence.inferentialConvergenceOutOf10}/10.

Core independent evidence lines: ${summary.independentEvidenceLines}.

Orientation-only evidence lines: ${summary.orientationEvidenceLines}.

Cross-domain equivalence demonstrated: ${confidence.crossDomainEquivalenceOutOf10}/10.

Unification thesis support: ${confidence.unificationThesisSupportOutOf10}/10.

Next frontier: ${frontier.nextTarget}.

## Intent

${intent.primary}

${intent.ontologyBoundary}

${intent.equivalenceStandard}

${intent.inferenceStandard}

${intent.reviewQuestion}

## Glossary

${glossaryRows}

## What This Milestone Is

This is a completed external-review milestone for the sandbox layer. It is intended to give reviewers a stable, inspectable artifact before further modelling proceeds. The milestone bundles the current assumptions, external benchmark results, confidence posture, source anchors, limitations, and next validation gates.

The milestone is complete in the sense that the sandbox has moved from internal-only coherence work into a multi-domain external benchmark suite and has corrected closure drift in confidence framing, benchmark breadth, H2O2 compression, boundary-verification limits, glossary coverage, and unification mapping. It is not complete in the sense of final theory validation.

## What Was Tested

| Benchmark | Evidence line | Domain | Comparator | Status | Checks | Score | Limitation |
|---|---|---|---|---|---:|---:|---|
${benchmarkRows}

The benchmark pass count is not the same as independent-domain breadth. The suite has ${completion.totalBenchmarks} benchmark entries and ${completion.checksPassed}/${completion.totalChecks} passing checks, but the core independent evidence-line count is ${summary.independentEvidenceLines}, plus ${summary.orientationEvidenceLines} orientation-only boundary check. EM-02 through EM-07 collapse into one electromagnetic evidence line, and silicate network/NBO/T collapse into one broader material-structure group.

## Unification Map

| Benchmark family | Currently separate domain | Grammar variables exercised | Current reading |
|---|---|---|---|
${unificationRows}

## Current Evidence Reading

The sandbox now has externally anchored checks across molecule torsion, H2O2 absolute barrier transfer, held-out hydrazine cation torsion ordering, ionic ordering, qualitative electromagnetic ordering, Coulomb direction/ratio, two-source electric-field superposition, asymmetric three-source field geometry, continuous electric/magnetic field-line topology, electrostatic equipotential geometry, calibrated point-charge field magnitude, roughness-controlled interface scatter, silicate network order, and NBO/T material composition accounting. The boundary phase prediction is retained only as orientation evidence. The suite includes held-out material and interface checks, post-closure EM checks, and multiple quantitative checks. Its value proposition is not better mathematics; it is the possibility that one grammar can recover equivalent outputs across domains that are normally handled by separate models.

The positive evidence is that the same broad route/continuity grammar can repeatedly distinguish reference order from deliberately wrong alternatives without changing global ontology boundaries. The main weakness is that many checks are still qualitative ordering tests, and the quantitative checks are narrow: torsion shape/ratio, equilibrium angle, H2O2 barrier transfer, and composition accounting.

## H2O2 Compression Closure

The H2O2 cis/trans barrier-ratio discrepancy is quantified rather than left as a qualitative caveat:

| Measure | Value |
|---|---:|
${h2o2CompressionRows}

${
  h2o2AbsolutePass
    ? 'The prior roughly 2x compression is resolved in the current grammar version. This reduces the strongest previous falsification pressure, but it should not be treated as final validation because the anti-planar release was introduced after the failure was observed.'
    : 'This is the strongest known grammar limitation and the strongest current candidate for falsification. The roughly 2x compression factor means the current grammar does not recover the experimental separation between the shallow trans barrier and the high cis barrier. It is not resolved as a physical energy calibration, and it remains one of the strongest reasons not to raise inferential convergence above the current moderate level.'
}

The absolute transfer check sharpens the diagnosis by applying the ethane-derived energy scale to H2O2 without fitting either H2O2 endpoint:

| Measure | Value |
|---|---:|
${h2o2AbsoluteRows}

${
  h2o2AbsolutePass
    ? hydrazineCation
      ? 'This is now a convergence pass for the H2O2 transfer check: both trans and cis barriers land within tolerance under the ethane-derived scale. Hydrazine cation then tests the anti-planar release mechanism without endpoint fitting.'
      : 'This is now a convergence pass for the H2O2 transfer check: both trans and cis barriers land within tolerance under the ethane-derived scale. The next step is not more H2O2 fitting; it is an independent held-out torsion transfer check that can test whether anti-planar release generalizes.'
    : 'This is a mixed diagnostic, not a new convergence pass. The cis barrier lands on scale, but the trans barrier is overpredicted by roughly 2x. The next peroxide revision should therefore target the shallow trans barrier floor and relative closure/phase scaling, not broad energy rescaling.'
}

## Held-Out Torsion Transfer

Hydrazine cation tests anti-planar release on a separate N-N torsion target without fitting hydrazine endpoints:

| Measure | Value |
|---|---:|
${hydrazineRows}

${
  hydrazineTransferPass
    ? 'The held-out hydrazine cation torsion transfer passes ordering, ratio, and absolute magnitude checks under the ethane scale.'
    : hydrazineOrderingPass
    ? 'The held-out hydrazine cation torsion check supports anti-planar release qualitatively and ratiometrically, but misses absolute barrier magnitudes. The calibration-gap diagnostic shows the miss is not solved by a clean global multiplier: the 0 degree barrier needs about 3.04x, the 180 degree barrier needs about 2.21x, and the best single multiplier would still leave a relative-barrier shape error. This reduces H2O2-overfit concern without establishing a calibrated torsional energy model.'
    : hydrazineCation
    ? 'The held-out hydrazine cation torsion check fails to generalize anti-planar release, which should reduce confidence in the H2O2 refinement.'
    : 'No held-out torsion transfer check has been run yet.'
}

## Boundary Benchmark Verification

Boundary benchmark verification status: ${boundaryBenchmark?.predictionManifest?.verificationStatus ?? 'unavailable'}.

This benchmark is retained as a documented qualitative pass because it records explicit prediction criteria and named external references. It is not treated as a fully independent historical blind prediction and is classified as orientation evidence only, not core convergence evidence. Its inferential weight is therefore lower than a timestamped held-out benchmark.

## Confidence

${summary.confidence.rationale}

${confidence.reading}

Confidence should be read as inferential convergence, not proof-of-substrate framing. It asks how much independent, non-circular evidence has converged on the grammar as a coherent explanatory framework relative to conventional domain models. The right next confidence increase requires calibrated physical-property prediction, a stricter held-out benchmark against a conventional comparator, or a new non-molecular domain check with no rescaling or endpoint anchoring.

## Explicit Non-Claims

${nonClaims.map((claim) => `- ${claim}`).join('\n')}

## Remaining Gates

${summary.remainingExternalGates.map((gate) => `- ${gate}`).join('\n')}

## Source Anchors

${sourceRows}

## Assumptions and Risks

${assumptionRows}

## Reviewer Questions

${reviewPackage.reviewerQuestions.map((question) => `- ${question}`).join('\n')}

## Recommended Next Stage

Do not extend the sandbox laterally until the review package has been read. EM-05 completed the recommended topology broadening step, EM-06 links scalar potential geometry to the vector-field checks, EM-07 adds calibrated point-charge field magnitude, H2O2 absolute barrier transfer has reduced the strongest prior falsification candidate, and hydrazine cation has tested anti-planar release as a held-out torsion ordering check. The next stage should pick one high-value calibrated target rather than another shallow fixture:

- Move held-out torsion transfer from qualitative/ratiometric ordering toward calibrated absolute barrier magnitudes.
- A measured material-property correlation downstream of NBO/T, such as viscosity, durability, or conductivity.
- A calibrated roughness/scatter quantity, not only specular/diffuse ordering.
- A conventional-comparator review that asks whether the Relational Substrate grammar adds predictive leverage over standard physical models.
- A conductor/material-media or time-dependent propagation comparator that tests whether EM-07 generalizes beyond point-charge electrostatics.
`;

await writeFile(new URL('milestone-external-review-summary.md', outDir), markdown);

const aiReviewPrompt = `# AI Review Prompt: Relational Substrate Sandbox Closure Milestone

You are reviewing the Relational Substrate sandbox closure package.

Your task is not to endorse the theory. Your task is to evaluate whether the sandbox, as described in the attached milestone summary, has corrected closure drift and is ready to proceed from sandbox work into stricter quantitative validation.

## Primary Intent

The Relational Substrate sandbox tests whether a small unified grammar of route, closure, phase, charge, and continuity variables can reproduce, with reasonable equivalence, outputs and orderings that established domain models already produce while providing one ontological framework across phenomena those models usually treat separately.

Do not treat the sandbox as a literal substrate simulation. It does not simulate T0 directly, does not derive atoms or molecules from T1 vortons, and does not replace quantum chemistry, molecular dynamics, optics, glass-property, Fresnel, BRDF, or rough-surface scattering solvers.

The standard is equivalence-with-unification, not displacement. A useful review asks whether the grammar has enough independent, non-circular evidential convergence to justify stricter validation.

## Document to Review

Review the attached or pasted file:

\`milestone-external-review-summary.md\`

Local source path:

\`${milestoneSummaryPath}\`

## Current Reported Status

- Sandbox completion: ${completion.sandboxCompletionPct}%
- Benchmarks: ${completion.benchmarkPasses}/${completion.totalBenchmarks} passing
- Checks: ${completion.checksPassed}/${completion.totalChecks} passing
- Core independent evidence lines: ${summary.independentEvidenceLines}
- Orientation-only evidence lines: ${summary.orientationEvidenceLines}
- Grammar internal coherence: ${confidence.internalCoherenceOutOf10}/10
- Inferential convergence confidence: ${confidence.inferentialConvergenceOutOf10}/10
- Cross-domain equivalence demonstrated: ${confidence.crossDomainEquivalenceOutOf10}/10
- Unification thesis support: ${confidence.unificationThesisSupportOutOf10}/10

Do not assume these scores are correct. Audit whether the evidence described in the summary supports them.

## Required Review Output

Produce a structured review with these sections:

1. Executive verdict: ready for external review, ready with revisions, or not ready.
2. Intent and ontology boundary audit: check whether T0/T1/T2 separation is clear and whether analogy is being confused with mechanism.
3. Equivalence standard audit: assess whether the document correctly uses equivalence-with-unification rather than proof or displacement framing.
4. Evidence audit: identify the strongest benchmark, weakest benchmark, and any hidden tuning or permissive tolerance risk.
5. Benchmark breadth audit: assess whether ${summary.independentEvidenceLines} core independent evidence lines plus ${summary.orientationEvidenceLines} orientation-only boundary check is a fair breadth count.
6. Torsion audit: evaluate whether the H2O2 post-refinement pass plus hydrazine cation held-out ordering pass credibly reduce overfit concern, and whether the hydrazine absolute-magnitude miss is weighted honestly.
7. Boundary benchmark audit: evaluate whether the documented-but-not-timestamped status is stated honestly enough.
8. Unification map audit: assess whether the benchmarks actually support the stated cross-domain unification thesis.
9. Confidence calibration: give your own scores for grammar internal coherence, cross-domain equivalence, evidence independence, unification thesis support, and inferential convergence.
10. Next validation target: choose exactly one next target, prioritizing calibrated prediction or a held-out conventional comparator over more shallow fixture depth.

Apply a skeptical but constructive standard. Penalize overclaims, proof-framing, weak comparators, qualitative wins presented as strong validation, and confidence increases without calibrated prediction. Credit clear non-claims, explicit ontology boundaries, source anchoring, held-out checks, quantified limitations, and honest downgrade language.

## Optional Summary Paste Area

Paste \`milestone-external-review-summary.md\` below this line if not attaching it separately.

---
`;

await writeFile(new URL('milestone-external-review-ai-prompt.md', outDir), aiReviewPrompt);

console.log('Milestone status: complete for external review');
console.log(`Inferential convergence confidence: ${confidence.inferentialConvergenceOutOf10}/10`);
console.log(`Wrote ${milestoneSummaryPath}`);
console.log(`Wrote ${aiReviewPromptPath}`);
