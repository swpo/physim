# NOTEBOOK: lenia-multichannel

Sprint 1 started 2026-10-24 14:28 UTC.

## Engine and positive controls

**E1. Multi-channel engine (tools/engine_src.py, copied into every world).** Chan 2020 update
`A_c <- clip(A_c + dt * sum_{k->c} h_k G(K_k * A_src(k)) / sum_{k->c} h_k)`, kernels with B rings
(peaks b in twelfths) inside radius r*R, quad4 kernel core and quad4 growth, exactly as in
`LeniaNDKC.calc_once`. Creature data: cloned github.com/Chakazul/Lenia, parsed all 4047 creature
records in `Python/found/*.json` (1856 are 3-channel/15-kernel). Decoder for Chan's RLE written.

**E2. Catalogue screen (screens/chan_catalogue_controls.png, 128², 400 steps).** Rows:
`*OmIrd`, `MIRd+`, `*mIRde`, `*mIpRDe`, `*fast cell`, `*nexus cell`, `* rectus`, `*** rectus`.
All 13 tried survive; `*fast cell` = cyan shell around orange/magenta core, glides;
`*mIRde`/`*mIpRDe` divide into two; rectus = fast gliders with magenta wings. Engine reproduces
Chan's creatures, so the "known multi-channel creature class" goal is met.
Worlds: `worlds/mc-fastcell`, `worlds/mc-mIRde` (planted copies).

**E3. mc-mIRde long run (192², t=100).** Divides into two daughters repeatedly but daughters
re-merge or one dissolves; at 128² with 2 copies and 1500 steps the mass grows 944 -> 4500
and component count 3 -> 11 (net growth of a population of blobs that collide and merge).

## Random graph screens from noise (tools/screen_random.py)

**S1. 5 graph families x 60 random rules, 96², R=10, 400 steps (t=40), noise patch 60% of side.**
Data: `screen_data/*.json`; galleries `screens/rnd_<family>_individuals.png`.

| family | dead | sea | blob/pattern | transient | "individuals" (classifier) |
|---|---|---|---|---|---|
| full (Chan 233 template, 15 kernels) | 43 | 6 | 7 | 1 | 3 |
| cycle (0->1->2->0) | 28 | 11 | 10 | 4 | 7 |
| star (channel 0 hub) | 27 | 10 | 10 | 4 | 9 |
| two (2 channels, all edges) | 22 | 19 | 3 | 0 | 16 |
| shell (designed core + outer-ring shell + shell inhibits core) | 20 | 14 | 7 | 4 | 15 |

Looking at the galleries, most "individuals" are frozen dot lattices filling the seeded square
(L1/L2 tissue). By eye, rules that give **discrete, separated individuals**: two#56, two#13(lattice,
no), star#7, cycle#37, shell#17, shell#5: ~6/300 = 2%. Fewer kernels/channels = more viable rules;
the full 15-kernel graph is mostly dead under uniform random sampling.

**S2. Re-run of candidates with a different noise seed (screens/promote_candidates_r1.png).**
- two#56: noise -> 4-5 cyan-core / orange-spiky-shell individuals, which then **bind into a chain**
  linked by orange bridges, and the chain is stable. Promising (L3 + binding).
- shell#17: cyan rings (hollow) + one writhing orange/cyan thing; rings stationary.
- cycle#37: one or two tiny dots. star#7: dies with this seed. two#13: dot lattice.

## Metabolism (food field)

**M1. Gated growth (positive growth x F, eating, starvation).** Kills `*mIRde` for every setting
tried (eat 0.02-0.3, starve 0.1-0.3), even with mean F ~0.93: Chan creatures are finely balanced
and any multiplicative change of the growth term destroys them. Negative.

**M2. Material metabolism ("conserve"): matter can only be built from local food, yield Y; decay
dissipates; food regrows (rho) and diffuses (D).** Where food is plentiful the dynamics are
unchanged. With rho=0.005 the replicators dig food wells and starve (screens/food_mirde_starve.png).
rho=0.02 D=2: population ~2-8 blobs, food mean 0.65-0.75; rho=0.05 D=2: 20-30 blobs, food ~0.75.
Population size follows the food supply. Needs a no-food ablation and longer runs.

