# PHASE-3 GENESIS — which L2 landscapes are L1-growable? (SUMMARY)

**Verdicts: FS (functional sawtooth) PASS — the teaser's self-written standing
sawtooth, frozen, FUNCTIONS as a track at NATIVE amplitude: G-SLIDE, G-PARK,
G-BRAKE all pass, dx-refine 0.0%. RS (self-dug racetrack) PASS with an honest
amplitude ledger — an orbiting xv heterodimer writes a closed b-ring (7.1 revs,
G-RING PASS); frozen + anchor removed, the ring alone guides fresh blobs: native
depth guides the slow species (2.68 revs, control straight), x4 captures even the
fast tau=6.0 traveler (7.1 revs, r rms 0.38px); a parked IMMOBILE tau=5.7 blob on
the scaled ring SELF-LAUNCHES into orbit (RT3's negative fully inverted, bond-free).
GN (genesis from noise) HONEST NULL, quantified: zero nucleation events for all
sigma<=0.20 across gamma in [-30,+0.25] x {s1,s2,s3} x tau_b {50,200} x Db {0,0.5};
pure-noise nucleation gap sigma in (0.20,0.50] lands directly in spot soup;
b-fluctuation transfer <=1.6e-3 vs vacuum Turing threshold b*=-1.013 (theory:
vacuum linear stability is gamma-INDEPENDENT — genesis must be finite-amplitude).**

## Engine
sim.py = bfield/sim.py physics (4-field isok b-coupling, verbatim) + freeze_b
(hold b as static environment), binit_from + b_scale (landscape transplant with
shape/amplitude separation), optional 2nd species with M7 xv cross-v coupling
(b sources from & couples to the motile species u1 only; vacuum exact).
Smoke anchors: pair tau=6 c=0.140785 (bfield C0 to 0.000%); xv rotor orbits;
freeze+vacuum surgery exact (u_dev=0.0, b frozen). Conventions IMEX-FFT dx=0.5
dt=0.02; landscapes from bfield/data/T5_ramp_final.npz (the teaser state, L=96... 
actually 192x192 grid = L=96 at dx=0.5) and RS1_end (ring, written here).

## 1. FUNCTIONAL SAWTOOTH (teaser closed: the M5 landscape IS a natural fixed point)
Frozen teaser landscape (tau=6.0 writer, g=-0.05, tb=1000, Db=0, 4000tu ~ 5 laps):
one tooth per lap: fresh cliff at the writer (rise 0.0019 over ~6px behind the
blob... the "cliff" is the fresh-deposit edge), exponential ramp with slope
2.35e-5/px closing the lap (e-fold c*tau_b=125px > L: the lap-decay 0.49 sets
tooth height). Groove is 2D: transverse FWHM 5.5px.

Function tests at tau=5.7 (pair-only zone: lone blob provably immobile on flat b;
control FS5 v=0.0 exactly):
- G-SLIDE PASS: cliff-side start x=48.5 slides -9.3px into the trough (moving-seg
  v 0.0084-0.0166, peak 0.025); ramp-side start x=25 slides +16.3px at v=0.0039.
- G-PARK PASS: both settle at the trough: FS2 x_end=41.6 (trough 43.5, 1.9px),
  tail v 6e-5; FS1b (6000tu) x_end=41.7, v=1e-5. Damped capture oscillation.
- G-BRAKE PASS: sigma=2e-3, parked at trough: stays within [41.1,43.8] 2000tu.
- dx-refine: net_x -11.71 vs -11.70, moving-seg v diff 0.0% (dx=0.25 vs 0.5).

SELF-WRITTEN vs HAND-BUILT (M5 saw eps=5e-4, P=32, frac=0.85; same engine, HS runs):
| quantity              | self-written (native) | hand-built M5    | ratio |
|-----------------------|----------------------|------------------|-------|
| teeth per 96px        | 1 (one per lap)      | 3 (P=32)         | 0.33x |
| tooth height          | 0.0019               | 0.0136           | 0.14x |
| ramp slope            | 2.35e-5/px           | 5e-4/px          | 0.047x|
| cliff slope           | 3.2e-4/px            | 2.8e-3/px        | 0.11x |
| rails                 | FREE (groove FWHM 5.5px; FSRAIL: +6px offset homes to line in 600tu, then parks) | separate chan_eps=0.002 term | — |
| slide v (ramp)        | 0.0039               | 0.0084 (HS1; E5 0.0125) | 0.46x |
| slide v (cliff)       | 0.0084-0.0166        | 0.0038 (HS2)     | 2.2-4.4x |
| brake (sigma 2e-3)    | net -1.7px/2000tu    | net -0.3px/2000tu| both PASS |
| chi = v/|slope|       | ramp 165, cliff 52   | ramp 17, cliff 1.3 | 10-40x |
The self-written track is WEAKER-but-more-efficient: near-onset response is
sublinear in slope, so the hand track wastes slope; and it comes with rails and
park spots built in. Direction convention: self-track's downstream = TOWARD the
fresh edge from behind (the writer's wake pulls followers forward — same sign
as stigmergy attract BF3).

AMPLITUDE LADDER (b_scale x{1,2,4,7.3}, start parked at trough):
x1 parks (brake works), x2 trough-rattles +-2.5px (marginal), x4 ESCAPES and
circulates (c->0.017-0.039 still growing at 3000tu), x7.3 (amplitude-matched to
hand tooth) circulates at c~0.09 with lap time 1255tu. At x7.3 the groove LEVEL
(-0.019 mean) sits in the C3 traveling band: LV1 uniform-b control shows kicked
c=0.0216 (level-motility) but LV2 unkicked stays parked (level alone does not
self-launch); the tooth SHAPE adds direction + 4x speed. Kicked +x (against the
tooth) at x7.3: rides 75px, REVERSES at the shallow end, returns at c=-0.098:
the self-written tooth is a motion DIODE (one-way track). So: the same
self-written shape is a PARKING TRACK at native amplitude and a ONE-WAY
RACETRACK at machine amplitude — b_scale in (2,4) is the phase boundary.

## 2. SELF-DUG RACETRACK (RT3 negative inverted)
WRITE: xv heterodimer (M tau1=5.7 + S tau2=2.5, eta=0.1, d0=8; M7 cert config),
b on M only, gamma=-0.05, tau_b=1000, Db=0: rotor self-starts, orbits S 7.14 revs
in 4000tu at r=8.4 while digging -> STANDING RING in b: annulus r in (5.5,11.5),
depth mean 0.0055 (= tooth-scale!), closure |b|min/|b|max = 0.62. G-RING PASS.
(Writer budget curve: g=-0.05: 7.14 revs, depth 0.0055, closure 0.62 | g=-0.15:
0.61 revs — well-drag slows the rotor 12x — depth 0.0170, closure 0.53 |
g=-0.30: SELF-TRAPS at 0.55 revs, C-arc closure 0.0. Deep rings must be written
slowly at low gamma, not greedily: the bfield lap-digging trap at rotor scale.)

FUNCTION (freeze b, vacuum blob sector = anchor REMOVED, fresh blobs pasted):
- native depth: guides the SLOW species: tau=5.76 (kd=0.3 tangential) locks to
  the ring 2.68 revs/3000tu, r=8.8+-0.5 (RS3c); CONTROL (b erased): exact
  straight line. tau=5.7 parked ON ring creeps -163deg along it (G-CIRC PASS).
  The fast tau=6.0 traveler (c=0.125) is only deflected 22deg (momentum too
  high) — native ring is a guide for near-onset movers, not a wall.
- x4 depth (0.022): FULL CAPTURE of tau=6.0: 7.09 revs, r=9.37, radial rms
  0.38px, omega=0.0179 (G-ORBIT PASS with control).
- SELF-LAUNCH ORBIT (headline): fresh tau=5.7 blob (immobile species!) parked on
  the frozen ring, NO kick, NO anchor, NO bond: self-launches azimuthally and
  orbits: x4 5.4 revs omega=0.0088, x7.3 8.6 revs omega=0.0139 r=8.70+-0.25.
  vs M7 rotor omega=0.0111 (bond+anchor machinery). The ring valley alone now
  does what RT3's static engineered ring could not: the self-dug groove is
  deeper-per-px (matched to blob width 5.5px) and its LEVEL sits in the
  launch-capable band — an autonomously-written, bond-free circular conveyor.

## 3. GENESIS FROM NOISE — quantified honest NULL
Theory first (GN0): vacuum exactness makes the b-coupling QUADRATIC in
deviations: vacuum linear stability is INDEPENDENT of gamma, tau_b, D_b. Uniform-b
Turing threshold (3-field dispersion): b* = -1.013 — but |b| <= |gamma| (tanh
source), and s2 is GATED at blob threshold (chicken-egg: no blob, no source).
Only s1 (linear in u-u0) can transfer noise into b.
Battery (T=1500-3000, allow_empty, L=96): sigma {2e-3..0.20} x gamma {0, -0.5,
-1.2, -2.0, +0.25, -30} x {s1,s2,s3} x tau_b {50,200} x Db {0,0.5}: ZERO
nucleation events in ALL cells (ncomp=0 at every record; 12 runs). Ceilings:
max|u-u0| = 0.316 at sigma=0.20 (vs threshold deviation 0.953); max|b| = 1.6e-3
(s1, g=-0.5, tb=50) and 0.042 even at the absurd gamma=-30 — a factor 24 below
b*. Pure-noise nucleation: sigma=0.50 nucleates at t=5 into 54-59-component spot
soup (replication cascade, not structure); sigma gap (0.20, 0.50] brackets the
threshold; noise >= 0.09 already kills existing blobs, so the nucleation window
CANNOT sustain what it creates (survivor control at sigma=0.10 lives but random-
walks 28px). CONCLUSION: no trails-beget-blobs channel exists in this model
class below the spot-soup cliff: structure needs a seeded blob first. The L1
world is a good vacuum — creation is gated at finite amplitude (consistent with
the program's soliton picture; honest negative, first-class).

## 4. REDUCTION MAP (L2 feature -> L1-growable?)
| L2 feature   | growable? | L1 process                          | fidelity vs hand-built | evidence |
|--------------|-----------|-------------------------------------|------------------------|----------|
| TOOTH (saw)  | YES       | one-way circulation + relaxation (teaser config frozen) | height 0.14x, functions at native (slide/park/brake all pass); amplitude-matched version flips function to racetrack | FS1-FS5, FSB, FSR |
| RAMP         | YES       | trail decay behind steady motion (b=B0 exp(-s/c tau_b)) | slope 0.047x but chi 10x (more efficient per slope) | FS2, HS1 |
| RAIL         | YES (free)| 2D dig: groove transverse profile IS the rail | FWHM 5.5px vs hand chan_eps cap 24px; homing works (+6px -> line) | FSRAIL |
| RING         | YES       | orbiting heterodimer writes annulus (G-RING 0.62 closure) | depth 0.0055 native (= 0.4x hand tooth height); closure-depth trade-off at deep gamma | RS1, RS4 |
| DOCK (park spot) | YES   | trough of self-written tooth = parking brake | native brake ~ hand brake (both hold at 2e-3 noise) | FS4 vs HS3 |
| racetrack conveyor | YES at 4x amplitude | frozen ring/saw + level-in-launch-band | self-launch orbit 8.6 revs (no analog in hand-built M5 — NEW function) | RS3a/b, FS3 |
| blob itself  | NO (from noise) | none below spot-soup cliff | — | GN battery |
Legitimacy note: GROWABLE here = the landscape was written by autonomous L1
dynamics from certified L3 components (traveler, rotor) and then FUNCTIONS
frozen; the freeze itself (gamma->0) is the one exogenous step — the L2->L1
reduction is: L2 static landscapes are snapshots of slow L1 b-dynamics
(tau_b >> everything), exact in the tau_b->inf limit.

## Honest negatives & traps
- RS2a: native ring does NOT capture the fast traveler (momentum mismatch);
  amplitude x4 needed. Speed-matching rule: guide depth must scale with c.
- RS4/RS6: gamma=-0.30 writer self-traps -> open C-arc (closure 0.0); already at
  gamma=-0.15 the well-drag cuts rotation 12x (0.61 revs) though the ring still
  mostly closes (0.53) — ring writing has a budget ceiling like lap-digging.
- FSB x2: neither parks nor circulates (trough rattling) — the ladder has a
  mushy middle, don't operate there.
- Scale surgery (b_scale != 1) is an L2 intervention: results so labeled
  (SHAPE-ONLY findings); native-amplitude rows are the L1-pure claims.
- Genesis null is for THIS coupling class (isok trilinear + tanh source):
  a linear-in-b source term in the u-equation vacuum sector would change the
  story — out of scope (vacuum exactness is the program's honesty anchor).

## Files
results.json (50+ records, append-only, fcntl-locked) · sim.py/runjob.py/
drive.py/metrics.py (locked pre-battery) · data/*.npz (tracks+states incl.
RS1_end ring landscape) · strips/fig1_reduction_map_evidence.png,
fig2_ring_write_phases.png, film_ring_selflaunch_orbit.gif,
film_saw_circulation.gif.

## Budget
4-field L=96: 15-21 tu/s solo, 2.3-4.8 at 3-wide; 6-field (two=True) 6.1 solo.
Routine run (T=2000-4000) 2-11 min at parallelism; dx=0.25 one-off 23 min.
