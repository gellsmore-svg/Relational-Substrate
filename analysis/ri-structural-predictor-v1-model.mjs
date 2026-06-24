// RI structural predictor v1 implementation (predeclaration: see
// ri-structural-predictor-v1-predeclaration.mjs). Equations transcribed verbatim
// from Shannon & Fischer 2016 (cached preprint pp.5-8). Fixed parameters only; no
// fitted coefficients. All polarizabilities and molar volumes in Angstrom^3.
//
// This module computes predictions; it asserts no evidence. It carries an explicit
// flag that the eqn (6) anion-volume O2- parameterisation must be anchored against a
// Shannon-Fischer worked example before it is used in a scored prediction.

const FOUR_PI = 4 * Math.PI;
const B = FOUR_PI / 3; // Lorentz factor b
export const AE_C = 2.26; // Anderson-Eggleton electron-overlap factor (Eggleton 1991)

function assertFinite(value, label) {
  if (!Number.isFinite(value)) throw new Error(`${label} must be finite.`);
}

// Eqn (4a): total polarizability from refractive index and molar volume, AE form.
export function polarizabilityFromIndex(n, molarVolume, c = AE_C) {
  assertFinite(n, 'n');
  assertFinite(molarVolume, 'molarVolume');
  if (n <= 0 || molarVolume <= 0) throw new Error('n and molarVolume must be positive.');
  const x = n * n - 1;
  return (x * molarVolume) / (FOUR_PI + (B - c) * x);
}

// Eqn (4b): refractive index from total polarizability and molar volume, AE form.
export function indexFromPolarizability(alphaTotal, molarVolume, c = AE_C) {
  assertFinite(alphaTotal, 'alphaTotal');
  assertFinite(molarVolume, 'molarVolume');
  if (molarVolume <= 0) throw new Error('molarVolume must be positive.');
  const denom = (c - B) * alphaTotal + molarVolume;
  if (denom <= 0) throw new Error('non-physical denominator in AE inverse (check inputs).');
  const nSquared = (FOUR_PI * alphaTotal) / denom + 1;
  if (nSquared <= 0) throw new Error('non-physical n^2 in AE inverse.');
  return Math.sqrt(nSquared);
}

// Eqn (5): additivity. ions = [{ alpha, count }].
export function totalPolarizability(ions) {
  if (!Array.isArray(ions) || ions.length === 0) throw new Error('ions must be a non-empty array.');
  return ions.reduce((sum, ion) => {
    assertFinite(ion.alpha, 'ion.alpha');
    assertFinite(ion.count, 'ion.count');
    return sum + ion.count * ion.alpha;
  }, 0);
}

// Eqn (6): anion-volume-corrected anion polarizability.
// alpha_minus = alpha_minus_free * 10^( -No / Van^nexp ).
// NOTE: the numeric interpretation of {alpha_minus_free=1.79, No=-1.776} relative
// to the reported in-crystal O2- range (e.g. ~1.44 in SiO2) is NOT yet anchored to
// a Shannon-Fischer worked example. Until anchorOxygenModel() is satisfied, callers
// must not use this in a scored prediction.
export function anionPolarizability({ freeIonAlpha, No, nexp, anionMolarVolume }) {
  assertFinite(freeIonAlpha, 'freeIonAlpha');
  assertFinite(No, 'No');
  assertFinite(nexp, 'nexp');
  assertFinite(anionMolarVolume, 'anionMolarVolume');
  if (anionMolarVolume <= 0) throw new Error('anionMolarVolume must be positive.');
  return freeIonAlpha * 10 ** (-No / anionMolarVolume ** nexp);
}

export const O2_MINUS_PARAMS = { freeIonAlpha: 1.79, No: -1.776, nexp: 1.2 };

// Coordination-resolved Ca2+ polarizabilities (Shannon-Fischer 2016 cation table).
export const CA_ALPHA_BY_CN = {
  5: 1.91, 6: 1.79, 7: 1.67, 8: 1.57, 9: 1.48, 10: 1.39, 11: 1.32, 12: 1.25,
};
export const SI_ALPHA = 0.284; // Si4+ [4]

// Predict the scalar index for a structural ion set at a given molar volume.
export function predictIndex({ ions, molarVolume, c = AE_C }) {
  return indexFromPolarizability(totalPolarizability(ions), molarVolume, c);
}

// Guard: the eqn-6 oxygen model must be anchored before scored use. Returns the
// relative error against a provided source anchor {anionMolarVolume, expectedAlpha}.
export function anchorOxygenModel(anchor, tolerance = 0.02) {
  const got = anionPolarizability({ ...O2_MINUS_PARAMS, anionMolarVolume: anchor.anionMolarVolume });
  const relError = Math.abs(got - anchor.expectedAlpha) / anchor.expectedAlpha;
  return { got, expected: anchor.expectedAlpha, relError, anchored: relError <= tolerance };
}
