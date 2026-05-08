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
const emDielectricMedia = await readOptionalJson('external-em-dielectric-media-comparator.json');
const emWavePropagation = await readOptionalJson('external-em-wave-propagation-comparator.json');
const emBoundaryPropagation = await readOptionalJson('external-em-boundary-propagation-comparator.json');
const emObliqueFresnel = await readOptionalJson('external-em-oblique-fresnel-comparator.json');
const emMultilayerInterference = await readOptionalJson('external-em-multilayer-interference-comparator.json');
const emAbsorbingMedia = await readOptionalJson('external-em-absorbing-media-comparator.json');
const emRoughSurfaceScatter = await readOptionalJson('external-em-rough-surface-scatter-comparator.json');
const emDiffractionGrating = await readOptionalJson('external-em-diffraction-grating-comparator.json');
const emSingleSlitEnvelope = await readOptionalJson('external-em-single-slit-envelope-comparator.json');
const emDoubleSlitEnvelope = await readOptionalJson('external-em-double-slit-envelope-comparator.json');
const silicateHeldout = await readOptionalJson('external-silicate-heldout-benchmark.json');
const roughnessHeldout = await readOptionalJson('external-roughness-heldout-benchmark.json');
const materialNbo = await readOptionalJson('external-material-nbo-quantitative-benchmark.json');
const materialRefractiveIndex = await readOptionalJson('external-material-refractive-index-challenge.json');
const roughnessCalibratedScatter = await readOptionalJson('external-roughness-calibrated-scatter-benchmark.json');
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
  emDielectricMedia && {
    label: 'EM-08 dielectric media comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'ideal conductor/dielectric electrostatic media',
    conventionalComparator: 'parallel-plate capacitance, dielectric field reduction, conductor screening, and energy-density relations',
    status: emDielectricMedia.status,
    score: emDielectricMedia.score,
    checksPassed: emDielectricMedia.checks.filter((check) => check.pass).length,
    checksTotal: emDielectricMedia.checks.length,
    limitation: 'ideal electrostatic media comparator; imports permittivity and ideal conductor constraints rather than deriving material response or Maxwell dynamics',
    confidenceEffect: emDielectricMedia.confidenceEffect,
  },
  emWavePropagation && {
    label: 'EM-09 wave propagation comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'vacuum plane-wave electromagnetic propagation',
    conventionalComparator: 'plane-wave speed, E/B, transverse geometry, Poynting direction, impedance, and phase relations',
    status: emWavePropagation.status,
    score: emWavePropagation.score,
    checksPassed: emWavePropagation.checks.filter((check) => check.pass).length,
    checksTotal: emWavePropagation.checks.length,
    limitation: 'calibrated plane-wave relation comparator; imports c, permittivity, and permeability rather than deriving electrodynamics or radiation generation',
    confidenceEffect: emWavePropagation.confidenceEffect,
  },
  emBoundaryPropagation && {
    label: 'EM-10 boundary propagation comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'normal-incidence electromagnetic boundary propagation',
    conventionalComparator: 'dielectric-boundary reflection, transmission, phase inversion, speed change, and energy balance',
    status: emBoundaryPropagation.status,
    score: emBoundaryPropagation.score,
    checksPassed: emBoundaryPropagation.checks.filter((check) => check.pass).length,
    checksTotal: emBoundaryPropagation.checks.length,
    limitation: 'normal-incidence imported-index boundary comparator; not a full Fresnel, rough-interface, absorption, or Maxwell-equation solver',
    confidenceEffect: emBoundaryPropagation.confidenceEffect,
  },
  emObliqueFresnel && {
    label: 'EM-11 oblique Fresnel comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'oblique-incidence dielectric boundary propagation',
    conventionalComparator: 's/p Fresnel reflectance, Brewster angle, grazing trend, critical angle, and total internal reflection',
    status: emObliqueFresnel.status,
    score: emObliqueFresnel.score,
    checksPassed: emObliqueFresnel.checks.filter((check) => check.pass).length,
    checksTotal: emObliqueFresnel.checks.length,
    limitation: 'ideal lossless imported-index Fresnel comparator; not rough, absorbing, multilayer, diffraction, or Maxwell-equation optics',
    confidenceEffect: emObliqueFresnel.confidenceEffect,
  },
  emMultilayerInterference && {
    label: 'EM-12 multilayer interference comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'normal-incidence thin-film optical interference',
    conventionalComparator:
      'quarter-wave anti-reflection cancellation, off-design degradation, half-wave recurrence, and nonideal coating-index behavior',
    status: emMultilayerInterference.status,
    score: emMultilayerInterference.score,
    checksPassed: emMultilayerInterference.checks.filter((check) => check.pass).length,
    checksTotal: emMultilayerInterference.checks.length,
    limitation:
      'ideal lossless imported-index thin-film comparator; not rough, absorbing, broadband coating, graded-index, oblique, or Maxwell-equation optics',
    confidenceEffect: emMultilayerInterference.confidenceEffect,
  },
  emAbsorbingMedia && {
    label: 'EM-13 absorbing media comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'complex-index absorbing optical media',
    conventionalComparator:
      'complex-index reflectance, extinction-coefficient absorption, Beer-Lambert attenuation, thickness scaling, transparent-limit recovery, and energy accounting',
    status: emAbsorbingMedia.status,
    score: emAbsorbingMedia.score,
    checksPassed: emAbsorbingMedia.checks.filter((check) => check.pass).length,
    checksTotal: emAbsorbingMedia.checks.length,
    limitation:
      'narrow analytic absorbing-media comparator; not roughness scattering, lossy multilayer transfer, broadband spectra, nonlinear response, or Maxwell-equation optics',
    confidenceEffect: emAbsorbingMedia.confidenceEffect,
  },
  emRoughSurfaceScatter && {
    label: 'EM-14 rough-surface scatter comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'calibrated rough optical boundary scatter',
    conventionalComparator:
      'Bennett-Porteus total integrated scatter, specular-loss factor, roughness scaling, wavelength scaling, incidence-angle scaling, smooth-limit recovery, and reflected-energy budget',
    status: emRoughSurfaceScatter.status,
    score: emRoughSurfaceScatter.score,
    checksPassed: emRoughSurfaceScatter.checks.filter((check) => check.pass).length,
    checksTotal: emRoughSurfaceScatter.checks.length,
    limitation:
      'smooth-surface roughness/TIS comparator; not full BRDF, PSD integration, deep roughness, broadband spectra, diffraction, or Maxwell-equation optics',
    confidenceEffect: emRoughSurfaceScatter.confidenceEffect,
  },
  emDiffractionGrating && {
    label: 'EM-15 diffraction grating comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'periodic-aperture optical diffraction',
    conventionalComparator:
      'grating-equation order angles, spectral dispersion, central-order non-dispersion, order symmetry, order cutoff, and screen-position scaling',
    status: emDiffractionGrating.status,
    score: emDiffractionGrating.score,
    checksPassed: emDiffractionGrating.checks.filter((check) => check.pass).length,
    checksTotal: emDiffractionGrating.checks.length,
    limitation:
      'scalar grating-equation comparator; not finite-envelope, blaze-efficiency, broadband-intensity, vector-diffraction, radiation-generation, or Maxwell-equation optics',
    confidenceEffect: emDiffractionGrating.confidenceEffect,
  },
  emSingleSlitEnvelope && {
    label: 'EM-16 single-slit envelope comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'finite-aperture scalar optical diffraction',
    conventionalComparator:
      'single-slit minima, sinc-squared intensity envelope, central maximum, side-lobe relative intensity, wavelength scaling, slit-width scaling, symmetry, and screen-position mapping',
    status: emSingleSlitEnvelope.status,
    score: emSingleSlitEnvelope.score,
    checksPassed: emSingleSlitEnvelope.checks.filter((check) => check.pass).length,
    checksTotal: emSingleSlitEnvelope.checks.length,
    limitation:
      'scalar single-slit Fraunhofer comparator; not double-slit interference, grating combs, vector diffraction, broadband intensities, resolving power, radiation-generation, or Maxwell-equation optics',
    confidenceEffect: emSingleSlitEnvelope.confidenceEffect,
  },
  emDoubleSlitEnvelope && {
    label: 'EM-17 double-slit envelope comparator',
    evidenceLine: 'electromagnetic field ordering',
    domain: 'two-aperture scalar optical diffraction',
    conventionalComparator:
      'double-slit fringe spacing, constructive/destructive conditions, single-slit envelope modulation, missing orders, slit-separation scaling, wavelength scaling, symmetry, and screen-position mapping',
    status: emDoubleSlitEnvelope.status,
    score: emDoubleSlitEnvelope.score,
    checksPassed: emDoubleSlitEnvelope.checks.filter((check) => check.pass).length,
    checksTotal: emDoubleSlitEnvelope.checks.length,
    limitation:
      'scalar double-slit Fraunhofer comparator; exercises route/closure/phase/continuity but does not exercise charge non-trivially; not full vector diffraction, broadband intensity prediction, resolving power, aperture aberrations, radiation-generation, or Maxwell-equation optics',
    confidenceEffect: emDoubleSlitEnvelope.confidenceEffect,
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
  roughnessCalibratedScatter && {
    label: 'Roughness calibrated scatter quantity',
    evidenceLine: 'optical/interface boundary ordering',
    domain: 'calibrated rough optical/interface scatter',
    conventionalComparator:
      'Bennett-Porteus total integrated scatter, specular fraction, roughness scaling, wavelength scaling, and reflected-budget closure',
    status: roughnessCalibratedScatter.status,
    score: roughnessCalibratedScatter.score,
    checksPassed: roughnessCalibratedScatter.checks.filter((check) => check.pass).length,
    checksTotal: roughnessCalibratedScatter.checks.length,
    limitation:
      'calibrated smooth-surface TIS comparator; imports conventional roughness-scatter relation and does not model BRDFs, PSDs, broadband spectra, deep roughness, or Maxwell-equation surface scattering',
    confidenceEffect: roughnessCalibratedScatter.confidenceEffect,
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
  materialRefractiveIndex && {
    label: 'Material refractive-index challenge',
    evidenceLine: 'material measured property calibration',
    domain: 'measured silicate optical property',
    conventionalComparator:
      'source-anchored SiO2, Na2SiO3, and held-out NaAlSi3O8 refractive-index targets checked against current material grammar outputs',
    status: materialRefractiveIndex.status,
    score: materialRefractiveIndex.score,
    checksPassed: materialRefractiveIndex.checks.filter((check) => check.pass).length,
    checksTotal: materialRefractiveIndex.checks.length,
    limitation:
      'unresolved measured-property challenge; current grammar has a first-pass topology-only refractive-index proxy and a target-implied repair candidate that fails fresh anorthite validation, but no validated tolerance-clearing density, polarizability, Sellmeier, dispersion, or optical-property model',
    confidenceEffect: materialRefractiveIndex.confidenceEffect,
  },
].filter(Boolean);

function grammarVariablesFor(benchmark) {
  if (benchmark.orientationOnly) return 'route, phase, continuity; orientation-only';
  if (benchmark.label === 'EM-17 double-slit envelope comparator') {
    return 'route, closure, phase, continuity; charge not exercised non-trivially';
  }
  if (benchmark.label === 'Roughness calibrated scatter quantity') {
    return 'route, closure, phase, continuity; charge not exercised non-trivially';
  }
  if (benchmark.evidenceLine.includes('measured property')) {
    return 'charge, closure, continuity; phase predictor absent';
  }
  if (benchmark.evidenceLine === 'electromagnetic field ordering') {
    if (benchmark.label.includes('Coulomb') || benchmark.label.includes('superposition') || benchmark.label.includes('three-source') || benchmark.label.includes('field-line') || benchmark.label.includes('equipotential') || benchmark.label.includes('field magnitude') || benchmark.label.includes('dielectric')) {
      return 'charge, route, closure, phase, continuity';
    }
    return 'route, closure, phase, continuity; charge imported or inactive';
  }
  if (benchmark.evidenceLine.includes('torsion')) return 'route, closure, phase';
  if (benchmark.evidenceLine.includes('ionic')) return 'charge, closure, continuity';
  if (benchmark.evidenceLine.includes('silicate') || benchmark.evidenceLine.includes('NBO')) {
    return 'charge, closure, continuity';
  }
  if (benchmark.evidenceLine.includes('interface')) return 'route, phase, continuity';
  return 'route, closure, phase, charge, continuity';
}

function grammarVariableTokensFor(benchmark) {
  if (benchmark.orientationOnly) return ['route', 'phase', 'continuity'];
  if (
    benchmark.label === 'EM-17 double-slit envelope comparator' ||
    benchmark.label === 'Roughness calibrated scatter quantity'
  ) {
    return ['route', 'closure', 'phase', 'continuity'];
  }
  if (benchmark.evidenceLine === 'electromagnetic field ordering') {
    if (benchmark.grammarVariablesExercised?.includes('charge,')) {
      return ['route', 'closure', 'phase', 'charge', 'continuity'];
    }
    return ['route', 'closure', 'phase', 'continuity'];
  }
  return benchmark.grammarVariablesExercised
    .split(';')[0]
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

for (const benchmark of benchmarks) {
  benchmark.grammarVariablesExercised = grammarVariablesFor(benchmark);
}

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
  ['material measured property calibration', 'network/material structure'],
  ['optical/interface boundary ordering', 'rough optical/interface ordering'],
]);
const coreBenchmarks = benchmarks.filter((benchmark) => !benchmark.orientationOnly);
const independentEvidenceLines = new Set(
  coreBenchmarks.map((benchmark) => coreEvidenceGroups.get(benchmark.evidenceLine) ?? benchmark.evidenceLine)
).size;
const orientationEvidenceLines = benchmarks.filter((benchmark) => benchmark.orientationOnly).length;
const externalCompletionPct = round(Math.min(benchmarks.length / roadmap.benchmarkTargets.length, 1) * 100);
const evidenceLineSummaries = Array.from(
  benchmarks.reduce((groups, benchmark) => {
    const group = coreEvidenceGroups.get(benchmark.evidenceLine) ?? benchmark.evidenceLine;
    const current = groups.get(group) ?? {
      evidenceLine: group,
      benchmarkCount: 0,
      checksPassed: 0,
      checksTotal: 0,
      variables: new Set(),
      orientationOnly: Boolean(benchmark.orientationOnly),
      benchmarks: [],
    };
    current.benchmarkCount += 1;
    current.checksPassed += benchmark.checksPassed;
    current.checksTotal += benchmark.checksTotal;
    current.orientationOnly = current.orientationOnly || Boolean(benchmark.orientationOnly);
    current.benchmarks.push(benchmark.label);
    for (const variable of grammarVariableTokensFor(benchmark)) {
      current.variables.add(variable);
    }
    groups.set(group, current);
    return groups;
  }, new Map()).values()
).map((group) => ({
  ...group,
  variables: Array.from(group.variables).join(', '),
}));
const hasBlindStylePass = boundaryBlind?.status?.includes('qualitative pass');
const hasQuantitativePass = ethaneQuant?.status === 'quantitative tolerance pass';
const hasSecondNumericPass = h2o2Quant?.status === 'quantitative angle pass';
const hasTighterPeroxideRatio = h2o2Quant?.metrics?.barrierRatioCompressionFactor <= 2.5;
const hasHeldoutMaterialPass = silicateHeldout?.status === 'held-out qualitative pass';
const hasFactorTwoPeroxideRatio = h2o2Quant?.metrics?.barrierRatioCompressionFactor <= 2;
const hasHeldoutInterfacePass = roughnessHeldout?.status === 'held-out interface pass';
const hasQuantitativeMaterialPass = materialNbo?.status === 'quantitative material pass';
const hasMaterialRefractiveIndexChallenge =
  materialRefractiveIndex?.status === 'measured material refractive-index challenge unresolved';
