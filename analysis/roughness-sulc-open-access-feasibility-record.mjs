import { mkdir, writeFile } from 'node:fs/promises';

// Open-access source record for the profile-PSD versus scatter-derived-PSD
// comparator v0 (model-form predeclaration hash ad3892b700d0b82f).
//
// While the reserved Duparre et al. (2002) target stayed access-blocked, an
// open-access same-construct source was located and read in full: Sulc et al.,
// Coatings 13, 1853 (2023). Because its full numerical content (Table 3 and
// Figure 5) was inspected during accessibility verification, it is recorded as an
// EXPOSED / feasibility-only source under the same rule that bars Tayabaly: it can
// inform implementation, but it is NOT a fresh held-out validation target.
//
// No score is produced. The comparator's independent-profile-PSD input cannot be
// numerically populated from this source (see blocker below), so nothing is fitted
// or claimed as evidence.

const outDir = new URL('./out/', import.meta.url);

const source = {
  citation:
    'V. Sulc, J. Vohanka, I. Ohlidal, P. Klapetek, M. Ohlidal, N. J. Kaur, F. Vizca, Multi-Wavelength Angle-Resolved Scattering of Randomly Rough Surfaces Based on the Scalar Diffraction Theory, Coatings 13, 1853 (2023)',
  doi: '10.3390/coatings13111853',
  openAccessRoute:
    'Unpaywall -> Brno University of Technology DSpace repository PDF (publisher MDPI HTML/PDF is Akamai bot-blocked to non-browser clients)',
  cachedAt: 'analysis/source-cache/sulc-2023-coatings-13-1853.pdf (+ .txt; source-cache is gitignored)',
};

const constructConfirmed = {
  matchesModelForm: true,
  modelFormHash: 'ad3892b700d0b82f',
  details: [
    'four randomly rough silicon samples (anodic oxidation), rms heights ~12 nm (smoothest) to ~24 nm (roughest)',
    'angle-resolved scattering measured at normal incidence for three wavelengths 457.9, 514.5, and 647.1 nm (argon/krypton ion laser), polar angle up to 60 degrees',
    'a scattering-derived PSDF is recovered from the multi-wavelength ARS data (scalar diffraction theory; ARS-infinity exact, ARS1/ARS0 approximate)',
    'an independent AFM topography PSDF is obtained for the same samples via Gwyddion 2.59',
    'Figure 5 overlays the scattering-derived PSDF (ARS0/ARS1/ARS-infinity) against the AFM PSDF for each sample -- exactly the independent-profile-PSD versus scatter-derived-PSD comparison',
    'the scattering-derived PSDF support (region II) spans k = 0.0005 to 0.012 nm^-1, about 1.38 decades, comfortably above the 0.5-decade minimum',
  ],
};

const extractability = {
  scatterDerivedPsd:
    'numerically reconstructable without digitization: Table 3 gives, per sample and approach, sigma_II and the node log-derivatives l1..l6 (and tau for ARS-infinity); with the fixed node positions kmin, 0.001, 0.002, 0.004, 0.008, kmax nm^-1 and the spline continuity conditions, the exponential-of-quadratic-spline PSDF (Eq. 12) is determined over region II',
  independentAfmPsd:
    'NOT numerically available: the AFM PSDF appears only as a plotted curve in Figure 5; Table 3 reports only its scalar integrated values sigma_II and sigma_T, not the curve. The Data Availability Statement says data are available only upon reasonable request from the corresponding author',
  tabulatedScalarCrossCheck:
    'Table 3 does expose a real numerical AFM-versus-scatter agreement at the scalar level (region-II rms): e.g. sample 1 ARS-infinity sigma_II 10.0 nm vs AFM 9.9 nm; sample 2 14.5 vs 14.9; sample 3 18.0 vs 16.8; sample 4 21.2 vs 18.9. This is an rms-over-region-II agreement, NOT the frequency-resolved shape the comparator scores',
};

const scoringStatus = {
  formTwoScoreable: false,
  reason:
    'the comparator log-log interpolates the independent profile (AFM) PSD at each scatter-PSD frequency, so it needs the AFM PSDF as numerical rows; here the AFM PSDF is figure-only. The scatter side is fully reconstructable, but with one curve missing no shape comparison can be run',
  evidenceClassification:
    'exposed / feasibility-only (full numerical content read before any reservation); not eligible as fresh held-out validation',
};

