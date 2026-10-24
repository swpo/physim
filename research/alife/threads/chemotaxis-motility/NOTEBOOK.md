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

## Pursuit ablations (seed 0, 160², `packs/pursuit_abl_*`; overrides recorded in each FACTS command line)
| variant | predator bodies touching prey (late half) | shuffled null |
|---|---|---|
| full (chi_x = chi_y = 8) | 0.86 | 0.27 |
| no pursuit (chi_y = 0) | 0.58 | 0.58 |
| no evasion (chi_x = 0) | 0.99 | 0.21 |
| neither | 0.56 | 0.52 |
- Pairing is caused by pursuit (chi_y): without it, contact is at chance. Without evasion, predators are carried *inside* the
  prey swimmers (white overlap in the sheet), so the contact is total but the predator no longer sits behind the prey.
  With evasion, the predator sits in the concave rear, so evasion is what shapes the pair.
- Without pursuit, predators (half the prey's mass) condense late and stay as round spots and expanding rings: the prey
  signal speeds up predator condensation.

## kstrail controls (seed 0, 192²)
- `packs/kstrail_abl_noh` (chi_h = 0): ~30-60 static round spots that coarsen slowly; max 2.5 body lengths; 0 splits.
  **The trail repellent is the propulsion operator.**
- `packs/kstrail_dthalf` (dt 0.025, spf 120): same picture, 24.6 body lengths max. The reported speed is halved only because
  labkit converts frames to time with META dt (0.05). Numerically robust to dt.

## toxtrail: the repellent trail is also toxic (fork of kstrail) — `worlds/toxtrail`
- Kinetics from t_on = 150: cooperative growth g rho^3/(rh^2+rho^2) and death kd h rho.
- kd 0.005 (`packs/toxtrail_screen`, 160², t=800): ~9 swimmers maintained, total mass oscillating around +20%;
  27 splits and 25 merges (turnover). Clumps formed in collisions lose mass and re-shed swimmers. kd 0.01: mass falls 80%
  but a few swimmers survive (one travels 35 body lengths).
- Ablation chi_h = 0 (`packs/toxtrail_abl_noh`): static spots shrink stepwise and some vanish (43 → 20 bodies, mass -60%),
  then plateau. **Motility helps survival but static spots can balance at a smaller size.** The prediction "static dies" is only
  partly confirmed.

## toxforage: toxtrail + consumed, regrowing nutrient (metabolism)
- g 0.1, c 2, r 0.01, Dn 0.5 (160², t=800 screen tf1): ~10 swimmers persist, each with a red waste tail and a dark
  depleted-food wake. 24 tracks move >= 1 body length (max 20.8). Mass settles 42% below the initial value.
- But the r = 0.01 3-seed pack (first `packs/toxforage`, since replaced) declined slowly in every seed (rho 1 → 0.58/0.52/0.32 by t=800),
  so it is not a steady state. r sweep at 128², t=1500: r 0.03 declines (1 → 0.54), r 0.06 is stationary (1.0-1.5, 6-7 bodies).
- **Promoted toxforage with r = 0.06** (`packs/toxforage`, 160², t=1200, 3 seeds): rho/rho0 at t=300..1200 stays at 1.1-1.4 / 1.5-1.9 /
  1.0-1.2, with 9-14 bodies throughout. Individuals live ~300-500 t (tracks.png #26, #125, #144) within constant turnover
  (collisions → clumps → clumps poisoned and re-shed swimmers). No track spans the whole run.
- Ablation r = 0 (`packs/toxforage_abl_r0`): rho falls to 0.14 and bodies 11 → 4 by t=1200, still falling. **The population depends
  on the regrowing nutrient.** Note: the global nutrient stays ~0.9 at r 0.06; food is depleted only locally (the wakes).

## Damage tests
- labkit `--damage 100:0.5` on toxforage seed0 (`packs/toxforage_damage`) hit the largest component, which is a 416-px clump, not a
  swimmer. The hole closed within one frame and the clump re-shed crescents within ~30 t (`damage_crops.png`). Not a clean test.
- `damage1.py` damages ONE median-size swimmer (~40-47% of its mass erased through the centroid) and follows it next to the undamaged run.
  toxforage seeds 0 and 2 (`screens/damage1_toxforage*.png`): the body re-forms a compact polar crescent within ~12-18 t and is
  indistinguishable in size from the control by ~50 t (growth refills it). Seed 1: the damaged body was attached to a clump and
  follows the control's fate. kstrail seed 1 (`screens/damage1_kstrail.png`, mass conserved): it re-forms a smaller swimmer
  that goes through the same polarity phases as the control.

## kstrail ±10% jitter (seed 0, 160², t=600; /tmp only, not packed)
- chi_h 4.32 / 5.28, chi_a 21.6 / 26.4, rho0 0.045 / 0.055: every variant gives spontaneous swimmers that move 8.9-15.5 body lengths
  (13-19 moving tracks). chi_a 21.6 condenses later and shows the expanding-ring stage most clearly (t 210-234).

## ecology: pursuit + toxforage kinetics (predation k 0.2, yield 0.5, toxic trails for both)
- `packs/ecology` (192², t=1000, 3 seeds): coexistence in all seeds, ~21-24 prey and ~18-20 predator bodies after t=250.
  Predators touching prey 0.93 / 0.96 / 0.94 (null 0.30-0.34): almost every predator rides a prey crescent while depleting
  its food (black nutrient wakes).
- `packs/ecology_long_160` (t=2000): stable coexistence, ~14 prey and 12 predator bodies, small fluctuations, **no sustained
  Lotka-Volterra cycles**. One overshoot peak after kinetics switch on (prey peak t~210, predators t~270), then damped.
  Totals are strongly correlated with a lag of 20-35 t (r 0.86-0.95), but that is dominated by pairs moving as one unit.
- Ablation k = 0 (`packs/ecology_abl_k0`, t=800): predators -95% (they die without prey), prey +1%, against prey -24% at t=800
  with predation. **Predators depend on eating prey, and predation lowers prey abundance.**
- The tracker merges a pursuing predator and its prey into one component (matter = both channels), so labkit tracks are short
  and the lineage panel is not meaningful for this world.
- Invalid control: qfrac = 0 does not remove predators (initial noise seeds predator mass, which grew 7.8x).

## kstrail long run (seed 0, 192², t=1800) — `packs/kstrail_long`
- **Swimmers are transient in the mass-conserving world.** Body count 14 → 9 (t=600) → 5 (t=1200) → 2 (t=1800). Collisions build
  saturated triangular aggregates that never move again and absorb swimmers. Final state: 2 immotile blobs.
- Compare `packs/toxforage_long_128` (r 0.06, t=1500): stationary 6-7 swimmers. Self-toxicity is the size control that keeps the
  swimmer phase alive (clumps poison themselves and re-shed swimmers).

## Fission screens (end of sprint, 128², t=1050, /tmp only)
- toxforage g 0.2 / kd 0.01 and g 0.3 / kd 0.015 / r 0.1: faster turnover but no fission. Persistent splits 2 and 0, max generation ≤ 1;
  splits are collision debris re-separating, not a grown swimmer dividing. Stronger kinetics alone do not give L6, so the
  next sprint needs an explicit size-selection operator.

Sprint 1 ended ~16:05 UTC.

# Sprint 2 (started 16:37 UTC)
Committee digest: division needs core starvation + slow interior transport (active-droplets, autopoiesis); L7 bar = variation
during the run + neutral control + 3 seeds. Challenge: fork a mechanism from another thread.

## fission.py: dense tracker for clean fission
labkit samples every 6 t and cannot separate division from collision debris. `fission.py` samples every 2 t, links by overlap
of 2-px-dilated masks, and calls a split CLEAN when the parent's lineage had no merge for >= 40 t and >= 2 children
survive >= 40 t. Generation = number of clean fissions in the ancestry. Writes a crop strip of the first 4 clean fissions.
(Fixed a bug where generations were assigned before propagation.)

- toxforage (Da 4), 128², t=1200: 58 splits, **3 clean fissions** (strip: an elongated hook swimmer pinches into two). Max gen 1.
  So the sprint-1 world already reproduces, rarely.
- Screens (128², t=1200, seed 0): g 0.15 / kd 0.0075 → 2 clean fissions; ka 0.2 / chi_a 48 → 8; **Da 2 → 11 (gen 5)**; Da 1 → 0
  (bodies too small to grow); r 0.1 / g 0.15 → 707 splits, 0 clean (fragmenting mess).

## swimfission = toxforage with Da 2 (attractant range 6.3 → 4.5 px) — `worlds/swimfission`, `packs/swimfission`
- `packs/fission_swimfission_s{0,1,2}.json/_strip.png` (160², t=1200): **10 / 10 / 15 clean fissions, max generation 4 / 3 / 5**,
  ~11 bodies late. Strips show binary fission: a swimmer elongates along its heading, pinches at the waist into two equal
  daughters, and they swim apart.
- labkit pack: 43-45 moving tracks per seed (up to 27 body lengths), persistent splits 3-8, labkit max generation 2-3.
- Mechanism: growth at the front lengthens the body along its axis. Once the length exceeds ~2x the attractant range, the
  cohesion cannot hold the two ends and the waist thins (the active-droplets rule "body > internal transport length").
