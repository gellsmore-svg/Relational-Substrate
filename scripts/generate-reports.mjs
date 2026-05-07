import { mkdir } from 'node:fs/promises';
import { spawn } from 'node:child_process';

const reportSteps = [
  'molecule:coordinates',
  'molecule:calibration',
  't1:coupling',
  't1:sweep',
  't1:stability',
  't1:refine',
  'molecule:peroxide-refine',
  'molecule:peroxide-torsion',
  'molecule:ethane-torsion',
  'molecule:ionic-lattice',
  'material:silicate-network',
  'material:mixed-modifier',
  'material:nbo-stoichiometry',
  'interface:boundary-transition',
  'interface:phase-continuity',
  'interface:roughness-scatter',
  'model:assumptions',
  'model:frontier',
  'model:external-roadmap',
  'benchmark:h2o2',
  'benchmark:h2o2-quant',
  'benchmark:ethane',
  'benchmark:ethane-quant',
  'benchmark:h2o2-absolute',
  'benchmark:ionic',
  'benchmark:boundary-blind',
  'benchmark:em-ordering',
  'benchmark:em-coulomb',
  'benchmark:em-superposition',
  'benchmark:em-three-source',
  'benchmark:em-field-lines',
  'benchmark:silicate-heldout',
  'benchmark:roughness-heldout',
  'benchmark:material-nbo',
  'benchmark:summary',
  'milestone:external-review',
];

await mkdir(new URL('../analysis/out/', import.meta.url), { recursive: true });

for (const step of reportSteps) {
  await run('npm', ['run', step]);
}

function run(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: 'inherit', shell: false });
    child.on('error', reject);
    child.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${command} ${args.join(' ')} exited with ${code}`));
      }
    });
  });
}
