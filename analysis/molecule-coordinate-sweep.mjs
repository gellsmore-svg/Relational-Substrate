import { mkdir, writeFile } from 'node:fs/promises';
import { clamp01, scoreCandidate } from './molecule-model.mjs';

const outDir = new URL('./out/', import.meta.url);

const defaultReferenceProvenance = {
  sourceName: 'NIST CCCBDB geometry data',
  sourceUrl: 'https://cccbdb.nist.gov/geometriesx.asp',
  status: 'rounded gas-phase geometry anchor',
  caution: 'Used as a classical calibration anchor only; it does not define AMS ontology.',
};

const referenceData = {
  H2: {
    family: 'diatomic covalent',
    bondLength: 0.741,
    bondAngle: null,
    routeBase: 0.82,
    valenceCapacity: 1,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Diatomic reference length, approximate gas-phase equilibrium scale.',
  },
  HCl: {
    family: 'diatomic covalent',
    bondLength: 1.275,
    bondAngle: null,
    routeBase: 0.8,
    valenceCapacity: 1,
    polarityVector: 1.05,
    provenance: defaultReferenceProvenance,
    notes: 'Polar diatomic reference length, approximate gas-phase equilibrium scale.',
  },
  F2: {
    family: 'diatomic covalent',
    bondLength: 1.412,
    bondAngle: null,
    routeBase: 0.78,
    valenceCapacity: 1,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Diatomic fluorine reference length, approximate gas-phase equilibrium scale.',
  },
  H2O: {
    family: 'bent polar',
    bondLength: 0.957,
    bondAngle: 104.5,
    routeBase: 0.72,
    valenceCapacity: 2,
    polarityVector: 1.85,
    provenance: defaultReferenceProvenance,
    notes: 'Bent water geometry, approximate O-H length and H-O-H angle.',
  },
  H2S: {
    family: 'bent polar',
    bondLength: 1.336,
    bondAngle: 92.1,
    routeBase: 0.69,
    valenceCapacity: 2,
    polarityVector: 0.97,
    provenance: defaultReferenceProvenance,
    notes: 'Bent hydrogen sulfide geometry, approximate S-H length and H-S-H angle.',
  },
  SO2: {
    family: 'bent polar',
    bondLength: 1.432,
    bondAngle: 119.5,
    routeBase: 0.76,
    valenceCapacity: 2,
    polarityVector: 1.63,
    provenance: defaultReferenceProvenance,
    notes: 'Bent sulfur dioxide geometry, approximate S-O length and O-S-O angle.',
  },
  CO2: {
    family: 'linear triatomic',
    bondLength: 1.162,
    bondAngle: 180,
    routeBase: 0.84,
    valenceCapacity: 4,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Linear carbon dioxide geometry, approximate C-O length.',
  },
  HCN: {
    family: 'linear triatomic',
    bondLength: 1.11,
    bondAngle: 180,
    routeBase: 0.82,
    valenceCapacity: 4,
    polarityVector: 2.98,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded linear proxy from separate H-C and C-N gas-phase distances',
    },
    notes: 'Linear hydrogen cyanide proxy, approximate H-C and C-N gas-phase distances.',
  },
  OCS: {
    family: 'linear triatomic',
    bondLength: 1.35,
    bondAngle: 180,
    routeBase: 0.8,
    valenceCapacity: 4,
    polarityVector: 0.71,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded linear proxy from separate C-O and C-S gas-phase distances',
    },
    notes: 'Linear carbonyl sulfide proxy, approximate C-O and C-S gas-phase distances.',
  },
  CH4: {
    family: 'tetrahedral covalent',
    bondLength: 1.087,
    bondAngle: 109.47,
    torsion: 70.53,
    routeBase: 0.76,
    valenceCapacity: 4,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Tetrahedral methane geometry, approximate C-H length and H-C-H angle.',
  },
  SiH4: {
    family: 'tetrahedral covalent',
    bondLength: 1.48,
    bondAngle: 109.47,
    torsion: 70.53,
    routeBase: 0.72,
    valenceCapacity: 4,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Tetrahedral silane geometry, approximate Si-H length and H-Si-H angle.',
  },
  CF4: {
    family: 'tetrahedral covalent',
    bondLength: 1.323,
    bondAngle: 109.47,
    torsion: 70.53,
    routeBase: 0.78,
    valenceCapacity: 4,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Tetrahedral carbon tetrafluoride geometry, approximate C-F length and F-C-F angle.',
  },
  BF3: {
    family: 'trigonal planar covalent',
    bondLength: 1.307,
    bondAngle: 120,
    torsion: 0,
    routeBase: 0.82,
    valenceCapacity: 3,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Trigonal planar boron trifluoride geometry, approximate B-F length and F-B-F angle.',
  },
  BCl3: {
    family: 'trigonal planar covalent',
    bondLength: 1.742,
    bondAngle: 120,
    torsion: 0,
    routeBase: 0.79,
    valenceCapacity: 3,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Trigonal planar boron trichloride geometry, approximate B-Cl length and Cl-B-Cl angle.',
  },
  H2CO: {
    family: 'asymmetric planar covalent',
    bondLength: 1.139,
    bondAngle: 120,
    torsion: 0,
    routeBase: 0.79,
    valenceCapacity: 3,
    polarityVector: 2.33,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded planar carbonyl proxy from gas-phase geometry anchors',
    },
    notes: 'Planar formaldehyde proxy with unequal C=O and C-H route lengths and strong carbonyl polarity.',
  },
  H2CS: {
    family: 'asymmetric planar covalent',
    bondLength: 1.352,
    bondAngle: 120,
    torsion: 0,
    routeBase: 0.76,
    valenceCapacity: 3,
    polarityVector: 1.68,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded planar thiocarbonyl proxy from gas-phase geometry anchors',
    },
    notes: 'Planar thioformaldehyde proxy with unequal C=S and C-H route lengths and weaker polarity than formaldehyde.',
  },
  NH3: {
    family: 'trigonal pyramidal covalent',
    bondLength: 1.012,
    bondAngle: 106.7,
    routeBase: 0.74,
    valenceCapacity: 3,
    polarityVector: 1.47,
    provenance: defaultReferenceProvenance,
    notes: 'Trigonal pyramidal ammonia geometry, approximate N-H length and H-N-H angle.',
  },
  PH3: {
    family: 'trigonal pyramidal covalent',
    bondLength: 1.42,
    bondAngle: 93.5,
    routeBase: 0.7,
    valenceCapacity: 3,
    polarityVector: 0.58,
    provenance: defaultReferenceProvenance,
    notes: 'Trigonal pyramidal phosphine geometry, approximate P-H length and H-P-H angle.',
  },
  O2: {
    family: 'diatomic covalent',
    bondLength: 1.208,
    bondAngle: null,
    routeBase: 0.86,
    valenceCapacity: 2,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Diatomic oxygen reference length, approximate gas-phase equilibrium scale.',
  },
  N2: {
    family: 'diatomic covalent',
    bondLength: 1.098,
    bondAngle: null,
    routeBase: 0.9,
    valenceCapacity: 3,
    polarityVector: 0,
    provenance: defaultReferenceProvenance,
    notes: 'Diatomic nitrogen reference length, approximate gas-phase equilibrium scale.',
  },
  CO: {
    family: 'diatomic covalent',
    bondLength: 1.128,
    bondAngle: null,
    routeBase: 0.86,
    valenceCapacity: 3,
    polarityVector: 0.12,
    provenance: defaultReferenceProvenance,
    notes: 'Polar carbon monoxide diatomic reference length, approximate gas-phase equilibrium scale.',
  },
  C2H2: {
    family: 'linear unsaturated covalent',
    bondLength: 1.203,
    bondAngle: 180,
    routeBase: 0.84,
    valenceCapacity: 4,
    polarityVector: 0,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded linear unsaturated proxy from gas-phase geometry anchors',
    },
    notes: 'Acetylene proxy using C-C route length as the representative unsaturated linear axis.',
  },
  C2H4: {
    family: 'trigonal planar covalent',
    bondLength: 1.339,
    bondAngle: 120,
    torsion: 0,
    routeBase: 0.82,
    valenceCapacity: 3,
    polarityVector: 0,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded planar unsaturated proxy from gas-phase geometry anchors',
    },
    notes: 'Ethene proxy with planar sp2 geometry and a C=C route anchor.',
  },
  C2H6: {
    family: 'rotatable covalent',
    bondLength: 1.535,
    bondAngle: 109.5,
    torsion: 60,
    routeBase: 0.78,
    valenceCapacity: 4,
    polarityVector: 0,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded staggered rotatable single-bond proxy',
    },
    notes: 'Ethane proxy for a saturated single-bond route with torsional rotatability.',
  },
  H2O2: {
    family: 'rotatable covalent',
    bondLength: 1.475,
    bondAngle: 94.8,
    torsion: 111.5,
    routeBase: 0.7,
    valenceCapacity: 2,
    polarityVector: 1.56,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded non-planar peroxide torsion proxy',
    },
    notes: 'Hydrogen peroxide proxy for torsion-sensitive non-planar O-O coupling.',
  },
  NO2: {
    family: 'bent polar',
    bondLength: 1.193,
    bondAngle: 134.3,
    routeBase: 0.78,
    valenceCapacity: 2,
    polarityVector: 0.32,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded bent radical proxy from gas-phase geometry anchors',
    },
    notes: 'Nitrogen dioxide proxy for asymmetric bent/radical behaviour; spin detail is outside current scope.',
  },
  NaCl: {
    family: 'ionic pair',
    bondLength: 2.36,
    bondAngle: null,
    routeBase: 0.68,
    valenceCapacity: 1,
    polarityVector: 2.36,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded gas-phase pair-distance proxy',
    },
    notes: 'Gas-phase NaCl pair distance proxy; ionic solid behaviour is not represented by this two-body model.',
  },
  LiF: {
    family: 'ionic pair',
    bondLength: 1.564,
    bondAngle: null,
    routeBase: 0.7,
    valenceCapacity: 1,
    polarityVector: 1.56,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded gas-phase pair-distance proxy',
    },
    notes: 'Gas-phase LiF pair distance proxy; ionic solid behaviour is not represented by this two-body model.',
  },
  benzene: {
    family: 'aromatic ring',
    bondLength: 1.397,
    bondAngle: 120,
    torsion: 0,
    routeBase: 0.96,
    valenceCapacity: 3,
    polarityVector: 0,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded planar aromatic proxy',
    },
    notes: 'Planar aromatic ring proxy, approximate C-C length and C-C-C angle.',
  },
  pyridine: {
    family: 'aromatic ring',
    bondLength: 1.39,
    bondAngle: 120,
    torsion: 0,
    routeBase: 0.93,
    valenceCapacity: 3,
    polarityVector: 0.65,
    provenance: {
      ...defaultReferenceProvenance,
      status: 'rounded planar aromatic heteroring proxy',
    },
    notes: 'Planar aromatic heteroring proxy, approximate ring bond length and ring angle.',
  },
};

