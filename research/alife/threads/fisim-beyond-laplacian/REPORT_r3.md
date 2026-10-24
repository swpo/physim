# REPORT r3: fisim-beyond-laplacian (final sprint)

## 1. Headline

**The committee's heredity assay gives a clear negative, and the stop rule fires. A marker that
arises inside a cell from a kick is not inherited through division, gated or not. At the pinch,
the membrane-gated marker collapses into one daughter as a small dot; that dot survives and
re-fills its cell, and the sister is unmarked. Without the gate (Dh 0.05 or 0.1 at dx=0.5, and Dh 0.02 at dx=0.25), the marker vanishes from both
daughters by t≈90-120. So the ungated loss is not grid pinning.** The gate keeps an arisen marker
alive in one lineage in 1/3 seeds where every ungated arm loses it in 3/3. That is retention,
not heredity. The cell-filling kick (the one allowed fix) did not change the outcome. L7 is
dropped. Planted, cell-filling markers (xcell-her) remain the thread's only true-breeding kinds.

> **Correction after the committee's final review.** (1) `assay/summary_oncells.json` labels cells
> without periodic merging, so cells cut by the box edge are counted twice: gated_fill seed 0 has 1
> on-cell at t=300, not 2. (2) The split-frame `on_on_frac` from `assay_an.py` must not be quoted.
> (3) My fission mechanism below is wrong. In all three judges' frames the body grows and glides out
> from under a nearly stationary h domain, h is stranded in the neck, both daughters get a dot at the
> inner pole, and at most one dot survives. A planted poke at t=0 in the evo2-N genome fails the same
> way, so "planted vs arisen" is not the variable. The xcell-her success holds only in its own regime
> (its genome and the timing of its planted, cell-filling marks).

## 2. Claims

| world / assay | claimed level | strongest evidence | known weaknesses |
|---|---|---|---|
| heredity assay (`assay.py`, genome xcell-evo2-N) | **L7 dropped** (stop rule) | `screens/assay_hcrops_s0.png` (absolute h scale): the kicked cell fills with h (t=40), pinches (t=60), h collapses to one daughter (t=90) and re-fills it (t=120-300, gated only). `assay/summary_oncells.json`: on-cells at t = 40/120/200/300. Gated fill: [2,3,1,2], [2,0,0,0], [2,0,0,0]. Gated polar: [2,1,1,2], [2,0,0,0], [2,0,0,0]. Ungated Dh 0.05 and 0.1, both kicks: [2,0,0,0] in all 12 runs. Resolved ungated Dh 0.02 at dx=0.25 (cell-filling kick, 2 seeds): [3,0,0,0], [2,0,0,0], lost by t=90 | Only 2 kicked founders per run, so per-division statistics are small; I report on-cell counts over time instead. The dx=0.25 arm has 2 seeds, not 3 (16 min per run). |
| `xcell-evo2-S/N` (r2) | L6[L3] low (committee) | unchanged | r2 headline corrected in place (it omitted 3 on→on+off) |
| `xcell-her` (r1) | L3 high; planted-kind heredity Supported | unchanged; showcase movie | planted kinds, narrow kb window |
| `xcell-a` (r1) | L4b[L3] medium | unchanged | passive compartment |

## 3. Mechanisms learned

- **Why arisen marks fail where planted ones succeed: what matters is domain size at fission,
  not the gate.** A planted mark (xcell-her: σ 2.5, amp 2.2, set into a round cell at t=0)
  fills the cell before the first pinch. A kick-arisen mark in the evo2 genome also fills the
  cell (t=40). But in the elongating cell (my interpretation of the crops, not separately tested), the bistable h front retreats toward one pole as
  the neck forms: the neck is narrow, the body tilt (bdep) is weakest there, and the
  curvature cost is highest. One daughter inherits a sub-critical remnant (lost) and the other
  a dot. The gate holds that dot in place, so it can regrow once its daughter rounds up.
  Without the gate the dot diffuses out before the daughter rounds up. Prediction: anything that
  strengthens the tilt in the neck during fission (purification by growth, cross-inhibition
  so that both halves are re-seeded) should rescue heredity. The gate alone cannot.
- **A split-frame classifier is fooled by pinching domains.** At the pinch frame both halves
  still contain h, so "on+on" is scored, followed by "conversions" in the next frames. Per-time
  on-cell counts and crops at a fixed absolute scale are the honest measure. This also explains
  why r1's planted-kind counts were clean: there both halves really kept h.
- **Dilution vs division time.** With disk erasure at 0.5 per t (≈10× r2), a cell is erased
  every ~40 t, faster than it divides (~50-70 t). Only 6-7 divisions per run, none from an
  on-parent. A dilution-driven selection experiment in this genome needs division faster than
  erasure, and the global cap prevents that.

## 4. Negative results

- Heredity of arisen marks: gated retains in one lineage in 1/3 seeds and never in both
  daughters; ungated 0/3 at Dh 0.05 and 0.1. Cell-filling kick = polar kick.
- Assay at kill 0.5 per t + kick at t=100: no on-divisions at all (6-7 divisions per run).
- The selection experiment (secondary 1) was not run, because the assay failed its pass condition.
- Intrinsic death (secondary 2): not attempted this sprint (time went to the assay and the final deliverables).
- My `assay_an.py` edit broke its indentation once (all analyses failed); fixed and re-run.

## 5. Final deliverables

`FINAL.md` (thread summary), `movies/showcase.mp4` (xcell-her, two true-breeding kinds of
membrane cells; 0.8 MB). Assay frames (seed 0, gated vs ungated, every 6 t):
`assay/*_frames6t.npz`. Full frames regenerate with `python assay.py ARM SEED --kick fill --kick_t 20 --kill 0 --T 300`.
