import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';

const outDir = new URL('./out/', import.meta.url);

const steps = [
  {
    script: 'ri-structural-descriptor-validation.mjs',
    stage: 'prelookup descriptor guardrail',
    role: 'baseline RI descriptor separability and coefficient diagnostics',
  },
  {
    script: 'ri-topology-volume-descriptor-diagnostic.mjs',
    stage: 'topology volume descriptors',
    role: 'fold-density / oxygen-volume / Lorentz-Lorenz descriptor exposure',
  },
  {
    script: 'external-ri-gehlenite-fresh-validation.mjs',
    stage: 'fresh melilite failure',
    role: 'paper-backed gehlenite validation against frozen pre-melilite RI families',
  },
  {
    script: 'ri-melilite-topology-diagnostic.mjs',
    stage: 'melilite topology diagnosis',
    role: 'separates melilite topology, Ca scaffold, and T-site chemistry',
  },
  {
    script: 'external-ri-akermanite-source-qualified-validation.mjs',
    stage: 'source-qualified melilite failure',
    role: 'akermanite check showing failure is not only tetrahedral Al',
  },
  {
    script: 'ri-ca-scaffold-response-diagnostic.mjs',
    stage: 'variable-type diagnosis',
    role: 'distinguishes Al charge-compensation response from Ca scaffold response',
  },
  {
    script: 'ri-ca-scaffold-repair-diagnostic.mjs',
    stage: 'post-failure repair diagnostic',
    role: 'tests Ca and Ca/Mg scaffold split as calibration debt',
  },
  {
    script: 'external-ri-hardystonite-ca-scaffold-validation.mjs',
    stage: 'same-topology Ca-scaffold validation',
    role: 'hardystonite failure exposes T1 Zn / d10 buffering problem',
  },
  {
    script: 'ri-melilite-t1-cation-diagnostic.mjs',
    stage: 'T1 cation source anchoring',
    role: 'records radii and dielectric polarizability scales for Al/Mg/Zn',
  },
  {
    script: 'ri-melilite-t1-field-buffer-diagnostic.mjs',
    stage: 'T1 field-buffer diagnosis',
    role: 'splits T1 response into field strength, polarizability, and d10 marker',
  },
  {
    script: 'ri-melilite-t1-buffer-freeze-contract.mjs',
    stage: 'model-form freeze',
    role: 'locks allowed descriptors, rejected shortcuts, falsifiers, and target classes',
  },
  {
    script: 'ri-rankinite-target-prequalification.mjs',
    stage: 'rankinite source qualification',
    role: 'reserves rankinite as Ca-scaffold transfer target without scoring',
  },
  {
    script: 'ri-melilite-repeat-target-screen.mjs',
    stage: 'same-class melilite screen',
    role: 'defers gugiaite/alumoakermanite and keeps rankinite as cleaner falsifier',
  },
  {
    script: 'external-ri-rankinite-ca-scaffold-transfer-validation.mjs',
    stage: 'rankinite transfer validation',
    role: 'tests scalar Ca-scaffold transfer outside melilite',
  },
  {
    script: 'ri-ca-silicate-topology-target-screen.mjs',
    stage: 'Ca-only topology target screen',
    role: 'promotes kilchoanite over larnite/wollastonite as paired-polymorph discriminator',
  },
  {
    script: 'external-ri-kilchoanite-ca-scaffold-transfer-validation.mjs',
    stage: 'kilchoanite transfer validation',
    role: 'paired Ca3Si2O7 polymorph test after rankinite',
  },
  {
    script: 'ri-ca-scaffold-topology-gate-diagnostic.mjs',
    stage: 'topology gate synthesis',
    role: 'consolidates melilite versus Ca3Si2O7 residual pattern',
  },
  {
    script: 'ri-structural-gate-source-diagnostic.mjs',
    stage: 'source-backed structural gate',
    role: 'promotes Ca polyhedral environment and silicate-unit connectivity as gates',
  },
  {
    script: 'ri-structural-numeric-readiness-diagnostic.mjs',
    stage: 'numeric structural readiness',
    role: 'blocks numeric bridge-angle fitting until comparable structure values are sourced',
  },
  {
    script: 'ri-cif-geometry-extraction-diagnostic.mjs',
    stage: 'CIF geometry extraction',
    role: 'derives candidate bridge-angle and scaffold-distance descriptors from COD CIF coordinates',
  },
  {
    script: 'ri-cif-residual-separation-diagnostic.mjs',
    stage: 'CIF residual separation',
    role: 'joins CIF geometry to frozen split-Ca residuals without fitting a new optical coefficient',
  },
  {
    script: 'ri-cif-candidate-gate-diagnostic.mjs',
    stage: 'CIF candidate gate',
    role: 'states falsifiable Ca-scaffold gate hypotheses without promoting a threshold',
  },
  {
    script: 'ri-heldout-larnite-reservation-diagnostic.mjs',
    stage: 'held-out larnite reservation',
    role: 'reserves larnite with optical and CIF sources before geometry extraction or RI scoring',
  },
  {
    script: 'ri-larnite-gate-classification-diagnostic.mjs',
    stage: 'held-out larnite gate classification',
    role: 'classifies larnite CIF geometry against frozen Ca-scaffold gates before optical scoring',
  },
  {
    script: 'external-ri-larnite-ca-scaffold-transfer-validation.mjs',
    stage: 'larnite transfer validation',
    role: 'scores larnite after frozen gate classification to test non-transfer of melilite Ca uplift',
  },
  {
    script: 'ri-larnite-density-control-contrast-diagnostic.mjs',
    stage: 'larnite density-control contrast',
    role: 'explains baseline-density pass versus split-Ca failure without promoting a repair',
  },
  {
    script: 'ri-density-control-falsifier-reservation-diagnostic.mjs',
    stage: 'density-control falsifier reservation',
    role: 'reserves merwinite as the next high-density control target without scoring it',
  },
  {
    script: 'external-ri-merwinite-density-control-validation.mjs',
    stage: 'merwinite density-control validation',
    role: 'scores reserved merwinite under frozen families while preserving Mg-bearing limitation',
  },
  {
    script: 'ri-post-merwinite-target-reservation-diagnostic.mjs',
    stage: 'post-merwinite target reservation',
    role: 'reserves spurrite to reduce the merwinite Mg confound without scoring it',
  },
  {
    script: 'ri-wollastonite-polytype-source-lock-screen.mjs',
    stage: 'wollastonite polytype source-lock screen',
    role: 'blocks wollastonite scoring until optical constants, density, and CIF refer to one polytype',
  },
  {
    script: 'external-ri-spurrite-confound-substitution-validation.mjs',
    stage: 'spurrite confound-substitution validation',
    role: 'scores reserved spurrite under frozen families while preserving carbonate limitation',
  },
  {
    script: 'ri-pure-ca-si-o-source-exhaustion-screen.mjs',
    stage: 'pure Ca-silicate source exhaustion screen',
    role: 'records that no new pure Ca-Si-O held-out target is source-locked under current rules',
  },
  {
    script: 'ri-ca-scaffold-model-form-quarantine-diagnostic.mjs',
    stage: 'Ca-scaffold model-form quarantine',
    role: 'quarantines baseline, split-Ca, and split-Ca/Mg families as reference diagnostics only',
  },
  {
    script: 'ri-structural-model-form-predeclaration.mjs',
    stage: 'structural RI model-form predeclaration',
    role: 'freezes the next allowed structural descriptor set before any new target scoring',
  },
];

