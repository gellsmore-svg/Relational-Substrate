import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, digits = 4) {
  return Number(value.toFixed(digits));
}

function pctError(model, external) {
  return ((model - external) / external) * 100;
}

function evaluateBarrier(modelCm1, externalCm1) {
  const errorPct = pctError(modelCm1, externalCm1);
  return {
    regime: externalCm1 > 700 ? 'large barrier' : externalCm1 >= 250 ? 'small barrier' : 'free-rotor diagnostic',
    pass: externalCm1 > 700 ? Math.abs(errorPct) <= 35 : externalCm1 >= 250 ? modelCm1 >= externalCm1 * 0.5 && modelCm1 <= externalCm1 * 2 : null,
    errorPct: round(errorPct, 2),
    absoluteErrorPct: round(Math.abs(errorPct), 2),
  };
}

function rowFor(result, angle, label, externalCm1) {
  const model = result.frozenRows.find((entry) => entry.angle === angle);
  return {
    sideAngle: result.sideAngle,
    label,
    angle,
    modelCm1: model.modelCm1,
    modelTopology: model.topology,
    externalCm1,
    ...evaluateBarrier(model.modelCm1, externalCm1),
  };
}

function bracketComparison(result, external) {
  const rows = [
    rowFor(result, 0, 'cis', external.barriers.cis),
    rowFor(result, 180, 'trans-grid', external.barriers.trans),
  ];
  const nearestMaximum = result.topology.nearestTransPathMaximum;
  const nearestMaximumErrorPct = pctError(nearestMaximum.modelCm1, external.barriers.trans);
  const topologyPass = !result.topology.spuriousTransLocalMinimum;
  const barrierPass = rows.every((row) => row.pass !== false);
  return {
    sideAngle: result.sideAngle,
    modelMinimum: result.modelPredictedMinimum,
    comparisonRows: rows,
    nearestTransPathMaximum: {
      ...nearestMaximum,
      externalTransCm1: external.barriers.trans,
      errorPct: round(nearestMaximumErrorPct, 2),
      absoluteErrorPct: round(Math.abs(nearestMaximumErrorPct), 2),
    },
    topologyPass,
    barrierPass,
    pass: topologyPass && barrierPass,
  };
}

function markdownRows(rows) {
  const header = '| side angle | barrier | grid angle | model cm-1 | external cm-1 | model topology | error % | pass |';
  const rule = '|---:|---|---:|---:|---:|---|---:|---|';
  const body = rows.map((row) => `| ${row.sideAngle} | ${row.label} | ${row.angle} | ${row.modelCm1} | ${row.externalCm1} | ${row.modelTopology} | ${row.errorPct} | ${row.pass === null ? 'diagnostic' : row.pass ? 'yes' : 'no'} |`);
  return [header, rule, ...body].join('\n');
}

function topologyRows(comparisons) {
  const header = '| side angle | trans topology | nearest model max angle | nearest model max cm-1 | external trans cm-1 | nearest max error % | topology pass |';
  const rule = '|---:|---|---:|---:|---:|---:|---|';
  const body = comparisons.map((comparison) => `| ${comparison.sideAngle} | ${comparison.comparisonRows.find((row) => row.label === 'trans-grid').modelTopology} | ${comparison.nearestTransPathMaximum.angle} | ${comparison.nearestTransPathMaximum.modelCm1} | ${comparison.nearestTransPathMaximum.externalTransCm1} | ${comparison.nearestTransPathMaximum.errorPct} | ${comparison.topologyPass ? 'yes' : 'no'} |`);
  return [header, rule, ...body].join('\n');
}

