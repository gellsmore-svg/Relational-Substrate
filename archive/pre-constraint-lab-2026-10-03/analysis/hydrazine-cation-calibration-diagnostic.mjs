import { readFile, writeFile, mkdir } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

const source = await readJson('external-hydrazine-cation-torsion-benchmark.json');
const rows = source.rows;

const row0 = rows.find((row) => row.angle === 0);
const row90 = rows.find((row) => row.angle === 90);
const row180 = rows.find((row) => row.angle === 180);

const nonzeroRows = [row0, row180];
const bestSingleMultiplier =
  nonzeroRows.reduce((sum, row) => sum + row.modelCm1 * row.externalCm1, 0) /
  nonzeroRows.reduce((sum, row) => sum + row.modelCm1 ** 2, 0);

const globalScaleFor180 = row180.externalCm1 / row180.modelCm1;
const cationCrowdingBoostCm1 = (row0.externalCm1 - row0.modelCm1 * globalScaleFor180) / row0.cisCrowding;

function modelRow(row, mode) {
  let cm1;
  if (mode === 'current') {
    cm1 = row.modelCm1;
  } else if (mode === 'bestSingle') {
    cm1 = row.modelCm1 * bestSingleMultiplier;
  } else if (mode === 'twoParameter') {
    cm1 = row.modelCm1 * globalScaleFor180 + row.cisCrowding * cationCrowdingBoostCm1;
  } else if (mode === 'shapeOnly') {
    cm1 = row.modelCm1 + row.cisCrowding * ((row0.externalCm1 - row0.modelCm1) / row0.cisCrowding);
  } else {
    throw new Error(`Unknown mode ${mode}`);
  }
  const errorPct = row.externalCm1 === 0 ? 0 : ((cm1 - row.externalCm1) / row.externalCm1) * 100;
  return {
    angle: row.angle,
    externalCm1: row.externalCm1,
    modelCm1: round(cm1, 2),
    errorPct: round(errorPct, 2),
  };
}

const modes = ['current', 'bestSingle', 'shapeOnly', 'twoParameter'];
const diagnostics = Object.fromEntries(
  modes.map((mode) => [mode, rows.map((row) => modelRow(row, mode))])
);

const report = `# Hydrazine Cation Calibration Diagnostic

## Status

This is a side diagnostic only. It is not fed into benchmark scoring, model state, or milestone confidence.

Claude review classified the two-parameter repair as calibration interpolation. It may be printed once to decompose the miss, but it must not be promoted.

## Coefficients Implied By Exposed Hydrazine

| Quantity | Value |
|---|---:|
| Best single multiplier | ${round(bestSingleMultiplier, 4)} |
| Global scale required by 180 degree row | ${round(globalScaleFor180, 4)} |
| Cation crowding boost implied after 180 scale | ${round(cationCrowdingBoostCm1, 2)} cm-1 per cisCrowding unit |
| 0 degree cisCrowding | ${row0.cisCrowding} |
| 180 degree cisCrowding | ${row180.cisCrowding} |

## Comparison

| Mode | Angle | External cm-1 | Model cm-1 | Error |
|---|---:|---:|---:|---:|
${modes.flatMap((mode) =>
  diagnostics[mode].map((row) =>
    `| ${mode === 'twoParameter' ? 'twoParameter calibration interpolation' : mode} | ${row.angle} | ${row.externalCm1} | ${row.modelCm1} | ${row.errorPct}% |`
  )
).join('\n')}

## Reading

The decomposition confirms the absolute miss is mostly global for the cation: the 180 degree row, where cisCrowding is zero, still needs a ${round(globalScaleFor180, 4)}x multiplier. A shape-only crowding patch can force the 0 degree barrier but cannot repair the 180 degree barrier. A two-parameter repair exactly interpolates both nonzero exposed barriers and is therefore calibration interpolation, not validation.

Next clean step: predeclare hydroxylamine as the primary fresh torsion target and neutral hydrazine as a paired confirmatory target, with no coefficient changes before execution.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('hydrazine-cation-calibration-diagnostic.md', outDir), report);
console.log(report);
