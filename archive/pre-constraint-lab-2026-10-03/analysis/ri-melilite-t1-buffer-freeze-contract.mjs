import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const allowedDescriptors = [
  {
    descriptor: 'Ca scaffold baseline',
    expression: 'Ca/O or Ca per volume, only inside an explicit topology class',
    role: 'baseline covariate',
    frozenUse: 'may shift melilite RI upward relative to feldspar/glass calibration, but cannot absorb T1 chemistry',
  },
  {
    descriptor: 'T1 high-field term',
    expression: 'z/r2 using Shannon CN4 radius',
    role: 'Al-like T1 occupancy marker',
    frozenUse: 'separates trivalent high-field T1 cations from divalent Mg/Zn-like T1 cations',
  },
  {
    descriptor: 'T1 d10 class',
    expression: 'binary filled-d-shell marker for Zn-like T1 occupancy',
    role: 'buffer/gating marker',
    frozenUse: 'prevents Zn dielectric polarizability from being passed through additively',
  },
  {
    descriptor: 'T1 dielectric polarizability',
    expression: 'Qin et al. 2023 CN4 dielectric polarizability scale',
    role: 'ordered descriptor only',
    frozenUse: 'may be recorded, but cannot be used as a direct optical pass-through term without a separate frozen conversion rule',
  },
];

const rejectedDescriptors = [
  {
    descriptor: 'raw cation response = Al/O * cation field delta',
    rejection: 'collapses to zero for akermanite even though Ca scaffold remains optically important',
  },
  {
    descriptor: 'raw T1 polarizability pass-through',
    rejection: 'orders Al < Mg < Zn while measured melilite RI orders Mg < Al < Zn',
  },
  {
    descriptor: 'Ca scaffold as sufficient melilite variable',
    rejection: 'hardystonite overprediction shows Ca scaffold absorbed T1 chemistry variance',
  },
];

const frozenExpectations = [
  {
    expectation: 'Zn-like T1 occupancy',
    testablePattern: 'should not inherit the full positive Ca-scaffold uplift; raw Ca-scaffold-only predictions are expected to overpredict',
    falsifier: 'a fresh Zn-like T1 melilite lands accurately on the Ca-scaffold-only prediction without a Zn buffer',
  },
  {
    expectation: 'Mg-like T1 occupancy',
    testablePattern: 'should remain closer to the Ca-scaffold baseline than Zn-like occupancy does',
    falsifier: 'a fresh Mg-like T1 melilite shows a large hardystonite-like negative residual',
  },
  {
    expectation: 'Al-like high-field occupancy',
    testablePattern: 'should not be inferred from dielectric polarizability; field strength and charge class carry the distinction',
    falsifier: 'a fresh Al-like T1 row follows raw polarizability ordering rather than high-field class behavior',
  },
  {
    expectation: 'non-melilite Ca scaffold transfer',
    testablePattern: 'should weaken if melilite topology is the true scaffold carrier',
    falsifier: 'a Ca-rich non-melilite silicate is accurately predicted by the melilite Ca-scaffold baseline without topology adjustment',
  },
];

const nextTargetClasses = [
  {
    targetClass: 'same-class melilite repeat',
    examples: 'another Zn-, Mg-, or Al-bearing melilite with source-grade optical constants',
    value: 'strongest direct test because it checks an existing T1 class without adding a new T1 chemistry class',
    risk: 'hard to find natural, composition-clean rows with primary RI/density sources',
    priority: 1,
  },
  {
    targetClass: 'rankinite-like Ca silicate',
    examples: 'rankinite Ca3Si2O7',
    value: 'tests Ca-rich sorosilicate/scaffold response without Mg/Al/Zn T1 chemistry',
    risk: 'changes topology, so a failure separates melilite specificity from general Ca scaffold only if the source is strong',
    priority: 2,
  },
  {
    targetClass: 'wollastonite-like Ca chain silicate',
    examples: 'wollastonite CaSiO3',
    value: 'tests whether Ca scaffold transfers outside melilite into a well-sourced chain silicate',
    risk: 'topology shift is large; use as a scaffold-transfer falsifier, not a melilite model validation',
    priority: 3,
  },
  {
    targetClass: 'merwinite-like Ca-Mg silicate',
    examples: 'merwinite Ca3MgSi2O8',
    value: 'tests Mg-bearing Ca scaffold outside melilite',
    risk: 'mixes Mg chemistry and topology transfer, so it is less clean than rankinite or wollastonite',
    priority: 4,
  },
];

const contract = {
  source: 'ri-melilite-t1-buffer-freeze-contract.mjs',
  status: 'frozen model-form contract; no coefficients and no new validation score',
  allowedDescriptors,
  rejectedDescriptors,
  frozenExpectations,
  nextTargetClasses,
  decision:
    'Freeze the next RI validation around Ca scaffold baseline + T1 high-field + T1 d10 buffer. Do not use raw polarizability as a direct optical predictor.',
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Melilite T1-Buffer Freeze Contract

## Scope

This freezes the next model form after the hardystonite failure and source-anchored T1 polarizability diagnostic. It is not a fitted predictor. It has no new coefficients and scores no new material.

The purpose is to lock the allowed descriptors, rejected shortcuts, expected failure modes, and next target class before any fresh RI validation is attempted.

## Allowed Descriptors

${table(
  ['Descriptor', 'Expression', 'Role', 'Frozen use'],
  allowedDescriptors.map((row) => [row.descriptor, row.expression, row.role, row.frozenUse])
)}

## Rejected Shortcuts

${table(
  ['Descriptor', 'Reason rejected'],
  rejectedDescriptors.map((row) => [row.descriptor, row.rejection])
)}

## Frozen Expectations

${table(
  ['Expectation', 'Testable pattern', 'Falsifier'],
  frozenExpectations.map((row) => [row.expectation, row.testablePattern, row.falsifier])
)}

## Next Target Classes

${table(
  ['Priority', 'Target class', 'Examples', 'Value', 'Risk'],
  nextTargetClasses.map((row) => [row.priority, row.targetClass, row.examples, row.value, row.risk])
)}

## Decision

Freeze the next RI validation around:

1. Ca scaffold baseline;
2. T1 high-field term;
3. T1 d10 buffer;
4. topology class as an explicit gate.

Do not use raw T1 dielectric polarizability as a direct optical RI predictor. The strongest next target is a same-class melilite repeat if a source-grade row can be found. If not, rankinite-like Ca silicate is the cleanest scaffold-transfer test because it removes Mg/Al/Zn T1 chemistry while keeping a Ca-rich silicate substrate.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-melilite-t1-buffer-freeze-contract.json', outDir), JSON.stringify(contract, null, 2));
await writeFile(new URL('ri-melilite-t1-buffer-freeze-contract.md', outDir), markdown);

console.log(markdown);