const hasRoughnessCalibratedScatterPass =
  roughnessCalibratedScatter?.status === 'calibrated roughness scatter pass';
const hasEmOrderingPass = emOrdering?.status === 'qualitative EM ordering pass';
const hasEmCoulombPass = emCoulomb?.status === 'equation-level Coulomb ordering pass';
const hasEmSuperpositionPass = emSuperposition?.status === 'held-out superposition comparator pass';
const hasEmThreeSourcePass = emThreeSource?.status === 'non-symmetric three-source comparator pass';
const hasEmFieldLinePass = emFieldLines?.status === 'continuous field-line topology pass';
const hasEmEquipotentialPass = emEquipotential?.status === 'equipotential geometry comparator pass';
const hasEmFieldMagnitudePass = emFieldMagnitude?.status === 'calibrated field magnitude comparator pass';
const hasEmDielectricMediaPass = emDielectricMedia?.status === 'dielectric media comparator pass';
const hasEmWavePropagationPass = emWavePropagation?.status === 'plane-wave propagation comparator pass';
const hasEmBoundaryPropagationPass = emBoundaryPropagation?.status === 'boundary propagation comparator pass';
const hasEmObliqueFresnelPass = emObliqueFresnel?.status === 'oblique Fresnel comparator pass';
const hasEmMultilayerInterferencePass =
  emMultilayerInterference?.status === 'multilayer interference comparator pass';