const familyWeights = {
  'diatomic covalent': {
    valenceSatisfaction: 0.2,
    geometryFit: 0.12,
    angleStrain: 0.04,
    bondStrain: 0.28,
    polarityBalance: 0.08,
    routeContinuity: 0.22,
    ringClosure: 0,
    stericObstruction: 0.06,
  },
  'bent polar': {
    valenceSatisfaction: 0.16,
    geometryFit: 0.16,
    angleStrain: 0.18,
    bondStrain: 0.1,
    polarityBalance: 0.18,
    routeContinuity: 0.14,
    ringClosure: 0,
    stericObstruction: 0.08,
  },
  'trigonal pyramidal covalent': {
    valenceSatisfaction: 0.16,
    geometryFit: 0.17,
    angleStrain: 0.19,
    bondStrain: 0.11,
    polarityBalance: 0.17,
    routeContinuity: 0.13,
    ringClosure: 0,
    stericObstruction: 0.07,
  },
  'linear triatomic': {
    valenceSatisfaction: 0.16,
    geometryFit: 0.18,
    angleStrain: 0.22,
    bondStrain: 0.12,
    polarityBalance: 0.1,
    routeContinuity: 0.18,
    ringClosure: 0,
    stericObstruction: 0.04,
  },
  'linear unsaturated covalent': {
    valenceSatisfaction: 0.16,
    geometryFit: 0.18,
    angleStrain: 0.2,
    bondStrain: 0.16,
    polarityBalance: 0.08,
    routeContinuity: 0.18,
    ringClosure: 0,
    stericObstruction: 0.04,
  },
  'tetrahedral covalent': {
    valenceSatisfaction: 0.18,
    geometryFit: 0.18,
    angleStrain: 0.2,
    bondStrain: 0.12,
    polarityBalance: 0.08,
    routeContinuity: 0.16,
    ringClosure: 0,
    stericObstruction: 0.08,
  },
  'rotatable covalent': {
    valenceSatisfaction: 0.16,
    geometryFit: 0.16,
    angleStrain: 0.14,
    bondStrain: 0.13,
    polarityBalance: 0.11,
    routeContinuity: 0.14,
    ringClosure: 0,
    stericObstruction: 0.16,
  },
  'trigonal planar covalent': {
    valenceSatisfaction: 0.17,
    geometryFit: 0.18,
    angleStrain: 0.2,
    bondStrain: 0.12,
    polarityBalance: 0.08,
    routeContinuity: 0.17,
    ringClosure: 0,
    stericObstruction: 0.08,
  },
  'asymmetric planar covalent': {
    valenceSatisfaction: 0.16,
    geometryFit: 0.17,
    angleStrain: 0.18,
    bondStrain: 0.14,
    polarityBalance: 0.14,
    routeContinuity: 0.15,
    ringClosure: 0,
    stericObstruction: 0.06,
  },
  'aromatic ring': {
    valenceSatisfaction: 0.14,
    geometryFit: 0.16,
    angleStrain: 0.14,
    bondStrain: 0.12,
    polarityBalance: 0.06,
    routeContinuity: 0.18,
    ringClosure: 0.16,
    stericObstruction: 0.04,
  },
  'ionic pair': {
    valenceSatisfaction: 0.16,
    geometryFit: 0.12,
    angleStrain: 0.02,
    bondStrain: 0.18,
    polarityBalance: 0.22,
    routeContinuity: 0.12,
    ringClosure: 0,
    stericObstruction: 0.18,
  },
};

function scoreFamilyCandidate(candidate, family) {
  const weights = familyWeights[family];
  const score =
    candidate.valenceSatisfaction * weights.valenceSatisfaction +
    candidate.geometryFit * weights.geometryFit +
    (1 - candidate.angleStrain) * weights.angleStrain +
    (1 - candidate.bondStrain) * weights.bondStrain +
    candidate.polarityBalance * weights.polarityBalance +
    candidate.routeContinuity * weights.routeContinuity +
    candidate.ringClosure * weights.ringClosure +
    (1 - candidate.stericObstruction) * weights.stericObstruction;

  return clamp01(score);
}

function vec(x, y, z = 0) {
  return { x, y, z };
}

function add(a, b) {
  return vec(a.x + b.x, a.y + b.y, a.z + b.z);
}

function sub(a, b) {
  return vec(a.x - b.x, a.y - b.y, a.z - b.z);
}

function scale(a, factor) {
  return vec(a.x * factor, a.y * factor, a.z * factor);
}

function dot(a, b) {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}

