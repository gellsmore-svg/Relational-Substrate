import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const docsDir = new URL('../docs/', import.meta.url);

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

function uniqueByUrl(sources) {
  const seen = new Set();
  return sources.filter((source) => {
    if (!source?.url || seen.has(source.url)) return false;
    seen.add(source.url);
    return true;
  });
}

function statusIcon(pass) {
  return pass ? 'pass' : 'review';
}

const summary = await readJson('external-benchmark-summary.json');
const milestone = await readJson('milestone-external-review-summary.json');
const em17 = await readJson('external-em-double-slit-envelope-comparator.json');
const explicitArtifacts = (
  await Promise.all([
    readOptionalJson('external-h2o2-benchmark.json'),
    readOptionalJson('external-h2o2-quantitative-benchmark.json'),
    readOptionalJson('external-h2o2-absolute-barrier-benchmark.json'),
    readOptionalJson('external-hydrazine-cation-torsion-benchmark.json'),
    readOptionalJson('external-ethane-benchmark.json'),
    readOptionalJson('external-ethane-quantitative-benchmark.json'),
    readOptionalJson('external-ionic-benchmark.json'),
    readOptionalJson('external-boundary-blind-benchmark.json'),
    readOptionalJson('external-em-ordering-benchmark.json'),
    readOptionalJson('external-em-coulomb-comparator.json'),
    readOptionalJson('external-em-superposition-comparator.json'),
    readOptionalJson('external-em-three-source-comparator.json'),
    readOptionalJson('external-em-field-line-topology-comparator.json'),
    readOptionalJson('external-em-equipotential-comparator.json'),
    readOptionalJson('external-em-field-magnitude-comparator.json'),
    readOptionalJson('external-em-dielectric-media-comparator.json'),
    readOptionalJson('external-em-wave-propagation-comparator.json'),
    readOptionalJson('external-em-boundary-propagation-comparator.json'),
    readOptionalJson('external-em-oblique-fresnel-comparator.json'),
    readOptionalJson('external-em-multilayer-interference-comparator.json'),
    readOptionalJson('external-em-absorbing-media-comparator.json'),
    readOptionalJson('external-em-rough-surface-scatter-comparator.json'),
    readOptionalJson('external-em-diffraction-grating-comparator.json'),
    readOptionalJson('external-em-single-slit-envelope-comparator.json'),
    readOptionalJson('external-em-double-slit-envelope-comparator.json'),
    readOptionalJson('external-silicate-heldout-benchmark.json'),
    readOptionalJson('external-roughness-heldout-benchmark.json'),
    readOptionalJson('external-material-nbo-quantitative-benchmark.json'),
    readOptionalJson('external-material-refractive-index-challenge.json'),
    readOptionalJson('external-roughness-calibrated-scatter-benchmark.json'),
  ])
).filter(Boolean);

const sources = uniqueByUrl(
  explicitArtifacts.flatMap((artifact) =>
    Array.isArray(artifact.external?.sources)
      ? artifact.external.sources.map((source) => ({
          benchmark: artifact.source,
          ...source,
        }))
      : []
  )
);

const materialRefractiveIndex = explicitArtifacts.find(
  (artifact) => artifact.source === 'external-material-refractive-index-challenge.mjs'
);

const driftChecks = [
  {
    area: 'Benchmark scope',
    status: statusIcon(Boolean(materialRefractiveIndex) && summary.benchmarkPasses < summary.benchmarks.length),
    finding:
      'The aggregate now includes an explicit unresolved material refractive-index challenge with a first-pass topology-only predictor, a target-implied repair candidate that fails fresh anorthite validation, and a second-generation modifier-identity candidate that fits current rows but remains target-informed calibration debt. Reviewers should verify that neither candidate is treated as a hidden material-property pass.',
  },
  {
    area: 'EM evidence independence',
    status: 'review',
    finding:
      'EM-02 through EM-17 are depth checks inside one electromagnetic evidence line, not separate independent domains. They should increase confidence in grammar breadth within EM but should not be counted as independent cross-domain evidence.',
  },
  {
    area: 'Double-slit completeness',
    status: statusIcon(em17.status === 'double-slit envelope comparator pass'),
    finding:
      'EM-17 covers scalar bright/dark fringe positions, finite-slit modulation, missing-order suppression, symmetry, scaling, and screen mapping. It deliberately excludes vector diffraction, broadband intensities, resolving power, radiation generation, and Maxwell solving.',
  },
  {
    area: 'Confidence drift',
    status: 'pass',
    finding:
      `The confidence posture remains conservative after adding calibrated roughness scatter and an unresolved material-property challenge: inferential convergence is ${summary.confidence.updatedInferentialConvergenceOutOf10}/10 and unification support is ${summary.confidence.unificationThesisSupportOutOf10}/10. This keeps scalar EM depth, imported smooth-surface TIS accounting, and NBO/T composition accounting from being counted as near-decisive evidence.`,
  },
  {
    area: 'Non-claim discipline',
    status: 'review',
    finding:
      'The milestone report explicitly says the sandbox is not proof of the theory, not T0 simulation, not vorton-to-atom derivation, and not a quantum chemistry, material property, BRDF, diffraction, roughness, Fresnel, or Maxwell solver.',
  },
  {
    area: 'Known weak points',
    status: 'review',
    finding:
      'Remaining gates still include the unresolved material refractive-index challenge, held-out torsion absolute magnitudes, roughness/interface movement beyond smooth-surface TIS, and EM movement beyond scalar double-slit envelope coupling. Hydrazine absolute-magnitude miss is the live torsion falsification pressure after the H2O2 pass.',
  },
];