## r-two56: spontaneous shelled cells (promoted)

**P1. Pack `packs/r-two56` (192², 3 seeds, t=100).** All seeds: the noise square first grows a
two-layer rim (cyan inside, orange outside) around the whole tissue (t=4-9), then the tissue
breaks up and **cells pinch off the rim**: white centre, cyan ring, orange spiky shell, diameter
~20 px (2R). 4-8 cells per seed survive to the end, stationary; some cells stay bound in pairs via
orange bridges (seed 0). Seed 1 makes a large hollow vesicle (cyan ring, orange coat, empty
interior) that lives t=40-65 then tears into a crescent. FACTS rim-vs-core 0.5-0.75,
rim-vs-outside 0.46-0.53: shell = channel 1 high, core = channel 0 high.

**P2. Ablations (screens/r-two56_ablations.png, rows: none, -k0..-k5, -k4&k5).**
- k0 (0->0, single ring r=0.59R, m=0.15, narrow): **size limiter**. Without it the cells never stop
  growing: bilayer worms (cyan core, orange coat) that invade everything.
- k1 (0->0, 3 rings, m=0.47): without it, sea.
- k2, k3 (1->1): without either, everything dies.
- k4 (0->1, shell grows where ring-sensed core density ~0.23): without it, orange labyrinth sea.
  This is the **membrane mechanism**: the shell can only exist at the distance from the core where
  the nonlocally sensed core density hits k4's set point.
- k5 (1->0, broad, m=0.5): without it, the core dies: **the core needs its shell**.
- both cross edges: orange labyrinth only.
So the cell is a mutual dependence: core makes shell at a set distance, shell feeds core.

**P3. Damage (screens/r-two56_damage_side_vs_core.png; dmg script in scratch).** Single isolated
cell at t=100. Side cut 10% and 20% of the cell area: full regrowth within ~t=10. Side cut 30%
or 50%: cell dies. Any core disk, even 10%: the cyan core collapses to a ring and the whole cell
dies. labkit `--damage 120:0.5` packs (`packs/r-two56_damage`): damaged cells die. **L4a not met**
(threshold < 30%). Interesting asymmetry: the shell is repairable, the core is not.

**P4. Mutating the size limiter (k0 weight h0 0.413 -> 0.05-0.33, from noise).** h0 <= 0.33 gives
**expanding hollow vesicles** (cyan ring coated with orange on both sides) that grow, buckle and
shed small cells from their surface; h0=0.05 gives worms. A single planted cell
(`worlds/r-two56-cell`) is unchanged for h0 in [0.1, 0.413] and m0 in [0.13, 0.19]: the cell is
a very robust attractor (k0 is inactive inside a formed cell). No binary fission found.

## Metabolism, continued

**M3. Static cells don't eat.** r-two56 + conserve food: food dips while cells form, then returns
to 1.0: a formed static Lenia cell has zero matter turnover, so a "build from food" metabolism
never charges it. Only things that move or grow pay.

**M4. Motile shelled glider + food (mcf-fastcell, Y=2).** Starves in ~500 steps (turnover at the
moving front is large). **Y=5, rho=0.01, D=1: two gliders persist for 6000 steps with mean food
0.65, leaving dark depletion trails** (foraging). Ablations: rho=0 -> both die at step ~2000 when
mean food reaches 0.3-0.35; Fmax=F0=0.5 -> die by 1300; 0.25 -> die by 430; 0.1 -> die by 210.
The glider depends on the food it consumes: L4c candidate on an L3 (shell + core) creature.

**M5. Replicator + food, 128², 4000 steps.** no food coupling: 3 -> 19-26 blobs; rho=0.02 D=2:
bounded at 1-4 blobs (food 0.65-0.85); rho=0.01 D=4: extinct at ~1450; rho=0: extinct by 726
while mean food is still 0.75 (local wells). Population size is set by food supply.

## More random rules (screen 2) and two new spontaneous worlds

