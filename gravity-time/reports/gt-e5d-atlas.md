# GT-E5D atlas: durable renewal against the anchor-local traffic comparator NL

*Frozen plan `c74d896` (plan_hash `6a83dbb788ac…`); payload `228b7bb9d313…`; consulted hub `38c2501`. Exact finite-generator values; ties relative 1e-9.*

## Item status

| Item | Status | Wall s | Problems |
| --- | --- | ---: | --- |
| FREE-N5-CLOSEW-weak_favour | complete | 0.44 | none |
| FREE-N5-CSPH-strong_favour+weak_favour | complete | 0.38 | none |
| FREE-N5-NULL-none | complete | 0.33 | none |
| FREE-N5-PATHF-weak_suppress | complete | 0.26 | none |
| FREE-N5-PATHH-weak_favour | complete | 0.28 | none |
| FREE-N5-PCOMP-weak_favour+weak_favour | complete | 0.33 | none |
| FREE-N6-CLOSEW-weak_favour | complete | 1.9e+02 | none |
| FREE-N6-CSPH-strong_favour+weak_favour | complete | 2.1e+02 | none |
| FREE-N6-NULL-none | complete | 2.1e+02 | none |
| FREE-N6-PATHF-weak_suppress | complete | 2e+02 | none |
| FREE-N6-PATHH-weak_favour | complete | 2.1e+02 | none |
| FREE-N6-PCOMP-weak_favour+weak_favour | complete | 1.9e+02 | none |

## Frozen checks

- `FREE-N5-CLOSEW-weak_favour`: pass
- `FREE-N5-CSPH-strong_favour+weak_favour`: pass
- `FREE-N5-NULL-none`: pass
- `FREE-N5-PATHF-weak_suppress`: pass
- `FREE-N5-PATHH-weak_favour`: pass
- `FREE-N5-PCOMP-weak_favour+weak_favour`: pass
- `FREE-N6-CLOSEW-weak_favour`: pass
- `FREE-N6-CSPH-strong_favour+weak_favour`: pass
- `FREE-N6-NULL-none`: pass
- `FREE-N6-PATHF-weak_suppress`: pass
- `FREE-N6-PATHH-weak_favour`: pass
- `FREE-N6-PCOMP-weak_favour+weak_favour`: pass
- `NULL_fixed_point`: {'5': 'pass', '6': 'pass'}

## FREE-N5-CLOSEW-weak_favour:F_TRI

Status computed; target macro net current (max relative) 1.810e-14; NL reversible: True; within-cell local-rate CV max 0.2229.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.2477 | 0.1331 | 0.2333 | 0.2448 | 0.2447 | higher ×1.012 | higher ×1.012 |
| U1 | 0.09142 | 0.05914 | 0.1016 | 0.09462 | 0.09433 | lower ×0.9662 | lower ×0.9692 |
| U2 | 0.04546 | 0.0313 | 0.05391 | 0.04817 | 0.04794 | lower ×0.9437 | lower ×0.9483 |
| U4 | 0.01261 | 0.009164 | 0.01621 | 0.01312 | 0.013 | lower ×0.9617 | lower ×0.9706 |
| U8 | 0.001204 | 8.369e-04 | 0.001593 | 0.001093 | 0.001074 | higher ×1.102 | higher ×1.121 |
| C1 | 0.3691 | 0.4442 | 0.4353 | 0.3865 | 0.3854 | lower ×0.955 | lower ×0.9577 |
| C2 | 0.1835 | 0.2351 | 0.2311 | 0.1968 | 0.1959 | lower ×0.9327 | lower ×0.937 |
| C4 | 0.05093 | 0.06883 | 0.06947 | 0.05358 | 0.0531 | lower ×0.9505 | lower ×0.9591 |
| C8 | 0.004862 | 0.006286 | 0.006829 | 0.004464 | 0.004389 | higher ×1.089 | higher ×1.108 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.4968 | computed | 0.4285 / 0.4404 / 0.4393 | 0.06404 / 0.06516 / 0.06462 | 0.6699 / 0.654 / 0.6566 |
| 2 | 0.2701 | computed | 0.1744 / 0.1907 / 0.1902 | 0.007946 / 0.0115 / 0.01139 | 0.7142 / 0.679 / 0.6797 |
| 3 | 0.2331 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N5-CSPH-strong_favour+weak_favour:F_TRI

