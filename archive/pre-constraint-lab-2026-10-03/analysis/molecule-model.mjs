export function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

export function scoreCandidate(candidate) {
  const score =
    candidate.valenceSatisfaction * 0.18 +
    candidate.geometryFit * 0.16 +
    (1 - candidate.angleStrain) * 0.14 +
    (1 - candidate.bondStrain) * 0.12 +
    candidate.polarityBalance * 0.12 +
    candidate.routeContinuity * 0.14 +
    candidate.ringClosure * 0.08 +
    (1 - candidate.stericObstruction) * 0.06;

  return clamp01(score);
}

export function candidate(name, type, values) {
  return {
    name,
    type,
    valenceSatisfaction: values.valenceSatisfaction,
    geometryFit: values.geometryFit,
    angleStrain: values.angleStrain,
    bondStrain: values.bondStrain,
    polarityBalance: values.polarityBalance,
    routeContinuity: values.routeContinuity,
    ringClosure: values.ringClosure,
    stericObstruction: values.stericObstruction,
  };
}

export const molecules = [
  {
    formula: 'H2',
    reading: 'A single saturated coupling relation should outrank stretched or unsatisfied variants.',
    reference: candidate('reference single coupling', 'reference', {
      valenceSatisfaction: 0.98,
      geometryFit: 0.96,
      angleStrain: 0,
      bondStrain: 0.03,
      polarityBalance: 0.92,
      routeContinuity: 0.82,
      ringClosure: 0,
      stericObstruction: 0.02,
    }),
    manualVariants: [
      candidate('overstretched coupling', 'perturbed', {
        valenceSatisfaction: 0.72,
        geometryFit: 0.58,
        angleStrain: 0,
        bondStrain: 0.55,
        polarityBalance: 0.9,
        routeContinuity: 0.42,
        ringClosure: 0,
        stericObstruction: 0.02,
      }),
      candidate('unsatisfied separate atoms', 'bad', {
        valenceSatisfaction: 0.32,
        geometryFit: 0.2,
        angleStrain: 0,
        bondStrain: 0.82,
        polarityBalance: 0.75,
        routeContinuity: 0.08,
        ringClosure: 0,
        stericObstruction: 0.01,
      }),
    ],
  },
  {
    formula: 'H2O',
    reading: 'A bent polar geometry should outrank linear or badly compressed variants.',
    reference: candidate('reference bent polar geometry', 'reference', {
      valenceSatisfaction: 0.96,
      geometryFit: 0.94,
      angleStrain: 0.05,
      bondStrain: 0.04,
      polarityBalance: 0.82,
      routeContinuity: 0.72,
      ringClosure: 0,
      stericObstruction: 0.08,
    }),
    manualVariants: [
      candidate('forced linear geometry', 'perturbed', {
        valenceSatisfaction: 0.94,
        geometryFit: 0.48,
        angleStrain: 0.72,
        bondStrain: 0.08,
        polarityBalance: 0.45,
        routeContinuity: 0.58,
        ringClosure: 0,
        stericObstruction: 0.1,
      }),
      candidate('compressed bonds', 'bad', {
        valenceSatisfaction: 0.88,
        geometryFit: 0.52,
        angleStrain: 0.35,
        bondStrain: 0.68,
        polarityBalance: 0.68,
        routeContinuity: 0.44,
        ringClosure: 0,
        stericObstruction: 0.42,
      }),
    ],
  },
  {
    formula: 'CO2',
    reading: 'A linear geometry with balanced whole-molecule polarity should outrank bent imbalance.',
    reference: candidate('reference linear balanced geometry', 'reference', {
      valenceSatisfaction: 0.96,
      geometryFit: 0.96,
      angleStrain: 0.03,
      bondStrain: 0.04,
      polarityBalance: 0.93,
      routeContinuity: 0.84,
      ringClosure: 0,
      stericObstruction: 0.08,
    }),
    manualVariants: [
      candidate('bent polar imbalance', 'perturbed', {
        valenceSatisfaction: 0.92,
        geometryFit: 0.55,
        angleStrain: 0.58,
        bondStrain: 0.05,
        polarityBalance: 0.42,
        routeContinuity: 0.66,
        ringClosure: 0,
        stericObstruction: 0.12,
      }),
      candidate('uneven bond lengths', 'bad', {
        valenceSatisfaction: 0.86,
        geometryFit: 0.58,
        angleStrain: 0.08,
        bondStrain: 0.62,
        polarityBalance: 0.55,
        routeContinuity: 0.5,
        ringClosure: 0,
        stericObstruction: 0.12,
      }),
    ],
  },
  {
    formula: 'CH4',
    reading: 'A saturated tetrahedral geometry should outrank planar or crowded variants.',
    reference: candidate('reference tetrahedral geometry', 'reference', {
      valenceSatisfaction: 0.98,
      geometryFit: 0.95,
      angleStrain: 0.04,
      bondStrain: 0.05,
      polarityBalance: 0.86,
      routeContinuity: 0.76,
      ringClosure: 0,
      stericObstruction: 0.06,
    }),
    manualVariants: [
      candidate('forced planar geometry', 'perturbed', {
        valenceSatisfaction: 0.96,
        geometryFit: 0.46,
        angleStrain: 0.7,
        bondStrain: 0.07,
        polarityBalance: 0.82,
        routeContinuity: 0.6,
        ringClosure: 0,
        stericObstruction: 0.18,
      }),
      candidate('crowded asymmetric geometry', 'bad', {
        valenceSatisfaction: 0.9,
        geometryFit: 0.5,
        angleStrain: 0.48,
        bondStrain: 0.28,
        polarityBalance: 0.62,
        routeContinuity: 0.54,
        ringClosure: 0,
        stericObstruction: 0.68,
      }),
    ],
  },
  {
    formula: 'benzene',
    reading: 'A planar sixfold ring with distributed route coherence should outrank broken or localised rings.',
    reference: candidate('reference planar distributed ring', 'reference', {
      valenceSatisfaction: 0.95,
      geometryFit: 0.94,
      angleStrain: 0.06,
      bondStrain: 0.06,
      polarityBalance: 0.88,
      routeContinuity: 0.96,
      ringClosure: 0.96,
      stericObstruction: 0.1,
    }),
    manualVariants: [
      candidate('localised alternating strain', 'perturbed', {
        valenceSatisfaction: 0.9,
        geometryFit: 0.72,
        angleStrain: 0.24,
        bondStrain: 0.26,
        polarityBalance: 0.78,
        routeContinuity: 0.58,
        ringClosure: 0.86,
        stericObstruction: 0.12,
      }),
      candidate('broken ring route', 'bad', {
        valenceSatisfaction: 0.76,
        geometryFit: 0.58,
        angleStrain: 0.34,
        bondStrain: 0.38,
        polarityBalance: 0.74,
        routeContinuity: 0.26,
        ringClosure: 0.22,
        stericObstruction: 0.14,
      }),
    ],
  },
];

