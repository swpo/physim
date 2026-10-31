# fed_vortices: PhySim-style suite, controls vs independent_native

10 cases, 8 forecast members per control, 2 truth members per case; score_case joint energy, equal-group mean over 6 groups. Ratio = control / independent_native (case means); 90% case-bootstrap interval; 'sep' = interval above 1 and above the numerical null's; the null row says whether its interval overlaps 0.9-1.1.

| control | aggregate | ratio | 90% interval | cases worse | sep |
|---|---|---|---|---|---|
| independent_native | 0.05836 | 1.00 | 1.00-1.00 | 0/10 | ref |
| ignore_actions | 0.3781 | 6.48 | 4.98-7.98 | 9/10 | yes |
| wrong_probe_geometry | 0.5772 | 9.89 | 8.68-11.37 | 10/10 | yes |
| initial_persistence | 0.9301 | 15.94 | 14.68-17.35 | 10/10 | yes |
| ablate_adv0 | 0.629 | 10.78 | 9.93-11.84 | 10/10 | yes |
| ablate_kF0 | 6.619 | 113.40 | 104.00-124.43 | 10/10 | yes |
| numerical_null | 0.05706 | 0.98 | 0.94-1.02 | 5/10 | like ref |

Per group: ratio to independent_native (reference score in the first row).

| control | device0/om | device0/Y | device1/om | device1/Y | global/om | global/Y |
|---|---|---|---|---|---|---|
| independent_native (score) | 0.0439 | 0.0474 | 0.0474 | 0.0191 | 0.0952 | 0.097 |
| ignore_actions | 6.96 | 9.24 | 5.43 | 11.40 | 6.72 | 4.22 |
| wrong_probe_geometry | 23.95 | 20.01 | 13.97 | 25.75 | 1.80 | 1.41 |
| initial_persistence | 19.73 | 21.13 | 17.01 | 39.69 | 8.39 | 13.88 |
| ablate_adv0 | 15.23 | 14.21 | 15.76 | 35.41 | 6.27 | 4.21 |
| ablate_kF0 | 11.63 | 13.81 | 9.41 | 31.52 | 175.36 | 214.33 |
| numerical_null | 0.98 | 0.99 | 0.98 | 0.99 | 0.99 | 0.96 |

Per case: aggregate ratio to independent_native.

| case | program | ignore_actions | wrong_probe_geometry | initial_persistence | ablate_adv0 | ablate_kF0 | numerical_null |
|---|---|---|---|---|---|---|---|
| c001 | sham | 0.99 | 10.70 | 16.19 | 12.10 | 128.54 | 1.09 |
| c002 | pulse_d0_om | 5.65 | 7.40 | 13.17 | 8.96 | 90.86 | 0.91 |
| c003 | pulse_d0_Y | 10.18 | 14.01 | 19.27 | 12.10 | 128.52 | 0.96 |
| c004 | pulse_d1_om | 4.53 | 7.98 | 13.33 | 9.34 | 104.41 | 1.04 |
| c005 | pulse_d1_Y | 5.42 | 7.91 | 12.70 | 8.83 | 89.25 | 0.85 |
| c006 | probe_shift | 2.62 | 11.32 | 17.91 | 12.64 | 138.41 | 1.04 |
| c007 | probe_wide | 7.43 | 9.70 | 15.54 | 10.51 | 107.34 | 1.01 |
| c008 | move_during_pulse | 7.62 | 9.48 | 17.95 | 11.47 | 125.08 | 0.92 |
| c009 | two_sources | 10.87 | 7.84 | 16.39 | 9.63 | 102.73 | 1.05 |
| c010 | feed_delayed | 9.66 | 16.59 | 20.88 | 15.27 | 151.93 | 0.96 |

Simulation CPU recorded in cached ensembles: 0.87 h.
