import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-tbhp-target-reservation.json', outDir),
    'utf8',
  ),
);

const report = {
  source: 'peroxide-tbhp-source-extraction.mjs',
  date: '2026-06-23',
  target: {
    molecule: 'tert-butyl hydroperoxide',
    formula: '(CH3)3COOH',
    predeclarationHash: reservation.predeclaration.hash,
  },
  sourceReference: {
    citation:
      'E. Vogt et al., Coupling of torsion and OH-stretching in tert-butyl hydroperoxide. II, J. Chem. Phys. 154, 164307 (2021)',
    doi: '10.1063/5.0048022',
    localText: 'analysis/source-cache/vogt-2021-tbhp-torsion-oh-stretch-ii.txt',
  },
  torsionConstruct: {
    coordinate: 'C-O-O-H dihedral, tau',
    construct: 'effective ground-state potential-energy torsion',
    equilibriumDegrees: 113.56,
    equivalentMinimumDegrees: 246.44,
    transBarrierCoordinateDegrees: 180,
    sourceDescription:
      'symmetric double-well with equivalent minima and a trans barrier at 180 degrees',
  },
  barrierComparators: {
    sourceLocation: 'Table II footnote a',
    groundStateLmCm1: 286,
    groundStateRpCm1: 335,
    interpretation:
      'independent local-mode and reaction-path effective ground-state torsional barriers',
  },
  experimentalConstructSupport: {
    sourceLocation: 'abstract and Results section',
    observation:
      'gas-phase spectra show OH-stretch/torsion combination features and direct evidence of tunnelling splitting in the fundamental region',
    limitation:
      'the extracted absolute barriers are calculated effective-potential values, not direct experimental barrier measurements',
  },
};

const markdown = `# TBHP Source Extraction

## Torsion Construct

| Field | Value |
|---|---|
| coordinate | ${report.torsionConstruct.coordinate} |
| construct | ${report.torsionConstruct.construct} |
| equilibrium | ${report.torsionConstruct.equilibriumDegrees} degrees |
| equivalent minimum | ${report.torsionConstruct.equivalentMinimumDegrees} degrees |
| trans comparator | ${report.torsionConstruct.transBarrierCoordinateDegrees} degrees |

## Ground-State Barrier Comparators

| Model | Barrier |
|---|---:|
| local mode | ${report.barrierComparators.groundStateLmCm1} cm-1 |
| reaction path | ${report.barrierComparators.groundStateRpCm1} cm-1 |

Experimental support: ${report.experimentalConstructSupport.observation}.

Limitation: ${report.experimentalConstructSupport.limitation}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('peroxide-tbhp-source-extraction.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('peroxide-tbhp-source-extraction.md', outDir), markdown);

console.log(`TBHP equilibrium torsion extracted: ${report.torsionConstruct.equilibriumDegrees} degrees`);
