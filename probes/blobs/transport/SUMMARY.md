# M5-prep TRANSPORT — background fields + transport primitives (SUMMARY)

**Verdicts: P1 GRADIENT/DRIFT PASS (2 coupling modes, curves + seeds + dx/2) ·
P2 SELECTIVITY PARTIAL (quantitative 1.4x, no sign splitting; flip-window sorting is
conditional — see honest negatives) · P3 BLOCKING PASS + CHANNELING PASS ·
P4 NOISE-RATCHET NEGATIVE (deterministic saw conveys one-shot; circulation parked) ·
B7 PASS. Plus one foundational HONEST NEGATIVE: M3 species A is not a continuum
object — replaced by A' (iso-line d=0.65) for all M4/M5 work.**

## World & environment coupling (honesty)
M3 "MAXC" vvw world (5 fields, iso-background line, u*=v*=w*=-0.86756) with ONE static
scalar environment field b(x) (time-independent, built into the PDE's constant terms —
no events, no per-blob code). Node-convention grids; dx=0.5 IMEX-FFT is the working
resolution (M3 dx=1 euler reproduced exactly as control; cmp_m3.py).

Two coupling modes (both are "k1-type" additive drives; declared per run):
- **mode k1**  : k1_i -> k1_i + c_i*b(x). The naive dial. Moves the local Turing/
  stability balance WITH the force -> usable only in a narrow |b| window.
- **mode isod**: displacement along the M3 iso-line: k1_i -> k1_i + c_i*b*UB,
  k4_i -> k4_i + c_i*b (UB=-0.86756). Reaction perturbation is c_i*b*(UB - w), which
  VANISHES on the quiescent background: a zero-footprint force field that acts only
  where a blob already deforms w. Force<->stability decoupled by construction.
  (Discovered here; the designed-for-M5 transport dial.)

b profiles (periodic-safe): tri (slope +-eps, ridge x=L/2, trough x=0) and saw
(asymmetric teeth, frac parameter). Background stays quiescent (no nucleation,
max deviation <1e-4) for all used eps at dx=0.5 (bgcheck.json).

## P1 — single-blob drift curves ("downstream" defined)
**mode k1** (tri, x0=24 on the +eps branch, dx=0.5): UP-gradient drift (toward higher
k1 = softer/bigger-blob side).
  B:  v = +2.64*eps + 27*eps^2 (R2=0.999998, 8 pts eps in [0.00125, 0.0095])
      3 seeds @0.0025 (noise 2.5e-3): v spread <0.5%; dx=0.25 check: -1.1%.
  A': v = +4.43*eps - 169*eps^2 (R2=0.9995, 6 pts) — 1.68x faster at eps->0.
      3 seeds @0.0025: 0.0095/0.0109/0.0113; dx=0.25: +4.8%. (Sublinear: it climbs
      toward its stability edge and slows/fattens.)
  **FLIP bifurcation (B)**: at eps* in (0.0095, 0.010) the up-drift REVERSES:
  v=-0.047 @0.010 (5x the forward speed), blob shrinks to a fast ~17px^2 state and
  parks near the trough. Reproduced at 0.0125 with 3 seeds (v -0.024/-0.047/-0.056).
  This is a second dissipative-soliton branch, not death — flavor conserved.