const completenessChecklist = [
  'Verify every benchmark row has an artifact, source anchor, status, score, explicit limitation, and confidence effect.',
  'Check that EM-17 equations match standard scalar Fraunhofer double-slit optics: d sin(theta) = m lambda, d sin(theta) = (m + 1/2) lambda, envelope sinc(beta)^2, and missing orders where an interference maximum coincides with a single-slit minimum.',
  `Confirm the report keeps breadth and depth separate: ${summary.benchmarks.length} benchmarks, ${summary.independentEvidenceLines} core independent evidence lines, and ${summary.orientationEvidenceLines} orientation-only evidence line.`,
  'Confirm boundary-phase evidence remains labelled orientation-only and is not inflated into independent proof.',
  'Audit whether any wording implies direct substrate proof, direct T0 simulation, or displacement of conventional models.',
  'Check whether confidence increments after EM-15 through EM-17 are modest enough for scalar analytic optics comparators.',
  'Confirm that the recalibrated confidence score stays near 6/10 until a calibrated material-property prediction, measured scatter curve, or held-out absolute torsion transfer passes.',
  'Confirm that the material refractive-index row is treated as an unresolved measured-property challenge, not as a benchmark pass.',
  'Check whether the second-generation modifier-identity refractive-index candidate is sufficiently predeclared for the next held-out target, and whether it still omits required variables such as density, cation field strength, molar refraction, or polarizability.',
  'Identify any missing source citations or comparator assumptions that should be made explicit before external review.',
  'Recommend the next falsification-oriented benchmark, prioritizing calibrated quantities or held-out cases over more same-family EM depth checks.',
];

const requestedClaudeOutput = [
  'List any drift from the stated ontology boundary or equivalence-with-unification standard.',
  'List any overclaiming or underqualified confidence language.',
  'List any completeness gaps in EM-17, the aggregate summary, or the milestone report.',
  'Separate blocking issues from advisory improvements.',
  'State whether the package is ready for external review as a sandbox milestone, not as proof of the theory.',
  'Propose the next two highest-value validation tasks.',
];

const reviewPacket = {
  source: 'claude-drift-completeness-review.mjs',
  status: 'Claude drift and completeness review packet',
  generatedFrom: [
    'external-benchmark-summary.json',
    'milestone-external-review-summary.json',
    'external-em-double-slit-envelope-comparator.json',
  ],
  currentMetrics: {
    status: summary.status,
    sandboxCompletionPct: summary.confidence.updatedSandboxCompletionPct,
    internalCoherenceOutOf10: summary.confidence.updatedInternalCoherenceOutOf10,
    inferentialConvergenceOutOf10: summary.confidence.updatedInferentialConvergenceOutOf10,
    crossDomainEquivalenceOutOf10: summary.confidence.crossDomainEquivalenceOutOf10,
    unificationThesisSupportOutOf10: summary.confidence.unificationThesisSupportOutOf10,
    benchmarkPasses: `${summary.benchmarkPasses}/${summary.benchmarks.length}`,
    checksPassed: `${summary.passedChecks}/${summary.totalChecks}`,
    independentEvidenceLines: summary.independentEvidenceLines,
    orientationEvidenceLines: summary.orientationEvidenceLines,
  },
  em17: {
    status: em17.status,
    score: em17.score,
    modeledSubset: em17.external.modeledSubset,
    notModeled: em17.external.notModeled,
    metrics: em17.metrics,
    checks: em17.checks.map((check) => ({
      check: check.check,
      pass: check.pass,
      expectation: check.expectation,
      modelValue: check.modelValue,
      reading: check.reading,
    })),
  },
  materialRefractiveIndexChallenge: materialRefractiveIndex
    ? {
        status: materialRefractiveIndex.status,
        score: materialRefractiveIndex.score,
        rows: materialRefractiveIndex.rows,
        checks: materialRefractiveIndex.checks,
      }
    : null,
  driftChecks,
  completenessChecklist,
  remainingGates: summary.remainingExternalGates,
  evidenceLineSummaries: summary.evidenceLineSummaries,
  nonClaims: milestone.nonClaims,
  requestedClaudeOutput,
  sources,
};

