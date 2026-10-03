import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const source = {
  citation: 'S. Dalbouha, M. L. Senent, and N. Komiha, J. Chem. Phys. 142, 074304 (2015)',
  doi: '10.1063/1.4907941',
  localPdf: 'analysis/source-cache/dalbouha-2015-ch3ooh.pdf',
  localText: 'analysis/source-cache/dalbouha-2015-ch3ooh.txt',
  sourceType: 'CCSD(T)/aug-cc-pVTZ torsional potential surface with CCSD(T)-F12 structural context',
};

const reservedTarget = {
  molecule: 'methyl hydroperoxide',
  formula: 'CH3OOH',
  alias: 'MeOOH',
  reservation: 'peroxide-fresh-rotor-target-reservation.mjs',
  sourceLock: 'peroxide-methyl-hydroperoxide-source-lock-screen.mjs',
};

const frozenRepair = {
  releaseStrength: 0.25,
  releaseOnsetDegrees: 155,
  releaseSpanDegrees: 20,
  status: 'unchanged by source extraction',
};

const torsionConvention = {
  methylTorsionTheta: '(H5C3X1Y2 + H6C3X1Y2 + H7C3X1Y2) / 3 - 180 degrees',
  hydroxylTorsionAlpha: 'H4Y2X1C3 - 180 degrees; X=O, Y=O for CH3OOH',
  independentCoordinates: ['theta: methyl torsion', 'alpha: OH torsion'],
  scoringRelevance:
    'The peroxide repair candidate applies to the anti-planar release of the H-bearing O-O rotor; alpha is the directly relevant OH torsion coordinate.',
};

const torsionGrid = {
  thetaDegrees: [0, 90, 180, -90],
  alphaDegrees: [0, 30, 60, 90, 120, 150, 180],
  planarSymmetryRule: 'for planar alpha values 0 and 180 degrees, E(alpha, theta) = E(alpha, -theta)',
  nonOptimizedCoordinates: 'all other internal coordinates optimized for each grid point at CCSD/aug-cc-pVTZ',
};

const extractedValues = [
  {
    key: 'V3',
    label: 'methyl internal-rotation barrier',
    valueCm1: 1071.31,
    comparatorType: 'computed',
    method: 'CCSD(T)/aug-cc-pVTZ',
    table: 'Table V',
    usableForRepairGate: false,
    reason: 'methyl torsion is not the peroxide OH anti-planar release comparator',
  },
  {
    key: 'Vtrans_YH',
    label: 'OH trans barrier',
    valueCm1: 162.74,
    comparatorType: 'computed',
    method: 'CCSD(T)/aug-cc-pVTZ',
    table: 'Table V',
    usableForRepairGate: true,
    reason: 'directly tests whether the anti-planar OH torsion should be lightly penalized rather than treated as a high-strain failure',
  },
  {
    key: 'Vcis_YH',
    label: 'OH cis barrier',
    valueCm1: 2012.43,
    comparatorType: 'computed',
    method: 'CCSD(T)/aug-cc-pVTZ',
    table: 'Table V',
    usableForRepairGate: true,
    reason: 'anchors the high-penalty cis-crowding side of the peroxide OH torsion coordinate',
  },
  {
    key: 'ground_split_00_minus',
    label: 'effective ground-state splitting between 0 0+ and 0 0-',
    valueCm1: 10.978,
    comparatorType: 'computed',
    method: 'CCSD(T)/aug-cc-pVTZ effective torsional Hamiltonian',
    table: 'Table VI',
    usableForRepairGate: false,
    reason: 'useful sanity check for low trans barrier, but not a direct static barrier target',
  },
];

const extractedGeometry = {
  sourceTable: 'Table I',
  method: 'CCSD(T)-F12/VTZ',
  values: {
    O1O2Angstrom: 1.4463,
    C3O1Angstrom: 1.4117,
    H4O2Angstrom: 0.9631,
    C3O1O2Degrees: 105.5,
    H4O2O1Degrees: 100.0,
    H4O2O1C3Degrees: 111.9,
  },
  usage:
    'geometry can seed a CH3OOH-specific scoring scaffold, but it is not sufficient by itself to score the repair candidate without freezing a CH3OOH coordinate model',
};

