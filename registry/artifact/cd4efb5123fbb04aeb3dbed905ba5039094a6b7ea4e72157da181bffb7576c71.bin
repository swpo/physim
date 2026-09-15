# M6 BFIELD — promote the background b to a dynamical field (SUMMARY)

**Verdicts: BF1 PASS (3 seeds + dx-refine 0.14%) · BF2 PASS (self-profile law,
launch curve + threshold, backreaction curve + self-trap boundary, trail law
0.002-0.6% on Db=0 combos) · BF3 PASS (trail-mediated deflection, both signs,
control-relative gates cleared 2.5-3.4x) · BF4 HONEST PARTIAL (capture into a
self-dug channel certified noiselessly + mechanism triangle; noisy asymptotic
confinement fails the locked bound; space-partition candidate = clean NEGATIVE;
uncertified bonus: b-assembly of a motile molecule with negative control) ·
B7 PASS. Headline: SELF-LAUNCH — a new motility mechanism below the drift
bifurcation, c = 0.209*gamma^0.34.**

## The field
Machine's static isok load, made dynamical (4th field; source = where blobs are):

    db/dt = (gamma*S(u) - b)/tau_b + D_b lap b
    coupling (isok, exact): k1_eff = k1 + u0*b, k4_eff = k4 + b
      == one reaction term  +b*(u0 - w)  in the u-equation.
    S = tanh(max(u - THR, 0)/0.4)   ["s2" core deposit, bounded by construction;
      s1 = tanh((u-u0)/1) signed and s3 = tanh((w-u0)/0.3) halo variants mapped]

- **Vacuum exactness survives dynamics** (V0): u=v=w=u0, b=0 is an exact fixed
  point for all three sources (deviation 1e-16 over 200tu, with saw static field
  stacked on top). The b-coupling is quadratic in deviations (delta_b*delta_w),
  so vacuum linear stability is unchanged. No clipping anywhere; |b| bounded by
  |gamma| through the tanh source.
- gamma < 0: blob digs a WELL (self-attraction). gamma > 0: blob builds a HILL
  (self-repulsion). tau_b in {50,200,1000} >> tau; D_b in {0,0.25,0.5,1,2}.
- World: A=4 single-species family (M4), IMEX-FFT dx=0.5 dt=0.02, L=96 (128/192
  documented), M4 stamp ICs, machine tracking verbatim. gamma=0 anchors reproduce
  M4/machine to 0.0-0.02% (C0: pair tau=6 c=0.140785 sep 14.779; single tau=5.7
  decays; pair tau=5.7 c=0.059236 sep 15.233).

## Q1 SELF-PROFILE (parked blob, tau=5.7)
- **Well law (gamma<0, Db=0)**: b_core = 0.976*gamma for gamma in [-0.02,-1.0];
  0.976 = tanh((u_peak-THR)/0.4) exactly (saturation, not fit). Profile = plateau
  filling the blob core (flat to r~2px, edge r~3.5px, zero outside). Depth is
  tau_b-INDEPENDENT (fixed point); tau_b only sets approach time.
- **Dilution (Db>0)**: healing length ell = sqrt(Db*tau_b) >> blob radius makes
  the well shallow+wide: b_core(gamma=-0.05, tb=200) = -0.0488 / -0.0037 / -0.0013
  at Db = 0 / 0.5 / 2.0 (13x / 38x dilution). Monotone. PASS.
- **Survival window in gamma** (tau=5.7, tb=200, Db=0, T=1500):
  negative side: alive & parked at gamma = -1.0 (b_core -0.986, area 44.25) —
  DEEP LOCAL wells do not kill the blob, even 5x beyond the machine's uniform
  static edge (b=-0.15 pair replication): **locality is protective** (the C3
  level window is a uniform-b result; the self-dug well is core-sized).
  positive side: self-launch from gamma >= ~0.005; traveling alive to +0.25
  (b_max 0.186 < static +0.2 edge); **REPLICATION at gamma >= +0.30**.
  Window: gamma in [-1.0(tested), ~+0.27].