- Species destabilization limits (k1-mode, the price of this dial): static-window
  edges at dx=0.5 are k1_B in (-1.62,-1.59] and k1_A' in (-1.55,-1.53]; a climbing
  blob destabilizes (area>2x) when local k1_eff crosses ~-1.54 (B) / ~-1.53 (A').
  Practical safe window: |b| <= ~0.03 for B cargo, ~0.015 for A'.
**mode isod** (same protocol): DOWN-d drift (toward smaller d = bigger-species end).
  B: v = -0.906*eps (R2>0.999 per-fit, 5 pts eps in [0.00125, 0.01]); slight
  superlinearity by 0.03 (7-pt through-origin slope -1.04). 3 seeds @0.005:
  -0.00441/-0.00438/-0.00443; dx=0.25 check: -0.00441 (0.6% => unpinned).
  **eps=0.01-0.02 SAFE** (area 30->34; k1-mode had flipped+shrunk at 0.0095):
  the whole tri span L/2=48px is traversable.
  A': v = -0.00585 @0.005 = 1.33x B, same sign.
  eps=0.03: transports 23px then grows at d~0.05 (trough leaves B's iso-window) —
  honest ceiling of the isod dial at THIS tooth depth (b_max=0.72 in d units).

## P2 — species selectivity (the sorting primitive)
- Same-coupling response is same-sign in both modes; magnitude contrast A'/B = 1.3-1.7.
  => **no free opposite-sign sorting in this pair with a shared dial. HONEST.**
- Conditional sign-sorting DOES exist in k1-mode via the flip window: at eps=0.0105,
  B reverses (net -x of the compact blob) while A' still climbs (+x) — demonstrated
  in one two-blob world (sort_demo run; y-separated lanes) — but both species sit in
  their destabilization zones there (B shrunk-state OK; A' fattens after ~3-4 blob
  lengths). Usable only as a short-range separator, not certified as a curve.
- Per-species coupling constants c_i are legitimate environment design (c is part of
  the static field spec, like k4_i): with c=(0,1), B feels the naked ramp
  (v=+0.0154@0.0025, 2.27x the shared-dial speed — shared-w backreaction quantified)
  while A' experiences only the w-mediated drag (v=-0.0064, 3 seeds) — opposite
  DIRECTIONS by construction. The M5 machine should use species-split coupling or
  the flip window for sorting.

## P3 — obstacles: blocking + channeling (self-assembled walls)
Walls are NOT M2 chains (M2's bond point is a different world: single-species Dv=2,
tau=2.5; in the M3 vvw world all pairs repel — no binding). Instead: **stripe walls
self-assembled from the gradient physics itself** — a blob parked at the tri ridge
destabilizes into a y-spanning stationary stripe (the "destabilization" failure mode
turned into a construction tool; area saturates ~316px^2, then STATIC, holds at
lower eps and under cargo impact).
- **BLOCKING (B-stripe wall at ridge vs B cargo, k1-mode):** cargo parks at a
  standoff gap from the wall; monotone standoff(eps) curve (6 pts):
    eps:      0.00125  0.00175  0.0025  0.003  0.00375  0.005
    standoff: 15.74    14.74    14.18   13.39  12.90    (12.9 then cargo fattens)
  3 seeds @0.0025 (14.18/14.34/14.36) + out-of-grid launch x0=16 (14.19: same
  attractor from 32px away). eps_max(blocking) < 0.005: above it the cargo sits in
  its own growth zone at the standoff. Control without wall: passes and destabilizes
  at the ridge. Wall survives every run (x=48+-0.2).
- **CHANNELING (two A'-stripe rails y=8,24, cargo B between, k1-mode eps=0.005,
  couple=(0,1) so rails are force-free):** cargo is centered to the channel
  centerline from any y0 >= 10 (capture curve, 6 pts: y_rms 1.49/1.21/1.02/0.72/0.00
  for y0=10..16, y_end -> 15.3-16.0); at y0=9 (1px from rail) the RAIL captures it
  (rides at y~8.1: rails attract at contact). 2 extra noise seeds identical to 1e-2px.
  Control (no rails): y never centers. Channel-following length: full compact
  transit ~17px (limited by the k1-mode ridge zone, not by the channel).

## P4 — ratchet (stretch)
- **Noise ratchet: honest NEGATIVE.** Saw (f=0.7, eps=0.0025), B parked at apex,
  sigma=0.02/0.03 (blob survives; 8-13x the M3 cert noise), 3000 tu: net |dx| <=
  0.21 px, v ~ 1e-5-1e-6 px/tu. The blob's positional diffusion is essentially zero
  (dissipative soliton = stiff collective coordinate; also cf. M0 pinning) => no
  Kramers hopping on any usable timescale. Unbiased noise does NOT transport here.
- Deterministic saw current (no noise): net motion follows the tooth asymmetry
  (f=0.7: +x, f=0.3: -x mirror; ~12px to the first apex, ~0.0036/0.0067 px/tu mean),
  but the apex is absorbing in k1-mode (level crosses the growth zone), so it's a
  one-shot conveyor, not circulation. Circulation redesign belongs to isod-mode
  (no level-kill) — left for M5 proper with the M4 results in hand.

## Foundational honest negative: M3 species A
At dx=0.5 (BOTH steppers: imexfft dt=0.01 AND day0-euler dt=0.0025) the A blob
(k1=-1.0, k4=1.4) grows 36->3200 px^2 into a labyrinth. M3-A's compact 169px form is
dx=1 LATTICE STABILIZATION (same trap class as M2's dx=1 bond ladder). B is fine
(30.25px^2, 10ktu longrun PASS at dx=0.5). Iso-line rescue scan (d=0.2..0.7):
**A' = d=0.65 (k1=-1.56391, k4=2.05)** stable eps=0 (T=2000; 10ktu longrun: compact
for 8600 tu, then a slow instability grows — documented, area 36.25 constant until
then; d=0.6/0.7 also stable at T=2000, d<=0.55 grow). A' vs B contrast is modest
(36 vs 30 px^2, w-print ratio ~1.2): the 6.8x size-contrast pair does NOT survive
continuum refinement — M4/M5 should either work at dx=1 explicitly-declared, or use
B + A' with reduced contrast, or re-engineer a big species (open item for controller).

## Files
sim.py (vvw + static b(x), k1/isod modes, init_from-composable states, fcntl-locked
results IO) · metrics.py (LOCKED; 2 documented pre-cert amendments: growth guard,
channel compact-phase guard) · runjob.py/drive.py (job runner) · results.json
(114 runs, append-only) · data/*.npz (every track + final fields) · strips/fig0-4 ·
NOTES.md (working log) · jobs_*.json (exact job specs for every campaign).

## Budget (B7)
dx=0.5 L=96 5-field: 5.5-6 tu/s => routine candidate (900-1500 tu) = 2.5-4.5 min. PASS.
dx=0.25 checks 17-22 min (one-offs, documented); 10ktu longruns ~30-64 min (anchors).
