# M7 ROTATION — heterodimer rotor (SUMMARY, blob-rotor searcher)

**Verdict: RT1 PASS — the HETERODIMER ROTOR is a certified rotation ATTRACTOR
(spontaneous, basin-robust, 10-point omega dial, grid-clean, 10ktu longrun).
RT2 PASS — first CROSS-SPECIES BINDING, via cross-wired v-channel; w-channel no-go
mechanism quantified. Same-species 3-rotor exists (dial+seeds+grid) but its basin is
knife-edged (honest partial). RT3 ring demo: honest negative — the bond outcompetes
the background ring; the "planetary" film is the heterodimer itself. B7 PASS.**

## The architecture that made it work: "xv" (6 fields)

    du_i/dt = Du lap u_i + lam u_i - u_i^3 - k3 v_i - k4 w_i + k1      i=1 (M), 2 (S)
    dv_i/dt = (u_i + eta*(u_j - u0) - v_i)/tau_i + Dv_i lap v_i        j = 3-i
    dw_i/dt = (u_i - w_i)/theta + Dw lap w_i

Two FULLY PRIVATE copies of the certified M4 world (M0 params; A_i = tau_i*Dv_i = 4
both, so both species share the exact M4 statics and the SAME stamp), coupled ONLY
through the slow-inhibitor drive: each species' v relaxes toward its own u plus a
weak imprint eta*(u_j-u0) of the other species. eta=0 is EXACTLY two copies of M4
(smoke test reproduced the traveling-bond anchor: c=0.14075, sep=14.779). The uniform
background solves the coupled system for ANY eta (cross term vanishes identically at
u_j=u0): background invariance by construction, verified by 6-field dispersion check
(max growth -0.20 at eta=0.1) and by clean 10ktu runs.
Species: **M** (motile dial, tau1 in [5.4, 6.1], Dv1=4/tau1), **S** (anchor,
tau2=2.5 — deep below every drift threshold). Conventions: IMEX-FFT dx=0.5 dt=0.02
L=96 periodic, M4 stamp method + kick convention (sub-pixel Fourier-shift paste; at
grid-aligned positions = M4 protocol exactly).

## Why it works (predicted from the stamp BEFORE the first run; NOTES.md)
The A=4 single-blob stamp gives the v-response to a blob: dv(r) = (1+A k^2)^{-1} du:
core +1.04, ZERO at r=6.1, NEGATIVE ring r in (6,15) (min -0.048 at r~8), dead beyond
15. dw(r) is monotone-positive. Cross-wiring v hands the neighbor exactly this
oscillatory halo as a landscape (-k3*eta*dv(r) in k1-units): repulsive core + well at
r~8 => cross-bond predicted at d* 7-9 (OBSERVED 7.5-8.0). And because v is the
PROPULSION field, S's halo is a self-assembled CIRCULAR RAIL for M: radially
confining, azimuthally flat. Radial mode: bond well. Speed: M's own drift attractor.
Only soft mode: orbit sense. **Rotation is not a delicate trajectory here; it is the
generic escape of the propulsion instability inside a circular constraint.**

## RT1 — heterodimer rotor certification (metrics.py LOCKED pre-cert)
Reference point: eta12=eta21=0.1, d0=8, M tau1=5.7, S tau2=2.5.
- **Spontaneous**: noiseless, NO KICK, from the static cross-bond: rotation self-starts
  from round-off (t~1000tu) and locks. 3 noise seeds (sigma=2e-3, no kick): 3/3
  spontaneous rotors, |omega| spread 0.32%, signs (-,-,+) — CW/CCW symmetry breaking.
- **Basin**: tangential kicks misaligned 70/90/110 deg: all lock to the same |omega|
  (spread 0.03%). Escape noise test: rotor survives sigma=0.01/0.02/0.04 (2500tu,
  omega steady, sep 8.44+-0.3; single-blob death ~0.09) — bond + rotation robust.
