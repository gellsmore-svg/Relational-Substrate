import { mkdir, writeFile } from 'node:fs/promises';
import { scorePsdBackedBrdfShape } from './roughness-psd-brdf-model.mjs';

const outDir = new URL('./out/', import.meta.url);
const wavelengthMeters = 632.8e-9;
const incidenceAngleDegrees = 3;
const scatterAngles = [-12, -8, -4, 0, 8, 12, 16];

function frequency(angle) {
  return (
    Math.abs(
      Math.sin((angle * Math.PI) / 180) -
        Math.sin((incidenceAngleDegrees * Math.PI) / 180),
    ) / wavelengthMeters
  );
}

const frequencies = scatterAngles.map(frequency).sort((a, b) => a - b);
const minimumFrequency = frequencies[0] * 0.8;
const maximumFrequency = frequencies.at(-1) * 1.2;
const psdRows = Array.from({ length: 30 }, (_, index) => {
  const fraction = index / 29;
  const spatialFrequencyPerMeter =
    minimumFrequency * (maximumFrequency / minimumFrequency) ** fraction;
  return {
    spatialFrequencyPerMeter,
    psd: 1e-24 * (spatialFrequencyPerMeter / minimumFrequency) ** -1.7,
  };
});

function interpolateFixture(frequencyValue) {
  return 1e-24 * (frequencyValue / minimumFrequency) ** -1.7;
}

const matchingBrdfRows = scatterAngles.map((scatterAngleDegrees) => ({
  scatterAngleDegrees,
  brdf: interpolateFixture(frequency(scatterAngleDegrees)) * 3.5e25,
}));
const reversedBrdfRows = matchingBrdfRows.map((row) => ({
  scatterAngleDegrees: row.scatterAngleDegrees,
  brdf: 1 / row.brdf,
}));

const matching = scorePsdBackedBrdfShape({
  wavelengthMeters,
  incidenceAngleDegrees,
  specularAngleDegrees: incidenceAngleDegrees,
  specularMaskDegrees: 0.1,
  psdRows,
  brdfRows: matchingBrdfRows,
});
const reversed = scorePsdBackedBrdfShape({
  wavelengthMeters,
  incidenceAngleDegrees,
  specularAngleDegrees: incidenceAngleDegrees,
  specularMaskDegrees: 0.1,
  psdRows,
  brdfRows: reversedBrdfRows,
});

const checks = [
  {
    check: 'known matching fixture passes',
    pass: matching.passed,
    value: matching.status,
  },
  {
    check: 'known reversed fixture fails',
    pass: !reversed.passed,
    value: reversed.status,
  },
  {
    check: 'matching fixture has near-zero shape error',
    pass: matching.metrics.meanAbsoluteError < 1e-10,
    value: matching.metrics.meanAbsoluteError,
  },
  {
    check: 'matching fixture rank correlation is one',
    pass: Math.abs(matching.metrics.spearman - 1) < 1e-10,
    value: matching.metrics.spearman,
  },
];

const passed = checks.every((check) => check.pass);
const report = {
  source: 'roughness-psd-brdf-feasibility-diagnostic.mjs',
  date: '2026-06-24',
  status: passed
    ? 'psd-brdf-scorer-known-answer-pass'
    : 'psd-brdf-scorer-known-answer-fail',
  validationClaim: false,
  evidenceStatus: 'none; synthetic implementation fixtures only',
  implementation: {
    interpolation: 'log-log linear within measured PSD support',
    extrapolation: 'prohibited',
    specularMask: 'strict angular exclusion',
    normalization: 'independent maxima over identical surviving rows',
  },
  matching,
  reversed,
  checks,
  decision: passed
    ? 'the scorer is ready for a source-locked tungsten JSON artifact without changing the frozen comparator'
    : 'repair the scorer before consuming any recovered source data',
};

const markdown = `# PSD-Backed BRDF Scorer Feasibility

Status: **${report.status}**

This is a synthetic known-answer test. It adds no evidence.

| Check | Value | Result |
|---|---|---|
${checks
  .map(
    (row) =>
      `| ${row.check} | ${row.value} | ${row.pass ? 'pass' : 'fail'} |`,
  )
  .join('\n')}

Implementation:

- PSD interpolation: ${report.implementation.interpolation}
- extrapolation: ${report.implementation.extrapolation}
- normalization: ${report.implementation.normalization}

Decision: ${report.decision}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-psd-brdf-feasibility-diagnostic.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-psd-brdf-feasibility-diagnostic.md', outDir),
  markdown,
);

console.log(`PSD/BRDF scorer feasibility: ${report.status}`);
