### Conditions (focus view, pooled over the 8 seeds and 8, 16, 32 ticks)

| condition | number | one-sided 90% bounds of the per-seed contrast (>= 0 means it holds) | at the point estimate | reading |
|---|---|---|---|---|
| C1_main_Gstar_all_states_le_0.7 | closed 0.482 | mean +2.169, lower +0.896, upper +3.442 | holds | holds clearly |
| C2_main_Gstar_heaviest_left_out_le_0.7 | closed 0.664 | mean +0.199, lower -0.633, upper +1.032 | holds | close |
| C3_control_Gstar_ge_0.7 | closed 0.784 | mean +0.430, lower -0.170, upper +1.030 | holds | close |
| C4_main_H_ge_0.7 | closed 0.599 | mean -1.005, lower -2.095, upper +0.085 | fails | close |
| C5_main_stand_in_share_ge_0.10 | share -0.087 | mean -0.215, lower -0.288, upper -0.143 | fails | fails clearly; depends on A (in no verdict here) |

Verdict: **CLOSE CALL**; the plan's rule at the point estimates: **NO-GO**.

### Per seed, main arm (focus view, share of the public-to-oracle gap closed over 8, 16, 32 ticks)

| seed | rho, D_X, a0 (pilot) | items | heaviest state's share of the gap | G* is | G2 | G3 | A_act | G* | G*, heaviest out | H | H, heaviest out |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | 0.0200, 0.500, 0.0300 | 28 | 0.51 | A_act | +0.18 | +0.16 | +0.23 | +0.23 | +0.38 | +0.28 | +0.48 |
| 32 | 0.0200, 0.500, 0.0300 | 32 | 0.49 | A_act | +0.21 | +0.16 | +0.50 | +0.50 | +0.87 | +0.53 | +0.96 |
| 33 | 0.0200, 0.500, 0.0300 | 24 | 0.60 | A_act | +0.06 | +0.07 | +0.51 | +0.51 | +0.98 | +0.48 | +0.95 |
| 34 | 0.0200, 0.500, 0.0300 | 32 | 0.30 | A_act | +0.50 | +0.30 | +0.54 | +0.54 | +0.69 | +0.67 | +0.89 |
| 35 | 0.0200, 0.500, 0.0300 | 32 | 0.29 | A_act | +0.24 | +0.21 | +0.29 | +0.29 | +0.36 | +0.60 | +0.50 |
| 36 | 0.0200, 0.500, 0.0300 | 24 | 0.51 | A_act | +0.38 | -0.30 | +0.90 | +0.90 | +0.80 | +0.98 | +0.97 |
| 37 | 0.0200, 0.500, 0.0300 | 28 | 0.26 | A_act | +0.59 | +0.32 | +0.78 | +0.78 | +0.81 | +0.96 | +0.96 |
| 38 | 0.0200, 0.500, 0.0300 | 28 | 0.64 | A_act | +0.23 | +0.24 | +0.37 | +0.37 | +0.89 | +0.42 | +1.03 |
| **pooled** | | | | | **+0.29** | **+0.17** | **+0.48** | **+0.48** | **+0.66** | **+0.60** | **+0.79** |
| median of seeds | | | | | +0.24 | +0.19 | +0.51 | +0.51 | +0.80 | +0.57 | +0.96 |
| leave-one-seed-out range | | | | | +0.25 to +0.32 | +0.15 to +0.21 | +0.44 to +0.53 | +0.44 to +0.53 | +0.63 to +0.77 | +0.55 to +0.64 | +0.76 to +0.89 |
| bootstrap over seeds, 5%-95% | | | | | +0.20 to +0.38 | +0.08 to +0.24 | +0.38 to +0.62 | +0.38 to +0.62 | +0.52 to +0.82 | +0.48 to +0.72 | +0.65 to +0.95 |

### Per horizon, main arm (pooled over seeds; share of the gap at that horizon closed)

