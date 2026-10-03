import { spawn } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';

// Consolidated runner for the roughness PSD/scatter model-form track. It
// regenerates, in narrative order, the two frozen comparator lineages:
//   Form 1 -- conventional Rayleigh-Rice PSD-backed BRDF shape comparator v0
//   Form 2 -- independent-profile-PSD versus BRDF-derived-PSD shape comparator v0
// Each step is a small deterministic script writing Markdown/JSON under
// analysis/out/. This runner adds a status column read back from each step's JSON
// so the whole track -- including the deliberately blocked/failed-but-expected
// source locks -- is auditable in one place. It asserts no evidence and changes
// no confidence; the scorers are validated only on synthetic known-answer fixtures.

const outDir = new URL('./out/', import.meta.url);

const steps = [
  // ----- Form 1: Rayleigh-Rice PSD-backed raw BRDF shape comparator -----
  {
    script: 'roughness-psd-brdf-model-form-predeclaration.mjs',
    form: 'Form 1',
    stage: 'model-form predeclaration',
    role: 'freezes the Rayleigh-Rice PSD-backed BRDF shape comparator v0 before any target scoring',
  },
  {
    script: 'roughness-psd-brdf-source-availability-screen.mjs',
    form: 'Form 1',
    stage: 'source-availability screen',
    role: 'metadata screen; selects the Tayabaly optical-flat source for reservation',
  },
  {
    script: 'roughness-tungsten-brdf-target-reservation.mjs',
    form: 'Form 1',
    stage: 'tungsten target reservation',
    role: 'reserves the first Le Bohec tungsten specimen before full-text extraction',
  },
  {
    script: 'roughness-tungsten-brdf-source-lock-screen.mjs',
    form: 'Form 1',
    stage: 'tungsten source lock',
    role: 'fails the lock: angular BRDF trace has no stated wavelength for the frozen mapping',
  },
  {
    script: 'roughness-tayabaly-brdf-target-reservation.mjs',
    form: 'Form 1',
    stage: 'tayabaly target reservation',
    role: 'reserves the first Tayabaly optical-flat specimen and condition before lookup',
  },
  {
    script: 'roughness-tayabaly-brdf-source-lock-screen.mjs',
    form: 'Form 1',
    stage: 'tayabaly source lock',
    role: 'fails the lock: source exposes BRDF-derived PSDscatter, not raw angular BRDF rows',
  },
  {
    script: 'roughness-psd-brdf-feasibility-diagnostic.mjs',
    form: 'Form 1',
    stage: 'scorer known-answer test',
    role: 'synthetic feasibility: matching fixture passes, inverse-shape fixture fails',
  },
  // ----- Form 2: independent-profile-PSD versus scatter-derived-PSD comparator -----
  {
    script: 'roughness-profile-psd-scatter-psd-predeclaration.mjs',
    form: 'Form 2',
    stage: 'model-form predeclaration',
    role: 'freezes the profile-PSD versus scatter-derived-PSD shape comparator v0 (hash ad3892b700d0b82f)',
  },
  {
    script: 'roughness-profile-psd-scatter-psd-feasibility-diagnostic.mjs',
    form: 'Form 2',
    stage: 'scorer known-answer test',
    role: 'synthetic feasibility: offset-only match passes, inverse-shape fails, support/exclusion drops verified',
  },
  {
    script: 'roughness-profile-psd-scatter-psd-source-screen.mjs',
    form: 'Form 2',
    stage: 'source screen',
    role: 'metadata screen; selects Duparre 2002, rejects Schroeder/Harvey/Optik on construct',
  },
  {
    script: 'roughness-duparre-profile-psd-scatter-psd-target-reservation.mjs',
    form: 'Form 2',
    stage: 'duparre target reservation',
    role: 'reserves Duparre 2002 with a source-order rule (hash 5305a937566e8b24) before lookup',
  },
  {
    script: 'roughness-duparre-profile-psd-scatter-psd-source-lock-screen.mjs',
    form: 'Form 2',
    stage: 'duparre source lock',
    role: 'blocked: full text paywalled / 403; required facts not exposed, nothing fabricated',
  },
  {
    script: 'roughness-sulc-open-access-feasibility-record.mjs',
    form: 'Form 2',
    stage: 'sulc open-access record',
    role: 'open-access same-construct source read; exposed/feasibility-only; AFM PSD is figure-only so no score',
  },
];

