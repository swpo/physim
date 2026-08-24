# PHASE-5 MEMBRANE — closed bounding structures & cargo-in-cell (SUMMARY)

**Verdicts: R1 PASS — closed single-species blob rings (A4s family) certified N=4-12,
noise-robust, continuum-clean (dx->0.25 shift 0.023%), 10ktu longruns; ring radius obeys
R = d*/(2 sin(pi/N)). R2a PASS — enclosed vacuum measurably differs from outside (interior
u-pool +0.0346 (N5) .. +0.0006 (N12), all >1e-4 floor). R2b DELIVERED — the operational
membrane: v-channel is POROUS (20/20 transmit; gaps are attractive channels), one-way
cross-w channel CLOSES the pores: measured barrier ridge V_w = 0.046*etaw k1-units at the
gap saddle vs 0.82*etaw at cores; confinement boundary mapped in (tau1, etaw). R3 PASS —
THE MONEY SHOT: cargo blob confined INSIDE the closed ring 3000tu under working noise,
4/4 seeds (3 motile + 1 static), ring closed + census frozen at every record, zero-nucleation
control clean. R4 honest map — one-way membrane is structurally rigid (COM drift = noise
floor); legal two-way window exists only at eta21=0.01 where the response is below the
noise floor; all stronger backreaction wirings destroy the cargo (mapped, quantified).
BONUS: alternating-species ring (A-B-A-B, cross-bond braced) certified as a second membrane
material. TRAP FOUND (program-critical): A5 statics under IMEX dt=0.02 are an integrator
artifact — dt<=0.005 required; A4 family exact at dt=0.02.**

## Engine
sim.py = rotor/sim.py (xv twin-world) + per-species Dv freed (mix static families),
one-way/two-way cross-w channel etaw_ij (enters w_i like eta enters v_i; vacuum-exact:
vanishes at u_j=u0), 3-field fast path, cargo-free prerelax (dress the interior vacuum
before pasting cargo), coupling ramp, film recorder. Smoke anchors reproduced pre-campaign:
A5 pair d*->15.71 @dt=0.005 (binding), M4 travel c=0.140785 sep=14.774 (composite exact),
xv rotor omega=0.011064 (rotor exact). Numerics: IMEX-FFT dx=0.5 dt=0.02 L=96 periodic,
stamp paste + kick conventions verbatim from M4/M7. metrics.py LOCKED before certification
(cycle-C_N closure test, crowding flags, G_RING/G_GRID/G_ENCLOSE/G_BARRIER/G_CARGO gates).

## R1 — closed rings exist (pi_1 != 0 by construction, stability by physics)
Working material: **A4s family = tau=2.5, Dv=1.6 (A=4 statics, same stamp as M4), dt=0.02.**
- N=4,5,6,8,10,12 rings seeded at R0=d*/(2sin(pi/N)): ALL pass G_RING at T=5000tu,
  noiseless AND sigma=2e-3: ncomp==N every record, bond graph == cycle C_N every record
  (t>=250tu), no crowding, radius equilibrated. L=96 box caps N<=12 (image gap ~35px).
- Ring law: realized chord 15.39-15.45px ~ pair d*=15.40: a ring is N pair-bonds bent
  by topology. No angular stiffness needed — closure is the brace.
- ATTRACTOR, not balance: two-sided convergence — N6 rings from chord0 13.5/14.5/17/18
  all -> R=15.4015 (0.0001 reproducibility); N8 from 4 starts -> 20.119; N12 from
  chord0 14.5 -> 29.70. Inward pull observed from 13.5 (0.7px inside d*).
- Longruns: N6 and N10 at working noise: 10,000tu, gate PASS (R drift <0.003px/5ktu).
- G_GRID: dx=0.25 reruns N6/N10: R shift 0.023% (<<3% band). Continuum objects.
- A5 family (tau=2.5, Dv=2.0, the deep-bond point): N6 certifies at dt=0.02 but the
  family's statics are dt-artifacted (below); N>=8 inflate + replicate at dt=0.02.
  A4s is the membrane material of record.

