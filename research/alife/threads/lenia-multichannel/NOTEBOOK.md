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
