# NOTEBOOK: chemotaxis-motility

Sprint 1 started 2026-10-24 14:31 UTC. Quick screens: `screen.py` (8 snapshots per channel + a
time-coded overlay of rho, blue = early, red = late; prints a late-half blob speed).
Screens are in `screens/`, and file names encode the parameter overrides.

## kstrail: Keller-Segel spots + self-secreted slow repellent ("trail")
`worlds/kstrail/world.py`. rho (volume filling) climbs a fast attractant a and descends a slow repellent h; both are secreted by rho.

- **v0, volume filling via cell-centred (1-rho) factor + clip**: lost 80% of mass to clipping. Fixed
  with a face flux v*rho_up*(1-rho_down) (exactly conservative, bounded). *Lesson: do not clip a
  conserved quantity.*
- **chi_h sweep at rho0=0.15** (`ks_*`, `kstrail_ch*`): chi_h <= 0.3 gives a static spot lattice that
  coarsens; chi_h 0.8 gives dim moving crescents in a crowded sea. At 0.5-0.65 small blobs move
  but are absorbed into large saturated (rho=1) spots, which never move. **Saturated bodies are immotile:**
  the repellent under a flat plateau has no gradient across the body.
- **low mass** (`kl_*`, rho0 0.05): coarsening stops at small, unsaturated bodies, and all of them swim
  (late-half speed ~0.25 px/t, 100% moving). But headings snap to the grid diagonals.
- **direction test** (scratch `dirtest.py`: one blob, trail seeded behind at angle θ): first-order upwinding,
  then MUSCL: a blob seeded at 20° turns to 45°, and one at 0° dies. Grid anisotropy. Fix: resolve the body
  (all lengths x2: Dr 1.2, Da 4, Dh 0.2, chi x4) plus a MUSCL/van Leer flux. Afterwards 0° stays at 0° and 20°
  wanders between 30 and 60° (no snapping), and the swimmer persists. Speed ~0.5 px/t.
- **scale-2 screens** (`k2_*`, 128²): chi_h 4.8 gives ~8 comet swimmers that form from noise; chi_h 6.4 gives
  3-5 swimmers; chi_h 8 gives a turbulent sea (no individuals). Window ~4.8-6.4.
- **pack** `packs/kstrail` (seed 0, 128², t=600): formation route spot → expanding ring (rho rim,
  h inside) → ring ruptures → crescent swimmer (tracks.png #0). Swimmers are polar: a bright rho crescent
  in front and an h cloud behind. Shape is kept for >250 t (#17). They collide, merge and split, so no track
  lives longer than 50% of the run. Crowded at 128².

## forager: chemotaxis up a consumed, regrowing nutrient + growth/death
`worlds/forager/world.py` (parent kstrail). The repellent trail is replaced by nutrient depletion.
- Linear growth: spots form, then starve, and the population goes uniform. Quadratic (Allee) growth with a (1-rho) factor:
  dense bodies cannot grow. Pressure (kp rho^3) instead of volume filling: round bodies, but explicit
  instability/NaN at high density. Hill growth + volume filling: large, static, saturated blobs that grow.
  Fast nutrient diffusion keeps depletion symmetric, so spots do not move (fo_e/f lattice).
  Slow nutrient diffusion leads to extinction (fi/fh). All at scale 1 (under-resolved). To revisit at scale 2 and low density.

## kstrail promoted (192², 3 seeds) — `packs/kstrail`
- Defaults: scale-2 lengths, chi_a 24, chi_h 4.8, rho0 0.05. All three seeds: spontaneous swimmers (9-11 at the end),
  22-25 tracks moving >= 1 body length, up to 23 body lengths, speed ~0.5/t. seed1 tracks.png: #15 is the same
  polar crescent from t=132 to 600 (rho front, h cloud behind); #33 is born from a two-lobed body at t~261 and persists.
- Weaknesses seen: collisions merge swimmers, and large merged bodies (the triangle in seed1, top-left) become
  saturated and immotile. They can re-shed swimmers ("persistent splits" 3-5), but over long runs immotile
  aggregates may win. Not tested beyond t=600.

## pursuit: two kstrail species with cross-taxis — `worlds/pursuit`, `packs/pursuit` (160², 3 seeds)
- Predators (q) climb the prey attractant (chi_y 8); prey descend the predator attractant (chi_x 8). No kinetics
  (k = g = 0): pure pursuit and evasion, each species conserved.
- Swimmers of both species form from noise. **Predators lodge in the concave rear of prey crescents and the pair
  travels together** (chaser and fleer at equal speed: a bound pursuit composite). Pairs dominate the late frames.
- `pairing.py`: late-half fraction of predator bodies touching prey is 0.86 / 0.91 / 0.76 (seeds 0-1-2), against
  a shuffled-prey null of 0.27 / 0.27 / 0.31.
- Ecology attempts (predation k, yield e, Allee prey growth on nutrient): every combination tried so far goes extinct
  (pp1, pp2, gr1, gr3, gr4). The prey die in the diffuse phase before swimmers condense (Allee growth is ~0 at rho0=0.05).
  gr2 survived but grew into large immotile amoeboid blobs. Added a `t_on` switch (kinetics start after
  condensation) to separate the two phases.
