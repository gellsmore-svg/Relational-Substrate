function assertFinite(value, label) {
  if (!Number.isFinite(value)) {
    throw new Error(`${label} must be finite.`);
  }
}

export function degreesToRadians(degrees) {
  return (degrees * Math.PI) / 180;
}

export function spatialFrequency({
  scatterAngleDegrees,
  incidenceAngleDegrees,
  wavelengthMeters,
}) {
  assertFinite(scatterAngleDegrees, 'scatterAngleDegrees');
  assertFinite(incidenceAngleDegrees, 'incidenceAngleDegrees');
  assertFinite(wavelengthMeters, 'wavelengthMeters');
  if (wavelengthMeters <= 0) {
    throw new Error('wavelengthMeters must be positive.');
  }
  return (
    Math.abs(
      Math.sin(degreesToRadians(scatterAngleDegrees)) -
        Math.sin(degreesToRadians(incidenceAngleDegrees)),
    ) / wavelengthMeters
  );
}

function sortPsdRows(rows) {
  if (!Array.isArray(rows) || rows.length < 2) {
    throw new Error('PSD requires at least two rows.');
  }
  const sorted = rows
    .map((row, index) => {
      assertFinite(row.spatialFrequencyPerMeter, `PSD row ${index} frequency`);
      assertFinite(row.psd, `PSD row ${index} value`);
      if (row.spatialFrequencyPerMeter <= 0 || row.psd <= 0) {
        throw new Error('PSD frequencies and values must be positive for log-log interpolation.');
      }
      return { ...row };
    })
    .sort(
      (left, right) =>
        left.spatialFrequencyPerMeter - right.spatialFrequencyPerMeter,
    );
  for (let index = 1; index < sorted.length; index += 1) {
    if (
      sorted[index].spatialFrequencyPerMeter ===
      sorted[index - 1].spatialFrequencyPerMeter
    ) {
      throw new Error('PSD frequencies must be unique.');
    }
  }
  return sorted;
}