Status computed; target macro net current (max relative) 0.4318; NL reversible: False; within-cell local-rate CV max 0.3559.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.1508 | 0.1331 | 0.02868 | 0.06748 | 0.07663 | higher ×2.235 | higher ×1.968 |
| U1 | 0.05125 | 0.05914 | 0.01018 | 0.02737 | 0.03208 | higher ×1.872 | higher ×1.597 |
| U2 | 0.02869 | 0.0313 | 0.004199 | 0.01346 | 0.0159 | higher ×2.131 | higher ×1.804 |
| U4 | 0.008631 | 0.009164 | 7.421e-04 | 0.003389 | 0.004243 | higher ×2.547 | higher ×2.034 |
| U8 | 0.001115 | 8.369e-04 | 2.485e-05 | 2.309e-04 | 3.283e-04 | higher ×4.83 | higher ×3.397 |
| C1 | 0.3398 | 0.4442 | 0.355 | 0.4056 | 0.4187 | lower ×0.8377 | lower ×0.8115 |
| C2 | 0.1902 | 0.2351 | 0.1464 | 0.1994 | 0.2075 | lower ×0.9535 | lower ×0.9166 |
| C4 | 0.05721 | 0.06883 | 0.02587 | 0.05021 | 0.05537 | higher ×1.139 | higher ×1.033 |
| C8 | 0.007394 | 0.006286 | 8.665e-04 | 0.003422 | 0.004285 | higher ×2.161 | higher ×1.726 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.9201 | computed | 0.3402 / 0.4067 / 0.4198 | 0.05774 / 0.05076 / 0.05601 | 0.31 / 0.1335 / 0.1481 |
| 2 | 0.0796 | computed | 0.3075 / 0.3526 / 0.3663 | 0.02315 / 0.02428 / 0.02669 | 0.3534 / 0.2118 / 0.2176 |
| 3 | 2.969e-04 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N5-PATHF-weak_suppress:F_TRI

Status computed; target macro net current (max relative) 0.4776; NL reversible: False; within-cell local-rate CV max 0.1995.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.007738 | 0.1331 | 0.01465 | 0.01465 | 0.01578 | lower ×0.5281 | lower ×0.4902 |
| U1 | 0.00246 | 0.05914 | 0.004729 | 0.004729 | 0.00514 | lower ×0.5202 | lower ×0.4786 |
| U2 | 6.919e-04 | 0.0313 | 0.001706 | 0.001706 | 0.001895 | lower ×0.4057 | lower ×0.3651 |
| U4 | 6.663e-05 | 0.009164 | 2.308e-04 | 2.308e-04 | 2.660e-04 | lower ×0.2887 | lower ×0.2505 |
| U8 | 6.382e-07 | 8.369e-04 | 4.478e-06 | 4.478e-06 | 5.569e-06 | lower ×0.1425 | lower ×0.1146 |
| C1 | 0.3179 | 0.4442 | 0.3227 | 0.3227 | 0.3256 | lower ×0.9851 | lower ×0.9763 |
| C2 | 0.08942 | 0.2351 | 0.1164 | 0.1164 | 0.12 | lower ×0.7682 | lower ×0.7448 |
| C4 | 0.00861 | 0.06883 | 0.01575 | 0.01575 | 0.01685 | lower ×0.5466 | lower ×0.511 |
| C8 | 8.247e-05 | 0.006286 | 3.056e-04 | 3.056e-04 | 3.528e-04 | lower ×0.2699 | lower ×0.2337 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.9892 | computed | 0.3178 / 0.3227 / 0.3256 | 0.008611 / 0.01576 / 0.01686 | 0.02574 / 0.04786 / 0.05016 |
| 2 | 0.01074 | computed | 0.3526 / 0.3466 / 0.3481 | 0.008423 / 0.01295 / 0.01367 | 0.03672 / 0.06038 / 0.06356 |
| 3 | 3.574e-05 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N5-PATHH-weak_favour:F_TRI

