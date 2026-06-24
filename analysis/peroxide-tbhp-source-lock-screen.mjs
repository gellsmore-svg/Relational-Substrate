import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-tbhp-target-reservation.json', outDir),
    'utf8',
  ),
);

const target = {
  molecule: 'tert-butyl hydroperoxide',
  formula: '(CH3)3COOH',
  reservedBy: 'peroxide-tbhp-target-reservation.mjs',
  predeclarationHash: reservation.predeclaration.hash,
};

const sources = [
  {
    role: 'primary torsion model and spectroscopy source',
    citation:
      'E. Vogt et al., Coupling of torsion and OH-stretching in tert-butyl hydroperoxide. II, J. Chem. Phys. 154, 164307 (2021)',
    doi: '10.1063/5.0048022',
    url: 'https://www.osti.gov/pages/servlets/purl/1853713',
    localPdf: 'analysis/source-cache/vogt-2021-tbhp-torsion-oh-stretch-ii.pdf',
    localText: 'analysis/source-cache/vogt-2021-tbhp-torsion-oh-stretch-ii.txt',
    usefulBecause:
      'reports the source torsion convention, equilibrium angle, trans barrier coordinate, two ground-state barrier calculations, and experimental spectra supporting the double-well construct',
  },
  {
    role: 'companion cold/warm overtone source',
    citation:
      'A. S. Hansen et al., Coupling of torsion and OH-stretching in tert-butyl hydroperoxide. I, J. Chem. Phys. 154, 164306 (2021)',
    doi: '10.1063/5.0048020',
    url: 'https://www.osti.gov/pages/biblio/1780162',
    usefulBecause:
      'independent companion experiment/model context for the first overtone region',
  },
];

const sourceLockDecision = {
  status: 'source-locked; extraction permitted',
  sameSurfaceComparator: true,
  construct: 'potential-energy COOH torsion with equivalent minima and trans barrier',
  experimentalSupport:
    'gas-phase OH-stretch/torsion spectra and observed tunnelling splitting support the double-well torsional construct',
  evidenceEligibility:
    'post-reservation computed-comparator scoring with experimental construct support; not a direct experimental absolute-barrier validation',
};

const report = {
  source: 'peroxide-tbhp-source-lock-screen.mjs',
  date: '2026-06-23',
  target,
  sources,
  sourceLockDecision,
  blockedActions: [
    'do not score from abstract text',
    'do not alter the source torsion convention',
    'do not average the two model barriers into a fitted target',
    'do not tune the 45-degree selection tolerance or live release parameters',
  ],
};

const markdown = `# TBHP Source-Lock Screen

Status: **${sourceLockDecision.status}**

The source provides a same-surface equilibrium torsion and trans barrier
coordinate. Experimental spectra independently support the double-well and
tunnelling construct.

Evidence eligibility: ${sourceLockDecision.evidenceEligibility}.

## Sources

| Role | Citation | DOI | Locked use |
|---|---|---|---|
${sources
  .map((row) => `| ${row.role} | ${row.citation} | ${row.doi} | ${row.usefulBecause} |`)
  .join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-tbhp-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-tbhp-source-lock-screen.md', outDir), markdown);

console.log(`TBHP source lock: ${sourceLockDecision.status}`);
