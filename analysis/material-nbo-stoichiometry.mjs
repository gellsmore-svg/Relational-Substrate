import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const cases = [
  {
    formula: 'SiO2',
    materialType: 'fully polymerized silica network',
    networkFormers: { Si: 1, Al: 0 },
    modifiers: { Na: 0, K: 0, Ca: 0, Mg: 0 },
    oxygen: 2,
    expectedNboT: 0,
    expectedChargeBalancedAl: 0,
  },
  {
    formula: 'Na2SiO3',
    materialType: 'sodium metasilicate network',
    networkFormers: { Si: 1, Al: 0 },
    modifiers: { Na: 2, K: 0, Ca: 0, Mg: 0 },
    oxygen: 3,
    expectedNboT: 2,
    expectedChargeBalancedAl: 0,
  },
  {
    formula: 'NaAlSi3O8',
    materialType: 'charge-balanced aluminosilicate network',
    networkFormers: { Si: 3, Al: 1 },
    modifiers: { Na: 1, K: 0, Ca: 0, Mg: 0 },
    oxygen: 8,
    expectedNboT: 0,
    expectedChargeBalancedAl: 1,
  },
  {
    formula: 'CaAl2Si2O8',
    materialType: 'charge-balanced calcium aluminosilicate framework',
    networkFormers: { Si: 2, Al: 2 },
    modifiers: { Na: 0, K: 0, Ca: 1, Mg: 0 },
    oxygen: 8,
    expectedNboT: 0,
    expectedChargeBalancedAl: 2,
  },
  {
    formula: 'KAlSi3O8',
    materialType: 'charge-balanced potassium aluminosilicate framework',
    networkFormers: { Si: 3, Al: 1 },
    modifiers: { Na: 0, K: 1, Ca: 0, Mg: 0 },
    oxygen: 8,
    expectedNboT: 0,
    expectedChargeBalancedAl: 1,
  },
];

function round(value, places = 4) {
  return Number(value.toFixed(places));
}

function modifierCharge(modifiers) {
  return modifiers.Na + modifiers.K + modifiers.Ca * 2 + modifiers.Mg * 2;
}

function monovalentModifierCharge(modifiers) {
  return modifiers.Na + modifiers.K;
}

function divalentModifierCharge(modifiers) {
  return modifiers.Ca * 2 + modifiers.Mg * 2;
}

function nboAccounting(testCase) {
  const tetrahedralCations = testCase.networkFormers.Si + testCase.networkFormers.Al;
  const chargeRequiredForAl = testCase.networkFormers.Al;
  const excessModifierCharge = Math.max(0, modifierCharge(testCase.modifiers) - chargeRequiredForAl);
  const nboT = tetrahedralCations > 0 ? excessModifierCharge / tetrahedralCations : 0;
  const chargeBalancedAl = Math.min(chargeRequiredForAl, modifierCharge(testCase.modifiers));

  return {
    formula: testCase.formula,
    materialType: testCase.materialType,
    tetrahedralCations,
    modifierCounts: testCase.modifiers,
    modifierCharge: modifierCharge(testCase.modifiers),
    monovalentModifierCharge: monovalentModifierCharge(testCase.modifiers),
    divalentModifierCharge: divalentModifierCharge(testCase.modifiers),
    chargeRequiredForAl,
    chargeBalancedAl,
    excessModifierCharge,
    nboT: round(nboT),
    expectedNboT: testCase.expectedNboT,
    nboTError: round(Math.abs(nboT - testCase.expectedNboT)),
    expectedChargeBalancedAl: testCase.expectedChargeBalancedAl,
    chargeBalancedAlError: round(Math.abs(chargeBalancedAl - testCase.expectedChargeBalancedAl)),
  };
}

const rows = cases.map(nboAccounting);