| view | start states | policy | 4 ticks | 8 | 16 | 32 | pooled 8-32 |
|---|---|---|---|---|---|---|---|
| focus | all | G2 | +0.97 | +0.88 | +0.76 | -0.07 | +0.29 |
| focus | all | G3 | +0.91 | +0.90 | +0.70 | -0.26 | +0.17 |
| focus | all | A_act | +0.91 | +0.88 | +0.77 | +0.25 | +0.48 |
| focus | all | G* | +0.91 | +0.88 | +0.77 | +0.25 | +0.48 |
| focus | all | H | +0.94 | +0.96 | +0.95 | +0.36 | +0.60 |
| focus | all | G1 | +0.07 | +0.40 | +0.35 | -0.35 | -0.06 |
| focus | all | G4 | +0.92 | +0.89 | +0.74 | -0.77 | -0.13 |
| focus | all | pub0 | +0.31 | -0.16 | -2.08 | -1.05 | -1.12 |
| focus | heaviest out | G2 | +0.97 | +0.89 | +0.77 | -0.16 | +0.44 |
| focus | heaviest out | G3 | +0.90 | +0.90 | +0.70 | -0.52 | +0.28 |
| focus | heaviest out | A_act | +0.90 | +0.87 | +0.77 | +0.43 | +0.66 |
| focus | heaviest out | G* | +0.90 | +0.87 | +0.77 | +0.43 | +0.66 |
| focus | heaviest out | H | +0.94 | +0.95 | +0.94 | +0.55 | +0.79 |
| focus | heaviest out | G1 | +0.06 | +0.41 | +0.30 | -1.00 | -0.18 |
| focus | heaviest out | G4 | +0.92 | +0.89 | +0.73 | -2.02 | -0.30 |
| focus | heaviest out | pub0 | +0.30 | -0.16 | -2.07 | -2.70 | -1.79 |
| cell-resolved list | all | G2 | +0.98 | +0.89 | +0.75 | -0.12 | +0.24 |
| cell-resolved list | all | G3 | +0.91 | +0.91 | +0.67 | -0.26 | +0.14 |
| cell-resolved list | all | A_act | +0.93 | +0.89 | +0.80 | +0.29 | +0.50 |
| cell-resolved list | all | G* | +0.96 | +0.89 | +0.82 | +0.28 | +0.50 |
| cell-resolved list | all | H | +0.95 | +0.97 | +0.96 | +0.40 | +0.62 |
| cell-resolved list | heaviest out | G2 | +0.98 | +0.90 | +0.76 | -0.26 | +0.37 |
| cell-resolved list | heaviest out | G3 | +0.91 | +0.91 | +0.67 | -0.52 | +0.23 |
| cell-resolved list | heaviest out | A_act | +0.92 | +0.88 | +0.79 | +0.47 | +0.68 |
| cell-resolved list | heaviest out | G* | +0.96 | +0.88 | +0.82 | +0.43 | +0.67 |
| cell-resolved list | heaviest out | H | +0.96 | +0.96 | +0.95 | +0.62 | +0.82 |

Share of the pooled gap at 8, 16, 32 ticks (focus view): 0.18, 0.22, 0.59.

### Per seed and horizon, main arm (focus view, all start states)

| seed | G* 8 | G* 16 | G* 32 | A_act 8 | A_act 16 | A_act 32 | H 8 | H 16 | H 32 |
|---|---|---|---|---|---|---|---|---|---|
| 31 | +0.89 | +0.76 | +0.03 | +0.89 | +0.76 | +0.03 | +0.89 | +0.97 | +0.06 |
| 32 | +0.95 | +0.85 | +0.35 | +0.95 | +0.85 | +0.35 | +1.00 | +0.93 | +0.36 |
| 33 | +0.94 | +0.99 | +0.15 | +0.94 | +0.99 | +0.15 | +1.00 | +0.97 | +0.08 |
| 34 | +0.82 | +0.55 | +0.33 | +0.82 | +0.55 | +0.33 | +1.01 | +1.00 | +0.16 |
| 35 | +0.88 | +0.85 | +0.04 | +0.88 | +0.85 | +0.04 | +0.78 | +0.80 | +0.52 |
| 36 | +0.97 | +0.73 | +0.94 | +0.97 | +0.73 | +0.94 | +1.01 | +0.99 | +0.97 |
| 37 | +0.83 | +0.70 | +0.86 | +0.83 | +0.70 | +0.86 | +0.97 | +0.96 | +0.96 |
| 38 | +0.91 | +0.90 | +0.15 | +0.91 | +0.90 | +0.15 | +1.00 | +1.02 | +0.18 |

### The history-only stand-in, main arm (focus view)

