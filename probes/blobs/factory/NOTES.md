# blob-factory — WORKING NOTES (phase 3, L3->L2 machine search)

## Mission (brief, 2026-02-19)
Fulfillment-center primitives from certified L3 components, in the xv world
(M7 6-field arch) + machine-style static backgrounds:
1. ROLLER ADVECTION: parked rotor (tau1 in ROTOR-ONLY zone) + third blob at graze
   distance d in {10,12,15,20}: v_cargo(d) + capture/deflection map. Null OK.
2. UNLOAD/RELEASE DOCK: eta(x) static field entering v-eq exactly like isok enters
   u (drive ~ (u_j-u0) vanishes at vacuum): eta->0 null zone releases towed cargo.
3. SPECIES FORK: per-species rails (bfield vs bfield2) Y-junction sorts M from S.
4. GLUE: chain two certified primitives in one world; map interference.

## Architecture decisions (engine = fork of rotor/sim.py, conventions verbatim)
- eta(x,y) static COUPLING FIELD: dv_i/dt = (u_i + eta_i(x,y)(u_j-u0) - v_i)/tau_i.
  Vacuum-exact for ANY static eta (cross term vanishes at u_j=u0) — same class as
  isok. Kinds: const / xstep (dock) / xbox.
- Per-species isok b_i(x,y): k1+u0*b_i, k4+b_i in species i u-eq only. u0 exact
  root for all b (machine/NOTES isok). Kinds: chan / saw+chan / forkchan (rail
  Y-junction) / ringcone (rotor verbatim).
- Species roles (M7): M = species1 (tau1 dials drift, A=4), S = species2
  (tau2=2.5, deep-static anchor: can NEVER self-move; natural cargo).
- KEY physics inherited: cross-bond d*=7.98 (eta=0.05) / 7.5-7.6 (eta=0.1);
  same-species A=4 bond d*=15.4, basin [14.5,19.5]; M-M pair travels at
  tau1=5.7 (c=0.0595); rotor-only zone tau1 in [5.52,5.636); S-M interact ONLY
  via eta (w private): eta=0 => cargo is INVISIBLE to carrier.

## Predictions from stamp math (write BEFORE runs)
- Cross-halo v-landscape (k1-units, per eta): core repulsive r<6.1, attractive
  ring r in (6,15), min at r~8, dead >15.
- ROLLER: cargo S parked in anchor's same-species bond ring (r*=15.4) = circular
  rail (azimuthally flat). M orbiting at r=8.44 sweeps past at closest approach
  ~7 (aligned) — inside cross-attraction. Sweep asymmetry (v-memory tau2 lag +
  cargo displacement during pass) -> nonzero net azimuthal ratchet expected;
  sign uncertain (drag-along vs slingshot-back). |v_tan| ~ eta-scale: could be
  tiny; quantify vs CTRL eta21=0 (cargo blind: exact null) and no-rotor control.
