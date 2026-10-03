// Synthetic known-answer test for the profile-PSD versus scatter-derived-PSD
// shape comparator v0 (predeclaration hash ad3892b700d0b82f).
//
// This adds NO evidence. It proves the scorer accepts a curve that matches the
// independent profile PSD shape (up to a vertical offset) and rejects an
// inverse-shape curve, before any source-locked numerical data is consumed.

import { mkdir, readFile, writeFile } from 'node:fs/promises';
import {
  PREDECLARATION_HASH,
  scoreProfilePsdVsScatterPsdShape,
} from './roughness-profile-psd-scatter-psd-model.mjs';

const outDir = new URL('./out/', import.meta.url);

// Confirm the frozen comparator hash still matches the committed predeclaration.
const predeclaration = JSON.parse(
  await readFile(
    new URL('roughness-profile-psd-scatter-psd-predeclaration.json', outDir),
    'utf8',
  ),
);
const hashMatchesPredeclaration =
  predeclaration.predeclaration.hash === PREDECLARATION_HASH;

// Independent topography profile PSD: a smooth inverse-power law over a decade.
const minimumFrequency = 6e3; // m^-1
const maximumFrequency = 6e4; // m^-1, just over one decade of support
const profilePsdRows = Array.from({ length: 25 }, (_, index) => {
  const fraction = index / 24;
  const spatialFrequencyPerMeter =
    minimumFrequency * (maximumFrequency / minimumFrequency) ** fraction;
  return {
    spatialFrequencyPerMeter,
    psd: 2e-18 * (spatialFrequencyPerMeter / minimumFrequency) ** -1.9,
  };
});

function trueProfilePsd(frequency) {
  return 2e-18 * (frequency / minimumFrequency) ** -1.9;
}

// Twelve PSDscatter sample frequencies inside the support, plus two that the
// scorer must drop: one below support and one inside a source-defined exclusion.
const sampleFrequencies = Array.from({ length: 12 }, (_, index) => {
  const fraction = index / 11;
  return minimumFrequency * 1.05 * (maximumFrequency / (minimumFrequency * 1.05)) ** fraction;
});
const exclusions = [{ minPerMeter: 3.1e4, maxPerMeter: 3.4e4, reason: 'synthetic instrument-signature notch' }];

// Matching fixture: scatter PSD equals the profile shape times a constant
// vertical offset (median-centering must remove the offset → near-zero error).
const verticalOffset = 41.7;
const matchingScatterRows = [
  { spatialFrequencyPerMeter: minimumFrequency * 0.5, psd: 9.9e-19 }, // below support, must drop
  ...sampleFrequencies.map((spatialFrequencyPerMeter) => ({
    spatialFrequencyPerMeter,
    psd: trueProfilePsd(spatialFrequencyPerMeter) * verticalOffset,
  })),
];

// Inverse-shape fixture: scatter PSD is the reciprocal shape (anti-correlated).
const inverseScatterRows = sampleFrequencies.map((spatialFrequencyPerMeter) => ({
  spatialFrequencyPerMeter,
  psd: 1e-37 / trueProfilePsd(spatialFrequencyPerMeter),
}));

const matching = scoreProfilePsdVsScatterPsdShape({
  profilePsdRows,
  scatterPsdRows: matchingScatterRows,
  exclusions,
});
const inverse = scoreProfilePsdVsScatterPsdShape({
  profilePsdRows,
  scatterPsdRows: inverseScatterRows,
  exclusions,
});

const checks = [
  {
    check: 'committed predeclaration hash matches the scorer constant',
    pass: hashMatchesPredeclaration,
    value: `${predeclaration.predeclaration.hash} vs ${PREDECLARATION_HASH}`,
  },
  {
    check: 'matching offset-only fixture passes',
    pass: matching.passed,
    value: matching.status,
  },
  {
    check: 'inverse-shape fixture fails',
    pass: !inverse.passed,
    value: inverse.status,
  },
  {
    check: 'matching fixture drops the below-support and excluded rows',
    pass: matching.metrics !== null && matching.metrics.survivingRowCount === sampleFrequencies.length - 1,
    value:
      matching.metrics === null
        ? 'no metrics'
        : `${matching.metrics.survivingRowCount} surviving of ${sampleFrequencies.length} in-band samples`,
  },
  {
    check: 'matching fixture has near-zero centered shape error',
    pass: matching.metrics !== null && matching.metrics.meanAbsoluteCenteredLog10Error < 1e-10,
    value: matching.metrics ? matching.metrics.meanAbsoluteCenteredLog10Error : 'no metrics',
  },
  {
    check: 'matching fixture rank correlation is one',
    pass: matching.metrics !== null && Math.abs(matching.metrics.spearman - 1) < 1e-10,
    value: matching.metrics ? matching.metrics.spearman : 'no metrics',
  },
  {
    check: 'inverse fixture rank correlation is negative one',
    pass: inverse.metrics !== null && Math.abs(inverse.metrics.spearman + 1) < 1e-10,
    value: inverse.metrics ? inverse.metrics.spearman : 'no metrics',
  },
];

const passed = checks.every((check) => check.pass);
const report = {
  source: 'roughness-profile-psd-scatter-psd-feasibility-diagnostic.mjs',
  date: '2026-06-24',
  status: passed
    ? 'profile-psd-scatter-psd-scorer-known-answer-pass'
    : 'profile-psd-scatter-psd-scorer-known-answer-fail',
  predeclarationHash: PREDECLARATION_HASH,
  validationClaim: false,
  evidenceStatus: 'none; synthetic implementation fixtures only',
  implementation: {
    interpolation: 'log-log linear within independent profile PSD support',
    extrapolation: 'prohibited; below/above support rows dropped',
    exclusionHandling: 'source-defined instrument/specular/validity ranges dropped',
    normalization: 'subtract each curve median log10 over identical surviving rows',
  },
  matching,
  inverse,
  checks,
  decision: passed
    ? 'the comparator is ready for a source-locked profile-PSD/PSDscatter artifact without changing the frozen model form'
    : 'repair the comparator before consuming any recovered source data',
};

const markdown = `# Profile-PSD versus Scatter-Derived-PSD Scorer Feasibility

Status: **${report.status}**

This is a synthetic known-answer test. It adds no evidence.

| Check | Value | Result |
|---|---|---|
${checks
  .map((row) => `| ${row.check} | ${row.value} | ${row.pass ? 'pass' : 'fail'} |`)
  .join('\n')}

Implementation:

- profile PSD interpolation: ${report.implementation.interpolation}
- extrapolation: ${report.implementation.extrapolation}
- exclusion handling: ${report.implementation.exclusionHandling}
- normalization: ${report.implementation.normalization}

Decision: ${report.decision}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-profile-psd-scatter-psd-feasibility-diagnostic.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-profile-psd-scatter-psd-feasibility-diagnostic.md', outDir),
  markdown,
);

console.log(`Profile/scatter PSD scorer feasibility: ${report.status}`);