const scoringGate = {
  status: 'source values extracted; scoring still blocked until model-consumption script is frozen',
  allowedNextStep:
    'create a CH3OOH scoring script that consumes this extraction artifact, uses alpha as the OH torsion coordinate, and compares predicted ordering against Vtrans_YH << Vcis_YH',
  blockedActions: [
    'do not tune release strength/onset/span after seeing these values',
    'do not count a computed-comparator pass as experimental validation',
    'do not score methyl torsion V3 as a peroxide anti-planar release success',
    'do not change the reserved target unless this extraction artifact is marked failed',
  ],
};

const report = {
  source: 'peroxide-methyl-hydroperoxide-source-extraction.mjs',
  date: '2026-06-23',
  reservedTarget,
  sourceReference: source,
  frozenRepair,
  torsionConvention,
  torsionGrid,
  extractedGeometry,
  extractedValues,
  scoringGate,
};

const markdown = `# Methyl Hydroperoxide Source Extraction

## Scope

This artifact extracts source-backed CH3OOH values after the target reservation and source-lock screen. It does not score the model, does not retune the peroxide anti-planar release parameters, and does not claim evidence increase.

Date: ${report.date}

## Source

${table(
  ['Field', 'Value'],
  [
    ['Citation', source.citation],
    ['DOI', source.doi],
    ['Local PDF', source.localPdf],
    ['Local extracted text', source.localText],
    ['Source type', source.sourceType],
  ],
)}

## Reserved Target And Frozen Repair

${table(
  ['Field', 'Value'],
  [
    ['Target', `${reservedTarget.molecule} (${reservedTarget.formula}; ${reservedTarget.alias})`],
    ['Reservation', reservedTarget.reservation],
    ['Source lock', reservedTarget.sourceLock],
    ['Frozen repair', `strength=${frozenRepair.releaseStrength}; onset=${frozenRepair.releaseOnsetDegrees}; span=${frozenRepair.releaseSpanDegrees}`],
    ['Frozen status', frozenRepair.status],
  ],
)}

## Torsion Convention

${table(
  ['Field', 'Value'],
  [
    ['Methyl torsion theta', torsionConvention.methylTorsionTheta],
    ['Hydroxyl torsion alpha', torsionConvention.hydroxylTorsionAlpha],
    ['Independent coordinates', torsionConvention.independentCoordinates.join('; ')],
    ['Scoring relevance', torsionConvention.scoringRelevance],
  ],
)}

## Source Torsion Grid

${table(
  ['Field', 'Value'],
  [
    ['Theta grid', torsionGrid.thetaDegrees.join(', ')],
    ['Alpha grid', torsionGrid.alphaDegrees.join(', ')],
    ['Planar symmetry', torsionGrid.planarSymmetryRule],
    ['Other coordinates', torsionGrid.nonOptimizedCoordinates],
  ],
)}

## Extracted Geometry

${table(
  ['Quantity', 'Value'],
  [
    ['Source table', extractedGeometry.sourceTable],
    ['Method', extractedGeometry.method],
    ['O1-O2', `${extractedGeometry.values.O1O2Angstrom} A`],
    ['C3-O1', `${extractedGeometry.values.C3O1Angstrom} A`],
    ['H4-O2', `${extractedGeometry.values.H4O2Angstrom} A`],
    ['C3-O1-O2', `${extractedGeometry.values.C3O1O2Degrees} deg`],
    ['H4-O2-O1', `${extractedGeometry.values.H4O2O1Degrees} deg`],
    ['H4-O2-O1-C3', `${extractedGeometry.values.H4O2O1C3Degrees} deg`],
    ['Usage', extractedGeometry.usage],
  ],
)}

## Extracted Torsion Values

${table(
  ['Key', 'Label', 'Value', 'Comparator', 'Method', 'Table', 'Usable for repair gate', 'Reason'],
  extractedValues.map((row) => [
    row.key,
    row.label,
    `${row.valueCm1} cm-1`,
    row.comparatorType,
    row.method,
    row.table,
    row.usableForRepairGate ? 'yes' : 'no',
    row.reason,
  ]),
)}

## Scoring Gate

${table(
  ['Field', 'Value'],
  [
    ['Status', scoringGate.status],
    ['Allowed next step', scoringGate.allowedNextStep],
  ],
)}

## Blocked Actions

${scoringGate.blockedActions.map((item) => `- ${item}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-methyl-hydroperoxide-source-extraction.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-methyl-hydroperoxide-source-extraction.md', outDir), markdown);

console.log(markdown);