Status computed; target macro net current (max relative) 0.6093; NL reversible: False; within-cell local-rate CV max 0.2817.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.03598 | 0.1331 | 0.01155 | 0.02647 | 0.0287 | higher ×1.359 | higher ×1.254 |
| U1 | 0.01561 | 0.05914 | 0.003603 | 0.009325 | 0.01025 | higher ×1.674 | higher ×1.523 |
| U2 | 0.007772 | 0.0313 | 0.001241 | 0.003893 | 0.004323 | higher ×1.996 | higher ×1.798 |
| U4 | 0.001974 | 0.009164 | 1.527e-04 | 6.905e-04 | 7.922e-04 | higher ×2.859 | higher ×2.492 |
| U8 | 1.322e-04 | 8.369e-04 | 2.430e-06 | 2.327e-05 | 2.854e-05 | higher ×5.681 | higher ×4.632 |
| C1 | 0.4339 | 0.4442 | 0.312 | 0.3523 | 0.3573 | higher ×1.231 | higher ×1.215 |
| C2 | 0.216 | 0.2351 | 0.1074 | 0.1471 | 0.1507 | higher ×1.469 | higher ×1.434 |
| C4 | 0.05486 | 0.06883 | 0.01322 | 0.02609 | 0.02761 | higher ×2.103 | higher ×1.987 |
| C8 | 0.003674 | 0.006286 | 2.105e-04 | 8.791e-04 | 9.946e-04 | higher ×4.179 | higher ×3.694 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.9913 | computed | 0.434 / 0.3523 / 0.3572 | 0.0549 / 0.02613 / 0.02765 | 0.07328 / 0.07168 / 0.0767 |
| 2 | 0.008672 | computed | 0.4002 / 0.3579 / 0.3608 | 0.04033 / 0.01839 / 0.01935 | 0.09949 / 0.1004 / 0.101 |
| 3 | 2.107e-05 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N5-PCOMP-weak_favour+weak_favour:F_TRI

Status computed; target macro net current (max relative) 6.602e-14; NL reversible: True; within-cell local-rate CV max 0.4479.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.2746 | 0.1331 | 0.1331 | 0.2682 | 0.2693 | higher ×1.024 | higher ×1.019 |
| U1 | 0.1061 | 0.05914 | 0.05914 | 0.106 | 0.1075 | higher ×1.001 | lower ×0.987 |
| U2 | 0.06017 | 0.0313 | 0.0313 | 0.05583 | 0.05678 | higher ×1.078 | higher ×1.06 |
| U4 | 0.01972 | 0.009164 | 0.009164 | 0.01619 | 0.0166 | higher ×1.218 | higher ×1.188 |
| U8 | 0.002393 | 8.369e-04 | 8.369e-04 | 0.001536 | 0.001598 | higher ×1.558 | higher ×1.497 |
| C1 | 0.3864 | 0.4442 | 0.4442 | 0.3954 | 0.3991 | lower ×0.9772 | lower ×0.9683 |
| C2 | 0.2191 | 0.2351 | 0.2351 | 0.2082 | 0.2108 | higher ×1.053 | higher ×1.039 |
| C4 | 0.07182 | 0.06883 | 0.06883 | 0.06036 | 0.06164 | higher ×1.19 | higher ×1.165 |
| C8 | 0.008716 | 0.006286 | 0.006286 | 0.005729 | 0.005933 | higher ×1.521 | higher ×1.469 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.4776 | computed | 0.465 / 0.4668 / 0.4692 | 0.09097 / 0.07689 / 0.07813 | 0.6805 / 0.6614 / 0.6529 |
| 2 | 0.3448 | computed | 0.1917 / 0.1812 / 0.1837 | 0.02437 / 0.01072 / 0.01095 | 0.7281 / 0.7138 / 0.7081 |
| 3 | 0.1776 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N6-CLOSEW-weak_favour:F_2PATH