function cross(a, b) {
  return vec(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}

function norm(a) {
  return Math.sqrt(dot(a, a));
}

function distance(a, b) {
  return norm(sub(a, b));
}

function average(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
}

function rms(values) {
  return values.length ? Math.sqrt(values.reduce((sum, value) => sum + value * value, 0) / values.length) : 0;
}

function maxOrZero(values) {
  return values.length ? Math.max(...values) : 0;
}

function standardDeviation(values) {
  if (!values.length) {
    return 0;
  }
  const mean = average(values);
  return Math.sqrt(values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length);
}

function angleDegrees(a, b, c) {
  const ba = sub(a, b);
  const bc = sub(c, b);
  const denominator = Math.max(norm(ba) * norm(bc), 1e-9);
  const cosine = Math.max(-1, Math.min(1, dot(ba, bc) / denominator));
  return (Math.acos(cosine) * 180) / Math.PI;
}

function torsionDegrees(a, b, c, d) {
  const b1 = sub(b, a);
  const b2 = sub(c, b);
  const b3 = sub(d, c);
  const n1 = cross(b1, b2);
  const n2 = cross(b2, b3);
  const m1 = cross(n1, scale(b2, 1 / Math.max(norm(b2), 1e-9)));
  return (Math.atan2(dot(m1, n2), dot(n1, n2)) * 180) / Math.PI;
}

function cloneAtoms(atoms) {
  return atoms.map((atom) => ({ ...atom, position: { ...atom.position } }));
}

function pairKey(a, b) {
  return [Math.min(a, b), Math.max(a, b)].join('-');
}

function rotatableStericClearance(definition, atoms) {
  if (!definition.rotatableGroups) {
    return null;
  }

  const distances = [];
  for (const [leftGroup, rightGroup] of definition.rotatableGroups) {
    for (const left of leftGroup) {
      for (const right of rightGroup) {
        distances.push(distance(atoms[left].position, atoms[right].position));
      }
    }
  }

  return distances.length ? Math.min(...distances) : null;
}

function deriveGeometryFromCoordinates(definition, atoms) {
  const bondLengths = definition.bonds.map(([a, b]) => distance(atoms[a].position, atoms[b].position));
  const bondLength = average(bondLengths);
  const bondAngle = average(definition.angles.map(([a, b, c]) => angleDegrees(atoms[a].position, atoms[b].position, atoms[c].position)));
  const torsion = average(definition.torsions.map(([a, b, c, d]) => Math.abs(torsionDegrees(atoms[a].position, atoms[b].position, atoms[c].position, atoms[d].position))));
  const ringClosureDistance = definition.ring ? distance(atoms[definition.ring[0]].position, atoms[definition.ring.at(-1)].position) : null;

  const chargeCentre = atoms.reduce((sum, atom) => add(sum, scale(atom.position, atom.partialCharge)), vec(0, 0, 0));
  const polarityVector = norm(chargeCentre);

  const bonded = new Set(definition.bonds.map(([a, b]) => pairKey(a, b)));
  const nonBondedDistances = [];
  for (let i = 0; i < atoms.length; i += 1) {
    for (let j = i + 1; j < atoms.length; j += 1) {
      if (!bonded.has(pairKey(i, j))) {
        nonBondedDistances.push(distance(atoms[i].position, atoms[j].position));
      }
    }
  }
  const rotatableClearance = rotatableStericClearance(definition, atoms);
  const stericClearance = rotatableClearance ?? (nonBondedDistances.length ? Math.min(...nonBondedDistances) : bondLength * 1.6);

  return {
    bondLength,
    bondAngle,
    torsion,
    ringClosureDistance,
    polarityVector,
    stericClearance,
    valenceMismatch: 0,
    routeBase: definition.routeBase,
    valenceCapacity: definition.valenceCapacity,
    ringWeight: definition.ring ? 1 : 0,
  };
}

function deriveCoordinateFeatures(definition, atoms, valenceMismatch) {
  const bonded = new Set(definition.bonds.map(([a, b]) => pairKey(a, b)));
  const bondLengths = definition.bonds.map(([a, b]) => distance(atoms[a].position, atoms[b].position));
  const angles = definition.angles.map(([a, b, c]) => angleDegrees(atoms[a].position, atoms[b].position, atoms[c].position));
  const torsions = definition.torsions.map(([a, b, c, d]) => Math.abs(torsionDegrees(atoms[a].position, atoms[b].position, atoms[c].position, atoms[d].position)));
  const ringAtoms = definition.ring ? definition.ring.slice(0, -1).map((index) => atoms[index].position) : [];
  const ringPlanarity = ringAtoms.length ? standardDeviation(ringAtoms.map((position) => position.z)) : null;
  const ringClosureDistance = definition.ring ? distance(atoms[definition.ring[0]].position, atoms[definition.ring.at(-1)].position) : null;

  const chargeCentre = atoms.reduce((sum, atom) => add(sum, scale(atom.position, atom.partialCharge)), vec(0, 0, 0));
  const nonBondedDistances = [];
  for (let i = 0; i < atoms.length; i += 1) {
    for (let j = i + 1; j < atoms.length; j += 1) {
      if (!bonded.has(pairKey(i, j))) {
        nonBondedDistances.push(distance(atoms[i].position, atoms[j].position));
      }
    }
  }
  const rotatableClearance = rotatableStericClearance(definition, atoms);
  const stericClearance = rotatableClearance ?? (nonBondedDistances.length ? Math.min(...nonBondedDistances) : average(bondLengths) * 1.6);

  return {
    bondLengths,
    angles,
    torsions,
    ringPlanarity,
    ringClosureDistance,
    polarityVector: norm(chargeCentre),
    nonBondedDistances,
    stericClearance,
    valenceMismatch,
    geometry: {
      bondLength: average(bondLengths),
      bondAngle: average(angles),
      torsion: average(torsions),
      ringClosureDistance,
      polarityVector: norm(chargeCentre),
      stericClearance,
      valenceMismatch,
      routeBase: definition.routeBase,
      valenceCapacity: definition.valenceCapacity,
      ringWeight: definition.ring ? 1 : 0,
    },
  };
}

function deriveCandidateFromCoordinateFeatures(definition, features, referenceFeatures, meta = {}) {
  const tolerances = definition.tolerances;
  const bondDeviations = features.bondLengths.map((length, index) =>
    clamp01(Math.abs(length - referenceFeatures.bondLengths[index]) / tolerances.bondLength)
  );
  const angleDeviations = features.angles.map((angle, index) =>
    clamp01(Math.abs(angle - referenceFeatures.angles[index]) / tolerances.bondAngle)
  );
  const torsionDeviations = features.torsions.map((torsion, index) =>
    clamp01(Math.abs(torsion - referenceFeatures.torsions[index]) / tolerances.torsion)
  );
  const polarityDeviation = clamp01(Math.abs(features.polarityVector - referenceFeatures.polarityVector) / tolerances.polarityVector);
  const stericDeviation = clamp01((referenceFeatures.stericClearance - features.stericClearance) / tolerances.stericClearance);
  const valenceDeviation = clamp01(Math.abs(features.valenceMismatch - referenceFeatures.valenceMismatch) / tolerances.valenceMismatch);
  const ringPlanarityDeviation =
    features.ringPlanarity === null ? 0 : clamp01(features.ringPlanarity / Math.max(tolerances.ringClosureDistance, 1e-9));

  const bondRms = rms(bondDeviations);
  const bondMax = maxOrZero(bondDeviations);
  const angleRms = rms(angleDeviations);
  const angleMax = maxOrZero(angleDeviations);
  const torsionRms = rms(torsionDeviations);
  const torsionMax = maxOrZero(torsionDeviations);

  const bondStrain = clamp01(bondRms * 0.65 + bondMax * 0.2 + valenceDeviation * 0.15);
  const angleStrain = clamp01(angleRms * 0.52 + angleMax * 0.18 + torsionRms * 0.16 + torsionMax * 0.06 + ringPlanarityDeviation * 0.08);
  const geometryFit = clamp01(1 - (bondRms * 0.2 + bondMax * 0.08 + angleRms * 0.22 + angleMax * 0.08 + torsionRms * 0.1 + ringPlanarityDeviation * 0.18 + stericDeviation * 0.14));
  const routeContinuity = clamp01(definition.routeBase - bondRms * 0.08 - angleRms * 0.1 - torsionRms * 0.08 - ringPlanarityDeviation * 0.18 - valenceDeviation * 0.16);
  const polarityBalance = clamp01(1 - polarityDeviation * 0.72 - valenceDeviation * 0.12);
  const ringClosure = definition.ring ? clamp01(1 - ringPlanarityDeviation * 0.7 - torsionRms * 0.2 - bondRms * 0.1) : 0;
  const stericObstruction = stericDeviation;
  const valenceSatisfaction = clamp01(1 - valenceDeviation * 0.82 - bondMax * 0.08);

  return {
    name: meta.name || 'coordinate candidate',
    type: meta.type || 'generated',
    mode: 'coordinate-distribution',
    geometry: features.geometry,
    coordinateMetrics: {
      bondRms,
      bondMax,
      angleRms,
      angleMax,
      torsionRms,
      torsionMax,
      ringPlanarity: ringPlanarityDeviation,
      polarity: polarityDeviation,
      steric: stericDeviation,
      valence: valenceDeviation,
    },
    valenceSatisfaction,
    geometryFit,
    angleStrain,
    bondStrain,
    polarityBalance,
    routeContinuity,
    ringClosure,
    stericObstruction,
  };
}

function waterAtoms() {
  const length = referenceData.H2O.bondLength;
  const halfAngle = (referenceData.H2O.bondAngle / 2) * (Math.PI / 180);
  return [
    { element: 'O', partialCharge: -0.6, position: vec(0, 0, 0) },
    { element: 'H', partialCharge: 0.3, position: vec(Math.sin(halfAngle) * length, Math.cos(halfAngle) * length, 0) },
    { element: 'H', partialCharge: 0.3, position: vec(-Math.sin(halfAngle) * length, Math.cos(halfAngle) * length, 0) },
  ];
}

function methaneAtoms() {
  const length = referenceData.CH4.bondLength / Math.sqrt(3);
  return [
    { element: 'C', partialCharge: -0.2, position: vec(0, 0, 0) },
    { element: 'H', partialCharge: 0.05, position: vec(length, length, length) },
    { element: 'H', partialCharge: 0.05, position: vec(length, -length, -length) },
    { element: 'H', partialCharge: 0.05, position: vec(-length, length, -length) },
    { element: 'H', partialCharge: 0.05, position: vec(-length, -length, length) },
  ];
}

function benzeneAtoms() {
  const side = referenceData.benzene.bondLength;
  return Array.from({ length: 6 }, (_, index) => {
    const theta = (index / 6) * Math.PI * 2;
    return { element: 'C', partialCharge: 0, position: vec(Math.cos(theta) * side, Math.sin(theta) * side, 0) };
  });
}

function diatomicDefinition(formula, leftElement, rightElement, leftCharge = 0, rightCharge = 0, toleranceOverrides = {}) {
  const data = referenceData[formula];
  return {
    formula,
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: leftElement, partialCharge: leftCharge, position: vec(-data.bondLength / 2, 0, 0) },
      { element: rightElement, partialCharge: rightCharge, position: vec(data.bondLength / 2, 0, 0) },
    ],
    bonds: [[0, 1]],
    angles: [],
    torsions: [],
    ring: null,
    tolerances: {
      bondLength: 0.18,
      bondAngle: 35,
      torsion: 60,
      ringClosureDistance: 0.45,
      polarityVector: 0.65,
      stericClearance: 0.45,
      valenceMismatch: 1,
      ...toleranceOverrides,
    },
  };
}

