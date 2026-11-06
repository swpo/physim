# VW-0 estimator calibration on linear-Gaussian worlds

N = 40000 trajectories per program (3 programs: empty + 2 random admissible), oracle 8000 x 16 fresh-noise branches; 8-fold standard errors. z = (estimate - closed form)/SE over all horizons 1-16 and pasts 0-16.

| world | n0 | gap max abs z | gap rms z | Ve max abs z | Vu max abs z | ceiling max abs z | block-gap max abs z | leak info max rel err | leak dims equal | response max abs err | sing. value max rel err | capacity rel err | obs rate abs err (bits) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ring | 24 | 2.04 | 1.04 | 2.30 | 1.77 | 1.83 | 0.84 | 0.0005 | True | 5.0e-16 | 0.0064 | 0.0017 | 0.0173 |
| ring-conserved | 24 | 3.48 | 1.60 | 1.83 | 1.50 | 2.40 | 1.27 | 0.0012 | True | 7.2e-16 | 0.0091 | 0.0044 | 0.0091 |
| random | 16 | 1.87 | 0.94 | 1.55 | 0.60 | 1.63 | 0.58 | 0.0013 | True | 1.4e-15 | 0.0062 | 0.0025 | 0.0115 |
| concat(ring,random) | 40 | 1.52 | 0.83 | 1.85 | 1.33 | 1.77 | 0.53 | 0.0010 | True | 8.7e-16 | 0.0076 | 0.0003 | 0.0087 |
| stack(ring) | 24 | 2.35 | 1.20 | 1.91 | 1.93 | 2.44 | 1.29 | 0.0002 | True | 5.6e-16 | 0.0077 | 0.0024 | 0.0119 |
| refine(ring,eta=0.0) | 48 | 1.36 | 0.80 | 1.32 | 1.26 | 1.17 | 0.57 | 0.0003 | True | 4.4e-16 | 0.0096 | 0.0015 | 0.0183 |
| refine(ring,eta=0.3) | 48 | 1.74 | 0.98 | 2.05 | 1.46 | 1.72 | 0.59 | 0.0007 | True | 6.1e-16 | 0.0094 | 0.0013 | 0.0202 |

## ring world (n0 = 24, n_obs = 6): closure, estimate +- SE / closed form

| tau | Vu | Ve(p=1) | Ve(p=16) | gap(p=0) nats | gap(p=1) nats | gap(p=16) nats | gap(p=inf) nats | ceiling(p=16) |
|---|---|---|---|---|---|---|---|---|
| 1 | 2.405+-0.003 / 2.400 | 2.655 / 2.653 | 2.629+-0.005 / 2.627 | 4.940 / 4.942 | 0.297+-0.005 / 0.300 | 0.268+-0.005 / 0.271 | 0.271 | 0.9799 / 0.9797 |
| 2 | 4.040+-0.003 / 4.037 | 4.297 / 4.296 | 4.270+-0.006 / 4.270 | 3.387 / 3.386 | 0.187+-0.005 / 0.187 | 0.168+-0.005 / 0.169 | 0.169 | 0.9758 / 0.9756 |
| 4 | 6.493+-0.005 / 6.488 | 6.693 / 6.708 | 6.670+-0.009 / 6.687 | 1.977 / 1.984 | 0.092+-0.005 / 0.101 | 0.082+-0.005 / 0.091 | 0.091 | 0.9748 / 0.9720 |
| 8 | 9.488+-0.009 / 9.487 | 9.603 / 9.619 | 9.591+-0.016 / 9.607 | 0.892 / 0.902 | 0.037+-0.006 / 0.042 | 0.033+-0.005 / 0.038 | 0.038 | 0.9743 / 0.9706 |
| 16 | 12.097+-0.012 / 12.089 | 12.112 / 12.130 | 12.109+-0.022 / 12.126 | 0.259 / 0.265 | 0.005+-0.006 / 0.010 | 0.004+-0.006 / 0.009 | 0.009 | 0.9941 / 0.9746 |

## Atay one-step split (nats): estimate / closed form (p_max = 16; closed form p = inf in brackets)

| world | leak | memory | residual |
|---|---|---|---|
| ring | 0.2967 / 0.3005 | 0.0288 / 0.0292 [0.0292] | 0.2679 / 0.2713 [0.2713] |
| ring-conserved | 0.2977 / 0.2938 | 0.0337 / 0.0336 [0.0336] | 0.2640 / 0.2602 [0.2602] |
| random | 1.8976 / 1.8971 | 0.7026 / 0.7072 [0.7072] | 1.1951 / 1.1899 [1.1899] |
| concat(ring,random) | 2.2000 / 2.1975 | 0.7323 / 0.7364 [0.7364] | 1.4677 / 1.4612 [1.4612] |
| stack(ring) | 0.0836 / 0.0943 | 0.0061 / 0.0062 [0.0062] | 0.0775 / 0.0881 [0.0881] |
| refine(ring,eta=0.0) | 0.2921 / 0.3005 | 0.0295 / 0.0292 [0.0292] | 0.2625 / 0.2713 [0.2713] |
| refine(ring,eta=0.3) | 0.5470 / 0.5555 | 0.0130 / 0.0127 [0.0127] | 0.5341 / 0.5428 [0.5428] |

