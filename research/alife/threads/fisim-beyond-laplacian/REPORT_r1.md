# REPORT r1: fisim-beyond-laplacian

## 1. Headline

**I added three vacuum-exact operators to the PhySim/blobkit genome: a front-deposited
membrane channel, a Cahn-Hilliard term, and membrane-gated diffusion. With them, m4 spots
become membrane-bounded cells that keep a fast-diffusing cargo inside. With one more
feedback and a global cap, the cells divide, and the daughters inherit both the membrane
and the contents. Adding a bistable marker gives two kinds of cells that breed true
through two generations: over 3 seeds, 14 on→on+on and 19 off→off+off divisions, with 0 mixed divisions and 0 switches (xcell-her). With weak noise, kinds still breed true but the marker is occasionally lost at an unequal division (6 events over 3 seeds), so variation arises during the run.** The
genome keeps blobkit's conventions: the exact vacuum, IMEX-FFT, dx=0.5, dt=0.02. The
stepper matches blobkit m4 to 4e-14. The spec is in `XGENOME_SPEC.md`.

## 2. Claims

| world | claimed level | strongest evidence | known weaknesses |
|---|---|---|---|
| `xcell-a` | **L4b[L3]**, L4a weak: motile membrane-bounded cells with contained cargo | `packs/xcell-a/seed{0,1,2}`: 8/8/8 cells alive start to end, 7.9-8.6 body lengths; sheet/tracks show an orange membrane ring around a white body+cargo core. Containment: `screens/profiles_containment.png` (cargo 1.24 at the centre, ≈0 beyond the ring; 0.44 with a smooth tail when the gate is ablated) | Bodies are planted (pokes); motility is inherited from m4 (an RD drift instability), not new. The membrane is deposited by a local function of u, so it can only exist where a body front is. Repair (L4a): 30% erasure of all fields is healed (body, ring, cargo) within ~10 time units (`packs/xcell-a-damage30`, `screens/damage30_crop.png`), but this is cheap because membrane and cargo are slaved to the body. 50% damage kills the cell. |
| `xcell-div` | **L6[L3]**: membrane cells divide, daughters carry membrane + cargo, 2 generations | `packs/xcell-div/seed{0,1,2}`: 13/15/15 persistent splits, max generation 2, 21-23 cells; lineage.png; sheet t=54-88 dumbbell membranes pinch | The population saturates by t≈200 (global cap), so it stops at 2 generations. One rod per seed fails to divide. The gate is not required for division (see §3). |
| `xcell-her` | **L6[L3] with true-breeding kinds**, partial L7 (heredity only) | `packs/xcell-her/seed{0..2}` + `kinds.json/png`: on-cells 6/5/5 → 12/9/9, off-cells 4/5/5 → 9/14/10; splits on→on+on 6/4/4, off→off+off 5/9/5, mixed 0, switches 0 (all seeds); sheet: white (body+h) vs cyan-centred (h-off) cells, both kinds pinch with their membrane at t≈70-90 | No variation arises during the run (no switching) and kh=0 means no selection. Kinds are assigned at seeding (half the cells get an h poke). |
| `xcell-her-noise0.3` | heredity + variation (L7 ingredients, no selection) | `packs/xcell-her-noise0.3` (seed 0) + `packs/xcell-her-noise0.3-s12` (seeds 1, 2), `kinds.json`: on→on+on 9/7/8, off→off+off 4/7/8, mixed 0; on→off marker loss 3/2/1 events at t≈68-88. `screens/her_noise_switch_crops.png`: at a pinch the whole h domain goes to one daughter; the other emerges h-off and stays off | Only seed 0's events are checked by eye. One off→on flip in seed 1 (same cell, 12 time units after its loss) is probably classifier flicker. Variation is one-way (loss only). kh=0, so there is no selection. |
| `xcell-her-sel` | **L7 Weak**: true-breeding kinds with different growth | `packs/xcell-her-sel/seed{0,1,2}/kinds.json`: h-on 6/5/5 → 6/5/5 (0 divisions; they become long rods); h-off 4/5/5 → 9/11/12. Sheet: rods (on) vs round dividing cells (off) | Kinds planted, no variation arising, and the 'selection' is the on-kind's morphological failure to divide rather than a graded fitness difference. |
| `xcell-turn` | **L6[L3]**, 4-6 generations | `packs/xcell-turn/seed{0,1,2}`: 18/19/16 persistent splits, max generation 5/6/4; seed0 lineage: 2 founders (6 of 8 planted cells die by t≈30, leaving ghost membranes) → 20 cells | Not sustained turnover: divisions stop once the population saturates (t≈350-550). The early die-off is an IC transient. |

