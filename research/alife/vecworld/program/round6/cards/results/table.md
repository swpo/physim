# World cards: comparison table (run A; ratios from medians over test states)

Columns: sigma_hat at the block and the population level (the verdict uses the larger where the level is predictable); PF(8), c(8), w_theta(8): predictable fraction, closure ceiling of the cheap family and weight of a prior-sized error in the hidden part, block view, 8 ticks; PL10%/Vorc: plug-in loss of a 10%-of-prior neighbour over the oracle variance; bodies, half-life (ticks); body law c(8): ceiling of the single-body law for displacement on quiet steps; act_ms: predictable shift of an aimed 200-nat input over the oracle variance at 4 ticks, and the same over the cheap family's error; tick share: mean over block channels, and the largest population component; member share (block view); pop c(8); learned dc(16): ceiling of the slow features minus the hand view at 16 ticks (the smaller of the two orders); late = early; ms per member-tick (compile included where the world's only run was a first call: the 128-px rows).

| world | role | verdict | sigma_hat block | sigma_hat pop | PF(8) | c(8) | w_theta(8) | PL10%/Vorc | bodies | half-life | body law c(8) | act_ms | act / cheap error | tick share block | tick share pop, max | member share | pop c(8) | learned dc(16) | late = early | ms/member-tick |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gliders | designed | exam-worthy + actions | 0.097 | 0.20 | 0.99 | 0.45 | 0.058 | 0.026 | 7.47 | 23.4 | 0.97 | 6.42 | 0.13 | 4.6e-07 | 0.042 | 0.73 | 0.14 | -0.14 | yes | 1.50 |
| vortex64 | designed | exam-worthy + reading-worthy + actions | 0.082 | 0.35 | 0.93 | 0.46 | 0.055 | 0.010 | 8.00 | 51.3 | 0.88 | 19.7 | 1.81 | 0.028 | 0.58 | 0.34 | 0.62 | 0.034 | yes | 4.78 |
| membrane | designed | exam-worthy + reading-worthy + actions | 0.012 | 0.16 | 1.00 | 1.00 | 0.018 | 0.15 | 14.5 | 215 | 0.66 | 5.25 | 2.19 | -0.001 | 0.058 | 0.073 | 0.83 | -0.028 | yes | 0.14 |
| foundry_04470 | shortlist | exam-worthy + reading-worthy + actions | 0.44 | 0.89 | 1.00 | 0.52 | 0.96 | 189 | 18.9 | 22.0 | 0.41 | 4.19 | 0.015 | 2.5e-05 | 0.068 | 0.15 | 0.053 | 0.093 | yes | 0.045 |
| foundry_04186 | shortlist | exam-worthy + reading-worthy + actions | 0.44 | 0.68 | 0.99 | 0.50 | 0.90 | 12.1 | 10.1 | 20.4 | 0.86 | 12.1 | 0.38 | 1.4e-05 | 0.36 | 0.058 | 0.34 | -0.21 | yes | 0.049 |
| foundry_00262 | shortlist | exam-worthy + reading-worthy + actions | 0.49 | 0.71 | 1.00 | 0.51 | 0.84 | 304 | 12.0 | 20.1 | 0.88 | 3.78 | 0.001 | -7.2e-06 | 0.078 | 0.19 | 0.23 | -0.14 | no | 0.049 |
| foundry_07567 | shortlist | exam-worthy + actions | 0.48 | 0.77 | 0.99 | 0.50 | 0.95 | 81.9 | 11.1 | 11.2 | 0.67 | 7.33 | 0.16 | 2.8e-05 | 0.036 | 0.095 | 0.16 | 0.049 | yes | 0.049 |
| foundry_06845 | shortlist | exam-worthy + actions | 0.31 | 0.92 | 1.00 | 0.74 | 1.02 | 27.2 | 12.4 | 14.2 | 0.46 | 8.38 | 0.098 | 8.3e-06 | 0.022 | 0.11 | 0.10 | -0.30 | yes | 0.048 |
| foundry_01672 | shortlist | exam-worthy + actions | 0.28 | 0.49 | 1.00 | 0.76 | 0.94 | 125 | 4.06 | 37.3 | 0.95 | 20.5 | 0.33 | 1.1e-05 | 0.13 | 0.16 | 0.44 | -0.23 | yes | 0.049 |
| foundry_03078 | shortlist | exam-worthy + reading-worthy + actions | 0.29 | 0.54 | 1.00 | 0.74 | 0.84 | 33.3 | 13.2 | 36.2 | 0.89 | 19.0 | 0.33 | 2.4e-04 | 0.47 | 0.035 | 0.42 | -0.19 | yes | 0.049 |
| ctl_noise | control | dull: nothing predictable | 1.00 | 1.00 | -0.005 | -0.00 | n/a | 1.2e-04 | 11.6 | 0.80 | n/a | 0.00 | 0.00 | -5.8e-06 | 0.014 | 0.005 | -0.00 | 0.12 | n/a | 0.021 |
| ctl_freebodies | control | dull: the hidden part has no weight | 0.007 | 0.063 | 0.95 | 0.74 | 0.003 | 6.5e-04 | 5.37 | 40.4 | 0.98 | 4.27 | 0.66 | -1.3e-05 | 0.053 | 0.073 | 0.35 | -0.086 | yes | 0.020 |
| ctl_uniform_00000 | control | dull: predictable by the cheap family | 0.005 | n/a | 0.58 | 0.99 | 2.38 | 0.048 | 0.00 | n/a | n/a | 3.56 | 3.60 | 9.1e-06 | n/a | 0.41 | n/a | -0.011 | no | 0.046 |
| ctl_uniform_00002 | control | dull: predictable by the cheap family | 0.028 | n/a | 0.46 | 0.97 | 407 | 0.90 | 0.00 | n/a | n/a | 4.47 | 4.46 | 0.003 | n/a | 9.1e-04 | n/a | -0.020 | yes | 0.046 |
| ctl_uniform_00003 | control | dull: predictable by the cheap family | 2.5e-04 | n/a | 0.99 | 1.00 | 55.2 | 3.75 | 0.013 | 11.6 | n/a | 6.22 | 6.01 | 8.2e-04 | n/a | 0.17 | n/a | -0.004 | no | 0.046 |
| ctl_uniform_00004 | control | dull: predictable by the cheap family | 1.6e-04 | n/a | 0.99 | 1.00 | 2.03 | 2.89 | 0.002 | n/a | n/a | 5.98 | 5.94 | 0.002 | n/a | 0.049 | n/a | -0.005 | no | 0.046 |
| ctl_frozen_00001 | control | dull: predictable by the cheap family | 2.9e-04 | 0.026 | 1.00 | 1.00 | 0.004 | 0.49 | 0.68 | 220 | 0.00 | 14.1 | 13.1 | 1.3e-04 | 0.055 | 0.78 | 0.93 | -4.0e-04 | no | 0.048 |
| ctl_frozen_00011 | control | dull: predictable by the cheap family | 3.0e-04 | 0.032 | 0.99 | 1.00 | 0.010 | 0.017 | 0.55 | 76.7 | -0.00 | 11.9 | 12.0 | 9.2e-04 | 0.26 | 0.28 | 1.00 | -0.002 | no | 0.048 |
| ctl_frozen_00022 | control | dull: predictable by the cheap family | 1.8e-04 | 0.055 | 1.00 | 1.00 | 0.24 | 17.6 | 18.5 | 5299 | 0.00 | 1.34 | 0.64 | 0.005 | 0.92 | 0.046 | 0.97 | 2.3e-05 | yes | 0.047 |
| ctl_frozen_00024 | control | dull: predictable by the cheap family | 5.1e-04 | 0.045 | 1.00 | 1.00 | 1.72 | 3.73 | 13.5 | 1199 | 0.017 | 6.62 | 5.70 | 9.4e-04 | 0.67 | 0.097 | 0.97 | -7.8e-04 | no | 0.048 |
| ctl_diffusion_0 | control | dull: predictable by the cheap family | 7.8e-04 | n/a | 0.89 | 1.00 | 4.2e-04 | 4.9e-05 | 0.00 | n/a | n/a | 4.74 | 4.71 | 1.4e-04 | n/a | 0.096 | n/a | -0.008 | n/a | 0.046 |
| ctl_diffusion_1 | control | dull: predictable by the cheap family | 1.7e-08 | n/a | 0.98 | 1.00 | 8.1e-09 | 4.0e-10 | 0.00 | n/a | n/a | 4.92 | 4.88 | 7.9e-04 | n/a | 0.15 | n/a | -0.003 | n/a | 0.046 |
| foundry_00060 | candidate | exam-worthy + reading-worthy + actions | 0.10 | 0.39 | 1.00 | 0.94 | 0.70 | 38.0 | 5.22 | 29.6 | 0.57 | 9.32 | 0.30 | 0.001 | 0.34 | 0.061 | 0.64 | -0.046 | yes | 0.047 |
| foundry_00124 | candidate | dull: the hidden part has no weight | 0.036 | 0.15 | 1.00 | 0.98 | 0.25 | 37.7 | 16.6 | 173 | 0.61 | 3.38 | 0.16 | 0.003 | 0.33 | 0.48 | 0.87 | -0.084 | no | 0.045 |
| foundry_00416 | candidate | exam-worthy + reading-worthy + actions | 0.034 | 0.16 | 1.00 | 0.98 | 0.58 | 16.7 | 6.42 | 117 | 0.47 | 14.3 | 1.74 | 2.8e-04 | 0.65 | 0.16 | 0.92 | -0.10 | yes | 0.046 |
| foundry_02755 | candidate | exam-worthy + reading-worthy + actions | 0.14 | 0.41 | 1.00 | 0.89 | 0.63 | 44.7 | 10.8 | 44.2 | 0.75 | 22.3 | 0.49 | 9.3e-06 | 0.34 | 0.19 | 0.60 | -0.14 | no | 0.046 |
| foundry_03062 | candidate | dull: predictable by the cheap family | 0.028 | 0.042 | 1.00 | 0.98 | 1.64 | 137 | 6.63 | 89.8 | 0.85 | 28.9 | 1.29 | 0.001 | 0.91 | 0.027 | 0.96 | -0.12 | no | 0.046 |
| foundry_03101 | candidate | exam-worthy + reading-worthy + actions | 0.039 | 0.25 | 1.00 | 0.97 | 0.76 | 18.9 | 12.1 | 54.2 | 0.63 | 16.8 | 0.67 | 3.9e-06 | 0.53 | 0.29 | 0.77 | -0.041 | yes | 0.047 |
| foundry_03854 | candidate | dull: predictable by the cheap family | 0.008 | 0.015 | 1.00 | 1.00 | 0.67 | 9.95 | 6.64 | 114 | 0.00 | 12.0 | 4.82 | 7.9e-04 | 0.89 | 0.054 | 0.99 | -0.005 | no | 0.047 |
| foundry_04289 | candidate | exam-worthy + reading-worthy + actions | 0.23 | 0.52 | 1.00 | 0.82 | 0.79 | 49.1 | 13.8 | 27.8 | 0.78 | 9.01 | 0.050 | 1.5e-04 | 0.27 | 0.19 | 0.41 | -0.100 | yes | 0.046 |
| foundry_04495 | candidate | exam-worthy + actions | 0.19 | 0.024 | 1.00 | 0.86 | 1.13 | 90.3 | 8.88 | 68.4 | 0.99 | 77.4 | 0.36 | 4.2e-04 | 0.93 | 0.092 | 0.99 | -0.44 | no | 0.046 |
| foundry_04833 | candidate | exam-worthy + reading-worthy + actions | 0.11 | 0.51 | 0.99 | 0.92 | 0.73 | 2.11 | 17.3 | 85.3 | 0.34 | 9.10 | 1.95 | 5.4e-04 | 0.50 | 0.14 | 0.53 | 0.069 | yes | 0.045 |
| foundry_04919 | candidate | exam-worthy + reading-worthy + actions | 0.014 | 0.18 | 0.99 | 0.99 | 0.92 | 0.25 | 19.2 | 96.5 | 0.028 | 7.54 | 4.67 | 0.056 | 0.98 | 5.0e-04 | 0.81 | -0.002 | yes | 0.045 |
| foundry_05671 | candidate | exam-worthy + reading-worthy + actions | 0.020 | 0.16 | 1.00 | 0.99 | 0.81 | 8.34 | 14.1 | 80.2 | 0.33 | 10.8 | 3.13 | 0.017 | 0.55 | 0.11 | 0.83 | 0.023 | yes | 0.045 |
| foundry_07760 | candidate | exam-worthy + reading-worthy + actions | 0.090 | 0.18 | 1.00 | 0.95 | 0.72 | 5.36 | 14.7 | 104 | 0.67 | 16.3 | 1.23 | 0.002 | 0.93 | 0.022 | 0.82 | -0.15 | no | 0.046 |
| foundry_07820 | candidate | dull: predictable by the cheap family | 0.024 | 0.065 | 1.00 | 0.99 | 0.67 | 11.9 | 18.5 | 241 | 0.17 | 13.3 | 4.28 | 2.0e-04 | 0.85 | 0.11 | 0.94 | 0.003 | no | 0.045 |
| foundry_07913 | candidate | dull: predictable by the cheap family | 0.046 | 0.041 | 1.00 | 0.98 | 11.4 | 15.9 | 14.5 | 202 | 0.89 | 16.5 | 1.90 | 5.7e-04 | 0.92 | 0.054 | 0.97 | -0.011 | no | 0.046 |
| foundry_08010 | candidate | dull: predictable by the cheap family | 0.022 | 0.064 | 1.00 | 0.99 | 0.42 | 22.7 | 9.41 | 68.9 | 0.53 | 22.4 | 2.67 | 0.002 | 0.86 | 0.12 | 0.94 | -0.046 | no | 0.046 |
| foundry_00005 | prior | dull: predictable by the cheap family | 0.010 | n/a | 0.58 | 0.99 | 0.087 | 0.006 | 0.00 | n/a | n/a | 4.01 | 4.07 | 3.4e-06 | n/a | 0.12 | n/a | 0.012 | n/a | 0.047 |
| foundry_00006 | prior | dull: predictable by the cheap family | 4.9e-04 | n/a | 0.98 | 1.00 | 0.006 | 0.004 | 0.00 | n/a | n/a | 5.31 | 5.13 | 3.8e-04 | n/a | 0.15 | n/a | -0.002 | n/a | 0.047 |
| foundry_00007 | prior | dull: predictable by the cheap family | 0.002 | n/a | 0.89 | 1.00 | 0.017 | 0.002 | 0.00 | n/a | n/a | 5.46 | 5.39 | 3.4e-05 | n/a | 0.098 | n/a | -0.011 | n/a | 0.046 |
| foundry_00008 | prior | dull: predictable by the cheap family | 4.3e-04 | n/a | 0.98 | 1.00 | 4.82 | 0.028 | 0.002 | n/a | n/a | 7.83 | 7.83 | 0.17 | n/a | 4.6e-04 | n/a | -0.003 | n/a | 0.046 |
| foundry_00009 | prior | dull: the hidden part has no weight | 0.002 | 0.070 | 1.00 | 1.00 | 0.54 | 8.84 | 13.7 | 210 | 0.00 | 0.90 | 0.40 | 0.002 | 0.90 | 0.12 | 0.90 | 6.9e-04 | n/a | 0.049 |
| foundry_00010 | prior | dull: predictable by the cheap family | 0.005 | 0.041 | 1.00 | 1.00 | 0.33 | 1.76 | 17.9 | 239 | 0.00 | 3.46 | 1.90 | 0.004 | 0.38 | 0.011 | 0.96 | -0.004 | n/a | 0.047 |
| foundry_00012 | prior | dull: predictable by the cheap family | 0.001 | n/a | 0.96 | 1.00 | 0.93 | 0.22 | 0.00 | n/a | n/a | 6.88 | 6.87 | 2.8e-04 | n/a | 0.19 | n/a | -0.003 | n/a | 0.047 |
| foundry_00013 | prior | exam-worthy + actions | 0.019 | 0.20 | 1.00 | 0.99 | 0.48 | 4.97 | 21.3 | 416 | 0.015 | 3.43 | 0.78 | 0.002 | 0.71 | 0.015 | 0.84 | -0.011 | n/a | 0.047 |
| foundry_00014 | prior | dull: predictable by the cheap family | 0.00 | n/a | 0.83 | 1.00 | 18.0 | 0.21 | 0.00 | n/a | n/a | 3.20 | 3.30 | 0.65 | n/a | 6.8e-06 | n/a | -0.026 | n/a | 0.046 |
| foundry_00015 | prior | dull: predictable by the cheap family | 2.7e-04 | n/a | 0.99 | 1.00 | 1.53 | 0.17 | 0.048 | 19.1 | n/a | 7.18 | 7.16 | 0.002 | n/a | 0.069 | n/a | -0.006 | n/a | 0.046 |
| foundry_00016 | prior | dull: predictable by the cheap family | 3.3e-04 | n/a | 0.99 | 1.00 | 0.009 | 0.004 | 0.00 | n/a | n/a | 8.25 | 8.07 | 1.5e-04 | n/a | 0.48 | n/a | -0.001 | n/a | 0.047 |
| foundry_00017 | prior | dull: predictable by the cheap family | 2.3e-04 | n/a | 0.99 | 1.00 | 8.7e-04 | 0.002 | 0.074 | 15.4 | n/a | 6.88 | 6.70 | 0.001 | n/a | 0.16 | n/a | -6.2e-04 | n/a | 0.047 |
| foundry_00018 | prior | dull: predictable by the cheap family | 8.6e-04 | n/a | 0.96 | 1.00 | 7.27 | 47.7 | 0.00 | n/a | n/a | 5.89 | 5.87 | 5.3e-04 | n/a | 0.097 | n/a | -0.005 | n/a | 0.047 |
| foundry_00019 | prior | dull: predictable by the cheap family | 0.007 | n/a | 0.94 | 1.00 | 1.48 | 0.14 | 0.37 | 24.4 | n/a | 9.04 | 8.49 | 0.026 | n/a | 0.021 | n/a | -0.015 | n/a | 0.048 |
| foundry_00020 | prior | dull: predictable by the cheap family | 0.003 | n/a | 0.90 | 1.00 | 0.008 | 6.2e-04 | 0.00 | n/a | n/a | 5.66 | 5.51 | 4.1e-05 | n/a | 0.18 | n/a | 0.001 | n/a | 0.047 |
| foundry_00021 | prior | dull: predictable by the cheap family | 0.002 | 0.018 | 0.99 | 1.00 | 2.15 | 17.7 | 24.0 | 2972 | 0.00 | 1.11 | 0.92 | 3.5e-05 | 0.15 | 0.87 | 1.01 | 0.002 | n/a | 0.047 |
| foundry_00023 | prior | dull: predictable by the cheap family | 0.026 | n/a | 0.45 | 0.98 | 1.43 | 0.005 | 0.00 | n/a | n/a | 3.71 | 3.69 | 0.002 | n/a | 0.001 | n/a | -0.085 | n/a | 0.047 |
| foundry_00025 | prior | dull: predictable by the cheap family | 0.001 | 0.015 | 1.00 | 1.00 | 0.64 | 9.49 | 24.0 | 18358 | 0.21 | 2.58 | 1.45 | 8.2e-04 | 0.58 | 0.11 | 0.97 | 8.5e-04 | n/a | 0.047 |
| foundry_00026 | prior | dull: predictable by the cheap family | 0.014 | 0.009 | 1.00 | 0.99 | 0.52 | 26.1 | 2.71 | 84.2 | 0.24 | 50.6 | 2.10 | 0.004 | 0.94 | 0.054 | 0.99 | -0.079 | n/a | 0.049 |
| foundry_00027 | prior | dull: little predictable | 0.23 | n/a | 0.12 | 0.98 | 65.6 | 3.5e-04 | 0.00 | n/a | n/a | 3.02 | 2.95 | -3.0e-08 | n/a | 0.012 | n/a | 0.39 | n/a | 0.046 |
| foundry_00028 | prior | dull: predictable by the cheap family | 3.3e-04 | 0.019 | 1.00 | 1.00 | 0.50 | 45.3 | 12.2 | 817 | 0.00 | 7.40 | 5.33 | 0.002 | 0.96 | 0.013 | 0.98 | -2.1e-04 | n/a | 0.048 |
| foundry_00029 | prior | dull: predictable by the cheap family | 4.6e-04 | n/a | 0.97 | 1.00 | 6.02 | 1.08 | 0.012 | 10.4 | n/a | 7.24 | 7.17 | 5.1e-04 | n/a | 0.17 | n/a | -0.005 | n/a | 0.047 |
| foundry_00030 | prior | dull: predictable by the cheap family | 0.004 | n/a | 0.98 | 1.00 | 0.20 | 0.74 | 0.00 | n/a | n/a | 3.09 | 2.78 | 1.6e-04 | n/a | 0.10 | n/a | 0.005 | n/a | 0.047 |
| foundry_00031 | prior | dull: the hidden part has no weight | 9.6e-04 | 0.083 | 1.00 | 1.00 | 66.5 | 44.7 | 5.12 | 181 | 0.16 | 9.62 | 8.29 | 1.3e-04 | 0.042 | 0.60 | 0.93 | 0.001 | n/a | 0.047 |
| foundry128_04470 | size | exam-worthy + reading-worthy + actions | 0.39 | 0.15 | 1.00 | 0.60 | 0.84 | 191 | 71.6 | 25.5 | 0.35 | 1.57 | 0.005 | 3.2e-05 | 0.11 | 0.81 | 0.85 | 0.14 | n/a | 1.06 |
| foundry128_04186 | size | exam-worthy + reading-worthy + actions | 0.38 | 0.61 | 0.98 | 0.58 | 0.81 | 9.26 | 37.5 | 20.5 | 0.87 | 3.89 | 0.13 | 5.6e-05 | 0.82 | 0.065 | 0.48 | -0.24 | n/a | 0.20 |
| foundry128_00262 | size | exam-worthy + reading-worthy + actions | 0.45 | 0.54 | 1.00 | 0.57 | 0.82 | 294 | 46.3 | 22.3 | 0.84 | 1.02 | 2.6e-04 | 4.4e-05 | 0.36 | 0.34 | 0.44 | -0.17 | n/a | 0.19 |
| foundry128_07567 | size | exam-worthy + actions | 0.44 | 0.71 | 0.99 | 0.54 | 0.97 | 115 | 44.1 | 11.1 | 0.20 | 2.73 | 0.055 | 5.9e-05 | 0.22 | 0.14 | 0.35 | -7.2e-04 | n/a | 0.19 |
| foundry128_06845 | size | exam-worthy + actions | 0.31 | 0.89 | 1.00 | 0.73 | 1.05 | 31.5 | 48.4 | 14.4 | 0.069 | 2.25 | 0.023 | -3.2e-06 | 0.075 | 0.13 | 0.070 | -0.28 | n/a | 0.19 |
| foundry128_01672 | size | exam-worthy + reading-worthy + actions | 0.28 | 0.41 | 1.00 | 0.75 | 0.93 | 124 | 14.9 | 36.9 | 0.89 | 7.00 | 0.12 | 2.6e-06 | 0.11 | 0.11 | 0.65 | -0.25 | n/a | 0.19 |
| foundry128_03078 | size | exam-worthy + reading-worthy + actions | 0.31 | 0.77 | 1.00 | 0.74 | 0.84 | 32.1 | 52.5 | 37.5 | 0.72 | 4.45 | 0.070 | 3.0e-04 | 0.78 | 0.080 | 0.27 | -0.13 | n/a | 0.19 |
| vortex128 | size | exam-worthy + actions | 0.15 | 0.26 | 0.91 | 0.32 | 0.11 | 0.014 | 31.7 | 43.9 | 0.90 | 6.16 | 0.62 | 0.059 | 0.80 | 0.16 | 0.73 | -0.041 | n/a | 14.2 |
