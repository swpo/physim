# M4 COMPOSITE DYNAMICS — SUMMARY (blob-composite searcher)

**Verdict: B5 PASS — mode (a) TRAVELING BOND certified. B1 PASS. B7 PASS.**
Bonus: 3-blob traveling train. Honest negatives: rotation not observed; the M2 bond
point itself (A=5) cannot travel — boundary mapped.

## The round-1 tension, resolved by one structural fact
The steady-state equations depend on (tau, Dv) ONLY through the product
**A = tau*Dv** (steady v: u = v - tau*Dv*lap v). So the entire STATIC landscape —
blob profile, oscillatory tail, bond well — is constant along Dv = A/tau, while tau
alone dials the drift (dynamic) instability. Binding was certified at A=5, motility
at A ~ 3.1-3.6: different static worlds, hence the round-1 "tension". The M4 family:
**fix A = 4 (static bond exists: M2's tau=2, Dv=2 point), walk tau up with Dv = 4/tau.**

## Certified working family (all else M0; IMEX-FFT, dx=0.5, dt=0.02, L=96 periodic)
    lam=2, k1=-0.7, k3=1, k4=1.5, theta=0.7, Du=1, Dw=20;  Dv = 4/tau, dial tau.
IC = binding stamp method with an A=4-native stamp (relaxed at Dv=1.6, tau=2.5,
2000tu, L=64, dx=0.5); kick = v,w stamp components pasted 0.5 px displaced.
Metrics locked pre-cert in metrics.py (windows, gates, tolerances).

## B5 — TRAVELING BOND (wake-locked tandem), the main result
- **Pair drift bifurcation: tau_c(pair) = 5.636**, sqrt law
  **c_pair = sqrt(0.0560 (tau - 5.636))**, r2 = 0.996 on 5 traveling points
  (5.65, 5.7, 5.8, 5.9, 6.0; static at 5.5/5.6). Monotone PASS.
- **Out-of-window audit (round-1 style): tau = 6.1 held out** — predicted
  c = 0.1611, measured 0.1516 (travel_bond), error 6.3% <= 15%. PASS.
- **Bond survives motion**: sep contracts smoothly 15.40 (static d*) -> 14.76 at
  tau=6.1, with sep_std < 0.006 px in the cert window; ncomp==2 at every record
  post-transient in every certified run.
- **3 seeds** (tau=6.0, sigma=2e-3, d0=15, NO kick, T=3200): spontaneous tandem
  take-off, c = 0.14065/0.14085/0.14074 (0.15% spread), sep = 14.774-14.781,
  free directions {163.6, 116.6, -2.9} deg. Doubles as **B1: alive & bound 3200 tu
  under working noise** (also holds at 5x noise, sigma=0.01).
- **Unpinning**: c_pair(dx=0.25) = 0.14077 vs c_pair(dx=0.5) = 0.14075 — 0.02%.
  Speed isotropic to 4e-5 across axis angles {30, 57, 120, 203}; final directions
  0/4 (kicked) + 0/3 (noise-seeded) lattice-clustered. Honest: strict 5-deg
  kick-following was 2/4 (the 57-deg run reoriented +24 deg during the
  tandem-formation transient, then ran perfectly straight at a non-lattice angle).
- **Composite vs single — genuinely NEW dynamics:**
  1. **Pair-only drift zone**: single tau_c = 5.748 (own sqrt fit r2=0.999).
     In tau in (5.636, 5.748) the bound pair travels steadily (e.g. c=0.058 at 5.7,
     sustained 4000tu) while the kicked single decays to rest. The pair moves
     BEFORE its constituents can.
  2. **Speed boost**: above both onsets c_pair = 0.1408 > c_single = 0.1234 (+14%).
  3. **Discrete tandem shells**: two-sided convergence to sep* = 14.78 (c=0.1408)
     from d0=13,15,18; second shell sep* = 25.68 (c=0.1235) from d0=21; shell
     spacing 10.9 ~ tail wavelength 10.8. Wake-locked soliton-train physics.
  4. **Fore-aft symmetry breaking**: follower slightly larger/dimmer than leader
     (areas 33.25 vs 32.5 px, peaks 1.1233 vs 1.1262).
  5. **Trimer train**: 3-chain travels at c = 0.1430 (> pair > single), seps
     [14.5, 14.8] stable 2500tu — train speed grows with length.
- Mechanism (documented, not just curve-fit): motion is ALONG the bond axis
  (motion-bond angle = 180.1 deg): the follower sits in the leader's oscillatory
  wake; leader is pushed by the follower's front tail. The traveling bond REPLACES
  the static bond above tau_c (no coexistence): noiseless unkicked pairs sit still
  until tau=5.8 takes off from round-off; with working noise take-off is spontaneous
  from the zone edge. Below tau_c all kick channels relax back to the static bond.

## Boundary map (honest negatives, first-class)
- **A=5 (the certified M2 bond point family, incl. P7s): NO composite motion.**
  Singles stationary to tau=6.0 (kd=0.5 kicks), pairs statically bound and immobile
  (omega=0, c=0, sep->15.45-15.53) up to tau=6.0; tau>=6.5 singles REPLICATE
  (t_split 348->44 tu). Drift is preempted by replication: the M2 bond at
  (Dv=2, tau=2.5) cannot be made to move by raising tau — you must lower A.
- **Replication ceiling on A=4**: traveling pairs cascade at tau >= 6.2
  (ncomp 48-55 within ~100 tu). Working corridor: tau in (5.636, ~6.15).
- **A=4.5**: travel onset ~6.2 (c=0.025) — corridor continues but narrows toward
  replication; **A=3.5**: traveling bond at 5.2-5.5 (c up to 0.186), splits at 5.8.
  The (A, tau) corridor is coherent: lower A = earlier onset + earlier replication.
- **Rotation (target b): NOT observed.** Counter-tangential pair kicks unbind the
  pair near onset; equilateral-triangle curl kicks: tau=5.5 rotates ~53 deg during
  the kick transient then locks (omega -> 3e-8 rad/tu ~ 0); tau=6.0 converts curl
  into pure translation (c=0.151, omega ~ 1e-4 rad/tu ~ drift noise). Consistent
  with M2's static triangle.
- **Internal oscillation (target c): metastable only.** Perpendicular co-kicked
  pairs form a breathing dimer (sep 15.9 +- 0.32, period ~151 tu, motion transverse
  to bond) that persists ~1500 tu, then reorganizes into the in-line tandem.
  Reported, not certified.
- **Near-onset caveat**: tau=5.65 c still relaxing at T=2000 (0.020 -> 0.0173 by
  4000 tu); locked-protocol values near onset are ~10-15% above asymptotic.

## Gate verdicts
- **B5 PASS**: traveling bond certified (5-pt c(tau) curve + sqrt law r2=0.996,
  OOW prediction 6.3%, 3/3 seeds, bond stable under motion, unpinned 0.02%).
- **B1 PASS**: 3200 tu under sigma=2e-3 (3 seeds, bound + traveling throughout);
  3000-4000 tu noiseless longruns clean; survives sigma=0.01.
- **B7 PASS**: routine candidate (pair, T=2000, dx=0.5) = 100-235 s < 5 min at
  ~12-20 tu/s single-core; dx=0.25 unpinning one-off 312 s documented separately.

## Integrator note
All M4 runs: IMEX-FFT dx=0.5 dt=0.02 (motility's certified scheme). Controls rerun
on THIS engine: M1 point c=0.0820 (M1 cert: 0.082, 0.0% off); P7s pair d0=17 ->
sep 15.43 vs M2's dx=0.5 d*=15.70 (1.7% off M2's Euler value, same 1.8% band M2
itself saw between resolutions/integrators — documented, no re-cert needed).
Mixed-pair (vvw A-B) channel not needed: same-field pairs delivered mode (a).

## Files
- results.json — every run appended live (122 records: controls, A=5/A=4/A=4.5/A=3.5
  ladders, cert curve, seeds, isotropy, unpinning, boundaries, trimer, verdicts).
- sim.py (engine: IMEX-FFT + Euler, stamp worlds, multi-blob identity tracking),
  metrics.py (LOCKED pre-cert).
- strips/fig1_travel_bond_cert.png (c(tau) pair vs single + pair-only zone; bond
  length under motion; 3-seed free-direction take-off; tandem field snapshot).
- strips/fig2_ladder_map_trimer.png (tandem shells; A=4 mode map; trimer train).
- data/ (stamps, final-field snapshots).
