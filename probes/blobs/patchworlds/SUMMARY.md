# PATCHWORLDS — partition-of-unity world composition: first basic tests

**Verdict: PoU composition is SENSIBLE and works on the first try — with one sharp
new law (seams exert a body force ∝ ∇rho on every localized object) and one
mandatory guardrail (chord pre-flight incl. blob-existence, not just vacuum
stability).** All 5 planned tests + 3 discriminating controls completed; 33 rows
in results.json; no blowups, no seam nucleation anywhere.

Units: lu = dx1-px program units (blob radius ~3, tail wavelength ~11, d*=15.4,
w-halo sqrt(Dw*theta)=3.7). Grid 96x96 lu (192^2 cells, dx=0.5). Patch B =
x in [24,72), tanh seams at 24/72, widths w in {4,12,24} (10-90% = 2.2w).
Engine: `patch_lib.run_patched` — map-aware fork of l0 `run_genome` (per-pixel
maps for lam,k1,u0,Du,tau,Dch,W,K). Spatially-varying diffusion via
**base-implicit + conservative explicit div(dD grad f)** split — this is the
litreview-R1-compliant reference implementation for patchworlds v2 (no naive
D(x)*lap or lap(D·); mass-conserving by construction; stability asserted
dt·max(dD)·4/dx² < 0.5).

## P1 IDENTITY (null test) — PASS
Scalar path bit-identical to `run_genome` (max|dF| = 0.0 over 300 tu). Forcemap
path (every param a constant rho-blend map A|A) max|dF| = 1.6e-14 = float
associativity only. The machinery adds nothing.

## P0 CHORD PRE-FLIGHT (added per litreview R2) — template established
M0→M4(5.8) chord: vacuum dispersion max_k Re λ < 0 at all 21 s (A=tau·Dv spans
3→4); 2-D pokes at s=0.25/0.5/0.75 all give 1 healthy blob. PASS → the P2 seam
interior is habitable.
**Trap found in P3's pair (control C1/C2):** M0→M0(k1=-0.8) chord is
vacuum-stable everywhere, but the s=1 endpoint (and s≳0.9) does not support
blobs at all (poke dies). **Pre-flight must include blob-existence pokes at
endpoints + mid-chord, not just linear stability.**

## P2 TRAVELER AT SEAM — headline: PENETRATE, then seam-force creep
M0 | M4(tau=5.8, c≈0.055) aligned vacuum, both tau and Dv blended.
- **Traveler CROSSES the seam at every width** (w=4/12/24: crosses x=24 at
  t=222/300/950) despite tau_eff(seam)=4.40 being deep sub-onset: momentum/wake
  carries it through the dead ramp in ~100-300 tu. No rebound, no death, no
  splitting, no seam-trapped state. Checklist: penetrate=YES, rebound/pin/
  oscillate/slide-along/seam-state=no.
- **After crossing it never fully stops**: it creeps deeper into A with
  monotonically decaying v (~1e-3-1e-2 lu/tu). **P6 (fresh static blobs, no
  crossing history) proves this is a static seam force, not momentum**: at
  d=4/8/13/20 lu from the seam, v ≈ -(0.37-0.46)·drho/dx — statics are expelled
  from the seam down the weight gradient, range = whole ramp (2.2w). A blob
  "parks" only where ∇rho≈0 (patch centers). The force scale at w=12 is
  ~1e-2 lu/tu max ≈ 20% of the traveler's free speed.
- **Refraction (oblique 45° incidence, w=12): exit is bent to NORMAL** (0.0°,
  tangential speed dies during the ramp transit; total lateral advance 6.7 lu).
  Seams collimate incoming travelers to normal exit — a lens/collimator, the
  litreview's "refraction" entry with a definite sign.
- **One-way by construction**: A is a static world; kicked A-side seeds coast
  0.9 lu and stall (w4_in). Asymmetric transmission comes free with asymmetric
  worlds.
- **P7 tau-only seam (Dv GLOBAL — the litreview-preferred mode): traveler does
  NOT cross.** It decelerates, touches x=26.25, is pushed back, and **parks at a
  stable 8.7 lu standoff inside B**. So the seam composition MODE selects the
  boundary physics: tau+Dv blend → penetrable membrane; tau-only (wiring-only)
  seam → soft repelling wall with a parking orbit. Both are useful primitives
  (gates vs fences).
- Static control at patch-A center: drift ≤0.12 lu over 2000 tu (far-field
  seam force ≈ 0 — force is ramp-localized).

## P3 NON-ALIGNED VACUA (k1_orig -0.7 | -0.8, du0=-0.048) — safe ramp + fence + cliff
- **Settle: PASS both widths.** No nucleation; background → smooth u0(x) ramp
  within 2.1e-3 (w=4) / 7e-4 (w=12) of the naive rho-blend; initial RHS max
  1.25e-3 ≈ controller's predicted ~2e-3 seam source. Wide seams ~4x cleaner.
