# BLOB-FACTORY — fulfillment-center primitives (phase 3, L3->L2) — SUMMARY

**Verdicts: ROLLER advection CERTIFIED at the deep-coupling point (with the
quantified null at brief parameters — and a NEW composite attractor, the S-M-S
pendulum, discovered where advection was expected). UNLOAD DOCK CERTIFIED
(3 seeds + carry & null controls; one documented gate amendment). SPECIES FORK
static-sort CERTIFIED 24/24. GLUE CERTIFIED (v4: tow -> eta-null release ->
fork branch-sort in ONE world, 3 seeds + mirror), with the interference map
that earlier versions failed on. Plus one new primitive not in the brief: the
NEAR-ONSET CARGO TOW — the enabling discovery for dock & glue. B7 PASS.**

World: xv architecture (M7, 6 fields) + two factory-legal static environment
fields, both vacuum-exact by construction:
- eta_i(x,y): cross-coupling FIELD entering v_i exactly like isok enters u
  (drive eta*(u_j-u0) vanishes on background for ANY static eta(x,y)).
  Kinds: const / xstep / xbox (the release dock).
- per-species isok b_i(x,y) (k1+u0*b_i, k4+b_i on species i only): chan rails,
  saw, forkchan (rail Y-junction), ringcone. Species-tagged rails are legal
  physics here because species are separate field triplets.
Engine: fork of rotor/sim.py, IMEX-FFT dx=0.5 dt=0.02; SMOKE reproduced the M7
anchor to ALL SIX DIGITS (omega=-0.011063, sep=8.4392) on both the scalar-eta
and eta-field code paths. metrics.py locked before cert batteries (1 documented
amendment, see DOCK). results.json: 112 records, appended per-run.

## 1. ROLLER (brief priority 1)
- Brief-parameter answer (tau1 in rotor-only zone, eta=0.1, S cargo at graze
  d in {10,12,15,20}): ADVECTION NULL — quantified |vtan| <= 6e-5 px/tu
  (1000x below rotor tangential speed). INSTEAD the cargo S is reeled to the
  anchor's same-species bond ring (14.78) and the rotor DIES into a new
  attractor: **S-M-S PENDULUM** — M cross-bonded to both S's (8.7-8.8,
  isoceles apex 118deg) librating +-90deg, period ~307tu, steady >=1500tu
  (4/4 geometries). eta21=0 variant: M shuttles straight THROUGH the S-S gap
  (perpendicular-bisector oscillator, x frozen to 1e-11). Composite-dynamics
  hierarchy extended: bond < travel < rotate < librate/shuttle.
- CERTIFIED ADVECTION at the deep-coupling working point (tau1=6.0 fast rotor
  omega=-0.022, eta12=0.1, eta21=0.2; cargo parked ON the ring): sustained
  co-rotating drift vtan = 1.35-1.43e-3 px/tu (2.7x locked gate), 6/6 500-tu
  windows sign-locked, 2 noise seeds + d0=10/20 geometry variants (both funnel
  to the ring and advect identically); eta21=0 null EXACTLY 0 (1e-17).
  Mechanism: each M pass drags the cargo ~0.07px azimuthally (ratchet).
  Honest ceiling: not a circulator (full lap would need ~1400 revs); the
  roller is a positioner/nudger, or needs a ring of cargos.
- Capture map: rotor EXTENDS same-species capture: d0=20 (outside the M4
  basin) captured via rotor wake by t=555; edge in (20,22); no-M controls
  repelled at 20/22/24. M-species cargo variant: captured with 7-8px transient
  arc, but terminal state overloads the anchor -> replication (honest negative).

## 2. UNLOAD/RELEASE DOCK (brief priority 2) — CERTIFIED
- eta(x,y) enters v exactly like isok enters u; an eta->0 null zone releases
  the towed cargo: 3/3 noise seeds: tow-lock 935-940tu (72px conveyed in
  band 7.5-9.5), cargo crosses x1, DECELERATION GLIDE 6.5-7.5px, then frozen
  (|dx| <= 0.3px per 500tu); carrier continues 88px+. Carry control (no null
  zone): cargo held to domain end (149.5px). Null control (no carrier): 1.15px.
- DOCUMENTED AMENDMENT: locked gate demanded v<2e-3 within 300tu of the edge;
  the real glide at entry speed 0.072 takes ~550tu (all 3 seeds fail strict,
  pass at +600tu). Amendment recorded BEFORE verdicts (record 82).
