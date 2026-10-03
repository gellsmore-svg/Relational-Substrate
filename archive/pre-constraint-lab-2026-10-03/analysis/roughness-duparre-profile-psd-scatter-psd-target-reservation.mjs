import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { formatPredeclaration, predeclare } from './predeclaration-gate.mjs';

// Fresh target reservation for the profile-PSD versus scatter-derived-PSD
// comparator v0 (model-form predeclaration hash ad3892b700d0b82f). Reserves the
// Duparre et al. (2002) round-robin selected by the metadata source screen,
// freezing a source-ORDER selection rule before any numerical lookup so the
// sample and instrument are not chosen on agreement with the comparator.
//
// Only the abstract and index metadata have been seen at reservation time. The
// scattering wavelength, sample list, and curve values are NOT yet known and are
// resolved at the later full-text source-lock gate.

const outDir = new URL('./out/', import.meta.url);

const screen = JSON.parse(
  await readFile(
    new URL('roughness-profile-psd-scatter-psd-source-screen.json', outDir),
    'utf8',
  ),
);
const modelForm = JSON.parse(
  await readFile(
    new URL('roughness-profile-psd-scatter-psd-predeclaration.json', outDir),
    'utf8',
  ),
);

const target =
  'the first sample in Duparre et al. (2002, Applied Optics 41, 154-171) source-presentation order whose results expose both an independently measured topography PSD and an angle-resolved-scattering-derived PSD over a shared spatial-frequency overlap band, using the source-stated scattering wavelength and geometry';
const pre = predeclare({
  target,
  modelForm: 'conventional independent-profile-PSD versus BRDF-derived-PSD shape comparator v0',
  descriptors: ['surface_height_psd_1d', 'brdf_derived_surface_psd_1d'],
  heldOut: true,
  requireConventional: true,
  conventionalComparators: ['surface_height_psd_1d', 'brdf_derived_surface_psd_1d'],
});

const frozenContract = {
  servesModelFormHash: modelForm.predeclaration.hash,
  topographyInstrumentPrecedence: [
    'atomic force microscope',
    'mechanical profiler (Talystep)',
    'confocal laser scanning microscope',
  ],
  sampleSelection:
    'use the first sample in source presentation order whose results expose both (a) an independently measured topography PSD and (b) an angle-resolved-scattering-derived PSD; skip an earlier sample only if the source does not expose both PSD classes for it or the two do not share an overlap band',
  instrumentSelection:
    'take the independent topography PSD from the first instrument present for that sample in the frozen precedence (AFM, then mechanical profiler, then confocal); the comparison curve is the angle-resolved-scattering-derived PSD',
  conditionSelection:
    'use the source-stated scattering wavelength and geometry for that sample angle-resolved-scattering PSD',
  observable:
    'compare the independent topography PSD with the angle-resolved-scattering-derived PSD directly in spatial-frequency space; shape only, never raw BRDF or absolute magnitude',
  support:
    'use only scattering-PSD rows inside the independent topography PSD support and outside every source-defined instrument, validity, or band-limit exclusion; never extrapolate',
  interpolation:
    'log-log interpolate the independent topography PSD at each surviving scattering-PSD frequency',
  normalization:
    'subtract each curve median log10 over the identical surviving rows',
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
  boundary:
    'conventional shape comparator only; no substrate-specific evidence and no automatic confidence increase',
};

const report = {
  source: 'roughness-duparre-profile-psd-scatter-psd-target-reservation.mjs',
  date: '2026-06-24',
  status: 'Duparre 2002 profile-PSD versus scatter-PSD target reserved before full-text extraction',
  validationClaim: false,
  evidenceStatus: 'none; reservation only, no curve values inspected',
  sourceCandidate: screen.selected,
  predeclaration: pre,
  frozenContract,
  blockedActions: [
    'do not choose the sample or topography instrument based on curve agreement',
    'do not use a jointly inverted single PSD as either curve',
    'do not treat the angle-resolved-scattering-derived PSD as the independent topography PSD',
    'record source-lock failure if the first eligible sample does not expose at least eight matched rows over at least 0.5 decade or the scattering wavelength is not stated',
  ],
  nextGate:
    'open the full Duparre et al. (2002) paper and source-lock the first eligible sample identity, its independent topography PSD instrument and curve, the angle-resolved-scattering-derived PSD, the scattering wavelength and geometry, and the shared overlap band, before extracting any numerical PSD rows; build the scoring case runner enforcing this reservation hash at that point',
};

const predeclarationBlock = formatPredeclaration(pre).replace(
  '### Predeclaration (gate #1/#2)',
  '### Predeclaration (fresh profile-PSD versus scatter-PSD target)',
);

const markdown = `# Duparre 2002 Profile-PSD versus Scatter-PSD Target Reservation

Status: **${report.status}**

Serves model form: \`${frozenContract.servesModelFormHash}\`.

${predeclarationBlock}

Sample selection: ${frozenContract.sampleSelection}.

Instrument selection: ${frozenContract.instrumentSelection}.

Condition selection: ${frozenContract.conditionSelection}.

## Pass/Fail

${frozenContract.passFail.map((item) => `- ${item}`).join('\n')}

Boundary: ${frozenContract.boundary}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-duparre-profile-psd-scatter-psd-target-reservation.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-duparre-profile-psd-scatter-psd-target-reservation.md', outDir),
  markdown,
);

console.log(`Duparre profile/scatter PSD reservation: ${pre.hash}`);
