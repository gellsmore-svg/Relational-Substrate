import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

function pctError(model, external) {
  return ((model - external) / external) * 100;
}

function barrierRegime(externalCm1) {
  if (externalCm1 < 250) {
    return {
      regime: 'free-rotor diagnostic',
      pass: null,
      rule: 'external barrier < 250 cm-1: diagnostic only',
    };
  }
  if (externalCm1 <= 700) {
    return {
      regime: 'small barrier',
      pass: null,
      rule: '250-700 cm-1: predicted barrier must lie within [0.5x, 2x] external',
    };
  }
  return {
    regime: 'large barrier',
    pass: null,
    rule: '>700 cm-1: absolute percent error <= 35 percent',
  };
}

function evaluateBarrier(modelCm1, externalCm1) {
  const regime = barrierRegime(externalCm1);
  const errorPct = pctError(modelCm1, externalCm1);
  let pass = null;
  if (regime.regime === 'small barrier') {
    pass = modelCm1 >= externalCm1 * 0.5 && modelCm1 <= externalCm1 * 2;
  } else if (regime.regime === 'large barrier') {
    pass = Math.abs(errorPct) <= 35;
  }

  return {
    ...regime,
    pass,
    errorPct: round(errorPct, 2),
    absoluteErrorPct: round(Math.abs(errorPct), 2),
  };
}

function rowFor(prelookup, angle, externalLabel, externalCm1) {
  const model = prelookup.frozenRows.find((entry) => entry.angle === angle);
  const evaluation = evaluateBarrier(model.modelCm1, externalCm1);
  return {
    label: externalLabel,
    angle,
    modelCm1: model.modelCm1,
    externalCm1,
    ...evaluation,
  };
}

function markdownRows(rows) {
  const header = '| barrier | angle | model cm-1 | external cm-1 | error % | rule | pass |';
  const rule = '|---|---:|---:|---:|---:|---|---|';
  const body = rows.map((row) => `| ${row.label} | ${row.angle} | ${row.modelCm1} | ${row.externalCm1} | ${row.errorPct} | ${row.regime} | ${row.pass === null ? 'diagnostic' : row.pass ? 'yes' : 'no'} |`);
  return [header, rule, ...body].join('\n');
}

