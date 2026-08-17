# MORPHO COUNTER — search summary (2026-02-17)

## Verdict
**PASS (all 5 gates)** on the flagship point; the mechanism is real, emergent,
and robust in a finite but comfortable basin. It is a *self-oscillating
integer counter*: a Turing stripe ring whose own wavelength-error signal
drives a slow control field into a hysteresis loop around a forbidden
setpoint, so the stripe count n ticks 5 <-> 6 forever like a relaxation clock
that can only speak in integers.

## Mechanism (one paragraph)
Schnakenberg kinetics (a=0.1, b=0.9, Du=1, Dv=11) on a periodic ring (L=64,
ny=8 quasi-1D) form n stripes. A third field C multiplies reaction rate T(C)
= C^(2*sigma), so the intrinsic wavenumber is k_c(C) = k_c(1)*C^sigma while
diffusion stays fixed. On the ring, k is quantized (k_n = 2*pi*n/L) and each
integer branch n is *locally stable across a finite C interval* (Eckhaus-type
multistability => hysteresis). C evolves slowly by a purely local rule:
dC/dt = eps * gate * (k*^2 - S)/k*^2, where S = |grad w|^2 / w^2 is the local
squared wavenumber MEASURED from the pattern itself (band-passed u), and the
setpoint k*^2 is placed in the S-gap BETWEEN branches n=5 and n=6. Neither
rung satisfies the setpoint: on n=5, S < k*^2 so C rises until 5 loses
stability and a stripe inserts; on n=6, S > k*^2 so C falls until a stripe
zips out. Result: an autonomous integer limit cycle (period ~1000-1500 t)
computed by the micro physics — no scheduled events, no imposed clock.

## Hierarchy (layer -> variable -> timescale, flagship numbers)
| layer | variable | timescale | separation |
|---|---|---|---|
| L1 micro | u,v reaction-diffusion kinetics (pixel trace ACF) | tau1 ~ 9-15 t | — |
| L2 meso | requantization defect events: envelope pinch -> phase slip -> healing (envmin, mode amplitudes A5/A6) | tau2 ~ 80-135 t | tau2/tau1 ~ 6-12x |
| L3 macro | integer stripe count n(t): square-wave 5<->6; C(t) sawtooth slaved to it | tau3 ~ 1000-1700 t | tau3/tau2 ~ 10-20x |
Scale-separation product tau3/tau1 ~ 100-170x. All three variables are
directly measurable from fields (count = FFT mode / zero crossings; events =
envelope pinches; kinetics = any pixel).

## Flagship candidate (theory coordinates)
Dv=11 (band ratio k_hi/k_lo = 1.79), L=64 with rung pair (5,6),
kappa=0.5 (setpoint mid-gap), eps=3.2e-3 (drive gain), noise=2e-3,
sigma=1.0, Dc=10, dt=0.1, ny=8. kstar2 = 0.268 from seeded 2-point
calibration (S plateaus: n=5 -> 0.227, n=6 -> 0.309).
Runtime: ~6-9 s per 60k-tick probe on one core (G5 budget-real).
Backup passer: same point with eps=2.8e-3 (4/4 seeds).
More robust re-centred variant: kappa=0.45, eps=3.0e-3 (3/4 seeds at 60k,
10/12 jitter at 120k).

## Gate results
- **G1 HIERARCHY: PASS.** 3 layers; adjacent separations >= 5x on 4/4 seeds
  (sep12 = 7.4-10.3, sep23 = 11-14 at the flagship). Measured, not assumed:
  tau1 from pixel ACF, tau2 from locked event metric, tau3 from dwell stats.
- **G2 SIMPLE TOP: PASS.** compact_top_fit(model=switch) on n(t):
  r2 = 0.87-1.00, n_flips = 7-8 in 60k ticks (>= 6 required) on 4/4 seeds.
- **G3 COMPUTED NOT IMPOSED: PASS.** three response curves, all smooth and
  monotone: (a) period vs eps over 5 values 1.4e-3 -> 5.6e-3: T = 2518 ->
  470 t, T ~ 3.8/eps (the clock rate is the micro drive gain — nothing is
  scheduled); (b) duty cycle vs kappa over 5 values 0.3 -> 0.7: 0.28 -> 0.59
  monotone; (c) staircase jump position C(5->6) vs sigma over 5 values:
  1.131 -> 1.077 monotone, consistent with C_jump ~ (k_jump/k_c1)^(1/sigma).
- **G4 ROBUST: PASS (with an honestly mapped basin).** Flagship eps=3.2e-3:
  4/4 seeds. +-10% jitter on ALL searched params (Dv, kappa, eps, noise):
  4/6 at 60k, 5/6 rechecked at 120k; pooled with 12 extra draws: 13/18.
  Re-centred kappa=0.45 variant: 10/12 jitter at 120k. Failure mode is NOT
  mechanism loss (33/36 jitter draws still show the 3-layer counter): it is
  the G2 r2>=0.85 threshold when a third rung (7 or 4) contaminates the
  2-level square wave (r2 0.80-0.85), or sep12 dipping to ~4x. Physics
  survives everywhere in the +-10% box; the *certificate* survives in ~72-83%
  of it.
