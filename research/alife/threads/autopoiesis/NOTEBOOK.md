# Autopoiesis notebook

Sprint 1 start: 2026-10-24 14:28 UTC. Tools: `screen.py` (quick strips with dimmed substrate, per-frame
stats), `sweep.py` (lattice SCL membrane-closure screen: fraction of samples where the planted ring
still encloses >= half its area; 2 seeds x 3000 sweeps).

## 1. Lattice SCL reference (`worlds/scl_lattice`)
Numba random-sequential SCL on 64x64: hole/S/K/L, link bonds as 8-bit masks, McMullin-style
rules (bond angle >= 90 deg, no diagonal crossing, bonded links immobile, S permeates bonded L
by jumping over it, K + 2S -> K + L, L -> 2S). Planted 9-px ring around one catalyst.
- v0 (p_ext=0.9: any link adjacent to a chain end bonds): the ring persists 1000 sweeps but
  internal links bond onto gap ends and grow inward spurs; the interior fills with debris
  chains and K eventually escapes (`screens/scl_base.png`). Classic SCL failure mode.
- v1: added **splice** (a free link touching two chain ends bonds to both at once, p=1) and
  made end-to-end joins likely (p_join=0.9) but single-end extension rare (p_ext=0.05).
  Closure fraction 0.59/0.64 (2 seeds) at p_dis=5e-4; 0.00/0.03 at p_dis=2e-3.
- separate decay for free links (p_disf=5e-3, cleans leaked links): no robust gain (0.39-0.78).
- MIN_SEP=3 (bond angle >= 135 deg, stiffer membrane) + p_dis=2e-4: closure 0.67/0.76, the best
  lattice setting. Gaps open and are re-spliced continually; catalysts sometimes escape through
  a gap (`screens/scl_k3.png`, 3 catalysts). Lattice SCL membranes are maintained but leaky:
  consistent with the historical record.

## 2. Gated protocell, continuum SCL on a Gray-Scott replicator (`worlds/gated_protocell`)
Fields S, K, L, M. K + S -> K + L; L polymerizes into M where |grad L| is large (edge of the
link cloud); M gates the diffusion of L (and optionally K) through div(D g(M) grad u) with face
mobility min(g_i, g_j); K autocatalysis S K^2 needs h(L) (Hill), so the catalyst only grows where
the membrane holds links in.
- numerics: explicit Euler blew up (K^2 S consuming more S than present once K was trapped);
  fixed by capping consumption at 0.5 S per step, and clipping. Central-difference |grad L|
  gave dotted (checkerboard) membranes; smoothing L before the gradient fixed it.
- b=0.2, gated K: 4 small cells (ring of M, K inside) form from the 4 GS seeds and then freeze
  in a steady state: no growth, no division (`screens/gp_L0-0.1_b-0.2.png`). L3 morphology but static.
- membrane ablation (cM=0, no polymerization): L diffuses away, h(L) falls, K dies everywhere
  within ~1500 steps (`screens/gp5_*cM-0.0*`). The membrane is necessary for the catalyst.
- K autocatalysis gated off outside the wall: membrane-trapped GS cells freeze (no growth); with
  K ungated or weakly gated, the GS spots die before a wall forms (8 configs, `screens/gp6_*`,
  `screens/gp4_*`). Gray-Scott kinetics are too fragile to share a cell with a barrier. Parked.

## 3. scl_divide: flexible lattice membranes (`worlds/scl_divide`)
Added to the lattice SCL: K pore block (K cannot step onto a site touching >= 2 chain ends),
bond-fluctuation moves of bonded links (hop to a neighbouring hole/S if all bonds stay valid),
link insertion into an existing bond (A-B -> A-L-B), and segment reconnection (A-A', B-B' touching
-> A-B, A'-B': fission of one loop / fusion of two), K replication from free links.
- moves into holes only: production creates holes inside, so the membrane drifts INWARD and the
  cell shrinks (225 -> 161 px, `screens/sd1.png`). Osmotic intuition reversed.
- moves into holes or S: membrane random-walks, gaps' ends drift apart and never re-splice;
  reconnection at p=0.5 shatters the cell into many tiny loops (`screens/sd2.png`).
- chain ends immobile + reconnection forbidden for loops < 16 links: closure fraction 0.01-0.93,
  no setting robust across 2 seeds (16 configs). **Negative:** in the lattice, membrane
  flexibility and gap repair pull against each other; I did not find a regime with both.

## 4. Phase protocell (`worlds/phase_protocell`): membrane = Allen-Cahn domain wall
Idea: make closure topological. phi is an inside-phase order parameter with Allen-Cahn dynamics;
its double well is tilted by links L (a (L - th)), so the inside phase only spreads where the
cell's own links are; K and L mobility ~ phi^2 (held in); K autocatalysis (logistic) ~ phi;
links made by K from substrate S; S fed from a bath (F (1-S)). Initial condition: 4 planted
blobs (phi profile radius 6, K and L in radius 4); everything else self-organizes.
- GS kinetics inside the phase: dies in all 6 tried settings, even with K ungated (spot rims
  need growth outside the phase). Switched to logistic K.
