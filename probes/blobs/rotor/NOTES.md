# M7 rotor notes

M7 ROTOR PLAN (2026-02-19)
==========================
Facts inherited:
- A=4 family: M0 + Dv=4/tau, dial tau. IMEX-FFT dx=0.5 dt=0.02 L=96. stamp_A4_dx05.npz.
- pair onset tau_c=5.636, single onset 5.748, replication >=6.2. c_pair=sqrt(.056(tau-5.636)).
- static d*=15.4, traveling sep*=14.78, shell2 25.68, tail wavelength ~10.9. bond basin [14.5,19.5].
- M4 negatives: curl-kick triangle locks (5.5) or translates (6.0); counter-tang kicks unbind near onset (kd=0.5).
- blobs slide DOWN b in isok load (park at b minima). machine rails/saw conventions.
- vvw arch: cross-species = repulsion only (shared w monotone at relevant r?); private v = binding channel.

Designs:
 (ii) same-species rotors EARLY: pair counter-tangential GENTLE kicks (kd 0.1-0.3) near onset;
      triangle curl+chase, tau scan 5.60-6.1 incl pair-only zone (5.636,5.748) which M4 never scanned for rotation.
 (1b bridge) bond-only orbit test in SINGLE species: center blob held by b-cone (cap 6), orbiter
      bonded at 15.4, kicked tangential; does the bond turn propulsion into orbit? informs (i).
 (i) heterodimer: NEW ARCH "xv" = 6 fields, fully private (u_i,v_i,w_i) + cross-wired v:
      dv_i = (u_i - v_i + eta*(u_j - u0))/tau_i + Dv_i lap v_i.  eta=0 EXACTLY two copies of M4.
      A_i=tau_i*Dv_i=4 both => identical statics, same stamp. tau_1 motile (5.65-6.1), tau_2 anchored (2.5).
      Cross-imprint via v carries oscillatory tail => cross-binding predicted; d*_cross predictable from
      stamp: dv1_hat = eta du_hat/(1+4k^2), landscape dk1_eff=-k3 dv1, well at most-negative ring.
 (iii) ring-valley orbit demo: b=eps*min(|r-R0|,cap,...) racetrack + planet demos + film. RT3.
RT2: cross-bond curve (d*, basin, escape) OR no-go map incl. w-channel vs v-channel imprint quantification.
Gates: RT1 (attractor: >=3 revs steady omega, +-20deg kick basin, 3 seeds, omega(dial)>=4pts, dx spot),
RT2, RT3, B7 <=5min routine.

KEY DESIGN INSIGHT (from stamp radial profiles, A=4):
- dv(r) [private v halo] = (1+A k^2)^-1 response to du: core +1.04, ZERO at r=6.1,
  NEGATIVE ring r in (6,15) with min -0.048 at r~8, ~0 beyond 15 (weak 2nd dip -0.0006 at 18).
- dw(r): monotone positive decay (repulsive only) -> confirms M3 "shared w can't bind".
- CROSS-WIRE dv_i/dt = (u_i - v_i + eta*(u_j - u0))/tau: blob j imprints eta*dv(r) on v_i.
  v enters u-eq as -k3*v => effective dk1(r) = -k3*eta*dv(r) = +0.048*eta at r=8 (max),
  NEGATIVE core r<6 (self-avoiding). => STABLE cross-bond predicted at d* ~ 7-9,
  well depth ~0.05*eta in k1-units.
- THE ROTOR MECHANISM FOR FREE: the anchor's v-halo is a RING VALLEY in the motile
  blob's OWN propulsion field (v_1). Tangentially flat, radially confining =
  self-assembled circular rail. Propulsion direction settles tangential -> orbit;
  only soft mode = CW/CCW. Design (i) and design (iii) are the same physics,
  one field-mediated, one background-mediated.
- Twin-private-w architecture (6 fields: u_i,v_i,w_i + cross-v eta): at eta=0 each
  species is EXACTLY the M4 A=4 world (same stamp, same tau_c laws); background
  preserved exactly for any eta (cross term vanishes at uniform state since u_j=u0).
  Per-species tau_i independent: M (tau_1 in drift corridor) + S (tau_2=2.5 static).


## STATUS 2026-02-19 (post-consolidation)
DONE. See SUMMARY.md. 104 results.json records. RT1 PASS (heterodimer), RT2 PASS
(cross-bond + no-go), triangle partial (basin knife-edge honest), RT3 honest negative
(bond outcompetes ring at safe eps), B7 PASS. Scorecard sent to parent.
