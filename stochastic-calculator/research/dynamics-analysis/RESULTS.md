# Passive-readout and recurrence results

Pure: single-polarity cardinality. Ready: pure plus all records ready.
Terminal counts use seed-level Wilson intervals; occupancy intervals use 1,000 seed-level bootstrap resamples.
Checkpoints and observers share trajectories and are not independent replications.

## SC-026: observer-controls-v1

350 trajectories, 3 checkpoint(s) each; burn-in 0.
All cell/seed/checkpoint combinations and paired tape hashes verified.

| Cell | Horizon | Pure correct | Ready correct | Pure occupancy | Ready occupancy | Mean population | Cap rejects |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-cap32 | 500 | 0/50 | 0/50 | 0.0000 | 0.0000 | 27.15 | 1273 |
| C-cap32 | 2000 | 0/50 | 0/50 | 0.0000 | 0.0000 | 28.68 | 6235 |
| C-cap32 | 8000 | 0/50 | 0/50 | 0.0000 | 0.0000 | 29.13 | 26149 |
| C-cap128 | 500 | 0/50 | 0/50 | 0.0000 | 0.0000 | 48.43 | 0 |
| C-cap128 | 2000 | 0/50 | 0/50 | 0.0000 | 0.0000 | 100.78 | 3590 |
| C-cap128 | 8000 | 0/50 | 0/50 | 0.0000 | 0.0000 | 118.96 | 22488 |
| C-cap512 | 500 | 0/50 | 0/50 | 0.0000 | 0.0000 | 48.43 | 0 |
| C-cap512 | 2000 | 0/50 | 0/50 | 0.0000 | 0.0000 | 143.15 | 0 |
| C-cap512 | 8000 | 0/50 | 0/50 | 0.0000 | 0.0000 | 387.79 | 12982 |
| CG | 500 | 50/50 | 0/50 | 0.8349 | 0.0086 | 7.60 | 0 |
| CG | 2000 | 50/50 | 1/50 | 0.9587 | 0.0071 | 7.15 | 0 |
| CG | 8000 | 50/50 | 1/50 | 0.9897 | 0.0079 | 7.04 | 0 |
| CGR | 500 | 50/50 | 50/50 | 0.8349 | 0.6549 | 7.60 | 0 |
| CGR | 2000 | 50/50 | 50/50 | 0.9587 | 0.9137 | 7.15 | 0 |
| CGR | 8000 | 50/50 | 50/50 | 0.9897 | 0.9784 | 7.04 | 0 |
| CGR-45 | 500 | 41/50 | 0/50 | 0.4331 | 0.0000 | 46.91 | 0 |
| CGR-45 | 2000 | 50/50 | 44/50 | 0.8334 | 0.2400 | 45.53 | 0 |
| CGR-45 | 8000 | 50/50 | 50/50 | 0.9584 | 0.8015 | 45.13 | 0 |
| CGR-100 | 500 | 22/50 | 0/50 | 0.1643 | 0.0000 | 103.37 | 0 |
| CGR-100 | 2000 | 50/50 | 0/50 | 0.6587 | 0.0000 | 101.16 | 0 |
| CGR-100 | 8000 | 50/50 | 50/50 | 0.9147 | 0.4738 | 100.29 | 0 |

Complete intervals, recurrence counts and paired readout disagreements are in `statistics.json`.

## SC-027: recurrent-resolution-v1

350 trajectories, 1 checkpoint(s) each; burn-in 4000.
All cell/seed/checkpoint combinations and paired tape hashes verified.

| Cell | Horizon | Pure correct | Ready correct | Pure occupancy | Ready occupancy | Mean population | Cap rejects |
| --- | --- | --- | --- | --- | --- | --- | --- |
| b0-cap32 | 8000 | 50/50 | 0/50 | 1.0000 | 0.0099 | 7.00 | 0 |
| b0.01-cap32 | 8000 | 44/50 | 0/50 | 0.9543 | 0.0094 | 7.09 | 0 |
| b0.05-cap32 | 8000 | 35/50 | 0/50 | 0.7757 | 0.0074 | 7.52 | 0 |
| b0.2-cap32 | 8000 | 16/50 | 0/50 | 0.2914 | 0.0020 | 10.01 | 0 |
| b0.5-cap32 | 8000 | 1/50 | 0/50 | 0.0095 | 0.0001 | 22.26 | 1553 |
| b0.05-cap128 | 8000 | 35/50 | 0/50 | 0.7757 | 0.0074 | 7.52 | 0 |
| b0.2-cap128 | 8000 | 16/50 | 0/50 | 0.2914 | 0.0020 | 10.01 | 0 |

Complete intervals, recurrence counts and paired readout disagreements are in `statistics.json`.

| Cell | Predicted stationary pure occupancy | Measured occupancy (95% seed bootstrap) | Escapes | Complete returns |
| --- | --- | --- | --- | --- |
| b0-cap32 | 1.00000 | 1.00000 (1.00000-1.00000) | 0 | 0 |
| b0.01-cap32 | 0.95023 | 0.95434 (0.94636-0.96184) | 233 | 227 |
| b0.05-cap32 | 0.76774 | 0.77569 (0.76042-0.79067) | 943 | 928 |
| b0.2-cap32 | 0.29024 | 0.29141 (0.27231-0.31067) | 1429 | 1395 |
| b0.5-cap32 | 0.00770 | 0.00948 (0.00686-0.01254) | 123 | 86 |
| b0.05-cap128 | 0.76774 | 0.77569 (0.76042-0.79067) | 943 | 928 |
| b0.2-cap128 | 0.29022 | 0.29141 (0.27231-0.31067) | 1429 | 1395 |

The comparator was specified before collection. Burn-in alone does not establish equilibrium; intervals are marginal, not simultaneous.

## SC-027R: recurrent-replication-v1

200 trajectories, 1 checkpoint(s) each; burn-in 4000.
All cell/seed/checkpoint combinations and paired tape hashes verified.

| Cell | Horizon | Pure correct | Ready correct | Pure occupancy | Ready occupancy | Mean population | Cap rejects |
| --- | --- | --- | --- | --- | --- | --- | --- |
| b0.01-cap32 | 8000 | 48/50 | 0/50 | 0.9492 | 0.0080 | 7.11 | 0 |
| b0.05-cap32 | 8000 | 42/50 | 0/50 | 0.7704 | 0.0059 | 7.54 | 0 |
| b0.2-cap32 | 8000 | 14/50 | 0/50 | 0.2922 | 0.0021 | 10.11 | 1 |
| b0.5-cap32 | 8000 | 0/50 | 0/50 | 0.0093 | 0.0001 | 22.65 | 1652 |

Complete intervals, recurrence counts and paired readout disagreements are in `statistics.json`.

| Cell | Predicted stationary pure occupancy | Measured occupancy (95% seed bootstrap) | Escapes | Complete returns |
| --- | --- | --- | --- | --- |
| b0.01-cap32 | 0.95023 | 0.94925 (0.94167-0.95630) | 231 | 229 |
| b0.05-cap32 | 0.76774 | 0.77043 (0.75460-0.78509) | 947 | 939 |
| b0.2-cap32 | 0.29024 | 0.29223 (0.27547-0.31019) | 1465 | 1429 |
| b0.5-cap32 | 0.00770 | 0.00930 (0.00584-0.01343) | 103 | 70 |

The comparator was specified before collection. Burn-in alone does not establish equilibrium; intervals are marginal, not simultaneous.