function bentTriatomicDefinition(formula, centerElement, outerElement, centerCharge, outerCharge, toleranceOverrides = {}) {
  const data = referenceData[formula];
  const halfAngle = (data.bondAngle / 2) * (Math.PI / 180);
  return {
    formula,
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: centerElement, partialCharge: centerCharge, position: vec(0, 0, 0) },
      { element: outerElement, partialCharge: outerCharge, position: vec(Math.sin(halfAngle) * data.bondLength, Math.cos(halfAngle) * data.bondLength, 0) },
      { element: outerElement, partialCharge: outerCharge, position: vec(-Math.sin(halfAngle) * data.bondLength, Math.cos(halfAngle) * data.bondLength, 0) },
    ],
    bonds: [
      [0, 1],
      [0, 2],
    ],
    angles: [[1, 0, 2]],
    torsions: [],
    ring: null,
    tolerances: {
      bondLength: 0.2,
      bondAngle: 30,
      torsion: 60,
      ringClosureDistance: 0.45,
      polarityVector: 0.8,
      stericClearance: 0.45,
      valenceMismatch: 1,
      ...toleranceOverrides,
    },
  };
}

function tetrahedralDefinition(formula, centerElement, outerElement, centerCharge, outerCharge, toleranceOverrides = {}) {
  const data = referenceData[formula];
  const length = data.bondLength / Math.sqrt(3);
  return {
    formula,
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: centerElement, partialCharge: centerCharge, position: vec(0, 0, 0) },
      { element: outerElement, partialCharge: outerCharge, position: vec(length, length, length) },
      { element: outerElement, partialCharge: outerCharge, position: vec(length, -length, -length) },
      { element: outerElement, partialCharge: outerCharge, position: vec(-length, length, -length) },
      { element: outerElement, partialCharge: outerCharge, position: vec(-length, -length, length) },
    ],
    bonds: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
    ],
    angles: [
      [1, 0, 2],
      [1, 0, 3],
      [1, 0, 4],
      [2, 0, 3],
      [2, 0, 4],
      [3, 0, 4],
    ],
    torsions: [[1, 2, 3, 4]],
    ring: null,
    tolerances: {
      bondLength: 0.22,
      bondAngle: 28,
      torsion: 45,
      ringClosureDistance: 0.45,
      polarityVector: 0.65,
      stericClearance: 0.55,
      valenceMismatch: 1,
      ...toleranceOverrides,
    },
  };
}

function trigonalPlanarDefinition(formula, centerElement, outerElement, centerCharge, outerCharge, toleranceOverrides = {}) {
  const data = referenceData[formula];
  return {
    formula,
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: centerElement, partialCharge: centerCharge, position: vec(0, 0, 0) },
      { element: outerElement, partialCharge: outerCharge, position: vec(data.bondLength, 0, 0) },
      { element: outerElement, partialCharge: outerCharge, position: vec(Math.cos((2 * Math.PI) / 3) * data.bondLength, Math.sin((2 * Math.PI) / 3) * data.bondLength, 0) },
      { element: outerElement, partialCharge: outerCharge, position: vec(Math.cos((4 * Math.PI) / 3) * data.bondLength, Math.sin((4 * Math.PI) / 3) * data.bondLength, 0) },
    ],
    bonds: [
      [0, 1],
      [0, 2],
      [0, 3],
    ],
    angles: [
      [1, 0, 2],
      [1, 0, 3],
      [2, 0, 3],
    ],
    torsions: [[1, 2, 0, 3]],
    ring: null,
    tolerances: {
      bondLength: 0.2,
      bondAngle: 22,
      torsion: 30,
      ringClosureDistance: 0.45,
      polarityVector: 0.7,
      stericClearance: 0.5,
      valenceMismatch: 1,
      ...toleranceOverrides,
    },
  };
}

function asymmetricPlanarCarbonylDefinition(formula, dominantElement, dominantLength, dominantCharge, outerLength, outerCharge, hcoAngleDegrees, toleranceOverrides = {}) {
  const data = referenceData[formula];
  const hcoAngle = hcoAngleDegrees * (Math.PI / 180);
  const centerCharge = -(dominantCharge + outerCharge * 2);

  return {
    formula,
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: 'C', partialCharge: centerCharge, position: vec(0, 0, 0) },
      { element: dominantElement, partialCharge: dominantCharge, position: vec(dominantLength, 0, 0) },
      { element: 'H', partialCharge: outerCharge, position: vec(Math.cos(hcoAngle) * outerLength, Math.sin(hcoAngle) * outerLength, 0) },
      { element: 'H', partialCharge: outerCharge, position: vec(Math.cos(-hcoAngle) * outerLength, Math.sin(-hcoAngle) * outerLength, 0) },
    ],
    bonds: [
      [0, 1],
      [0, 2],
      [0, 3],
    ],
    angles: [
      [1, 0, 2],
      [1, 0, 3],
      [2, 0, 3],
    ],
    torsions: [[1, 2, 0, 3]],
    ring: null,
    tolerances: {
      bondLength: 0.18,
      bondAngle: 22,
      torsion: 28,
      ringClosureDistance: 0.45,
      polarityVector: 0.85,
      stericClearance: 0.45,
      valenceMismatch: 1,
      ...toleranceOverrides,
    },
  };
}

function trigonalPyramidalDefinition(formula, centerElement, outerElement, centerCharge, outerCharge, toleranceOverrides = {}) {
  const data = referenceData[formula];
  const angle = data.bondAngle * (Math.PI / 180);
  const z = data.bondLength * Math.sqrt(Math.max((Math.cos(angle) + 0.5) / 1.5, 0));
  const radius = Math.sqrt(Math.max(data.bondLength * data.bondLength - z * z, 0));

  return {
    formula,
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: centerElement, partialCharge: centerCharge, position: vec(0, 0, 0) },
      { element: outerElement, partialCharge: outerCharge, position: vec(radius, 0, z) },
      { element: outerElement, partialCharge: outerCharge, position: vec(Math.cos((2 * Math.PI) / 3) * radius, Math.sin((2 * Math.PI) / 3) * radius, z) },
      { element: outerElement, partialCharge: outerCharge, position: vec(Math.cos((4 * Math.PI) / 3) * radius, Math.sin((4 * Math.PI) / 3) * radius, z) },
    ],
    bonds: [
      [0, 1],
      [0, 2],
      [0, 3],
    ],
    angles: [
      [1, 0, 2],
      [1, 0, 3],
      [2, 0, 3],
    ],
    torsions: [[1, 2, 0, 3]],
    ring: null,
    tolerances: {
      bondLength: 0.2,
      bondAngle: 30,
      torsion: 55,
      ringClosureDistance: 0.45,
      polarityVector: 0.75,
      stericClearance: 0.5,
      valenceMismatch: 1,
      ...toleranceOverrides,
    },
  };
}

function aromaticRingDefinition(formula, elements, charges, toleranceOverrides = {}) {
  const data = referenceData[formula];
  return {
    formula,
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: Array.from({ length: 6 }, (_, index) => {
      const theta = (index / 6) * Math.PI * 2;
      return {
        element: elements[index],
        partialCharge: charges[index],
        position: vec(Math.cos(theta) * data.bondLength, Math.sin(theta) * data.bondLength, 0),
      };
    }),
    bonds: [
      [0, 1],
      [1, 2],
      [2, 3],
      [3, 4],
      [4, 5],
      [5, 0],
    ],
    angles: [
      [5, 0, 1],
      [0, 1, 2],
      [1, 2, 3],
      [2, 3, 4],
      [3, 4, 5],
      [4, 5, 0],
    ],
    torsions: [
      [0, 1, 2, 3],
      [1, 2, 3, 4],
      [2, 3, 4, 5],
    ],
    ring: [0, 1, 2, 3, 4, 5, 0],
    tolerances: {
      bondLength: 0.12,
      bondAngle: 18,
      torsion: 25,
      ringClosureDistance: 0.35,
      polarityVector: 0.75,
      stericClearance: 0.4,
      valenceMismatch: 1,
      ...toleranceOverrides,
    },
  };
}

function acetyleneDefinition() {
  const data = referenceData.C2H2;
  const ch = 1.061;
  const cc = data.bondLength;
  return {
    formula: 'C2H2',
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: 'H', partialCharge: 0.08, position: vec(-(cc / 2 + ch), 0, 0) },
      { element: 'C', partialCharge: -0.08, position: vec(-cc / 2, 0, 0) },
      { element: 'C', partialCharge: -0.08, position: vec(cc / 2, 0, 0) },
      { element: 'H', partialCharge: 0.08, position: vec(cc / 2 + ch, 0, 0) },
    ],
    bonds: [
      [0, 1],
      [1, 2],
      [2, 3],
    ],
    angles: [
      [0, 1, 2],
      [1, 2, 3],
    ],
    torsions: [[0, 1, 2, 3]],
    ring: null,
    tolerances: { bondLength: 0.16, bondAngle: 22, torsion: 35, ringClosureDistance: 0.45, polarityVector: 0.65, stericClearance: 0.5, valenceMismatch: 1 },
  };
}

