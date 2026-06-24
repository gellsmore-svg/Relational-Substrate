import { mkdir, writeFile } from 'node:fs/promises';
import {
  AE_C,
  O2_MINUS_PARAMS,
  anionPolarizability,
  indexFromPolarizability,
  polarizabilityFromIndex,
  totalPolarizability,
} from './ri-structural-predictor-v1-model.mjs';

// Synthetic / source-anchor feasibility test for the v1 predictor machinery
// (predeclaration ri-structural-predictor-v1-predeclaration.mjs). Adds no evidence.
// It (1) validates the Anderson-Eggleton forward/inverse round-trip, (2) validates
// additivity, and (3) HONESTLY checks whether the eqn (6) anion-volume O2- model as
// transcribed reproduces the Shannon-Fischer SiO2 oxygen value (~1.44 A^3). The
// oxygen check is expected to flag: the parameter interpretation is not yet anchored,
// which correctly blocks scored use until resolved.

const outDir = new URL('./out/', import.meta.url);

// (1) Anderson-Eggleton round-trip over a mineral-relevant grid.
const indices = [1.40, 1.50, 1.60, 1.65, 1.74, 1.85, 1.90];
const volumes = [20, 40, 60, 100, 180, 300];
let maxRoundtripError = 0;
for (const n of indices) {
  for (const vm of volumes) {
    const alpha = polarizabilityFromIndex(n, vm, AE_C);
    const back = indexFromPolarizability(alpha, vm, AE_C);
    maxRoundtripError = Math.max(maxRoundtripError, Math.abs(back - n));
  }
}

// (2) Additivity sanity: a synthetic 2-ion compound.
const additivityCheck = totalPolarizability([
  { alpha: 1.79, count: 1 },
  { alpha: 0.284, count: 1 },
]);
const additivityExpected = 1.79 + 0.284;

// (3) Source-anchor check for the eqn (6) oxygen model. SF2016 reports the
// in-crystal O2- polarizability in SiO2 as ~1.44 A^3. Quartz anion molar volume
// V_an = unit-cell volume / number of O ~ 113.0/6 ~ 18.83 A^3. Try the transcribed
// sign (No = -1.776) and the corrected sign (No = +1.776) and compare to 1.44.
const sio2AnionMolarVolume = 18.83;
const sio2ExpectedAlphaO = 1.44;
const oxygenTranscribed = anionPolarizability({ ...O2_MINUS_PARAMS, anionMolarVolume: sio2AnionMolarVolume });
const oxygenSignFlipped = anionPolarizability({ ...O2_MINUS_PARAMS, No: -O2_MINUS_PARAMS.No, anionMolarVolume: sio2AnionMolarVolume });
const oxygenAnchorTolerance = 0.03;
const oxygenAnchored =
  Math.abs(oxygenTranscribed - sio2ExpectedAlphaO) / sio2ExpectedAlphaO <= oxygenAnchorTolerance ||
  Math.abs(oxygenSignFlipped - sio2ExpectedAlphaO) / sio2ExpectedAlphaO <= oxygenAnchorTolerance;

const checks = [
  {
    check: 'Anderson-Eggleton (4a)<->(4b) round-trip recovers n',
    pass: maxRoundtripError < 1e-10,
    value: maxRoundtripError,
  },
  {
    check: 'additivity (5) sums ion polarizabilities',
    pass: Math.abs(additivityCheck - additivityExpected) < 1e-12,
    value: additivityCheck,
  },
  {
    check: 'eqn (6) O2- model reproduces the SF2016 SiO2 oxygen value (~1.44 A^3)',
    pass: oxygenAnchored,
    value: `transcribed No=-1.776 -> ${oxygenTranscribed.toFixed(3)}; sign-flipped No=+1.776 -> ${oxygenSignFlipped.toFixed(3)}; target ${sio2ExpectedAlphaO}`,
  },
];

const machineryValid = checks[0].pass && checks[1].pass;
const oxygenAnchorPass = checks[2].pass;
const status = machineryValid
  ? oxygenAnchorPass
    ? 'v1-machinery-validated-and-oxygen-anchored'
    : 'v1-machinery-validated-oxygen-model-NOT-anchored-scoring-blocked'
  : 'v1-machinery-FAILED';

const report = {
  source: 'ri-structural-predictor-v1-feasibility-diagnostic.mjs',
  date: '2026-06-24',
  status,
  validationClaim: false,
  evidenceStatus: 'none; synthetic machinery test plus a source-anchor check',
  predictorPredeclaration: 'ri-structural-predictor-v1-predeclaration.mjs',
  checks,
  reading:
    'The Anderson-Eggleton forward/inverse and additivity are implemented correctly (round-trip error ~machine epsilon). The eqn (6) anion-volume O2- model as transcribed does NOT reproduce the Shannon-Fischer SiO2 oxygen value under either sign of No at the assumed quartz anion volume, so the oxygen parameterisation is not yet anchored. Per the v1 predeclaration next-gate, scoring is blocked until the exact SF2016 oxygen parameters (free-ion alpha, No, and the anion-volume convention SF2016 used) are pinned against a worked source value. The AE+additivity core can be used now; the oxygen term cannot.',
};

const markdown = `# RI Predictor v1 Feasibility / Source-Anchor Test

Status: **${status}**

This is a machinery + source-anchor test. It adds no evidence.

| Check | Value | Result |
|---|---|---|
${checks.map((c) => `| ${c.check} | ${c.value} | ${c.pass ? 'pass' : 'FLAG'} |`).join('\n')}

Reading: ${report.reading}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-structural-predictor-v1-feasibility-diagnostic.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-structural-predictor-v1-feasibility-diagnostic.md', outDir), markdown);

console.log(`RI predictor v1 feasibility: ${status}`);