## TRAP (program-critical): A5 + IMEX dt=0.02 is an integrator artifact
The A5 pair at dt=0.02 slides THROUGH d*=15.7 (15.56@1500tu, 15.21@2500tu), hits the
14.4 saddle and replicates (~2600tu). Reproduced with composite/sim.py (engine-independent).
dt=0.005: freezes at d*=15.7112 (1e-7/100tu). dt=0.0025: d*=15.7241. The M2 certification
used explicit Euler dt=0.0025 — consistent. RULE: A=5 statics need dt<=0.005 under IMEX-FFT;
A=4 at dt=0.02 reproduces all anchors exactly (c=0.140785). (Retroactively explains
composite's "integrator band" 15.43-vs-15.70 note.)

## R2a — the inside is a different vacuum (enclosure asymmetry)
Azimuthal-mean interior deviations vs outside (outside |mean| ~ 1e-4), certified finals:
| N  | R (px) | u_in - u_out | v_in - v_out | w_in - w_out |
|----|--------|--------------|--------------|--------------|
| 5  | 13.14  | +0.0346      | -0.0109      | +0.0087      |
| 6  | 15.40  | +0.0120      | -0.0040      | +0.0061      |
| 8  | 20.12  | +0.0026      | -0.0021      | +0.0024      |
| 10 | 24.91  | +0.0013      | -0.0012      | +0.0013      |
| 12 | 29.73  | +0.0006      | -0.0005      | +0.0006      |
Sign structure (u,w up; v down) matches stamp-tail superposition; decays with N but stays
above the 1e-4 detection floor through N=12. An enclosed composition-relevant field pool
exists — the "inside affects the whole" lever for phase 6.

## R2b — what makes it a membrane (barrier physics, the deliverable curve)
Cargo = A4 blob (species 1), membrane = the N10 ring (species 2), one-way couplings so the
membrane hands the cargo a static landscape (measured from the actual ring state, k1-units):
- **v-channel (eta12, the rotor binding channel) is POROUS**: the gap saddle has NO ridge —
  U drops from ~0 (center) to -0.0042*(eta12/0.05) INTO the wall: gaps are attractive
  channels; only cores repel (+0.052 at r=R on a blob spoke). Probes: 20/20 TRANSMIT
  (tau1 5.8-6.2 x eta12 {0.05,0.1} x aim {gap,blob}). The ring survives every transit
  (census-frozen 10/10 blobs, cycle closed) — transit-proof but porous.
  eta12=0.1 wall contact REPLICATES cargo (near-onset kick, factory lesson reproduced).
- **cross-w channel (etaw12) closes the pores**: w-halo is monotone-positive (no zero
  crossing — the M7 no-go inverted into wall material). Measured barrier:
  V_w(gap saddle) = 0.046*etaw, V_w(core) = 0.82*etaw k1-units; interior bowl floor
  ~0.0004*etaw at center, cage wall at r~10 (V=0.003*etaw) + main rampart r 18-25.
- **Confinement boundary in (tau1, etaw)** (kicked-at-gap probes, T=2500):
  tau1=5.8 (c~0.055): TRANSMIT at etaw<=0.7; CONFINED at 0.9-1.0 (4 runs: rc_max<=9.4).
  tau1>=5.9 (c>=0.094): TRANSMITS at every stable etaw (<=1.0), often with wall-contact
  replication. => genuine speed-dependent barrier, not a hard wall: barrier ridge
  0.046*etaw k1-units stops the near-onset walker but not free travelers.
- **Nucleation ceiling** (no-cargo controls): the dressed interior vacuum is metastable —
  spontaneous nucleation at etaw>=1.05 (800tu; noiseless); etaw<=1.0 clean; working point
  0.9 clean for 3000tu WITH working noise (seeded control). Membrane strength budget:
  etaw in [0.8, 1.0].
- Wiring hygiene: one-way etaw12 is block-triangular => vacuum dispersion = certified
  single-species (checked -0.196 max growth); IC shock fixed by cargo-free prerelax 500tu
  (instant-paste at etaw>=1.2 nucleates rings of daughter blobs at r=18/29 — an IC
  artifact, not physics; prerelax removes it at every etaw<=1.0).

## R3 — CARGO IN CELL (the money shot) — 4/4 PASS
Config of record: N10 A4s ring (R=24.91) + etaw12=0.9 one-way + prerelax 500tu +
working noise sigma=2e-3 + T=3000tu:
- 3 seeds MOTILE cargo (tau1=5.8, kicked at a gap): confined 3/3 — r_c max 9.3-9.4px
  (cage radius ~10px, never near the wall zone), cargo alive (ncomp1==1 throughout),
  ring ncomp2==10 AND bond-cycle closed at EVERY record. Cargo bounces around the cage
  (median r_c 6.9) — visibly alive in the film.
- 1 seed STATIC cargo (tau1=2.5): parks at r_c=3.3, same gates: the cell holds still cargo too.
- CONTROL: same membrane, no cargo, working noise, 3000tu: ZERO nucleation (the confined
  blob is the seeded one).
- Films: strips/film_R3_cargo_in_cell.gif (376 frames, 1500tu), fig4 frame strip.

## R4 — coupled motion: honest wiring map (mostly negative, quantified)
- One-way membrane (R3 config) is STRUCTURALLY rigid: membrane dynamics never see cargo;
  COM drift 0.006-0.011px/3000tu = noise floor. (Expected; measured anyway.)
- Mutual w (etaw21 0.2/0.5): FAIL — w-w feedback nucleation cascade (cargo replicates
  t~50) or vacuum detonation during prerelax (dispersion +0.058 at k=0 at 0.9/0.9).
- Membrane->cargo v + cargo->membrane v (eta21 0.05/0.1): FAIL — membrane's 10-blob
  v-imprint kicks the near-onset cargo apart at wall contact (t~260).
- eta21=0.01: LEGAL 2-way membrane — 2/2 confined, all census gates pass. But membrane
  response to cargo approaches: nearest-blob excursions -0.024..+0.005px vs per-blob
  noise sigma 0.010px: NO resolvable push (<=2.4 sigma, sign-inconsistent, and the w-cage
  keeps cargo >=15.9px from any membrane blob — its eta*dv halo at that range is ~2e-4
  k1-units, beneath everything). eta21=0.02 already replicates cargo.
- NOISELESS HAMMER (eta21=0.01 vs eta21=0 control, same kick, T=2500, both confined):
  the confined mover DOES move the membrane deterministically — but as a sub-pixel PULL:
  blobs within 15-18px of the cargo deflect radially INWARD -0.014px mean (toward the
  cargo's weak v-well; n=123 records), decaying to +-0.001px beyond 21px; max single-blob
  deviation 0.036px; membrane COM 0.0039px (control 0.0000 exactly). The same coupling
  perturbs the CARGO 10.3px (trajectory divergence vs control) — the wiring asymmetry
  makes the light thing move, not the wall.
=> R4 verdict: RIGID-MEMBRANE NULL at working noise (max response ~1.4x noise sigma);
   deterministic sub-pixel pull certified noiselessly. The push experiment proper needs
   cargo->membrane coupling >=0.02, which replicates this cargo — an architecture
   boundary, documented. Open doors: heavier/multi-blob cargo (splits the coupling
   budget), or a floppier ring material (A5 at dt<=0.005, 4x cost).

## BONUS — alternating-species ring (xv, A-B-A-B)
Nhalf=5 (10 blobs, R=13.27) and Nhalf=6 (12 blobs, R=15.60), mutual eta=0.05, both species
tau=2.5: 4/4 pass 5000tu noiseless + working noise; cross-bond 2N-cycle closed every record;
cross-chords 8.08-8.20 (pair d*=7.976 + curvature stretch); same-species second neighbors
sit at 15.60 ~ their own d*=15.4 shell: DOUBLE BRACING (both interaction shells satisfied
simultaneously). A second, stiffer membrane material with strict compositional order.

## Files
- results.json (all runs, ~90 records, appended live), metrics.py (locked pre-cert),
  sim.py, runjob.py, NOTES.md (predictions written before runs), specs/ (job specs).
- strips/: fig1 ring portraits (N=4-12 u-fields), fig2 R1 certification (attractor
  convergence, ring law, enclosure asymmetry, A5-dt trap), fig3 barrier (V_w landscape,
  (tau,etaw) outcome map, confined trajectory), fig4 cargo-in-cell frames,
  film_R3_cargo_in_cell.gif (THE film).
- data/: track/final/probe npz per run; MEMBRANE_N10/N6.npz canonical ring states;
  Vw_N10.npz + Veff_N10.npz measured landscapes; enc_profiles.npz.

## What phase 6 gets
- A certified CELL: closed membrane + interior pool + confinement, all field physics.
- Membrane material menu: A4s single-species ring (soft, porous-to-fast), + cross-w
  wall dial etaw (0.8-1.0 budget), + alternating xv ring (stiffer, ordered).
- The species-selectivity dial IS the barrier curve: at etaw=0.9, tau1=5.8 cargo is
  confined while tau1>=5.9 species pass — a speed-selective channel for free.
- The A5-dt rule (dt<=0.005) and the w-w feedback no-go for future wiring.
