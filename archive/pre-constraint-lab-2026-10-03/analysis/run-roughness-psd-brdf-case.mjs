import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { basename } from 'node:path';
import { scorePsdBackedBrdfShape } from './roughness-psd-brdf-model.mjs';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('roughness-tungsten-brdf-target-reservation.json', outDir),
    'utf8',
  ),
);
const inputPath = process.argv[2];
if (!inputPath) {
  throw new Error(
    'Usage: node analysis/run-roughness-psd-brdf-case.mjs source-data.json',
  );
}
const input = JSON.parse(await readFile(inputPath, 'utf8'));
if (input.predeclarationHash !== reservation.predeclaration.hash) {
  throw new Error('Source artifact does not match the reserved tungsten target hash.');
}
if (input.geometry?.scanPlane !== 'in-plane') {
  throw new Error('Only the frozen in-plane geometry is accepted.');
}

const result = scorePsdBackedBrdfShape({
  wavelengthMeters: input.geometry.wavelengthMeters,
  incidenceAngleDegrees: input.geometry.incidenceAngleDegrees,
  specularAngleDegrees: input.geometry.specularAngleDegrees,
  specularMaskDegrees: input.geometry.specularMaskDegrees,
  psdRows: input.psd.rows,
  brdfRows: input.brdf.rows,
});
const report = {
  source: 'run-roughness-psd-brdf-case.mjs',
  date: new Date().toISOString().slice(0, 10),
  inputFile: basename(inputPath),
  predeclarationHash: input.predeclarationHash,
  sourceReference: input.source,
  provenance: input.provenance,
  result,
  evidenceBoundary:
    'conventional PSD-backed BRDF shape comparator only; no substrate-specific support',
};
await mkdir(outDir, { recursive: true });
const outputName = `roughness-psd-brdf-case-${basename(inputPath, '.json')}.json`;
await writeFile(new URL(outputName, outDir), `${JSON.stringify(report, null, 2)}\n`);
console.log(`PSD/BRDF case: ${result.status}`);
console.log(`Supported rows: ${result.rows.length}`);
console.log(`Wrote ${new URL(outputName, outDir).pathname}`);
