# COUPLED COUNTERS (sync tower) — round-2 summary (2026-02-18)

## Verdict
**Mutual mode-locking of two integer counters: CONFIRMED and mapped.**
L4 (relative phase) exists with a textbook Arnold-tongue phenomenology:
a wide 1:1 plateau (rho pinned to 1.0000+-0.005 over a 1.7x detuning range),
sharp edges, tongue width ~linear in coupling, and a diverging slip period
at the edge. Gate outcome (honest): G1/G3/G5 PASS, G2 PASS for the in-tongue
regime (plateau law), G2 **FAIL for the near-edge slip regime as a strict
r2>=0.85 sawtooth** — slip trains are quasi-periodic (CV ~ 0.35-0.49) because
each ring's own defect events jitter the slip nucleation. G4: in-tongue 3/4
seeds + 4/4 jitter PASS; slip-regime robust as a REGIME (slips in 19/19
campB3 runs; verdict correct in 8/8 jitter draws) but the strict-G2 point
certification fails. We report the slip side as a mapped regime with a
measured scaling law, not a certified 4-layer clock.

## Setup (all internal, no forcing)
Two certified round-1 counter rings (Dv=11, L=64, pair 5<->6, kstar2=0.2682,
mid-gap servo) with different gains eps1 = eps_g*sqrt(R), eps2 = eps_g/sqrt(R)
(eps_g=2.4e-3) => natural periods T_i ~ 3.8/eps_i, detuning ratio R.
Coupling: pointwise C-leakage dC_i/dt += kc*(C_j - C_i) — transverse
diffusion between stacked annuli. sync_sim.py batches both rings in one
(2,ny,nx) array; ~12s/100k ticks.

## L4 metric (locked before certification)
phi_i(t) = piecewise-linear cycle phase interpolated between UP-flips of
ring i's dominant 2-level count; Delta = phi1 - phi2 in cycles;
slips = hysteretic integer-winding events of Delta; rho = winding ratio;
locked = 0 slips AND max|Delta - median| < 1 cycle over >= 8 joint cycles.
T_slip (pooled) = sum(spans)/sum(|net winding|) across seeds.

## Hierarchy (flagship in-tongue point R=1.3, kc=2e-3)
| layer | variable | timescale |
|---|---|---|
| L1 kinetics | pixel ACF | tau1 ~ 12-15 t |
| L2 defect events | envelope pinch/heal | tau2 ~ 87-104 t (sep12 ~ 6-7x) |
| L3 counter cycle | n_i(t) square wave | T3 ~ 1410 t (sep23 ~ 14-18x) |
| L4 phase relation | Delta(t) | locked: bounded for >= 28 cycles (>=40k t, no drift); slip regime: T_slip 2.3k-23k t (sep34 1.3-19x, grows to infinity at the edge) |
Tick -> L4 span: 0.1 (dt) -> 40 000+ t = 4e5 ticks: 5.5 decades.

## The laws (G3)
1. **1:1 plateau (staircase):** rho(R) = 1.0000 +- 0.005 for R in [1.0, 1.727]
   at kc=2e-3 (12 points, campA); uncoupled rho tracks R (1.22 at R=1.33).
   Above the edge rho detaches and climbs toward R (no clean 3:2 plateau at
   this kc/noise — washed out by defect jitter; honest negative).
2. **G3a slip divergence:** pooled over 3 seeds x 7 detunings
   (t up to 80k per point): T_slip = 22627, 8203, 5881, 6002, 3702, 3362,
   2295 for R = 1.76 ... 2.30. Free power-law fit vs (R - R_c), R_c = 1.7271
   measured independently by bisection: **exponent -0.72, r2 = 0.945**
   (fixed -1/2: r2 = 0.856; exponent range -0.53..-0.87 as R_c varies within
   its bisection bracket [1.719, 1.735] + placement uncertainty).
   Monotone divergence: YES (one soft inversion 1.85/1.92 within seed noise).
   Saddle-node-ghost -1/2 is CONSISTENT but not sharply resolved; the
   effective exponent is steepened by noise-assisted slips near the edge
   (Kramers correction) — stated as such, no overclaim.