## Leak, input and observation capacity: estimate / closed form

| world | leak info p=1 (nats) | leak info p=16 | leak dim p=16 / rank | excitable dim/tick | visible dim | capacity bound (bits/tick) | atom SNR median | atoms visible | obs rate p=16 (bits/tick) | obs channel bound (bits) |
|---|---|---|---|---|---|---|---|---|---|---|
| ring | 11.852 / 11.850 | 12.193 / 12.189 | 6/24 / 6/24 | 1 | 5 / 5 | 4.691 / 4.699 | 3.481 / 3.516 | 0.870 / 0.870 | 10.341 / 10.357 | 17.474 / 17.464 |
| ring-conserved | 11.730 / 11.744 | 12.088 / 12.096 | 5/23 / 5/23 | 1 | 5 / 5 | 4.964 / 4.943 | 3.881 / 3.855 | 0.870 / 0.870 | 8.671 / 8.680 | 21.125 / 21.105 |
| random | 4.817 / 4.824 | 8.045 / 8.045 | 8/16 / 8/16 | 3 | 1 / 1 | 1.678 / 1.682 | 0.391 / 0.393 | 0.000 / 0.000 | 5.315 / 5.309 | 7.780 / 7.782 |
| concat(ring,random) | 16.664 / 16.673 | 20.215 / 20.234 | 14/40 / 14/40 | 4 | 12 / 12 | 8.030 / 8.027 | 3.510 / 3.516 | 0.941 / 0.941 | 15.674 / 15.666 | 25.252 / 25.246 |
| stack(ring) | 7.425 / 7.426 | 7.540 / 7.540 | 3/24 / 3/24 | 1 | 2 / 2 | 3.140 / 3.147 | 1.872 / 1.885 | 0.685 / 0.685 | 6.488 / 6.499 | 10.758 / 10.755 |
| refine(ring,eta=0.0) | 11.847 / 11.850 | 12.192 / 12.189 | 6/48 / 6/48 | 1 | 5 / 5 | 4.692 / 4.699 | 3.499 / 3.516 | 0.870 / 0.870 | 10.375 / 10.357 | 17.473 / 17.464 |
| refine(ring,eta=0.3) | 12.570 / 12.578 | 12.947 / 12.948 | 6/48 / 6/48 | 1 | 5 / 5 | 4.437 / 4.443 | 3.169 / 3.184 | 0.870 / 0.870 | 10.769 / 10.749 | 18.565 / 18.539 |

## Composition

- concat: closed-form gap(concat) - gap(ring) - gap(random), max over the table: 1.8e-15 nats (additive).
- exactly lumpable refinement (level -1, n = 48): gap minus base gap, max: 1.8e-15 nats (the refinement is invisible at level 1).
- leaky refinement (eta = 0.3): gap minus base gap at p = 16, tau = 1..16: 0.272, 0.287, 0.186, 0.069, 0.015 nats.
- commutation_refine(ring,eta=0.0)_T1: delta^2 estimate 0.0010 (MC bias removed 0.2698) / closed form 0.0000
- commutation_refine(ring,eta=0.0)_T4: delta^2 estimate -0.0022 (MC bias removed 0.4972) / closed form 0.0000
- commutation_refine(ring,eta=0.3)_T1: delta^2 estimate 0.2331 (MC bias removed 0.2698) / closed form 0.2304
- commutation_refine(ring,eta=0.3)_T4: delta^2 estimate 0.2027 (MC bias removed 0.5324) / closed form 0.2015

## Exam harness: Kalman reference (exact level-1 ceiling) and oracle, MSE estimate +- SE / closed form

| world | tau | persistence | Kalman | Kalman closed form | oracle | oracle closed form |
|---|---|---|---|---|---|---|
| ring | 1 | 2.946 | 2.630+-0.014 | 2.627 | 2.403 | 2.400 |
| ring | 2 | 5.022 | 4.277+-0.023 | 4.270 | 4.048 | 4.037 |
| ring | 4 | 8.402 | 6.660+-0.035 | 6.687 | 6.470 | 6.488 |
| ring | 8 | 13.566 | 9.607+-0.047 | 9.607 | 9.482 | 9.487 |
| ring | 16 | 19.696 | 12.172+-0.065 | 12.126 | 12.135 | 12.089 |
| random | 1 | 4.214 | 1.137+-0.022 | 1.140 | 0.642 | 0.643 |
| random | 2 | 7.545 | 1.524+-0.022 | 1.512 | 1.138 | 1.138 |
| random | 4 | 5.077 | 1.836+-0.016 | 1.824 | 1.675 | 1.649 |
| random | 8 | 6.679 | 2.245+-0.017 | 2.255 | 2.205 | 2.215 |
| random | 16 | 5.020 | 2.481+-0.020 | 2.484 | 2.473 | 2.477 |
