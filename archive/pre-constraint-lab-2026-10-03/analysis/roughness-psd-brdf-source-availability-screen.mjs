import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const screeningRule = {
  scope: 'title, abstract, repository description, and search-index screening only',
  requiredSignals: [
    'angular BRDF measured at a stated optical wavelength and incidence',
    'surface PSD measured independently by profilometry, AFM, interferometry, or equivalent topography',
    'same physical specimen or an explicitly matched witness specimen',
    'source appears to expose enough curve support for at least five non-specular rows',
  ],
  prohibitedAtThisStage: [
    'extracting numerical PSD or BRDF curve points',
    'selecting a specimen based on agreement with the frozen comparator',
    'using a PSD inferred from the target BRDF as an independent predictor',
  ],
};

const candidates = [
  {
    source:
      'K. Tayabaly, J. C. Stover, R. E. Parks, M. Dubin, and J. H. Burge, Use of the surface PSD and incident angle adjustments to investigate near specular scatter from smooth surfaces, Proc. SPIE 8838, 883805 (2013)',
    doi: '10.1117/12.2024612',
    metadataSignals: [
      'abstract explicitly identifies profile-generated surface power spectra',
      'abstract explicitly identifies direct scatterometer measurements on coated and uncoated optical flats',
      'abstract reports measurements at several known wavelengths and use of Rayleigh-Rice prediction',
    ],
    availability: 'high',
    decision: 'reserve-next',
    reason:
      'The source description directly matches the frozen independent-PSD-to-angular-BRDF construct and identifies both measurement modalities before numerical extraction.',
  },
  {
    source:
      'J. E. Harvey et al., Limitations of Rayleigh-Rice perturbation theory for describing surface scatter, Proc. SPIE 6672, 66720B (2007)',
    doi: '10.1117/12.734502',
    metadataSignals: [
      'abstract and indexed figure descriptions expose wavelength-tagged BRDF curves',
      'reported PSD curves are calculated from those BRDF measurements rather than independently measured topography',
    ],
    availability: 'high-but-dependent',
    decision: 'reject-current-gate',
    reason:
      'The apparent PSD/BRDF agreement is an inverse-scattering self-consistency check, not an independent PSD prediction of held-out BRDF shape.',
  },
  {
    source:
      'M. Le Bohec et al., Relationship between topographic parameters and BRDF for tungsten surfaces in the visible spectrum, Optik 303, 171750 (2024)',
    doi: '10.1016/j.ijleo.2024.171750',
    metadataSignals: [
      'independent confocal PSD and angular BRDF are present',
      'full source inspection found no wavelength attached to the angular BRDF profile',
    ],
    availability: 'construct-blocked',
    decision: 'retain-failed-source-lock',
    reason:
      'The frozen spatial-frequency mapping cannot pair the two measurement classes without a source-reported BRDF wavelength.',
  },
];

const selected = candidates.find((candidate) => candidate.decision === 'reserve-next');
const report = {
  source: 'roughness-psd-brdf-source-availability-screen.mjs',
  date: '2026-06-24',
  status: 'metadata-only PSD/BRDF replacement-source screen complete',
  screeningRule,
  candidates,
  selected,
  evidenceStatus: 'none; no target curve values inspected or scored',
  nextGate:
    'reserve the first source-presented eligible Tayabaly et al. optical-flat specimen and condition before opening the full paper',
};

const markdown = `# Roughness PSD/BRDF Source-Availability Screen

Status: **${report.status}**

No numerical PSD or BRDF curve values were extracted.

| Candidate | Availability | Decision | Reason |
|---|---|---|---|
${candidates
  .map(
    (row) =>
      `| ${row.source} | ${row.availability} | ${row.decision} | ${row.reason} |`,
  )
  .join('\n')}

Selected source: ${selected.source}.

Evidence status: ${report.evidenceStatus}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-psd-brdf-source-availability-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-psd-brdf-source-availability-screen.md', outDir),
  markdown,
);

console.log(`Roughness PSD/BRDF source selection: ${selected.doi}`);