- Sources s1/s3 share all phenomenology (parked well to -0.3; launch at +0.15;
  s1 replicates at +0.30 like s2, s3's halo spreads the deposit -> still
  traveling clean at +0.30). s2 = certification source.

## Q1b SELF-LAUNCH — NEW MOTILITY MECHANISM (the volcano works)
At tau=5.7, 0.048 BELOW the single-blob drift bifurcation (tau_c=5.748): parked
blob + gamma>0, **no kick, no noise** -> spontaneous take-off. Mechanism: the
hill saturates (t ~ tau_b), any symmetry break puts the blob on its own slope,
sliding is self-reinforcing because the hill lags (tau_b >> blob response):
autophoresis from a bounded deposit. NOT the M4 drift bifurcation:
- **Launch curve** (locked T=3000, Db=0, tb=200): gamma = 0.005/0.0075/0.010/
  0.015/0.02/0.05/0.10 -> c = 0.0326/0.0391/0.0440/0.0521/0.0569/0.0755/0.0919.
  Monotone; **c = 0.209*gamma^0.341 (r2=0.991)** — NOT a sqrt-in-tau law.
- Sub-threshold: gamma = 0.001, 0.002 parked to T=6000/3000 (c < 4e-4) with the
  hill fully saturated. **Threshold gamma* in (0.002, 0.005)** at tb=200 Db=0.
- tau_b moves the threshold: tb=50 g*=(0.01,0.02]; tb=1000 g=0.02 launches
  (c=0.034 at T=4000, still building). D_b SUPPRESSES launch: at Db=0.5,
  gamma=0.05 parked to T=3000, 0.08/0.10 parked to T=1500 (dilution flattens
  the local slope) — D_b is a launch-threshold dial.
- **BF1 coexistence at the flagship point** (g=+0.05, tb=200, Db=0, sigma=2e-3,
  T=3000, no kick): 3/3 seeds alive, traveling, spontaneous take-off in free
  directions, c = 0.07553/0.07569/0.07579 (0.34% spread), b in window all run.
  Parked-well coexistence (g=-0.05, same noise): alive, net drift 0.006px,
  b_core -0.0488 in [-0.055,-0.040]. **dx-refine: c(0.25)/c(0.5) - 1 = 0.14%**
  (kicked launch protocol) — unpinned, continuum. BF1 PASS.

## Q2 BACKREACTION ON MOTION (tau=6.0 traveler, kicked, tb=200, Db=0, T=1500)
- 7-pt curve + control: gamma = -0.05/-0.02/0/+0.02/+0.05/+0.10/+0.15 ->
  c = 0.1088/0.1193/0.1234/0.1267/0.1306/0.1346/0.1369. Monotone; gamma=0
  reproduces the M4 single anchor 0.1234 to 0.0%.
  **gamma<0 = effective-mass slowdown** (drags its own well: -12% at -0.05);
  **gamma>0 = plowing speedup** (surfs its own back-hill: +6% at +0.05).
- **SELF-TRAPPING transition**: gamma <= -0.07 the traveler is CAUGHT by its own
  deepening well: net displacement < 40px, straightness < 0.4, x(t) rattles
  (amplitude ~10-20px) while the blob stays alive and locally fast (c_tail up to
  0.11 — orbiting in the trap). Boundary gamma_trap in (-0.07, -0.05] at tb=200.
- tau_b dependence at gamma=+-0.05: drag/boost shrink as tau_b grows (slower
  field = shallower co-moving deformation): c(g=-0.05) = TRAPPED/0.1088/0.1209/
  0.1212 at tb = 100/200/500/1000(L128); c(g=+0.05) = 0.1349/0.1306/0.1253/
  0.1253. Both branches -> c0 = 0.1234 as tau_b -> inf... EXCEPT the +side at
  tb=100 (faster field = larger deposit under the blob = stronger push). Faster
  wells trap earlier: tb=100 traps at gamma=-0.05 already.

