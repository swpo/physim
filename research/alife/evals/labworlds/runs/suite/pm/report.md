# phase_membrane: PhySim-style suite, controls vs independent_native

13 cases, 8 forecast members per control, 2 truth members per case; score_case joint energy, equal-group mean over 12 groups. Ratio = control / independent_native (case means); 90% case-bootstrap interval; 'sep' = interval above 1 and above the numerical null's; the null row says whether its interval overlaps 0.9-1.1.

| control | aggregate | ratio | 90% interval | cases worse | sep |
|---|---|---|---|---|---|
| independent_native | 0.193 | 1.00 | 1.00-1.00 | 0/13 | ref |
| ignore_actions | 0.4448 | 2.30 | 1.93-2.69 | 11/13 | yes |
| wrong_probe_geometry | 0.3552 | 1.84 | 1.68-2.02 | 13/13 | yes |
| initial_persistence | 1.393 | 7.21 | 6.42-8.22 | 13/13 | yes |
| ablate_chi0 | 1.458 | 7.55 | 6.83-8.52 | 13/13 | yes |
| ablate_gate0 | 2.847 | 14.75 | 13.16-16.82 | 13/13 | yes |
| ablate_a2 | 1.453 | 7.53 | 6.72-8.57 | 13/13 | yes |
| numerical_null | 0.1682 | 0.87 | 0.77-0.97 | 4/13 | like ref |

Per group: ratio to independent_native (reference score in the first row).

| control | device0/S | device0/K | device0/L | device0/phi | device1/S | device1/K | device1/L | device1/phi | global/S | global/K | global/L | global/phi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| independent_native (score) | 0.111 | 0.105 | 0.129 | 0.11 | 0.312 | 0.304 | 0.318 | 0.286 | 0.162 | 0.154 | 0.153 | 0.173 |
| ignore_actions | 2.33 | 4.47 | 3.42 | 3.20 | 2.34 | 2.16 | 1.98 | 2.27 | 1.58 | 2.02 | 1.97 | 1.62 |
| wrong_probe_geometry | 2.25 | 3.38 | 3.68 | 3.19 | 1.37 | 1.83 | 2.26 | 1.66 | 1.01 | 1.04 | 1.03 | 1.03 |
| initial_persistence | 12.26 | 13.18 | 9.85 | 12.44 | 4.98 | 4.55 | 4.16 | 5.66 | 7.00 | 10.44 | 7.21 | 9.30 |
| ablate_chi0 | 9.15 | 9.00 | 8.99 | 7.54 | 4.65 | 3.58 | 3.61 | 3.54 | 13.12 | 13.05 | 13.56 | 15.33 |
| ablate_gate0 | 13.45 | 10.96 | 7.09 | 11.81 | 5.30 | 3.55 | 3.41 | 3.73 | 30.72 | 44.51 | 49.13 | 29.54 |
| ablate_a2 | 12.16 | 11.53 | 7.77 | 12.50 | 5.03 | 4.34 | 3.45 | 5.82 | 11.80 | 10.68 | 9.96 | 10.29 |
| numerical_null | 0.92 | 0.92 | 0.94 | 0.95 | 0.76 | 0.78 | 0.82 | 0.79 | 1.00 | 0.99 | 1.02 | 0.95 |

Per case: aggregate ratio to independent_native.

| case | program | ignore_actions | wrong_probe_geometry | initial_persistence | ablate_chi0 | ablate_gate0 | ablate_a2 | numerical_null |
|---|---|---|---|---|---|---|---|---|
| c001 | sham | 0.86 | 2.32 | 8.01 | 9.39 | 18.23 | 8.84 | 0.99 |
| c002 | pulse_d0_S | 1.84 | 1.42 | 6.41 | 6.57 | 13.05 | 6.60 | 0.81 |
| c003 | pulse_d0_K | 2.32 | 1.69 | 7.56 | 7.19 | 15.51 | 7.82 | 1.15 |
| c004 | pulse_d0_L | 3.22 | 1.81 | 9.98 | 9.32 | 18.99 | 9.66 | 0.93 |
| c005 | pulse_d0_phi | 2.45 | 2.34 | 11.74 | 13.13 | 25.47 | 12.62 | 0.97 |
| c006 | pulse_d1_S | 2.53 | 2.15 | 6.97 | 7.54 | 13.80 | 7.51 | 0.54 |
| c007 | pulse_d1_K | 2.16 | 1.44 | 5.87 | 6.42 | 11.38 | 6.26 | 0.56 |
| c008 | pulse_d1_L | 3.34 | 2.19 | 8.42 | 8.45 | 15.76 | 8.70 | 1.08 |
| c009 | pulse_d1_phi | 2.01 | 1.69 | 4.52 | 5.29 | 9.71 | 4.85 | 1.02 |
| c010 | probe_shift | 0.93 | 2.05 | 6.12 | 6.90 | 13.83 | 6.75 | 0.87 |
| c011 | probe_wide | 1.97 | 1.83 | 5.72 | 6.06 | 12.39 | 5.55 | 0.93 |
| c012 | move_during_pulse | 3.64 | 2.77 | 13.12 | 12.87 | 27.37 | 13.56 | 1.21 |
| c013 | two_sources | 3.85 | 1.19 | 7.31 | 6.76 | 12.87 | 7.41 | 0.56 |

Simulation CPU recorded in cached ensembles: 1.46 h.
