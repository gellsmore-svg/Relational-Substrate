// Scorer for the frozen "conventional independent-profile-PSD versus
// BRDF-derived-PSD shape comparator v0" (predeclaration hash ad3892b700d0b82f).
//
// This comparator exists because some sources (e.g. Tayabaly et al. 2013)
// expose a BRDF-derived PSDscatter curve rather than raw angular BRDF rows. It
// compares an INDEPENDENTLY measured one-dimensional surface-height profile PSD
// against the source-reported PSDscatter directly in spatial-frequency space.
//
// It carries no substrate-specific evidence weight. It is a conventional shape
// comparator only: shape, one surface state, one wavelength/incidence/scan
// convention. It must never be read as raw BRDF prediction or absolute magnitude.

import { interpolatePsdLogLog } from './roughness-psd-brdf-model.mjs';

const PREDECLARATION_HASH = 'ad3892b700d0b82f';

function assertFinite(value, label) {
  if (!Number.isFinite(value)) {
    throw new Error(`${label} must be finite.`);
  }
}

function log10(value) {
  return Math.log(value) / Math.LN10;
}

function median(values) {
  if (values.length === 0) throw new Error('median of empty set');
  const sorted = [...values].sort((left, right) => left - right);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 0
    ? (sorted[middle - 1] + sorted[middle]) / 2
    : sorted[middle];
}

// Linear-interpolated percentile on the sorted sample (rank = p*(n-1)).
function percentile(values, fraction) {
  if (values.length === 0) throw new Error('percentile of empty set');
  const sorted = [...values].sort((left, right) => left - right);
  if (sorted.length === 1) return sorted[0];
  const rank = fraction * (sorted.length - 1);
  const lowerIndex = Math.floor(rank);
  const upperIndex = Math.ceil(rank);
  if (lowerIndex === upperIndex) return sorted[lowerIndex];
  const weight = rank - lowerIndex;
  return sorted[lowerIndex] * (1 - weight) + sorted[upperIndex] * weight;
}

function ranks(values) {
  return values.map(
    (value) =>
      1 +
      values.filter((candidate) => candidate < value).length +
      (values.filter((candidate) => candidate === value).length - 1) / 2,
  );
}

function pearson(left, right) {
  const leftMean = left.reduce((sum, value) => sum + value, 0) / left.length;
  const rightMean = right.reduce((sum, value) => sum + value, 0) / right.length;
  const numerator = left.reduce(
    (sum, value, index) => sum + (value - leftMean) * (right[index] - rightMean),
    0,
  );
  const leftScale = Math.sqrt(
    left.reduce((sum, value) => sum + (value - leftMean) ** 2, 0),
  );
  const rightScale = Math.sqrt(
    right.reduce((sum, value) => sum + (value - rightMean) ** 2, 0),
  );
  if (leftScale === 0 || rightScale === 0) return 0;
  return numerator / (leftScale * rightScale);
}

function isExcluded(frequency, exclusions) {
  return exclusions.some((range) => {
    const lower = range.minPerMeter ?? -Infinity;
    const upper = range.maxPerMeter ?? Infinity;
    return frequency >= lower && frequency <= upper;
  });
}

