import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const candidates = [
  {
    target: 'methyl chloroperoxide',
    formula: 'CH3OOCl',
    rotorClass: 'halogen-substituted methyl peroxide O-O rotor',
    sourceSignal:
      'primary article metadata explicitly states that the torsional potential of methyl chloroperoxide was calculated',
    source:
      'E. Drougas and A. M. Kosmas, Quantum mechanical studies of isomeric and conformeric structures of methyl-chloro-peroxide, Int. J. Quantum Chem. (2004), DOI 10.1002/qua.20012',
    freshness:
      'no numerical torsion coordinate, energy, barrier, or profile shape has been extracted in this project',
    transferBoundary:
      'adjacent peroxide-family boundary test; Cl replaces the terminal H/alkyl group and may introduce electronic effects outside hydroperoxide transfer',
    decision: 'reserve',
  },
  {
    target: 'peracetic acid',
    formula: 'CH3C(O)OOH',
    rotorClass: 'peroxyacid with coupled OH, C-O, and methyl torsions',
    sourceSignal: 'explicit one-dimensional cuts of a three-dimensional PES',
    freshness:
      'excluded: numerical conformer and barrier values were exposed before reservation',
    transferBoundary: 'coupled multi-rotor system',
    decision: 'diagnostic-only',
  },
  {
    target: 'hydroxymethyl hydroperoxide',
    formula: 'HOCH2OOH',
    rotorClass: 'coupled hydroxy/hydroperoxy rotor',
    sourceSignal: 'optimized conformers and spectroscopy source available',
    freshness: 'reserved previously',
    transferBoundary:
      'source lock failed because conformer changes mix multiple dihedrals and hydrogen-bond topology',
    decision: 'source-blocked',
  },
];

const selected = candidates.find((candidate) => candidate.decision === 'reserve');
const report = {
  source: 'peroxide-v2-source-availability-screen.mjs',
  date: '2026-06-24',
  status: 'metadata-only v2 source-availability screen complete',
  screeningRule: {
    allowed: 'title, abstract, citation, and source-description metadata only',
    required:
      'explicit torsional potential or one-dimensional torsional scan for a fresh peroxide-family identity',
    prohibited:
      'numerical torsions, energies, barriers, Fourier coefficients, or profile-shape extraction before reservation',
  },
  candidates,
  selected,
  evidenceStatus: 'none; metadata screening only',
  nextGate:
    'reserve methyl chloroperoxide under the frozen v2 formula and quantitative profile thresholds before full-source inspection',
};

const markdown = `# Peroxide v2 Source-Availability Screen

Status: **${report.status}**

| Target | Formula | Decision | Source signal | Boundary |
|---|---|---|---|---|
${candidates
  .map(
    (row) =>
      `| ${row.target} | ${row.formula} | ${row.decision} | ${row.sourceSignal} | ${row.transferBoundary} |`,
  )
  .join('\n')}

Selected: **${selected.target} (${selected.formula})**.

This is an adjacent-family boundary test, not an assumption that chlorine and
hydrogen/alkyl substitution are equivalent.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-v2-source-availability-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('peroxide-v2-source-availability-screen.md', outDir),
  markdown,
);

console.log(`Peroxide v2 source selection: ${selected.target}`);
