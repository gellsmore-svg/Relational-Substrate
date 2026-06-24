import { mkdir, readFile, writeFile } from 'node:fs/promises';

// Metadata-only replacement-source screen for the profile-PSD versus
// scatter-derived-PSD comparator v0 (predeclaration hash ad3892b700d0b82f).
//
// Tayabaly et al. (2013) is deliberately NOT eligible here: its silicon-wafer
// figures were inspected before this model form was frozen, so the
// predeclaration restricts it to implementation feasibility only, never fresh
// validation. This screen looks for a DIFFERENT paired surface that exposes, for
// one specimen state, an independently measured topography PSD AND a same-state
// scattering-derived PSD.
//
// Scope is strictly title, abstract, and search-index metadata. No numerical PSD
// or scatter curve values are extracted, and no specimen is selected on agreement
// with the frozen comparator.

const outDir = new URL('./out/', import.meta.url);

const predeclaration = JSON.parse(
  await readFile(
    new URL('roughness-profile-psd-scatter-psd-predeclaration.json', outDir),
    'utf8',
  ),
);

const screeningRule = {
  modelFormPredeclarationHash: predeclaration.predeclaration.hash,
  scope: 'title, abstract, publisher landing page, and search-index screening only',
  requiredSignals: [
    'surface PSD measured independently by topography (AFM, profilometry, interferometry, confocal, or equivalent)',
    'a scattering-derived surface PSD obtained from angle-resolved scattering or BRDF for the SAME specimen state',
    'both PSD classes reported in a shared spatial-frequency representation that could later expose at least eight matched rows spanning at least 0.5 decade',
    'a stated optical wavelength and geometry for the scattering measurement, or a clear path to one in the full text',
  ],
  prohibitedAtThisStage: [
    'extracting numerical PSD or scatter curve points',
    'selecting a specimen or instrument pairing based on agreement with the frozen comparator',
    'using a single PSD jointly inverted from combined optical data as if it were two independent curves',
    'reusing Tayabaly et al. (2013), an exposed-feasibility source, as fresh validation',
  ],
};

const candidates = [
  {
    source:
      'A. Duparre, J. Ferre-Borrull, S. Gliech, G. Notni, J. Steinert, and J. M. Bennett, Surface characterization techniques for determining the root-mean-square roughness and power spectral densities of optical components, Applied Optics 41, 154-171 (2002)',
    doi: '10.1364/AO.41.000154',
    metadataSignals: [
      'abstract states 15 samples were measured by AFM, mechanical profiler (Talystep), confocal laser scanning microscope, angle-resolved scattering, and total scattering',
      'abstract states two-dimensional PSD functions were computed from the digitized data specifically to allow direct comparison across instruments despite different spatial-wavelength band limits',
      'this provides, per sample, an independent topography PSD and a separate scattering-derived PSD in a shared PSD representation',
    ],
    openRequirements: [
      'the scattering wavelength and geometry are not stated in the abstract and must be locked from the full text before extraction',
      'one single sample and one single topography instrument must be frozen as the independent-PSD source before lookup',
      'the topography-PSD and scattering-PSD overlap band must be confirmed to expose at least eight matched rows over at least 0.5 decade',
    ],
    availability: 'high',
    decision: 'reserve-next',
    reason:
      'It is a same-sample round-robin that reports both an independent topography PSD and a scattering-derived PSD in one PSD representation, which is exactly the frozen independent-profile-PSD versus scatter-derived-PSD construct, and it is not the exposed Tayabaly source.',
  },
  {
    source:
      'S. Schroeder, A. Duparre, L. Coriand, A. Tuennermann, D. H. Penalver, and J. E. Harvey, Modeling of light scattering in different regimes of surface roughness, Optics Express 19, 9820-9835 (2011)',
    doi: '10.1364/OE.19.009820',
    metadataSignals: [
      'title and abstract emphasize modeling measured scatter across smooth-to-rough regimes from PSD',
      'unclear from metadata whether an independent topography PSD and a same-state scattering-derived PSD are both reported as comparable curves rather than a measured-versus-modeled scatter comparison',
    ],
    availability: 'secondary',
    decision: 'defer',
    reason:
      'A modeled-scatter-versus-measured-scatter emphasis would not supply two independent PSD curves; hold as a fallback only if the primary candidate fails source lock.',
  },
  {
    source:
      'J. E. Harvey et al., Calculating BRDFs from surface PSDs for moderately rough optical surfaces, Proc. SPIE 7426, 74260I (2009)',
    doi: '10.1117/12.831302',
    metadataSignals: [
      'title and abstract describe a method to calculate BRDF from a surface PSD for moderately rough surfaces',
      'the moderately-rough regime explicitly departs from the smooth-surface Rayleigh-Rice proportionality the comparator assumes',
    ],
    availability: 'method-paper',
    decision: 'reject-current-gate',
    reason:
      'This is a forward PSD-to-BRDF method paper in a regime outside the frozen smooth-surface scope, not an independent topography PSD versus same-state scattering PSD comparison.',
  },
  {
    source:
      'Optical method for determining the power spectral density function of randomly rough surfaces by simultaneous processing of spectroscopic reflectometry, variable-angle spectroscopic ellipsometry and angle-resolved scattering data, Optik (2023); ScienceDirect PII S0030402623002711',
    doi: null,
    metadataSignals: [
      'abstract describes jointly inverting reflectometry, ellipsometry, and ARS into one PSD function',
    ],
    availability: 'reject-construct',
    decision: 'reject-current-gate',
    reason:
      'A single jointly inverted PSD is not an independent topography PSD set against a separate scattering-derived PSD; using it would collapse the two curves the comparator must keep independent.',
  },
];

const selected = candidates.find((candidate) => candidate.decision === 'reserve-next');

const report = {
  source: 'roughness-profile-psd-scatter-psd-source-screen.mjs',
  date: '2026-06-24',
  status: 'metadata-only profile-PSD versus scatter-PSD replacement-source screen complete',
  validationClaim: false,
  evidenceStatus: 'none; no target curve values inspected or scored',
  screeningRule,
  candidates,
  selected,
  nextGate:
    'reserve the Duparre et al. (2002) round-robin with one frozen sample, one frozen topography instrument as the independent PSD, and the angle-resolved-scattering-derived PSD as the comparison curve, then resolve the scattering wavelength and geometry from the full text before extracting any numerical PSD rows',
};

const markdown = `# Profile-PSD versus Scatter-PSD Source Screen

Status: **${report.status}**

Model form predeclaration hash: \`${screeningRule.modelFormPredeclarationHash}\`.

No numerical PSD or scatter curve values were extracted. Scope was abstract and
index metadata only.

| Candidate | Availability | Decision | Reason |
|---|---|---|---|
${candidates
  .map(
    (row) => `| ${row.source} | ${row.availability} | ${row.decision} | ${row.reason} |`,
  )
  .join('\n')}

Selected source: ${selected.source}.

Open requirements before any numerical lookup:

${selected.openRequirements.map((item) => `- ${item}`).join('\n')}

Evidence status: ${report.evidenceStatus}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-profile-psd-scatter-psd-source-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-profile-psd-scatter-psd-source-screen.md', outDir),
  markdown,
);

console.log(`Profile/scatter PSD source screen: ${selected.doi}`);