- **omega(tau1) dial, 10 points** (5.52..6.10, all cls=rotor, >=4.3 locked revs each,
  sep_std<0.01, steady_rel<7e-3): 0.0035, 0.0047, 0.0052, 0.0074, 0.0093, 0.0111,
  0.0143, 0.0176, 0.0214, 0.0259 rad/tu. Monotone PASS. Locked sqrt-law gate:
  r2=0.9515 (>=0.90 PASS, x_c=5.548). HONEST: a straight line fits better
  (r2=0.9972, slope 0.0369, zero at 5.41) — near-onset the rotor inherits its speed
  from the propulsion attractor tangentially constrained, not from a fresh Hopf
  sqrt-law. Onset bracketed (5.50, 5.52]: at 5.50 omega decays 0.0031->0.0010 over
  8000tu (back to static bond); at 5.52 locks 8000tu at 0.00352.
- **Orbit geometry**: sep dilates with speed 7.87->8.83 px (5.52->6.0; static d* is
  7.5-8.0) — centrifugal-like bond stretch, opposite to the traveling bond's
  contraction (15.4->14.76). tau1=6.1 still rotor-clean 3000tu.
- **Anchor**: S stays put (net <0.9 px per 4000tu; wobble r=0.42px counter-orbit).
  Mechanism decomposition: eta12-only (M feels S; S blind) still rotates
  (omega=-0.0124, S_net=0.0 exactly): S is a passive pivot; the mutual eta21 term
  only adds an 11% drag. eta21-only: NO rotation (M has no rail; coasts to rest,
  sep 19.9 static). The rotor is M's propulsion + S's rail. Backreaction ballast.
- **Grid**: omega(dx=0.25) vs (dx=0.5) at T=1800: -0.011064 vs -0.011063 (0.009%).
- **Longrun**: 10000 tu at reference: 17.4 locked revolutions, sep 8.437+-0.004,
  areas frozen (33.25/33.25) — the rotor is the long-time state (B1-grade).
- **ROTOR-ONLY ZONE (new composite dynamics)**: the rotor spins at tau1=5.52, below
  the M4 pair tau_c=5.636 and far below single tau_c=5.748 — rotation from
  constituents that can NEITHER travel alone NOR travel as a same-species pair.
  With the pair-only zone this completes the hierarchy: single-static < pair-travel
  < rotor-spin thresholds. omega ~ [propulsion] x [1/R rail curvature]: the rail
  softens the drift threshold like the wake-lock did, but ~2x more strongly.

## RT2 — cross-species binding (the missing piece, now present)
- **Bond curve** (statics universal in A=4; run at tau1=tau2=2.5): eta=0.05:
  d0 in {5,6,7,8,10,12,14} ALL -> d* = 7.976 (two-sided, exact to 3 digits, T=2000;
  compact 6000tu). eta=0.1: d* = 7.5-7.6 from d0>=7; HONEST: the eta=0.1 both-slow
  static dimer is METASTABLE — balloons area 33->280 at t~1700tu (d0<=6 balloons
  faster). The ROTATING dimer at the same eta never balloons (10ktu clean):
  **rotation stabilizes the bond** (motion outruns the local-growth clock, as M4's
  travel outran replication).
- **eta map**: 0.05 clean statics; 0.1 rotor-clean; >=0.15 M splits near onset
  (~100tu) and statics balloon; 0.3 symmetric near onset = replication cascade;
  antisymmetric "chase" wiring (+0.3/-0.3, both static): cascade too. Channel
  usable at eta in [0.05, 0.125]; omega(eta) at tau1=5.7: 0.0071/0.0111/0.0124 —
  rail depth is a second speed dial.
- **No-go map (why nothing else binds)**: w-halo dw(r): monotone positive, no zero
  crossing => the shared-w channel (M3 vvw) can ONLY repel, at any coupling sign
  magnitude tried in M3. The v-halo is the unique oscillatory (sign-changing)
  mediator in this model class; cross-binding requires wiring the SLOW channel.
  Quantified: cross-landscape depth 0.05*eta k1-units at r=8 vs w-channel ~+0.5*
  monotone. Design rule shipped: bind through the channel that overshoots.