const checks = [
  {
    check: 'Fully polymerized silica has zero NBO/T',
    formula: 'SiO2',
    expected: 0,
    modelValue: rows.find((row) => row.formula === 'SiO2').nboT,
    pass: rows.find((row) => row.formula === 'SiO2').nboT === 0,
  },
  {
    check: 'Sodium metasilicate has NBO/T of 2',
    formula: 'Na2SiO3',
    expected: 2,
    modelValue: rows.find((row) => row.formula === 'Na2SiO3').nboT,
    pass: rows.find((row) => row.formula === 'Na2SiO3').nboT === 2,
  },
  {
    check: 'Albite-like aluminosilicate charge balances Al without NBO excess',
    formula: 'NaAlSi3O8',
    expected: 'NBO/T 0 and one charge-balanced Al',
    modelValue: `NBO/T ${rows.find((row) => row.formula === 'NaAlSi3O8').nboT}; charge-balanced Al ${
      rows.find((row) => row.formula === 'NaAlSi3O8').chargeBalancedAl
    }`,
    pass:
      rows.find((row) => row.formula === 'NaAlSi3O8').nboT === 0 &&
      rows.find((row) => row.formula === 'NaAlSi3O8').chargeBalancedAl === 1,
  },
  {
    check: 'Anorthite-like calcium aluminosilicate charge balances two Al without NBO excess',
    formula: 'CaAl2Si2O8',
    expected: 'NBO/T 0 and two charge-balanced Al',
    modelValue: `NBO/T ${rows.find((row) => row.formula === 'CaAl2Si2O8').nboT}; charge-balanced Al ${
      rows.find((row) => row.formula === 'CaAl2Si2O8').chargeBalancedAl
    }`,
    pass:
      rows.find((row) => row.formula === 'CaAl2Si2O8').nboT === 0 &&
      rows.find((row) => row.formula === 'CaAl2Si2O8').chargeBalancedAl === 2,
  },
  {
    check: 'Orthoclase-like potassium aluminosilicate charge balances Al without NBO excess',
    formula: 'KAlSi3O8',
    expected: 'NBO/T 0 and one charge-balanced Al',
    modelValue: `NBO/T ${rows.find((row) => row.formula === 'KAlSi3O8').nboT}; charge-balanced Al ${
      rows.find((row) => row.formula === 'KAlSi3O8').chargeBalancedAl
    }`,
    pass:
      rows.find((row) => row.formula === 'KAlSi3O8').nboT === 0 &&
      rows.find((row) => row.formula === 'KAlSi3O8').chargeBalancedAl === 1,
  },
];

const passed = checks.filter((check) => check.pass).length;
const diagnosis =
  passed === checks.length
    ? 'NBO/T charge-balance accounting matches the held-out silicate composition targets'
    : 'NBO/T charge-balance accounting failed at least one silicate composition target';

const json = {
  source: 'material-nbo-stoichiometry.mjs',
  status: 'quantitative material composition diagnostic; not a property simulator',
  diagnosis,
  rows,
  checks,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('material-nbo-stoichiometry.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate Material NBO/T Stoichiometry

## Scope

This diagnostic checks quantitative non-bridging-oxygen-per-tetrahedron accounting for simple silicate and aluminosilicate compositions.

It does not predict viscosity, durability, density, or diffusion. It checks whether the topology grammar can account for modifier charge, aluminium charge compensation, and NBO/T before making material-property claims.

## Summary

Diagnosis: ${diagnosis}.

| Formula | Material type | T cations | Modifier charge | Al charge need | Charge-balanced Al | Excess modifier charge | NBO/T | Expected NBO/T | NBO/T error |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
${rows
  .map(
    (row) =>
      `| ${row.formula} | ${row.materialType} | ${row.tetrahedralCations} | ${row.modifierCharge} | ${row.chargeRequiredForAl} | ${row.chargeBalancedAl} | ${row.excessModifierCharge} | ${row.nboT} | ${row.expectedNboT} | ${row.nboTError} |`
  )
  .join('\n')}

## Checks

| Check | Formula | Expected | Model value | Pass |
|---|---|---|---|---|
${checks
  .map((check) => `| ${check.check} | ${check.formula} | ${check.expected} | ${check.modelValue} | ${check.pass ? 'yes' : 'no'} |`)
  .join('\n')}

## Reading

This adds a narrow quantitative material target: charge-balance NBO/T. It is a prerequisite for material-property prediction, not a substitute for measured property calibration.
`;

await writeFile(new URL('material-nbo-stoichiometry.md', outDir), markdown);

console.log(`NBO/T checks passed: ${passed}/${checks.length}`);
console.log(`Diagnosis: ${diagnosis}`);
console.log(`Wrote ${new URL('material-nbo-stoichiometry.md', outDir).pathname}`);
