# cips_iso: frozen suite, controls vs independent_native

12 cases; 4 members per control ensemble, 2 truths per case; PhySim score_case joint energy, equal-group mean over 12 groups. Ratio = control / independent_native (means over the cases the control ran on); 90% case-bootstrap interval. Band = band_native / independent_native, all cases: 0.97-1.11. 'sep' = interval above the band's upper bound.

| control | cases | ratio | 90% interval | cases worse | sep |
|---|---|---|---|---|---|
| ignore_actions | 12 | 4.73 | 3.64-5.86 | 12/12 | yes |
| wrong_probe_geometry | 12 | 6.72 | 6.19-7.34 | 12/12 | yes |
| initial_persistence | 12 | 8.15 | 6.96-9.48 | 12/12 | yes |
| band_native | 4 | 1.05 | 0.97-1.11 | 3/4 | band |
| ablate_chi0 | 2 | 94.21 | 88.46-100.51 | 2/2 | yes |
| ablate_kF0 | 2 | 276.27 | 264.30-289.42 | 2/2 | yes |
| ablate_chis0 | 2 | 11.75 | 10.62-12.97 | 2/2 | yes |
| ablate_d0 | 2 | 24.18 | 22.05-26.49 | 2/2 | yes |
| ablate_DF10 | 2 | 79.70 | 77.04-82.57 | 2/2 | yes |
| numerical_null | 3 | 1.12 | 1.09-1.15 | 3/3 | null |

Per group: ratio to independent_native over the cases each control ran on.

| control | device0/e | device0/p | device0/F | device0/s | device1/e | device1/p | device1/F | device1/s | global/e | global/p | global/F | global/s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ignore_actions | 8.22 | 11.33 | 7.31 | 5.10 | 6.73 | 9.51 | 9.22 | 3.84 | 1.36 | 5.89 | 2.77 | 4.61 |
| wrong_probe_geometry | 15.29 | 14.65 | 13.17 | 8.31 | 18.48 | 20.52 | 19.42 | 10.59 | 1.00 | 1.08 | 1.00 | 0.97 |
| initial_persistence | 16.62 | 21.36 | 14.24 | 9.29 | 9.90 | 13.40 | 12.04 | 5.00 | 4.05 | 8.81 | 4.48 | 7.42 |
| band_native | 1.07 | 1.06 | 1.03 | 1.05 | 1.25 | 1.24 | 1.21 | 1.27 | 0.94 | 0.97 | 1.01 | 0.93 |
| ablate_chi0 | 29.14 | 42.73 | 79.11 | 8.89 | 27.82 | 41.29 | 66.26 | 9.13 | 141.04 | 183.80 | 118.04 | 145.89 |
| ablate_kF0 | 17.47 | 43.96 | 70.25 | 8.03 | 25.86 | 53.59 | 109.77 | 9.99 | 143.01 | 275.00 | 1085.67 | 212.67 |
| ablate_chis0 | 1.00 | 1.00 | 1.00 | 6.65 | 1.00 | 1.00 | 1.00 | 9.12 | 1.00 | 1.00 | 1.00 | 121.64 |
| ablate_d0 | 11.63 | 11.88 | 14.92 | 7.03 | 7.10 | 7.70 | 11.59 | 4.05 | 38.89 | 31.23 | 38.51 | 25.36 |
| ablate_DF10 | 18.20 | 45.67 | 38.03 | 13.54 | 7.55 | 32.62 | 35.81 | 3.60 | 29.75 | 293.88 | 114.64 | 210.21 |
| numerical_null | 1.14 | 1.22 | 1.22 | 1.17 | 1.16 | 1.13 | 1.14 | 1.20 | 1.04 | 1.06 | 1.13 | 1.06 |

Groups not to rely on (control's group interval reaches the band's group interval):

- wrong_probe_geometry: global/e, global/p, global/F, global/s
- ablate_chis0: device0/e, device0/p, device0/F, device1/e, device1/p, device1/F, global/e, global/p, global/F

Per case: aggregate ratio to independent_native (blank: not run on that case).

| case | program | ignore_actions | wrong_probe_geometry | initial_persistence | band_native | ablate_chi0 | ablate_kF0 | ablate_chis0 | ablate_d0 | ablate_DF10 | numerical_null |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c001 | sham | 1.09 | 6.71 | 5.97 | 1.13 | 88.46 | 264.30 | 10.62 | 26.49 | 82.57 | 1.09 |
| c002 | probe_shift | 1.46 | 5.36 | 4.01 |  |  |  |  |  |  |  |
| c003 | probe_wide | 6.96 | 6.09 | 11.54 |  |  |  |  |  |  |  |
| c004 | p_d0 | 7.63 | 6.54 | 8.43 | 0.87 | 100.51 |  |  |  |  |  |
| c005 | p_d1 | 3.81 | 6.16 | 6.64 |  |  |  |  |  |  |  |
| c006 | Fp_d0 | 6.60 | 8.39 | 7.17 |  |  | 289.42 |  |  |  | 1.10 |
| c007 | Fp_d1 | 4.81 | 9.53 | 9.65 |  |  |  |  |  |  |  |
| c008 | Fm_d0 | 5.04 | 5.05 | 7.04 | 1.08 |  |  |  | 22.05 | 77.04 | 1.17 |
| c009 | Fm_d1 | 4.70 | 7.37 | 9.69 |  |  |  |  |  |  |  |
| c010 | s_d0 | 3.65 | 7.97 | 8.33 |  |  |  | 12.97 |  |  |  |
| c011 | move_during_pulse | 4.44 | 6.28 | 9.01 |  |  |  |  |  |  |  |
| c012 | two_sources | 9.49 | 6.91 | 14.68 | 1.09 |  |  |  |  |  |  |

Per case and sensor for the mechanism controls and the null: device0 / device1 / global.

| case | program | ablate_chi0 | ablate_kF0 | ablate_chis0 | ablate_d0 | ablate_DF10 | numerical_null |
|---|---|---|---|---|---|---|---|
| c001 | sham | 20.8/28.7/138.3 | 28.1/38.0/443.4 | 3.4/5.3/15.6 | 13.9/7.9/37.9 | 21.2/16.9/131.1 | 1.4/1.3/0.9 |
| c002 | probe_shift |  |  |  |  |  |  |
| c003 | probe_wide |  |  |  |  |  |  |
| c004 | p_d0 | 51.9/22.7/143.1 |  |  |  |  |  |
| c005 | p_d1 |  |  |  |  |  |  |
| c006 | Fp_d0 |  | 28.5/30.6/553.5 |  |  |  | 1.2/1.0/1.1 |
| c007 | Fp_d1 |  |  |  |  |  |  |
| c008 | Fm_d0 |  |  |  | 5.7/5.2/34.1 | 29.3/10.8/119.0 | 0.9/1.3/1.2 |
| c009 | Fm_d1 |  |  |  |  |  |  |
| c010 | s_d0 |  |  | 4.5/5.3/20.7 |  |  |  |
| c011 | move_during_pulse |  |  |  |  |  |  |
| c012 | two_sources |  |  |  |  |  |  |