const hasEmAbsorbingMediaPass = emAbsorbingMedia?.status === 'absorbing media comparator pass';
const hasEmRoughSurfaceScatterPass =
  emRoughSurfaceScatter?.status === 'rough surface scatter comparator pass';
const hasEmDiffractionGratingPass = emDiffractionGrating?.status === 'diffraction grating comparator pass';
const hasEmSingleSlitEnvelopePass = emSingleSlitEnvelope?.status === 'single-slit envelope comparator pass';
const hasEmDoubleSlitEnvelopePass = emDoubleSlitEnvelope?.status === 'double-slit envelope comparator pass';
const hasH2O2AbsoluteMixed = h2o2Absolute?.status === 'absolute barrier mixed diagnostic';
const hasHydrazineHeldoutPass = hydrazineCation?.status === 'held-out torsion transfer pass';
const hasHydrazineOrderingPass = hydrazineCation?.status === 'held-out torsion ordering pass with quantitative miss';

const confidence = {
  previousSandboxCompletionPct: roadmap.currentStatus.sandboxCompletionPct,
  updatedSandboxCompletionPct: hasMaterialRefractiveIndexChallenge ? 99.999 : hasEmDoubleSlitEnvelopePass ? 99.998 : hasEmSingleSlitEnvelopePass ? 99.997 : hasEmDiffractionGratingPass ? 99.996 : hasEmRoughSurfaceScatterPass ? 99.994 : hasEmAbsorbingMediaPass ? 99.992 : hasEmMultilayerInterferencePass ? 99.99 : hasEmObliqueFresnelPass ? 99.985 : hasEmBoundaryPropagationPass ? 99.98 : hasEmWavePropagationPass ? 99.97 : hasEmDielectricMediaPass ? 99.95 : hasEmFieldMagnitudePass ? 99.9 : hasEmEquipotentialPass ? 99.8 : hydrazineCation ? 99.7 : h2o2Absolute ? 99.6 : hasEmFieldLinePass ? 99.5 : hasEmThreeSourcePass ? 99.2 : hasEmSuperpositionPass ? 99 : hasEmCoulombPass ? 98.5 : hasEmOrderingPass ? 98 : hasQuantitativeMaterialPass ? 97 : hasHeldoutInterfacePass ? 96 : hasFactorTwoPeroxideRatio ? 94 : hasHeldoutMaterialPass ? 93 : hasTighterPeroxideRatio ? 91 : hasSecondNumericPass ? 90 : hasQuantitativePass ? 88 : hasBlindStylePass ? 84 : benchmarks.length >= 3 ? 80 : 76,
  previousInternalCoherenceOutOf10: roadmap.currentStatus.internalCoherenceConfidenceOutOf10,
  updatedInternalCoherenceOutOf10: hasMaterialRefractiveIndexChallenge ? 8.0 : hasRoughnessCalibratedScatterPass ? 8.1 : hasEmDoubleSlitEnvelopePass ? 8.0 : hasEmSingleSlitEnvelopePass ? 7.9 : hasEmDiffractionGratingPass ? 7.8 : hasEmRoughSurfaceScatterPass ? 7.7 : hasEmAbsorbingMediaPass ? 7.6 : hasEmMultilayerInterferencePass ? 7.5 : hasEmObliqueFresnelPass ? 7.4 : hasEmBoundaryPropagationPass ? 7.3 : hasEmWavePropagationPass ? 7.2 : hasEmDielectricMediaPass ? 7.1 : hasEmFieldMagnitudePass ? 7.0 : hasEmEquipotentialPass ? 6.9 : hasH2O2AbsolutePass ? 7.7 : hasH2O2AbsoluteMixed ? 7.3 : hasQuantitativeMaterialPass ? 7.5 : hasHeldoutInterfacePass ? 7.4 : hasFactorTwoPeroxideRatio ? 7.3 : hasHeldoutMaterialPass ? 7.2 : hasTighterPeroxideRatio ? 7.1 : hasSecondNumericPass ? 7.0 : hasQuantitativePass ? 6.9 : hasBlindStylePass ? 6.7 : benchmarks.length >= 3 ? 6.5 : 6.3,
  previousInferentialConvergenceOutOf10: roadmap.currentStatus.inferentialConvergenceConfidenceOutOf10,
  updatedInferentialConvergenceOutOf10: hasMaterialRefractiveIndexChallenge ? 6.25 : hasRoughnessCalibratedScatterPass ? 6.3 : hasEmDoubleSlitEnvelopePass ? 6.2 : hasEmSingleSlitEnvelopePass ? 6.15 : hasEmDiffractionGratingPass ? 6.1 : hasEmRoughSurfaceScatterPass ? 6.05 : hasEmAbsorbingMediaPass ? 6.0 : hasEmMultilayerInterferencePass ? 5.95 : hasEmObliqueFresnelPass ? 5.9 : hasEmBoundaryPropagationPass ? 5.85 : hasEmWavePropagationPass ? 5.8 : hasEmDielectricMediaPass ? 5.75 : hasEmFieldMagnitudePass ? 5.7 : hasEmEquipotentialPass ? 5.65 : hasHydrazineHeldoutPass ? 6.0 : hasHydrazineOrderingPass ? 5.9 : hasH2O2AbsolutePass ? 5.8 : hasH2O2AbsoluteMixed ? 5.5 : hasEmFieldLinePass ? 5.6 : hasEmThreeSourcePass ? 5.5 : hasEmSuperpositionPass ? 5.4 : hasEmCoulombPass ? 5.3 : hasEmOrderingPass ? 5.1 : hasQuantitativeMaterialPass ? 5.0 : hasHeldoutInterfacePass ? 4.8 : hasFactorTwoPeroxideRatio ? 4.6 : hasHeldoutMaterialPass ? 4.4 : hasTighterPeroxideRatio ? 4.1 : hasSecondNumericPass ? 4.0 : hasQuantitativePass ? 3.8 : hasBlindStylePass ? 3.4 : benchmarks.length >= 3 ? 3.0 : 2.7,
  crossDomainEquivalenceOutOf10: hasRoughnessCalibratedScatterPass ? 5.7 : hasEmDoubleSlitEnvelopePass ? 5.5 : hasEmSingleSlitEnvelopePass ? 5.45 : hasEmDiffractionGratingPass ? 5.4 : hasEmRoughSurfaceScatterPass ? 5.35 : hasEmAbsorbingMediaPass ? 5.3 : hasEmMultilayerInterferencePass ? 5.25 : hasEmObliqueFresnelPass ? 5.2 : hasEmBoundaryPropagationPass ? 5.15 : hasEmWavePropagationPass ? 5.1 : hasEmDielectricMediaPass ? 5.05 : hasEmFieldMagnitudePass ? 5.0 : hasEmEquipotentialPass ? 4.9 : hasEmFieldLinePass ? 4.8 : hasEmThreeSourcePass ? 4.7 : hasEmSuperpositionPass ? 4.6 : hasEmCoulombPass ? 4.5 : hasEmOrderingPass ? 4.4 : hasQuantitativeMaterialPass ? 4.3 : hasHeldoutInterfacePass ? 4.2 : hasHeldoutMaterialPass ? 4.0 : hasBlindStylePass ? 3.4 : 3.0,
  evidenceIndependenceOutOf10: independentEvidenceLines >= 6 ? 4.5 : independentEvidenceLines >= 5 ? 4.0 : 3.2,
  unificationThesisSupportOutOf10: hasRoughnessCalibratedScatterPass ? 5.2 : hasEmDoubleSlitEnvelopePass ? 5.0 : hasEmSingleSlitEnvelopePass ? 4.95 : hasEmDiffractionGratingPass ? 4.9 : hasEmRoughSurfaceScatterPass ? 4.85 : hasEmAbsorbingMediaPass ? 4.8 : hasEmMultilayerInterferencePass ? 4.75 : hasEmObliqueFresnelPass ? 4.7 : hasEmBoundaryPropagationPass ? 4.65 : hasEmWavePropagationPass ? 4.6 : hasEmDielectricMediaPass ? 4.55 : hasEmFieldMagnitudePass ? 4.5 : hasEmEquipotentialPass ? 4.45 : hasEmFieldLinePass ? 4.4 : hasEmThreeSourcePass ? 4.3 : hasEmSuperpositionPass ? 4.2 : hasEmCoulombPass ? 4.1 : hasEmOrderingPass ? 3.9 : hasQuantitativeMaterialPass ? 3.5 : hasHeldoutInterfacePass ? 3.3 : hasBlindStylePass ? 3.0 : 2.6,
  rationale:
    hasMaterialRefractiveIndexChallenge
      ? 'External anchoring now includes an explicit measured material-property challenge, and it is unresolved: SiO2, Na2SiO3, held-out NaAlSi3O8, and fresh-validation CaAl2Si2O8 refractive-index targets are source-anchored; the current topology-only refractive-index proxy clears SiO2 but misses the material set, and the target-implied slope/framework-Al candidate fails fresh anorthite validation. Inferential convergence is held near 6/10 because the material-property gate remains open.'
      : hasRoughnessCalibratedScatterPass
      ? 'External anchoring now includes a calibrated roughness/interface scatter quantity: Bennett-Porteus total integrated scatter, specular fraction, roughness/wavelength scaling, and reflected-budget closure. Inferential convergence rises only slightly because this imports a conventional smooth-surface approximation and does not yet solve measured material properties, held-out torsion absolute magnitudes, full BRDFs, or Maxwell surface scattering.'
      : hasEmDoubleSlitEnvelopePass
      ? 'External anchoring now includes double-slit diffraction-envelope behavior, but the confidence scale has been recalibrated downward after review: EM-02 through EM-17 deepen one electromagnetic evidence line rather than opening new independent domains, and the latest additions remain scalar analytic comparators importing conventional equations and constants. The current reading is meaningful sandbox progress, not a near-decisive convergence claim.'
      : hasEmSingleSlitEnvelopePass
      ? 'External anchoring now includes single-slit diffraction-envelope behavior: aperture minima, sinc-squared side-lobe intensity, central maximum recovery, wavelength/slit-width scaling, symmetry, and screen-position mapping. Inferential convergence rises only slightly because EM-16 remains scalar Fraunhofer single-slit optics rather than vector diffraction, broadband intensity prediction, resolving power, radiation generation, or Maxwell optics.'
      : hasEmDiffractionGratingPass
      ? 'External anchoring now includes diffraction-grating behavior: grating-equation order angles, spectral angular dispersion, central-order non-dispersion, positive/negative order symmetry, order cutoff, and screen-position scaling. Inferential convergence rises only slightly because EM-15 remains a scalar periodic-aperture equation check rather than finite-envelope, blaze-efficiency, broadband-intensity, vector-diffraction, radiation-generation, or Maxwell optics.'
      : hasEmRoughSurfaceScatterPass
      ? 'External anchoring now includes calibrated rough-surface scatter behavior: Bennett-Porteus total integrated scatter, specular-loss factor, roughness scaling, wavelength scaling, incidence-angle scaling, smooth-limit recovery, and reflected-energy budgeting. Inferential convergence rises only slightly because EM-14 remains a smooth-surface analytic approximation rather than full BRDF, PSD, deep-roughness, broadband, diffraction, or Maxwell surface-scatter simulation.'
      : hasEmAbsorbingMediaPass
      ? 'External anchoring now includes absorbing optical media behavior: complex-index reflectance, extinction-coefficient absorption, Beer-Lambert attenuation, thickness scaling, transparent-limit recovery, and single-entry energy accounting. Inferential convergence rises only slightly because EM-13 remains a narrow analytic absorbing-media comparator rather than rough, broadband, nonlinear, thermal, or Maxwell material simulation.'
      : hasEmMultilayerInterferencePass
      ? 'External anchoring now includes thin-film interference behavior: quarter-wave anti-reflection cancellation, off-design wavelength degradation, half-wave recurrence, and nonideal coating-index partial improvement. Inferential convergence rises only slightly because EM-12 remains ideal lossless imported-index thin-film optics rather than rough, absorbing, broadband, or Maxwell coating simulation.'
      : hasEmObliqueFresnelPass
      ? 'External anchoring now includes oblique Fresnel behavior: s/p polarization split, Brewster-angle p-reflectance cancellation, grazing trend, critical angle, and total internal reflection. Inferential convergence rises only slightly because EM-11 remains ideal lossless imported-index optics rather than rough, absorbing, multilayer, or Maxwell boundary simulation.'
      : hasEmBoundaryPropagationPass
      ? 'External anchoring now includes normal-incidence boundary propagation: impedance/reflection splitting, phase inversion, speed change, and lossless energy balance. Inferential convergence rises only slightly because EM-10 remains an imported-index, normal-incidence boundary check rather than full Fresnel optics, rough media, or Maxwell boundary simulation.'
      : hasEmWavePropagationPass
      ? 'External anchoring now includes plane-wave propagation behavior: vacuum speed relation, E/B coupling, transverse field geometry, Poynting direction, impedance, and phase translation continuity. Inferential convergence reaches 7/10 only cautiously because EM-09 imports c, permittivity, and permeability rather than deriving electrodynamics or radiation generation.'
      : hasEmDielectricMediaPass
      ? 'External anchoring now includes ideal conductor/dielectric media behavior: parallel-plate capacitance scaling, dielectric field reduction, conductor interior screening, and energy-density consistency. Inferential convergence rises only slightly because EM-08 imports permittivity and ideal conductor constraints rather than deriving material response or solving time-dependent Maxwell dynamics.'
      : hasEmFieldMagnitudePass
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
  hasMaterialRefractiveIndexChallenge
    ? 'Replace or revise the failed refractive-index slope/framework-Al candidate, then validate on a new held-out material composition before promotion.'
    : 'Move material checks from composition accounting to measured property calibration.',
  hasH2O2AbsolutePass
    ? hydrazineCation
      ? 'Move held-out torsion transfer from qualitative/ratiometric ordering toward calibrated absolute barrier magnitudes.'
      : 'Test anti-planar release on a new held-out torsion system without fitting its endpoints.'
    : h2o2Absolute
    ? 'Resolve transferred H2O2 trans-barrier overprediction without fitting H2O2 endpoints or breaking cis-barrier scale.'
    : 'Move peroxide from ratio-shape checks toward absolute barrier-height calibration.',
  ...(hasRoughnessCalibratedScatterPass
    ? []
    : ['Move roughness/interface checks beyond qualitative ordering into calibrated scatter quantities.']),
  'Move calibrated roughness/interface checks beyond smooth-surface TIS into BRDF/PSD, measured scatter curves, or broadband surface response.',
  ...(hasEmCoulombPass ? [] : ['Move electromagnetic ordering from qualitative checks toward explicit equation-level comparators.']),
  ...(hasEmSuperpositionPass ? [] : ['Move EM-02 from pairwise Coulomb ratios toward held-out superposition or field-geometry checks.']),
  ...(hasEmThreeSourcePass ? [] : ['Move EM-03 from symmetric two-source layouts toward non-symmetric three-source field geometry or calibrated field magnitude comparisons.']),
  ...(hasEmFieldLinePass ? [] : ['Move EM-04 from finite vector fixtures toward continuous field-line topology, equipotential geometry, or calibrated field magnitude comparisons.']),
  ...(hasEmEquipotentialPass ? [] : ['Move EM-05 from qualitative field-line topology toward equipotential geometry, calibrated field magnitude, or time-dependent propagation.']),
  ...(hasEmFieldMagnitudePass ? [] : ['Move EM-06 from electrostatic potential geometry toward calibrated field magnitude, conductors/material media, or time-dependent propagation.']),
  ...(hasEmDielectricMediaPass ? [] : ['Move EM-07 from calibrated point-charge fields toward conductors/material media or time-dependent propagation.']),
  ...(hasEmWavePropagationPass ? [] : ['Move EM-08 from ideal conductor/dielectric media toward time-dependent propagation or material-response derivation.']),
  ...(hasEmBoundaryPropagationPass ? [] : ['Move EM-09 from imported-constant plane-wave relations toward material-response derivation, boundary propagation, or radiation generation.']),
  ...(hasEmObliqueFresnelPass ? [] : ['Move EM-10 from normal-incidence imported-index boundaries toward oblique Fresnel behavior, rough/multilayer boundaries, or radiation generation.']),
  ...(hasEmMultilayerInterferencePass
    ? []
    : ['Move EM-11 from ideal lossless Fresnel optics toward rough/multilayer boundaries, absorption, or radiation generation.']),
  ...(hasEmAbsorbingMediaPass
    ? []
    : [
        'Move EM-12 from ideal lossless multilayer interference toward rough boundaries, absorption, broadband coatings, or radiation generation.',
      ]),
  ...(hasEmRoughSurfaceScatterPass
    ? []
    : [
        'Move EM-13 from narrow absorbing-media optics toward rough boundaries, calibrated scatter, broadband material spectra, or radiation generation.',
      ]),
  ...(hasEmDiffractionGratingPass
    ? []
    : [
        'Move EM-14 from smooth-surface TIS roughness approximation toward BRDF/PSD scatter, broadband material spectra, diffraction, or radiation generation.',
      ]),
  ...(hasEmSingleSlitEnvelopePass
    ? []
    : [
        'Move EM-15 from scalar grating-equation diffraction toward finite-envelope diffraction, resolving power, broadband intensities, or radiation generation.',
      ]),
  ...(hasEmDoubleSlitEnvelopePass
    ? []
    : [
        'Move EM-16 from scalar single-slit diffraction envelope toward double-slit/grating envelope coupling, resolving power, broadband intensities, or radiation generation.',
      ]),
  'Move EM-17 from scalar double-slit envelope coupling toward resolving power, broadband intensities, vector diffraction, or radiation generation.',
];