function etheneDefinition() {
  const data = referenceData.C2H4;
  const cc = data.bondLength;
  const ch = 1.087;
  const spread = (120 * Math.PI) / 180;
  return {
    formula: 'C2H4',
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: 'C', partialCharge: -0.12, position: vec(-cc / 2, 0, 0) },
      { element: 'C', partialCharge: -0.12, position: vec(cc / 2, 0, 0) },
      { element: 'H', partialCharge: 0.06, position: vec(-cc / 2 + Math.cos(spread) * ch, Math.sin(spread) * ch, 0) },
      { element: 'H', partialCharge: 0.06, position: vec(-cc / 2 + Math.cos(spread) * ch, -Math.sin(spread) * ch, 0) },
      { element: 'H', partialCharge: 0.06, position: vec(cc / 2 - Math.cos(spread) * ch, Math.sin(spread) * ch, 0) },
      { element: 'H', partialCharge: 0.06, position: vec(cc / 2 - Math.cos(spread) * ch, -Math.sin(spread) * ch, 0) },
    ],
    bonds: [
      [0, 1],
      [0, 2],
      [0, 3],
      [1, 4],
      [1, 5],
    ],
    angles: [
      [2, 0, 1],
      [3, 0, 1],
      [2, 0, 3],
      [4, 1, 0],
      [5, 1, 0],
      [4, 1, 5],
    ],
    torsions: [
      [2, 0, 1, 4],
      [3, 0, 1, 5],
    ],
    ring: null,
    tolerances: { bondLength: 0.17, bondAngle: 20, torsion: 28, ringClosureDistance: 0.45, polarityVector: 0.65, stericClearance: 0.5, valenceMismatch: 1 },
  };
}

function ethaneDefinition() {
  const data = referenceData.C2H6;
  const cc = data.bondLength;
  const ch = 1.095;
  const axial = ch / 3;
  const radius = Math.sqrt(Math.max(ch * ch - axial * axial, 0));
  const hydrogens = [];
  for (let i = 0; i < 3; i += 1) {
    const theta = (i / 3) * Math.PI * 2;
    hydrogens.push({ element: 'H', partialCharge: 0.04, position: vec(-cc / 2 - axial, Math.cos(theta) * radius, Math.sin(theta) * radius) });
  }
  for (let i = 0; i < 3; i += 1) {
    const theta = ((i / 3) * Math.PI * 2) + Math.PI / 3;
    hydrogens.push({ element: 'H', partialCharge: 0.04, position: vec(cc / 2 + axial, Math.cos(theta) * radius, Math.sin(theta) * radius) });
  }
  return {
    formula: 'C2H6',
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: 'C', partialCharge: -0.12, position: vec(-cc / 2, 0, 0) },
      { element: 'C', partialCharge: -0.12, position: vec(cc / 2, 0, 0) },
      ...hydrogens,
    ],
    bonds: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
      [1, 5],
      [1, 6],
      [1, 7],
    ],
    angles: [
      [2, 0, 1],
      [3, 0, 1],
      [4, 0, 1],
      [5, 1, 0],
      [6, 1, 0],
      [7, 1, 0],
    ],
    torsions: [
      [2, 0, 1, 5],
      [3, 0, 1, 6],
      [4, 0, 1, 7],
    ],
    rotatableGroups: [[[2, 3, 4], [5, 6, 7]]],
    ring: null,
    tolerances: { bondLength: 0.22, bondAngle: 30, torsion: 50, ringClosureDistance: 0.45, polarityVector: 0.65, stericClearance: 0.55, valenceMismatch: 1 },
  };
}

function peroxideDefinition() {
  const data = referenceData.H2O2;
  const oo = data.bondLength;
  const oh = 0.967;
  const angle = data.bondAngle * (Math.PI / 180);
  const torsion = data.torsion * (Math.PI / 180);
  const xOffset = Math.cos(angle) * oh;
  const radial = Math.sin(angle) * oh;
  return {
    formula: 'H2O2',
    family: data.family,
    routeBase: data.routeBase,
    valenceCapacity: data.valenceCapacity,
    atoms: [
      { element: 'O', partialCharge: -0.35, position: vec(-oo / 2, 0, 0) },
      { element: 'O', partialCharge: -0.35, position: vec(oo / 2, 0, 0) },
      { element: 'H', partialCharge: 0.35, position: vec(-oo / 2 - xOffset, radial, 0) },
      { element: 'H', partialCharge: 0.35, position: vec(oo / 2 + xOffset, Math.cos(torsion) * radial, Math.sin(torsion) * radial) },
    ],
    bonds: [
      [0, 1],
      [0, 2],
      [1, 3],
    ],
    angles: [
      [2, 0, 1],
      [0, 1, 3],
    ],
    torsions: [[2, 0, 1, 3]],
    rotatableGroups: [[[2], [3]]],
    ring: null,
    tolerances: { bondLength: 0.2, bondAngle: 28, torsion: 45, ringClosureDistance: 0.45, polarityVector: 0.85, stericClearance: 0.5, valenceMismatch: 1 },
  };
}

