import { mkdir, readFile, writeFile } from 'node:fs/promises';

// Source-lock attempt for the reserved Duparre et al. (2002) profile-PSD versus
// scatter-derived-PSD target (reservation hash 5305a937566e8b24, serving model
// form ad3892b700d0b82f).
//
// The reservation requires three full-text facts before any numerical extraction:
// the sample presentation order (hence the first eligible sample), the stated
// angle-resolved-scattering wavelength/geometry, and a topography-PSD/scatter-PSD
// overlap band exposing at least eight matched rows over at least 0.5 decade.
//
// None of these are available from the abstract or accessible index metadata. The
// publisher full text (Optica) is paywalled and the ResearchGate full text returns
// HTTP 403. Per the discipline, this is recorded as an access block, not a guess:
// no sample identity, wavelength, or curve value is asserted from secondary
// search-engine summaries.

const outDir = new URL('./out/', import.meta.url);

const reservation = JSON.parse(
  await readFile(
    new URL('roughness-duparre-profile-psd-scatter-psd-target-reservation.json', outDir),
    'utf8',
  ),
);

const accessAttempts = [
  {
    location: 'Optica (Applied Optics) publisher landing page, ao-41-1-154',
    result: 'abstract and citation metadata only; full text paywalled',
  },
  {
    location:
      'ResearchGate full-text page (publication 11464315)',
    result: 'HTTP 403 Forbidden; full text not retrievable without authentication',
  },
  {
    location:
      'Fraunhofer IOF PSD-analysis competence page (claimed by a search summary to host the PDF)',
    result:
      'checked: the page hosts only annual-report PDFs and a publica.fraunhofer.de search link; it does NOT host this paper. The search-summary PDF claim was false.',
  },
  {
    location: 'publica.fraunhofer.de repository search',
    result:
      'results are rendered client-side (JavaScript); record/full-text availability could not be read by static fetch',
  },
];

const requiredFacts = [
  {
    fact: 'sample presentation order and the first eligible sample identity',
    status: 'unconfirmed: not exposed in accessible metadata',
  },
  {
    fact: 'angle-resolved-scattering wavelength and geometry',
    status: 'unconfirmed: not stated in the abstract',
  },
  {
    fact: 'a same-sample topography PSD and scatter-derived PSD plotted over a shared spatial-frequency band',
    status:
      'plausible from the abstract (2D PSDs computed from all techniques for direct comparison) but the paired-plot presentation is not verifiable without full text',
  },
  {
    fact: 'overlap band exposing at least eight matched rows over at least 0.5 decade',
    status: 'unconfirmed: requires full-text curve inspection',
  },
];

const sourceLockDecision = {
  status: 'source-lock-blocked-full-text-not-accessible',
  scoringAllowed: false,
  reservationHash: reservation.predeclaration.hash,
  servesModelFormHash: reservation.frozenContract.servesModelFormHash,
  reason:
    'the reserved target requires the sample presentation order, the stated scattering wavelength/geometry, and a verified topography-PSD/scatter-PSD overlap band, none of which are exposed by the abstract or accessible index; the publisher full text is paywalled and the ResearchGate full text returns 403, so the lock cannot be completed without fabricating source facts',
  evidenceStatus: 'none; no sample identity, wavelength, or curve value asserted',
  prohibited: [
    'do not assert the first sample identity or material from a secondary search-engine summary',
    'do not assume a 632.8 nm or any other scattering wavelength without the source stating it',
    'do not extract or estimate any numerical PSD rows',
  ],
  recovery: [
    'obtain verified full text via institutional Optica access (the Fraunhofer IOF competence page was checked and does not host the PDF; the publica.fraunhofer.de repository may hold an author copy but renders client-side and needs an interactive session to confirm), then confirm the three required facts and source-lock against hash 5305a937566e8b24',
    'do NOT fall back to Schroeder et al., Opt. Express 19, 9820 (2011) for this comparator: checked 2026-06-24, it is measured-ARS versus modeled-ARS (topography PSD is the model input) and supplies no independent scatter-derived PSD curve; it is a Form-1 candidate only. If Duparre 2002 stays inaccessible, run a fresh metadata screen for another same-specimen independent-topography-PSD plus scatter-derived-PSD source',
  ],
};

const report = {
  source: 'roughness-duparre-profile-psd-scatter-psd-source-lock-screen.mjs',
  date: '2026-06-24',
  validationClaim: false,
  reservation: {
    hash: reservation.predeclaration.hash,
    target: reservation.predeclaration.target,
    sourceCandidate: reservation.sourceCandidate,
  },
  accessAttempts,
  requiredFacts,
  sourceLockDecision,
};

const markdown = `# Duparre 2002 Profile-PSD versus Scatter-PSD Source-Lock Screen

Status: **${sourceLockDecision.status}**

Reservation hash: \`${sourceLockDecision.reservationHash}\` (serves model form \`${sourceLockDecision.servesModelFormHash}\`).

## Access Attempts

| Location | Result |
|---|---|
${accessAttempts.map((row) => `| ${row.location} | ${row.result} |`).join('\n')}

## Required Full-Text Facts

| Fact | Status |
|---|---|
${requiredFacts.map((row) => `| ${row.fact} | ${row.status} |`).join('\n')}

Reason: ${sourceLockDecision.reason}.

Scoring allowed: **no**.

Recovery:

${sourceLockDecision.recovery.map((item) => `- ${item}`).join('\n')}

Evidence status: ${sourceLockDecision.evidenceStatus}.
`;

await mkdir(outDir, { recursive: true });
await writeFile(
  new URL('roughness-duparre-profile-psd-scatter-psd-source-lock-screen.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(
  new URL('roughness-duparre-profile-psd-scatter-psd-source-lock-screen.md', outDir),
  markdown,
);

console.log(`Duparre profile/scatter PSD source lock: ${sourceLockDecision.status}`);
