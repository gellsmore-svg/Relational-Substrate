# Fixed-proposal results

C: conservation; G: no growth; R: irreversible readiness.
Intervals are trial-level marginal 95% Wilson intervals. Cells use paired tapes.
Readability and correctness are terminal measurements, not convergence proofs.

## constraint-ablation-v1

100 seeds per cell; 2000 proposals per trial.

| Cell | Correct | 95% interval | Readable | Identity preserved | Mean escapes |
| --- | --- | --- | --- | --- | --- |
| none | 0/100 | 0.000-0.037 | 0.010 | 0/100 | 0.00 |
| C | 0/100 | 0.000-0.037 | 0.000 | 100/100 | 0.00 |
| G | 0/100 | 0.000-0.037 | 1.000 | 0/100 | 0.00 |
| R | 0/100 | 0.000-0.037 | 0.010 | 0/100 | 0.00 |
| CG | 1/100 | 0.002-0.054 | 0.010 | 100/100 | 1.62 |
| CR | 0/100 | 0.000-0.037 | 0.000 | 100/100 | 0.00 |
| GR | 0/100 | 0.000-0.037 | 1.000 | 0/100 | 0.00 |
| CGR | 100/100 | 0.963-1.000 | 1.000 | 100/100 | 0.00 |

Verified identical proposal hashes across cells for all 100 paired seeds.
Paired discordances against full global constraints with matching inputs are retained in `statistics.json`.

## constraint-followups-v1

100 seeds per cell; 2000 proposals per trial.

| Cell | Correct | 95% interval | Readable | Identity preserved | Mean escapes |
| --- | --- | --- | --- | --- | --- |
| s0.9 | 0/100 | 0.000-0.037 | 1.000 | 0/100 | 0.06 |
| s0.99 | 0/100 | 0.000-0.037 | 0.990 | 0/100 | 0.60 |
| s0.999 | 48/100 | 0.385-0.577 | 0.990 | 48/100 | 0.45 |
| s0.9999 | 95/100 | 0.888-0.978 | 1.000 | 95/100 | 0.04 |
| s1 | 100/100 | 0.963-1.000 | 1.000 | 100/100 | 0.00 |
| zero-global | 100/100 | 0.963-1.000 | 1.000 | 100/100 | 0.00 |
| negative-global | 100/100 | 0.963-1.000 | 1.000 | 100/100 | 0.00 |
| 45-global | 87/100 | 0.790-0.922 | 0.870 | 100/100 | 0.00 |
| 100-global | 0/100 | 0.000-0.037 | 0.000 | 100/100 | 0.00 |
| zero-local | 100/100 | 0.963-1.000 | 1.000 | 100/100 | 0.00 |
| negative-local | 98/100 | 0.930-0.994 | 0.980 | 100/100 | 0.00 |
| 45-local | 19/100 | 0.125-0.278 | 0.190 | 100/100 | 0.00 |
| 100-local | 0/100 | 0.000-0.037 | 0.000 | 100/100 | 0.00 |

Verified identical proposal hashes across cells for all 100 paired seeds.
Paired discordances against full global constraints with matching inputs are retained in `statistics.json`.