const coordinateMolecules = [
  {
    formula: 'H2',
    family: referenceData.H2.family,
    routeBase: referenceData.H2.routeBase,
    valenceCapacity: referenceData.H2.valenceCapacity,
    atoms: [
      { element: 'H', partialCharge: 0, position: vec(-referenceData.H2.bondLength / 2, 0, 0) },
      { element: 'H', partialCharge: 0, position: vec(referenceData.H2.bondLength / 2, 0, 0) },
    ],
    bonds: [[0, 1]],
    angles: [],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.18, bondAngle: 35, torsion: 60, ringClosureDistance: 0.45, polarityVector: 0.55, stericClearance: 0.45, valenceMismatch: 1 },
  },
  diatomicDefinition('HCl', 'H', 'Cl', 0.18, -0.18, { bondLength: 0.2, polarityVector: 0.75, stericClearance: 0.5 }),
  diatomicDefinition('F2', 'F', 'F', 0, 0, { bondLength: 0.16, polarityVector: 0.55, stericClearance: 0.45 }),
  {
    formula: 'H2O',
    family: referenceData.H2O.family,
    routeBase: referenceData.H2O.routeBase,
    valenceCapacity: referenceData.H2O.valenceCapacity,
    atoms: waterAtoms(),
    bonds: [
      [0, 1],
      [0, 2],
    ],
    angles: [[1, 0, 2]],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.18, bondAngle: 30, torsion: 60, ringClosureDistance: 0.45, polarityVector: 0.75, stericClearance: 0.4, valenceMismatch: 1 },
  },
  bentTriatomicDefinition('H2S', 'S', 'H', -0.3, 0.15, { bondLength: 0.22, bondAngle: 32, polarityVector: 0.8, stericClearance: 0.5 }),
  bentTriatomicDefinition('SO2', 'S', 'O', 0.6, -0.3, { bondLength: 0.2, bondAngle: 24, polarityVector: 0.85, stericClearance: 0.5 }),
  {
    formula: 'CO2',
    family: referenceData.CO2.family,
    routeBase: referenceData.CO2.routeBase,
    valenceCapacity: referenceData.CO2.valenceCapacity,
    atoms: [
      { element: 'O', partialCharge: -0.35, position: vec(-referenceData.CO2.bondLength, 0, 0) },
      { element: 'C', partialCharge: 0.7, position: vec(0, 0, 0) },
      { element: 'O', partialCharge: -0.35, position: vec(referenceData.CO2.bondLength, 0, 0) },
    ],
    bonds: [
      [0, 1],
      [1, 2],
    ],
    angles: [[0, 1, 2]],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.16, bondAngle: 25, torsion: 60, ringClosureDistance: 0.45, polarityVector: 0.65, stericClearance: 0.45, valenceMismatch: 1 },
  },
  {
    formula: 'HCN',
    family: referenceData.HCN.family,
    routeBase: referenceData.HCN.routeBase,
    valenceCapacity: referenceData.HCN.valenceCapacity,
    atoms: [
      { element: 'H', partialCharge: 0.25, position: vec(-1.064, 0, 0) },
      { element: 'C', partialCharge: 0.15, position: vec(0, 0, 0) },
      { element: 'N', partialCharge: -0.4, position: vec(1.156, 0, 0) },
    ],
    bonds: [
      [0, 1],
      [1, 2],
    ],
    angles: [[0, 1, 2]],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.16, bondAngle: 25, torsion: 60, ringClosureDistance: 0.45, polarityVector: 0.9, stericClearance: 0.45, valenceMismatch: 1 },
  },
  {
    formula: 'OCS',
    family: referenceData.OCS.family,
    routeBase: referenceData.OCS.routeBase,
    valenceCapacity: referenceData.OCS.valenceCapacity,
    atoms: [
      { element: 'O', partialCharge: -0.35, position: vec(-1.16, 0, 0) },
      { element: 'C', partialCharge: 0.5, position: vec(0, 0, 0) },
      { element: 'S', partialCharge: -0.15, position: vec(1.56, 0, 0) },
    ],
    bonds: [
      [0, 1],
      [1, 2],
    ],
    angles: [[0, 1, 2]],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.2, bondAngle: 25, torsion: 60, ringClosureDistance: 0.45, polarityVector: 0.85, stericClearance: 0.55, valenceMismatch: 1 },
  },
  {
    formula: 'CH4',
    family: referenceData.CH4.family,
    routeBase: referenceData.CH4.routeBase,
    valenceCapacity: referenceData.CH4.valenceCapacity,
    atoms: methaneAtoms(),
    bonds: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
    ],
    angles: [
      [1, 0, 2],
      [1, 0, 3],
      [1, 0, 4],
      [2, 0, 3],
      [2, 0, 4],
      [3, 0, 4],
    ],
    torsions: [[1, 2, 3, 4]],
    ring: null,
    tolerances: { bondLength: 0.2, bondAngle: 28, torsion: 45, ringClosureDistance: 0.45, polarityVector: 0.65, stericClearance: 0.5, valenceMismatch: 1 },
  },
  tetrahedralDefinition('SiH4', 'Si', 'H', -0.2, 0.05, { bondLength: 0.24, stericClearance: 0.65 }),
  tetrahedralDefinition('CF4', 'C', 'F', 0.8, -0.2, { bondLength: 0.2, polarityVector: 0.7, stericClearance: 0.55 }),
  trigonalPlanarDefinition('BF3', 'B', 'F', 0.45, -0.15, { bondLength: 0.18, bondAngle: 20, polarityVector: 0.65, stericClearance: 0.5 }),
  trigonalPlanarDefinition('BCl3', 'B', 'Cl', 0.45, -0.15, { bondLength: 0.22, bondAngle: 20, polarityVector: 0.75, stericClearance: 0.65 }),
  asymmetricPlanarCarbonylDefinition('H2CO', 'O', 1.21, -0.55, 1.1, 0.05, 121.8),
  asymmetricPlanarCarbonylDefinition('H2CS', 'S', 1.61, -0.38, 1.09, 0.04, 121.5, { bondLength: 0.22, polarityVector: 0.9, stericClearance: 0.55 }),
  trigonalPyramidalDefinition('NH3', 'N', 'H', -0.45, 0.15, { bondLength: 0.18, bondAngle: 28, polarityVector: 0.7, stericClearance: 0.45 }),
  trigonalPyramidalDefinition('PH3', 'P', 'H', -0.18, 0.06, { bondLength: 0.24, bondAngle: 32, polarityVector: 0.65, stericClearance: 0.6 }),
  {
    formula: 'O2',
    family: referenceData.O2.family,
    routeBase: referenceData.O2.routeBase,
    valenceCapacity: referenceData.O2.valenceCapacity,
    atoms: [
      { element: 'O', partialCharge: 0, position: vec(-referenceData.O2.bondLength / 2, 0, 0) },
      { element: 'O', partialCharge: 0, position: vec(referenceData.O2.bondLength / 2, 0, 0) },
    ],
    bonds: [[0, 1]],
    angles: [],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.14, bondAngle: 35, torsion: 60, ringClosureDistance: 0.45, polarityVector: 0.55, stericClearance: 0.45, valenceMismatch: 1 },
  },
  {
    formula: 'N2',
    family: referenceData.N2.family,
    routeBase: referenceData.N2.routeBase,
    valenceCapacity: referenceData.N2.valenceCapacity,
    atoms: [
      { element: 'N', partialCharge: 0, position: vec(-referenceData.N2.bondLength / 2, 0, 0) },
      { element: 'N', partialCharge: 0, position: vec(referenceData.N2.bondLength / 2, 0, 0) },
    ],
    bonds: [[0, 1]],
    angles: [],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.12, bondAngle: 35, torsion: 60, ringClosureDistance: 0.45, polarityVector: 0.55, stericClearance: 0.45, valenceMismatch: 1 },
  },
  diatomicDefinition('CO', 'C', 'O', 0.12, -0.12, { bondLength: 0.13, polarityVector: 0.65, stericClearance: 0.45 }),
  acetyleneDefinition(),
  etheneDefinition(),
  ethaneDefinition(),
  peroxideDefinition(),
  bentTriatomicDefinition('NO2', 'N', 'O', 0.4, -0.2, { bondLength: 0.17, bondAngle: 22, polarityVector: 0.75, stericClearance: 0.45 }),
  {
    formula: 'NaCl',
    family: referenceData.NaCl.family,
    routeBase: referenceData.NaCl.routeBase,
    valenceCapacity: referenceData.NaCl.valenceCapacity,
    atoms: [
      { element: 'Na', partialCharge: 1, position: vec(-referenceData.NaCl.bondLength / 2, 0, 0) },
      { element: 'Cl', partialCharge: -1, position: vec(referenceData.NaCl.bondLength / 2, 0, 0) },
    ],
    bonds: [[0, 1]],
    angles: [],
    torsions: [],
    ring: null,
    tolerances: { bondLength: 0.35, bondAngle: 35, torsion: 60, ringClosureDistance: 0.45, polarityVector: 1.2, stericClearance: 0.7, valenceMismatch: 1 },
  },
  diatomicDefinition('LiF', 'Li', 'F', 1, -1, { bondLength: 0.3, polarityVector: 1.1, stericClearance: 0.65 }),
  {
    formula: 'benzene',
    family: referenceData.benzene.family,
    routeBase: referenceData.benzene.routeBase,
    valenceCapacity: referenceData.benzene.valenceCapacity,
    atoms: benzeneAtoms(),
    bonds: [
      [0, 1],
      [1, 2],
      [2, 3],
      [3, 4],
      [4, 5],
      [5, 0],
    ],
    angles: [
      [5, 0, 1],
      [0, 1, 2],
      [1, 2, 3],
      [2, 3, 4],
      [3, 4, 5],
      [4, 5, 0],
    ],
    torsions: [
      [0, 1, 2, 3],
      [1, 2, 3, 4],
      [2, 3, 4, 5],
    ],
    ring: [0, 1, 2, 3, 4, 5, 0],
    tolerances: { bondLength: 0.12, bondAngle: 18, torsion: 25, ringClosureDistance: 0.35, polarityVector: 0.65, stericClearance: 0.4, valenceMismatch: 1 },
  },
  aromaticRingDefinition('pyridine', ['N', 'C', 'C', 'C', 'C', 'C'], [-0.35, 0.12, 0.04, 0.03, 0.04, 0.12]),
];

const perturbations = [
  { label: 'scale', levels: [-0.12, -0.06, 0, 0.06, 0.12] },
  { label: 'bend', levels: [-0.18, -0.09, 0, 0.09, 0.18] },
  { label: 'twist', levels: [-0.22, -0.11, 0, 0.11, 0.22] },
  { label: 'warp', levels: [-0.18, -0.09, 0, 0.09, 0.18] },
  { label: 'polar-skew', levels: [-0.16, -0.08, 0, 0.08, 0.16] },
  { label: 'crowd', levels: [-0.16, -0.08, 0, 0.08, 0.16] },
  { label: 'valence-mismatch', levels: [0, 0.25, 0.5] },
];

function perturbAtoms(definition, levels) {
  let atoms = cloneAtoms(definition.atoms);
  const [scaleLevel, bendLevel, twistLevel, warpLevel, polarLevel, crowdLevel, valenceMismatch] = levels;

  atoms = atoms.map((atom) => ({ ...atom, position: scale(atom.position, 1 + scaleLevel) }));

  atoms = atoms.map((atom, index) => {
    if (index === 0) {
      return atom;
    }
    const p = atom.position;
    return { ...atom, position: vec(p.x, p.y + bendLevel * Math.abs(p.x), p.z + warpLevel * (index % 2 === 0 ? 1 : -1)) };
  });

  const twistAngle = twistLevel * Math.PI;
  atoms = atoms.map((atom, index) => {
    if (index === 0) {
      return atom;
    }
    const p = atom.position;
    const localAngle = twistAngle * (index / Math.max(atoms.length - 1, 1));
    const cos = Math.cos(localAngle);
    const sin = Math.sin(localAngle);
    return { ...atom, position: vec(p.x * cos - p.y * sin, p.x * sin + p.y * cos, p.z) };
  });

  atoms = atoms.map((atom) => ({ ...atom, partialCharge: atom.partialCharge + polarLevel * Math.sign(atom.partialCharge || 1) }));

  if (crowdLevel !== 0) {
    atoms = atoms.map((atom, index) => (index === 0 ? atom : { ...atom, position: scale(atom.position, 1 + crowdLevel) }));
  }

  return { atoms, valenceMismatch };
}

function linearizeBent(definition) {
  const atoms = cloneAtoms(definition.atoms);
  const leftLength = distance(atoms[0].position, atoms[1].position);
  const rightLength = distance(atoms[0].position, atoms[2].position);
  atoms[0].position = vec(0, 0, 0);
  atoms[1].position = vec(-leftLength, 0, 0);
  atoms[2].position = vec(rightLength, 0, 0);
  return atoms;
}