const status =
  hasMaterialRefractiveIndexChallenge
    ? 'external anchoring sharpened: measured material refractive-index challenge unresolved'
    : hasRoughnessCalibratedScatterPass
    ? 'external anchoring broadened: calibrated roughness scatter benchmark passes'
    : hasEmDoubleSlitEnvelopePass
    ? 'external anchoring broadened: double-slit envelope comparator passes'
    : hasEmSingleSlitEnvelopePass
    ? 'external anchoring broadened: single-slit envelope comparator passes'
    : hasEmDiffractionGratingPass
    ? 'external anchoring broadened: diffraction grating comparator passes'
    : hasEmRoughSurfaceScatterPass
    ? 'external anchoring broadened: rough-surface scatter comparator passes'
    : hasEmAbsorbingMediaPass
    ? 'external anchoring broadened: absorbing media comparator passes'
    : hasEmMultilayerInterferencePass
    ? 'external anchoring broadened: multilayer interference comparator passes'
    : hasEmObliqueFresnelPass
    ? 'external anchoring broadened: oblique Fresnel comparator passes'
    : hasEmBoundaryPropagationPass
    ? 'external anchoring broadened: boundary propagation comparator passes'
    : hasEmWavePropagationPass
    ? 'external anchoring broadened: wave propagation comparator passes'
    : hasEmDielectricMediaPass
    ? 'external anchoring broadened: dielectric media comparator passes'
    : hasEmFieldMagnitudePass
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
  evidenceLineSummaries,
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

