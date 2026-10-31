# c53 fed vortices: lab bundle controls (15 cases)

Ratios = control score / mean of 16 independent 4-member native slices; native band (aggregate) 0.94-1.05.

| control | cases | aggregate ratio | 90% CI | cases beyond the native band |
|---|---|---|---|---|
| independent_native | 15 | 0.97 | 0.94-1.01 | 0/15 |
| ignore_actions | 15 | 11.75 | 8.71-14.92 | 14/15 |
| initial_persistence | 15 | 23.62 | 21.45-25.93 | 15/15 |
| wrong_probe_geometry | 15 | 13.50 | 12.63-14.48 | 15/15 |
| ablate_adv0 | 15 | 116.21 | 109.28-123.03 | 15/15 |
| ablate_kF0 | 15 | 154.31 | 145.90-162.77 | 15/15 |
| ablate_body_gain | 15 | 12.23 | 11.03-13.62 | 15/15 |
| numerical_null | 15 | 1.02 | 0.98-1.06 | 1/15 |
| ablate_k0 | 5 | 238.10 | 209.89-272.82 | 5/5 |
| ablate_mu0 | 5 | 1989.19 | 1781.65-2173.10 | 5/5 |

Per case (ratio; band = slice min-max):

| case | program | native64 | band | ignore_actions | initial_persistence | wrong_probe_geometry | ablate_adv0 | ablate_kF0 | ablate_body_gain | numerical_null | ablate_k0 | ablate_mu0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c001 | sham | 0.0376 | 0.91-1.09 | 1.03 | 20.12 | 12.43 | 109.59 | 147.98 | 10.15 | 0.97 | 233.53 | 1976.31 |
| c002 | probe_shift | 0.0402 | 0.86-1.34 | 4.94 | 17.91 | 11.50 | 101.80 | 138.73 | 9.81 | 1.15 | - | - |
| c003 | probe_wide | 0.0366 | 0.89-1.17 | 10.27 | 22.22 | 12.26 | 111.84 | 151.89 | 10.01 | 0.94 | - | - |
| c004 | pulse_then_move | 0.0325 | 0.86-1.36 | 11.09 | 21.41 | 13.46 | 125.71 | 167.31 | 11.05 | 1.10 | - | - |
| c005 | move_then_pulse | 0.0384 | 0.92-1.11 | 9.17 | 19.30 | 12.16 | 109.18 | 145.08 | 9.99 | 1.02 | - | - |
| c006 | two_sources | 0.0253 | 0.86-1.25 | 21.51 | 28.76 | 14.99 | 152.06 | 199.14 | 14.15 | 0.96 | - | - |
| c007 | move_during_pulse | 0.0359 | 0.93-1.09 | 10.14 | 19.89 | 12.27 | 115.25 | 153.41 | 9.87 | 0.94 | - | - |
| c008 | delayed_feed | 0.0322 | 0.90-1.17 | 6.74 | 24.83 | 18.69 | 134.44 | 167.34 | 12.21 | 0.98 | - | 2233.61 |
| c009 | feed_neck | 0.0427 | 0.84-1.31 | 21.61 | 29.36 | 17.48 | 108.42 | 132.28 | 19.47 | 1.13 | 224.14 | - |
| c010 | starve_neck | 0.0327 | 0.84-1.26 | 6.05 | 23.71 | 12.54 | 116.16 | 162.34 | 12.78 | 0.95 | - | 2179.85 |
| c011 | feed_vortex | 0.0331 | 0.81-1.27 | 25.26 | 34.81 | 14.74 | 123.94 | 159.20 | 16.70 | 1.11 | 272.48 | - |
| c012 | starve_vortex | 0.0342 | 0.88-1.26 | 13.47 | 28.04 | 12.68 | 113.61 | 157.88 | 11.21 | 0.89 | - | 2137.29 |
| c013 | stir_cut | 0.0480 | 0.84-1.15 | 5.95 | 18.46 | 11.02 | 84.48 | 118.22 | 10.27 | 1.16 | 184.51 | 1578.25 |
| c014 | follow_vortex | 0.0326 | 0.93-1.11 | 9.06 | 17.51 | 12.77 | 122.44 | 165.50 | 11.46 | 0.94 | - | - |
| c015 | feed_and_follow | 0.0280 | 0.87-1.35 | 25.61 | 32.46 | 14.75 | 142.83 | 184.51 | 15.07 | 0.92 | 307.93 | - |

Per group (ratio; group band in the first row):