function bendLinearTriatomic(definition, angleDegreesValue) {
  const atoms = cloneAtoms(definition.atoms);
  const leftLength = distance(atoms[1].position, atoms[0].position);
  const rightLength = distance(atoms[1].position, atoms[2].position);
  const halfAngle = (angleDegreesValue / 2) * (Math.PI / 180);
  atoms[1].position = vec(0, 0, 0);
  atoms[0].position = vec(-Math.sin(halfAngle) * leftLength, Math.cos(halfAngle) * leftLength, 0);
  atoms[2].position = vec(Math.sin(halfAngle) * rightLength, Math.cos(halfAngle) * rightLength, 0);
  return atoms;
}

function planarize(definition) {
  return cloneAtoms(definition.atoms).map((atom) => ({ ...atom, position: vec(atom.position.x, atom.position.y, 0) }));
}

function pyramidalizePlanar(definition) {
  const atoms = cloneAtoms(definition.atoms);
  atoms.slice(1).forEach((atom, index) => {
    const scaleFactor = 0.94;
    atom.position = vec(atom.position.x * scaleFactor, atom.position.y * scaleFactor, index % 2 === 0 ? 0.36 : 0.24);
  });
  return atoms;
}

function eclipseEthane(definition) {
  const atoms = cloneAtoms(definition.atoms);
  const cc = distance(atoms[0].position, atoms[1].position);
  const ch = distance(atoms[0].position, atoms[2].position);
  const axial = ch / 3;
  const radius = Math.sqrt(Math.max(ch * ch - axial * axial, 0));
  for (let i = 0; i < 3; i += 1) {
    const theta = (i / 3) * Math.PI * 2;
    atoms[5 + i].position = vec(cc / 2 + axial, Math.cos(theta) * radius, Math.sin(theta) * radius);
  }
  return atoms;
}

function warpRing(definition) {
  return cloneAtoms(definition.atoms).map((atom, index) => ({
    ...atom,
    position: vec(atom.position.x, atom.position.y, index % 2 === 0 ? 0.28 : -0.28),
  }));
}

const controlBuilders = {
  H2O: [
    {
      label: 'linear H2O decoy',
      expectedFailure: 'bent-polar angle collapse',
      atoms: linearizeBent,
    },
  ],
  SO2: [
    {
      label: 'linear SO2 decoy',
      expectedFailure: 'bent-polar angle collapse',
      atoms: linearizeBent,
    },
  ],
  NH3: [
    {
      label: 'planar NH3 decoy',
      expectedFailure: 'pyramidal polarity flattening',
      atoms: planarize,
    },
  ],
  BF3: [
    {
      label: 'pyramidal BF3 decoy',
      expectedFailure: 'planar brace warping',
      atoms: pyramidalizePlanar,
    },
  ],
  C2H6: [
    {
      label: 'eclipsed C2H6 decoy',
      expectedFailure: 'rotatable-route crowding',
      atoms: eclipseEthane,
    },
  ],
  CO2: [
    {
      label: 'bent CO2 decoy',
      expectedFailure: 'linear-route bending',
      atoms: (definition) => bendLinearTriatomic(definition, 135),
    },
  ],
  benzene: [
    {
      label: 'warped benzene decoy',
      expectedFailure: 'aromatic planarity loss',
      atoms: warpRing,
    },
  ],
};

function* levelTuples(index = 0, prefix = []) {
  if (index === perturbations.length) {
    yield prefix;
    return;
  }

  for (const level of perturbations[index].levels) {
    yield* levelTuples(index + 1, [...prefix, level]);
  }
}

function buildModel(definition, referenceGeometry) {
  return {
    formula: definition.formula,
    reference: referenceGeometry,
    tolerances: definition.tolerances,
  };
}

function formatNumber(value) {
  if (value === null || value === undefined) {
    return 'n/a';
  }
  return Number(value.toFixed(4));
}

function compact(row) {
  return {
    name: row.name,
    score: Number(row.score.toFixed(4)),
    genericScore: Number(row.genericScore.toFixed(4)),
    familyScore: Number(row.familyScore.toFixed(4)),
    changedPerturbations: row.changedPerturbations,
    geometry: {
      bondLength: formatNumber(row.geometry.bondLength),
      bondAngle: formatNumber(row.geometry.bondAngle),
      torsion: formatNumber(row.geometry.torsion),
      ringClosureDistance: formatNumber(row.geometry.ringClosureDistance),
      polarityVector: formatNumber(row.geometry.polarityVector),
      stericClearance: formatNumber(row.geometry.stericClearance),
      valenceMismatch: formatNumber(row.geometry.valenceMismatch),
    },
    derived: {
      geometryFit: Number(row.geometryFit.toFixed(3)),
      routeContinuity: Number(row.routeContinuity.toFixed(3)),
      bondStrain: Number(row.bondStrain.toFixed(3)),
      angleStrain: Number(row.angleStrain.toFixed(3)),
      polarityBalance: Number(row.polarityBalance.toFixed(3)),
      ringClosure: Number(row.ringClosure.toFixed(3)),
      stericObstruction: Number(row.stericObstruction.toFixed(3)),
    },
    coordinateMetrics: {
      bondRms: Number(row.coordinateMetrics.bondRms.toFixed(3)),
      bondMax: Number(row.coordinateMetrics.bondMax.toFixed(3)),
      angleRms: Number(row.coordinateMetrics.angleRms.toFixed(3)),
      angleMax: Number(row.coordinateMetrics.angleMax.toFixed(3)),
      torsionRms: Number(row.coordinateMetrics.torsionRms.toFixed(3)),
      ringPlanarity: Number(row.coordinateMetrics.ringPlanarity.toFixed(3)),
      steric: Number(row.coordinateMetrics.steric.toFixed(3)),
    },
  };
}

function candidateKey(row) {
  return [
    row.score.toFixed(4),
    row.geometry.bondLength?.toFixed(4) ?? 'na',
    row.geometry.bondAngle?.toFixed(4) ?? 'na',
    row.geometry.torsion?.toFixed(4) ?? 'na',
    row.geometry.ringClosureDistance?.toFixed(4) ?? 'na',
    row.geometry.polarityVector?.toFixed(4) ?? 'na',
    row.geometry.stericClearance?.toFixed(4) ?? 'na',
    row.geometry.valenceMismatch?.toFixed(4) ?? 'na',
  ].join('|');
}

function uniqueRows(rows, limit) {
  const seen = new Set();
  const unique = [];

  for (const row of rows) {
    const key = candidateKey(row);
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    unique.push(row);
    if (unique.length === limit) {
      break;
    }
  }

  return unique;
}

const globalPerturbationCounts = Object.fromEntries(perturbations.map((item) => [item.label, 0]));
let totalIterations = 0;
let zeroEffectIterations = 0;
const results = [];

