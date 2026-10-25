# ringswim-dl2: ringed Allen-Cahn cells from noise that swim and divide, with the ring held through both (C:swim-divide)

`world.py` is c07's ringswim-waste-256 (`20261025T0922-c07-ringswim-256`, SIMD and SIBM established
separately) with one change: the link mobility DL is 0.2 instead of 0.1. Links are made inside the cell
(b K S, K held in by phi^2 mobility), drift up the wall indicator (chi = 2) and decay at dL = 0.02. At
DL = 0.1 a link made in the core decays before it reaches the wall, so labkit's aggregate ring sat at
1.45-1.47; at DL = 0.2 (the explicit-scheme limit is 0.25) it is 1.60-1.62 on all three seeds.
Everything else (phase tilt, catalyst, waste, per-body phoretic drive mu = 1.5) is unchanged.

## Screen (128^2, seed 0, t = 12000, labkit aggregate L rim/core; screen/)

| variant | L rim/core | cells final | max BL (labkit) |
|---|---|---|---|
| c07 (DL 0.1, chi 2) | 1.47 | 12 | 3.3 |
| chi 4 / chi 6 | 1.23 / 1.50 | 3 / 3 (cells fuse) | 1.8 / 1.9 |
| dL 0.01, b 0.025 | 1.25 | 3 | 2.2 |
| **DL 0.2** | **1.63** | 7 | 4.8 |
| DL >= 0.3 | numerically unstable (explicit Euler, D dt > 1/4) | | |

## Claim runs (256^2, seeds 0-2)

labkit packs (`pack/`, t = 10000): from smoothed noise everywhere (sheet t = 0) a bounded population
of 25-32 cells (occupancy 0.18-0.19); L membrane-like in aggregate, rim/core 1.60 / 1.60 / 1.62,
rim/outside 5.3-5.5, membrane-like individually in 166/220, 170/224, 147/191 cells.

`ringtrack.py` (c07's overlap tracker plus a per-cell ring score measured by distance to the cell's own
contour: mean L within 3 px inside the contour / mean L deeper than max(4 px, half the cell's depth);
labkit's centroid profile understates crescents), t = 20000, `data/`:

| run | cell-frames with ring >= 1.5 | persistent splits | max gen | splits / merges | tracks >= 3 BL (ring >= 1.5 in >= half their frames) | lineages: swim >= 3 BL + ring + persistent split |
|---|---|---|---|---|---|---|
| seed 0 | 99.9% (median 2.04) | 96 | 14 | 241 / 169 | 44 (44) | 1 (#570 -> 692, 693) |
| seed 1 | 99.9% (median 1.99) | 79 | 15 | 211 / 181 | 82 (82) | 3 (#563, #536, #426) |
| seed 2 | 99.9% (median 2.05) | 112 | 15 | 282 / 201 | 41 (41) | 2 (#123, #72) |
| chi = 0, seed 0 (B control) | **0%** (median 1.11) | 20 | 2 | 32 / 0 | 77 (0) | 0 |
| mu = 0, seed 1 (M control) | 100% | 80 | 5 | 266 / 0 | **0** | 0 |

The ring does work: without it (chi = 0) the cells swim further but divide 5x less (20 vs 96 persistent
splits, generation 2 vs 14). Without the drive (mu = 0) nothing swims 3 body lengths and the ring and
division stay.

## The track

Seed 1, ringtrack #563 (`img/strip_s1_563.png`, `img/div_s1_563.png`): a crescent with its link ring
(ring score 1.81-2.31 in every scored frame) swims 6.4 body lengths (122 px) from t = 14540 to 17900,
elongates and pinches at t ~ 17920 into #665 and #666; both keep the ring (median 1.90 and 1.82, 100% of
frames >= 1.5) and swim on, 4.9 and 3.6 body lengths. Seed 2 #123 (`img/strip_s2_123.png`) and seed 0 #570
(`img/strip_s0_570.png`) are further examples.

## Limits

- The drive is c07's per-body label average (nonlocal: each body moves rigidly with the mean substrate
  gradient over its pixels), as in the established SIMD claim.
- Genealogy is reticulate (merges 0.64-0.86 of splits); generation counts pass through merges. Tracks
  break at collisions, so only 1-3 track segments per seed show swimming >= 3 BL and a persistent
  split in one segment; most swimmers end in a merge. #563 itself starts at a tracker identity break
  (no parent recorded at t = 14540).
- The ring is chi-driven adsorption of the cell's own product (RUBRIC L3 quasi-equilibrium clause); the
  chi drift is written against grad 4phi(1-phi), but the cell makes all of L itself.
- The division at #563 is unequal (a small end piece and a long crescent). No dt or resolution test;
  controls on one seed each; no Laplacian-only twin.