export function scoreProfilePsdVsScatterPsdShape(input) {
  const {
    profilePsdRows,
    scatterPsdRows,
    exclusions = [],
  } = input;
  if (!Array.isArray(profilePsdRows) || profilePsdRows.length < 2) {
    throw new Error('profilePsdRows must hold at least two rows.');
  }
  if (!Array.isArray(scatterPsdRows)) {
    throw new Error('scatterPsdRows must be an array.');
  }
  if (!Array.isArray(exclusions)) {
    throw new Error('exclusions must be an array of frequency ranges.');
  }

  // Keep each PSDscatter row only when it lies inside the independent profile
  // PSD support (interpolation returns null outside support; no extrapolation)
  // AND outside every source-defined instrument/specular/validity exclusion.
  const surviving = scatterPsdRows
    .map((row, index) => {
      assertFinite(row.spatialFrequencyPerMeter, `PSDscatter row ${index} frequency`);
      assertFinite(row.psd, `PSDscatter row ${index} value`);
      if (row.spatialFrequencyPerMeter <= 0 || row.psd <= 0) {
        throw new Error('PSDscatter frequencies and values must be positive.');
      }
      const predictedProfilePsd = interpolatePsdLogLog(
        profilePsdRows,
        row.spatialFrequencyPerMeter,
      );
      return {
        spatialFrequencyPerMeter: row.spatialFrequencyPerMeter,
        scatterPsd: row.psd,
        predictedProfilePsd,
        excluded: isExcluded(row.spatialFrequencyPerMeter, exclusions),
      };
    })
    .filter((row) => row.predictedProfilePsd !== null && !row.excluded)
    .sort(
      (left, right) =>
        left.spatialFrequencyPerMeter - right.spatialFrequencyPerMeter,
    );

  // Enforce unique surviving frequencies for clean log-log slope intervals.
  for (let index = 1; index < surviving.length; index += 1) {
    if (
      surviving[index].spatialFrequencyPerMeter ===
      surviving[index - 1].spatialFrequencyPerMeter
    ) {
      throw new Error('Surviving PSDscatter frequencies must be unique.');
    }
  }

  if (surviving.length < 8) {
    return {
      status: 'insufficient-surviving-rows',
      predeclarationHash: PREDECLARATION_HASH,
      rows: surviving,
      metrics: null,
      checks: [
        {
          check: 'at least eight surviving matched frequency rows',
          pass: false,
          value: surviving.length,
        },
      ],
      passed: false,
    };
  }

  const profileLog = surviving.map((row) => log10(row.predictedProfilePsd));
  const scatterLog = surviving.map((row) => log10(row.scatterPsd));
  const profileMedian = median(profileLog);
  const scatterMedian = median(scatterLog);

  // Subtract each curve's own median log10 over the identical surviving rows.
  // Removes one constant vertical scale offset, preserves frequency shape.
  const centeredProfile = profileLog.map((value) => value - profileMedian);
  const centeredScatter = scatterLog.map((value) => value - scatterMedian);
  const residuals = centeredProfile.map(
    (value, index) => value - centeredScatter[index],
  );
  const absoluteResiduals = residuals.map((value) => Math.abs(value));

  const rows = surviving.map((row, index) => ({
    ...row,
    profileLog10: profileLog[index],
    scatterLog10: scatterLog[index],
    centeredProfileLog10: centeredProfile[index],
    centeredScatterLog10: centeredScatter[index],
    centeredResidualLog10: residuals[index],
  }));

  const spearman = pearson(ranks(profileLog), ranks(scatterLog));
  const meanAbsoluteCenteredLog10Error =
    absoluteResiduals.reduce((sum, value) => sum + value, 0) /
    absoluteResiduals.length;
  const ninetiethPercentileAbsoluteResidual = percentile(
    absoluteResiduals,
    0.9,
  );

  // Adjacent log-log slope-sign agreement. Frequencies are sorted ascending and
  // unique, so the log-frequency denominator is positive; the slope sign equals
  // the sign of the log10-PSD increment.
  let agreeingIntervals = 0;
  const intervalCount = surviving.length - 1;
  for (let index = 1; index < surviving.length; index += 1) {
    const profileSlopeSign = Math.sign(profileLog[index] - profileLog[index - 1]);
    const scatterSlopeSign = Math.sign(scatterLog[index] - scatterLog[index - 1]);
    if (profileSlopeSign === scatterSlopeSign) agreeingIntervals += 1;
  }
  const slopeSignAgreement = agreeingIntervals / intervalCount;

  const minimumFrequency = surviving[0].spatialFrequencyPerMeter;
  const maximumFrequency = surviving.at(-1).spatialFrequencyPerMeter;
  const frequencyDecades = log10(maximumFrequency / minimumFrequency);

  const checks = [
    {
      check: 'at least eight surviving matched frequency rows',
      pass: surviving.length >= 8,
      value: surviving.length,
    },
    {
      check: 'surviving rows span at least 0.5 decade in spatial frequency',
      pass: frequencyDecades >= 0.5,
      value: frequencyDecades,
    },
    {
      check: 'Spearman rank correlation is at least 0.8',
      pass: spearman >= 0.8,
      value: spearman,
    },
    {
      check: 'median-centered log10-shape MAE is at most 0.25 dex',
      pass: meanAbsoluteCenteredLog10Error <= 0.25,
      value: meanAbsoluteCenteredLog10Error,
    },
    {
      check: '90th-percentile absolute centered log10 residual is at most 0.60 dex',
      pass: ninetiethPercentileAbsoluteResidual <= 0.6,
      value: ninetiethPercentileAbsoluteResidual,
    },
    {
      check: 'adjacent log-log slope signs agree for at least 80 percent of intervals',
      pass: slopeSignAgreement >= 0.8,
      value: slopeSignAgreement,
    },
  ];
  const passed = checks.every((check) => check.pass);

  return {
    status: passed
      ? 'profile-psd-scatter-psd-shape-pass'
      : 'profile-psd-scatter-psd-shape-fail',
    predeclarationHash: PREDECLARATION_HASH,
    rows,
    metrics: {
      spearman,
      meanAbsoluteCenteredLog10Error,
      ninetiethPercentileAbsoluteResidual,
      slopeSignAgreement,
      frequencyDecades,
      survivingRowCount: surviving.length,
    },
    checks,
    passed,
  };
}

export { PREDECLARATION_HASH };
