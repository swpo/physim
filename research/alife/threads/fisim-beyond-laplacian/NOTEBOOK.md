# NOTEBOOK — fisim-beyond-laplacian

Append-only. Screens: 128² grid (L=64, dx=0.5, dt=0.02), T=200, soup of 6 dressed pokes
(blobkit convention), seed 0, image in `screens/`. "width" = 10-90% front width of the
activator at the mid-level contour, px (m4 baseline 3.39 px).

## Sprint 1 (start 2026-10-24 14:29 UTC)

**S0 Extended stepper + parity.** `xgenome.py` reimplements blobkit `run_genome` stepping
(explicit reaction with old fields, exact Fourier diffusion) and adds optional, vacuum-exact
operators (kern, band, ch, taxis, porous, adv, perm). Parity on m4, one poke, 1000 steps,
f64, noise-free: max |diff| = 3.8e-14 (`parity.py`). Baseline m4 soup: 6 motile spots,
width 3.39 px (`screens/base_m4.png`).

**S1 nonlocal ring kernel replaces w's diffusion (R=4, D=0)** → space-filling spot/stripe
Turing pattern, 44 blobs, occ 0.29. Ring kernel inhibition in place of a 20x-diffusing
inhibitor loses the solitary regime. Negative for individuals. (`screens/kern_w_R4.0.png`)

**S1b extra ring-kernel inhibitor channel on top of m4 (R=6)** → same: labyrinth of spots
(38 blobs). Negative. (`screens/kern_new_R6.0.png`)

**S2 taxis χ=+2 (u climbs grad v, its own slow inhibitor)** → Keller-Segel-like
self-focusing: all bodies collapse/die except one very tight spot (width 1.37 px, the
sharpest front of the sprint) — sharpness at the price of all but one individual.
(`screens/taxis_chi2.0.png`). **χ=-2** (u flees its wake) → spots stretch into travelling
worms/arcs; space-filling. (`screens/taxis_chi-2.0.png`)

**S3 Cahn-Hilliard membrane channel m, deposited by band g=4s(1-s) of the body (passive,
Km=0)** → every motile spot carries a crisp ring of m at its rim plus fading ring wakes
behind it. Bodies unchanged (6 spots, width 3.39). First clean "boundary layer differs
from inside and outside". (`screens/ch_mem_.png`)

**S4 porous (Du 1→0.2 + Dm z²)** → bodies widen and tile space (48 blobs, occ 0.41).
Front sharper (2.39 px) but not individuals. (`screens/porous_.png`)

**S5 advection of all fields by -α grad v**: α=+1 (down the inhibitor gradient) →
spots multiply into a crowded soup of 23-28 small spots; α=-1 → spots shrink and slow, 6-7
survive, front unchanged. (`screens/adv_c0_alpha*.png`)

**S6 containment: cell = S3 membrane + cargo channel c (driven by z_u, D=4, τ=5) whose
diffusion is gated, D_c·exp(-β m).** β=5: cargo mean inside bodies 0.96 vs 0.35 with
β=0 (ablation), cargo far outside ≈0. Bodies, membrane rings, motility unchanged.
(`screens/cell_beta5.0.png`, `cell_beta0.0.png`). Km=-0.5 (membrane activates body):
ring-shaped bodies and loops tile space (negative). Km=+0.5: everything dies.

**S7 cargo feeds back on body (K[u,c]=-kc), β=5**: kc=0.5 → bodies grow into large
membrane-wrapped cells, then elongate into worms and fill space; kc=0.25/0.35 → bodies grow
and DIVIDE (dumbbell membranes), then fill space with rods. β=0 + kc=0.5 → also fills
space, but membrane rings form only around spots and cargo leaks (in/far ratio 2.4 vs 25).
(`screens/cellfb_*.png`)

**S8 + global depletion channel (D=100, τ=10, K=Kg)**: Kg=1 → cells grow, elongate,
divide via a dumbbell-shaped membrane, and the population saturates at ~16 discrete
membrane-bounded cells (L=64); each daughter carries its own ring and cargo.
Kg=3 → no division, 6 cells. (`screens/cellpop_Kg1.0.png`, `cellpop_Kg3.0.png`).
Promoted as `worlds/xcell-div` (ablations `xcell-div-nogate`, `xcell-div-nofb`).

