import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const structures = [
  {
    material: 'gehlenite',
    codId: '1000048',
    sourceUrl: 'https://www.crystallography.net/cod/1000048.cif',
    reference:
      'Swainson et al. 1992, Neutron Diffraction Study of the Akermanite-Gehlenite Solid Solution Series',
    gateClass: 'melilite CaO8 tetrahedral-sheet scaffold',
    cell: { a: 7.685, b: 7.685, c: 5.0636, alpha: 90, beta: 90, gamma: 90 },
    symOps: [
      'x,y,z',
      '1/2-x,1/2+y,-z',
      '-x,-y,z',
      '1/2+x,1/2-y,-z',
      '-y,x,-z',
      '1/2+y,1/2+x,z',
      'y,-x,-z',
      '1/2-y,1/2-x,z',
    ],
    atoms: [
      ['Ca1', 'Ca', 0.3389, 0.1611, 0.5104],
      ['Al1', 'T', 0, 0, 0],
      ['T2', 'T', 0.1434, 0.3566, 0.954],
      ['O1', 'O', 0.5, 0, 0.1765],
      ['O2', 'O', 0.1427, 0.3573, 0.2835],
      ['O3', 'O', 0.0876, 0.1678, 0.8078],
    ],
    tetrahedralElements: new Set(['T']),
    scaffoldElements: new Set(['Ca']),
  },
  {
    material: 'akermanite',
    codId: '9006935',
    sourceUrl: 'https://www.crystallography.net/cod/9006935.cif',
    reference:
      'Kusaka et al. 2001, Determination of structures of Ca2CoSi2O7, Ca2MgSi2O7, and Ca2(Mg.55Fe.45)Si2O7, sample T = 297 K',
    gateClass: 'melilite CaO8 tetrahedral-sheet scaffold',
    cell: { a: 7.8348, b: 7.8348, c: 5.0087, alpha: 90, beta: 90, gamma: 90 },
    symOps: [
      'x,y,z',
      '1/2-y,1/2-x,z',
      'y,-x,-z',
      '1/2-x,1/2+y,-z',
      '-x,-y,z',
      '1/2+y,1/2+x,z',
      '-y,x,-z',
      '1/2+x,1/2-y,-z',
    ],
    atoms: [
      ['Mg', 'Mg', 0, 0, 0],
      ['Ca', 'Ca', 0.3318, 0.1682, 0.5066],
      ['Si', 'Si', 0.1397, 0.3603, 0.935],
      ['O1', 'O', 0, 0.5, 0.82],
      ['O2', 'O', 0.1402, 0.3598, 0.2551],
      ['O3', 'O', 0.0825, 0.187, 0.7883],
    ],
    tetrahedralElements: new Set(['Mg', 'Si']),
    scaffoldElements: new Set(['Ca']),
  },
  {
    material: 'rankinite',
    codId: '9012094',
    sourceUrl: 'https://www.crystallography.net/cod/9012094.cif',
    reference: 'Saburi et al. 1976, Refinement of the structure of rankinite',
    gateClass: 'Ca-polyhedra sheet plus inserted disilicate',
    cell: { a: 10.557, b: 8.885, c: 7.858, alpha: 90, beta: 119.586, gamma: 90 },
    symOps: ['x,y,z', '1/2+x,1/2-y,z', '1/2-x,1/2+y,-z', '-x,-y,-z'],
    atoms: [
      ['Ca1', 'Ca', 0.00867, 0.05871, 0.28957],
      ['Ca2', 'Ca', 0.16829, 0.57424, 0.20934],
      ['Ca3', 'Ca', 0.34078, 0.90736, 0.2849],
      ['Si1', 'Si', 0.09055, 0.21502, 0.98429],
      ['Si2', 'Si', 0.29602, 0.23395, 0.43206],
      ['O1', 'O', 0.35625, 0.3973, 0.42113],
      ['O2', 'O', 0.17948, 0.23873, 0.50723],
      ['O3', 'O', 0.40989, 0.10295, 0.54763],
      ['O4', 'O', 0.20191, 0.15519, 0.2098],
      ['O5', 'O', 0.09903, 0.39489, 0.97373],
      ['O6', 'O', 0.14429, 0.14102, 0.84624],
      ['O7', 'O', 0.9282, 0.16241, 0.93207],
    ],
    tetrahedralElements: new Set(['Si']),
    scaffoldElements: new Set(['Ca']),
  },
  {
    material: 'kilchoanite',
    codId: '9009443',
    sourceUrl: 'https://www.crystallography.net/cod/9009443.cif',
    reference: 'Taylor 1971, The crystal structure of kilchoanite, Ca6(SiO4)(Si3O10)',
    gateClass: 'mixed silicate-unit scaffold',
    cell: { a: 11.42, b: 5.09, c: 21.95, alpha: 90, beta: 90, gamma: 90 },
    symOps: [
      'x,y,z',
      '1/2+x,1/2+y,1/2+z',
      'x,-y,1/2+z',
      '1/2+x,1/2-y,+z',
      'x,y,1/2-z',
      '1/2+x,1/2+y,-z',
      'x,-y,-z',
      '1/2+x,1/2-y,1/2-z',
    ],
    atoms: [
      ['Ca1', 'Ca', -0.0134, 0, 0],
      ['Ca2', 'Ca', 0.286, 0.003, 0.25],
      ['Ca3', 'Ca', 0.0107, 0.005, 0.1679],
      ['Ca4', 'Ca', 0.2177, 0.501, 0.104],
      ['Si1', 'Si', 0.097, 0.426, 0.25],
      ['Si2', 'Si', 0.408, 0.94, 0.0997],
      ['Si3', 'Si', 0.24, 0, 0],
      ['O1', 'O', 0.164, 0.297, 0.1919],
      ['O2', 'O', -0.033, 0.293, 0.25],
      ['O3', 'O', 0.098, 0.759, 0.25],
      ['O4', 'O', 0.346, 0.793, 0.1584],
      ['O5', 'O', 0.035, 0.707, 0.0919],
      ['O6', 'O', 0.334, 0.802, 0.0402],
      ['O7', 'O', 0.404, 0.255, 0.0954],
      ['O8', 'O', 0.16, 0.179, 0.0412],
    ],
    tetrahedralElements: new Set(['Si']),
    scaffoldElements: new Set(['Ca']),
  },
  {
    material: 'larnite',
    codId: '9017424',
    sourceUrl: 'https://www.crystallography.net/cod/9017424.cif',
    reference:
      'Yamnova et al. 2011, Crystal structure of larnite beta-Ca2SiO4 and specific features of polymorphic transitions in dicalcium orthosilicate',
    gateClass: 'Ca orthosilicate beta-dicalcium-silicate scaffold',
    cell: { a: 5.5051, b: 6.7551, c: 9.3108, alpha: 90, beta: 94.513, gamma: 90 },
    symOps: ['x,y,z', '1/2+x,1/2-y,1/2+z', '1/2-x,1/2+y,1/2-z', '-x,-y,-z'],
    atoms: [
      ['Ca1', 'Ca', 0.2207, -0.0024, 0.702],
      ['Ca2', 'Ca', 0.2273, 0.3426, 0.4303],
      ['Si', 'Si', 0.2328, 0.2813, 0.0816],
      ['O1', 'O', 0.2828, 0.5121, 0.06],
      ['O2', 'O', 0.0212, 0.2481, 0.1919],
      ['O3', 'O', 0.4867, 0.1683, 0.1381],
      ['O4', 'O', 0.1561, 0.1712, -0.0725],
    ],
    tetrahedralElements: new Set(['Si']),
    scaffoldElements: new Set(['Ca']),
  },
];

