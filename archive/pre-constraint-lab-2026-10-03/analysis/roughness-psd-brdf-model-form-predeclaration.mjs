import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const target =
  'future fresh measured rough surface with paired one-dimensional height PSD and in-plane BRDF rows; exact surface must be reserved before numerical extraction';
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

const frozenModel = {
  geometry:
    'in-plane reflection; incidence and scatter angles measured from the surface normal',
  spatialFrequency:
    'abs(sin(thetaScatter) - sin(thetaIncidence)) / wavelength',
  prediction:
    'interpolate measured one-dimensional height PSD at the mapped spatial frequency',
  normalization:
    'divide predicted PSD samples and measured BRDF samples by their respective maxima over the same frozen non-specular rows',
  excludedRows:
    'specular core and any row whose mapped spatial frequency falls outside measured PSD support',
  passFail: [
    'at least five non-specular BRDF rows survive the frozen support and angular masks',
    'predicted and measured peak-side ordering agree',
    'Spearman rank correlation is at least 0.8',
    'normalized-shape mean absolute error is at most 0.20',
    'integrated normalized predicted and measured shape areas differ by at most 20 percent',
  ],
  scope:
    'shape only at one wavelength, incidence, polarization, material state, and scan direction',
  prohibitedClaims: [
    'absolute BRDF magnitude',
    'polarization transfer',
    'two-dimensional isotropic PSD reconstruction from one-dimensional data',
    'multiple scattering or deep roughness',
    'substrate-specific evidence',
  ],
};

const report = {
  source: 'roughness-psd-brdf-model-form-predeclaration.mjs',
  date: '2026-06-24',
  status: 'PSD-backed BRDF shape model form frozen before target selection',
  validationClaim: false,
  predeclaration: pre,
  frozenModel,
  nextGate:
    'screen primary measured datasets for one fresh surface with paired PSD and BRDF under matched conditions',
};

const predeclarationBlock = formatPredeclaration(pre).replace(
  '### Predeclaration (gate #1/#2)',
  '### Predeclaration (PSD-backed BRDF model form)',
);

const markdown = `# Roughness PSD/BRDF Model-Form Predeclaration

Status: **${report.status}**

${predeclarationBlock}

## Frozen Comparator

- spatial frequency: \`${frozenModel.spatialFrequency}\`
- prediction: ${frozenModel.prediction}
- normalization: ${frozenModel.normalization}
- scope: ${frozenModel.scope}

## Pass/Fail

${frozenModel.passFail.map((item) => `- ${item}`).join('\n')}

All descriptors are conventional controls. A pass can deepen the existing
roughness/interface evidence line but cannot count as substrate-specific
support.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-psd-brdf-model-form-predeclaration.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-psd-brdf-model-form-predeclaration.md', outDir),
  markdown,
);

console.log(`PSD/BRDF model-form predeclaration: ${pre.hash}`);