Status computed; target macro net current (max relative) 9.285e-14; NL reversible: True; within-cell local-rate CV max 0.3651.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.6407 | 0.194 | 0.523 | 0.6615 | 0.6438 | lower ×0.9685 | lower ×0.9951 |
| U1 | 0.1427 | 0.0569 | 0.1435 | 0.1508 | 0.1458 | lower ×0.9462 | lower ×0.9785 |
| U2 | 0.03678 | 0.02328 | 0.04074 | 0.03888 | 0.03651 | lower ×0.9459 | higher ×1.008 |
| U4 | 0.002393 | 0.002793 | 0.003286 | 0.00244 | 0.002148 | lower ×0.9807 | higher ×1.114 |
| U8 | 1.322e-05 | 4.022e-05 | 2.260e-05 | 1.072e-05 | 8.053e-06 | higher ×1.233 | higher ×1.642 |
| C1 | 0.2227 | 0.2933 | 0.2744 | 0.228 | 0.2265 | lower ×0.977 | lower ×0.9833 |
| C2 | 0.05741 | 0.12 | 0.07788 | 0.05878 | 0.0567 | lower ×0.9767 | higher ×1.012 |
| C4 | 0.003734 | 0.0144 | 0.006282 | 0.003688 | 0.003336 | higher ×1.013 | higher ×1.119 |
| C8 | 2.063e-05 | 2.074e-04 | 4.321e-05 | 1.621e-05 | 1.251e-05 | higher ×1.273 | higher ×1.65 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 2 | 1 | computed | 0.2227 / 0.228 / 0.2265 | 0.003734 / 0.003688 / 0.003336 | 0.913 / 0.923 / 0.9129 |

## FREE-N6-CLOSEW-weak_favour:F_TRI

Status computed; target macro net current (max relative) 9.352e-14; NL reversible: True; within-cell local-rate CV max 0.281.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.1169 | 0.1844 | 0.2182 | 0.1291 | 0.1275 | lower ×0.9057 | lower ×0.9169 |
| U1 | 0.04318 | 0.1064 | 0.1064 | 0.05159 | 0.05084 | lower ×0.837 | lower ×0.8495 |
| U2 | 0.02264 | 0.06733 | 0.06289 | 0.02812 | 0.02766 | lower ×0.8052 | lower ×0.8187 |
| U4 | 0.007148 | 0.02914 | 0.02429 | 0.009088 | 0.008866 | lower ×0.7865 | lower ×0.8062 |
| U8 | 0.001057 | 0.006122 | 0.004459 | 0.001247 | 0.001194 | lower ×0.847 | lower ×0.8849 |
| C1 | 0.3695 | 0.5771 | 0.4878 | 0.3998 | 0.3988 | lower ×0.9242 | lower ×0.9264 |
| C2 | 0.1937 | 0.3651 | 0.2882 | 0.2179 | 0.217 | lower ×0.8891 | lower ×0.8928 |
| C4 | 0.06116 | 0.158 | 0.1113 | 0.07042 | 0.06956 | lower ×0.8685 | lower ×0.8792 |
| C8 | 0.009039 | 0.0332 | 0.02043 | 0.009666 | 0.009367 | lower ×0.9352 | lower ×0.965 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.1114 | computed | 0.4941 / 0.5147 / 0.5095 | 0.1061 / 0.1144 / 0.1116 | 0.8356 / 0.8202 / 0.8232 |
| 2 | 0.1265 | computed | 0.3153 / 0.3417 / 0.3413 | 0.0288 / 0.03436 / 0.03418 | 0.867 / 0.8467 / 0.8452 |
| 3 | 0.3108 | computed | 0.173 / 0.1921 / 0.1938 | 0.00747 / 0.01015 / 0.01039 | 0.8337 / 0.8103 / 0.8058 |
| 4 | 0.4513 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N6-CSPH-strong_favour+weak_favour:F_2PATH