| items | share s = (L(P0s) - L(Cs)) / (L(K) - L(Cs)) | state-given gap | kept | skill of Cs, of the oracle's |
|---|---|---|---|---|
| declared mix, 8-32 ticks | -0.087 | 0.153 | -0.36 | 0.628 |
| aimed only | -0.075 | 0.185 | -0.26 | 0.625 |
| blind only | -0.160 | 0.048 | -2.02 | 0.611 |
| none only | -0.093 | 0.047 | -1.32 | 0.664 |
| mix, 8 ticks | 0.036 | 0.071 | +0.42 | 0.834 |
| mix, 16 ticks | 0.036 | 0.093 | +0.30 | 0.772 |
| mix, 32 ticks | -1.255 | 0.325 | -0.79 | 0.204 |

s per seed: -0.015, -0.023, -0.208, -0.015, 0.043, -1.199, 0.045, -0.160; median -0.019; leave-one-seed-out -0.117 to -0.040; bootstrap over seeds 5%-95% -0.217 to -0.008.

### Per seed, control arm (focus view, share of the public-to-oracle gap closed over 8, 16, 32 ticks)

| seed | rho, D_X, a0 (pilot) | items | heaviest state's share of the gap | G* is | G2 | G3 | A_act | G* | G*, heaviest out | H | H, heaviest out |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | 0.0200, 0.500, 0.0300 | 28 | 0.22 | A_act | +0.49 | +0.40 | +0.81 | +0.81 | +0.83 | +0.96 | +0.97 |
| 32 | 0.0200, 0.500, 0.0300 | 32 | 0.26 | A_act | +0.44 | +0.44 | +0.87 | +0.87 | +0.82 | +0.96 | +0.94 |
| 33 | 0.0200, 0.500, 0.0300 | 24 | 0.23 | A_act | +0.66 | +0.05 | +0.95 | +0.95 | +0.97 | +0.96 | +0.97 |
| 34 | 0.0200, 0.500, 0.0300 | 32 | 0.25 | A_act | +0.63 | +0.48 | +0.87 | +0.87 | +0.88 | +0.85 | +0.98 |
| 35 | 0.0200, 0.500, 0.0300 | 32 | 0.22 | A_act | +0.71 | +0.70 | +0.82 | +0.82 | +0.79 | +0.97 | +0.99 |
| 36 | 0.0200, 0.500, 0.0300 | 24 | 0.50 | A_act | +0.49 | +0.09 | +0.91 | +0.91 | +0.83 | +0.97 | +0.93 |
| 37 | 0.0200, 0.500, 0.0300 | 28 | 0.20 | G3 | +0.61 | +0.38 | +0.75 | +0.38 | +0.41 | +0.98 | +0.96 |
| 38 | 0.0200, 0.500, 0.0300 | 28 | 0.35 | A_act | +0.54 | +0.51 | +0.88 | +0.88 | +0.87 | +1.03 | +1.10 |
| **pooled** | | | | | **+0.58** | **+0.38** | **+0.85** | **+0.78** | **+0.77** | **+0.96** | **+0.98** |
| median of seeds | | | | | +0.58 | +0.42 | +0.87 | +0.87 | +0.83 | +0.97 | +0.97 |
| leave-one-seed-out range | | | | | +0.56 to +0.60 | +0.34 to +0.43 | +0.84 to +0.88 | +0.76 to +0.88 | +0.74 to +0.86 | +0.95 to +0.97 | +0.96 to +0.98 |
| bootstrap over seeds, 5%-95% | | | | | +0.53 to +0.63 | +0.26 to +0.49 | +0.81 to +0.89 | +0.65 to +0.89 | +0.64 to +0.88 | +0.92 to +0.98 | +0.96 to +1.00 |

### Per horizon, control arm (pooled over seeds; share of the gap at that horizon closed)