export function interpolatePsdLogLog(rows, frequency) {
  assertFinite(frequency, 'frequency');
  const sorted = sortPsdRows(rows);
  const minimum = sorted[0].spatialFrequencyPerMeter;
  const maximum = sorted.at(-1).spatialFrequencyPerMeter;
  if (frequency < minimum || frequency > maximum) return null;
  const exact = sorted.find(
    (row) => row.spatialFrequencyPerMeter === frequency,
  );
  if (exact) return exact.psd;
  const upperIndex = sorted.findIndex(
    (row) => row.spatialFrequencyPerMeter > frequency,
  );
  const lower = sorted[upperIndex - 1];
  const upper = sorted[upperIndex];
  const logFrequency = Math.log(frequency);
  const fraction =
    (logFrequency - Math.log(lower.spatialFrequencyPerMeter)) /
    (Math.log(upper.spatialFrequencyPerMeter) -
      Math.log(lower.spatialFrequencyPerMeter));
  return Math.exp(
    Math.log(lower.psd) + fraction * (Math.log(upper.psd) - Math.log(lower.psd)),
  );
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
    (sum, value, index) =>
      sum + (value - leftMean) * (right[index] - rightMean),
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

function trapezoidalArea(rows, valueKey) {
  return rows.slice(1).reduce((sum, row, index) => {
    const prior = rows[index];
    return (
      sum +
      ((row[valueKey] + prior[valueKey]) / 2) *
        (row.scatterAngleDegrees - prior.scatterAngleDegrees)
    );
  }, 0);
}

export function scorePsdBackedBrdfShape(input) {
  const {
    wavelengthMeters,
    incidenceAngleDegrees,
    specularAngleDegrees = incidenceAngleDegrees,
    specularMaskDegrees = 0.1,
    psdRows,
    brdfRows,
  } = input;
  if (!Array.isArray(brdfRows)) {
    throw new Error('brdfRows must be an array.');
  }
  const mappedRows = brdfRows
    .map((row, index) => {
      assertFinite(row.scatterAngleDegrees, `BRDF row ${index} angle`);
      assertFinite(row.brdf, `BRDF row ${index} value`);
      if (row.brdf < 0) throw new Error('BRDF values must be non-negative.');
      const mappedFrequency = spatialFrequency({
        scatterAngleDegrees: row.scatterAngleDegrees,
        incidenceAngleDegrees,
        wavelengthMeters,
      });
      return {
        ...row,
        mappedFrequencyPerMeter: mappedFrequency,
        predictedPsd: interpolatePsdLogLog(psdRows, mappedFrequency),
        maskedBySpecularCore:
          Math.abs(row.scatterAngleDegrees - specularAngleDegrees) <
          specularMaskDegrees,
      };
    })
    .filter(
      (row) => !row.maskedBySpecularCore && row.predictedPsd !== null,
    )
    .sort(
      (left, right) => left.scatterAngleDegrees - right.scatterAngleDegrees,
    );

  if (mappedRows.length < 5) {
    return {
      status: 'insufficient-supported-rows',
      rows: mappedRows,
      metrics: null,
      checks: [
        {
          check: 'at least five supported non-specular rows',
          pass: false,
          value: mappedRows.length,
        },
      ],
      passed: false,
    };
  }

  const maximumPredicted = Math.max(
    ...mappedRows.map((row) => row.predictedPsd),
  );
  const maximumMeasured = Math.max(...mappedRows.map((row) => row.brdf));
  if (maximumPredicted <= 0 || maximumMeasured <= 0) {
    throw new Error('Supported predicted and measured shapes must have positive maxima.');
  }
  const rows = mappedRows.map((row) => ({
    ...row,
    normalizedPredicted: row.predictedPsd / maximumPredicted,
    normalizedMeasured: row.brdf / maximumMeasured,
  }));
  const predictedValues = rows.map((row) => row.normalizedPredicted);
  const measuredValues = rows.map((row) => row.normalizedMeasured);
  const spearman = pearson(ranks(predictedValues), ranks(measuredValues));
  const meanAbsoluteError =
    rows.reduce(
      (sum, row) =>
        sum + Math.abs(row.normalizedPredicted - row.normalizedMeasured),
      0,
    ) / rows.length;
  const predictedPeak = rows.reduce((best, row) =>
    row.normalizedPredicted > best.normalizedPredicted ? row : best,
  );
  const measuredPeak = rows.reduce((best, row) =>
    row.normalizedMeasured > best.normalizedMeasured ? row : best,
  );
  const peakSideOrdering =
    Math.sign(predictedPeak.scatterAngleDegrees - specularAngleDegrees) ===
    Math.sign(measuredPeak.scatterAngleDegrees - specularAngleDegrees);
  const predictedArea = trapezoidalArea(rows, 'normalizedPredicted');
  const measuredArea = trapezoidalArea(rows, 'normalizedMeasured');
  const areaDifferenceFraction =
    measuredArea === 0
      ? predictedArea === 0
        ? 0
        : Infinity
      : Math.abs(predictedArea - measuredArea) / measuredArea;
  const checks = [
    {
      check: 'at least five supported non-specular rows',
      pass: rows.length >= 5,
      value: rows.length,
    },
    {
      check: 'peak-side ordering agrees',
      pass: peakSideOrdering,
      value: `${predictedPeak.scatterAngleDegrees} versus ${measuredPeak.scatterAngleDegrees}`,
    },
    {
      check: 'Spearman rank correlation is at least 0.8',
      pass: spearman >= 0.8,
      value: spearman,
    },
    {
      check: 'normalized-shape MAE is at most 0.20',
      pass: meanAbsoluteError <= 0.2,
      value: meanAbsoluteError,
    },
    {
      check: 'normalized area difference is at most 20 percent',
      pass: areaDifferenceFraction <= 0.2,
      value: areaDifferenceFraction,
    },
  ];
  const passed = checks.every((check) => check.pass);
  return {
    status: passed ? 'psd-backed-brdf-shape-pass' : 'psd-backed-brdf-shape-fail',
    rows,
    metrics: {
      spearman,
      meanAbsoluteError,
      predictedPeakAngleDegrees: predictedPeak.scatterAngleDegrees,
      measuredPeakAngleDegrees: measuredPeak.scatterAngleDegrees,
      predictedArea,
      measuredArea,
      areaDifferenceFraction,
    },
    checks,
    passed,
  };
}
