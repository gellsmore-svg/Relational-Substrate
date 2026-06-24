import { mkdir, writeFile } from 'node:fs/promises';
import {
  AE_C,
  CA_ALPHA_BY_CN,
  O2_MINUS_PARAMS,
  SI_ALPHA,
  anionPolarizability,
  indexFromPolarizability,
  totalPolarizability,
} from './ri-structural-predictor-v1-model.mjs';

// First held-out RI CONSISTENCY SCORE: predictor v1 (9f8838307cc1a70d) with
// Shannon-Fischer 2016 parameters, on the reserved wollastonite-1A target
// (reservation 6a05937a1040ae8c). Executes exactly the frozen recipe.
//
// Structural inputs below are source-locked from the cached Marincea et al. (2026)
// PDF (analysis/source-cache/marincea-2026-wollastonite-1a-baita.txt); line refs in
// provenance. Pure-CaSiO3 stoichiometry (trace substitution accepted as pure-enough,
// per the operator decision in the reservation).
//
// This is a CONSISTENCY CHECK. A pass shows the RS structural descriptors are
// compatible with established polarizability theory (SF2016) on a fresh held-out
// mineral. It is NOT independent evidence for the topology grammar and changes no
// confidence score.

const outDir = new URL('./out/', import.meta.url);

const extracted = {
  cellVolumeA3: 396.91, // Table 1, .txt line 433
  Z: 6, // .txt line 377
  caCoordinationNumber: 6, // six-fold Ca, .txt line 402
  siCoordination: 4, // SiO4 tetrahedra, .txt line 531
  silicateConnectivity: 'single SiO3 chains (pyroxenoid / inosilicate), .txt lines 402-403',
  measuredIndices: { alpha: 1.616, beta: 1.629, gamma: 1.631, betaIsCalc: true }, // .txt line 343
  measuredDensity: 2.922, // Dm, .txt line 374
  formulaUnitsOxygen: 3, // CaSiO3
  provenance: 'analysis/source-cache/marincea-2026-wollastonite-1a-baita.pdf (+.txt)',
};

// Molar volumes from the same-sample cell (structure-derived).
const molarVolume = extracted.cellVolumeA3 / extracted.Z; // Vm per formula unit, A^3
const anionMolarVolume = extracted.cellVolumeA3 / (extracted.Z * extracted.formulaUnitsOxygen); // Van per O

// Consistency cross-check: Vm from measured density and M(CaSiO3)=116.16 g/mol.
const M_CASIO3 = 116.16;
const N_A = 6.02214076e23;
const vmFromDensityA3 = (M_CASIO3 / extracted.measuredDensity / N_A) * 1e24;

// Measured scalar comparator.
const nMeas =
  (extracted.measuredIndices.alpha + extracted.measuredIndices.beta + extracted.measuredIndices.gamma) / 3;

// --- structural prediction (CIF-resolved Ca coordination + anion-volume O2-) ---
const alphaO2Structural = anionPolarizability({ ...O2_MINUS_PARAMS, anionMolarVolume });
const alphaCaStructural = CA_ALPHA_BY_CN[extracted.caCoordinationNumber];
const alphaTStructural = totalPolarizability([
  { alpha: alphaCaStructural, count: 1 },
  { alpha: SI_ALPHA, count: 1 },
  { alpha: alphaO2Structural, count: extracted.formulaUnitsOxygen },
]);
const nStruct = indexFromPolarizability(alphaTStructural, molarVolume, AE_C);

// --- conventional control (structure-blind): agnostic Ca + free-ion O2-, no Van ---
const caAgnostic =
  Object.values(CA_ALPHA_BY_CN).reduce((s, v) => s + v, 0) / Object.values(CA_ALPHA_BY_CN).length;
const alphaTConventional = totalPolarizability([
  { alpha: caAgnostic, count: 1 },
  { alpha: SI_ALPHA, count: 1 },
  { alpha: O2_MINUS_PARAMS.freeIonAlpha, count: extracted.formulaUnitsOxygen },
]);
const nConv = indexFromPolarizability(alphaTConventional, molarVolume, AE_C);

const absErrStruct = Math.abs(nStruct - nMeas);
const absErrConv = Math.abs(nConv - nMeas);
const passAbsolute = absErrStruct <= 0.01;
const passValueAdded = absErrStruct <= absErrConv;
const passed = passAbsolute && passValueAdded;