Status computed; target macro net current (max relative) 0.9388; NL reversible: False; within-cell local-rate CV max 0.7799.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.06011 | 0.194 | 0.03725 | 0.06633 | 0.07173 | lower ×0.9063 | lower ×0.8379 |
| U1 | 0.01201 | 0.0569 | 0.006446 | 0.01419 | 0.0157 | lower ×0.8463 | lower ×0.7648 |
| U2 | 0.006661 | 0.02328 | 0.003857 | 0.00786 | 0.00911 | lower ×0.8475 | lower ×0.7311 |
| U4 | 0.001216 | 0.002793 | 3.970e-04 | 9.262e-04 | 0.001149 | higher ×1.313 | higher ×1.059 |
| U8 | 6.237e-05 | 4.022e-05 | 4.190e-06 | 1.281e-05 | 1.815e-05 | higher ×4.867 | higher ×3.435 |
| C1 | 0.1998 | 0.2933 | 0.173 | 0.2139 | 0.2189 | lower ×0.9339 | lower ×0.9127 |
| C2 | 0.1108 | 0.12 | 0.1035 | 0.1185 | 0.127 | lower ×0.9351 | lower ×0.8726 |
| C4 | 0.02024 | 0.0144 | 0.01066 | 0.01396 | 0.01602 | higher ×1.449 | higher ×1.263 |
| C8 | 0.001038 | 2.074e-04 | 1.125e-04 | 1.932e-04 | 2.531e-04 | higher ×5.37 | higher ×4.1 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 2 | 1 | computed | 0.1998 / 0.2139 / 0.2189 | 0.02024 / 0.01396 / 0.01602 | 0.4367 / 0.3907 / 0.4095 |

## FREE-N6-CSPH-strong_favour+weak_favour:F_TRI

Status computed; target macro net current (max relative) 0.8236; NL reversible: False; within-cell local-rate CV max 0.9031.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.1317 | 0.1844 | 0.02583 | 0.05027 | 0.06226 | higher ×2.62 | higher ×2.115 |
| U1 | 0.05309 | 0.1064 | 0.01076 | 0.02363 | 0.03062 | higher ×2.247 | higher ×1.734 |
| U2 | 0.03069 | 0.06733 | 0.004896 | 0.01231 | 0.01661 | higher ×2.494 | higher ×1.848 |
| U4 | 0.0108 | 0.02914 | 0.001079 | 0.003586 | 0.005295 | higher ×3.013 | higher ×2.041 |
| U8 | 0.001751 | 0.006122 | 5.808e-05 | 3.392e-04 | 6.031e-04 | higher ×5.161 | higher ×2.903 |
| C1 | 0.4031 | 0.5771 | 0.4166 | 0.4701 | 0.4919 | lower ×0.8576 | lower ×0.8196 |
| C2 | 0.233 | 0.3651 | 0.1895 | 0.2448 | 0.2667 | lower ×0.9518 | lower ×0.8737 |
| C4 | 0.08204 | 0.158 | 0.04178 | 0.07134 | 0.08504 | higher ×1.15 | lower ×0.9647 |
| C8 | 0.01329 | 0.0332 | 0.002248 | 0.006748 | 0.009687 | higher ×1.97 | higher ×1.372 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.9366 | computed | 0.4038 / 0.4705 / 0.4928 | 0.08266 / 0.07167 / 0.08566 | 0.2462 / 0.08716 / 0.1045 |
| 2 | 0.06302 | computed | 0.369 / 0.4477 / 0.4578 | 0.05195 / 0.05481 / 0.06205 | 0.2939 / 0.1406 / 0.1684 |
| 3 | 4.163e-04 | computed | 0.3247 / 0.4371 / 0.4446 | 0.02969 / 0.04145 / 0.04507 | 0.2998 / 0.1762 / 0.2008 |
| 4 | 3.773e-07 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N6-PATHF-weak_suppress:F_2PATH