## Q3 TRAILS & STIGMERGY
- **Trail law** (BF2): behind a steady traveler, b_trail(s) = B0*exp(-s/s0) with
  **s0 = c*tau_b** (pure relaxation in the co-moving frame):
  (g=-0.05, tb=200, Db=0): s0_fit 21.63 vs pred 21.76 (0.6%, r2=0.99999);
  (g=+0.05, tb=500, Db=0, L=192): s0_fit 63.47 vs 63.47 (0.002%, r2=1.0);
  (g=+0.05, tb=200, Db=0.5): 19.0 vs 25.0 (24%, inside the 25% gate — transverse
  spreading shortens the apparent decay; documented Db correction).
  Persistence range = c*tau_b: at tb=1000 a trail spans >domain (125px).
- **BF3 CERT (mediated interaction with control)**: writer pair (tau=5.7
  pair-only zone) passes a PARKED reader at 20px lateral offset (reader cannot
  self-move there). Amendment-1 locked metric: ddy = reader deflection minus
  the gamma=0 control's (+5.89px, direct oscillatory tails — measured, the
  reason control-relative gates are needed). Results (sigma=2e-3):
  attract (gamma=-0.30, Db=1) seeds 1/2: **ddy = -9.2 / -10.3 px** (gate <=-3);
  repel (gamma=+0.30): **ddy = +7.4 px** (gate >=+3); all blobs alive, writers
  still traveling. Noiseless pilots agree (-9.7/+6.7; from 24px: -7.1).
  **A blob leaves a track that another blob follows/avoids minutes later:
  stigmergy in a PDE. BF3 PASS.**

## Q4 EMERGENT STRUCTURE (BF4) — honest ledger
Three candidates, locked by amendments BEFORE their batteries; two negatives,
one partial, one strong uncertified bonus:
1. **Writer-pair channels (P4)**: NEGATIVE as designed — two co-traveling wall
   pairs + middle pair interact through wakes directly; control shows the same
   dynamics (walls at 24-36px are inside wake range). Pilot only.
2. **Self-dug channel capture (batteries 1-3 + amendments 2-4)**:
   - Noiseless mechanism triangle CERTIFIED: probe launched parallel 22px from
     a dug groove (tau=6.0 writer, g=-0.50, tb=1000, Db=0.25, ~3 laps, depth
     ~-0.003..-0.010) is pulled INTO the channel and oscillates about it
     (P7a, +writing); with writing OFF during capture it still captures (P7d,
     passive decaying groove); with NO groove it runs exactly straight
     (P7c, v_y = 0.0). Capture range 22px >> any direct-tail scale.
   - Under noise (3 seeds): capture happens in every seed (crossing from 22px,
     co-travel, all alive, T=2500-5000), but the channel-frame transverse
     oscillation is weakly PUMPED (both blobs keep digging; amplitude grows
     28.6 -> 35.1px over ~2 periods in T=5000) -> the locked asymptotic
     confinement bound (1.5*A0) is crossed. **Batteries 1-2 FAIL their locked
     gates (writer wander / slingshot through decayed section); battery-3
     scoring: capture YES (3/3 + control), bounded confinement NO.**
     Verdict: HONEST PARTIAL — "trail-guided deflection and capture" is real
     and controlled; "permanent confinement" is not certifiable at these params.
3. **Mutual-avoidance space partition (amendment 5, BF4P)**: clean NEGATIVE.
   3 writers with repulsive trails (g=+0.35) NEVER partition the torus: wake
   shell-locking dominates and CLUSTERS them (R 0.75 -> 1.0-1.24, min gap
   2.5-14px; gamma=0 controls nearly identical). In a world whose motor is wake
   attraction, stigmergic avoidance loses at sub-replication gammas.