await mkdir(outDir, { recursive: true });

const startedAt = new Date().toISOString();
const results = [];

for (const [index, step] of steps.entries()) {
  const result = await runStep(step);
  results.push({ index: index + 1, ...step, ...result });
}

const finishedAt = new Date().toISOString();
const failed = results.filter((result) => result.exitCode !== 0);
const report = {
  source: 'ri-refractive-index-chain-runner.mjs',
  status: failed.length === 0 ? 'all RI chain steps completed' : 'one or more RI chain steps failed',
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

const markdown = `# RI Refractive-Index Chain Runner

## Scope

This runner regenerates the refractive-index diagnostic chain in order. It is a deterministic Node-based modelling workflow: each step is a small script that writes Markdown/JSON outputs under \`analysis/out/\`.

It deliberately does not update \`package.json\`; run it directly with:

\`\`\`sh
node analysis/ri-refractive-index-chain-runner.mjs
\`\`\`

## Status

| Field | Value |
|---|---|
| Started | ${startedAt} |
| Finished | ${finishedAt} |
| Status | ${report.status} |

## Steps

${table(
  ['#', 'Script', 'Stage', 'Role', 'Exit'],
  results.map((row) => [row.index, row.script, row.stage, row.role, row.exitCode])
)}
`;

await writeFile(new URL('ri-refractive-index-chain-runner.json', outDir), JSON.stringify(report, null, 2));
await writeFile(new URL('ri-refractive-index-chain-runner.md', outDir), markdown);

console.log(markdown);

if (failed.length > 0) {
  process.exitCode = 1;
}

function runStep(step) {
  return new Promise((resolve) => {
    const startedAtMs = Date.now();
    const child = spawn(process.execPath, [new URL(step.script, import.meta.url).pathname], {
      stdio: 'ignore',
      shell: false,
    });

    child.on('error', (error) => {
      resolve({
        exitCode: 1,
        durationMs: Date.now() - startedAtMs,
        error: error.message,
      });
    });

    child.on('close', (exitCode) => {
      resolve({
        exitCode,
        durationMs: Date.now() - startedAtMs,
      });
    });
  });
}