- **G5 BUDGET-REAL: PASS.** Full cycle in <= 1700 t = 17k ticks << 60k;
  60k-tick probe = 6-9 s single-core at L=64 (well under 3 min).

## The compact laws at the top
1. Counter period: T ~= 3.8 / eps (hysteresis-loop area / drive gain);
   verified over 4x in eps (last point deviates as tau3 -> tau2 crowding).
2. Hysteresis staircase (instrument-mode ramp, 3 seeds x 2 loops, L=64):
   up-jumps at C = 0.923, 1.107, 1.223, 1.375 (4->5->6->7->8);
   down-jumps at C = 1.031, 0.806, 0.660 (7->6->5->4, plus 8->7 at 1.032);
   loop widths Delta-C ~ 0.2-0.3, seed-reproducible to +-0.01. n(C) is a
   textbook hysteretic staircase (bistable interval per rung pair).

## Honest negative results / failed regions (all logged in results.json)
- Dv >= 15 at kappa=0.5 (wide Turing band): counter DEAD. S(n) plateaus are
  no longer separated cleanly; drive parks C without flipping n. Dv=25 (the
  classic stripe regime) never oscillates: 0 flips in 60k ticks.
- Dv=12 at L=48: dead (only rung 5 reachable; gap too wide to cross).
- kappa <= 0.2 or >= 0.9: dead or non-2-level (setpoint inside a branch's
  stable window -> C finds a fixed point; brief notes: kappa=0.1/0.9 give
  r2 ~ 0, constant n).
- eps <= 1.2e-3: fewer than 2 flips in 60k (period > window; a *slower* but
  live counter — fails G2's n_flips >= 6 within budget, not the physics).
- eps >= 4.8e-3: rung-skipping (4-7 visited), 2-level fraction < 0.92,
  r2 drops below 0.85. Drive too fast for adiabatic requantization.
- L=80/96 ladders (pairs (6,7)/(7,8)): counter runs but visits 4 rungs;
  r2 0.78-0.84 — the S-gaps shrink as n grows (gap ~ 1/n), so mid-gap
  setpoints tolerate less jitter. Small-n pairs are the good ones.
- L=48 pair (4,5) at Dv=10-11: strong square wave (r2 = 1.0!) but sep12
  only ~4x (tau2 ~ 45-70 t vs tau1 ~ 15 t): G1 fails by our own metric.
  Recorded as near-miss, not a pass.
- 2D (ny=48): the same mechanism works (film strips), with richer defect
  events (dislocation climb); certification was done on quasi-1D ny=8.
- Early metric bug (fixed before certification): tau2 measured against the
  FOLLOWING plateau only under-measured pinch onset on asymmetric rungs;
  v3 uses preceding-plateau onset + following-plateau healing. Sensitivity
  alternatives (heal-only ~ 28-58 t, pinch-only ~ 27-45 t) preserve all
  G1 verdicts at the flagship but shave margins; reported for honesty.

## What did NOT count
- No power-law claims: defect events are quasi-periodic, not scale-free
  (dwell CV ~ 0.2-0.4). powerlaw_tail not invoked. No criticality claimed.
- ramp-mode (triangle C set-point) used ONLY for the hysteresis instrument
  runs; the certified counter is 100% autonomous (mode="auto").

## Real-world analogue
Somite-counting / digit-number switching under a slowly adapting morphogen
gain; convection-roll quantization under slow heating feedback. The specific
auto-oscillation is closest to "wavelength hunting" in directional
solidification and to integer mode-hopping in lasers with slow gain feedback.

## Engine-integration sketch
World fields: u, v (existing RD pair machinery), C (one extra diffusive
field). Params: (a, b, Du, Dv, Dc, sigma, eps, kappa-derived kstar2, noise).
Update: 1 IMEX step per tick (FFT diffusion or 5-point stencil at dt<=0.05);
S-sensor = two box-blurs + gradient (all local stencils, engine-friendly);
drive = pointwise multiply-add, clip C to [0.5, 1.9]. Macro read-outs for
the dashboard: n (FFT argmax of ring profile), envmin, C-mean. Film: u field
+ count ticker; stripes visibly breathe, pinch, and snap to the new count.

## Files
- morpho_sim.py (engine), runner.py (metric-locked evaluator),
  sweep{,2,3}.py, g3_final.py, g3_sigma_staircase.py, g4_final.py,
  g4_jitter12.py, g4_recheck120k.py, g4_kap045.py, hysteresis.py,
  film_strip.py, fig_response.py; t*.py = dated scratch probes.
- results.json (master log: 279 probe runs incl. all failures),
  results_*.json (campaign shards).
- strips/: flagship_kymo.png (kymograph + 3-layer traces),
  flagship_u_2d.png / flagship_C_2d.png (2D film frames),
  hysteresis_staircase.png, response_curves.png, mode_competition.png,
  env_traces.png, L1_trace.png.
