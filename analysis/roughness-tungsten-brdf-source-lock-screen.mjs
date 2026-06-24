import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('roughness-tungsten-brdf-target-reservation.json', outDir),
    'utf8',
  ),
);

const sources = [
  {
    role: 'primary open-access article',
    citation:
      'M. Le Bohec et al., Relationship between topographic parameters and BRDF for tungsten surfaces in the visible spectrum, Optik 303, 171750 (2024)',
    doi: '10.1016/j.ijleo.2024.171750',
    repository:
      'University of Strathclyde Strathprints, CC BY 4.0 final published version',
    url:
      'https://strathprints.strath.ac.uk/89058/1/Le-Bohec-etal-Optik-2024-Relationship-between-topographic-parameters-and-BRDF-for-tungsten-surfaces.pdf',
    accessResult:
      'full 12-page PDF retrieved and inspected; figures 5 and 8 and table 1 are accessible',
  },
  {
    role: 'supplementary-data pointer',
    repository: 'article DOI supplementary-data link',
    accessResult:
      'main article identifies supplementary figures but states that numerical data will be made available on request; no paired numerical PSD/BRDF table is present in the retrieved article',
  },
];

const requirements = [
  {
    requirement: 'first specimen identity in source presentation order',
    status: 'locked: M100',
  },
  {
    requirement: 'first eligible visible-wavelength in-plane BRDF condition',
    status:
      'not available: figure 5 gives normalized angular BRDF at 10 degree incidence but does not state a measurement wavelength',
  },
  {
    requirement: 'same-specimen PSD numerical support',
    status:
      'figure-only: M100 PSD is plotted over 1.3-2.3 inverse micrometres in figure 8a',
  },
  {
    requirement: 'at least five matched non-specular BRDF rows',
    status:
      'not construct-matchable: figure 5 angular rows lack the wavelength required for spatial-frequency mapping',
  },
  {
    requirement: 'specular mask, wavelength, incidence, and scan direction',
    status:
      'partially locked: in-plane scan and 10 degree incidence are reported; wavelength and source-defined specular-core width are absent',
  },
];

const sourceLockDecision = {
  status: 'source-lock-failed-unpaired-psd-brdf-constructs',
  scoringAllowed: false,
  predeclarationHash: reservation.predeclaration.hash,
  reason:
    'the full source locks the first specimen as M100 and exposes separate figure-level PSD and normalized angular BRDF traces, but the angular BRDF condition has no stated wavelength. The frozen Rayleigh-Rice mapping requires wavelength to convert every scatter angle to spatial frequency, so the two traces cannot be paired without inventing a condition',
  evidenceAction: 'none; do not score or infer values',
  exposedFallback:
    'Irizar and Harnisch (2012) is accessible and demonstrates measured topography-to-BRDF comparison, but its numerical sample details were exposed before reservation and it may be used only for implementation feasibility, not fresh validation',
  recovery:
    'obtain the authors numerical M100 BRDF data with measurement wavelength and specular-mask metadata, or reserve a new target only after a metadata screen confirms paired wavelength-specific angular BRDF and independent surface PSD',
};

const report = {
  source: 'roughness-tungsten-brdf-source-lock-screen.mjs',
  date: '2026-06-24',
  target: reservation.predeclaration.target,
  sources,
  requirements,
  sourceLockDecision,
  blockedActions: [
    'do not assume that figure 5 was measured at 600 nm from the separate reflectivity discussion',
    'do not substitute the exposed 2012 sample as fresh validation',
    'do not digitize and pair figure 5 with figure 8 without a source-reported wavelength',
    'do not score the Rayleigh-Rice comparator',
  ],
};

const markdown = `# Tungsten PSD/BRDF Source-Lock Screen

Status: **${sourceLockDecision.status}**

| Requirement | Status |
|---|---|
${requirements
  .map((row) => `| ${row.requirement} | ${row.status} |`)
  .join('\n')}

Reason: ${sourceLockDecision.reason}.

Scoring allowed: **no**.

The source-order target is **M100**. Its PSD is visible in figure 8a, and its normalized angular BRDF is visible in figure 5. These are not numerically pairable under the frozen descriptor because figure 5 does not report the wavelength needed for the angular-to-spatial-frequency transform.

Exposed fallback: ${sourceLockDecision.exposedFallback}.

Recovery: ${sourceLockDecision.recovery}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-tungsten-brdf-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-tungsten-brdf-source-lock-screen.md', outDir),
  markdown,
);

console.log(`Tungsten PSD/BRDF source lock: ${sourceLockDecision.status}`);
