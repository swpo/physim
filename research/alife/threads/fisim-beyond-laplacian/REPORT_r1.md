# REPORT r1: fisim-beyond-laplacian

## 1. Headline

**I added three vacuum-exact operators to the PhySim/blobkit genome: a front-deposited
membrane channel, a Cahn-Hilliard term, and membrane-gated diffusion. With them, m4 spots
become membrane-bounded cells that keep a fast-diffusing cargo inside. With one more
feedback and a global cap, the cells divide, and the daughters inherit both the membrane
and the contents. Adding a bistable marker gives two kinds of cells that breed true
through two generations: 11 on→on+on, 0 mixed, 0 switches (xcell-her, seeds 0-1).** The
genome keeps blobkit's conventions: the exact vacuum, IMEX-FFT, dx=0.5, dt=0.02. The
stepper matches blobkit m4 to 4e-14. The spec is in `XGENOME_SPEC.md`.

## 2. Claims

| world | claimed level | strongest evidence | known weaknesses |
|---|---|---|---|
| `xcell-a` | **L4b[L3]**: motile membrane-bounded cells with contained cargo | `packs/xcell-a/seed{0,1,2}`: 8/8/8 cells alive start to end, 7.9-8.6 body lengths; sheet/tracks show an orange membrane ring around a white body+cargo core. Containment: `screens/profiles_containment.png` (cargo 1.24 at the centre, ≈0 beyond the ring; 0.44 with a smooth tail when the gate is ablated) | Bodies are planted (pokes); motility is inherited from m4 (an RD drift instability), not new. The membrane is deposited by a local function of u, so it can only exist where a body front is. 50% damage kills the struck cell (no repair). |
| `xcell-div` | **L6[L3]**: membrane cells divide, daughters carry membrane + cargo, 2 generations | `packs/xcell-div/seed{0,1,2}`: 13/15/15 persistent splits, max generation 2, 21-23 cells; lineage.png; sheet t=54-88 dumbbell membranes pinch | The population saturates by t≈200 (global cap), so it stops at 2 generations. One rod per seed fails to divide. The gate is not required for division (see §3). |
| `xcell-her` | **L6[L3] with true-breeding kinds**, partial L7 (heredity only) | `packs/xcell-her/seed{0..2}` + `kinds.json/png`: FILL_HER | No variation arises during the run (no switching) and kh=0 means no selection. Kinds are assigned at seeding (half the cells get an h poke). |
| `xcell-her-sel` | L7 attempt (selection) | FILL_SEL | FILL_SEL_W |
| `xcell-turn` | L6 with turnover (death + division) | FILL_TURN | FILL_TURN_W |

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
  cells. Cells shrink or die while others divide (screen counts 22→19→23→24). FILL_TURN_MECH

## 4. Negative results (one line each)

- Ring-kernel inhibition in place of (or added to) m4's fast inhibitor gives a space-filling Turing tiling, not individuals.
- Taxis of u up its own slow inhibitor (χ=+2): Keller-Segel collapse to one very sharp spot (front 1.37 px vs 3.39). All other bodies vanish.
- Taxis down it (χ=−2): bodies become travelling worms and arcs that fill space.
- Porous diffusion (Du 1→0.2 + z²): fronts sharper (2.39 px), but the bodies tile space.
- Advection by −α∇v: α=+1 proliferates small spots (23-28); α=−1 shrinks and slows the bodies.
- Membrane feeding the body (Km=−0.5) gives ring/loop bodies that tile space. Km=+0.5 kills everything.
- 50% damage kills an xcell-a cell (a CH "ghost envelope" persists for about 20 time units). 26% damage to xcell-div hit the stuck rod, which then resolved into round cells. Neither is repair.
- First xcell-div pack was rendered with the wrong state indices (my bug); regenerated.

## 5. Next sprint

1. **Variation + selection for L7**: put a small noise term on h, or a lower barrier, so
   kinds occasionally switch during the run. Also add continual turnover (waste or
   death), so generations keep coming instead of saturating at gen 2. Then measure
   per-kind growth with kh>0.
2. **Self-repair**: give the membrane a source independent of the front, e.g. a gated
   precursor that polymerizes, as in continuous SCL (LITERATURE §2.7.4). Then test 30%
   damage.
3. **A real phase-separated membrane** (FCH/CH with an amphiphile that the body produces) to
   replace the band deposit, so the membrane is an independent field and not a function
   of u.
4. Fork other threads' active-droplet bodies and add the perm gate (the transferable operator).
Needs: nothing beyond the current container. Packs at 160² take about 2.5 min per seed.