const tBondCutoff = 1.95;
const scaffoldCutoff = 3.05;

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function radians(degrees) {
  return (degrees * Math.PI) / 180;
}

function basis(cell) {
  const alpha = radians(cell.alpha);
  const beta = radians(cell.beta);
  const gamma = radians(cell.gamma);
  const ax = [cell.a, 0, 0];
  const bx = [cell.b * Math.cos(gamma), cell.b * Math.sin(gamma), 0];
  const cx = [
    cell.c * Math.cos(beta),
    (cell.c * (Math.cos(alpha) - Math.cos(beta) * Math.cos(gamma))) / Math.sin(gamma),
    0,
  ];
  cx[2] = Math.sqrt(Math.max(0, cell.c ** 2 - cx[0] ** 2 - cx[1] ** 2));
  return [ax, bx, cx];
}

function cart(frac, vectors) {
  return [
    frac[0] * vectors[0][0] + frac[1] * vectors[1][0] + frac[2] * vectors[2][0],
    frac[0] * vectors[0][1] + frac[1] * vectors[1][1] + frac[2] * vectors[2][1],
    frac[0] * vectors[0][2] + frac[1] * vectors[1][2] + frac[2] * vectors[2][2],
  ];
}

function sub(a, b) {
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

function norm(v) {
  return Math.sqrt(v.reduce((sum, value) => sum + value ** 2, 0));
}

function angleDegrees(a, vertex, b) {
  const va = sub(a, vertex);
  const vb = sub(b, vertex);
  const cosine = va.reduce((sum, value, index) => sum + value * vb[index], 0) / (norm(va) * norm(vb));
  return (Math.acos(Math.min(1, Math.max(-1, cosine))) * 180) / Math.PI;
}

function parseTerm(term, variables) {
  const compact = term.replace(/\s+/g, '').replace(/^\+/, '');
  if (compact === '') return 0;
  const normalized = compact.replace(/-/g, '+-');
  return normalized
    .split('+')
    .filter(Boolean)
    .reduce((sum, part) => {
      if (part in variables) return sum + variables[part];
      if (part.startsWith('-') && part.slice(1) in variables) return sum - variables[part.slice(1)];
      if (part.includes('/')) {
        const [num, denom] = part.split('/').map(Number);
        return sum + num / denom;
      }
      return sum + Number(part);
    }, 0);
}

function applySymOp(op, frac) {
  const variables = { x: frac[0], y: frac[1], z: frac[2] };
  return op.split(',').map((term) => mod1(parseTerm(term, variables)));
}

function mod1(value) {
  const result = value - Math.floor(value);
  return result < 1e-8 ? 0 : result;
}

function uniqueAtoms(structure) {
  const seen = new Set();
  const atoms = [];
  for (const [label, element, x, y, z] of structure.atoms) {
    for (const [opIndex, op] of structure.symOps.entries()) {
      const frac = applySymOp(op, [x, y, z]).map((value) => round(value, 6));
      const key = `${label}:${element}:${frac.join(',')}`;
      if (seen.has(key)) continue;
      seen.add(key);
      atoms.push({ label, element, opIndex, frac });
    }
  }
  return atoms;
}

function expandedAtoms(atoms, vectors) {
  const expanded = [];
  for (const atom of atoms) {
    for (let i = -1; i <= 1; i += 1) {
      for (let j = -1; j <= 1; j += 1) {
        for (let k = -1; k <= 1; k += 1) {
          const frac = [atom.frac[0] + i, atom.frac[1] + j, atom.frac[2] + k];
          expanded.push({ ...atom, translation: [i, j, k], cart: cart(frac, vectors) });
        }
      }
    }
  }
  return expanded;
}

function nearestNeighbors(center, candidates, allowedElements, cutoff) {
  return candidates
    .filter((candidate) => allowedElements.has(candidate.element))
    .map((candidate) => ({
      ...candidate,
      distance: norm(sub(candidate.cart, center.cart)),
    }))
    .filter((candidate) => candidate.distance > 1e-6 && candidate.distance <= cutoff)
    .sort((a, b) => a.distance - b.distance);
}

function summarize(values) {
  if (values.length === 0) return null;
  return {
    count: values.length,
    min: round(Math.min(...values)),
    max: round(Math.max(...values)),
    mean: round(values.reduce((sum, value) => sum + value, 0) / values.length),
  };
}

function analyzeStructure(structure) {
  const vectors = basis(structure.cell);
  const atoms = uniqueAtoms(structure);
  const expanded = expandedAtoms(atoms, vectors);
  const uniqueOxygens = atoms.filter((atom) => atom.element === 'O').map((atom) => ({ ...atom, cart: cart(atom.frac, vectors) }));
  const uniqueScaffolds = atoms
    .filter((atom) => structure.scaffoldElements.has(atom.element))
    .map((atom) => ({ ...atom, cart: cart(atom.frac, vectors) }));

  const bridgeRowsAll = uniqueOxygens
    .map((oxygen) => {
      const tNeighbors = nearestNeighbors(oxygen, expanded, structure.tetrahedralElements, tBondCutoff);
      const uniqueNeighborKeys = new Set();
      const uniqueNeighbors = [];
      for (const neighbor of tNeighbors) {
        const key = `${neighbor.label}:${neighbor.element}:${neighbor.frac.join(',')}:${neighbor.translation.join(',')}`;
        if (uniqueNeighborKeys.has(key)) continue;
        uniqueNeighborKeys.add(key);
        uniqueNeighbors.push(neighbor);
      }
      if (uniqueNeighbors.length !== 2) {
        return {
          oxygen: oxygen.label,
          tNeighborCount: uniqueNeighbors.length,
          tNeighbors: uniqueNeighbors.map((neighbor) => `${neighbor.label}@${round(neighbor.distance, 4)}`),
          angle: null,
        };
      }
      return {
        oxygen: oxygen.label,
        tNeighborCount: uniqueNeighbors.length,
        tNeighbors: uniqueNeighbors.map((neighbor) => `${neighbor.label}@${round(neighbor.distance, 4)}`),
        angle: round(angleDegrees(uniqueNeighbors[0].cart, oxygen.cart, uniqueNeighbors[1].cart), 3),
      };
    })
    .filter((row) => row.tNeighborCount >= 2);

  const bridgeRows = dedupeRows(
    bridgeRowsAll,
    (row) => `${row.oxygen}:${row.tNeighborCount}:${row.tNeighbors.join(',')}:${row.angle}`
  );

  const scaffoldRowsAll = uniqueScaffolds.map((site) => {
    const oxygenNeighbors = nearestNeighbors(site, expanded, new Set(['O']), scaffoldCutoff);
    const deDuped = [];
    const keys = new Set();
    for (const neighbor of oxygenNeighbors) {
      const key = `${neighbor.label}:${neighbor.frac.join(',')}:${neighbor.translation.join(',')}`;
      if (keys.has(key)) continue;
      keys.add(key);
      deDuped.push(neighbor);
    }
    return {
      site: site.label,
      element: site.element,
      coordinationCount: deDuped.length,
      minDistance: round(Math.min(...deDuped.map((neighbor) => neighbor.distance))),
      maxDistance: round(Math.max(...deDuped.map((neighbor) => neighbor.distance))),
      meanDistance: round(deDuped.reduce((sum, neighbor) => sum + neighbor.distance, 0) / deDuped.length),
    };
  });

  const scaffoldRows = dedupeRows(scaffoldRowsAll, (row) => `${row.site}:${row.coordinationCount}:${row.meanDistance}`);

  const angles = bridgeRows.map((row) => row.angle).filter((value) => value !== null);
  return {
    material: structure.material,
    codId: structure.codId,
    gateClass: structure.gateClass,
    sourceUrl: structure.sourceUrl,
    reference: structure.reference,
    bridgeRows,
    scaffoldRows,
    bridgeAngleSummary: summarize(angles),
    scaffoldCoordinationSummary: summarize(scaffoldRows.map((row) => row.coordinationCount)),
    scaffoldDistanceSummary: summarize(scaffoldRows.map((row) => row.meanDistance)),
  };
}

function dedupeRows(rows, keyFn) {
  const seen = new Set();
  const deduped = [];
  for (const row of rows) {
    const key = keyFn(row);
    if (seen.has(key)) continue;
    seen.add(key);
    deduped.push(row);
  }
  return deduped;
}

const analyses = structures.map(analyzeStructure);

const readinessShift = [
  {
    descriptor: 'T-O-T / Si-O-Si bridge angle',
    previousStatus: 'blocked',
    newStatus: 'CIF-derived candidate ready',
    caveat: 'Angles depend on bond cutoff and generated symmetry; validate against published bond-angle tables before fitting.',
  },
  {
    descriptor: 'Ca coordination count',
    previousStatus: 'categorical only',
    newStatus: 'CIF-derived numeric candidate ready',
    caveat: 'Coordination counts depend on the oxygen cutoff; keep cutoff fixed and record it with any model.',
  },
  {
    descriptor: 'Ca-O mean distance',
    previousStatus: 'partly ready',
    newStatus: 'CIF-derived numeric candidate ready',
    caveat: 'Use as diagnostic descriptor first; do not refit optical coefficients without held-out target.',
  },
];

const report = {
  source: 'ri-cif-geometry-extraction-diagnostic.mjs',
  status: 'CIF-derived geometry diagnostic; no optical fit',
  cutoffs: { tBondCutoff, scaffoldCutoff },
  analyses,
  readinessShift,
};

function table(headers, bodyRows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...bodyRows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI CIF Geometry Extraction Diagnostic

## Scope

This diagnostic computes structural descriptors from COD CIF coordinates for gehlenite, akermanite, rankinite, kilchoanite, and the reserved larnite target. It does not score a new optical target and does not fit a repair term.

Cutoffs:

- T-O bond cutoff: ${tBondCutoff} A
- Ca/M-O scaffold cutoff: ${scaffoldCutoff} A

## Summary

${table(
  ['Material', 'COD', 'Gate class', 'Bridge angle summary', 'Scaffold coordination summary', 'Mean scaffold distance summary'],
  analyses.map((row) => [
    row.material,
    row.codId,
    row.gateClass,
    row.bridgeAngleSummary
      ? `${row.bridgeAngleSummary.min}-${row.bridgeAngleSummary.max} deg; mean ${row.bridgeAngleSummary.mean}; n=${row.bridgeAngleSummary.count}`
      : 'none',
    row.scaffoldCoordinationSummary
      ? `${row.scaffoldCoordinationSummary.min}-${row.scaffoldCoordinationSummary.max}; mean ${row.scaffoldCoordinationSummary.mean}`
      : 'none',
    row.scaffoldDistanceSummary
      ? `${row.scaffoldDistanceSummary.min}-${row.scaffoldDistanceSummary.max} A; mean ${row.scaffoldDistanceSummary.mean}`
      : 'none',
  ])
)}

## Bridge Rows

${analyses
  .map(
    (analysis) => `### ${analysis.material}

${table(
  ['O site', 'T-neighbor count', 'T neighbors', 'Angle'],
  analysis.bridgeRows.map((row) => [
    row.oxygen,
    row.tNeighborCount,
    row.tNeighbors.join('; '),
    row.angle ?? 'not two-coordinate',
  ])
)}
`
  )
  .join('\n')}

## Scaffold Rows

${analyses
  .map(
    (analysis) => `### ${analysis.material}

${table(
  ['Site', 'Coordination count', 'Min distance', 'Mean distance', 'Max distance'],
  analysis.scaffoldRows.map((row) => [
    row.site,
    row.coordinationCount,
    row.minDistance,
    row.meanDistance,
    row.maxDistance,
  ])
)}
`
  )
  .join('\n')}

## Readiness Shift

${table(
  ['Descriptor', 'Previous status', 'New status', 'Caveat'],
  readinessShift.map((row) => [row.descriptor, row.previousStatus, row.newStatus, row.caveat])
)}

## Sources

${table(
  ['Material', 'COD source', 'Reference'],
  analyses.map((row) => [row.material, row.sourceUrl, row.reference])
)}

## Reading

The bridge-angle and scaffold-distance descriptors can now be treated as CIF-derived candidates. They should still be validated against published bond-angle tables before promotion to an optical coefficient. The immediate safe use is diagnostic: compare whether these descriptors separate melilite from Ca3Si2O7 polymorphs more cleanly than Ca/O or oxygen volume.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-cif-geometry-extraction-diagnostic.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-cif-geometry-extraction-diagnostic.md', outDir), markdown);

console.log(markdown);