**S3. 'two' family, 120 more rules (screen_data/two_s1.json, screens/rnd_two_individuals.png
is screen 1; screen 2 gallery in screens/ as rnd_two_s1).** dead 47, sea 25, blob/pattern 17,
transient 6, classifier-"individuals" 25. By eye: discrete individuals in 4 (#11, #60, #66, #85);
#66 is a sea with another noise seed (spontaneity is IC-sensitive for some rules).
Over both screens: **discrete individuals in ~10/420 random graphs (2.4%); shelled
(core + shell) cells in 2/420 (two#56, two-s1#85), all in the 2-channel family.**

**P5. r-two-s1-85 pack (192², 3 seeds, t=150).** Noise -> a packed, frozen "tissue" of ~30 shelled
cells (cyan core + white centre + orange shell, same morphology as r-two56) that stays inside the
seeded square. Lineage "splits" (up to generation 2) are flickering bridges between touching
cells, not division: count is flat. L3 cells, no motion, no reproduction.

**P6. r-two-s1-60 pack (192², 3 seeds, t=150).** Noise -> ~45 cyan individuals. Inside the crowd
they are static "bricks"/hourglasses; at the crowd edge round C-shaped gliders peel off and
wander (15-26 moving tracks per seed, more gliders over time). Planting either a brick or a glider
alone (screens/r-two-s1-60_planted_brick_and_glider.png): **both become the same glider**, so the
bricks are gliders arrested by crowding (jamming). Ablations (screens/r-two-s1-60_ablations.png):
k1 (0->0 ring) essential; k0 removal -> sea; k5 removal -> dense dot lattice, but replacing k5 by a
constant (m=5, screens/r-two-s1-60_k5_constant.png) keeps the gliders: **the orange channel only
supplies a constant decay bias; the glider is effectively single-channel Lenia.** The same
k5->constant test kills r-two56 (its shell really feeds its core).

## Robustness / numerics of r-two56

**N1. +-10% random jitter of every m, s, h (5 draws, 128², t=100):** 1/5 same behaviour,
1/5 a growing blob/worm, 3/5 die. Not robust in the full 18-parameter space.
**N2. dt/2 (T=20):** same formation (rim, budding cells) but cells die off slowly (6 -> 1 by
t=100). **R = 11, 12, 13 (grid scaled):** same cells, 2-3 survive. **R = 15:** everything dies by
t=67. (screens/r-two56_numerics_dthalf_R11_R13.png). Formation is qualitatively resolution- and
dt-robust over a small range; long-term cell survival is marginal and partly a discretization
effect. Numerical validity: weak.

## Replicators x food (the main line by the end of the sprint)

**R1. Screen of 47 catalogue creatures with R/r in their name (128², 1500 steps;
screens/chan_replicators_screen.png rows: #224, #331 *mR, #1121 Mird+, #1129 *mIRde,
#1130 MIRd+, #1187 *MIrd, #1195 R+).** Strong exponential replicators: #1130 `MIRd+` (1 -> 33
cells), #1195 `R+` (-> 29), #224 (fills grid as a dotted tissue). #1130 is a structured cell: white
core, orange cap on one side, dotted magenta halo; it elongates and splits (planted, from Chan).

**R2. mc-MIRd (#1130, no food, 192²).** 1 -> 65 cells by step 2000. With seed jitter 0.05 and
tracking on channel 0 only, labkit sees 11 persistent splits and generation 4 by t=150.
(Without jitter the 3 seeds are identical: one planted creature on a torus, rotations by 90
degrees are exact symmetries. Without core-only tracking the dotted halos fuse all cells into
one component and lineage reads generation 0.)

**R3. mcf-MIRd: MIRd+ + build-from-food metabolism (Y=2, D=2).** The colony becomes a
**front of dividing cells advancing into fresh food with a depleted interior behind it**
(screens/mcf-MIRd_rho0.01_160.png). Supply sets the regime:
- rho=0 (no regrowth): grows, eats the food, extinct by step ~2660 (screens/mcf-MIRd_rho0_160.png).
- rho=0.005: boom, overshoot to 19 cells, bust, extinct by step 5000 (128²).
- rho=0.01: persistent colony, ~20-26 cells at 160², food mean ~0.2.
- rho=0.02: space-limited; at confluence the cells turn into a **static white lattice that stops
  eating** (food recovers to 0.87; screens/mcf-MIRd_rho0.02_128.png). Same "jammed cells are
  metabolically inert" effect as M3.

**R4. mcf-mIRde at 192² (rho .02, D 2, 3 copies):** extinct in 2/3 seeds by t=300. The 128²
result (M5) was marginal. Negative/fragile.

**R5. Packs.** `packs/mc-MIRd` (no food, jitter 0.05, core-channel tracking): 16-17 persistent
splits, generation 4, ~40 cells by t=200 in all 3 seeds. `packs/mcf-MIRd` (rho=0.01, t=400):
boom to ~40 cells at t≈200 with food at ~0.2, then decline to 11-16 cells by t=400, which gather
into one compact colony; starving cells grow orange rings. `packs/mcf-MIRd-norefill` (rho=0):
extinct in 3/3 seeds (seed0 at t≈230), mean food still ~0.4 (local depletion).
`packs/mcf-fastcell-norefill`: gliders die one by one; 0, 0, 1 left at t=300.
mc-MIRd at dt/2 (T=20) still replicates: 2 -> 32 cells over the same simulated time.

## Two-species ecology (new mutation, end of sprint)

**E1. eco-MIRd-Rplus (tools/make_eco_world.py).** Two catalogue replicators, MIRd+ (#1130) and R+
(#1195), each with its own 3 channels and 15-kernel rule, coupled only through one shared food
field (build-from-food) and space exclusion (positive growth x (1 - other's occupancy)).
128², 4000 steps, seed 1: A alone 1 -> 13 -> 6 cells (food 0.18-0.36); B alone ~36-52 cells
(food ~0.15); together: B ~35-50, A persists as a 3-6-cell enclave
(screens/eco-MIRd-Rplus_both_128.png). R+'s catalogue pattern is already a 4-cell cluster, so the
start is unequal. Coexistence under competition is a first L5 candidate and a stepping stone to
selection.

**R6. Long runs of mcf-MIRd (128², 8000-10000 steps, seed 1).**
- rho=0.01, D=2: boom to 15 cells (food 0.14), decline, **extinct by step ~4500**; food recovers to 1.
- rho=0.01, D=8: grows to confluence (~30 cells), then a static dormant lattice; food -> 0.90.
- rho=0.0125, D=4: same dormant lattice (~33 cells), food -> 0.96.
- rho=0.015, D=2: same dormant lattice (~27 cells), food -> 0.97.
The colony either crashes before it reaches confluence (extinction), or reaches confluence and goes
dormant (jammed cells stop turning over, so they stop eating). So far there is no dynamic
steady state in which cells keep dividing and dying. That steady state is the target for
sprint 2: add a maintenance cost or death rate for dormant cells, or a spatially patchy food
supply.

## Spontaneous replication screen (negative)

**S4. 150 random 'two' graphs from a small 24 px noise patch (128², 1500 steps;
tools/screen_replicators.py, screen_data/rep_two_s0.json, screens/rep_screen_two_hits.png).**
7 flagged (individual count rising). 6 of them are **expanding dot or ring lattices** that tile
space from a front (L1/L2 tissue growth, like Gray-Scott spot fronts), not division of individuals.
The 7th (#144, worlds/r-rep144) breaks the patch into 3-4 orange C-shaped gliders whose count stays
flat over 3000 steps: the same C-glider class as r-two-s1-60. **0/150 spontaneous cell
replicators.** The C-shaped glider is a recurring attractor of 2-channel random rules.

## Population cycles (end of sprint)

**C1. mcf-MIRd at 192² (rho=0.01, D=2, no decay), 20000 steps
(screens/mcf-MIRd_192_20000steps_cycles.png).** Cells: 3 -> 34 (step 2600, food 0.22) -> 3
(step 5200-6100, food 0.74) -> 32 (step 8700, food 0.26) -> 2 -> **extinct at ~11300**. Two
consumer-resource boom-bust cycles with growing amplitude, then extinction. At 128² the first
crash is already fatal: the larger grid holds enough survivors to recolonise once.

**C2. Maintenance cost (new mutation): all matter decays at rate `decay` and must be rebuilt from
food (worlds/mcfd-MIRd).**
- decay 0.01 (rho 0.02, 128²): the cells still form the white lattice, but now pay for it.
  Food stays at 0.79 instead of recovering to 0.97, and the count is steady at 30-35.
- **decay 0.03 (rho 0.02, 128², 14000 steps): no dormant lattice. The population oscillates
  with continual division and death**: cells 19 (step 2000), 7 (4000-5000), 15 (6000), 12 (8000),
  7 (9000), 18 (10000), 2 (12000), 12 (14000). Food oscillates in antiphase between 0.23 and 0.73.
  3+ cycles without extinction (screens/mcfd-MIRd_decay0.03_14000steps.png).

  So a maintenance cost removes free dormancy and turns the boom-to-dormancy or boom-to-extinction
  outcomes into a sustained consumer-resource cycle. Pack: `packs/mcfd-MIRd`.

**C3. Packs and robustness of the cycle.** `packs/mcfd-MIRd` (128², 3 seeds, 14000 steps): all
seeds persist (3, 6 and 10 cells at the end; peaks of 25-28). Seed 2 shows 4 clean cycles with
period ≈380 time units, with matter and food in antiphase.
- **decay 0.025:** static fed lattice (~32 cells, food 0.6).
- **decay 0.035:** oscillating, 4-13 cells, alive at step 10000.
- **dt/2 (T=20, seed 2, 28000 steps = same 1400 time units):** about 2.5 cycles (troughs of 5-6
  cells), then **extinct at t≈1000** at a trough.

The cycle needs decay of about 0.03 or more, and survival through troughs is fragile: a small
population at the trough can be lost. A bigger grid or a spatially patchy food supply should help
(next sprint).

**C4. Two more checks.**
- mcfd-MIRd at **192²** (seed 0, 14000 steps): boom to 32, bust to 13, then a **noisy steady
  population of 20-28 cells with food ~0.4** through the end. On the larger grid the cycle is
  damped, presumably because local cycles fall out of phase and average out.
- **dt/2, seed 0** (28000 steps = t 1400): persists the whole run, 5-28 cells, food 0.24-0.59.
  The dt/2 extinction in C3 is seed-specific: dt/2 survives in 1/2 seeds.

---

# Sprint 2 (started 2026-10-24 16:37 UTC)

Committee digest: the L7 bar is variation arising during the run + a neutral control with the same
mutation rate + >=3 seeds. Challenge: fork a mechanism from another thread. I have reproduction and
metabolism, so I add heredity, forking the active-droplets idea (ad5-evolve: body-confined alleles,
mutation as droplet-scale events, because pixel-white noise averages out over a body).

**H1. mcg-MIRd (worlds/mcg-MIRd).** Base mcfd-MIRd (food + maintenance decay 0.03, cycling
population). New trait field g(x) carried by matter.
- Inheritance: matter built at x takes g_loc = blur(g*M)/blur(M) (Gaussian, 3 px), so new matter
  copies the trait of the cell it grows from; surviving matter keeps its g.
- Mutation: replication-error events at rate MU per step, adding N(0, DELTA) to g in a disk of radius
  MUT_R at a random matter pixel.
- Phenotype: yield Y*exp(SEL*g). SEL=0 is the neutral control with identical mutation.
First try (MU .002, DELTA .3, r 5, 128², 6000 steps): per-cell sd only 0.04, because the disk covers
a fraction of a cell and blur averages it away. With MU .004, DELTA .5, r 8 (8000 steps, seed 0):
- selection: mean g 0 -> +0.25, cell range [-0.14, +0.82]. High-g (orange) cells spread and take a
  region. By the end the efficient population is confluent and the dormant lattice is back
  (food 0.62): evolving efficiency pushes the ecology out of the cycling regime.
- neutral: mean drifts -0.11..+0.16, range [-0.5, +0.5].
Now running 3+3 seeds at 160², 12000 steps.

**H2. mcg-MIRd yield gene, 3 selection + 3 neutral seeds (160², 12000 steps; MU .004, DELTA .5,
MUT_R 8; screens/mcg_yield_selection_vs_neutral.png).**
- Ecology diverges cleanly. Selection runs reach 30-35 cells and a fed static lattice (food
  0.55-0.63) in 3/3; neutral runs keep cycling (5-22 cells, food 0.25-0.78) in 3/3.
- **The trait itself barely differs:** mean g over the second half is 0.22/0.11/0.08 (selection)
  vs 0.02/0.27/-0.01 (neutral), and the fraction of cells with g>0.2 is about 1/3 in both.
- The divergence appears by step 2000-3000, when mean g is still ~0.05. The base point (decay 0.03)
  sits at the cycle/lattice boundary (0.025 gives a lattice), so a small yield gain in a few cells
  tips the whole ecology into dormancy, which then stops turnover and selection.
- No cell-level selection demonstrated. Next: stronger selection, higher base decay to keep
  turnover, and a two-kind competition assay.

**H3. Competition assay, decay 0.04 (two planted kinds g=0 and g=0.5, MU=0, SEL=3 vs 0, 128²,
10000 steps, 3 seeds each).** Kinds breed true: traits stay exactly 0 and 0.5. Neutral (yield
Y=2): extinct by step 3332 in 3/3 (decay 0.04 is too costly for the baseline). Selection:
both kinds form a mixed, static lattice by step ~1700, and the kind frequencies freeze at their
colonization values (B fraction 0.39/0.60/0.67). **Once confluent, Lenia cells stop turning
over, so selection stops.** Selection needs the cycling regime (ongoing death and recolonization).

**H4. Competition assay in the cycling regime (decay 0.03; kinds g=0 and g=-0.3, MU=0, 128², 12000
steps; screens/mcg_competition_cycling.png, mcg_competition_sel_seed0.png).**
- Selection (SEL=1, so kind A has e^-0.3 = 74% yield): A's mass fraction falls 0.50 -> 0.07-0.08
  by step 2000 and to 0.01-0.05 afterwards, in 3/3 seeds. The population keeps cycling (2-14 cells).
  The residual 0.01-0.05 is probably intermediate-g matter at cell contacts.
- Neutral (SEL=0): A's fraction drifts: 0.50 -> 0.04 (seed 0), -> 0.1-0.2 (seed 1), -> **0.92**
  (seed 2, A takes over by drift).
- Neutral seeds 1 and 2 go extinct at step ~12000 (whole population, the known 128² fragility).
**Kinds breed true through division, and differential persistence follows the yield difference only
when it matters (selection vs neutral, 3+3 seeds).** The variation here is planted, not arising.

**H5. Purifying selection with mutations arising (ONE_SIDED: yield = Y*exp(SEL*min(g,0)), so
positive mutations are neutral and negative ones harmful; MU .004, 160², 10000 steps, 3+3).**
Cells with g < -0.2 in the second half: selection 1/75, 1/74, 0/92 vs neutral 0/56, 1/86, 13/95.
Mean g is the same in both, as designed. The direction fits purging, but 13 of the 14 come from
one neutral seed, so this is inconclusive. Rerunning at MU 0.012.

**H6. Purifying selection at MU 0.012 (160², 10000 steps, 3+3; screens/mcg_purifying_mu012.png,
mcg_purifying_neutral_seed0.png, mcg_purifying_sel_seed0.png).**
- Cells with g < -0.2 in the second half: **selection 0/86, 1/73, 0/97 vs neutral 29/56, 0/86, 5/95.**
- Mean g in the second half: selection +0.46/+0.40/+0.51 vs neutral -0.33/+0.38/+0.31.
- Neutral seed 0: a blue low-g lineage takes over by drift (mean g reaches -0.9 at step 9000).
  Selection never allows this.
- Under selection the mean ratchets upward: harmful variants are purged, while positive ones are
  neutral and drift freely.
- Pooled with H5 (MU .004): harmful cells 3/497 (selection) vs 48/474 (neutral). Seeds with ≥5
  harmful cells: 0/6 vs 3/6. The ecology keeps cycling in all 12 runs (no dormant lattice, because
  positive g carries no benefit).

World defaults are now this setting (MU 0.012, ONE_SIDED). The neutral control is
worlds/mcg-MIRd-neutral (SEL=0).
Movie: movies/mcg_selection_vs_neutral_seed0.mp4 (same seed and mutation sequence, side by side).