## Independent Evidence Lines

| Evidence line | Benchmarks | Checks | Grammar variables exercised | Counting status |
|---|---:|---:|---|---|
${evidenceLineSummaries
  .map(
    (line) =>
      `| ${line.evidenceLine} | ${line.benchmarkCount} | ${line.checksPassed}/${line.checksTotal} | ${line.variables} | ${line.orientationOnly ? 'orientation-only' : 'core evidence'} |`
  )
  .join('\n')}

## Benchmarks by Evidence Line

${evidenceLineSummaries
  .map((line) => {
    const rows = benchmarks
      .filter((benchmark) => (coreEvidenceGroups.get(benchmark.evidenceLine) ?? benchmark.evidenceLine) === line.evidenceLine)
      .map(
        (benchmark) =>
          `| ${benchmark.label} | ${benchmark.domain} | ${benchmark.conventionalComparator} | ${benchmark.grammarVariablesExercised} | ${benchmark.status} | ${benchmark.checksPassed}/${benchmark.checksTotal} | ${benchmark.score} | ${benchmark.limitation} |`
      )
      .join('\n');
    return `### ${line.evidenceLine}

This evidence line contains ${line.benchmarkCount} benchmark${line.benchmarkCount === 1 ? '' : 's'} and ${line.checksPassed}/${line.checksTotal} passing checks. It is counted as ${line.orientationOnly ? 'orientation-only evidence' : 'one core independent evidence line'}, not as ${line.benchmarkCount} independent line${line.benchmarkCount === 1 ? '' : 's'}.

| Benchmark | Domain | Comparator | Grammar variables exercised | Status | Checks | Score | Limitation |
|---|---|---|---|---|---:|---:|---|
${rows}`;
  })
  .join('\n\n')}

