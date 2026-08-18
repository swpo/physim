# M3 FLAVORS — two blob species in one world (SUMMARY)

**Verdict: B1 PASS (both species) · B3 PASS (100% classification, flavor conserved) · B7 PASS w/ caveat.**

## The world (pair "MAXC", architecture "vvw", 5 fields)

    du_i/dt = Du_i lap(u_i) + lam*u_i - u_i^3 - k3*v_i - k4_i*w + k1_i    i = 1 (A), 2 (B)
    dv_i/dt = (u_i - v_i)/tau + Dv lap(v_i)
    dw/dt   = ((u1+u2)/2 - w)/theta + Dw lap(w)          <- ONE shared long-range inhibitor

shared: lam=2, k3=1, tau=3, theta=0.7, Dv=1, Dw=20, L=96 periodic, dt=0.01 (day0 conventions)
species A: k1=-1.0,      k4=1.40, Du=0.65   ->  big broad spot,  area 169 px, peak u=1.10
species B: k1=-1.65067,  k4=2.15, Du=0.65   ->  small sharp spot, area 25 px, peak u=1.20

Design rule that made it work — **iso-background line**: pick species dials on
k1_i = -1.0 + d_i*ub, k4_i = 1.4 + d_i with ub = -0.86756 (A: d=0, B: d=0.75). Then the
homogeneous background is the SAME for both activators (u*=v*=w*=-0.86756), stays
linearly stable (max growth -0.28 over k in [0,3]; 5x5 dispersion check in flavors_core),
and each species sees the same quiescent medium while having different local physics.

## Architecture choice (option (a); by experiment, not fiat)
- **vvw (chosen)**: u1,v1 | u2,v2 private, w shared. Each species subsystem is EXACTLY the
  certified M0 model; species only talk through w -> clean inter-species repulsion.
- **vw (shared v, 4 fields): FAILED** — no stable lone-spot island anywhere in the scanned
  box (k1 in [-1.3,-0.5] x k4 in [1,4]): shared v adds short-range cross-coupling that turns
  every spot into a domain or destabilizes the background. Honest negative, probe1_arch.json.
- **w-only (3 fields)**: has spot islands, but drops v = the drift-bifurcation dial that
  M1/M4/M5 need. Kept as documented fallback, not shipped.
- (b) painted type-field: rejected per brief. (c) sign classes: unnecessary, (a) worked.

Subtlety: with the average drive (u1+u2)/2, a LONE spot drives w at half weight
(k4_eff = k4/2), so the M0 island relocates — the old M0 point dies as a lone species in
this world. The iso-background construction re-anchors everything.

## B1 — existence (cert_b1.json, 8/8 PASS)
- 1e4 tu clean AND 1e4 tu at sigma=2.5e-3 (sigma/amp = 1.2-1.3e-3 >= 1e-3), per species:
  alive, ncomp==1 at every 100-tu record, area constant to the pixel (A:169, B:25).
- Extra noisy seeds (1,2) at 2e3 tu: pass. dt/2 check: identical area/peak. Non-replicating.
- Parameter windows (contiguous persistent interval around locked value, T=300 probes):
  A: k1 1.32x · k4 1.32x · Du 2.38x · theta 2.22x · tau 2.67x  -> 5 dials >= 1.3x
  B: k1 1.28x · k4 1.29x · Du 2.00x · theta >=2.56x · tau >=4x -> 3 dials >= 1.3x
  (honest: B's own k1/k4 are 1.28-1.29x, just under the bar; requirement is >=2 dials.)

## B3 — port distinguishability (cert_b3.json, metrics.py LOCKED pre-cert)
Probe = 5x5 patch time series (5 samples over 60 tu) at the activity peak, noise on.
Three classifiers, constants frozen from clean lone calibration BEFORE certification:
1. `classify_full` — per-channel patch amplitude (du1 vs du2):            **20/20**
2. `classify_wport` — **w-field ONLY** (the one field both species share, i.e. the
   physical port any other blob can feel): w-bump half-width footprint:    **20/20**
3. `classify_size` — field-agnostic total-activity footprint:              **20/20**
Same-world check (A+B coexisting, probe each): 10/10 on both. Accuracy 100% >= 95%.
Signatures: 6.8x area, 3.9x w-footprint (143 vs 37 px), 2x w-peak (0.45 vs 0.23).
**Honest negative: blobs are non-oscillatory** (patch amplitude rel_std ~ 1e-4 under
noise) — local frequency is NOT a usable signature in this world; do not sell it.

## B3 — encounter table (cert_encounters*.json; 3 seeds each, sigma=2.5e-3, T=2000)

| pair | d0=10 (3 seeds)         | d0=6 (3 seeds)          |
|------|--------------------------|--------------------------|
| A+A  | **repel** -> sep 15.5-15.7 | **merge** -> ONE A-blob (174 px ~ lone 169) |
| A+B  | **repel** -> sep 13.1-13.2 | **repel** -> sep 11.1-11.2 |
| B+B  | **repel** -> sep 15.0      | **repel** -> sep 13.0      |

- Flavor conserved in ALL 18 runs: no conversion, no annihilation, census clean.
- Only non-conserving event: same-flavor A+A merge at strong overlap (2->1, deterministic
  across seeds) — documented conversion-free coalescence, standard dissipative-soliton behavior.
- Inter-species repulsion is w-mediated (B sits in A's w-bump and vice versa); the
  negative "mass" in the other species' channel under a blob is linear field response
  (dip below background), never a thresholded object.
- Encounters are deterministic up to noise (identical outcomes across seeds) — honest
  note: at sigma=2.5e-3 noise barely moves these blobs (lattice-pinned, cf. M0/M1).

## B7 — budget
282-320 us/step (5 fields, L=96, single core numpy) = 11-14 tu/s.
Routine candidate (800 tu pair world) = 71 s < 5 min. 1e4-tu B1 certs = 12-13 min each,
run 8-wide in parallel (~13 min wall). tu/sec documented per run in cert_b1.json.

## What M4/M5 get
- Two certified species with 6.8x size contrast and a per-species (k1_i, k4_i, Du_i) dial set
  on an explicit iso-background line: differential mobility/background response is available
  by construction (B's smaller w-footprint makes it the natural "cargo" flavor).
- Each species subsystem is exactly M0: M1's drift-bifurcation dials (tau per species if
  split) apply per species. tau windows: A 1.5-4.0, B 1.5->6.0 — room for species-selective
  drift (tau_A != tau_B) WITHOUT breaking existence.
- Interaction summary for machine design: A-A contact-repel/merge, B-B repel, A-B repel at
  ~11-13 px preferred gap. No binding here (M2's job): pure repulsion at all tested ranges.

## Files
flavors_core.py (physics), metrics.py (LOCKED classifiers + census), probe1-13 (search
trail incl. failures), cert_b1/b3/encounters/window/budget (+ .json/.log), strips/
(species_portraits.png, port_signatures.png, encounter_strips.png), results.json.