4. **b-ASSEMBLY -> MOTILE MOLECULE (PT3, uncertified bonus)**: 3 parked blobs,
   pairwise d0=24px (beyond the wake-bond basin ~19.5), gamma=-0.50 s3 halo
   wells (Db=2, tb=200; healing length 20px): the shared long-range well pulls
   all three into contact (t~400) -> they lock at M4 shell seps [15.1,15.1,15.7]
   (std<0.01px) -> **the assembled trimer SELF-LAUNCHES (t~800) and travels as
   a rigid V at c=0.0758 for >1200tu — at tau=5.7 where every constituent alone
   is provably immobile** (pair-only zone) and parked singles stay parked.
   gamma=0 control: pure expansion to 26.6px (no assembly). Pair versions:
   d0=24 contracts to the 14.9-15.2 shell (t_contact 210-335), control expands
   to 27.1. n=1 noiseless each; flagged as the natural BF4 cert target
   (gates drafted in PT3_triangle_readout).

## Q5 b_target TEASER (probe only)
One-way circulation writes ASYMMETRIC standing profiles: a tau=6.0 traveler
lapping the torus at tb=1000 leaves a **sawtooth-like b**: sharp fresh edge at
the blob (-0.0037), monotone exponential ramp behind decaying to -0.0018 at
one-lap distance; lap-decay ratio 0.49 vs exp(-T_lap/tau_b)=0.46 predicted (6%).
The M5 machine's saw-track shape (long ramp + cliff) IS the natural fixed point
of asymmetric motion writing into a relaxing field — a circulating blob digs its
own one-way track (gamma<0 moat) or builds a levee (gamma>0). Amplitude at
g=-0.05 is ~0.004 k4-units ~ the machine's tooth scale (0.008). The full inverse
problem (evolve b INTO the machine landscape: teeth + rails placement) remains
the merge milestone — not solved here.

## Honest negatives & traps (first-class)
- kick_d=1.0 SPLITS the tau=6.0 blob (replication in <=75tu even with gamma=0).
  M4's kd=0.5 is the max safe kick. (Invalidated pilot P6; rerun as P7.)
- Angled stamp kicks (ang != multiples of 90) QUANTIZE to the axis at dx=0.5
  when kd=0.5 (half-cell offset rounds away) — use parallel-launch geometries.
- Fixed-line channel gates are frame-brittle: grooves are MOVING objects
  co-evolving with their diggers; score in the channel/writer frame.
- Noisy gamma<0 travelers have diffusing heading (12.7px wander over T=2500 in
  fresh world) — any line-tied protocol must control for it.
- tau=5.7 pair writers at tb=1000 self-trap after ~2 laps for |gamma|>=0.4
  (lap-accumulated moat): writer budget limits dig depth per pass.
- Db>0 kills self-launch (dilution) at the same gammas that launch at Db=0:
  motility and trail-spreading trade off through ell=sqrt(Db*tau_b).
- Uniform-b window (machine C3) does NOT transfer to self-dug wells: locality
  is protective (alive at b_core=-0.99 local vs replication at b=-0.1 uniform).

## Files
- results.json — 180+ records, appended after every run (V0/C0 anchors, E1-E3
  scans, L/W/G digs, BF1-BF4 batteries incl. failed ones, teaser, verdicts).
- sim.py (4-field IMEX-FFT engine; vacuum_blob_sector surgery documented),
  runjob.py/drive.py, metrics.py (LOCKED + 5 dated amendments, all pre-battery).
- strips/: fig1_selfprofile_launch_backreaction.png, fig2_bf3_mediated.png,
  fig3_bf4_structures.png (+ working plots: trap_xt, bf4b_yt, p7_capture,
  fusion_pilot, p5_recruit, bf4_b1_relative).
- data/: every run npz (tracks, b stats, snapshots, chainable states).

## Budget (B7)
4-field L=96 IMEX-FFT: 13-18 tu/s -> routine candidate (T=1500) 85-115s. PASS.
L=128: ~8-11 tu/s (T=2500 ~ 300-360s, at the 5-min line, documented); tau_b=1000
long runs (T=3000-6000) and L=192/dx=0.25 one-offs documented (4-30 min).
