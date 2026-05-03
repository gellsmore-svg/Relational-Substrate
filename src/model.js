export const closedForms = ['circle', 'trefoil', 'double'];
export const transientForms = ['straight', 'sine', 'ribbon'];
export const scenarios = ['admit', 'return', 'store'];

export const scenarioPresets = {
  admit: { boundary: 0.82, route: 0.78, storage: 0.18, scatter: 0.12, reseat: 0.7 },
  return: { boundary: 0.22, route: 0.32, storage: 0.24, scatter: 0.18, reseat: 0.74 },
  store: { boundary: 0.48, route: 0.42, storage: 0.7, scatter: 0.5, reseat: 0.46 },
};

const formBias = {
  circle: { closure: 0.02, return: 0.03, bounded: 0, coherence: 0.03, reseat: 0.04, leakage: 0.02 },
  trefoil: { closure: 0.06, return: 0.04, bounded: 0.04, coherence: -0.01, reseat: -0.02, leakage: 0.01 },
  double: { closure: 0.04, return: 0.07, bounded: -0.01, coherence: -0.03, reseat: -0.01, leakage: -0.02 },
};

const transientBias = {
  straight: { route: 0.05, scatter: -0.03, storage: -0.02 },
  sine: { route: -0.02, scatter: 0.02, storage: 0.03 },
  ribbon: { route: -0.04, scatter: 0.04, storage: 0.02 },
};

const scenarioBias = {
  admit: { admitted: 0.22, returnedScale: 0.55, storedScale: 0.72, scattered: 0 },
  return: { admittedScale: 0.48, returned: 0.36, storedScale: 0.7, scattered: 0 },
  store: { admittedScale: 0.66, returnedScale: 1, stored: 0.22, scattered: 0.14 },
};

export function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

export function calculateOutcome(input) {
  const fBias = formBias[input.closedForm] || formBias.trefoil;
  const tBias = transientBias[input.transientForm] || transientBias.straight;
  const sBias = scenarioBias[input.scenario] || scenarioBias.admit;

  const boundary = input.boundary;
  const route = clamp01(input.route + tBias.route);
  const storageSetting = clamp01(input.storage + tBias.storage);
  const scatterSetting = clamp01(input.scatter + tBias.scatter);
  const reseat = input.reseat;

  let admitted = boundary * route * (1 - scatterSetting * 0.55);
  let returned = (1 - boundary) * (0.72 + (1 - route) * 0.28);
  let stored = storageSetting * (1 - route * 0.38);
  let scattered = scatterSetting * (1 - boundary * 0.26);

  if (sBias.admitted) admitted += sBias.admitted;
  if (sBias.returned) returned += sBias.returned;
  if (sBias.stored) stored += sBias.stored;
  if (sBias.scattered) scattered += sBias.scattered;
  if (sBias.admittedScale) admitted *= sBias.admittedScale;
  if (sBias.returnedScale) returned *= sBias.returnedScale;
  if (sBias.storedScale) stored *= sBias.storedScale;

  const total = admitted + returned + stored + scattered || 1;
  admitted /= total;
  returned /= total;
  stored /= total;
  scattered /= total;

  const closureStress = stored * 0.62 + scattered * 0.48 + (1 - reseat) * 0.36;
  const closureMetric = clamp01(0.72 + reseat * 0.18 - scattered * 0.32 + fBias.closure);
  const returnMetric = clamp01(boundary * 0.28 + route * 0.26 + reseat * 0.46 - stored * 0.18 + fBias.return);
  const boundedMetric = clamp01(0.86 - stored * 0.3 - scattered * 0.25 + boundary * 0.12 + fBias.bounded);
  const coherenceMetric = clamp01(route * 0.5 + boundary * 0.24 + reseat * 0.18 - scatterSetting * 0.34 + fBias.coherence);
  const reseatMetric = clamp01(reseat - closureStress * 0.24 + fBias.reseat);
  const leakageMetric = clamp01(1 - (stored * 0.38 + scattered * 0.5 + (1 - boundary) * 0.16) + fBias.leakage);
  const identityScore = clamp01(
    closureMetric * 0.18 +
      returnMetric * 0.18 +
      boundedMetric * 0.17 +
      coherenceMetric * 0.18 +
      reseatMetric * 0.14 +
      leakageMetric * 0.15
  );
  const identityPreserved = identityScore >= 0.62 && closureStress < 0.62;

  return {
    ...input,
    admitted,
    returned,
    stored,
    scattered,
    identityPreserved,
    closureStress,
    closureMetric,
    returnMetric,
    boundedMetric,
    coherenceMetric,
    reseatMetric,
    leakageMetric,
    identityScore,
    metrics: {
      closure: closureMetric,
      return: returnMetric,
      bounded: boundedMetric,
      coherence: coherenceMetric,
      reseat: reseatMetric,
      leakage: leakageMetric,
      identity: identityScore,
    },
  };
}
