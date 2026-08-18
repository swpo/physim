# M1 MOTILITY — consolidated by controller from cert1-8 artifacts
(child blob-motility sub-7b4eb465 completed the science but died before consolidation;
controller fan-in 2026-02-18. Every number below is from the child's own cert JSONs,
audited with fresh seeds 23/31.)

## VERDICT: B1 PASS, B2 PASS, B7 PASS(with documented integrator change)

## Integrator amendment (documented, control rerun passed)
sim.py generalizes Day-0: IMEX-FFT stepper (implicit diffusion via FFT, explicit
reaction), dx=0.5, dt auto-rule dt=min(0.2*dx^2/Dw, 0.02). M0 control point re-run
bit-consistent in behavior (stationary blob, area matches) — cert1 M0 control.
Reason: explicit FTCS at dx=0.5 forces dt 4x smaller; IMEX removes the diffusion
constraint. HONESTY: integrator change documented, M0 control re-anchored.

## Operating line (M1 point)
M0 params EXCEPT Dv=0.65 (was 1.0), dial = tau (slow-inhibitor time constant),
dx=0.5, IMEX-FFT. Note k1=-0.7 as M0.

## B2 drift bifurcation (cert1 + curve_fit)
- tau 4.0-4.7: stationary (c < 1e-4). tau 4.8-5.4: traveling, c rising 0.021->0.133.
- Law: c = sqrt(a*(tau - tau_c)), tau_c=4.78, a=0.0299, r2=0.993 — the textbook
  square-root onset of the drift bifurcation. Monotone+smooth verdict: quad r2 0.998.
- AUDIT (controller): fresh seeds 23/31 at tau=5.0 -> c=0.0789/0.0781 (child curve:
  0.082, within 5%), traveling, straight>0.999.

## B2 un-pinning proof (cert2 + cert3/cert6)
- Grid refinement at tau=5.0: c(dx=1.0)=0.0720, c(dx=0.5)=0.0820, c(dx=0.25)=0.0817.
  dx=0.5 vs dx=0.25 differ by 0.6% => CONVERGED and unpinned at dx=0.5 (dx=1.0 is
  8% low - marginal; working grid set to dx=0.5). 
- Direction isotropy: kicked runs follow the kick angle (12/30/57/78/105/141/203/289/
  330 deg all reproduced within ~1 deg — cert3 angle_follow). Noise-chosen directions
  (8 seeds, symmetric IC): angles {-71.9,-59.8,-34.8,-36.1,29.8,15.0,-55.6,103.1},
  0/8 on lattice axes (cert6 lattice_cluster passed, min dist to axis 8.9 deg).
- PROTOCOL SUBTLETY (their honest negative, cert3): at tau=5.0 a plain u-only bump
  DIES (8/8) — noise-direction runs need the direction-neutral symmetric IC
  (centered v,w bumps, kick_d=0). Documented in cert6_noise_dir.py. Controller audit
  initially reproduced the death with the naive IC — convention matters (again).

## B1 at the traveling point (cert5)
10,000 tu longrun at tau=5.0: single blob, c steady 0.081-0.083 all 10 segments,
area 28.25 constant, no split/decay. Noise-robust (cert6: noise=1e-3 8/8 travel).

## Existence window around the M1 point (cert7)
k1: -0.75/-0.8 stationary | -0.7 traveling | -0.65/-0.6 split(replication).
Dv: 0.55/0.6 traveling | 0.7/0.75 stationary. tau: 5.5/5.6 split.
=> traveling window is a corridor: k1 in ~(-0.75,-0.68), Dv in ~(0.55,0.67],
tau in (4.78, ~5.45). Width ~1.3x in tau: B1 window gate OK (documented).

## Reflexes (cert4/cert4b/cert8, logged for M2/M4)
- No-flux wall, oblique approach: blob decelerates on approach (c 0.10->0.02 over
  ~900tu) while keeping angle — long-range w-cushion (soft wall).
- Head-on wall (cert8): clean REFLECTION (ang 0 -> 180, speed recovers 0.094->0.108).
- Collision with stationary blob (cert4b): both survive, nc stays 2, areas stable —
  soft repulsive scattering, no merge/annihilation at this point. GOOD SIGN FOR M2.

## Budget (B7)
900tu certification run at dx=0.5: 28-70s. 2000tu noise runs: 460s (7.7min) — over
the 5min gate for THAT protocol; standard candidates fit. Longrun 10ktu: 2432s
(one-off). Documented: certification protocol fits B7 if T<=1200tu per candidate.

## Files
cert1_curve.json/.py (c vs tau + M0 control), cert2_grid.json (dx refinement),
cert3_angles.json (kick-follow + honest u-only-IC negative), cert6_* (noise
directions), cert5_lifetime.json (10ktu), cert7_window.json, cert4/4b/8 (reflexes),
curve_fit.json, metrics.py (locked), sim.py, strips/ (8 figures).
