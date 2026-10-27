# Q:marangoni-swimmer-spread, loop 2 (c50): seed 501, and does faster disc growth make distance pay?

World: the loop-1 world (20261027T0000-c50-marangoni-spread-loop1/world.py, unchanged; c45's three-kind mar 20/40/60 ladder,
all founders mar 40, mutation 2.5e-3 per body per frame, growing sink discs one per 50 t, R 24). Seed 501 (fresh), 128^2,
T=2000. Arms: E and its identical-event twin (MARS 40/40/40) at the loop-1 disc speed 0.08 px/t (the paired replicate of
loop 1); and, to test whether faster discs reward distance, E, twin, no-escape C and drive-off (MARS 0) at 0.16 px/t.
(A disc_dt 100 variant was lost to a container restart and not re-run.) Readouts as loop 1 (spread_stats.py, fate_kind.py,
c00's extract.py; an.sh runs them); outputs in out/, figure trait_s501.png.

| arm (seed 501) | trait mean t 1000 / 1600 / 2000 | bodies at 2000 | M passers (rod lengths, rear tip) | sqrt-area passers | escape share (k0, k1, k2) | D gradient | persistent splits k0/k1/k2 |
|---|---|---|---|---|---|---|---|
| E slow | 45.5 / 47.3 / 47.5 | 8 | **5 of 9** | 7 of 9 | 0.69 (4/5, 27/42, 11/14) | +0.04 [-0.84, +3.0] | 1/12/6 |
| twin slow | 40.0 / 40.0 / 37.5 | 8 | 2 of 10 | 6 of 10 | 0.64 (labels 6/7, 21/35, 3/5) | -0.19 [-0.61, +0.44] | 2/16/2 |
| E fast | 47.1 / 47.1 / 47.7 | 13 | 7 of 13 | 11 of 13 | 0.51 (0/2, 26/46, 7/17) | +0.03 [-0.31, +0.48] | 0/20/9 |
| twin fast | 43.8 / 50.8 / 56.0 | 10 | 7 of 17 | 14 of 17 | 0.44 (labels 1/5, 14/45, 17/23) | -0.15 [-0.38, +0.09] | 0/20/8 |
| C fast | 40.0 / 40.0 / 40.0 | 4 | 3 of 14 | 11 of 14 | removed at opening | -0.22 [-1.07, +0.14] | 0/18/4 |
| drive-off fast | 40.0 / 46.7 / 45.0 | 4 | 0 of 9 | 0 of 9 | 0.21 | +0.27 [-0.20, +1.08] | 0/15/3 |

Seed 500 (loop 1, slow): E 45.7 at T=2000 and 1 of 17 passers; twin 36.7 and 2 of 17.

## What it shows

1. **Paired seeds, slow discs (the question's design)**: the trait mean rises more in E than in the twin on both seeds
   (500: +5.7 vs -3.3; 501: +7.5 vs -2.5). The passing share is higher in E on seed 501 (5 of 9 vs 2 of 10) but not on
   seed 500 (1 of 17 vs 2 of 17). Seed-to-seed variation in the passing share (1/17 to 5/9 in E) is larger than any arm
   effect.
2. **Faster discs do not reward distance**: on seed 501, fast discs give the same passing share as slow ones in E
   (7/13 vs 5/9) and a higher one in the twin (7/17 vs 2/10); the twin's k2 label rises to 56 (drift) while E's mar-60 kind
   stays at 47.7. The selection gradient on D stays near zero in E at both speeds (+0.03, +0.04) and slightly negative
   in the twins and C. Escape share falls with faster discs (0.69 -> 0.51 in E).
3. **Swimmers translate; the discs do not fake passers**: drive-off rods under fast discs make 0 of 9 passers and escape
   0.21 of the time; every passer in E grows during its cycle (area x1.7-2.9) with the rear tip advancing 0.83-1.01 of the
   net displacement, so the discs do not move rods by dissolving their back.
4. **Mutation streams bias the drift**: on seed 501 the shared mutation stream sends k1 bodies to k2 five times for once to
   k0 in every arm; the drive-off arm's trait mean rises to 45-48 with no Marangoni effect at all. The twin absorbs this only
   on average: with 4-20 bodies per run, single lineages decide each trait-mean curve.
5. **Heredity bookkeeping holds**: kind changes on living bodies happen at logged mutations (1 unexplained of 63 changes
   across the six runs), 0-4 off-kind daughters per 36-58 checked.

## Reading and next step

Neither disc speed rewards distance per cycle; escape rewards speed while caught, and the mar-60 kind rises in E on 2/2
slow-disc seeds through escape (k2 escapes 11/14 on seed 501), but the M-gate share follows the seed more than the arm.
With 4-20 bodies per 128^2 run, the trait mean is set by one or two lineages, so 6-8 paired seeds at this size can show a
consistent trait-mean shift but are unlikely to show a consistent passing-share shift. Loop 3 tries a supply only movers
reach: short-lived rich patches (food flashes) on top of the sink discs, so that swimming far within a cycle finds more food
and shortens the cycle instead of lengthening it.

## Limits

One seed in this loop; 9-17 dividing tracks per arm; the fast-disc arms have no seed-500 partner. The twin shares the random
streams but not the bodies after the first frames. A 256^2 run would take about 70 min per arm here (timed), beyond this
loop.