await mkdir(outDir, { recursive: true });

const startedAt = new Date().toISOString();
const results = [];
for (const [index, step] of steps.entries()) {
  const run = await runStep(step);
  const status = await readStatus(step.script);
  results.push({ index: index + 1, ...step, ...run, reportedStatus: status });
}
const finishedAt = new Date().toISOString();

const failed = results.filter((result) => result.exitCode !== 0);
const report = {
  source: 'roughness-psd-scatter-chain-runner.mjs',
  status:
    failed.length === 0
      ? 'all roughness PSD/scatter chain steps completed'
      : 'one or more roughness chain steps failed to execute',
  note: 'execution success only; several steps intentionally record blocked or failed source locks. No evidence is asserted and no confidence changes.',
  startedAt,
  finishedAt,
  steps: results,
};

function table(headers, rows) {
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((row) => `| ${row.join(' | ')} |`),
  ].join('\n');
}

const markdown = `# Roughness PSD/Scatter Chain Runner

## Scope

Regenerates the roughness PSD/scatter model-form track in narrative order across
both frozen comparators (Form 1: Rayleigh-Rice PSD-backed raw BRDF; Form 2:
independent profile PSD versus scatter-derived PSD). Each step writes
Markdown/JSON under \`analysis/out/\`. Run directly with:

\`\`\`sh
node analysis/roughness-psd-scatter-chain-runner.mjs
\`\`\`

The "Exit" column is process success; the "Reported status" column is read back
from each step's JSON. Several source-lock steps intentionally report blocked or
failed locks -- that is the disciplined record, not a regression. No step asserts
substrate evidence; both scorers are validated only on synthetic known-answer
fixtures.

## Status

| Field | Value |
|---|---|
| Started | ${startedAt} |
| Finished | ${finishedAt} |
| Execution | ${report.status} |

## Steps

${table(
  ['#', 'Form', 'Stage', 'Script', 'Exit', 'Reported status'],
  results.map((row) => [
    row.index,
    row.form,
    row.stage,
    row.script,
    row.exitCode,
    row.reportedStatus,
  ]),
)}

## Live blocking point

Form 2 is fully built and synthetically validated, but real scoring is blocked
because this AFM + ARS literature publishes the independent topography PSD as a
figure, not numerical rows (Duparre 2002 access-blocked; Sulc 2023 readable but
AFM PSD figure-only; Sustek 2021 closed-access). Unblock paths are recorded in the
Sulc feasibility record and the Duparre source-lock screen.
`;

await writeFile(
  new URL('roughness-psd-scatter-chain-runner.json', outDir),
  `${JSON.stringify(report, null, 2)}\n`,
);
await writeFile(new URL('roughness-psd-scatter-chain-runner.md', outDir), markdown);

console.log(markdown);

if (failed.length > 0) {
  process.exitCode = 1;
}

async function readStatus(script) {
  const jsonName = script.replace(/\.mjs$/, '.json');
  try {
    const parsed = JSON.parse(await readFile(new URL(jsonName, outDir), 'utf8'));
    return parsed.status ?? parsed.sourceLockDecision?.status ?? 'recorded';
  } catch {
    return 'no-json';
  }
}

function runStep(step) {
  return new Promise((resolve) => {
    const startedAtMs = Date.now();
    const child = spawn(process.execPath, [new URL(step.script, import.meta.url).pathname], {
      stdio: 'ignore',
      shell: false,
    });
    child.on('error', (error) => {
      resolve({ exitCode: 1, durationMs: Date.now() - startedAtMs, error: error.message });
    });
    child.on('close', (exitCode) => {
      resolve({ exitCode, durationMs: Date.now() - startedAtMs });
    });
  });
}
