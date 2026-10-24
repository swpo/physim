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