## Remaining Gates

${remainingExternalGates.map((gate) => `- ${gate}`).join('\n')}

## Reading

The external anchors improve confidence that the current grammar can line up with known H2O2 torsion, ethane torsion, ionic-ordering, electromagnetic field-geometry/topology/potential/magnitude/media/propagation/boundary/Fresnel/multilayer/absorption/roughness-scatter/diffraction/interference-envelope checks, calibrated roughness/interface scatter accounting, and silicate/material-structure facts. The new measured material-property row is a deliberately unresolved refractive-index challenge, not a pass. The breadth count should be read as ${independentEvidenceLines} core independent evidence lines, plus ${orientationEvidenceLines} orientation-only boundary check, not ${benchmarks.length} fully independent domains. Silicate network, NBO/T, and the refractive-index challenge collapse into one broader material-structure group, roughness held-out and calibrated scatter remain one rough optical/interface line, and EM-02 through EM-17 are depth checks inside one electromagnetic evidence line. The result supports moderate inferential convergence under an equivalence-with-unification standard, not proof of substrate existence or displacement of conventional domain models.
`;

await writeFile(new URL('external-benchmark-summary.md', outDir), markdown);

console.log(`External benchmark status: ${status}`);
console.log(`Updated inferential convergence: ${confidence.updatedInferentialConvergenceOutOf10}/10`);
console.log(`Wrote ${new URL('external-benchmark-summary.md', outDir).pathname}`);