const siblingsAndLeads = [
  {
    source:
      'S. Sustek, J. Vohanka, I. Ohlidal, M. Ohlidal, V. Sulc, P. Klapetek, N. J. Kaur, Characterization of randomly rough surfaces using angle-resolved scattering of light and atomic force microscopy, J. Opt. 23, 105602 (2021)',
    doi: '10.1088/2040-8986/ac1f35',
    relation: 'same group, same AFM + ARS construct, single wavelength (reference [5] of Sulc 2023)',
    inspected: false,
    access:
      'closed; no open copy via Unpaywall, OpenAlex, or the authors own Brno VUT DSpace (the same repository that holds the Sulc 2023 PDF). Needs institutional/IOP access',
    status:
      'clean un-inspected potential fresh held-out target, but access-gated; metadata-only screening preserved its held-out status (full text not read)',
  },
  {
    source: 'A. Duparre et al., Applied Optics 41, 154-171 (2002)',
    doi: '10.1364/AO.41.000154',
    relation: 'previously reserved fresh held-out target (hash 5305a937566e8b24)',
    inspected: false,
    access: 'paywalled / ResearchGate 403',
    status: 'reservation stands; still blocked on verified full-text access',
  },
];

const systematicObstacle =
  'across this AFM + ARS literature the independent topography PSDF is published as a figure curve, while the scatter-derived PSDF is given parametrically. Numerically scoring the profile-PSD versus scatter-PSD comparator therefore requires author-provided or supplementary AFM PSD data (or an explicitly feasibility-grade figure digitization), not just open-access full text.';

const report = {
  source: 'roughness-sulc-open-access-feasibility-record.mjs',
  date: '2026-06-24',
  status: 'open-access same-construct source located, read, and classified; no score produced',
  validationClaim: false,
  evidenceStatus: 'none; exposed/feasibility-only source, no curve scored',
  modelFormHash: 'ad3892b700d0b82f',
  sourceRecord: source,
  constructConfirmed,
  extractability,
  scoringStatus,
  siblingsAndLeads,
  systematicObstacle,
  nextGates: [
    'to score Form 2 on real data, obtain the AFM PSDF numerical rows for one Sulc 2023 sample (corresponding-author request or a Gwyddion export of the published scans), then run the frozen comparator as an EXPOSED-source feasibility demonstration only (not fresh evidence)',
    'for fresh held-out evidence, reserve an un-inspected same-construct source before lookup; the Sustek 2021 sibling is the strongest candidate but is closed-access and needs institutional access; the Duparre 2002 reservation also still stands pending access',
  ],
};

const markdown = `# Sulc 2023 Open-Access Source Record (profile-PSD vs scatter-PSD v0)

Status: **${report.status}**

Model form: \`${report.modelFormHash}\`. Evidence status: ${report.evidenceStatus}.

Source: ${source.citation} (DOI ${source.doi}).
Open-access route: ${source.openAccessRoute}.
Cached: ${source.cachedAt}.

## Construct (confirmed)

${constructConfirmed.details.map((item) => `- ${item}`).join('\n')}

## Extractability

- scatter-derived PSD: ${extractability.scatterDerivedPsd}
- independent AFM PSD: ${extractability.independentAfmPsd}
- scalar cross-check only: ${extractability.tabulatedScalarCrossCheck}

## Form-2 scoring status

- scoreable: **${scoringStatus.formTwoScoreable ? 'yes' : 'no'}**
- reason: ${scoringStatus.reason}
- classification: ${scoringStatus.evidenceClassification}

## Siblings and leads

${siblingsAndLeads
  .map(
    (row) =>
      `- ${row.source} (DOI ${row.doi}) — ${row.relation}; inspected: ${row.inspected}; access: ${row.access}; ${row.status}`,
  )
  .join('\n')}

## Systematic obstacle

${systematicObstacle}

## Next gates

${report.nextGates.map((item) => `- ${item}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-sulc-open-access-feasibility-record.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-sulc-open-access-feasibility-record.md', outDir),
  markdown,
);

console.log(`Sulc 2023 open-access source record: ${report.status}`);
