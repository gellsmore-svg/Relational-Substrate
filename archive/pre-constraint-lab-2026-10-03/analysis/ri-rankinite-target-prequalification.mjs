import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const target = {
  material: 'rankinite',
  formula: 'Ca3Si2O7',
  topologyClass: 'rankinite-like Ca sorosilicate',
  role: 'reserved Ca-scaffold transfer target; not scored',
  reasonSelected:
    'Ca-rich sorosilicate with no Mg/Al/Zn T1 chemistry; tests whether the melilite Ca-scaffold baseline transfers outside melilite topology.',
  handbookSource: {
    url: 'https://handbookofmineralogy.org/pdfs/rankinite.pdf',
    densityMeasuredRange: [2.96, 3.0],
    densityCalculatedRange: [2.99, 3.0],
    opticalClass: 'biaxial (+)',
    alphaRange: [1.64, 1.643],
    betaRange: [1.643, 1.646],
    gammaRange: [1.65, 1.652],
    references:
      'Tilley 1942; Black 1969; Saburi et al. 1976; Deer, Howie, and Zussman 1986, as listed in the Handbook entry.',
  },
  secondarySource: {
    url: 'https://webmineral.com/data/Rankinite.shtml',
    status: 'secondary cross-check; lists same formula and links Handbook/RRUFF/Mindat source network',
  },
};

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function midpoint([min, max]) {
  return (min + max) / 2;
}

function biaxialScalar(alpha, beta, gamma) {
  return (alpha + beta + gamma) / 3;
}

function llFromN(n) {
  return (n ** 2 - 1) / (n ** 2 + 2);
}

const scalarMin = biaxialScalar(
  target.handbookSource.alphaRange[0],
  target.handbookSource.betaRange[0],
  target.handbookSource.gammaRange[0]
);
const scalarMax = biaxialScalar(
  target.handbookSource.alphaRange[1],
  target.handbookSource.betaRange[1],
  target.handbookSource.gammaRange[1]
);
const scalarMid = biaxialScalar(
  midpoint(target.handbookSource.alphaRange),
  midpoint(target.handbookSource.betaRange),
  midpoint(target.handbookSource.gammaRange)
);

const sourceQualification = {
  formula: 'Ca3Si2O7',
  densityForFutureScoring: round(midpoint(target.handbookSource.densityMeasuredRange)),
  densityPolicy: 'use measured-density midpoint unless a sample-specific density is found before scoring',
  scalarRiRange: [round(scalarMin), round(scalarMax)],
  scalarRiMidpoint: round(scalarMid),
  scalarPolicy: 'biaxial scalar target = (alpha + beta + gamma) / 3',
  lorentzLorenzScalarMidpoint: round(llFromN(scalarMid), 8),
  status: 'source-qualified reserved target; not scored',
};

const contractFit = {
  frozenContract: 'Ca scaffold baseline + T1 high-field + T1 d10 buffer + topology gate',
  targetClass: 'rankinite-like Ca silicate',
  expectedUse:
    'Tests non-melilite Ca scaffold transfer. It should not be treated as melilite model validation because topology changes.',
  falsifier:
    'If melilite Ca-scaffold baseline predicts rankinite accurately without topology adjustment, the topology-gated Ca-scaffold interpretation weakens.',
  nonFalsifier:
    'If rankinite fails under a melilite Ca-scaffold baseline, that supports topology gating but does not by itself calibrate the corrected model.',
};

const report = {
  source: 'ri-rankinite-target-prequalification.mjs',
  status: 'prequalification only; no prediction made',
  target,
  sourceQualification,
  contractFit,
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Rankinite Target Prequalification

## Scope

This is a source-qualification record only. It reserves rankinite as the next Ca-scaffold transfer target under the frozen T1-buffer contract. It does not score rankinite and does not change any model coefficients.

## Target

${table(
  ['Field', 'Value'],
  [
    ['Material', target.material],
    ['Formula', target.formula],
    ['Topology class', target.topologyClass],
    ['Role', target.role],
    ['Reason selected', target.reasonSelected],
  ]
)}

## Source Qualification

Primary source: ${target.handbookSource.url}

Secondary cross-check: ${target.secondarySource.url}

${table(
  ['Property', 'Value', 'Policy / reading'],
  [
    ['D(meas.)', target.handbookSource.densityMeasuredRange.join('-'), sourceQualification.densityPolicy],
    ['D(calc.)', target.handbookSource.densityCalculatedRange.join('-'), 'record only'],
    ['Optical class', target.handbookSource.opticalClass, 'biaxial scalar target allowed'],
    ['alpha', target.handbookSource.alphaRange.join('-'), 'Handbook range'],
    ['beta', target.handbookSource.betaRange.join('-'), 'Handbook range'],
    ['gamma', target.handbookSource.gammaRange.join('-'), 'Handbook range'],
    ['Scalar RI range', sourceQualification.scalarRiRange.join('-'), sourceQualification.scalarPolicy],
    ['Scalar RI midpoint', sourceQualification.scalarRiMidpoint, 'reserved target value for future scoring only'],
    ['Lorentz-Lorenz midpoint', sourceQualification.lorentzLorenzScalarMidpoint, 'reserved LL target value for future scoring only'],
  ]
)}

## Contract Fit

${table(
  ['Item', 'Reading'],
  [
    ['Frozen contract', contractFit.frozenContract],
    ['Target class', contractFit.targetClass],
    ['Expected use', contractFit.expectedUse],
    ['Falsifier', contractFit.falsifier],
    ['Non-falsifier', contractFit.nonFalsifier],
  ]
)}

## Decision

Rankinite is source-qualified as the next reserved target class if a melilite same-class repeat cannot be found first. It is clean for Ca-rich scaffold transfer because it removes Mg/Al/Zn T1 chemistry, but it changes topology. Use it to test topology-gated Ca scaffold transfer, not to validate a melilite-specific T1-buffer model.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-rankinite-target-prequalification.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-rankinite-target-prequalification.md', outDir), markdown);

console.log(markdown);