async function main() {
  const prelookup = JSON.parse(await readFile(new URL('disulfane-heteroatom-rotor-prelookup.json', outDir), 'utf8'));
  const external = {
    source: {
      label: 'J. Koput, An ab initio study on the equilibrium structure and torsional potential energy function of disulfane, Chemical Physics Letters 259 (1996) 146-150.',
      doi: '10.1016/0009-2614(96)00714-2',
      url: 'https://www.sciencedirect.com/science/article/pii/0009261496007142',
      note: 'ScienceDirect abstract reports cc-pVQZ equilibrium HSSH torsion 90.66 degrees, Vtrans = 1958 cm-1, and Vcis = 2714 cm-1.',
    },
    minimumAngle: 90.66,
    barriers: [
      { label: 'cis', angle: 0, cm1: 2714 },
      { label: 'trans', angle: 180, cm1: 1958 },
    ],
  };

  const comparisonRows = [
    rowFor(prelookup, 0, 'cis', 2714),
    rowFor(prelookup, 180, 'trans', 1958),
  ];
  const transPathRows = prelookup.frozenRows.filter((row) => row.angle >= 90 && row.angle <= 180);
  const transPathMaximum = transPathRows.reduce((best, row) => (row.modelCm1 > best.modelCm1 ? row : best), transPathRows[0]);
  const transPathMaximumErrorPct = pctError(transPathMaximum.modelCm1, 1958);
  const modelMinimum = prelookup.referenceStateRule.modelPredictedMinimum;
  const minimumErrorDegrees = Math.abs(modelMinimum - external.minimumAngle);
  const minimumPass = minimumErrorDegrees <= 30;
  const gridPointComparison =
    comparisonRows.find((row) => row.label === 'cis').modelCm1 >
    comparisonRows.find((row) => row.label === 'trans').modelCm1;
  const barrierPass = comparisonRows.every((row) => row.pass !== false);
  const topologyPass = false;
  const overallPass = minimumPass && topologyPass && barrierPass;
  const status = overallPass ? 'pass' : 'fail';
  const failureMode = overallPass
    ? 'none'
    : 'topological mismatch on the trans side: model predicts a spurious local minimum at 180 degrees where the external surface has a planar maximum.';

  const payload = {
    status,
    source: 'disulfane-heteroatom-rotor-comparison.mjs',
    target: 'disulfane H-S-S-H',
    external: {
      source: external.source,
    },
    lockedPrelookupFile: 'analysis/out/disulfane-heteroatom-rotor-prelookup.json',
    noRetune: true,
    score: 0.5,
    checks: [
      {
        id: 'minimum-location',
        pass: minimumPass,
        reading: 'Model minimum is within 30 degrees of the external minimum.',
      },
      {
        id: 'cis-barrier',
        pass: comparisonRows.find((row) => row.label === 'cis').pass,
        reading: 'Cis-side barrier magnitude passes the large-barrier tolerance.',
      },
      {
        id: 'trans-grid-barrier',
        pass: comparisonRows.find((row) => row.label === 'trans').pass,
        reading: 'The 180 degree grid value is far below the external trans barrier.',
      },
      {
        id: 'trans-topology',
        pass: topologyPass,
        reading: 'Model predicts a spurious trans local minimum rather than a planar trans maximum.',
      },
    ],
    confidenceEffect:
      'reduces torsion evidence-line confidence: the one fresh fully predeclared same-topology rotor transfers minimum and cis-side magnitude but fails trans-side topology and magnitude',
    modelMinimum,
    externalMinimum: external.minimumAngle,
    minimumErrorDegrees: round(minimumErrorDegrees, 2),
    minimumPass,
    gridPointComparison,
    topologyPass,
    transPathMaximum: {
      angle: transPathMaximum.angle,
      modelCm1: transPathMaximum.modelCm1,
      externalTransCm1: 1958,
      errorPct: round(transPathMaximumErrorPct, 2),
      absoluteErrorPct: round(Math.abs(transPathMaximumErrorPct), 2),
    },
    barrierPass,
    overallPass,
    failureMode,
    comparisonRows,
  };

  const md = `# Disulfane Heteroatom Rotor Locked Comparison

Status: ${status}

No model constants, geometry inputs, charge rules, angle grid, source tables, or scoring terms were changed after the prelookup output.

## Source

${external.source.label}

- DOI: ${external.source.doi}
- URL: ${external.source.url}
- reported comparison values used here: equilibrium torsion ${external.minimumAngle} degrees, trans barrier ${external.barriers[1].cm1} cm-1, cis barrier ${external.barriers[0].cm1} cm-1

## Minimum Location

- model minimum: ${modelMinimum} degrees
- external minimum: ${external.minimumAngle} degrees
- error: ${round(minimumErrorDegrees, 2)} degrees
- pass rule: within 30 degrees
- pass: ${minimumPass ? 'yes' : 'no'}

## Barrier Comparison

${markdownRows(comparisonRows)}

## Trans-Side Topology

- grid-point comparison: model value at 0 degrees is greater than model value at 180 degrees
- interpretation: this is not counted as an ordering pass, because the model predicts a spurious local minimum at 180 degrees
- nearest model maximum on the skew-to-trans path: ${transPathMaximum.modelCm1} cm-1 at ${transPathMaximum.angle} degrees
- external trans barrier: ${external.barriers[1].cm1} cm-1 at 180 degrees
- nearest-maximum error: ${round(transPathMaximumErrorPct, 2)} percent
- topology pass: no

## Verdict

${overallPass ? 'The disulfane same-topology transfer passes the locked criteria.' : 'The disulfane same-topology transfer fails the locked criteria.'}

Failure mode: ${failureMode}

Interpretation: the minimum location and cis-side barrier transfer, but the trans side fails both topology and magnitude. The model places a shallow local minimum at trans where the external surface has a large planar barrier. Under the no-retune lockbox, this is recorded as a fresh validation failure, not a calibration opportunity.
`;

  await mkdir(outDir, { recursive: true });
  await writeFile(new URL('disulfane-heteroatom-rotor-comparison.json', outDir), `${JSON.stringify(payload, null, 2)}\n`);
  await writeFile(new URL('disulfane-heteroatom-rotor-comparison.md', outDir), md);
  console.log(md);
}

await main();