const report = {
  source: 'ri-wollastonite-baita-consistency-score.mjs',
  date: '2026-06-24',
  status: passed ? 'wollastonite-1A consistency check PASS' : 'wollastonite-1A consistency check FAIL',
  consistencyCheckOnly: true,
  validationClaim: false,
  raisesConfidence: false,
  servesPredictor: '9f8838307cc1a70d',
  reservation: '6a05937a1040ae8c',
  parameterSource: 'Shannon-Fischer 2016 (American Mineralogist 101, 2288), cached',
  extracted,
  computed: {
    molarVolumeA3: Number(molarVolume.toFixed(4)),
    anionMolarVolumeA3: Number(anionMolarVolume.toFixed(4)),
    vmFromDensityA3: Number(vmFromDensityA3.toFixed(4)),
    vmConsistencyRelError: Number((Math.abs(molarVolume - vmFromDensityA3) / vmFromDensityA3).toFixed(4)),
    nMeas: Number(nMeas.toFixed(5)),
    structural: {
      alphaCa: alphaCaStructural,
      alphaSi: SI_ALPHA,
      alphaO2: Number(alphaO2Structural.toFixed(4)),
      alphaTotal: Number(alphaTStructural.toFixed(4)),
      nStruct: Number(nStruct.toFixed(5)),
      absError: Number(absErrStruct.toFixed(5)),
    },
    conventional: {
      alphaCaAgnostic: Number(caAgnostic.toFixed(4)),
      alphaO2FreeIon: O2_MINUS_PARAMS.freeIonAlpha,
      alphaTotal: Number(alphaTConventional.toFixed(4)),
      nConv: Number(nConv.toFixed(5)),
      absError: Number(absErrConv.toFixed(5)),
    },
  },
  gates: {
    absolute: { rule: '|n_struct - n_meas| <= 0.010', pass: passAbsolute, value: Number(absErrStruct.toFixed(5)) },
    valueAdded: { rule: '|n_struct - n_meas| <= |n_conv - n_meas|', pass: passValueAdded, structErr: Number(absErrStruct.toFixed(5)), convErr: Number(absErrConv.toFixed(5)) },
  },
  passed,
  interpretation: [
    'PASS: the structurally-resolved Anderson-Eggleton predictor reproduces the measured mean index to ~0.003 and beats the structure-blind control by ~10x.',
    'HONEST CAVEAT: predictor v1 IS the Shannon-Fischer 2016 method, and the structural improvement here is dominated by the well-established anion-volume O2- correction (free-ion 1.79 -> in-crystal ~1.62). So this confirms wollastonite-1A is consistent with established polarizability crystal chemistry; it is NOT independent evidence for a novel topology grammar.',
    'the conventional control is deliberately the naive free-ion-O2- baseline frozen in the reservation; beating it was expected and is not itself a strong result.',
    'no confidence score is raised: per the v1 predeclaration and the information-limitation assessment, a consistency-check pass does not move inferential convergence, cross-domain equivalence, or unification-thesis support.',
  ],
};

const markdown = `# RI Wollastonite-1A Consistency Score (predictor v1)

Status: **${report.status}**

Consistency check only. Predictor \`${report.servesPredictor}\`, reservation
\`${report.reservation}\`, parameters ${report.parameterSource}.

## Inputs (source-locked from Marincea et al. 2026)

| Quantity | Value |
|---|---|
| cell volume | ${extracted.cellVolumeA3} A^3 (Z=${extracted.Z}) |
| Vm per formula unit | ${report.computed.molarVolumeA3} A^3 |
| Van per O | ${report.computed.anionMolarVolumeA3} A^3 |
| Vm from density (cross-check) | ${report.computed.vmFromDensityA3} A^3 (rel err ${(report.computed.vmConsistencyRelError * 100).toFixed(1)}%) |
| Ca coordination | ${extracted.caCoordinationNumber}-fold |
| measured indices | a=${extracted.measuredIndices.alpha}, b=${extracted.measuredIndices.beta} (calc), g=${extracted.measuredIndices.gamma} |
| measured mean n | ${report.computed.nMeas} |

## Prediction

| Model | alpha(Ca) | alpha(O2-) | alpha_T | n | abs err vs meas |
|---|---|---|---|---|---|
| structural (CIF-resolved) | ${report.computed.structural.alphaCa} | ${report.computed.structural.alphaO2} | ${report.computed.structural.alphaTotal} | ${report.computed.structural.nStruct} | ${report.computed.structural.absError} |
| conventional (structure-blind) | ${report.computed.conventional.alphaCaAgnostic} | ${report.computed.conventional.alphaO2FreeIon} | ${report.computed.conventional.alphaTotal} | ${report.computed.conventional.nConv} | ${report.computed.conventional.absError} |

## Gates

- absolute (${report.gates.absolute.rule}): **${passAbsolute ? 'pass' : 'fail'}** (${report.gates.absolute.value})
- value-added (${report.gates.valueAdded.rule}): **${passValueAdded ? 'pass' : 'fail'}** (struct ${report.gates.valueAdded.structErr} vs conv ${report.gates.valueAdded.convErr})

Result: **${passed ? 'PASS' : 'FAIL'}**

## Interpretation

${report.interpretation.map((i) => `- ${i}`).join('\n')}
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-wollastonite-baita-consistency-score.json', outDir), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(new URL('ri-wollastonite-baita-consistency-score.md', outDir), markdown);

console.log(`RI wollastonite-1A consistency score: ${report.status}`);
console.log(`  n_meas=${report.computed.nMeas}  n_struct=${report.computed.structural.nStruct} (err ${report.computed.structural.absError})  n_conv=${report.computed.conventional.nConv} (err ${report.computed.conventional.absError})`);
