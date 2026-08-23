# MEMBRANE — plan of record + predictions (written BEFORE certification runs)

## Goal (phase 5, user direction)
Closed bounding structures: a blob ring with pi_1 != 0 (an inside and an outside),
operational membrane definition (in/out asymmetry + crossing barrier), cargo INSIDE,
then coupled motion. Ladder R1-R4 (see task brief / SUMMARY).

## Engine
membrane/sim.py = rotor/sim.py (xv architecture) with per-species Dv freed
(rotor hardcoded A_i=4). Membrane species can sit at the DEEP-BOND A=5 point
(tau=2.5, Dv=2.0, stamp_P7s) while cargo lives in the A=4 family (any tau).
Single-species fast path (3 fields) when species 2 is absent.
Smoke anchors required before any campaign:
  A5 pair d*->15.7 (binding), M4 travel c=0.1408 sep=14.78 (composite),
  xv rotor |omega|~0.0111 (rotor).

## Design predictions (stamp superposition, computed 2026-02-23, pre-run)
1. Ring geometry: bond length ~ d* => R(N) = d*/(2 sin(pi/N)):
   A5: N=6 R=15.7, N=8 R=20.5, N=10 R=25.4, N=12 R=30.3 (L=96 box: N=12
   diameter 60.7 leaves only 35px of vacuum to the periodic image — marginal;
   N<=10 safe; N=12 needs L=128).
2. Second-neighbor chords 27-30px: halo ~1e-4 — negligible; ring equilibrium
   is set by nearest-neighbor bonds; closure should not be curvature-limited
   for N>=6 (turn angle per bond 30-60 deg; the bond is radially stiff but
   the halo is isotropic, so no angular stiffness => rings are chains bent
   by topology, closure IS the brace).
3. Enclosure (R2a prediction): center-of-ring linear superposition:
   N=6 A5: du=+0.010, dw=+0.008, dv=+0.001 (tails OVERLAP at center)
   N=8 A5: du=-0.005, dv=-0.003, dw=+0.0002 (negative u/v pool inside)
   N=10/12: |du|<1e-3 — asymmetry should fade with N.
   => in/out asymmetry DETECTABLE (>1e-4) for N<=10, strongest N6/N8,
   sign flips between N=6 and N=8 (interesting if confirmed).
4. Barrier (R2b prediction): cargo (xv species 1, eta12>0) sees
   V_eff = -k3*eta12*sum dv2(|x-x_i|): N wells of depth ~eta12*0.048 k1-units
   at 8px off each membrane blob + repulsive cores. The GAP between two
   adjacent membrane blobs (d*=15.7 apart) has a saddle. Expect: slow cargo
   CAPTURED at the r~8 well ring inside; fast cargo TRANSMITS through the
   gap saddle; reflection in between => barrier curve = outcome vs kick/tau1.
5. Cargo-in-cell (R3): cargo parked at ring center is ~15-25px from every
   membrane blob: forces ~1e-3 k1-units — should park. Bigger risk is cargo
   drifting to the interior well ring (r~R-8) and sticking to the membrane
   from inside (CAPTURE) — still "confined", still a pass for G_CARGO, but
   the film wants a free interior blob; may need N=10 (more room) or eta12
   small.
6. Alternating xv ring (R1 fallback): cross-bond d*=7.976 at eta=0.05
   (both tau=2.5). 2N blobs on radius R=7.976/(2 sin(pi/2N)). Same-species
   2nd neighbors at 2*R*sin(2pi/2N)=15.5-15.9 for N=6 (close to the A4
   same-species d*~15.4 — BONUS bracing!). For eta=0.05 statics certified
   clean (rotor RT2); eta=0.1 balloons when static.

## Known traps (inherited)
- dx=1 square4 "molecule" was PINNING-ERA: everything here at dx=0.5, with a
  dx=0.25 continuum check on the certified ring (G_GRID).
- A5 replication saddle at sep~14.4 (d0=14 replicated in binding!) — rings
  must never compress below ~14.5; crowding flag at 12 is the hard alarm.
- Working noise 2e-3; A5 blob dies at 0.09.
- Census-frozen gates: ncomp1/2 exact at every record (no silent splits).
- Barrier probes: kicked A4 cargo at tau1>5.748 self-propels; below, it
  coasts and stops (kick=IC only). Use tau1 as the speed dial via
  self-propelled probes (steady c in 0.06-0.15) — cleaner than kick_d.

## Budget plan
3-field L=96 runs ~20 tu/s => 5000tu ring ~ 4 min; 6-field ~10 tu/s => 8 min.
R1 grid: 2 fam x 4 N x {noiseless,noise} = 16 runs ~ 1.5 h parallel on 10 cores.
Barrier curve: ~12 six-field probes T=2000 ~ 40 min. Longruns 2x.