| view | start states | policy | 4 ticks | 8 | 16 | 32 | pooled 8-32 |
|---|---|---|---|---|---|---|---|
| focus | all | G2 | +0.98 | +0.88 | +0.72 | +0.01 | +0.58 |
| focus | all | G3 | +0.91 | +0.91 | +0.67 | -0.66 | +0.38 |
| focus | all | A_act | +0.93 | +0.90 | +0.81 | +0.85 | +0.85 |
| focus | all | G* | +0.94 | +0.92 | +0.83 | +0.55 | +0.78 |
| focus | all | H | +0.96 | +0.98 | +0.95 | +0.93 | +0.96 |
| focus | all | G1 | +0.07 | +0.40 | +0.30 | -0.53 | +0.11 |
| focus | all | G4 | +0.93 | +0.89 | +0.71 | -0.63 | +0.40 |
| focus | all | pub0 | +0.31 | -0.21 | -2.62 | -6.44 | -2.86 |
| focus | heaviest out | G2 | +0.99 | +0.89 | +0.72 | -0.27 | +0.62 |
| focus | heaviest out | G3 | +0.92 | +0.91 | +0.66 | -1.16 | +0.45 |
| focus | heaviest out | A_act | +0.93 | +0.91 | +0.81 | +0.75 | +0.84 |
| focus | heaviest out | G* | +0.94 | +0.93 | +0.83 | +0.23 | +0.77 |
| focus | heaviest out | H | +0.96 | +0.98 | +0.95 | +1.02 | +0.98 |
| focus | heaviest out | G1 | +0.10 | +0.43 | +0.21 | -1.16 | +0.07 |
| focus | heaviest out | G4 | +0.93 | +0.89 | +0.70 | -1.03 | +0.48 |
| focus | heaviest out | pub0 | +0.32 | -0.20 | -2.93 | -12.58 | -3.45 |
| cell-resolved list | all | G2 | +0.98 | +0.89 | +0.76 | -0.21 | +0.49 |
| cell-resolved list | all | G3 | +0.91 | +0.91 | +0.60 | -1.05 | +0.18 |
| cell-resolved list | all | A_act | +0.91 | +0.90 | +0.86 | +0.78 | +0.84 |
| cell-resolved list | all | G* | +0.96 | +0.89 | +0.85 | +0.67 | +0.81 |
| cell-resolved list | all | H | +0.99 | +0.99 | +0.99 | +0.96 | +0.98 |
| cell-resolved list | heaviest out | G2 | +0.98 | +0.88 | +0.74 | -0.90 | +0.51 |
| cell-resolved list | heaviest out | G3 | +0.92 | +0.92 | +0.57 | -2.06 | +0.25 |
| cell-resolved list | heaviest out | A_act | +0.91 | +0.89 | +0.84 | +0.52 | +0.81 |
| cell-resolved list | heaviest out | G* | +0.96 | +0.89 | +0.84 | +0.29 | +0.76 |
| cell-resolved list | heaviest out | H | +0.98 | +0.98 | +0.98 | +0.84 | +0.96 |

Share of the pooled gap at 8, 16, 32 ticks (focus view): 0.34, 0.38, 0.28.

### Per seed and horizon, control arm (focus view, all start states)

| seed | G* 8 | G* 16 | G* 32 | A_act 8 | A_act 16 | A_act 32 | H 8 | H 16 | H 32 |
|---|---|---|---|---|---|---|---|---|---|
| 31 | +0.90 | +0.78 | +0.75 | +0.90 | +0.78 | +0.75 | +0.89 | +0.97 | +1.02 |
| 32 | +0.94 | +0.84 | +0.86 | +0.94 | +0.84 | +0.86 | +1.00 | +0.87 | +1.00 |
| 33 | +0.93 | +0.98 | +0.90 | +0.93 | +0.98 | +0.90 | +1.01 | +0.97 | +0.71 |
| 34 | +0.92 | +0.85 | +0.82 | +0.92 | +0.85 | +0.82 | +0.98 | +0.97 | +0.36 |
| 35 | +0.89 | +0.89 | +0.16 | +0.89 | +0.89 | +0.16 | +0.95 | +0.99 | +0.93 |
| 36 | +0.95 | +0.69 | +0.97 | +0.95 | +0.69 | +0.97 | +0.99 | +0.88 | +0.99 |
| 37 | +0.95 | +0.76 | -2.53 | +0.85 | +0.65 | +0.84 | +0.96 | +0.94 | +1.17 |
| 38 | +0.90 | +0.86 | +0.88 | +0.90 | +0.86 | +0.88 | +1.02 | +1.02 | +1.06 |

### The history-only stand-in, control arm (focus view)

| items | share s = (L(P0s) - L(Cs)) / (L(K) - L(Cs)) | state-given gap | kept | skill of Cs, of the oracle's |
|---|---|---|---|---|
| declared mix, 8-32 ticks | 0.035 | 0.074 | +0.37 | 0.777 |
| aimed only | 0.045 | 0.096 | +0.37 | 0.780 |
| blind only | -0.019 | 0.001 | -17.55 | 0.753 |
| none only | 0.018 | -0.001 | -9.55 | 0.780 |
| mix, 8 ticks | 0.042 | 0.069 | +0.52 | 0.855 |
| mix, 16 ticks | 0.046 | 0.082 | +0.45 | 0.804 |
| mix, 32 ticks | 0.008 | 0.070 | +0.07 | 0.654 |