- logistic K: F >= 0.01 -> one sea; F = 0.002-0.005 -> extinction; **F = 0.006-0.008 -> bounded
  cells that grow and divide**, 5 -> 47 cells by t=8000 (`packs/phase_protocell`). Lineage to
  generation 5, 22-33 persistent splits per seed, 3 seeds.
- structure (`screens/pp6_chan.png`): S depleted inside, K fills the interior, L is highest just
  inside the wall (a link-rich shell), wall = 2 px ring of 4 phi(1-phi).
- division mechanism: big cells starve at the centre (S dips), L drops below th in the middle,
  the phase there loses its tilt and the wall pinches through. Prediction: more feed -> bigger
  cells before division. Cell area at t=8000: F=0.0054: 71 px/cell, 0.006: 66, 0.0066: 88,
  0.008: 405 (with occasional large compound cells). Roughly holds; not monotone at the low end.
- ablations (all from the same 4 blobs): no mobility gating (gate=0) -> all dies by t~400;
  gating L but not K (gateK=0) -> dies; no link tilt (a=0) -> domains shrink by curvature and
  die; no phase (phi = 1) -> uniform K sea, no individuals. Packs `phase_protocell_nogate`,
  `phase_protocell_notilt`. Every link of the loop is necessary.
- jitter: F +-10% and th +-10% keep the same behaviour (24-45 cells at t=8000).
- dt halving (dt=0.5, 16000 steps): cell counts 10/24/36/47 at t=2000/4000/6000/8000,
  identical to dt=1 to 3 digits.
- damage (`packs/phase_protocell_damage`, `screens/damage_strip.png`): at t=1500 the largest cell
  (a horseshoe about to divide) loses a disk cutting its wall and 36% of its area. Both pieces
  re-close their walls within ~100-250 time units, regrow and keep dividing; by t~2800 the crop
  looks like the undamaged control.
- noise initial conditions (smoothed random phi, random K and L everywhere; 6 tries): always one
  sea first, then a synchronous starvation crash to extinction. Not spontaneous yet.
- the labkit damage disk sits at the centroid of the largest component: for a walled cell it
  only hits the interior, and for a cell wrapped over the periodic edge the mask is misplaced.
  My worlds' damage() hooks re-find the cell and cut its wall (documented in the hook).
- 2x resolution (256^2, D x4, dt 0.25, same layout): cells 8/10/16/22/31/35/38/49 at
  t=1k..8k vs 8/10/-/24/-/36/-/47 at base. Qualitatively and quantitatively the same.
- **from noise** (`worlds/phase_protocell_noise`, φ = smoothed Gaussian noise with mean 0 and sd
  0.15-0.25, K ~ U[0,0.6], L ~ U[0,0.1]): 6/6 tries reach 44-51 cells at t=8000, even from a
  3-8 px initial nucleus. Pack: 22-24 blobs at t=350, 11-19 survivors at t=650, 42-43 cells and
  gen 3-4 at t=8000.
- after LITERATURE.md arrived: closest prior art is the chemoton/vesicle line (Macia & Sole:
  Turing instability inside a vesicle drives division; Ono & Ikegami lattice cells divide).
  The specific construction (Allen-Cahn wall tilted by an internal product + phi^2 mobility
  gating) is not in the file.

## 5. Heredity: phase_kinds (two catalyst kinds, stochastic point mutation K1 -> K2)
- K2 faster (c2=0.3 vs 0.2), same link output: K2 lineage sweeps in 3/3 seeds
  (`packs/phase_kinds/seed*/kinds.png`): K1 cells peak ~49 at t~11k, then fall to 0 by t~25k,
  while K2 cells rise to 28-33. Mixed cells are rare and transient (within-cell takeover is fast).
- parasite K2 (c2=0.3, b2=0, no links): infected cells turn pale and die before becoming pure
  K2; the population declines to extinction by t~25k in 3/3 seeds (`packs/phase_kinds_parasite`).
- parasite threshold (screens, 32k steps): c2=0.24 -> purged in 3/3 seeds (45-51 cells); c2=0.27
  -> seed 0 extinct at 32k, seed 1 down to 3 cells; c2=0.30 -> extinct ~25k.
- controls: no mutation (c2 irrelevant): 52 cells, stable to t=32k. Neutral mutant (c2=c1=0.2):
  K2 never forms a cell; 52, 51 and 52 K1 cells at 32k (seeds 0, 1, 2). So the sweep needs the advantage and the
  collapse needs the parasite.
- open question: why do K1 cells die faster than mutation events hit them in the parasite runs?
  Hypothesis: infected cells grow fast, hog substrate and starve neighbours before dying.