- **Blob near seam: expelled into the shallow-vacuum world** (x0=16: parks
  x≈11 at w=4; still drifting at x=2 at 2500 tu for w=12). Force is NORMAL to
  the seam; the predicted along-seam drift did NOT appear at this mismatch
  (no dy at all — honest negative).
- **Existence cliff (the real finding):** a blob at x0=40 (rho_B=0.92) dies
  immediately — not seam physics but endpoint physics (C1: pure k1=-0.8 world
  cannot host blobs). Vacuum-misaligned patches partition space into habitable/
  lethal zones with a soft repulsive shoulder. That is a FENCE primitive, but
  it must be designed knowingly (P0 existence scan).

## P4 HALO LEAK (M0 | M4(4.0) static, w=24) — ordinary physics through the seam
- Aligned-vacuum seams carry **zero static structure** (far-field deviations
  <1e-6): wiring PoU is eta(x,y)-clean, as the controller math promised.
- w-halo crosses the seam and decays with length 2.6 lu (vs 1.35 near-blob);
  at 12 lu past the seam it is 4e-5 — leak real but tiny.
- **Cross-world blob-blob interaction: same tail physics as in-world.** At sep
  28 lu: nothing (<0.02 lu). At sep 20 lu: mutual repulsion (A -1.3, B +1.6 lu
  by t=2000) — and the same-world control pair at 20 lu repels identically
  (20→23.5). The seam neither screens nor invents interactions.

## P5 BOND STRADDLING THE SEAM — chemistry survives
- Control (uniform M4(4.0)): locks at d*=15.40, std 0.
- Across M0|M4(4.0), w=24: **bond survives 2500 tu, d* = 15.26 (-0.9%)**.
- w=4 (narrow): bond survives but the WHOLE molecule is expelled ~4.7 lu into
  patch A by the seam force (d* wobbles 15.15-15.53 while sliding). Seam force
  acts on molecules as units; chemistry is robust, geography is not.
- C3: pure-M0 pair at 15.4 is only marginally bound (drifts 15.2-15.5) — the
  straddling bond genuinely bridges a strong-well and a weak-well world.

## Is PoU composition sensible? — YES
1. **The machinery is exact where it must be** (P1 bit-identity; vacuum-safe
   wiring blends confirmed to <1e-6).
2. **Nothing pathological appeared**: no seam nucleation, no blowups, no
   parasitic states at any width, even at w=4 (≪ litreview's recommended 32-48
   at dx=1... note our w=4 lu = 8.8 lu 10-90% width still resolves 17 cells).
3. **Seams are OBJECTS with one clean law**: body force ≈ -0.4·∇rho_B on
   every localized structure (blob or molecule), always pointing down the
   gradient of the world it "belongs less to" (P6 curve). Everything else
   (crossing, parking, refraction-to-normal, one-way-ness) follows from this
   force + each world's own dispersion.

## Implementation implications (evolve-v3 / world-building)
- **patch_lib.run_patched is the reference engine**: maps only for differing
  params; D(x) via base-implicit + flux-form explicit split (document R1).
- **Mandatory P0**: per world pair, scan the straight chord — (a) vacuum
  dispersion, (b) poke/blob-existence at s∈{0.25,0.5,0.75,1}. Cheap (~1 min)
  and it catches the two real failure modes we found (existence cliff) and
  the litreview's blending-element disease.
- **Two seam modes, choose per edge**: full-native blend (tau+Dv) = penetrable
  one-way membrane; wiring-only (D global) = repelling fence with parking
  standoff. This is a design dial, not an implementation accident.
- **Expect ecotone depopulation**: the ∇rho force sweeps mobile objects out of
  ramps; population accumulates at patch centers and at tau-only parking
  shoulders (predicted steady-state structure for evolve-v3 merges: elites
  spatially sorted with evacuated seams; set w wide (≥12 lu tanh) to keep the
  force ≤1e-2 lu/tu and d* shifts <1%).
- **Census metrics near seams**: aligned-vacuum seams need no masking
  (<1e-6 structure); vacuum-misaligned seams DO (u0(x) ramp fools absolute
  thresholds — run_patched already thresholds per-pixel u0/lam maps).
- **Not yet tested** (honest scope): species-set mismatch (union-padding),
  bilin blending, >=2 seams interacting, noise-driven seam crossing stats,
  membrane-world (A4s) x tissue (ds3_014) patch — the natural next experiment.

## Files
- results.json (33 rows: conventions, P0-P7 + verdict rows)
- patch_lib.py (engine), worlds.py (geometry), p0..p7*.py (tests),
  make_strips.py / fig_p6p7.py (figures)
- strips/: p2_traveler_at_seam.png (kymos+tracks), p2_frames_w4_out.png,
  p3_settle_profiles.png, p3_drift.png, p4_halo.png, p5_bond.png,
  p6_p7_force_refraction.png
- data/: per-run npz (tracks, kymos, snapshots, settled profiles)