for (const definition of coordinateMolecules) {
  const referenceGeometry = deriveGeometryFromCoordinates(definition, definition.atoms);
  const referenceFeatures = deriveCoordinateFeatures(definition, definition.atoms, 0);
  const referenceCandidate = deriveCandidateFromCoordinateFeatures(definition, referenceFeatures, referenceFeatures, {
    name: 'reference coordinates',
    type: 'reference',
  });
  const referenceGenericScore = scoreCandidate(referenceCandidate);
  const referenceScore = scoreFamilyCandidate(referenceCandidate, definition.family);
  const referenceKey = [
    referenceGeometry.bondLength?.toFixed(4) ?? 'na',
    referenceGeometry.bondAngle?.toFixed(4) ?? 'na',
    referenceGeometry.torsion?.toFixed(4) ?? 'na',
    referenceGeometry.ringClosureDistance?.toFixed(4) ?? 'na',
    referenceGeometry.polarityVector?.toFixed(4) ?? 'na',
    referenceGeometry.stericClearance?.toFixed(4) ?? 'na',
    referenceGeometry.valenceMismatch?.toFixed(4) ?? 'na',
  ].join('|');
  const rows = [];
  const perturbationCounts = Object.fromEntries(perturbations.map((item) => [item.label, 0]));
  let moleculeZeroEffectIterations = 0;

  for (const tuple of levelTuples()) {
    const { atoms, valenceMismatch } = perturbAtoms(definition, tuple);
    const features = deriveCoordinateFeatures(definition, atoms, valenceMismatch);
    const geometry = features.geometry;
    const changedPerturbations = tuple.filter((value) => value !== 0).length;
    const currentKey = [
      geometry.bondLength?.toFixed(4) ?? 'na',
      geometry.bondAngle?.toFixed(4) ?? 'na',
      geometry.torsion?.toFixed(4) ?? 'na',
      geometry.ringClosureDistance?.toFixed(4) ?? 'na',
      geometry.polarityVector?.toFixed(4) ?? 'na',
      geometry.stericClearance?.toFixed(4) ?? 'na',
      geometry.valenceMismatch?.toFixed(4) ?? 'na',
    ].join('|');

    if (changedPerturbations > 0 && currentKey === referenceKey) {
      zeroEffectIterations += 1;
      moleculeZeroEffectIterations += 1;
    }

    tuple.forEach((value, index) => {
      if (value !== 0) {
        perturbationCounts[perturbations[index].label] += 1;
        globalPerturbationCounts[perturbations[index].label] += 1;
      }
    });

    const candidate = deriveCandidateFromCoordinateFeatures(definition, features, referenceFeatures, {
      name: changedPerturbations === 0 ? 'reference coordinates' : `${changedPerturbations}-coordinate perturbation`,
      type: changedPerturbations === 0 ? 'reference' : 'generated',
    });

    rows.push({
      ...candidate,
      genericScore: scoreCandidate(candidate),
      familyScore: scoreFamilyCandidate(candidate, definition.family),
      score: scoreFamilyCandidate(candidate, definition.family),
      changedPerturbations,
      perturbationValues: Object.fromEntries(perturbations.map((item, index) => [item.label, tuple[index]])),
    });
    totalIterations += 1;
  }

  const ranked = rows.sort((a, b) => b.score - a.score || a.changedPerturbations - b.changedPerturbations);
  const controls = (controlBuilders[definition.formula] ?? []).map((control) => {
    const atoms = control.atoms(definition);
    const features = deriveCoordinateFeatures(definition, atoms, 0);
    const candidate = deriveCandidateFromCoordinateFeatures(definition, features, referenceFeatures, {
      name: control.label,
      type: 'decoy-control',
    });
    const familyScore = scoreFamilyCandidate(candidate, definition.family);
    const genericScore = scoreCandidate(candidate);
    const decoyRank = ranked.filter((row) => row.score > familyScore).length + 1;
    const penalty = referenceScore - familyScore;

    return {
      label: control.label,
      expectedFailure: control.expectedFailure,
      familyScore,
      genericScore,
      decoyRank,
      referenceBeatsDecoy: referenceScore > familyScore,
      decoyPenalty: penalty,
      candidate: compact({
        ...candidate,
        score: familyScore,
        genericScore,
        familyScore,
        changedPerturbations: 'control',
      }),
    };
  });
  results.push({
    formula: definition.formula,
    family: definition.family,
    iterations: rows.length,
    referenceScore,
    referenceGenericScore,
    referenceRank: ranked.findIndex((row) => row.type === 'reference') + 1,
    aboveReference: ranked.filter((row) => row.score > referenceScore).length,
    withinFivePercent: ranked.filter((row) => row.score >= referenceScore * 0.95).length,
    strongFailures: ranked.filter((row) => row.score < 0.55).length,
    zeroEffectIterations: moleculeZeroEffectIterations,
    perturbationCounts,
    controls,
    top: uniqueRows(ranked, 12).map(compact),
    bottom: uniqueRows([...ranked].reverse(), 12).map(compact),
  });
}

const controlResults = results.flatMap((result) =>
  result.controls.map((control) => ({
    formula: result.formula,
    family: result.family,
    referenceScore: result.referenceScore,
    ...control,
  }))
);

const summary = {
  totalIterations,
  molecules: coordinateMolecules.length,
  perturbations: perturbations.map((item) => item.label),
  referenceData,
  familyWeights,
  globalPerturbationCounts,
  zeroEffectIterations,
  controlResults,
  results,
};

await mkdir(outDir, { recursive: true });
await writeFile(new URL('molecule-coordinate-sweep.json', outDir), JSON.stringify(summary, null, 2));

const markdown = `# AMS Molecule Coordinate Sweep

## Scope

This sweep perturbs actual atom coordinate sets, derives coordinate-feature distributions, then derives the AMS coherence variables from those distributions.

It is still a secondary-regime coherence bench. It does not treat atoms as vorton species and does not insert material parts between substrate and vorton formation.

## Scale

Molecules tested: ${coordinateMolecules.length}

Total coordinate iterations tried: ${totalIterations}

Zero-effect coordinate iterations: ${zeroEffectIterations}

Perturbation categories:

${perturbations.map((item) => `- ${item.label}`).join('\n')}

## Global Perturbation Counts

| Perturbation | Non-reference applications |
|---|---:|
${Object.entries(globalPerturbationCounts)
  .map(([label, count]) => `| ${label} | ${count} |`)
  .join('\n')}

## Reference Calibration Table

These are approximate classical anchors used to construct the coordinate references. They calibrate the bench; they do not define AMS ontology.

| Case | Family | Bond length | Bond angle | Route base | Polarity proxy | Provenance | Status | Notes |
|---|---|---:|---:|---:|---:|---|---|---|
${Object.entries(referenceData)
  .map(
    ([formula, data]) =>
      `| ${formula} | ${data.family} | ${data.bondLength ?? 'n/a'} | ${data.bondAngle ?? 'n/a'} | ${data.routeBase} | ${data.polarityVector} | ${data.provenance.sourceName} | ${data.provenance.status} | ${data.notes} |`
  )
  .join('\n')}

Reference source URL: ${defaultReferenceProvenance.sourceUrl}

## Family Weight Profiles

Each family uses the same variables but different weights. This prevents ionic pairs, aromatic rings, and diatomics from being judged as if their dominant constraints were identical.

| Family | Valence | Geometry | Angle | Bond | Polarity | Route | Ring | Steric |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
${Object.entries(familyWeights)
  .map(
    ([family, weights]) =>
      `| ${family} | ${weights.valenceSatisfaction} | ${weights.geometryFit} | ${weights.angleStrain} | ${weights.bondStrain} | ${weights.polarityBalance} | ${weights.routeContinuity} | ${weights.ringClosure} | ${weights.stericObstruction} |`
  )
  .join('\n')}

## Molecule Results

| Molecule | Family | Iterations | Reference rank | Reference score | Above reference | Within 95% | Strong failures | Zero-effect |
|---|---|---:|---:|---:|---:|---:|---:|---:|
${results
  .map(
    (result) =>
      `| ${result.formula} | ${result.family} | ${result.iterations} | ${result.referenceRank} | ${result.referenceScore.toFixed(4)} | ${result.aboveReference} | ${result.withinFivePercent} | ${result.strongFailures} | ${result.zeroEffectIterations} |`
  )
  .join('\n')}

## Decoy Control Results

These controls are deliberately wrong or strained geometries scored against the same reference features and family weights. Passing means the reference score remains above the control score.

| Molecule | Control | Expected failure | Reference score | Decoy score | Decoy rank | Reference beats decoy | Decoy penalty | Geometry fit | Angle strain | Torsion RMS | Ring planar | Steric |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
${controlResults
  .map(
    (control) =>
      `| ${control.formula} | ${control.label} | ${control.expectedFailure} | ${control.referenceScore.toFixed(4)} | ${control.familyScore.toFixed(4)} | ${control.decoyRank} | ${control.referenceBeatsDecoy ? 'yes' : 'no'} | ${control.decoyPenalty.toFixed(4)} | ${control.candidate.derived.geometryFit} | ${control.candidate.derived.angleStrain} | ${control.candidate.coordinateMetrics.torsionRms} | ${control.candidate.coordinateMetrics.ringPlanarity} | ${control.candidate.coordinateMetrics.steric} |`
  )
  .join('\n')}

## Top Coordinate Candidates

${results
  .map(
    (result) => `### ${result.formula}

| Rank | Candidate | Family score | Generic score | Changed | Bond length | Bond angle | Torsion | Polarity | Steric clearance | Valence mismatch | Bond RMS | Angle RMS | Torsion RMS | Ring planar | Geometry fit | Route |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
${result.top
  .map(
    (row, index) =>
      `| ${index + 1} | ${row.name} | ${row.familyScore} | ${row.genericScore} | ${row.changedPerturbations} | ${row.geometry.bondLength} | ${row.geometry.bondAngle} | ${row.geometry.torsion} | ${row.geometry.polarityVector} | ${row.geometry.stericClearance} | ${row.geometry.valenceMismatch} | ${row.coordinateMetrics.bondRms} | ${row.coordinateMetrics.angleRms} | ${row.coordinateMetrics.torsionRms} | ${row.coordinateMetrics.ringPlanarity} | ${row.derived.geometryFit} | ${row.derived.routeContinuity} |`
  )
  .join('\n')}`
  )
  .join('\n\n')}

## First Reading

This coordinate-level bench now uses distribution-derived metrics rather than scoring only representative averages. Bond strain, angle strain, torsion strain, ring planarity, polarity, steric pressure, and valence mismatch are all derived from coordinate features.

Top and bottom rows are deduplicated by derived coordinate profile. Zero-effect iterations are counted because some perturbations do not affect simple molecules with missing angle, torsion, or ring features.

Decoy controls are explicit wrong-geometry probes. They are not new calibration anchors; they test whether the current score rejects familiar failure modes without changing weights for individual molecules.
`;

await writeFile(new URL('molecule-coordinate-sweep-summary.md', outDir), markdown);

console.log(`Molecules tested: ${coordinateMolecules.length}`);
console.log(`Total coordinate iterations tried: ${totalIterations}`);
console.log(`Wrote ${new URL('molecule-coordinate-sweep-summary.md', outDir).pathname}`);