| control | device0/eat | device0/om | device0/speed | device0/Y | device1/eat | device1/om | device1/speed | device1/Y | global/eat | global/om | global/speed | global/Y |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| native band | 0.90-1.10 | 0.93-1.06 | 0.96-1.08 | 0.93-1.07 | 0.93-1.05 | 0.94-1.05 | 0.95-1.06 | 0.93-1.07 | 0.94-1.08 | 0.91-1.08 | 0.93-1.08 | 0.89-1.10 |
| ignore_actions | 26.21 | 18.44 | 13.07 | 31.75 | 17.11 | 16.01 | 15.25 | 20.37 | 18.75 | 7.35 | 5.00 | 8.33 |
| initial_persistence | 64.41 | 65.35 | 38.60 | 98.08 | 28.70 | 31.15 | 25.42 | 44.12 | 21.52 | 10.47 | 7.53 | 14.14 |
| wrong_probe_geometry | 55.38 | 46.71 | 25.71 | 47.47 | 25.14 | 26.82 | 20.52 | 32.30 | 3.88 | 1.35 | 1.10 | 2.11 |
| ablate_adv0 | 66.44 | 68.07 | 103.54 | 102.72 | 27.05 | 31.94 | 87.75 | 45.40 | 12.49 | 7.28 | 323.18 | 8.38 |
| ablate_kF0 | 17.90 | 11.28 | 46.52 | 73.87 | 17.63 | 18.69 | 40.17 | 37.51 | 327.61 | 246.95 | 148.58 | 358.65 |
| ablate_body_gain | 14.36 | 8.52 | 5.62 | 16.67 | 6.76 | 4.86 | 2.96 | 5.42 | 35.95 | 16.62 | 3.58 | 30.51 |
| numerical_null | 1.11 | 1.07 | 1.04 | 1.06 | 0.98 | 0.98 | 0.98 | 0.97 | 1.01 | 1.00 | 1.04 | 1.00 |
| ablate_k0 | 48.52 | 42.66 | 79.20 | 76.63 | 30.21 | 28.21 | 70.95 | 68.87 | 428.36 | 356.51 | 285.77 | 519.70 |
| ablate_mu0 | 86.77 | 170.63 | 401.23 | 224.17 | 38.71 | 108.74 | 310.44 | 120.92 | 1102.20 | 5220.80 | 3494.79 | 1246.19 |

Targeted programs: mechanism control ratio vs the case's native band maximum

| program | control | ratio | band max | fails |
|---|---|---|---|---|
| sham | ablate_body_gain | 10.15 | 1.09 | yes |
| sham | ablate_adv0 | 109.59 | 1.09 | yes |
| delayed_feed | ablate_body_gain | 12.21 | 1.17 | yes |
| delayed_feed | ablate_mu0 | 2233.61 | 1.17 | yes |
| feed_neck | ablate_body_gain | 19.47 | 1.31 | yes |
| feed_neck | ablate_k0 | 224.14 | 1.31 | yes |
| starve_neck | ablate_body_gain | 12.78 | 1.26 | yes |
| starve_neck | ablate_mu0 | 2179.85 | 1.26 | yes |
| feed_vortex | ablate_k0 | 272.48 | 1.27 | yes |
| starve_vortex | ablate_mu0 | 2137.29 | 1.26 | yes |
| stir_cut | ablate_k0 | 184.51 | 1.15 | yes |
| stir_cut | ablate_mu0 | 1578.25 | 1.15 | yes |
| follow_vortex | ablate_adv0 | 122.44 | 1.11 | yes |
| feed_and_follow | ablate_adv0 | 142.83 | 1.35 | yes |
| feed_and_follow | ablate_k0 | 307.93 | 1.35 | yes |

Per group: programs on which a control stays inside that group's per-case native band

| group | ignore_actions inside | wrong_probe_geometry inside | null beyond band (cases) | body_gain inside |
|---|---|---|---|---|
| device0/eat | sham, probe_wide, follow_vortex | - | 5 | - |
| device0/om | sham, probe_wide, follow_vortex | - | 4 | - |
| device0/speed | sham, probe_wide, follow_vortex | - | 2 | - |
| device0/Y | sham, probe_wide, follow_vortex | - | 4 | - |
| device1/eat | probe_shift, pulse_then_move, delayed_feed | - | 0 | - |
| device1/om | sham, probe_shift, pulse_then_move, delayed_feed | - | 0 | - |
| device1/speed | sham, probe_shift, delayed_feed | - | 0 | - |
| device1/Y | probe_shift, pulse_then_move, delayed_feed | - | 0 | - |
| global/eat | sham, probe_shift, probe_wide, follow_vortex | sham, probe_shift, probe_wide, pulse_then_move, follow_vortex | 2 | - |
| global/om | sham, probe_shift, probe_wide, follow_vortex | sham, probe_shift, probe_wide, pulse_then_move, move_then_pulse, move_during_pulse, starve_neck, follow_vortex, feed_and_follow | 0 | - |
| global/speed | sham, probe_shift, probe_wide, follow_vortex | sham, probe_shift, probe_wide, pulse_then_move, move_then_pulse, move_during_pulse, delayed_feed, feed_neck, starve_neck, starve_vortex, stir_cut, follow_vortex | 0 | - |
| global/Y | sham, probe_shift, probe_wide, follow_vortex | sham, probe_shift, probe_wide, pulse_then_move, move_then_pulse, move_during_pulse, starve_neck, follow_vortex, feed_and_follow | 1 | - |

Reward (K=2): native 64-member primary energy 0.0353 -> reward 0.726; initial persistence 1.026 -> 0.000. Worst native case 0.0480; PhySim's rule gives K = 1. Scales x10 would make K=2 calibrated.

Simulation CPU in cached control ensembles: 2.74 h.