async function main() {
  const prelookup = JSON.parse(await readFile(new URL('selenane-heteroatom-rotor-prelookup.json', outDir), 'utf8'));
  const external = {
    source: {
      label: 'N. Sahu, J. O. Richardson, and R. Berger, Instanton calculations of tunneling splittings in chiral molecules, Journal of Computational Chemistry 42(4), 210-221 (2021).',
      doi: '10.1002/jcc.26447',
      url: 'https://doi.org/10.1002/jcc.26447',
      note: 'Table 1 reports H2Se2 cis-barrier height 2264.8 cm-1 and trans-barrier height 1664.2 cm-1 at MP2/aug-cc-pVTZ.',
    },
    barriers: {
      cis: 2264.8,
      trans: 1664.2,
    },
    topology: 'C2 symmetric H2X2 enantiomer interconversion with cis and trans barrier pathways; trans is a barrier pathway, not a local minimum.',
  };
  const comparisons = prelookup.bracketResults.map((result) => bracketComparison(result, external));
  const allRows = comparisons.flatMap((comparison) => comparison.comparisonRows);
  const topologyPass = comparisons.every((comparison) => comparison.topologyPass);
  const barrierPass = comparisons.every((comparison) => comparison.barrierPass);
  const overallPass = topologyPass && barrierPass;
  const status = overallPass ? 'pass' : 'fail';
  const repeatedDisulfanePattern = comparisons.every((comparison) => !comparison.topologyPass);

  const payload = {
    status,
    source: 'selenane-heteroatom-rotor-comparison.mjs',
    target: 'selenane H-Se-Se-H',
    external: {
      source: external.source,
      topology: external.topology,
    },
    lockedPrelookupFile: 'analysis/out/selenane-heteroatom-rotor-prelookup.json',
    noRetune: true,
    score: 0,
    checks: [
      {
        id: 'cis-barrier-bracket',
        pass: comparisons.every((comparison) => comparison.comparisonRows.find((row) => row.label === 'cis').pass),
        reading: 'Cis barrier magnitude must pass for all bracket angles.',
      },
      {
        id: 'trans-grid-barrier-bracket',
        pass: comparisons.every((comparison) => comparison.comparisonRows.find((row) => row.label === 'trans-grid').pass),
        reading: 'The 180 degree grid value must pass the trans barrier magnitude for all bracket angles.',
      },
      {
        id: 'trans-topology-bracket',
        pass: topologyPass,
        reading: 'No bracket angle may predict a spurious local minimum at trans when the source reports a trans barrier pathway.',
      },
      {
        id: 'robustness-bracket',
        pass: overallPass,
        reading: 'Overall pass requires all bracket angles to pass topology and barrier rules.',
      },
    ],
    confidenceEffect:
      'adds a second heavier same-family chalcogen trans-side topology failure under held constants; this is suggestive systematic torsion-transfer failure, not calibration',
    repeatedDisulfanePattern,
    comparisons,
  };

  const md = `# H-Se-Se-H Heteroatom Rotor Locked Comparison

Status: ${status}

No model constants, geometry inputs, charge rules, angle grid, source tables, scoring terms, or reference-state rules were changed after the prelookup output.

## Source

${external.source.label}

- DOI: ${external.source.doi}
- URL: ${external.source.url}
- reported comparison values used here: cis barrier ${external.barriers.cis} cm-1, trans barrier ${external.barriers.trans} cm-1
- topology reading: ${external.topology}

## Barrier Comparison

${markdownRows(allRows)}

## Trans-Side Topology

${topologyRows(comparisons)}

## Verdict

The H-Se-Se-H same-topology transfer ${overallPass ? 'passes' : 'fails'} the locked criteria.

Failure mode: ${
    overallPass
      ? 'none'
      : 'repeated trans-side topology mismatch across the full bent-angle bracket: the model predicts a spurious local minimum at 180 degrees where the external source reports a trans barrier pathway.'
  }

Interpretation: ${
    repeatedDisulfanePattern
      ? 'This repeats the disulfane topology failure under held constants. Two heavier same-family chalcogen rows now show the same trans-side topology failure; this is suggestive systematic failure, not a conclusive final verdict.'
      : 'The result does not uniformly repeat the disulfane topology failure across the bracket.'
  }
`;

  await mkdir(outDir, { recursive: true });
  await writeFile(new URL('selenane-heteroatom-rotor-comparison.json', outDir), `${JSON.stringify(payload, null, 2)}\n`);
  await writeFile(new URL('selenane-heteroatom-rotor-comparison.md', outDir), md);
  console.log(md);
}

await main();