Status computed; target macro net current (max relative) 0.9751; NL reversible: False; within-cell local-rate CV max 0.2758.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.04103 | 0.194 | 0.03107 | 0.03107 | 0.04086 | higher ×1.321 | higher ×1.004 |
| U1 | 0.008378 | 0.0569 | 0.005014 | 0.005014 | 0.008277 | higher ×1.671 | higher ×1.012 |
| U2 | 0.00405 | 0.02328 | 0.003093 | 0.003093 | 0.00399 | higher ×1.309 | higher ×1.015 |
| U4 | 4.150e-04 | 0.002793 | 3.058e-04 | 3.058e-04 | 3.836e-04 | higher ×1.357 | higher ×1.082 |
| U8 | 4.392e-06 | 4.022e-05 | 2.977e-06 | 2.977e-06 | 3.497e-06 | higher ×1.475 | higher ×1.256 |
| C1 | 0.2042 | 0.2933 | 0.1614 | 0.1614 | 0.2026 | higher ×1.265 | higher ×1.008 |
| C2 | 0.0987 | 0.12 | 0.09956 | 0.09956 | 0.09764 | lower ×0.9914 | higher ×1.011 |
| C4 | 0.01011 | 0.0144 | 0.009843 | 0.009843 | 0.009388 | higher ×1.028 | higher ×1.077 |
| C8 | 1.070e-04 | 2.074e-04 | 9.580e-05 | 9.580e-05 | 8.558e-05 | higher ×1.117 | higher ×1.251 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 2 | 1 | computed | 0.2042 / 0.1614 / 0.2026 | 0.01011 / 0.009843 / 0.009388 | 0.3317 / 0.281 / 0.3387 |

## FREE-N6-PATHF-weak_suppress:F_TRI

Status computed; target macro net current (max relative) 0.7913; NL reversible: False; within-cell local-rate CV max 0.2156.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.007906 | 0.1844 | 0.01951 | 0.01951 | 0.02129 | lower ×0.4053 | lower ×0.3714 |
| U1 | 0.002896 | 0.1064 | 0.007758 | 0.007758 | 0.008627 | lower ×0.3733 | lower ×0.3357 |
| U2 | 0.001008 | 0.06733 | 0.003372 | 0.003372 | 0.003845 | lower ×0.299 | lower ×0.2623 |
| U4 | 1.370e-04 | 0.02914 | 6.712e-04 | 6.712e-04 | 8.070e-04 | lower ×0.2042 | lower ×0.1698 |
| U8 | 2.649e-06 | 0.006122 | 2.922e-05 | 2.922e-05 | 3.937e-05 | lower ×0.09066 | lower ×0.0673 |
| C1 | 0.3663 | 0.5771 | 0.3977 | 0.3977 | 0.4052 | lower ×0.9211 | lower ×0.904 |
| C2 | 0.1275 | 0.3651 | 0.1729 | 0.1729 | 0.1806 | lower ×0.7378 | lower ×0.7063 |
| C4 | 0.01733 | 0.158 | 0.03441 | 0.03441 | 0.0379 | lower ×0.5037 | lower ×0.4573 |
| C8 | 3.351e-04 | 0.0332 | 0.001498 | 0.001498 | 0.001849 | lower ×0.2237 | lower ×0.1812 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.9883 | computed | 0.3661 / 0.3976 / 0.4051 | 0.01732 / 0.03443 / 0.03793 | 0.02195 / 0.04849 / 0.05205 |
| 2 | 0.01164 | computed | 0.4002 / 0.4067 / 0.4117 | 0.01916 / 0.03091 / 0.03387 | 0.03148 / 0.07122 / 0.07694 |
| 3 | 6.035e-05 | computed | 0.4191 / 0.4143 / 0.419 | 0.01989 / 0.02823 / 0.03061 | 0.03683 / 0.07968 / 0.08665 |
| 4 | 3.049e-08 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N6-PATHH-weak_favour:F_2PATH

