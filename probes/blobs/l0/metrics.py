"""metrics.py — LOCKED L0 measurement conventions.
V4 LOCK (stage-3, 2026-02-22, controller-approved priorities):
 - A1 pokes carry kick_px=0.5 ALWAYS in stage-3 workers (stage-2 postmortem:
   symmetric pokes masked 22 travelers; steadiness gate separates coast).
 - Pokes are ACT-INDEXED: every act of a genome is poked separately (audit
   lesson: act-0 of s2_107_48 replicates, act-1 is the c=0.204 traveler).
 - NEW assays: a2_cross (cross-species encounter classes cross_bond/repel/
   approach/kill_i/kill_j/both_die/replicate), stack_probe (n-stack parking:
   stack_parked iff COM net <= 2px AND max blob drift <= 4px over T=2000,
   census intact), radial_profile (angle-averaged u-tail; detects
   sign-changing monotone tails that G0c cannot see).
 - Speed island runs use directed one-dial-at-a-time scans +-5/10% plus
   sigma=0.08 whole-genome jitters, kicked act-indexed A1, T=400.
V3 LOCK (stage-2, 2026-02-19, controller-approved fixes BEFORE pod batch):
 1. chem_box = wavelength+|Re| box ONLY (v2 osc-dominance clause had measured
    recall bug: rejected all 15 alive VVW jitters).
 2. A2: d*>30px => class bond_wrap_artifact (stage-1: fake d*=131.9 co-travel).
 3. A3 = adaptive tau ladder +-{1,2,5}% with early stop per side (was +-20%,
    0 onsets/200; M4 drift windows are ~2% wide). Ladder only on alive cands.
 4. shell_ratios d*/wl_G0c logged per bond; documented band [1.2,1.5] first
    shell (order-of-shell physics; batch 1.348+-.075, controller audit 1.208).
 5. fold_dist = 1-|k1/k1max| logged per act for EVERY candidate.
Stage-1 (s1v3) ran under V2; stage-2 shards run under V3.
V3.1 AMENDMENT (locked after M4-ref ladder validation, BEFORE pod batch):
 - A3 ladder pokes carry kd=0.5px kick (A3_KICK_PX; BF5 lesson: symmetric ICs
   mask traveling regimes) and run T=400 (A3_T).
 - travel requires STEADINESS: c_last/c_prev >= 0.7 (STEADY_RATIO) across the
   two final 150tu windows; decaying kicked transients = new class "coast"
   (near-onset critical slowing). Ladder walk: continue through persist/coast,
   stop side on travel (onset found) or hard fail (island edge).
 - motility flag adds "near_onset" (coast seen on ladder, no steady travel).
 VALIDATION on ref M4 tau=5.7 (single-blob drift threshold 5.748):
   -5%,-2% persist / -1% coast / +1%,+2% coast (critical slowing) / +5%
   TRAVEL c=0.038 steady. Ladder cost ~100 core-s per alive candidate.
V2 LOCK 2026-02-19: first batch (26 candidates, tag s1) ABORTED and DISCARDED
after ref-parity check inside the locked geometry showed the bare u-poke misses
ALL tau=5.7 certified refs (M1 trap: M4/XV/BFIELD die; dressed 0.6 poke revives
all four refs; dress 1.0 kills even M0). A1 is now a fixed two-variant PANEL:
bare poke, then (if not alive) dressed 0.6 poke; best class kept, variant logged;
A2 inherits the winning variant's dressing. Same panel for every candidate =
honest screening. 'persist' with area>=150px^2 reclassified 'domain' (labyrinth
caveat class, cf. M3 species-A continuum trap).

Numerics: IMEX-FFT dx=0.5 dt=0.02 periodic. ASSAY DOMAIN L=64 (N=128) — pair
assays are periodic-image-safe per M2 audit precedent (d0<=20, wrap gap >=44px).
Parity gates ran L=96 (certified geometry).

A1 poke PANEL: act i, Gaussian amp=2.0 sig=3.0 at center on vacuum, T=300, rec 5.
Variant 1 bare (channels at vacuum); variant 2 dressed (identity channels driven
by act get 0.6*W[c,act]*bump — M1 symmetric-centered-shadow convention) only if
variant 1 not travel/persist. Classes: die, replicate (ncomp>=4 early-exit),
blowup, multi (2-3 comps), domain (area>=150), travel (|c|>=C_TRAVEL last 150tu),
persist. Best-of-panel kept (order travel<persist<multi<domain<replicate<die),
variant + bare_cls logged.

A2 pair (first persist/travel act): pokes at d0 in {8,12,16,20} along x, T=400.
Classes: merge (ncomp->1), die, replicate, bond (|d(sep)/dt| < SEP_RATE_EPS over
last 150tu AND (moved>0.5px OR |d*-d0|>0.3)), static (never moved >0.5px — pinned
or neutral), repel (sep still growing), approach (still closing at T).
d* = mean sep over last window; compare to G0c wavelength (shell prediction).

A3 dial (same act): tau of heaviest identity channel *0.8 and *1.2, re-run A1.
motility flag: onset (any travel from non-travel base) / already / fragile
(class changed but not to travel) / robust_static / na.

Constants (LOCKED): C_TRAVEL=0.01 px/tu; REPL_N=4; SEP_RATE_EPS=0.002 px/tu;
A1_T=300; A2_T=400; POKE_AMP=2.0; POKE_SIG=3.0; WIN=150; REC=5.
Funnel: KMAX=3.0 NK=121; EXCITABLE_BAND=0.01; chemistry box 3<=wl<=30,
0.1<=|Re mu|<=1.5, osc decays <=2x faster than slowest monotone mode.

MAP-Elites descriptor (cell key):
  (n_act, n_chan_id, n_chan_tanh, tails_osc, chem_box, poke_classes_joined,
   pair_class_at_d0=12, motility_flag)
Cell exemplar: the funnel-passing genome with the MOST NEGATIVE g0a margin
(deepest vacuum stability) — a robustness choice, documented, not a fitness.
"""
A1_T = 300.0
A2_T = 400.0
ASSAY_L = 64.0
