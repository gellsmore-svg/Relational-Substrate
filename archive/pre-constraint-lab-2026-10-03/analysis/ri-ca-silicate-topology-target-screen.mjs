import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

function round(value, places = 6) {
  return Number(value.toFixed(places));
}

function midpoint([low, high]) {
  return (low + high) / 2;
}

function biaxialScalar(alpha, beta, gamma) {
  return (alpha + beta + gamma) / 3;
}

const candidates = [
  {
    material: 'kilchoanite',
    formula: 'Ca3Si2O7',
    topologyClass: 'kilchoanite Ca sorosilicate polymorph',
    sourceUrl: 'https://handbookofmineralogy.org/pdfs/kilchoanite.pdf',
    density: 2.992,
    opticalClass: 'biaxial (-)',
    alphaRange: [1.646, 1.647],
    betaRange: [1.648, 1.648],
    gammaRange: [1.65, 1.65],
    sourceStrength: 'Handbook-backed',
    topologyContrast: 'dimorphous with rankinite; same ideal Ca3Si2O7 formula but different topology',
    decision: 'promote as next topology-discriminator target',
  },
  {
    material: 'larnite',
    formula: 'Ca2SiO4',
    topologyClass: 'Ca orthosilicate',
    sourceUrl: 'https://handbookofmineralogy.org/pdfs/larnite.pdf',
    density: midpoint([3.28, 3.33]),
    opticalClass: 'biaxial (+)',
    alphaRange: [1.7, 1.715],
    betaRange: [1.715, 1.723],
    gammaRange: [1.725, 1.74],
    sourceStrength: 'Handbook-backed',
    topologyContrast: 'Ca-only silicate, but formula and polymerization differ strongly from rankinite',
    decision: 'defer until after rankinite/kilchoanite pair',
  },
  {
    material: 'wollastonite',
    formula: 'CaSiO3',
    topologyClass: 'Ca chain silicate / pyroxenoid',
    sourceUrl: 'https://handbookofmineralogy.org/pdfs/wollastonite.pdf',
    density: midpoint([2.86, 3.09]),
    opticalClass: 'biaxial (-)',
    alphaRange: [1.616, 1.64],
    betaRange: [1.628, 1.65],
    gammaRange: [1.631, 1.653],
    sourceStrength: 'Handbook-backed but broad property ranges',
    topologyContrast: 'Ca-only chain silicate; useful broad transfer test but source ranges are wide',
    decision: 'defer as broader transfer target',
  },
];

const enrichedCandidates = candidates.map((candidate) => {
  const scalarRange = [
    biaxialScalar(candidate.alphaRange[0], candidate.betaRange[0], candidate.gammaRange[0]),
    biaxialScalar(candidate.alphaRange[1], candidate.betaRange[1], candidate.gammaRange[1]),
  ];
  return {
    ...candidate,
    scalarRiRange: scalarRange.map((value) => round(value)),
    scalarRiMidpoint: round(midpoint(scalarRange)),
  };
});

const screen = {
  source: 'ri-ca-silicate-topology-target-screen.mjs',
  status: 'target screening only; no prediction made',
  decision:
    'Promote kilchoanite as the next target because it keeps Ca3Si2O7 fixed and varies topology relative to rankinite. Larnite and wollastonite remain later Ca-only topology-transfer tests.',
  candidates: enrichedCandidates,
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# RI Ca-Silicate Topology Target Screen

## Scope

This screen follows the rankinite Ca-scaffold transfer failure. It looks for the next target that varies topology while keeping the cation set as close as possible to Ca-Si-O. It does not score any candidate and does not change coefficients.

## Candidates

${table(
  [
    'Material',
    'Formula',
    'Topology class',
    'Density',
    'Optical class',
    'Scalar RI range',
    'Scalar RI midpoint',
    'Source strength',
    'Topology contrast',
    'Decision',
  ],
  enrichedCandidates.map((row) => [
    row.material,
    row.formula,
    row.topologyClass,
    round(row.density),
    row.opticalClass,
    row.scalarRiRange.join('-'),
    row.scalarRiMidpoint,
    row.sourceStrength,
    row.topologyContrast,
    row.decision,
  ])
)}

## Sources

${table(
  ['Material', 'Source URL'],
  enrichedCandidates.map((row) => [row.material, row.sourceUrl])
)}

## Decision

Kilchoanite is the cleanest next topology discriminator. It is dimorphous with rankinite and keeps the same ideal formula, Ca3Si2O7, while changing topology. That makes it much cleaner than larnite or wollastonite for distinguishing a real topology gate from a rankinite-specific anomaly.

Larnite and wollastonite remain useful later, but they change formula/polymerization more strongly. Wollastonite also has broad Handbook density and optical ranges, making it a weaker immediate scoring target.
`;

await mkdir(outDir, { recursive: true });
await writeFile(new URL('ri-ca-silicate-topology-target-screen.json', outDir), JSON.stringify(screen, null, 2));
await writeFile(new URL('ri-ca-silicate-topology-target-screen.md', outDir), markdown);

console.log(markdown);