Status computed; target macro net current (max relative) 0.949; NL reversible: False; within-cell local-rate CV max 0.654.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.03553 | 0.194 | 0.02711 | 0.04283 | 0.03665 | lower ×0.8295 | lower ×0.9692 |
| U1 | 0.006829 | 0.0569 | 0.004151 | 0.007829 | 0.0069 | lower ×0.8722 | lower ×0.9897 |
| U2 | 0.003674 | 0.02328 | 0.002614 | 0.004642 | 0.003706 | lower ×0.7916 | lower ×0.9914 |
| U4 | 3.761e-04 | 0.002793 | 2.505e-04 | 4.996e-04 | 3.690e-04 | lower ×0.7527 | higher ×1.019 |
| U8 | 3.926e-06 | 4.022e-05 | 2.289e-06 | 5.763e-06 | 3.612e-06 | lower ×0.6813 | higher ×1.087 |
| C1 | 0.1922 | 0.2933 | 0.1531 | 0.1828 | 0.1882 | higher ×1.051 | higher ×1.021 |
| C2 | 0.1034 | 0.12 | 0.09646 | 0.1084 | 0.1011 | lower ×0.9543 | higher ×1.023 |
| C4 | 0.01059 | 0.0144 | 0.009241 | 0.01167 | 0.01007 | lower ×0.9074 | higher ×1.052 |
| C8 | 1.105e-04 | 2.074e-04 | 8.445e-05 | 1.346e-04 | 9.853e-05 | lower ×0.8213 | higher ×1.122 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 2 | 1 | computed | 0.1922 / 0.1828 / 0.1882 | 0.01059 / 0.01167 / 0.01007 | 0.3254 / 0.3245 / 0.3177 |

## FREE-N6-PATHH-weak_favour:F_TRI

Status computed; target macro net current (max relative) 0.869; NL reversible: False; within-cell local-rate CV max 0.7973.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.03387 | 0.1844 | 0.01606 | 0.02912 | 0.03283 | higher ×1.163 | higher ×1.031 |
| U1 | 0.01605 | 0.1064 | 0.006161 | 0.01245 | 0.01444 | higher ×1.29 | higher ×1.111 |
| U2 | 0.008608 | 0.06733 | 0.002571 | 0.005879 | 0.007001 | higher ×1.464 | higher ×1.23 |
| U4 | 0.002604 | 0.02914 | 4.705e-04 | 0.001389 | 0.001753 | higher ×1.875 | higher ×1.485 |
| U8 | 2.536e-04 | 0.006122 | 1.724e-05 | 8.580e-05 | 1.220e-04 | higher ×2.956 | higher ×2.08 |
| C1 | 0.474 | 0.5771 | 0.3838 | 0.4274 | 0.4399 | higher ×1.109 | higher ×1.077 |
| C2 | 0.2542 | 0.3651 | 0.1601 | 0.2019 | 0.2132 | higher ×1.259 | higher ×1.192 |
| C4 | 0.07688 | 0.158 | 0.02931 | 0.0477 | 0.0534 | higher ×1.612 | higher ×1.44 |
| C8 | 0.007489 | 0.0332 | 0.001074 | 0.002946 | 0.003715 | higher ×2.542 | higher ×2.016 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.9913 | computed | 0.4741 / 0.4275 / 0.44 | 0.07694 / 0.04777 / 0.0535 | 0.05754 / 0.06223 / 0.0698 |
| 2 | 0.008634 | computed | 0.4428 / 0.4245 / 0.4294 | 0.06388 / 0.04035 / 0.04362 | 0.08013 / 0.09624 / 0.1076 |
| 3 | 3.117e-05 | computed | 0.3878 / 0.4289 / 0.4306 | 0.04978 / 0.03479 / 0.03695 | 0.08561 / 0.1133 / 0.1204 |
| 4 | 1.467e-08 | STRUCTURALLY_IMPOSSIBLE | — | — | — |

## FREE-N6-PCOMP-weak_favour+weak_favour:F_2PATH

