import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const target =
  'the first-listed tungsten specimen in Le Bohec et al. (2024), using one paired measured surface PSD and in-plane BRDF condition from the same specimen';
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
    'use the first tungsten specimen in source presentation order, independent of roughness or BRDF performance',
  conditionSelection:
    'use the first source-reported visible-wavelength in-plane BRDF condition for that specimen that has matching PSD support',
  spatialFrequency:
    'abs(sin(thetaScatter) - sin(thetaIncidence)) / wavelength',
  prediction:
    'interpolate the same-specimen one-dimensional PSD at each mapped spatial frequency',
  normalization:
    'normalize predicted PSD samples and measured BRDF samples independently by their maxima over the frozen surviving rows',
  masks: [
    'exclude the source-defined specular core or, if absent, rows within 0.1 degree of the specular direction',
    'exclude rows outside measured PSD spatial-frequency support',
    'require at least five surviving rows',
  ],
  passFail: [
    'predicted and measured peak-side ordering agree',
    'Spearman rank correlation is at least 0.8',
    'normalized-shape mean absolute error is at most 0.20',
    'normalized trapezoidal angular areas differ by at most 20 percent',
  ],
  boundary:
    'all terms are conventional optical comparators; no global confidence increase is automatic and no substrate-specific support is claimed',
};

const report = {
  source: 'roughness-tungsten-brdf-target-reservation.mjs',
  date: '2026-06-24',
  status: 'first-listed tungsten BRDF/PSD target reserved before numerical extraction',
  sourceCandidate: {
    citation:
      'M. Le Bohec et al., Relationship between topographic parameters and BRDF for tungsten surfaces in the visible spectrum, Optik 303, 171750 (2024)',
    doi: '10.1016/j.ijleo.2024.171750',
    metadataBasis:
      'abstract confirms several tungsten samples, measured BRDF, three-dimensional topography, and PSD extraction',
  },
  predeclaration: pre,
  frozenContract,
  blockedActions: [
    'do not select the smoothest, best-fitting, or most complete sample after opening the paper',
    'do not fit PSD parameters to the BRDF target',
    'do not use BRDF-derived PSD as an independent predictor',
    'record source-lock failure if paired numeric curves cannot be extracted under the frozen rule',
  ],
  nextGate:
    'open the full paper and source-lock the first-listed specimen, first eligible BRDF condition, PSD support, and numerical rows',
};

const predeclarationBlock = formatPredeclaration(pre).replace(
  '### Predeclaration (gate #1/#2)',
  '### Predeclaration (fresh tungsten PSD/BRDF target)',
);

const markdown = `# Tungsten PSD/BRDF Target Reservation

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
  new URL('roughness-tungsten-brdf-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-tungsten-brdf-target-reservation.md', outDir),
  markdown,
);

console.log(`Tungsten PSD/BRDF reservation: ${pre.hash}`);