export const geometryMolecules = [
  {
    formula: 'H2',
    reference: {
      bondLength: 0.74,
      bondAngle: null,
      torsion: null,
      ringClosureDistance: null,
      polarityVector: 0,
      stericClearance: 1.2,
      valenceMismatch: 0,
      routeBase: 0.82,
      valenceCapacity: 1,
      ringWeight: 0,
    },
    tolerances: {
      bondLength: 0.18,
      bondAngle: 35,
      torsion: 60,
      ringClosureDistance: 0.45,
      polarityVector: 0.55,
      stericClearance: 0.45,
      valenceMismatch: 1,
    },
  },
  {
    formula: 'H2O',
    reference: {
      bondLength: 0.96,
      bondAngle: 104.5,
      torsion: null,
      ringClosureDistance: null,
      polarityVector: 1.85,
      stericClearance: 1.05,
      valenceMismatch: 0,
      routeBase: 0.72,
      valenceCapacity: 2,
      ringWeight: 0,
    },
    tolerances: {
      bondLength: 0.18,
      bondAngle: 30,
      torsion: 60,
      ringClosureDistance: 0.45,
      polarityVector: 0.75,
      stericClearance: 0.4,
      valenceMismatch: 1,
    },
  },
  {
    formula: 'CO2',
    reference: {
      bondLength: 1.16,
      bondAngle: 180,
      torsion: null,
      ringClosureDistance: null,
      polarityVector: 0,
      stericClearance: 1.25,
      valenceMismatch: 0,
      routeBase: 0.84,
      valenceCapacity: 4,
      ringWeight: 0,
    },
    tolerances: {
      bondLength: 0.16,
      bondAngle: 25,
      torsion: 60,
      ringClosureDistance: 0.45,
      polarityVector: 0.65,
      stericClearance: 0.45,
      valenceMismatch: 1,
    },
  },
  {
    formula: 'CH4',
    reference: {
      bondLength: 1.09,
      bondAngle: 109.5,
      torsion: 60,
      ringClosureDistance: null,
      polarityVector: 0,
      stericClearance: 1.35,
      valenceMismatch: 0,
      routeBase: 0.76,
      valenceCapacity: 4,
      ringWeight: 0,
    },
    tolerances: {
      bondLength: 0.2,
      bondAngle: 28,
      torsion: 45,
      ringClosureDistance: 0.45,
      polarityVector: 0.65,
      stericClearance: 0.5,
      valenceMismatch: 1,
    },
  },
  {
    formula: 'benzene',
    reference: {
      bondLength: 1.39,
      bondAngle: 120,
      torsion: 0,
      ringClosureDistance: 0,
      polarityVector: 0,
      stericClearance: 1.25,
      valenceMismatch: 0,
      routeBase: 0.96,
      valenceCapacity: 3,
      ringWeight: 1,
    },
    tolerances: {
      bondLength: 0.12,
      bondAngle: 18,
      torsion: 25,
      ringClosureDistance: 0.35,
      polarityVector: 0.65,
      stericClearance: 0.4,
      valenceMismatch: 1,
    },
  },
];

