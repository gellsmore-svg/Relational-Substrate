import { mkdir, readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);
const reservation = JSON.parse(
  await readFile(
    new URL('peroxide-substituted-rotor-evidence-predeclaration.json', outDir),
    'utf8',
  ),
);

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const source = {
  citation:
    'A. C. P. Bitencourt, M. Ragni, G. S. Maciel, V. Aquilanti, and F. V. Prudente, J. Chem. Phys. 129, 154316 (2008)',
  doi: '10.1063/1.2992554',
  localPdf: 'analysis/source-cache/bitencourt-2008-o-o-torsion-levels.pdf',
  localText: 'analysis/source-cache/bitencourt-2008-o-o-torsion-levels.txt',
  repositoryUrl: 'https://repositorio.ufba.br/bitstream/ri/6014/1/C__Documents%20and%20Settings_rep...t.default_Cache_9_32_A9163d01.pdf',
  sourceType: 'B3LYP/6-311++G(3df,3pd) torsional barrier table with partition-function/torsional-level follow-up',
};

const target = {
  molecule: 'ethyl hydroperoxide',
  formula: 'C2H5OOH',
  sourceLabel: 'HOOEt',
  predeclaration: 'peroxide-substituted-rotor-evidence-predeclaration.mjs',
  predeclarationHash: reservation.predeclaration.hash,
};

const frozenRule = {
  name: 'substituted peroxide OH-torsion qualitative gate v0',
  releaseStrength: 0.25,
  releaseOnsetDegrees: 155,
  releaseSpanDegrees: 20,
  passFail:
    'predicted trans/cis penalty ratio < 0.35 and source trans/cis barrier ratio < 0.20, with predicted trans penalty lower than cis penalty',
};

const extractedGeometry = {
  sourceTable: 'Table I',
  method: 'B3LYP/6-311++G(3df,3pd)',
  values: {
    r1Angstrom: 0.966,
    ROOAngstrom: 1.451,
    r2Angstrom: 1.424,
    theta1Degrees: 100.4,
    theta2Degrees: 107.6,
    equilibriumDihedralDegrees: 114.5,
    a0Cm1: 21.3349,
    a1Cm1: 0.797795,
  },
};

const extractedBarriers = {
  sourceTable: 'Table I',
  method: 'B3LYP/6-311++G(3df,3pd)',
  values: {
    VcisCm1: 2270.55,
    VtransCm1: 236.46,
    transCisRatio: Number((236.46 / 2270.55).toFixed(4)),
  },
};

const potentialCoefficients = {
  sourceTable: 'Table II',
  expansion: 'V(w) = sum Ck cos(k w)',
  coefficientsCm1: {
    C0: 668.62,
    C1: 918.6,
    C2: 549.89,
    C3: 83.49,
    C4: 22.95,
    C5: 8.35,
  },
  rmsCm1: 4.27,
};

const extractionNotes = [
  'The previous non-locking search-index hint was for the HOOH diatom-diatom line, not the HOOEt row.',
  'The source-locked HOOEt row gives Vcis=2270.55 cm-1 and Vtrans=236.46 cm-1.',
  'This is computed-comparator evidence, not experimental barrier evidence.',
  'The predeclared gate was frozen before this source extraction.',
];

const report = {
  source: 'peroxide-ethyl-hydroperoxide-source-extraction.mjs',
  date: '2026-06-23',
  target,
  sourceReference: source,
  frozenRule,
  extractedGeometry,
  extractedBarriers,
  potentialCoefficients,
  extractionNotes,
};

const markdown = `# Ethyl Hydroperoxide Source Extraction

## Scope

This artifact extracts source-backed ethyl hydroperoxide torsion values after the substituted-peroxide evidence gate was predeclared. It does not retune the frozen rule.

Date: ${report.date}

## Source

${table(
  ['Field', 'Value'],
  [
    ['Citation', source.citation],
    ['DOI', source.doi],
    ['Local PDF', source.localPdf],
    ['Local extracted text', source.localText],
    ['Repository URL', source.repositoryUrl],
    ['Source type', source.sourceType],
  ],
)}

## Target And Frozen Rule

${table(
  ['Field', 'Value'],
  [
    ['Target', `${target.molecule} (${target.formula}; source label ${target.sourceLabel})`],
    ['Predeclaration', target.predeclaration],
    ['Predeclaration hash', target.predeclarationHash],
    ['Rule', frozenRule.name],
    ['Frozen release', `strength=${frozenRule.releaseStrength}; onset=${frozenRule.releaseOnsetDegrees}; span=${frozenRule.releaseSpanDegrees}`],
    ['Pass/fail', frozenRule.passFail],
  ],
)}

## Extracted Geometry

${table(
  ['Quantity', 'Value'],
  [
    ['Source table', extractedGeometry.sourceTable],
    ['Method', extractedGeometry.method],
    ['r1', `${extractedGeometry.values.r1Angstrom} A`],
    ['R_OO', `${extractedGeometry.values.ROOAngstrom} A`],
    ['r2', `${extractedGeometry.values.r2Angstrom} A`],
    ['theta1', `${extractedGeometry.values.theta1Degrees} deg`],
    ['theta2', `${extractedGeometry.values.theta2Degrees} deg`],
    ['equilibrium dihedral w', `${extractedGeometry.values.equilibriumDihedralDegrees} deg`],
    ['a0', `${extractedGeometry.values.a0Cm1} cm-1`],
    ['a1', `${extractedGeometry.values.a1Cm1} cm-1`],
  ],
)}

## Extracted Barriers

${table(
  ['Quantity', 'Value'],
  [
    ['Source table', extractedBarriers.sourceTable],
    ['Method', extractedBarriers.method],
    ['Vcis', `${extractedBarriers.values.VcisCm1} cm-1`],
    ['Vtrans', `${extractedBarriers.values.VtransCm1} cm-1`],
    ['Vtrans/Vcis', extractedBarriers.values.transCisRatio],
  ],
)}

## Potential Coefficients

${table(
  ['Coefficient', 'Value'],
  Object.entries(potentialCoefficients.coefficientsCm1).map(([key, value]) => [key, `${value} cm-1`]),
)}

RMS fit: ${potentialCoefficients.rmsCm1} cm-1.

## Notes

${extractionNotes.map((item) => `- ${item}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('peroxide-ethyl-hydroperoxide-source-extraction.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('peroxide-ethyl-hydroperoxide-source-extraction.md', outDir), markdown);

console.log(markdown);