## Same-species 3-rotor (design ii) — exists, knife-edged (honest partial)
A=4 equilateral triangle side 15.4, curl kicks kd=0.5:
- omega(tau): onset in (5.66, 5.70]; 5 rotating pts 5.70-6.00: 0.0041, 0.0069,
  0.0097, 0.0134, 0.0167 (monotone; omega*R = 0.62..1.11 x M4 c_pair law).
- tau=5.7 locked 6000tu (R=8.991+-0.003, com drift 6e-4 px/tu); 3 seeds at 5.8:
  3/3, spread 0.5%; grid dx=0.25: omega identical to 4 digits.
- NEGATIVES (the M4 frustration confirmed as a BASIN property): curl kicks
  misaligned +-20 deg -> the triangle converts to TRANSLATION (runs away, R->170);
  "chase" ICs fail both ways (5.7 static, 5.9 translation); tau=6.0 rotor decays
  into translation after ~2500tu; 6.1 translates. Same-species rotation exists on
  a measure-thin basin: certification-grade rotation needs the heterodimer's
  structural symmetry breaking (anchored pivot), exactly as hypothesized.
- M4 postmortem refined: same-species N-mers have BOTH modes available; the
  translational wake-lock is deeper (it feeds on the propulsion of ALL blobs
  cooperatively) and swallows the rotational basin at any misalignment. The
  heterodimer removes the translational channel STRUCTURALLY: S contributes no
  propulsion, so co-translation has nothing to pump it — the rotor basin is all
  that is left (70-110 deg kicks and pure noise all land there).

## RT3 — ring-valley orbit (honest negative, replaced by a better demo)
isok ring valley (R0=16, eps=5e-4, machine/ conventions) + b-cone-parked S +
eta=0.1: M IGNORES the background ring — it crosses the valley during its spiral-in
and locks onto the bond rail at r=8.77 with omega=-0.0167 (the free-rotor value at
tau1=5.9). Ring-only control (no bond): no capture at this depth for 4000tu.
R0=20 variant split at 1770tu. FINDING: at machine-safe load depths the
field-mediated bond is a far stiffer circular rail than any static valley —
the "planetary system" demo of the program vision IS the heterodimer rotor
(strips/fig3_rotor_film.png). Deeper rings live in the blob-reshaping regime
(M5 standoff caveats) — parked.

## Files
- results.json — 104 records, appended live (smoke anchor, RT2 grids, RT1 dial/
  basin/seeds/grid/longrun, triangle campaign, ring demos, mech decompositions,
  5 verdict records).
- sim.py (xv engine: 6-field IMEX-FFT, cross-v coupling, sub-pixel stamp paste,
  per-species trackers, ringcone isok load, dispersion check, fcntl results IO).
- runjob.py (job driver; inline cross/poly metrics), metrics.py (LOCKED pre-cert).
- strips/fig1_heterodimer_rotor_cert.png (dial, lock-in, 10ktu orbit, basin+seeds,
  fields+rail contour, noise escape).
- strips/fig2_triangle_crossbond_ring.png (triangle dial + basin failure inset,
  cross-bond curve, omega(eta), ring world, mechanism profile).
- strips/fig3_rotor_film.png (one full period, 5 frames, M red / S blue).
- data/ (49 track npz + locked/10k states + film snapshots).
- NOTES.md (plan of record + stamp-math prediction, written before any run).

## Budget (B7 PASS)
6-field L=96 dx=0.5: 10 tu/s solo, 2.3 tu/s at 8-wide parallel. Routine candidate
(T=1500) 2.5 min solo; dx=0.25 one-offs 38 min (documented); film re-run 1 min.

## What M8+ gets
- CROSS-SPECIES BINDING with a dialable well (eta) — flavor-selective molecules,
  hetero-chains, and rotor-based machines are now buildable.
- The rotor as a machine primitive: a localized angular-momentum source (stirrer)
  with omega dialable 0.0035-0.026 rad/tu by tau1 and eta, position-stable (S pivot),
  self-starting, noise-proof to 20x working noise.
- Design rules: bind through the oscillatory slow channel; break translational
  symmetry structurally (anchored partner), not by fine-tuned kicks; motion
  stabilizes bonds against local-growth metastability.