function normalizedDeviation(actual, expected, tolerance) {
  if (expected === null || actual === null) {
    return 0;
  }
  return clamp01(Math.abs(actual - expected) / tolerance);
}

export function deriveCandidateFromGeometry(molecule, geometry, meta = {}) {
  const reference = molecule.reference;
  const tolerances = molecule.tolerances;
  const bondDeviation = normalizedDeviation(geometry.bondLength, reference.bondLength, tolerances.bondLength);
  const angleDeviation = normalizedDeviation(geometry.bondAngle, reference.bondAngle, tolerances.bondAngle);
  const torsionDeviation = normalizedDeviation(geometry.torsion, reference.torsion, tolerances.torsion);
  const ringDeviation =
    reference.ringClosureDistance === null
      ? 0
      : normalizedDeviation(geometry.ringClosureDistance, reference.ringClosureDistance, tolerances.ringClosureDistance);
  const polarityDeviation = normalizedDeviation(geometry.polarityVector, reference.polarityVector, tolerances.polarityVector);
  const stericDeviation = clamp01((reference.stericClearance - geometry.stericClearance) / tolerances.stericClearance);
  const valenceDeviation = normalizedDeviation(geometry.valenceMismatch, reference.valenceMismatch, tolerances.valenceMismatch);

  const bondStrain = clamp01(bondDeviation * 0.85 + valenceDeviation * 0.15);
  const angleStrain = clamp01(angleDeviation * 0.72 + torsionDeviation * 0.18 + ringDeviation * 0.1);
  const geometryFit = clamp01(1 - (bondDeviation * 0.24 + angleDeviation * 0.32 + torsionDeviation * 0.14 + ringDeviation * 0.2 + stericDeviation * 0.1));
  const routeContinuity = clamp01(reference.routeBase - bondDeviation * 0.12 - angleDeviation * 0.12 - torsionDeviation * 0.08 - ringDeviation * 0.2 - valenceDeviation * 0.16);
  const polarityBalance = clamp01(1 - polarityDeviation * 0.72 - valenceDeviation * 0.12);
  const ringClosure = reference.ringWeight === 0 ? 0 : clamp01(1 - ringDeviation * 0.8 - torsionDeviation * 0.18);
  const stericObstruction = stericDeviation;
  const valenceSatisfaction = clamp01(1 - valenceDeviation * 0.82 - bondDeviation * 0.08);

  return {
    name: meta.name || 'geometry candidate',
    type: meta.type || 'generated',
    mode: meta.mode || 'geometry',
    geometry,
    deviations: {
      bond: bondDeviation,
      angle: angleDeviation,
      torsion: torsionDeviation,
      ring: ringDeviation,
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