**Render fix.** First xcell-div pack rendered state indices [0,4,5] (body, cargo, global)
instead of [0,3,4] (body, membrane, cargo); regenerated. Worlds now render only
[body, membrane, cargo(, waste)], positive parts of deviations.

**N1 numerics (cellpop Kg=1).** dt 0.02→0.01: same division sequence, 14-15 cells at
t=200 (`screens/cellpop_num_dt.png`). dx 0.5→0.333 (N=192, dt=0.01): 15 cells, same
sequence (`screens/cellpop_num_dx.png`).

**S9 spontaneity.** cellpop from smoothed Gaussian noise on u only (amp 1, σ=4 px, no
planted bodies, channels at vacuum) → 23 cells by t=43, 26-27 by t=300, every one with
its own membrane ring and cargo, packed in a near-hexagonal array
(`screens/cellpop_noise_a1.0_s4.0.png`).

**S10 what does the CH term do?** Radial profiles averaged over cells
(`screens/profiles_containment.png/json`), xcell-a genome, t=150:
- gate β=5 + CH: cargo 1.24 at centre → ≈0 by r≈4 (units); membrane peak 0.56 at r=3
  (the body's half-max radius), FWHM 8 px; m≈0.22 even at the centre.
- β=0: cargo 0.44 at centre, smooth √(Dτ) tail; same membrane.
- β=5, CH off (M=0): membrane is a 3-px line, peak 1.38; cargo 0.90 at centre.
So the band deposit makes the ring; CH *broadens* it to its interface width and caps
it near the m=1 well, which seals better (1.24 vs 0.90). CH is not the sharpening agent
here — the gate (nonlinear mobility) is what makes the cargo boundary sharp.

**P1 packs.** xcell-a (3 seeds): 8/8/8 persistent motile cells, 7.9-8.6 body lengths, no
splits, membrane ring visible in sheet and tracks. xcell-div (3 seeds): 13/15/15
persistent splits, max generation 2, 21-23 cells at T=400, saturation by t≈200; one
cell per seed sometimes becomes a long rod that never divides.

**D1 damage xcell-a, 50% at t=200** (`packs/xcell-a-damage`): the struck cell dies
(8→7); its CH membrane persists ~20 time units as an empty ring ("ghost envelope") then
fades. No repair at 50%. 30% queued.

**S11 turnover: + waste channel q (τ=40, D=2, membrane-gated, inhibits body K=0.3)**,
T=400: cell counts 22 → 19 → 23 → 24; some cells shrink and die while others divide.
(`screens/cellwaste_kw0.3.png`). Promoted as `xcell-turn` (T=800, N=128) with ablation
`xcell-turn-leaky` (waste not gated).

**S12 heredity prototype (`s_her.py`)**: body + membrane + global cap + a *bistable*
cargo activator h (-h³+h-0.2, vacuum = low root), promoted inside bodies by a body
deposit (tilt kb), gated by the membrane, and activating the body when on (kh). Half
the initial cells get an h poke.
- kb=0.15: h-domains shrink to dots and die by t≈200 (curvature beats tilt). Negative.
- kb=0.25 / 0.32 (kh=0.25): two kinds coexist for 300 time units: h-on cells (larger)
  and h-off cells (small) — neither switches. On-cells start to elongate and divide only
  at t≈250-300 (`screens/her_kb0.32.png`).
- kb=0.32, kh=0.4, T=500: on-cells grow into long rods (membrane-wrapped, h fills them)
  that do not pinch; off-cells shrink and vanish under the global cap. Selection between
  kinds, but no reproduction (`screens/her_kb0.32_kh0.4.png`).
- kb=0.32, kh=0.1 + xcell-div cargo drive (kc=0.25): same rods. The bistable h domain is a
  front with positive drive inside the body; it keeps invading and stretches the cell
  instead of letting it pinch (`screens/her_kb0.32_kh0.1_kc0.25.png`). Negative.

**A1 ablation pack xcell-div-nogate (β=0)**: cells STILL divide: 8 persistent splits, max
generation 2, 16 cells at T=400, and they stay motile (23 tracks ≥1 body length, max 8.7)
(`packs/xcell-div-nogate`). The division engine is the RD cargo feedback + global cap;
the gate roughly doubles the number of divisions (13-15 vs 8) and stops motility.

**A2 ablation xcell-div-nofb (kc=0)**: 8 cells, 0 splits, slow motility (3.6 body
lengths). Cargo→body feedback is necessary for division. (`packs/xcell-div-nofb`)

**D2 damage xcell-div, 26% of the largest component at t=200** (`packs/xcell-div-damage`):
the largest component is the stuck rod; after the cut it resolves into round cells and the
count goes 21→22, the rest unaffected. Not repair of the original; damage unjams a rod.

**S13 neutral marker (kb=0.25, kh=0, + xcell-div drive kc=0.25)**: on-cells divide and
both daughters keep h; off-cells divide and stay off (`screens/her_kb0.25_kh0.0_kc0.25.png`).
Promoted as `xcell-her` (+ `xcell-her-sel`, kh=0.1). `kinds.py` tracks cells between
rendered frames and classifies each cell by max h > 0.5.
xcell-her seed 0: on 6→12 (6 on→on+on splits), off 4→9 (5 off→off+off splits), 0 kind
switches, 0 mixed splits (`packs/xcell-her/seed0/kinds.png`, `kinds.json`). Discrete kinds
breed true through two generations. No variation arises (no switching) and with kh=0
there is no selection, by construction.

**P2 xcell-her, 3 seeds** (`packs/xcell-her/seed*/kinds.json`): on 6/5/5→12/9/9, off
4/5/5→9/14/10; on→on+on 6/4/4, off→off+off 5/9/5; mixed splits 0, switches 0 in every seed.
**xcell-her-sel (kh=0.1)**: on-cells never divide (they become rods): 6/5/5→6/5/5; off
4/5/5→9/11/12. Differential growth between true-breeding kinds, but through a morphology
failure.

**P3 xcell-turn, 3 seeds, T=800 (N=128)**: 18/19/16 persistent splits, max generation 5/6/4.
Seed 0: 6 of 8 planted cells die by t≈30 (ghost membranes visible), the 2 survivors
re-populate to 20 cells by t≈350, then the population is static. **xcell-turn-leaky**
(waste not gated): 8 cells, 0 splits, static. So the gated waste is needed for division in
this genome. Unexplained.

**D3 damage xcell-a 30% at t=200** (`packs/xcell-a-damage30`, `screens/damage30_crop.png`):
the struck cell survives; the membrane briefly fills the erased core (t=202), then body,
ring and contained cargo are restored by t≈210. All 8 cells live to the end.

**S14 variation by noise (xcell-her + additive activator noise).** Screens: noise 0.8 →
every cell on, plus nucleation of new cells (24-28); noise 0.3 → structure intact.
Packs `xcell-her-noise0.3`, `xcell-her-noise0.5` (seed 0). First `kinds.py` (cell *max* h)
gave 273 "switches" each way, which is flicker from noise spikes. I changed it to the
cell *mean* of h > 0.5 and re-ran it on all heredity packs (numbers above unchanged except
the start counts, now 5/5, and one t=4 off→on event per pack, which is the IC poke settling).
noise 0.3: on 5→12, off 5→12; on→on+on 9, off→off+off 4, mixed 0; 3 on→off events at
t=68-78. The crops (`screens/her_noise_switch_crops.png`) show these are real: at a pinch
the whole h domain goes to one daughter, and the other emerges h-off and stays off
(unequal partitioning, i.e. loss of the marker at division). noise 0.5: 15 nucleations
(new cells from noise), only 4 splits. Too noisy.

## Sprint 2 (start 2026-10-24 16:37 UTC)

Committee digest: gated mobility is the lab's convergent containment operator; L7 bar =
in-run variation + neutral control with the same mutation rate + >=3 seeds; challenge:
fork a mechanism from another thread. Plan: (1) turnover (consumed/regrowing resource or
maintenance cost) so selection keeps acting; (2) graded, *private* marker fitness (h-on
cells make less membrane-trapped waste) instead of kh (which made rods); (3) selection vs
neutral at the same noise, 3 seeds each; (4) one good movie.