await writeFile(new URL('claude-drift-completeness-review.json', outDir), JSON.stringify(reviewPacket, null, 2));

const markdown = `# Claude Drift And Completeness Review Packet

## Review Role

Review this as an external critique packet for the Relational Substrate sandbox. The question is not whether the theory is proven. The question is whether the generated research package has drifted from its stated boundaries, whether EM-17 is complete within its declared scalar scope, and whether the aggregate confidence claims remain proportionate.

## Current Metrics

| Measure | Value |
|---|---:|
| Status | ${summary.status} |
| Sandbox completion | ${summary.confidence.updatedSandboxCompletionPct}% |
| Internal coherence | ${summary.confidence.updatedInternalCoherenceOutOf10}/10 |
| Inferential convergence | ${summary.confidence.updatedInferentialConvergenceOutOf10}/10 |
| Cross-domain equivalence | ${summary.confidence.crossDomainEquivalenceOutOf10}/10 |
| Unification thesis support | ${summary.confidence.unificationThesisSupportOutOf10}/10 |
| Benchmark passes | ${summary.benchmarkPasses}/${summary.benchmarks.length} |
| Checks passed | ${summary.passedChecks}/${summary.totalChecks} |
| Core independent evidence lines | ${summary.independentEvidenceLines} |
| Orientation-only evidence lines | ${summary.orientationEvidenceLines} |

## EM-17 Summary

| Measure | Value |
|---|---:|
| Status | ${em17.status} |
| Score | ${em17.score} |
| Modeled subset | ${em17.external.modeledSubset} |
| Not modeled | ${em17.external.notModeled} |

EM-17 exercises route, closure, phase, and continuity. It does not exercise the charge variable in a non-trivial way; charge is explicitly inactive because this is a scalar wave-geometry diffraction comparator, not a charge-dynamics or radiation-generation model.

## Independent Evidence Lines

| Evidence line | Benchmarks | Checks | Grammar variables exercised | Counting status |
|---|---:|---:|---|---|
${summary.evidenceLineSummaries
  .map(
    (line) =>
      `| ${line.evidenceLine} | ${line.benchmarkCount} | ${line.checksPassed}/${line.checksTotal} | ${line.variables} | ${line.orientationOnly ? 'orientation-only' : 'core evidence'} |`
  )
  .join('\n')}

## EM-17 Checks

| Check | Expectation | Model value | Pass | Reading |
|---|---|---|---|---|
${em17.checks
  .map(
    (check) =>
      `| ${check.check} | ${check.expectation} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} | ${check.reading} |`
  )
  .join('\n')}

## Drift Audit Targets

${driftChecks.map((check) => `- ${check.area}: ${check.status}. ${check.finding}`).join('\n')}

## Completeness Checklist

${completenessChecklist.map((item) => `- ${item}`).join('\n')}

## Remaining Gates

${summary.remainingExternalGates.map((gate) => `- ${gate}`).join('\n')}

## Non-Claims To Preserve

${milestone.nonClaims.map((claim) => `- ${claim}`).join('\n')}

## Requested Claude Output

${requestedClaudeOutput.map((item) => `- ${item}`).join('\n')}

## Source Anchors

${sources.map((source) => `- ${source.label}: ${source.url}. ${source.note}`).join('\n')}

## File Context

- Aggregate summary: analysis/out/external-benchmark-summary.md
- Milestone review: analysis/out/milestone-external-review-summary.md
- EM-17 report: analysis/out/external-em-double-slit-envelope-comparator.md
- This packet: analysis/out/claude-drift-completeness-review.md
`;

await writeFile(new URL('claude-drift-completeness-review.md', outDir), markdown);
await mkdir(docsDir, { recursive: true });
await writeFile(new URL('claude-drift-completeness-review.md', docsDir), markdown);

console.log(`Claude review packet: ${reviewPacket.status}`);
console.log(`Wrote ${new URL('claude-drift-completeness-review.md', outDir).pathname}`);
console.log(`Wrote ${new URL('claude-drift-completeness-review.md', docsDir).pathname}`);