Spontaneity: the xcell-div genome forms ~26 membrane cells from smoothed noise on u alone
(`screens/cellpop_noise_a1.0_s4.0.png`). The packs use planted pokes.
Numerics: dt/2 and dx 0.5→0.333 reproduce the same division sequence and the same cell
count, 14-15 cells at t=200 (`screens/cellpop_num_*.png`).

## 3. Mechanisms and ablations

- **Membrane = front deposit, not phase separation.** `g = 4s(1−s)` vanishes at the vacuum
  and in saturated interiors, so it lays a channel exactly at the body's front. Without
  the Cahn-Hilliard term (M=0) the ring is a 3-px line, peak 1.38. With CH it is 8 px
  FWHM, capped near the x=1 well, and also present at a low level (≈0.2) inside.
  CH *broadens* and caps the membrane. It does not sharpen it.
- **Containment = gated mobility.** `∇·(D e^{−βm}∇c)` makes the boundary of a fast
  (D=4) cargo sharp: it drops from 1.24 to ≈0 across the ring (r≈2-4). Without the gate the
  profile is the RD tail of width √(Dτ)≈4.5. The membrane with CH seals better than the thin
  CH-free line (cargo 1.24 vs 0.90). This is the operator RD cannot replace: it makes a
  boundary sharp for a species whose own diffusion length is larger than the cell.
- **Division = RD cargo feedback + global cap; the gate modulates.** Without the cargo
  feedback (kc=0, `packs/xcell-div-nofb`) there are 0 splits. With the gate removed (β=0,
  `packs/xcell-div-nogate`) cells still divide (8 splits, max gen 2), stay motile, and
  divide about half as often. Without the global channel, cells grow into space-filling
  rods.
- **Heredity = bistable marker retained by the membrane.** A bistable activator h is held
  in its on-state inside bodies by a body deposit (tilt kb). The membrane gate keeps it in
  the cell, so at a pinch both halves keep it. kb=0.15: h-domains shrink by curvature and
  die. kb≥0.32 or kh≥0.25: the h front keeps invading and stretches cells into rods that
  never pinch. Inheritance works in a window (kb≈0.25, kh small).
- **Turnover = membrane-trapped waste.** A slow, gated, inhibiting waste channel ages
  cells. In the packs it mainly kills most planted cells early and lets the survivors re-expand through 4-6 generations. Ablation `xcell-turn-leaky` (waste not gated): 8 cells, 0 splits, almost static. Gated waste, oddly, *enables* division here, presumably because the trapped waste and the trapped cargo together destabilize the cell shape. The mechanism is unexplained.

## 4. Negative results (one line each)

- Ring-kernel inhibition in place of (or added to) m4's fast inhibitor gives a space-filling Turing tiling, not individuals.
- Taxis of u up its own slow inhibitor (χ=+2): Keller-Segel collapse to one very sharp spot (front 1.37 px vs 3.39). All other bodies vanish.
- Taxis down it (χ=−2): bodies become travelling worms and arcs that fill space.
- Porous diffusion (Du 1→0.2 + z²): fronts sharper (2.39 px), but the bodies tile space.
- Advection by −α∇v: α=+1 proliferates small spots (23-28); α=−1 shrinks and slows the bodies.
- Membrane feeding the body (Km=−0.5) gives ring/loop bodies that tile space. Km=+0.5 kills everything.
- 50% damage kills an xcell-a cell (a CH "ghost envelope" persists for about 20 time units). 26% damage to xcell-div hit the stuck rod, which then resolved into round cells. Neither is repair.
- First xcell-div pack was rendered with the wrong state indices (my bug); regenerated.
- Kind classification by cell *max* of h flickers under noise (273 false switches). The cell *mean* is robust.
- Noise 0.5 on activators nucleates new cells from vacuum (15 births) and suppresses division.

## 5. Next sprint

1. **Close L7**: combine noise-driven marker loss (xcell-her-noise0.3) with a *graded*
   fitness effect of h. kh=0.1 made on-cells into rods, so try a small kh that only changes
   division rate. Add continual turnover (death), so generations keep coming instead of
   saturating at gen 2. Then measure per-kind growth curves across seeds.
2. **Self-repair**: give the membrane a source independent of the front, e.g. a gated
   precursor that polymerizes, as in continuous SCL (LITERATURE §2.7.4). Then test 30%
   damage.
3. **A real phase-separated membrane** (FCH/CH with an amphiphile that the body produces) to
   replace the band deposit, so the membrane is an independent field and not a function
   of u.
4. Fork other threads' active-droplet bodies and add the perm gate (the transferable operator).
Needs: nothing beyond the current container. Packs at 160² take about 2.5 min per seed.
