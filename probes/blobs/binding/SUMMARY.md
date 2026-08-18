# M2 blob-binding — SUMMARY (blob-binding searcher)

## Working point (P7s) and the one-dial story
All params inherit M0 (lam=2, k1=-0.7, k3=1, k4=1.5, theta=0.7, Du=1, Dw=20); the binding
point changes exactly TWO dials from M0:

    Dv: 1.0 -> 2.0     (slows/broadens the v-inhibitor tail -> oscillatory tail strengthened)
    tau: 3.0 -> 2.5    (stabilizes the bound pair against a slow antisymmetric escape mode)

Theory guide: linearized spatial eigenvalues about u0 give a complex tail mode
(wavelength ~11 px) that is subdominant at M0 (mono decay 2.51 vs osc 2.20) and nearly
degenerate at Dv=2 (2.96 vs 2.77). Strictly osc-dominant corners of dial-space
(Dv>=4 w/ k3=1.5,k4=1.0; k4>=1.7) all FAILED: pair-triggered replication cascades.
Binding lives in the mono-marginal zone — the oscillatory tail is weak but sufficient.

## B1 existence (re-anchored at P7s, tau=2.5, Dv=2)
- Single blob, L=64, T=10,000 tu: 1 component throughout, area 37 px, peak u=1.11 (amp 1.81).
- Noise: survives sigma=2e-3 (>=1e-3*amp gate) and up to 0.075; blows up (area~900) at 0.09.
- Window: k1 -0.8 OK / -0.6 replicates; Dv 1.5-2.6 OK (area 37->215); tau 2.3-3.9 OK;
  k4 1.35-1.65 OK. >=1.3x width in tau and Dv and k4. PASS.

## B4 binding — the main result
**Bond curve (dx=0.5 continuum, L=48, T=2500):** two-sided convergence to
  d1* = 15.70 +- 0.02 px (~2.1 blob radii, ~1.4 tail wavelengths)
  from d0 = 15.5, 17.0, 18.5 (inward AND outward drift -> restoring force with zero
  crossing and negative slope). Inner starts (9-12.5) sit on a 14.4 plateau for ~1700 tu
  (remnant saddle) then slide out past d* to the box antipode; d0=14 hit the saddle and
  replicated 2->4; d0=20 is beyond the barrier (escapes to antipode: bond basin is
  roughly d in [14.5, 19.5]).
**Second minimum:** none observed for d0<=20 in continuum. dx=1 shows a ladder
  (14.65/16.0/18/20/22...) — that ladder is LATTICE PINNING, said plainly below.
**Unpinning check (the trap in the brief):** d*(dx=1)=15.99 vs d*(dx=0.5)=15.70,
  shift 1.8% < 10% => the d*~16 bond is a continuum object. PASS.
  (Honest caveat: basin STRUCTURE differs across resolution — at dx=1 extra pinned
  states at 14-15 and frozen pairs for d0>=18.5 appear; only the d*=15.7-16.0
  attractor survives refinement.)
**Bond strength (escape vs noise, dx=1, band=3px):** 15/15 runs CENSORED (no escape
  within 4000 tu) at sigma = 0.03/0.042/0.052/0.06/0.075 x 3 seeds. At 0.09 the single
  blob itself is destroyed, so escape is unmeasurable at any usable noise:
  bond lifetime > 4000 tu >> 10x single-blob relaxation (10 x 3.6 tu = 36 tu). PASS (bound
  below by censoring, not fitted).
  The activated (roughly exponential) trend is documented at the tau=3.0 reference point
  in its pinned well: censored (>=3-8k tu) at <=0.042; medians 1310 tu @ 0.045, 632 @ 0.052,
  502 @ 0.06 — escape times fall monotonically with noise as expected.

## tau=3.0 finding (honest instability)
At the original tau=3.0 (P7), the d*=14.65 "bond" seen at dx=1 is a saddle in the
continuum: dx=0.5 pairs hold 14.5-15.0 for ~1000-1500 tu then slide apart along the pair
axis (escape-mode e-fold ~140 tu) to the box antipode. dx=1 stability there was pure
lattice pinning. Lowering tau to 2.5 (or 2.0: d*=15.48; or theta 0.7->0.5: d*=14.38)
kills the escape mode. Raising Dw to 30 does not.

## Multi-blob molecules (tau=2.5, dx=1, T=3000)
- chain of 3 at d*: stable linear molecule, final seps [16.0, 16.0].
- triangle of 3 at d*: stable EQUILATERAL molecule [16.0, 16.12, 16.12].
- (tau=3.0, dx=1: chain3 [15.07,15.07] and square4 [14.4 x4] persisted; triangle drifted
  to a 24.65 pair + far blob — consistent with the tau=3 saddle.)
- No spontaneous rotation of the triangle (orientation constant to 1e-4 rad over 3000 tu)
  => B5 not observed for free.

## Gate verdicts
- B1 PASS (10k tu, noise 2e-3..0.075, window >=1.3x in >=2 dials, non-replicating)
- B4 PASS (d1*=15.7 continuum, two-sided restoring drift, lifetime >4000 tu >> 36 tu,
  unpinned within 1.8%)
- B5 NOT OBSERVED (no free rotation; not claimed)
- B7 PASS at dx=1 (2.3 min/candidate, ~22 tu/s at L=96); dx=0.5 checks 8-14 min each,
  used sparingly and documented.

## Honest negatives / traps hit
1. Osc-dominant tail params (theory-pretty) => replication cascades when pairs interact
   (D_64/C_46/B_66: singles fine, EVERY pair d0=12-31 exploded into 6-20 blobs).
2. Q1 (Dv=1.5, k4=1.7) bound at dx=1 (d*=13.3) but replication-cascaded at dx=0.5 —
   grid-fragile point, rejected.
3. Lattice pinning masquerading as binding: the entire dx=1 attractor ladder except
   d*=16; and ALL of M0's apparent pair attractors (13.27/14.14/15.99 + frozen >=18)
   are pinned states — M0 (Dv=1) has NO certified continuum bond in our data.
4. Seeding convention trap: v,w must start FLAT at u0 (day0 convention); seeding
   v=w=bumped-u kills the blob.
5. d0=14 continuum run replicated at the saddle — binding and replication instabilities
   are close together in this region; k1=-0.7 is only 0.1 from the replication edge.

## Files
- results.json — all campaigns (theory scan, failures, bond curves both resolutions,
  escape data, multi-blob, budget).
- sim.py / runjob.py — engine + job kinds (single/pair/multi/escape); metrics.py locked.
- strips/: fig5 bond curve + attractor map, fig6 escape-vs-noise, fig7 molecule gallery,
  fig1-4 exploratory (tau=3 pinning story, films).
- data/: every raw run JSON + field snapshots (npz).