Status computed; target macro net current (max relative) 3.570e-13; NL reversible: True; within-cell local-rate CV max 0.7039.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.7551 | 0.194 | 0.194 | 0.7589 | 0.7671 | lower ×0.9951 | lower ×0.9843 |
| U1 | 0.1713 | 0.0569 | 0.0569 | 0.1679 | 0.1771 | higher ×1.02 | lower ×0.9673 |
| U2 | 0.04568 | 0.02328 | 0.02328 | 0.04211 | 0.04547 | higher ×1.085 | higher ×1.005 |
| U4 | 0.003227 | 0.002793 | 0.002793 | 0.002378 | 0.002755 | higher ×1.357 | higher ×1.171 |
| U8 | 2.273e-05 | 4.022e-05 | 4.022e-05 | 7.799e-06 | 1.052e-05 | higher ×2.915 | higher ×2.161 |
| C1 | 0.2269 | 0.2933 | 0.2933 | 0.2212 | 0.2309 | higher ×1.026 | lower ×0.9827 |
| C2 | 0.0605 | 0.12 | 0.12 | 0.0555 | 0.05928 | higher ×1.09 | higher ×1.021 |
| C4 | 0.004273 | 0.0144 | 0.0144 | 0.003134 | 0.003591 | higher ×1.364 | higher ×1.19 |
| C8 | 3.011e-05 | 2.074e-04 | 2.074e-04 | 1.028e-05 | 1.371e-05 | higher ×2.929 | higher ×2.196 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 2 | 1 | computed | 0.2269 / 0.2212 / 0.2309 | 0.004273 / 0.003134 / 0.003591 | 0.9488 / 0.9465 / 0.9482 |

## FREE-N6-PCOMP-weak_favour+weak_favour:F_TRI

Status computed; target macro net current (max relative) 1.986e-13; NL reversible: True; within-cell local-rate CV max 0.6746.

| Quantity | target | N0 | ND | NK | NL | vs NK | vs NL |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R0 | 0.1388 | 0.1844 | 0.1844 | 0.1503 | 0.1573 | lower ×0.9237 | lower ×0.8826 |
| U1 | 0.05212 | 0.1064 | 0.1064 | 0.05933 | 0.06329 | lower ×0.8785 | lower ×0.8236 |
| U2 | 0.02844 | 0.06733 | 0.06733 | 0.03205 | 0.03443 | lower ×0.8876 | lower ×0.8262 |
| U4 | 0.009499 | 0.02914 | 0.02914 | 0.01042 | 0.01137 | lower ×0.9118 | lower ×0.8354 |
| U8 | 0.001426 | 0.006122 | 0.006122 | 0.001473 | 0.001647 | lower ×0.9682 | lower ×0.8659 |
| C1 | 0.3754 | 0.5771 | 0.5771 | 0.3947 | 0.4023 | lower ×0.9511 | lower ×0.9332 |
| C2 | 0.2049 | 0.3651 | 0.3651 | 0.2132 | 0.2189 | lower ×0.9609 | lower ×0.9361 |
| C4 | 0.06842 | 0.158 | 0.158 | 0.0693 | 0.07228 | lower ×0.9872 | lower ×0.9466 |
| C8 | 0.01027 | 0.0332 | 0.0332 | 0.009798 | 0.01047 | higher ×1.048 | lower ×0.9811 |

| Entry size | weight | status | C1 target/NK/NL | C4 target/NK/NL | return before exit target/NK/NL |
| --- | ---: | --- | --- | --- | --- |
| 1 | 0.09289 | computed | 0.5406 / 0.5552 / 0.5604 | 0.1348 / 0.1312 / 0.1346 | 0.8252 / 0.8278 / 0.821 |
| 2 | 0.2036 | computed | 0.3366 / 0.3453 / 0.35 | 0.04155 / 0.03251 / 0.03373 | 0.871 / 0.8658 / 0.8602 |
| 3 | 0.3961 | computed | 0.2047 / 0.1737 / 0.178 | 0.01903 / 0.007716 / 0.008136 | 0.8549 / 0.842 / 0.8362 |
| 4 | 0.3074 | STRUCTURALLY_IMPOSSIBLE | — | — | — |
