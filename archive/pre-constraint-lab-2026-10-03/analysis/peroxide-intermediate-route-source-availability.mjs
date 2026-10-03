import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const screeningRule = {
  scope: 'title, abstract, and bibliographic metadata only',
  requiredSignals: [
    'fresh peroxide-family molecular identity',
    'isolated-molecule or gas-phase treatment',
    'explicit torsional potential or torsion-dependent observable',
    'source plausibly exposes more than an equilibrium/trans endpoint pair',
  ],
  prohibitedAtThisStage: [
    'extracting numerical torsion coordinates',
    'extracting numerical relative energies or barrier heights',
    'choosing the target from numerical agreement with the live model',
  ],
};

const candidates = [
  {
    target: 'peroxyformic acid',
    formula: 'HC(O)OOH',
    rotorClass: 'carbonyl-substituted hydroperoxide O-O/COOH rotor',
    freshness: 'not present in existing scoring artifacts or the local source cache',
    sourceSignals: [
      {
        citation:
          'Y. N. Indulkar, M. K. Louie, and A. Sinha, UV Photochemistry of Peroxyformic Acid (HC(O)OOH): An Experimental and Computational Study Investigating 355 nm Photolysis, J. Phys. Chem. A 118 (2014)',
        doi: '10.1021/jp5039688',
        signal:
          'abstract explicitly contrasts the computed peroxyformic-acid torsional potential with H2O2 in an isolated-molecule photochemistry study',
      },
    ],
    availability: 'medium',
    decision: 'reserve',
    reason:
      'The carbonyl-substituted hydroperoxide is a fresh structural transfer and the source description explicitly identifies a torsional potential rather than only decomposition kinetics.',
  },
  {
    target: 'isopropyl hydroperoxide',
    formula: '(CH3)2CHOOH',
    rotorClass: 'branched alkyl hydroperoxide',
    freshness: 'not used',
    sourceSignals: [],
    availability: 'low-for-profile',
    decision: 'defer',
    reason:
      'Current metadata exposes thermochemistry and broad conformer studies, but not a clearly source-defined multi-point torsional profile.',
  },
  {
    target: 'hydroxymethyl hydroperoxide',
    formula: 'HOCH2OOH',
    rotorClass: 'hydroxy-substituted hydroperoxide with coupled internal rotors',
    freshness: 'previously named in backup lists but not scored',
    sourceSignals: [
      {
        citation:
          'Structure, spectroscopic properties, and photochemistry of hydroxymethyl hydroperoxide, J. Chem. Phys. 131, 104301 (2009)',
        doi: '10.1063/1.3231145',
        signal:
          'metadata identifies a dedicated structure and spectroscopy study, but the required same-surface intermediate torsion profile is not explicit',
      },
    ],
    availability: 'uncertain',
    decision: 'defer',
    reason:
      'Multiple coupled rotors create a construct-mapping risk before a clean intermediate O-O route is established.',
  },
];

const selected = candidates.find((candidate) => candidate.decision === 'reserve');
const report = {
  source: 'peroxide-intermediate-route-source-availability.mjs',
  date: '2026-06-24',
  status: 'metadata-only intermediate-route availability screen complete',
  screeningRule,
  candidates,
  selected,
  evidenceStatus: 'none; no numerical target values inspected',
  nextGate:
    'reserve peroxyformic acid and freeze a non-saturated multi-point quantitative criterion before numerical source extraction',
};

const markdown = `# Peroxide Intermediate-Route Source Availability

Status: **${report.status}**

This screen uses bibliographic metadata and abstracts only. It does not extract
target torsions, relative energies, barriers, or fitted potential terms.

| Target | Formula | Availability | Decision | Reason |
|---|---|---|---|---|
${candidates
  .map(
    (row) =>
      `| ${row.target} | ${row.formula} | ${row.availability} | ${row.decision} | ${row.reason} |`,
  )
  .join('\n')}

Selected identity: **${selected.target} (${selected.formula})**.

Evidence status: ${report.evidenceStatus}.

Next gate: ${report.nextGate}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-intermediate-route-source-availability.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-intermediate-route-source-availability.md', outDir),
  markdown,
);

console.log(`Intermediate-route availability selection: ${selected.target}`);
