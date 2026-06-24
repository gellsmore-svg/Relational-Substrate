import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('roughness-tayabaly-brdf-target-reservation.json', outDir),
    'utf8',
  ),
);

const sources = [
  {
    role: 'primary conference paper',
    citation:
      'K. Tayabaly, J. C. Stover, R. E. Parks, M. Dubin, and J. H. Burge, Use of the surface PSD and incident angle adjustments to investigate near specular scatter from smooth surfaces, Proc. SPIE 8838, 883805 (2013)',
    doi: '10.1117/12.2024612',
    fullTextLocation:
      'author-uploaded full text indexed at ResearchGate; 10 pages inspected',
    accessResult:
      'text, equations, captions, and page-level figures are accessible through the indexed PDF',
  },
];

const lockedTarget = {
  specimen: 'polished silicon wafer',
  specimenOrder: 'first surface in section 4 results',
  independentTopography:
    'MicroFinish Topographer 2.5x objective; azimuthally averaged two-dimensional PSD from measured surface map',
  topographyRmsNm: 1.44,
  firstExposedEligibleCondition: {
    wavelengthNm: 488,
    incidenceDegrees: 5,
    figure: 'Figure 4.2',
    reason:
      '633 nm is mentioned first in prose, but no 633 nm silicon-wafer 5 degree comparison curve is exposed; Figure 4.2 is the first plotted matched condition',
  },
  validSupport:
    'source states agreement is evaluated for f >= 6 cycles/mm, outside the scatterometer instrument-signature region',
  curvePresentation:
    'surface PSD and scatterometer-derived PSDscatter are plotted against spatial frequency on log-log axes',
};

const requirements = [
  {
    requirement: 'first eligible specimen identity',
    status: 'locked: polished silicon wafer',
  },
  {
    requirement: 'independently measured same-specimen PSD',
    status: 'locked: MFT 2.5x surface-map PSD',
  },
  {
    requirement: 'wavelength and incidence',
    status: 'locked: 488 nm and 5 degrees in Figure 4.2',
  },
  {
    requirement: 'instrument/specular exclusion',
    status: 'locked: exclude f < 6 cycles/mm',
  },
  {
    requirement: 'at least five source-exposed raw angular BRDF rows',
    status:
      'failed: only PSDscatter converted from BRDF with the Golden Rule is plotted',
  },
];

const sourceLockDecision = {
  status: 'source-lock-failed-raw-angular-brdf-not-exposed',
  scoringAllowed: false,
  predeclarationHash: reservation.predeclaration.hash,
  reason:
    'the source fully locks the specimen, independent surface PSD, wavelength, incidence, and valid frequency region, but Figure 4.2 plots BRDF-derived PSDscatter rather than raw BRDF versus scatter angle. Feeding PSDscatter to the frozen BRDF scorer would replace the held-out observable after target lookup',
  evidenceAction: 'none; retain the figure as source evidence but do not score it',
  recovery:
    'obtain the underlying CASI angular BRDF rows for the 488 nm, 5 degree silicon-wafer scan, or predeclare a separate independent-profile-PSD versus BRDF-derived-PSD comparator before selecting a fresh target for that model form',
};

const report = {
  source: 'roughness-tayabaly-brdf-source-lock-screen.mjs',
  date: '2026-06-24',
  target: reservation.predeclaration.target,
  sources,
  lockedTarget,
  requirements,
  sourceLockDecision,
  blockedActions: [
    'do not treat PSDscatter values as raw BRDF rows',
    'do not invert PSDscatter to BRDF without source-locked polarization-factor handling',
    'do not switch to the 84 degree condition because its agreement appears visually stronger',
    'do not switch to coated Zerodur after seeing its multi-wavelength curves',
  ],
};

const markdown = `# Tayabaly PSD/BRDF Source-Lock Screen

Status: **${sourceLockDecision.status}**

| Requirement | Status |
|---|---|
${requirements
  .map((row) => `| ${row.requirement} | ${row.status} |`)
  .join('\n')}

The frozen source-order target is the **polished silicon wafer**. The first
exposed matched condition is **488 nm, 5 degrees incidence**, with the source
requiring **f >= 6 cycles/mm** to avoid the instrument-signature region.

Reason: ${sourceLockDecision.reason}.

Scoring allowed: **no**.

Recovery: ${sourceLockDecision.recovery}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-tayabaly-brdf-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-tayabaly-brdf-source-lock-screen.md', outDir),
  markdown,
);

console.log(`Tayabaly PSD/BRDF source lock: ${sourceLockDecision.status}`);
