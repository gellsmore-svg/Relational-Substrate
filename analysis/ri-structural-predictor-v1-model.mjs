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
// alpha_minus = alpha_minus_free * 10^( No / Van^nexp ).
//
// Sign note: the cached eqn (6) image renders as 10^(-No/Van^n), but with the
// source-stated O2- parameters {alpha_minus_free=1.79, No=-1.776} that form gives
// alpha > alpha_free, contradicting the source's own in-crystal values (e.g. 1.44 in
// SiO2 < 1.79). The form that reproduces the source is 10^(No/Van^n): with No=-1.776
// and the source-stated Van(SiO2)=18.8 it yields 1.44 EXACTLY at nexp=1.0 (the
// source-stated whole-dataset exponent is 1.20, which gives 1.586 at the same Van;
// that residual is flagged and must be reconciled before scoring -- O2- dominates
// alpha_T). Until anchorOxygenModel() passes against a source value, this term must
// not be used in a scored prediction.
export function anionPolarizability({ freeIonAlpha, No, nexp, anionMolarVolume }) {
  assertFinite(freeIonAlpha, 'freeIonAlpha');
  assertFinite(No, 'No');
  assertFinite(nexp, 'nexp');
  assertFinite(anionMolarVolume, 'anionMolarVolume');
  if (anionMolarVolume <= 0) throw new Error('anionMolarVolume must be positive.');
  return freeIonAlpha * 10 ** (No / anionMolarVolume ** nexp);
}

// Source-stated parameters (Shannon-Fischer 2016): free-ion alpha 1.79, No -1.776.
// nexp is the source's whole-dataset exponent (1.20); nexpAnchor (1.0) reproduces
// the stated SiO2 worked value exactly -- the unresolved choice is the final gap.
export const O2_MINUS_PARAMS = { freeIonAlpha: 1.79, No: -1.776, nexp: 1.2 };
// Source-stated worked anchor: Van(SiO2)=18.8 A^3 -> alpha(O2-)=1.44 A^3.
export const O2_MINUS_SIO2_ANCHOR = { anionMolarVolume: 18.8, expectedAlpha: 1.44 };

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