3. **G3b tongue width vs coupling:** half-width ln(R_c) = 0.180, 0.322,
   0.365, 0.546, 0.826, 0.924 for kc = 0.5, 1, 1.5, 2, 4, 8 e-3.
   Linear through the 4 weakest: slope 228.7 per unit kc, r2 = 0.954;
   saturates for kc >= 4e-3 (width growth bends down as coupling stops being
   weak). 4+ points smooth & monotone: PASS.

## Gates
- G1 (4 layers, separations): PASS in-tongue (6.9-7.2x / 17-19x / plateau
  persists >= 28 cycles = "infinite" tau4); slip regime sep34 >= 5 only for
  R - R_c <= 0.05 (T_slip >= 8k), where slip counts per run drop to 2-3:
  slow-and-many-slips is self-contradictory in finite budget — reported.
- G2: in-tongue PASS (rho plateau = the compact law; constant with 0 slips,
  12-point staircase table). Slip strict sawtooth FAIL: best r2 0.86 (1/19
  runs >= 0.85 with >= 5 slips). Root cause measured: slip intervals CV
  0.35-0.49 nearly independent of kinetic noise (1e-5 -> 2e-3), i.e. the
  jitter is intrinsic (deterministic defect chaos), not thermal.
- G3: PASS (two curves above + staircase; all smooth/monotone within noise).
- G4: in-tongue R=1.3: seeds 3/4 (seed 3 has one early-transient slip at
  t~14k before settling locked — verified locked from t_cut=20k on a 400k
  run), jitter 4/4. Slip R=2.0: regime robust 4/4 seeds + 4/4 jitter (all
  slip, 3-12 slips), but strict G2+sep34 point-cert 2/8. R=1.85/noise=5e-4
  attempt: 1/4 seeds strict. Verdict: G4 PASS for the tongue, REGIME-PASS
  (law-level, not point-level) for slips.
- G5: PASS — locked cert 200k ticks ~ 30-45 s; slip runs 300-500k ~ 50-130 s;
  all <= 5 min.

## Honest caveats & negatives
- Slip trains are quasi-periodic, not clockwork: L4-slip fails strict G2.
  The intrinsic CV ~ 0.4 is a finding: integer clocks synchronized through a
  diffusive scalar channel inherit the defect-event jitter of the counting
  mechanism itself.
- No higher-order (3:2, 2:1) plateaus resolved at kc=2e-3 (rho drifts
  smoothly with seed scatter +-0.15 past the edge). Likely needs weaker
  noise + longer runs; not claimed.
- Tongue edges measured on the R>1 side only (ring-swap symmetry spot-checked
  at R=0.6 => locked, consistent).
- R_c has +-0.01 bisection/placement uncertainty which propagates to +-0.17
  in the scaling exponent; -1/2 sits inside the band at the wide end.
- eps_g=2.4e-3 keeps both rings below the rung-skip zone up to R=2.4; beyond
  R~2.4 ring 1 approaches eps~3.7e-3 where round-1 showed 3rd-rung pollution.
- Counting never died under coupling (alive 19/19 campB3, all g4 runs):
  "coupling destroys the counter" region NOT found for kc <= 8e-3 —
  C-leakage is gentle because both C fields live in the same [0.5,1.9] range.

## Real-world analogue
Coupled segmentation clocks (somitogenesis in neighboring tissue), circadian
entrainment, Josephson junction arrays (rho staircase = Shapiro-like steps;
T_slip divergence = junction phase slips near the critical current).

## Files
sync_sim.py (2-ring batched engine), sync_metrics.py (L4 phase/slip/rho),
sync_runner.py (locked evaluator), campA/B/B2/B3/C/C2 campaign scripts,
g4_sync.py, g4_slip2.py, t*_ probes; results.json (consolidated, 88 KB);
strips/L4_traces.png (locked vs slip Delta(t) + count trains),
strips/sync_laws.png (staircase, tongue width, slip divergence).
