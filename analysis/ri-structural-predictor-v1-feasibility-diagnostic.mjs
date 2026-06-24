import { mkdir, writeFile } from 'node:fs/promises';
import {
  AE_C,
  O2_MINUS_PARAMS,
  O2_MINUS_SIO2_ANCHOR,
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

// (3) Source-anchor check for the eqn (6) oxygen model, sign-corrected to
// alpha = alpha0 * 10^(No/Van^n). Anchor is source-stated: Van(SiO2)=18.8 A^3 ->
// alpha(O2-)=1.44 A^3 (SF2016). Evaluate at the source-stated exponent (1.20) and at
// the exponent that reproduces the anchor exactly (1.0).
const { anionMolarVolume: sio2Van, expectedAlpha: sio2ExpectedAlphaO } = O2_MINUS_SIO2_ANCHOR;
const oxygenAtN12 = anionPolarizability({ ...O2_MINUS_PARAMS, nexp: 1.2, anionMolarVolume: sio2Van });
const oxygenAtN10 = anionPolarizability({ ...O2_MINUS_PARAMS, nexp: 1.0, anionMolarVolume: sio2Van });
const relErrN12 = Math.abs(oxygenAtN12 - sio2ExpectedAlphaO) / sio2ExpectedAlphaO;
const relErrN10 = Math.abs(oxygenAtN10 - sio2ExpectedAlphaO) / sio2ExpectedAlphaO;
const oxygenSignCorrect = oxygenAtN12 < O2_MINUS_PARAMS.freeIonAlpha; // compression reduces alpha
const oxygenAnchoredAtSourceExponent = relErrN12 <= 0.02; // n=1.20 as the source states

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
    check: 'eqn (6) sign correct: compression reduces O2- below free-ion (1.79)',
    pass: oxygenSignCorrect,
    value: `alpha(O2-, SiO2) = ${oxygenAtN12.toFixed(3)} < 1.79`,
  },
  {
    check: 'eqn (6) reproduces source SiO2 anchor (1.44) at the source-stated exponent n=1.20',
    pass: oxygenAnchoredAtSourceExponent,
    value: `n=1.20 -> ${oxygenAtN12.toFixed(3)} (relErr ${(relErrN12 * 100).toFixed(1)}%); n=1.0 -> ${oxygenAtN10.toFixed(3)} (relErr ${(relErrN10 * 100).toFixed(1)}%); target ${sio2ExpectedAlphaO}`,
  },
];

const machineryValid = checks[0].pass && checks[1].pass && checks[2].pass;
const oxygenAnchorPass = checks[3].pass;
const status = machineryValid
  ? oxygenAnchorPass
    ? 'v1-machinery-validated-and-oxygen-anchored'
    : 'v1-machinery-validated-oxygen-sign-fixed-exponent-residual-scoring-blocked'
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
    'Anderson-Eggleton forward/inverse and additivity are exact (round-trip ~machine epsilon). The eqn (6) oxygen model is now SIGN-CORRECTED to alpha=alpha0*10^(No/Van^n): compression correctly reduces O2- below the free-ion 1.79, and with the source-stated parameters (alpha0=1.79, No=-1.776) and the source-stated Van(SiO2)=18.8 it reproduces the source SiO2 value 1.44 EXACTLY at exponent n=1.0, while the source-stated whole-dataset exponent n=1.20 gives 1.586 (~10% high) at the same anchor. Because O2- dominates alpha_T, this n=1.0-vs-1.20 residual is disqualifying for scoring, so the model is correctly still blocked. Remaining gap is narrow and specific: reconcile the exponent (read the SF2016 oxygen-polarizability table / additional worked Van-alpha pairs to confirm whether 1.44 is an n=1.20 value at a different Van, or n=1.0 applies). The AE+additivity core is usable now; the oxygen term is one reconciliation away.',
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
