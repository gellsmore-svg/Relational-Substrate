import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);
const screen = JSON.parse(
  await readFile(
    new URL('roughness-psd-brdf-source-availability-screen.json', outDir),
    'utf8',
  ),
);

const target =
  'the first source-presented Tayabaly et al. (2013) optical-flat specimen having independently measured profile PSD and surface-dominated angular BRDF, using its first source-listed wavelength and incidence with matched PSD support';
const pre = predeclare({
  target,
  modelForm: 'conventional Rayleigh-Rice PSD-backed BRDF shape comparator v0',
  descriptors: [
    'surface_height_psd_1d',
    'rayleigh_rice_spatial_frequency',
    'rayleigh_rice_brdf_shape',
  ],
  heldOut: true,
  requireConventional: true,
  conventionalComparators: [
    'surface_height_psd_1d',
    'rayleigh_rice_spatial_frequency',
    'rayleigh_rice_brdf_shape',
  ],
});

const frozenContract = {
  targetSelection:
    'use the first specimen in source presentation order that has an independently profile-measured PSD and a BRDF identified by the source as surface-dominated; skip an earlier specimen only if the source explicitly identifies bulk scatter or missing independent PSD',
  conditionSelection:
    'use that specimen first source-listed wavelength and incidence having at least five non-specular angular rows within independently measured PSD support',
  spatialFrequency:
    'abs(sin(thetaScatter) - sin(thetaIncidence)) / wavelength',
  prediction:
    'interpolate the independently measured one-dimensional profile PSD at each mapped spatial frequency',
  normalization:
    'normalize predicted PSD samples and measured BRDF samples independently by their maxima over the same surviving rows',
  masks: [
    'exclude the source-defined instrument or specular core; otherwise exclude rows within 0.1 degree of the specular direction',
    'exclude rows outside measured profile-PSD support',
    'require at least five surviving rows',
  ],
  passFail: [
    'predicted and measured peak-side ordering agree',
    'Spearman rank correlation is at least 0.8',
    'normalized-shape mean absolute error is at most 0.20',
    'normalized trapezoidal angular areas differ by at most 20 percent',
  ],
  boundary:
    'this is a conventional Rayleigh-Rice comparator; no substrate-specific evidence or automatic confidence increase is allowed',
};

const report = {
  source: 'roughness-tayabaly-brdf-target-reservation.mjs',
  date: '2026-06-24',
  status: 'Tayabaly optical-flat PSD/BRDF target reserved before full-text extraction',
  sourceCandidate: screen.selected,
  predeclaration: pre,
  frozenContract,
  blockedActions: [
    'do not choose the coated or uncoated flat based on curve agreement',
    'do not use a BRDF-derived PSD as the predictor',
    'do not fit PSD parameters to the held-out BRDF trace',
    'record source-lock failure if no first-eligible specimen exposes matched numerical curve support',
  ],
  nextGate:
    'open the full paper and source-lock the first eligible specimen identity, independent profile PSD, wavelength, incidence, angular BRDF rows, and instrument mask',
};

const predeclarationBlock = formatPredeclaration(pre).replace(
  '### Predeclaration (gate #1/#2)',
  '### Predeclaration (fresh optical-flat PSD/BRDF target)',
);

const markdown = `# Tayabaly Optical-Flat PSD/BRDF Target Reservation

Status: **${report.status}**

${predeclarationBlock}

Target selection: ${frozenContract.targetSelection}.

Condition selection: ${frozenContract.conditionSelection}.

## Pass/Fail

${frozenContract.passFail.map((item) => `- ${item}`).join('\n')}

Boundary: ${frozenContract.boundary}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-tayabaly-brdf-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-tayabaly-brdf-target-reservation.md', outDir),
  markdown,
);

console.log(`Tayabaly PSD/BRDF reservation: ${pre.hash}`);
