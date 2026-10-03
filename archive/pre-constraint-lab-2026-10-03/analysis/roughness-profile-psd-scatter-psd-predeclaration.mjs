import { mkdir, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

const outDir = new URL('./out/', import.meta.url);

const target =
  'future fresh smooth optical surface with an independently measured one-dimensional profile PSD and a same-state BRDF-derived PSDscatter curve; exact surface must be reserved before numerical extraction';
const pre = predeclare({
  target,
  modelForm:
    'conventional independent-profile-PSD versus BRDF-derived-PSD shape comparator v0',
  descriptors: ['surface_height_psd_1d', 'brdf_derived_surface_psd_1d'],
  heldOut: true,
  requireConventional: true,
});

const frozenModel = {
  observable:
    'compare independent topography PSD with source-derived PSDscatter directly in spatial-frequency space',
  support:
    'use only PSDscatter rows inside the independently measured PSD support and outside every source-defined instrument, specular, or validity exclusion; never extrapolate',
  interpolation:
    'log-log interpolate the independent profile PSD at each surviving PSDscatter frequency',
  normalization:
    'subtract each curve median log10 PSD over the identical surviving rows, preserving frequency-dependent shape while removing one constant vertical scale offset',
  minimumData: [
    'at least eight surviving matched frequency rows',
    'surviving rows span at least 0.5 decade in spatial frequency',
  ],
  passFail: [
    'Spearman rank correlation is at least 0.8',
    'median-centered log10-shape mean absolute error is at most 0.25 dex',
    '90th-percentile absolute centered log10 residual is at most 0.60 dex',
    'adjacent log-log slope signs agree for at least 80 percent of intervals',
  ],
  scope:
    'shape only for one surface state, wavelength, incidence, polarization treatment, scan convention, and BRDF-to-PSD conversion',
  prohibitedClaims: [
    'raw angular BRDF prediction',
    'absolute BRDF or PSD magnitude',
    'validity inside the source instrument-signature region',
    'multiple scattering or deep-roughness transfer',
    'substrate-specific evidence',
  ],
  exposedCasePolicy:
    'Tayabaly silicon-wafer figures were inspected before this model form was frozen and may be used only as implementation feasibility, never fresh validation',
};

const report = {
  source: 'roughness-profile-psd-scatter-psd-predeclaration.mjs',
  date: '2026-06-24',
  status: 'profile-PSD versus scatter-derived-PSD model form frozen',
  validationClaim: false,
  predeclaration: pre,
  frozenModel,
  nextGate:
    'implement synthetic known-answer checks, then screen metadata for a fresh paired surface before numerical target lookup',
};

const predeclarationBlock = formatPredeclaration(pre).replace(
  '### Predeclaration (gate #1/#2)',
  '### Predeclaration (profile PSD versus scatter-derived PSD)',
);

const markdown = `# Profile PSD versus Scatter-Derived PSD Predeclaration

Status: **${report.status}**

${predeclarationBlock}

## Frozen Comparator

- observable: ${frozenModel.observable}
- support: ${frozenModel.support}
- interpolation: ${frozenModel.interpolation}
- normalization: ${frozenModel.normalization}

## Minimum Data

${frozenModel.minimumData.map((item) => `- ${item}`).join('\n')}

## Pass/Fail

${frozenModel.passFail.map((item) => `- ${item}`).join('\n')}

Exposed-case policy: ${frozenModel.exposedCasePolicy}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-profile-psd-scatter-psd-predeclaration.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-profile-psd-scatter-psd-predeclaration.md', outDir),
  markdown,
);

console.log(`Profile/scatter PSD predeclaration: ${pre.hash}`);