## 6. Phase membrane (`worlds/phase_membrane`): links adsorb to the wall
Links drift up grad w, w = 4 phi(1-phi) (upwind flux, chi). Since only L at the wall tilts the
front, adsorbed links ARE the wall's support: a molecular membrane layer.
- chi=2: links form a 2-3 px ring at the wall, 3-4x interior (`screens/pm2_chan.png`); cells
  larger and irregular, with deaths, fusions (merges 7-12) and divisions; 15-17 cells at t=8000
  (3 seeds); persistent splits 9-12, gen 2-3 (`packs/phase_membrane`).
- chi=3: 14 bigger cells. chi=5 or 10 at th=0.15 -> one sea; chi=5 with th 0.2-0.45, or chi=10
  with th 0.5 -> extinction. A narrow window: adsorbed links make walls pushy and decouple them
  from central starvation.
- damage at t=2000 (35% of a 597 px cell incl. wall arc): crescent re-walled with a full link ring
  within ~100 time units, regrown by ~350 (`screens/pm_damage_strip.png`).

## 7. Phase swim (`worlds/phase_swim`): rigid-droplet phoresis
Each cell (component of phi > 0.05, labels merged across periodic edges) is advected (upwind)
with v = mu <grad S>_cell. No external gradient.
- slow S diffusion alone (DS 0.03-0.1) gives no motion: cells swell and invaginate (`screens/mot_*`).
- first version with non-periodic labels tore cells at the domain edge (artifact). Fixed.
- 2 seeds at mu=1: speed ~0 until t~2500, then 0.09 (neighbour halos break symmetry). mu=8-400
  saturates the velocity clip, giving diagonal worm-like streaks (artifact; `screens/swim_mu-400*`).
- single cell: mu=1 never moves (to t=3000); mu=3 breaks symmetry at t~1200 and swims a crescent
  with a depletion wake at 0.094-0.11 px per time unit, 17.7-18.5 body lengths over 6000 (3 seeds,
  `packs/phase_swim`). Headings: diagonal, -y, +x: locked to lattice directions. The swimmer grows
  into an arc and never divides (it never starves).
- jitter (seed 1, 4000 steps): mu 2.7 / 3.3 / F 0.0054 / F 0.0066 all swim at 0.085-0.10 px/time;
  mu=2.0 swims after t~2000. Area keeps growing (109 -> 1400-1900 px by t=4000) in every case.
- swim + divide attempts: lower feed (F 0.005-0.0055) -> swimmers become long bands wrapping the
  domain, no division. Adding wall adsorption (chi=2) -> big grid-aligned square cells that later
  collapse (`screens/swimchi_*`). Negative for now; swimmers need a size limit.

## 8. Robustness of phase_membrane (seed 0, t=8000)
chi 1.8/2.2: 22/16 cells; F 0.0054/0.0066: 11/28; th 0.135/0.165: 8 (large) / 6 (small) cells.
Bounded walled cells survive every +-10% jitter; th is the most sensitive knob.

Sprint 1 wall-clock: 14:28 -> ~15:50 UTC of simulation work, then report.

## 9. Late checks
- Lattice SCL, chain-based bond inhibition (my reading: a free link touching a doubly bonded link
  may only splice): closure 0.15/0.60 (p_ext 0.05) and 0.15/0.89 (p_ext 0.5) vs 0.67/0.76
  without. No robust gain. Also found that p_ext has **no effect** in the MIN_SEP=3 regime: the
  single-end extension branch is never reached in 3000 sweeps (identical runs for p_ext
  0.05/0.5/1.0); splice does all repair. McMullin's exact inhibition rule is still to check.
- `worlds/phase_trait` (prototype for next sprint): catalyst carries a continuous trait c
  (growth rate, Q = cK), link output b0 max(0, 1 - 3 (c - 0.2)), +-delta point mutations in a disk.
  delta=0.03, r=2: the trait is blended away inside cells (cell traits 0.196-0.204 after 16k).
  delta=0.1, r=5: spread grows (10-90%: 0.147-0.223 at 32k), mean drifts 0.200 -> 0.188.
  c0=0.4 is not viable (dies by 4k). Blending inheritance in a well-mixed cell interior is the
  obstacle: variation between cells needs discrete, cell-wide mutations.
- phase_trait convergence test (delta=0.1, r=5, 32k steps): start c0=0.15 -> mean 0.166 (seed 0) /
  0.164 (seed 1); start c0=0.20 -> 0.188 / 0.191. The two start points approach each other (gap
  0.05 -> 0.025 in both seeds): preliminary sign of stabilizing selection toward c ~ 0.17-0.18,
  between within-cell (faster) and between-cell (more links) selection. c0=0.25 is not viable.
  Not promoted to a pack; first thing to firm up next sprint (longer runs, 3 seeds, trait
  histograms over time).