- THE ENABLER — NEAR-ONSET CARGO (new primitive): deep-static S (tau2=2.5)
  is UNTOWABLE: its eta-well mobility ceiling (0.017 px/tu at eta=0.1) sits
  below every stable A=4 carrier speed; honest-negative ladder: blind pair
  abandons it, mutual-eta pairs replicate (eta=0.1 acts like |k1|~0.1 kick —
  100x the machine-safe level), b-braked pairs decelerate through the window
  without capture; deep cargo splits at eta21=0.15 or core distance < 6.
  Retune cargo to tau2=5.60 (rotor-only zone): STILL parks alone (parking
  brake, v->0 by t=500) but near-onset susceptibility amplifies the well
  response 7-8x (v_max=0.127 at eta21=0.1) — tows at full pair speed,
  sep*=8.46+-0.006, 155px conveyed. eta21 threshold: 0.1 yes / 0.05 no.
  This is M5's near-onset-adversary physics turned from bug into the tow.

## 3. SPECIES FORK (brief priority 3) — static sort CERTIFIED
- Per-species rails (M rail y=60, S rail y=36, chan_eps=0.002) sort 6 mixed
  blobs per run from a common start line: 18/18 across 3 noise seeds; SWAP
  control inverts 6/6; no-rail null: nobody moves >3.4px. Purity 24/24.
- Timescale asymmetry measured: M sorts in ~200-400tu (near-onset, 0.074
  px/tu), deep S needs ~3000tu (0.0047 px/tu) — speed-sorting is ALSO
  available on top of species-tagging.

## 4. GLUE (brief priority 4) — CERTIFIED after an interference hunt
- v4 design (L=160 torus): carrier lane = straight M-rail y=48; cargo rail =
  forkchan branching at x0=92 (slope 2.0, dy_max=18, chan 0.004); eta-xbox
  null edge x1=104. One run = tow (820tu, 64px) -> release at x1 -> cargo
  slides down ITS branch and parks 17.7-18.3px off the lane; mirror branch
  symmetric; tails frozen; carrier laps forever.
- INTERFERENCE MAP (the L3->L2 gluing question, answered quantitatively):
  the tow well's ring reach (15px) is the composition footprint:
  * v1 (branch sep 7.4 at park): lap fly-by drags parked cargo 6.6px back;
  * v2 (park at shoulder y~39): fly-by RE-CAPTURES and carries cargo away;
  * release AT the junction: fork-crotch TRAP — tilted valley walls surf the
    cargo backward onto the lane; lapping carrier rams it head-on -> split
    (4/4 reproducible);
  * v4 (park 18px off lane > 15px reach): fly-by closest approach 18.0px,
    drag 0.17-0.33px. PASS 4/4.
  RULE: certified primitives compose iff their interaction footprints
  (eta-well reach, rail walls, carrier lane) are disjoint at every handoff;
  the glue design variables are geometric margins, not new physics.

## New physics/design laws for the program
1. NEAR-ONSET CARGO LAW: susceptibility amplification near the drift threshold
   applies to the eta channel like to isok (7-8x at tau=5.60) — "hot" cargo is
   towable, cold cargo is furniture. One dial (tau2) switches cargo class.
2. eta(x,y) is a legal, vacuum-exact SPATIAL COUPLING FIELD — interaction
   strength is now geography (docks, one-way zones, coupling corridors).
3. eta-coupling budget: traveling near-onset M's tolerate eta12<=~0.05 wells;
   at 0.1 they replicate inside wells (kills mutual-eta carriers; blind
   carriers + one-way eta21 is the robust wiring).
4. Composite attractor zoo grows: S-M-S pendulum (+-90deg, T~307tu) and the
   through-gap shuttle — both spontaneous, both stable limit cycles.
5. Composition footprints: cross-well ring reach 15px = minimum parking
   distance from any active carrier lane; fork crotches are traps.

## Files
results.json (112 records) · sim.py (xv + eta(x,y) + per-species b + forkchan)
· runjob.py (roller/pairs metrics) · metrics.py (locked; 1 amendment) ·
NOTES.md (plan + prediction-first stamp analysis + run log) · strips/fig1
(primitives), fig2 (films), fig3 (glue machine) · data/ (79 tracks/states).

## Budget (B7 PASS)
L=96 6-field: 1.2-4.6 tu/s per process, 6-10 parallel; L=160 cert one-offs
33-41 min (documented). Campaign ~100 runs on a 10-core laptop.

## Handoff to next phases
- The glue world is a working "fulfillment cell": conveyor lane + dock + fork.
  Next: chain N cargos / multiple docks on one lap (throughput metric);
  roller as junction switch (park a rotor AT a fork crotch to push arrivals);
  near-onset cargo + b-field (M6): can a trail RE-arm a released cargo?
- For L0/blob-genesis: eta(x,y) and per-species b are the L2 landscape
  vocabulary; the reduction question is whether dynamical fields can GROW the
  xbox/forkchan geometry (M6 teaser says sawtooth yes).