- d=10: cargo inside same-species repulsive zone -> radial ejection competes;
  d=12: cross-wells overlap strongly at pass (s_min=3.6 < core radius: strong
  kick, maybe capture into M's well = orbit transfer); d=15: at bond ring, s_min
  ~6.6 ~ zero crossing; d=20: s_min~11.6 weak attraction, cargo barely held by
  same-species basin edge.
- DOCK: carrier = M-M traveling pair (tau1=5.7 kicked +x), cargo = S. Pair tows
  S via superposed cross-wells (predicted tow slots: leading/trailing on-axis at
  ~8 from a blob core, or saddle between at y=+-3). Tow speed = pair c (if bond
  holds). At eta->0 (xstep, width 3): well depth -> 0 smoothly over ~6px; cargo
  detaches, STOPS (deep-static), carrier continues. Control: const eta => carried
  to end. Control: no carrier => cargo parked forever.
- FORK: forkchan rails per species diverge after x0; tow bond (eta well ~depth
  prop to eta) vs transverse rail force (chan_eps): junction splits convoy when
  rail separation > bond reach (~10px) IF rail force can hold each species on
  its own branch. S response to rails is SLOW (far from onset: vvw-like linear
  ~ -0.9*chan_eps) — risk: S ignores rails on tow timescale -> use release
  (eta null zone) AT the junction instead, or steeper S rails (bfield2 only).

## Measurement conventions (locked in metrics.py before cert batteries)
- Roller: cargo azimuthal advection about anchor S: unwrapped phi_cargo(t),
  omega_all (whole-track fit), vtan = omega*r_mean; capture = cargo leaves
  anchor ring & locks to M orbit / cross-well (sep_MC < 10 sustained);
  deflection = radial exit beyond r>26 or azimuth jump then re-park.
- Dock: release = (carrier net_x continues >= 30px past null entry) AND (cargo
  x freezes: |dx|<1px over last 500tu) AND census 3/3 alive. Carry control:
  cargo tracks carrier to domain end (sep in tow band).
- Fork: purity over >=6 mixed arrivals = fraction of blobs ending in their
  species' bin (y side of branch at x > x0+20).

## Session log
- [t0] engine forked (sim.py: eta fields + per-species b + forkchan), runjob.py
  extended (roller/pairs metrics), metrics.py = rotor copy (extend+lock later).
- SMOKE plan: reproduce M7 anchor (tau1=5.7 eta=0.1 d0=8 T=1800): expect
  omega=-0.011063, sep=8.44 (rotor G_dx05_ref). Scalar path AND const-field path.

## Session log (running)
- SMOKE PASS: forked engine reproduces M7 anchor EXACTLY (omega=-0.011063,
  sep=8.4392 vs rotor G_dx05_ref -0.011063/8.439) on BOTH scalar-eta and
  const-eta-field code paths. Records 1-2.
- D0 tow probes (eta21=0.1, carrier-blind M-M pair tau1=5.7, c~0.06-0.09):
  * trail slot d=8: NOT TOWED. Pair leaves at full c; cargo dragged ~7px total,
    then abandoned; pair lapped torus and split cargo on second contact (t=1115).
  * push/mid slots: pair OVERRUNS cargo (sep 8->2.8), cargo area 33->25, SPLITS
    at t~120. Blind carrier at c=0.09 plows through cargo. Records 3-5.
  => SPEED MISMATCH is the obstacle: S-cargo response in eta-well << pair speed.
- R0 response battery launched: static blind M + cargo at d0={10,12,14} eta21
  {0.05,0.1}: v(sep) mobility curve -> critical tow speed c*.

## R1 ROLLER RESULTS (records 6-11) — headline: NO advection; NEW attractor found
- Cargo azimuthal advection pre-capture: omega ~ -4e-6 rad/tu (d0=10/12/15),
  vtan ~ 5e-5 px/tu — NULL at 1000x below rotor tangential speed. d0=20:
  -3.8e-5 rad/tu (same sign as rotor, 10x above the inner cases but still tiny).
- INSTEAD: the second S KILLS the rotor. All d0 in {10,12,15,20}: cargo S is
  reeled to sAC=14.78 (the M4 same-species bond!) while M drops to the
  cross-bond r~8.4-8.8 from BOTH S's: static isoceles S-M-S triangle
  (apex angle at M ~118deg) ... which is NOT static: M LIBRATES about the S-S
  axis, amplitude EXACTLY +-90deg steady over >=1500tu (limit cycle), period
  ~307tu. The drift instability pumps a pendulum mode instead of rotation.
- NULL (eta21=0, S's blind, rotor drive intact): M shuttles ALONG the
  perpendicular bisector straight THROUGH the S-S gap (x frozen at midpoint to
  1e-11, y swings +-7px through the axis), S-S at 15.4. A "shuttle oscillator".
- no-M control: S-S settle 15.0->15.44, zero azimuth. Confirms all azimuthal
  motion needs M; confirms same-species statics.
- d0=20 capture: r 20->16.8 by t=500 with rotor spinning (omegaM=-0.0055),
  full capture t~555, then rotor stalls -> pendulum. NOTE d0=20 is OUTSIDE the
  M2/M4 same-species basin [14.5,19.5] -> R2 battery (d0 20/22/24, with/without
  rotor) attributes capture range extension to the rotor.

## D0 TOW RESULTS (records 3-5) — speed mismatch quantified
- Blind carrier (eta12=0) M-M pair c~0.06-0.09 vs cargo well response:
  * trail slot d=8: cargo max drag speed ~0.005-0.014 px/tu (peak at sep~12,
    i.e. pulled toward RECEDING pair by the r in (6,15) attractive ring);
    pair escapes, cargo abandoned after ~7px of drag.
  * push slot d=8 ahead: pair PLOWS INTO cargo: sep 8->2.8 core overlap, cargo
    squeezed (area 33->25), SPLITS at t~120. Blind push = cargo destruction.
- C2 mutual-eta loaded pair (tau1=5.7): drops cargo AND REPLICATES (nc1 2->3 at
  t~1330; pair sep stretched to 18). eta-loaded traveling pairs are fragile.
=> tow ceiling ~0.014 px/tu at eta=0.1 << c_pair(5.7)=0.059. Matched-speed
   carrier needed: pair at tau1 just above 5.636 (c<=0.02) or deeper eta21.
   R0 battery (static M, cargo v(sep)) running to quantify the well force.

## R0 WELL-RESPONSE CURVE (records 13-16) — the tow design numbers
One-way eta21 (M static & blind): cargo S reeled from any d0<=14 to one-way
cross-bond d*=7.92 (eta21=0.1) / 8.04 (eta21=0.05). v_approach(sep):
- eta21=0.1: peak 0.0173 px/tu at sep~10.2; 0.013 at 9.2; falls to 0 at 7.92 and
  ~0.002 at 13.7. eta21=0.05: peak 0.0078 at 10 (~linear in eta: x2.2 for x2).
=> TOW CEILING: carrier speed must be <= ~0.017 (eta=0.1). Trailing-slot fixed
   point stable on INNER branch (dv/dsep>0): sep* solves v(sep*)=c_pair.
   c_pair(tau1) = sqrt(0.056(tau1-5.636)) -> tau1=5.64: c=0.015 (tow-able!),
   5.66: 0.037 (too fast at eta 0.1; OK at eta 0.2 if linear scaling holds).

## Carrier-candidate failures (records 12, 17-21, 28-29) — honest map
- D1 mutual-eta front push (5.66 & 5.7): leader replicates at t~80 as it enters
  the cargo well. eta=0.1 acts like a |k1| kick ~0.1*du >> machine b-safe 0.01:
  near-onset traveling M's REPLICATE inside a cross-well. Design rule: keep
  traveling M's BLIND (eta12=0) or eta12 <= ~0.05 when they must cross wells.
- S1 sandwich M-S-M (sep 16): M's replicate t~100 (same mechanism + squeeze).
- C2 mutual-eta pair + rear cargo: 5.7 replicates t=1330; 5.66 survives but
  crawls away (c ~ 0.006-0.018) leaving cargo (well 0.017 marginal).
- C1 MS heterodimer on rails (chan 0.002): NO translation. Rails convert the
  rotor soft mode into libration (M swings +-5px in y); S x-drift only
  -5.5e-4 px/tu at 5.7. Heterodimer tractor: NEGATIVE at these tau1.

## RM roller with M-SPECIES cargo (records 30-31) — capture YES, but unstable
M cargo from d0=15/20: reeled in (same-species wake of orbiter, range >=20),
azimuthal arc +7-8.5px during spiral (REAL advection, transient), M4-bonds to
orbiter at 14.4, then cargo ALSO cross-binds anchor (8.8), orbiter pushed to
12.5 -> overloaded anchor S REPLICATES t~985 (census change). M-cargo roller:
capture works, terminal state destroys the machine. HONEST NEGATIVE for v1.

## T-series plan (tow matching): blind pair (eta12=0) tau1 in {5.64, 5.66},
eta21 in {0.1, 0.2}, cargo rear slot d0=9; plus front slot at 5.64.
Predicted stable tow: (5.64, 0.1) sep*~9.7; (5.66, 0.2) sep*~9.5.

## Tow physics closed out (records 32-52)
- R0 push branch (cargo INSIDE d*): d0=6 pushed out to 7.917 smoothly (record 43);
  d0=5 SPLITS cargo (t=184) — core overlap kills. eta21=0.15 at d0=12: cargo
  reeled but SPLITS at t=470 (well too deep -> deformation). USABLE eta21<=0.1.
- F0 valley response (chan_eps=0.002, records 33-34): M near-onset runs at
  0.074 px/tu; S crawls at 0.0047 px/tu (16x slower). Both reach valley center.
  => per-species rails DO sort by speed; S response ~ vvw-linear class.
- T1 rear tow honest negatives: 5.64 pair kick-transient decays to c~0.008 BUT
  during decay (c>0.017 for first 1200tu) it outruns the well: cargo stranded.
  5.66/5.7 e0.2: pair escapes; on lap 2 the pair PLOWS through the parked cargo
  from behind -> cargo splits (they never bind: front slot is push-out branch).
- T3/T4/T5 b-braked carrier ladder: uniform species-1 isok b slows the blind
  pair: c(b) = 0.059 (b=0), 0.041 (0.01), 0.020 (0.02), 0.0067 (0.03) — but at
  b=0.025 the pair keeps decelerating (c->0.0007 by t=2500: near quasi-static
  stall b*~0.025-0.03, matches machine C3). Cargo at rear d0=8.7: NOT towed even
  at c~0.024-0.01 (T4_b0.025: sep 8.7->30.6 monotone; the pair decelerated
  THROUGH the tow window without capture; drag advanced cargo +1.8px vs blind
  0.0px — the well acts but the fixed point never establishes).
=> KEY numbers: well v_max = 0.0173 px/tu at sep=10.2 (eta21=0.1). A carrier
   holding c in (0.005, 0.015) steadily is needed. The A=4 pair has NO stable
   speed dial in that window (near-onset c is either >=0.02 or collapsing).
