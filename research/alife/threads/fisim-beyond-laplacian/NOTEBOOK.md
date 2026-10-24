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
