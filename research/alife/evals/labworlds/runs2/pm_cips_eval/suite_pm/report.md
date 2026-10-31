# phase_membrane_iso_noise: frozen suite, controls vs independent_native

14 cases; 4 members per control ensemble, 2 truths per case; PhySim score_case joint energy, equal-group mean over 12 groups. Ratio = control / independent_native (means over the cases the control ran on); 90% case-bootstrap interval. Band = band_native / independent_native, all cases: 0.81-1.23. 'sep' = interval above the band's upper bound.

| control | cases | ratio | 90% interval | cases worse | sep |
|---|---|---|---|---|---|
| ignore_actions | 14 | 3.63 | 2.93-4.43 | 13/14 | yes |
| wrong_probe_geometry | 14 | 2.42 | 2.17-2.71 | 14/14 | yes |
| initial_persistence | 14 | 9.96 | 9.04-11.01 | 14/14 | yes |
| band_native | 5 | 0.99 | 0.81-1.23 | 2/5 | band |
| ablate_a2 | 4 | 9.64 | 8.10-11.94 | 4/4 | yes |
| ablate_chi0 | 3 | 9.52 | 8.04-11.59 | 3/3 | yes |
| ablate_DS2 | 4 | 13.46 | 12.35-14.91 | 4/4 | yes |
| numerical_null | 3 | 0.99 | 0.91-1.05 | 1/3 | null |

Per group: ratio to independent_native over the cases each control ran on.

| control | device0/S | device0/K | device0/L | device0/phi | device1/S | device1/K | device1/L | device1/phi | global/S | global/K | global/L | global/phi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ignore_actions | 8.18 | 10.47 | 8.82 | 8.65 | 3.63 | 3.39 | 2.99 | 3.43 | 1.41 | 1.95 | 2.20 | 1.55 |
| wrong_probe_geometry | 4.13 | 5.98 | 6.11 | 5.46 | 1.94 | 2.65 | 3.07 | 2.31 | 1.06 | 1.04 | 1.05 | 1.02 |
| initial_persistence | 21.10 | 22.18 | 17.29 | 20.81 | 7.98 | 7.01 | 5.84 | 8.51 | 7.04 | 11.39 | 7.76 | 10.36 |
| band_native | 0.71 | 0.70 | 0.82 | 0.69 | 1.08 | 1.09 | 1.08 | 1.10 | 0.94 | 1.02 | 1.08 | 0.99 |
| ablate_a2 | 16.06 | 13.62 | 9.32 | 14.95 | 8.12 | 6.74 | 4.62 | 8.96 | 11.36 | 11.15 | 11.12 | 10.93 |
| ablate_chi0 | 11.14 | 9.69 | 9.00 | 9.47 | 9.18 | 5.23 | 4.49 | 4.89 | 12.92 | 14.33 | 15.74 | 15.18 |
| ablate_DS2 | 17.45 | 14.93 | 9.16 | 17.92 | 6.94 | 5.65 | 4.92 | 5.71 | 27.80 | 22.73 | 20.36 | 12.89 |
| numerical_null | 0.77 | 0.87 | 1.09 | 0.62 | 0.91 | 0.90 | 0.91 | 0.87 | 1.21 | 1.18 | 1.02 | 1.38 |

Groups not to rely on (control's group interval reaches the band's group interval):

- ignore_actions: global/S, global/K, global/phi
- wrong_probe_geometry: global/S, global/K, global/L, global/phi

Per case: aggregate ratio to independent_native (blank: not run on that case).

| case | program | ignore_actions | wrong_probe_geometry | initial_persistence | band_native | ablate_a2 | ablate_chi0 | ablate_DS2 | numerical_null |
|---|---|---|---|---|---|---|---|---|---|
| c001 | sham | 0.91 | 2.68 | 9.15 | 0.97 | 10.23 | 11.25 | 11.72 | 1.11 |
| c002 | probe_shift | 1.07 | 2.90 | 10.22 |  |  |  |  |  |
| c003 | probe_wide | 3.98 | 3.68 | 12.30 |  |  |  |  |  |
| c004 | K_d0 | 2.99 | 2.22 | 11.71 | 0.78 |  |  |  | 0.88 |
| c005 | L_d0 | 3.02 | 1.74 | 6.96 | 0.70 | 6.56 | 6.92 |  |  |
| c006 | L_rim | 5.78 | 2.91 | 10.23 |  | 10.74 | 11.80 |  |  |
| c007 | Sm_d0 | 3.41 | 1.62 | 8.20 |  |  |  |  | 0.96 |
| c008 | Sp_d0 | 7.35 | 2.95 | 12.71 |  |  |  | 13.99 |  |
| c009 | Sm_d1 | 3.27 | 2.96 | 13.12 |  |  |  | 15.69 |  |
| c010 | Sp_d1 | 5.35 | 2.74 | 10.76 | 1.26 |  |  | 13.19 |  |
| c011 | K_d1 | 2.78 | 2.18 | 7.30 |  |  |  |  |  |
| c012 | L_d1 | 5.62 | 3.00 | 13.14 |  | 13.25 |  |  |  |
| c013 | move_during_pulse | 2.35 | 1.75 | 8.26 |  |  |  |  |  |
| c014 | two_sources | 6.27 | 1.95 | 11.98 | 1.46 |  |  |  |  |

Per case and sensor for the mechanism controls and the null: device0 / device1 / global.

| case | program | ablate_a2 | ablate_chi0 | ablate_DS2 | numerical_null |
|---|---|---|---|---|---|
| c001 | sham | 13.5/6.2/15.8 | 13.0/5.6/21.6 | 13.0/4.4/26.0 | 0.6/1.0/1.7 |
| c002 | probe_shift |  |  |  |  |
| c003 | probe_wide |  |  |  |  |
| c004 | K_d0 |  |  |  | 1.3/0.7/1.1 |
| c005 | L_d0 | 7.0/6.1/6.8 | 5.2/5.5/9.0 |  |  |
| c006 | L_rim | 15.5/7.1/15.3 | 15.4/6.4/19.7 |  |  |
| c007 | Sm_d0 |  |  |  | 1.1/1.0/0.9 |
| c008 | Sp_d0 |  |  | 9.7/7.0/22.7 |  |
| c009 | Sm_d1 |  |  | 22.7/9.0/17.0 |  |
| c010 | Sp_d1 |  |  | 12.6/3.9/19.8 |  |
| c011 | K_d1 |  |  |  |  |
| c012 | L_d1 | 26.2/10.2/11.7 |  |  |  |
| c013 | move_during_pulse |  |  |  |  |
| c014 | two_sources |  |  |  |  |