s per seed: 0.032, 0.043, 0.057, 0.033, 0.065, -0.087, 0.052, 0.022; median 0.038; leave-one-seed-out 0.030 to 0.044; bootstrap over seeds 5%-95% 0.014 to 0.049.

### Scan C: the ranges of rho, D_X, a0 (screen gap, focus view, 8-32 ticks; 16 members)

| parameter | value | gap without input | gap, blind input | gap, aimed input | states with a focus cell | admissible |
|---|---|---|---|---|---|---|
| DX | 0.05 | 0.005 | 0.009 | 0.165 | 15 | yes |
| DX | 0.1 | 0.006 | 0.008 | 0.167 | 15 | yes |
| DX | 0.2 | 0.006 | 0.008 | 0.171 | 15 | yes |
| DX | 0.35 | 0.006 | 0.009 | 0.179 | 15 | yes |
| DX | 0.5 | 0.130 | 0.142 | 0.364 | 15 | no |
| a0 | 0.02 | 0.297 | 0.304 | 0.495 | 15 | no |
| a0 | 0.025 | 0.213 | 0.223 | 0.420 | 15 | no |
| a0 | 0.03 | 0.130 | 0.142 | 0.364 | 15 | no |
| a0 | 0.04 | 0.107 | 0.117 | 0.228 | 15 | no |
| a0 | 0.05 | 0.093 | 0.101 | 0.219 | 15 | no |
| rho | 0.005 | -0.002 | 0.025 | 0.411 | 15 | yes |
| rho | 0.01 | -0.004 | 0.017 | 0.305 | 15 | yes |
| rho | 0.02 | 0.130 | 0.142 | 0.364 | 15 | no |
| rho | 0.04 | n/a | n/a | n/a | 0 | no |
| rho | 0.08 | n/a | n/a | n/a | 0 | no |

Ranges: DX 0.5 to 0.5 (scan failed: the centre alone); a0 0.03 to 0.03 (scan failed: the centre alone); rho 0.02 to 0.02 (scan failed: the centre alone).

### Scan V: the hidden parameter set of the public law (8 members; headroom = state-given loss of the default-parameter law)

| parameter | family | viable at 0.8, 0.9, 1.1, 1.2 x default | headroom at those | box (x default) | headroom (smaller edge) | eligible |
|---|---|---|---|---|---|---|
| DK | transport | yes, yes, yes, yes | -0.003, -0.003, 0.007, 0.005 | 0.8 to 1.2 | -0.003 | no |
| DL | transport | yes, yes, yes, yes | 0.013, 0.006, 0.005, 0.009 | 0.8 to 1.2 | 0.009 | no |
| DS | transport | no, yes, yes, yes | 0.364, 0.046, 0.066, 0.230 | 0.9 to 1.2 | 0.046 | yes |
| Dp | transport | yes, yes, yes, yes | 0.438, 0.150, 0.098, 0.354 | 0.8 to 1.2 | 0.354 | yes |
| F | metabolism | no, no, yes, no | n/a, 0.360, 0.964, n/a | none | n/a | no |
| a | phase | yes, yes, no, no | 0.220, 0.014, 0.124, n/a | none | n/a | no |
| b | metabolism | no, yes, no, no | n/a, 0.273, 0.395, n/a | none | n/a | no |
| c | metabolism | yes, yes, yes, no | 0.200, 0.034, 0.028, 0.162 | 0.8 to 1.1 | 0.028 | yes |
| chi | link | yes, yes, yes, yes | 0.112, 0.026, 0.017, 0.066 | 0.8 to 1.2 | 0.066 | yes |
| dK | decay | yes, yes, yes, yes | 1.106, 0.286, 0.461, 0.821 | 0.8 to 1.2 | 0.821 | yes |
| dL | decay | no, yes, no, no | n/a, 0.737, 0.575, n/a | none | n/a | no |
| r | phase | yes, yes, yes, yes | 0.292, 0.083, 0.078, 0.161 | 0.8 to 1.2 | 0.161 | yes |
| th | phase | no, no, no, no | n/a, 0.851, 0.779, n/a | none | n/a | no |

Noise floor (the default law against itself): 0.003 +- 0.007. Hidden set: dK in 0.016 to 0.024 (decay, headroom 0.821), Dp in 0.08 to 0.12 (transport, headroom 0.354), r in 0.16 to 0.24 (phase, headroom 0.161), chi in 1.6 to 2.4 (link, headroom 0.066).
