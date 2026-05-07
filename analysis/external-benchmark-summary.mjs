import { readFile, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

async function readJson(name) {
  return JSON.parse(await readFile(new URL(name, outDir), 'utf8'));
}

async function readOptionalJson(name) {
  try {
    return await readJson(name);
  } catch {
    return null;
  }
}

function round(value, places = 2) {
  return Number(value.toFixed(places));
}

const roadmap = await readJson('external-benchmark-roadmap.json');
const h2o2 = await readOptionalJson('external-h2o2-benchmark.json');
const h2o2Quant = await readOptionalJson('external-h2o2-quantitative-benchmark.json');
const h2o2Absolute = await readOptionalJson('external-h2o2-absolute-barrier-benchmark.json');
const hydrazineCation = await readOptionalJson('external-hydrazine-cation-torsion-benchmark.json');
const ethane = await readOptionalJson('external-ethane-benchmark.json');
const ethaneQuant = await readOptionalJson('external-ethane-quantitative-benchmark.json');
const ionic = await readOptionalJson('external-ionic-benchmark.json');
const boundaryBlind = await readOptionalJson('external-boundary-blind-benchmark.json');
const emOrdering = await readOptionalJson('external-em-ordering-benchmark.json');
const emCoulomb = await readOptionalJson('external-em-coulomb-comparator.json');
const emSuperposition = await readOptionalJson('external-em-superposition-comparator.json');
const emThreeSource = await readOptionalJson('external-em-three-source-comparator.json');
const emFieldLines = await readOptionalJson('external-em-field-line-topology-comparator.json');
const emEquipotential = await readOptionalJson('external-em-equipotential-comparator.json');
const emFieldMagnitude = await readOptionalJson('external-em-field-magnitude-comparator.json');
const silicateHeldout = await readOptionalJson('external-silicate-heldout-benchmark.json');
const roughnessHeldout = await readOptionalJson('external-roughness-heldout-benchmark.json');
const materialNbo = await readOptionalJson('external-material-nbo-quantitative-benchmark.json');
const hasH2O2AbsolutePass = h2o2Absolute?.status === 'absolute barrier pass';

const benchmarks = [
  h2o2 && {
    label: 'H2O2 torsion profile',
    evidenceLine: 'H2O2 molecular torsion',
    domain: 'molecular conformational ordering',
    conventionalComparator: 'experimental and quantum-chemistry torsional barrier/profile references',
    status: h2o2.status,
    score: h2o2.score,
    checksPassed: h2o2.checks.filter((check) => check.pass).length,
    checksTotal: h2o2.checks.length,
    limitation: hasH2O2AbsolutePass
      ? 'qualitative ordering pass; prior compression resolved by later anti-planar release revision'
      : 'qualitative pass; cis/trans barrier ratio is directionally right but compressed',
    confidenceEffect: h2o2.confidenceEffect,
  },
  h2o2Quant && {
    label: 'H2O2 quantitative torsion angle',
    evidenceLine: 'H2O2 molecular torsion',
    domain: 'molecular conformational ordering',
    conventionalComparator: 'experimental and quantum-chemistry torsional barrier/profile references',
    status: h2o2Quant.status,
    score: h2o2Quant.score,
    checksPassed: h2o2Quant.checks.filter((check) => check.pass).length,
    checksTotal: h2o2Quant.checks.length,
    limitation: h2o2Quant.metrics?.barrierRatioShortfallPct <= 5
      ? 'quantitative angle pass; prior cis/trans compression resolved in current grammar version'
      : 'quantitative angle pass; cis/trans barrier contrast improved but remains compressed',
    confidenceEffect: h2o2Quant.confidenceEffect,
  },
  ethane && {
    label: 'Ethane torsion profile',
    evidenceLine: 'ethane molecular torsion',
    domain: 'molecular conformational ordering',
    conventionalComparator: 'experimental rotational barrier and molecular orbital/hyperconjugation accounts',
    status: ethane.status,
    score: ethane.score,
    checksPassed: ethane.checks.filter((check) => check.pass).length,
    checksTotal: ethane.checks.length,
    limitation: 'qualitative pass; normalized score is not an energy model',
    confidenceEffect: ethane.confidenceEffect,
  },
  ethaneQuant && {
    label: 'Ethane quantitative torsion tolerance',
    evidenceLine: 'ethane molecular torsion',
    domain: 'molecular conformational ordering',
    conventionalComparator: 'experimental rotational barrier and molecular orbital/hyperconjugation accounts',
    status: ethaneQuant.status,
    score: ethaneQuant.score,
    checksPassed: ethaneQuant.checks.filter((check) => check.pass).length,
    checksTotal: ethaneQuant.checks.length,
    limitation: 'quantitative tolerance pass; endpoint is scale-anchored and intermediate points are high',
    confidenceEffect: ethaneQuant.confidenceEffect,
  },
  h2o2Absolute && {
    label: 'H2O2 absolute barrier transfer',
    evidenceLine: 'H2O2 molecular torsion',
    domain: 'molecular conformational energy scale',
    conventionalComparator: 'experimental and quantum-chemistry H2O2 torsional barrier heights',
    status: h2o2Absolute.status,
    score: h2o2Absolute.score,
    checksPassed: h2o2Absolute.checks.filter((check) => check.pass).length,
    checksTotal: h2o2Absolute.checks.length,
    limitation:
      h2o2Absolute.status === 'absolute barrier pass'
        ? 'absolute barrier transfer pass; still not a full torsional energy surface'
        : 'mixed diagnostic; ethane-derived scale matches cis but overpredicts trans, preserving ratio compression',
    confidenceEffect: h2o2Absolute.confidenceEffect,
  },
  hydrazineCation && {
    label: 'Hydrazine cation held-out torsion transfer',
    evidenceLine: 'held-out heteroatom torsion transfer',
    domain: 'held-out molecular torsion energy ordering',
    conventionalComparator: 'NIST CCCBDB experimental internal-rotation barriers for N2H4+',
    status: hydrazineCation.status,
    score: hydrazineCation.score,
    checksPassed: hydrazineCation.checks.filter((check) => check.pass).length,
    checksTotal: hydrazineCation.checks.length,
    limitation:
      hydrazineCation.status === 'held-out torsion transfer pass'
        ? 'held-out torsion transfer pass; still a proxy geometry, not a molecular solver'
        : 'qualitative ordering pass but quantitative barrier magnitudes are low under ethane scale',
    confidenceEffect: hydrazineCation.confidenceEffect,
  },
  ionic && {
    label: 'Ionic lattice order',
    evidenceLine: 'ionic lattice ordering',
    domain: 'ionic solid structure',
    conventionalComparator: 'standard crystallographic ionic-lattice coordination models',
    status: ionic.status,
    score: ionic.score,
    checksPassed: ionic.checks.filter((check) => check.pass).length,
    checksTotal: ionic.checks.length,
    limitation: 'qualitative pass; full 6:6 coordination and lattice energy are not modeled',
    confidenceEffect: ionic.confidenceEffect,
  },
  boundaryBlind && {
    label: 'Boundary phase prediction',
    evidenceLine: 'orientation-only boundary phase',
    domain: 'optical/electromagnetic boundary behaviour',
    conventionalComparator: 'wave boundary continuity and Fresnel-style optics expectations',
    status: boundaryBlind.status,
    score: boundaryBlind.score,
    checksPassed: boundaryBlind.checks.filter((check) => check.pass).length,
    checksTotal: boundaryBlind.checks.length,
    limitation: 'orientation evidence only; documented qualitative pass, not independently timestamped, and not counted as core convergence evidence',
    confidenceEffect: boundaryBlind.confidenceEffect,
    orientationOnly: true,
  },
  emOrdering && {
    label: 'Electromagnetic ordering',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'electromagnetic qualitative behavior',
    conventionalComparator: 'standard electric-charge, magnetic-field-line, and plane-EM-wave ordering expectations',
    status: emOrdering.status,
    score: emOrdering.score,
    checksPassed: emOrdering.checks.filter((check) => check.pass).length,
    checksTotal: emOrdering.checks.length,
    limitation: 'qualitative EM ordering pass; not a Maxwell solver, Coulomb calculation, or derivation of c',
    confidenceEffect: emOrdering.confidenceEffect,
  },
  emCoulomb && {
    label: 'EM-02 Coulomb comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'static-charge equation-level comparator',
    conventionalComparator: 'Coulomb-law direction, charge-product, and inverse-square relative force ordering',
    status: emCoulomb.status,
    score: emCoulomb.score,
    checksPassed: emCoulomb.checks.filter((check) => check.pass).length,
    checksTotal: emCoulomb.checks.length,
    limitation: 'equation-level relative comparator; not an absolute force model or Maxwell solver',
    confidenceEffect: emCoulomb.confidenceEffect,
  },
  emSuperposition && {
    label: 'EM-03 superposition comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'static electric-field superposition geometry',
    conventionalComparator: 'electric-field superposition, symmetry cancellation, and dipole field direction expectations',
    status: emSuperposition.status,
    score: emSuperposition.score,
    checksPassed: emSuperposition.checks.filter((check) => check.pass).length,
    checksTotal: emSuperposition.checks.length,
    limitation: 'finite two-source vector comparator; not a continuous field-line or Maxwell solver',
    confidenceEffect: emSuperposition.confidenceEffect,
  },
  emThreeSource && {
    label: 'EM-04 three-source comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'asymmetric static electric-field geometry',
    conventionalComparator: 'electric-field vector superposition for non-symmetric three-source layouts',
    status: emThreeSource.status,
    score: emThreeSource.score,
    checksPassed: emThreeSource.checks.filter((check) => check.pass).length,
    checksTotal: emThreeSource.checks.length,
    limitation: 'finite asymmetric vector comparator; not a continuous field-line, potential, or Maxwell solver',
    confidenceEffect: emThreeSource.confidenceEffect,
  },
  emFieldLines && {
    label: 'EM-05 field-line topology comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'continuous electromagnetic field-line topology',
    conventionalComparator: 'electric field-line source divergence and magnetic field-line closed-loop topology',
    status: emFieldLines.status,
    score: emFieldLines.score,
    checksPassed: emFieldLines.checks.filter((check) => check.pass).length,
    checksTotal: emFieldLines.checks.length,
    limitation: 'qualitative topology comparator; not a Maxwell solver, calibrated field model, or derivation of light speed',
    confidenceEffect: emFieldLines.confidenceEffect,
  },
  emEquipotential && {
    label: 'EM-06 equipotential geometry comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'static electric potential/equipotential geometry',
    conventionalComparator: 'point-charge scalar-potential superposition and field-as-negative-gradient relation',
    status: emEquipotential.status,
    score: emEquipotential.score,
    checksPassed: emEquipotential.checks.filter((check) => check.pass).length,
    checksTotal: emEquipotential.checks.length,
    limitation: 'electrostatic scalar-potential geometry comparator; not calibrated magnitude, conductors, propagation, or Maxwell dynamics',
    confidenceEffect: emEquipotential.confidenceEffect,
  },
  emFieldMagnitude && {
    label: 'EM-07 field magnitude comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'calibrated static electric-field magnitude',
    conventionalComparator: 'point-charge electric-field magnitude and vector components using E = kq/r^2',
    status: emFieldMagnitude.status,
    score: emFieldMagnitude.score,
    checksPassed: emFieldMagnitude.checks.filter((check) => check.pass).length,
    checksTotal: emFieldMagnitude.checks.length,
    limitation: 'calibrated point-charge field comparator; imports Coulomb constant and does not model conductors, media, propagation, or Maxwell dynamics',
    confidenceEffect: emFieldMagnitude.confidenceEffect,
  },
  silicateHeldout && {
    label: 'Silicate held-out network order',
    evidenceLine: 'silicate network topology',
    domain: 'network solid/material structure',
    conventionalComparator: 'standard silicate tetrahedral network and modifier/NBO descriptions',
    status: silicateHeldout.status,
    score: silicateHeldout.score,
    checksPassed: silicateHeldout.checks.filter((check) => check.pass).length,
    checksTotal: silicateHeldout.checks.length,
    limitation: 'held-out qualitative pass; graph-level material order, not glass-property prediction',
    confidenceEffect: silicateHeldout.confidenceEffect,
  },
  roughnessHeldout && {
    label: 'Roughness held-out interface order',
    evidenceLine: 'optical/interface boundary ordering',
    domain: 'rough optical/material interface behaviour',
    conventionalComparator: 'rough-surface specular/diffuse scattering models',
    status: roughnessHeldout.status,
    score: roughnessHeldout.score,
    checksPassed: roughnessHeldout.checks.filter((check) => check.pass).length,
    checksTotal: roughnessHeldout.checks.length,
    limitation: 'held-out interface pass; qualitative roughness ordering, not scatter calibration',
    confidenceEffect: roughnessHeldout.confidenceEffect,
  },
  materialNbo && {
    label: 'Material NBO/T quantitative accounting',
    evidenceLine: 'aluminosilicate NBO/T accounting',
    domain: 'glass composition accounting',
    conventionalComparator: 'standard NBO/T stoichiometric accounting in aluminosilicate glasses',
    status: materialNbo.status,
    score: materialNbo.score,
    checksPassed: materialNbo.checks.filter((check) => check.pass).length,
    checksTotal: materialNbo.checks.length,
    limitation: 'quantitative material pass; composition accounting, not measured property prediction',
    confidenceEffect: materialNbo.confidenceEffect,
  },
].filter(Boolean);

const benchmarkPasses = benchmarks.filter((benchmark) => benchmark.status.includes('pass')).length;
const totalChecks = benchmarks.reduce((sum, benchmark) => sum + benchmark.checksTotal, 0);
const passedChecks = benchmarks.reduce((sum, benchmark) => sum + benchmark.checksPassed, 0);
const coreEvidenceGroups = new Map([
  ['H2O2 molecular torsion', 'H2O2 molecular torsion'],
  ['ethane molecular torsion', 'ethane molecular torsion'],
  ['held-out heteroatom torsion transfer', 'held-out heteroatom torsion transfer'],
  ['ionic lattice ordering', 'ionic solid ordering'],
  ['electromagnetic field ordering', 'electromagnetic field geometry/topology'],
  ['silicate network topology', 'network/material structure'],
  ['aluminosilicate NBO/T accounting', 'network/material structure'],
  ['optical/interface boundary ordering', 'rough optical/interface ordering'],
]);
const coreBenchmarks = benchmarks.filter((benchmark) => !benchmark.orientationOnly);
const independentEvidenceLines = new Set(
  coreBenchmarks.map((benchmark) => coreEvidenceGroups.get(benchmark.evidenceLine) ?? benchmark.evidenceLine)
).size;
const orientationEvidenceLines = benchmarks.filter((benchmark) => benchmark.orientationOnly).length;
const externalCompletionPct = round(Math.min(benchmarks.length / roadmap.benchmarkTargets.length, 1) * 100);
const hasBlindStylePass = boundaryBlind?.status?.includes('qualitative pass');
const hasQuantitativePass = ethaneQuant?.status === 'quantitative tolerance pass';
const hasSecondNumericPass = h2o2Quant?.status === 'quantitative angle pass';
const hasTighterPeroxideRatio = h2o2Quant?.metrics?.barrierRatioCompressionFactor <= 2.5;
const hasHeldoutMaterialPass = silicateHeldout?.status === 'held-out qualitative pass';
const hasFactorTwoPeroxideRatio = h2o2Quant?.metrics?.barrierRatioCompressionFactor <= 2;
const hasHeldoutInterfacePass = roughnessHeldout?.status === 'held-out interface pass';
const hasQuantitativeMaterialPass = materialNbo?.status === 'quantitative material pass';
const hasEmOrderingPass = emOrdering?.status === 'qualitative EM ordering pass';
const hasEmCoulombPass = emCoulomb?.status === 'equation-level Coulomb ordering pass';
const hasEmSuperpositionPass = emSuperposition?.status === 'held-out superposition comparator pass';
const hasEmThreeSourcePass = emThreeSource?.status === 'non-symmetric three-source comparator pass';
const hasEmFieldLinePass = emFieldLines?.status === 'continuous field-line topology pass';
const hasEmEquipotentialPass = emEquipotential?.status === 'equipotential geometry comparator pass';
const hasEmFieldMagnitudePass = emFieldMagnitude?.status === 'calibrated field magnitude comparator pass';
const hasH2O2AbsoluteMixed = h2o2Absolute?.status === 'absolute barrier mixed diagnostic';
const hasHydrazineHeldoutPass = hydrazineCation?.status === 'held-out torsion transfer pass';
const hasHydrazineOrderingPass = hydrazineCation?.status === 'held-out torsion ordering pass with quantitative miss';

const confidence = {
  previousSandboxCompletionPct: roadmap.currentStatus.sandboxCompletionPct,
  updatedSandboxCompletionPct: hasEmFieldMagnitudePass ? 99.9 : hasEmEquipotentialPass ? 99.8 : hydrazineCation ? 99.7 : h2o2Absolute ? 99.6 : hasEmFieldLinePass ? 99.5 : hasEmThreeSourcePass ? 99.2 : hasEmSuperpositionPass ? 99 : hasEmCoulombPass ? 98.5 : hasEmOrderingPass ? 98 : hasQuantitativeMaterialPass ? 97 : hasHeldoutInterfacePass ? 96 : hasFactorTwoPeroxideRatio ? 94 : hasHeldoutMaterialPass ? 93 : hasTighterPeroxideRatio ? 91 : hasSecondNumericPass ? 90 : hasQuantitativePass ? 88 : hasBlindStylePass ? 84 : benchmarks.length >= 3 ? 80 : 76,
  previousInternalCoherenceOutOf10: roadmap.currentStatus.internalCoherenceConfidenceOutOf10,
  updatedInternalCoherenceOutOf10: hasEmFieldMagnitudePass ? 7.9 : hasEmEquipotentialPass ? 7.8 : hasH2O2AbsolutePass ? 7.7 : hasH2O2AbsoluteMixed ? 7.3 : hasQuantitativeMaterialPass ? 7.5 : hasHeldoutInterfacePass ? 7.4 : hasFactorTwoPeroxideRatio ? 7.3 : hasHeldoutMaterialPass ? 7.2 : hasTighterPeroxideRatio ? 7.1 : hasSecondNumericPass ? 7.0 : hasQuantitativePass ? 6.9 : hasBlindStylePass ? 6.7 : benchmarks.length >= 3 ? 6.5 : 6.3,
  previousInferentialConvergenceOutOf10: roadmap.currentStatus.inferentialConvergenceConfidenceOutOf10,
  updatedInferentialConvergenceOutOf10: hasEmFieldMagnitudePass ? 6.8 : hasEmEquipotentialPass ? 6.7 : hasHydrazineHeldoutPass ? 6.9 : hasHydrazineOrderingPass ? 6.6 : hasH2O2AbsolutePass ? 6.6 : hasH2O2AbsoluteMixed ? 6.1 : hasEmFieldLinePass ? 6.3 : hasEmThreeSourcePass ? 5.5 : hasEmSuperpositionPass ? 5.4 : hasEmCoulombPass ? 5.3 : hasEmOrderingPass ? 5.1 : hasQuantitativeMaterialPass ? 5.0 : hasHeldoutInterfacePass ? 4.8 : hasFactorTwoPeroxideRatio ? 4.6 : hasHeldoutMaterialPass ? 4.4 : hasTighterPeroxideRatio ? 4.1 : hasSecondNumericPass ? 4.0 : hasQuantitativePass ? 3.8 : hasBlindStylePass ? 3.4 : benchmarks.length >= 3 ? 3.0 : 2.7,
  crossDomainEquivalenceOutOf10: hasEmFieldMagnitudePass ? 5.9 : hasEmEquipotentialPass ? 5.8 : hasEmFieldLinePass ? 5.6 : hasEmThreeSourcePass ? 5.0 : hasEmSuperpositionPass ? 4.9 : hasEmCoulombPass ? 4.8 : hasEmOrderingPass ? 4.7 : hasQuantitativeMaterialPass ? 4.5 : hasHeldoutInterfacePass ? 4.3 : hasHeldoutMaterialPass ? 4.0 : hasBlindStylePass ? 3.4 : 3.0,
  evidenceIndependenceOutOf10: independentEvidenceLines >= 6 ? 4.5 : independentEvidenceLines >= 5 ? 4.0 : 3.2,
  unificationThesisSupportOutOf10: hasEmFieldMagnitudePass ? 5.5 : hasEmEquipotentialPass ? 5.4 : hasEmFieldLinePass ? 5.2 : hasEmThreeSourcePass ? 4.5 : hasEmSuperpositionPass ? 4.4 : hasEmCoulombPass ? 4.2 : hasEmOrderingPass ? 3.9 : hasQuantitativeMaterialPass ? 3.5 : hasHeldoutInterfacePass ? 3.3 : hasBlindStylePass ? 3.0 : 2.6,
  rationale:
    hasEmFieldMagnitudePass
      ? 'External anchoring now includes calibrated point-charge electric-field magnitude: a published worked example, absolute microcoulomb field magnitude, inverse-square distance scaling, charge linearity, and vector components. Inferential convergence rises only slightly because EM-07 imports the conventional Coulomb constant and remains inside one electromagnetic evidence line rather than deriving electrodynamics or opening a new domain.'
      : hasEmEquipotentialPass
      ? 'External anchoring now includes electrostatic equipotential geometry: scalar potential superposition, dipole zero-potential symmetry, field/equipotential perpendicularity, and the field-as-negative-gradient relation. Inferential convergence rises only slightly because EM-06 is still uncalibrated electrostatic geometry inside the same electromagnetic evidence line, not a new independent domain or Maxwell-equation validation.'
      : hasHydrazineHeldoutPass
      ? 'External anchoring now includes a held-out hydrazine cation torsion transfer pass. Anti-planar release generalizes beyond H2O2 under the ethane energy scale, supporting a further but still cautious convergence increase.'
      : hasHydrazineOrderingPass
      ? 'External anchoring now includes a held-out hydrazine cation torsion check. Anti-planar release transfers qualitatively and the 0/180 barrier ratio stays within tolerance, but absolute barrier magnitudes are low under the ethane scale, so inferential convergence is held at 6.6/10 rather than raised.'
      : hasH2O2AbsolutePass
      ? 'External anchoring now includes a successful H2O2 absolute barrier transfer from the ethane energy scale. Inferential convergence rises because the strongest prior peroxide limitation would be materially reduced without fitting H2O2 endpoints.'
      : hasH2O2AbsoluteMixed
      ? 'External anchoring now includes an explicit H2O2 absolute barrier transfer from the ethane energy scale. The result is mixed: the cis barrier lands close, but the trans barrier is overpredicted by roughly 2x, preserving the cis/trans compression as a live grammar limitation. Inferential convergence is therefore held near 6/10 rather than increased after EM-05.'
      : hasEmFieldLinePass
      ? 'External anchoring now includes continuous field-line topology: electric source-line divergence and magnetic closed-loop continuity under one integration grammar. Inferential convergence rises above 6/10 because EM evidence moves beyond finite vector fixtures into global topology, but remains cautious because the check is qualitative, not a Maxwell-equation solver or calibrated field model, and H2O2 compression remains unresolved.'
      : hasEmThreeSourcePass
      ? 'External anchoring now includes a non-symmetric three-source electric-field geometry comparator. Inferential convergence remains at 5.5/10 after review recalibration: EM evidence now survives pairwise ratios, symmetric superposition, and asymmetric multi-source vector targets, but these are still finite static vector checks within one evidence line; H2O2 compression remains the strongest grammar limitation; and the boundary-phase benchmark is orientation evidence only.'
      : hasEmSuperpositionPass
      ? 'External anchoring now includes a held-out electric-field superposition geometry comparator. Inferential convergence rises modestly because EM evidence generalizes from pairwise Coulomb direction/ratio checks to multi-source vector cancellation and dipole reversal, but remains below 6/10 because the comparator is still static, symmetric, and not a calibrated field or Maxwell solver.'
      : hasEmCoulombPass
      ? 'External anchoring now includes an equation-level Coulomb direction and relative-ratio comparator. Inferential convergence rises modestly because a post-closure EM benchmark survived stricter mathematical pressure, but remains moderate because the comparator is static, small, and not a full electromagnetic field model.'
      : hasEmOrderingPass
      ? 'External anchoring now includes a non-molecular/material electromagnetic ordering check. Inferential convergence rises slightly because the unification map has broader domain coverage, but remains moderate because the new EM benchmark is qualitative and not a Maxwell-equation or speed-of-light derivation.'
      : hasQuantitativeMaterialPass
      ? 'External anchoring now includes exact quantitative NBO/T composition accounting in addition to held-out material/interface checks. Inferential convergence is real but moderate: molecule torsion sub-checks collapse to one broader chemistry evidence group, the H2O2 ratio remains compressed, and boundary-phase evidence is orientation-only rather than independently timestamped.'
      : hasHeldoutInterfacePass
      ? 'External anchoring now includes held-out material and interface checks, plus peroxide factor-2 ratio compression. Confidence crosses 5/10, but remains moderate because the interface/material checks are qualitative and the project still lacks absolute physical calibration.'
      : hasFactorTwoPeroxideRatio
      ? 'Peroxide cis/trans compression now clears an independent factor-2 bound while preserving the held-out silicate pass and other external checks. Confidence remains below 5/10 because the peroxide comparison is still a ratio, not an absolute energy surface, and material-property prediction is not quantitative.'
      : hasHeldoutMaterialPass
      ? 'External anchoring now includes a held-out non-molecule material benchmark in addition to torsion, ionic, and boundary checks. Confidence rises, but remains below 5/10 because the held-out pass is qualitative and the peroxide energy-ratio compression remains unresolved.'
      : hasTighterPeroxideRatio
      ? 'Peroxide cis/trans compression improved enough to clear a tighter 2.5x ratio bound while preserving the non-scaled angle pass. Confidence rises only slightly because the ratio is still materially compressed and the held-out prediction gate remains open.'
      : hasSecondNumericPass
      ? 'External anchoring now includes two numeric checks: a broad ethane torsion-shape tolerance and a non-scaled H2O2 equilibrium-angle tolerance. Confidence rises only slightly because peroxide barrier contrast is still compressed and the strongest prediction remains blind-style rather than held out.'
      : hasQuantitativePass
      ? 'External anchoring now includes qualitative molecule/material/interface checks, a blind-style boundary prediction, and a predeclared quantitative ethane tolerance. Confidence crosses 4/10, but remains conservative because the quantitative check is broad and partly scale-anchored.'
      : hasBlindStylePass
      ? 'Three external anchors plus one blind-style boundary prediction pass qualitative checks. Confidence rises, but remains below 4/10 because the blind step is not historical, not quantitative, and not a physical simulator.'
      : benchmarks.length >= 3
      ? 'Two torsion benchmarks and one non-torsion ionic-order benchmark pass qualitative checks. Confidence rises modestly because external anchoring is broader, but it remains low until blind and quantitative targets pass.'
      : 'Two independent torsion benchmarks pass qualitative ordering checks, but neither benchmark is a quantitative prediction and both are close to existing calibration families.',
};

const remainingExternalGates = [
  'Move material checks from composition accounting to measured property calibration.',
  hasH2O2AbsolutePass
    ? hydrazineCation
      ? 'Move held-out torsion transfer from qualitative/ratiometric ordering toward calibrated absolute barrier magnitudes.'
      : 'Test anti-planar release on a new held-out torsion system without fitting its endpoints.'
    : h2o2Absolute
    ? 'Resolve transferred H2O2 trans-barrier overprediction without fitting H2O2 endpoints or breaking cis-barrier scale.'
    : 'Move peroxide from ratio-shape checks toward absolute barrier-height calibration.',
  'Move roughness/interface checks beyond qualitative ordering into calibrated scatter quantities.',
  ...(hasEmCoulombPass ? [] : ['Move electromagnetic ordering from qualitative checks toward explicit equation-level comparators.']),
  ...(hasEmSuperpositionPass ? [] : ['Move EM-02 from pairwise Coulomb ratios toward held-out superposition or field-geometry checks.']),
  ...(hasEmThreeSourcePass ? [] : ['Move EM-03 from symmetric two-source layouts toward non-symmetric three-source field geometry or calibrated field magnitude comparisons.']),
  ...(hasEmFieldLinePass ? [] : ['Move EM-04 from finite vector fixtures toward continuous field-line topology, equipotential geometry, or calibrated field magnitude comparisons.']),
  ...(hasEmEquipotentialPass ? [] : ['Move EM-05 from qualitative field-line topology toward equipotential geometry, calibrated field magnitude, or time-dependent propagation.']),
  ...(hasEmFieldMagnitudePass ? [] : ['Move EM-06 from electrostatic potential geometry toward calibrated field magnitude, conductors/material media, or time-dependent propagation.']),
  'Move EM-07 from calibrated point-charge fields toward conductors/material media or time-dependent propagation.',
];

const status =
  hasEmFieldMagnitudePass
    ? 'external anchoring broadened: calibrated field magnitude comparator passes'
    : hasEmEquipotentialPass
    ? 'external anchoring broadened: equipotential geometry comparator passes'
    : hasHydrazineHeldoutPass
    ? 'held-out torsion transfer confirms anti-planar release'
    : hasHydrazineOrderingPass
    ? 'held-out torsion ordering supports anti-planar release with quantitative miss'
    : hasH2O2AbsolutePass
    ? 'falsification pressure reduced: H2O2 absolute barrier transfer passes'
    : hasH2O2AbsoluteMixed
    ? 'falsification pressure sharpened: H2O2 absolute barrier transfer is mixed'
    : hasEmFieldLinePass
    ? 'external anchoring broadened: continuous field-line topology comparator passes'
    : hasEmThreeSourcePass
    ? 'external anchoring broadened: asymmetric three-source field comparator passes'
    : hasEmSuperpositionPass
    ? 'external anchoring broadened: electric-field superposition comparator passes'
    : hasEmCoulombPass
    ? 'external anchoring broadened: Coulomb equation comparator passes'
    : hasEmOrderingPass
    ? 'external anchoring broadened: qualitative electromagnetic ordering passes'
    : hasQuantitativeMaterialPass
    ? 'external anchoring broadened: quantitative material accounting passes'
    : hasHeldoutInterfacePass
    ? 'external anchoring broadened: held-out interface benchmark passes'
    : hasFactorTwoPeroxideRatio
    ? 'external anchoring broadened: peroxide factor-2 compression gate passes'
    : hasHeldoutMaterialPass
    ? 'external anchoring broadened: held-out material benchmark passes'
    : hasTighterPeroxideRatio
    ? 'external anchoring broadened: peroxide compression gate tightens'
    : hasSecondNumericPass
    ? 'external anchoring broadened: second numeric gate passes'
    : hasQuantitativePass
    ? 'external anchoring broadened: quantitative tolerance gate passes'
    : hasBlindStylePass
    ? 'external anchoring broadened: blind-style boundary prediction passes'
    : benchmarkPasses >= 3
    ? 'external anchoring broadened: torsion and ionic-order checks pass'
    : benchmarkPasses >= 2
      ? 'external anchoring started: qualitative torsion checks pass'
    : 'external anchoring incomplete: fewer than two qualitative checks pass';

const json = {
  source: 'external-benchmark-summary.mjs',
  status,
  externalCompletionPct,
  benchmarkPasses,
  passedChecks,
  totalChecks,
  independentEvidenceLines,
  orientationEvidenceLines,
  confidence,
  benchmarks,
  remainingExternalGates,
};

await writeFile(new URL('external-benchmark-summary.json', outDir), JSON.stringify(json, null, 2));

const markdown = `# Relational Substrate External Benchmark Summary

## Status

${status}.

| Measure | Value |
|---|---:|
| External benchmark targets covered | ${benchmarks.length}/${roadmap.benchmarkTargets.length} |
| Core independent evidence lines | ${independentEvidenceLines} |
| Orientation-only evidence lines | ${orientationEvidenceLines} |
| External benchmark completion | ${externalCompletionPct}% |
| Benchmark passes | ${benchmarkPasses}/${benchmarks.length} |
| Checks passed | ${passedChecks}/${totalChecks} |

## Confidence Update

| Measure | Previous | Updated |
|---|---:|---:|
| Sandbox completion | ${confidence.previousSandboxCompletionPct}% | ${confidence.updatedSandboxCompletionPct}% |
| Grammar internal coherence | ${confidence.previousInternalCoherenceOutOf10}/10 | ${confidence.updatedInternalCoherenceOutOf10}/10 |
| Inferential convergence | ${confidence.previousInferentialConvergenceOutOf10}/10 | ${confidence.updatedInferentialConvergenceOutOf10}/10 |
| Cross-domain equivalence demonstrated | n/a | ${confidence.crossDomainEquivalenceOutOf10}/10 |
| Independence of evidence lines | n/a | ${confidence.evidenceIndependenceOutOf10}/10 |
| Unification thesis support | n/a | ${confidence.unificationThesisSupportOutOf10}/10 |

${confidence.rationale}

## Benchmarks

| Benchmark | Evidence line | Domain | Comparator | Status | Checks | Score | Limitation |
|---|---|---|---|---|---:|---:|---|
${benchmarks
  .map(
    (benchmark) =>
      `| ${benchmark.label} | ${benchmark.evidenceLine} | ${benchmark.domain} | ${benchmark.conventionalComparator} | ${benchmark.status} | ${benchmark.checksPassed}/${benchmark.checksTotal} | ${benchmark.score} | ${benchmark.limitation} |`
  )
  .join('\n')}

## Remaining Gates

${remainingExternalGates.map((gate) => `- ${gate}`).join('\n')}

## Reading

The external anchors improve confidence that the current grammar can line up with known H2O2 torsion, ethane torsion, ionic-ordering, electromagnetic field-geometry/topology/potential/magnitude checks, roughness-scatter, and silicate/material-structure facts. The breadth count should be read as ${independentEvidenceLines} core independent evidence lines, plus ${orientationEvidenceLines} orientation-only boundary check, not ${benchmarks.length} fully independent domains. Silicate network and NBO/T collapse into one broader material-structure group, and EM-02 through EM-07 are depth checks inside one electromagnetic evidence line. The result supports moderate inferential convergence under an equivalence-with-unification standard, not proof of substrate existence or displacement of conventional domain models.
`;

await writeFile(new URL('external-benchmark-summary.md', outDir), markdown);

console.log(`External benchmark status: ${status}`);
console.log(`Updated inferential convergence: ${confidence.updatedInferentialConvergenceOutOf10}/10`);
console.log(`Wrote ${new URL('external-benchmark-summary.md', outDir).pathname}`);
