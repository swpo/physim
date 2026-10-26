# c41 review of 20261026T1020-c37-sh-delay-map-negative

Planted spot, N=128, L=80, b=2 (the only b where the spot exists; b=1.6 kills it at these r), dt=0.1.

Linear theory for the translation (Goldstone) mode a(t) dx u0 with the slaved filter b(t):
- `-kap v` form: da/dt = kap a - kap b, db/dt = (a - b)/tau -> eigenvalue kap - 1/tau: drift for kap*tau > 1.
- `kap (v - u)` (PYR=1) form: da/dt = kap (b - a) -> eigenvalue -(kap + 1/tau): always stable for kap > 0;
  drift needs kap < 0 with |kap|*tau > 1 (the destabilising sign of Gurevich & Friedrich's delayed term).

| form | kap | tau | kick | result (t) | file |
|---|---|---|---|---|---|
| -kap v, r=-0.2 | 0.2 | 10 | 0 | static to t~170, then drifts 0.11/t, 8.3 body lengths by t=500 | rerun/claimed_inh_k02_t10 (labkit, seed 11) |
| -kap v, r=-0.2 | 0.2 | 10 | 0.02 | drifts from t~125, 0.135/t, 9.9 body lengths | rerun/kick_inh_k02_t10 seeds 11,12 |
| -kap v, r=-0.2 | 0.2 | 2 | 0.02 | static to t=500 (kap*tau 0.4) | snap_m2.png |
| PYR, r=-0.4 | +0.6 | 10 | 0 / 0.02 | static (as claimed) | rerun/claimed_pyr_k06_t10, rerun/kick_pyr_kp06_t10 |
| PYR | +0.3 | 10 | 0.02 | static | snap_p1.png |
| PYR | -0.05 | 10 | 0.02 | static (|kap|tau 0.5) | snap_p2.png |
| PYR | -0.08 | 10 | 0.02 | static to t=800 (0.8) | snap_p5.png |
| PYR | -0.12 | 10 | 0.02 | drift starts t~600 (1.2) | snap_p6.png |
| PYR | -0.15 | 10 | 0.02 | steady drift 0.078-0.093/t, 11.1 body lengths by t=800 | rerun/kick_pyr_km015_t10 seeds 11,12 |
| PYR | -0.3 | 10 | 0.02 | drifts, splits at t~70-85, nucleates a hex patch that fills the box, then a rotating spiral/target wave | rerun/kick_pyr_km03_t10 seeds 11,12 |

The drift threshold in the PYR form lies between |kap| tau = 0.8 and 1.2, as the linear theory says (1).

m3/m4 (snap_m3/m4.png) use the default b=1.6: the planted spot dies at r=-0.2 with or without kick, so the map must have used b=2 (m5: b=2, no kick, drifts from t~170).
c37's own probe_m2.png, bottom row (n=1, max 1.88-1.91), shows the spot off-centre at t=375 and wrapping at the right edge at t=500: the drift is in the parent's image.
