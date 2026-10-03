import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const screeningRule = {
  scope: 'metadata, title, abstract, and source-description screening only',
  requiredSignals: [
    'same molecular identity',
    'gas-phase or isolated-molecule treatment',
    'explicit torsional potential, torsion-vibration model, or hindered-rotation profile',
    'source appears capable of providing an equilibrium torsion and nonlocal comparator',
  ],
  prohibitedAtThisStage: [
    'extracting numerical equilibrium torsions',
    'extracting barrier heights or Fourier coefficients',
    'changing target choice based on numeric agreement',
  ],
};

const candidates = [
  {
    target: 'tert-butyl hydroperoxide',
    formula: '(CH3)3COOH',
    priorStatus: 'named previously as a backup candidate; no source values extracted or scored',
    sourceSignals: [
      {
        citation:
          'E. Vogt, R. M. Huchmala, C. V. Jensen, and H. G. Kjaergaard, Coupling of torsion and OH-stretching in tert-butyl hydroperoxide. I, J. Chem. Phys. 154, 164306 (2021)',
        doi: '10.1063/5.0048020',
        signal:
          'title and abstract identify a dedicated gas-phase TBHP torsion/OH-stretch study and torsional-potential model',
      },
      {
        citation:
          'E. Vogt, R. M. Huchmala, C. V. Jensen, and H. G. Kjaergaard, Coupling of torsion and OH-stretching in tert-butyl hydroperoxide. II, J. Chem. Phys. 154, 164307 (2021)',
        doi: '10.1063/5.0048022',
        signal:
          'abstract reports gas-phase fundamental/overtone spectra and strong OH-stretch/torsion coupling',
      },
    ],
    availability: 'high',
    decision: 'reserve-next',
    reason:
      'Only candidate with a dedicated same-molecule torsional-potential and gas-phase spectroscopy programme visible at metadata level.',
  },
  {
    target: 'methyl ethyl peroxide',
    formula: 'CH3OOC2H5',
    priorStatus: 'not used',
    sourceSignals: [],
    availability: 'low',
    decision: 'reject-current-gate',
    reason:
      'Search results are dominated by methyl ethyl ketone peroxide/catalyst ambiguity and do not identify a clean isolated-molecule torsional source.',
  },
  {
    target: 'di-tert-butyl peroxide',
    formula: '(CH3)3COOC(CH3)3',
    priorStatus: 'not used',
    sourceSignals: [
      {
        citation: 'multiple thermal decomposition and O-O bond dissociation studies',
        doi: null,
        signal:
          'sources focus on bond rupture kinetics and steric effects rather than a source-defined isolated O-O torsional profile',
      },
    ],
    availability: 'low-for-required-comparator',
    decision: 'defer',
    reason:
      'Source-rich for decomposition, but the required equilibrium-plus-nonlocal torsion comparator is not evident.',
  },
];

const selected = candidates.find((candidate) => candidate.decision === 'reserve-next');
const report = {
  source: 'peroxide-source-availability-screen.mjs',
  date: '2026-06-23',
  status: 'metadata-only source-availability screen complete',
  screeningRule,
  candidates,
  selected,
  evidenceStatus: 'none; no numerical target values inspected',
  nextGate:
    'reserve tert-butyl hydroperoxide under the frozen observable-route model before opening full text or extracting values',
};

const markdown = `# Peroxide Source-Availability Screen

Status: **${report.status}**

This screen uses metadata and abstract-level source descriptions only. No
target torsion or barrier values were extracted.

## Candidate Screen

| Target | Formula | Availability | Decision | Reason |
|---|---|---|---|---|
${candidates
  .map(
    (row) =>
      `| ${row.target} | ${row.formula} | ${row.availability} | ${row.decision} | ${row.reason} |`,
  )
  .join('\n')}

## Selected Identity

${selected.target} (${selected.formula}) is selected because dedicated
same-molecule gas-phase torsion and spectroscopy papers exist.

Evidence status: ${report.evidenceStatus}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-source-availability-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-source-availability-screen.md', outDir), markdown);

console.log(`Peroxide source-availability selection: ${selected.target}`);
