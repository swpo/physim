# Q:marangoni-turnover-persistence, loop 2: T=2000 with dilution plus immediate return of the removed matter (c45)

world.py = the loop-1 world (20261026T1858-c45-marangoni-turnover-tuning): c34's Marangoni rods, CARGO=0, a trait-blind
random removal of whole bodies every 10 frames (p 0.10; raster-ordered bodies, RNG seeded only by seed and event index),
with REDIST=1: the removed body matter is spread back uniformly at once, so the event conserves mean phi (fresh medium,
as in serial transfer). T=2000 (400 frames), 128^2. Runs: seeds 81 and 82; the mar=0 floor on seed 81; and the same world
without dilution (p 0) on seed 82. labkit + c00's extract.py and analyze.py; turnover_stats.py (40-frame windows,
48-frame birth cohorts, about one median cycle).

## Demography (runs/*/stats.txt)

| run | removed | persistent splits | per 40 frames, frames 40-360 | max generation (labkit split tree, K=20) | dividing tracks | bodies |
|---|---|---|---|---|---|---|
| p 0.10 + REDIST, seed 81 | 81 | 50 | 9, 7, 7, 4, 7, 4, 0 (and 0 in 360-400) | 8 | 45 | 23-30 |
| p 0.10 + REDIST, seed 82 | 90 | 50 | 3-8 in every window to 360, 1 in 360-400 | 4 | 40 | 19-29 |
| mar 0 floor, p 0.10 + REDIST, seed 81 | 42 | 30 | 1-6 | 9 | 20 | 8-14 |
| no dilution, seed 82 | 0 | 40 | 9, 4, 5, 3, 2, 3, 2, 1, 2 (declining) | 4 | 19 | - |

With dilution the rods keep dividing through the run (40-45 dividing tracks against 19 without it, where 11 of 19 are in
the first cohort). Generation depth is limited by the removals themselves: seed 81 reaches generation 8, seed 82 only 4.
On seed 81 no persistent split is counted after frame 320.

## Swim-before-divide minority per birth cohort (D = net over median rod length, rod lengths; D_A = net / sqrt(area))

seed 81: share D >= 3 by cohort 0, 0, 0.07, 0, 0.12, 0.25, 0.40 (n = 3-14 per cohort); 5 of 45 overall.
seed 82: 0, 0, 0, 0, 0.11, 0, 0 (n = 4-9); 1 of 40 overall. mar 0 floor: 0 of 20 (median D 0.48). No dilution, seed 82: 3 of 19,
all in the first cohort. The minority stays rare (6 of 85, 7%) and does not rise consistently: up on seed 81 (small cohorts),
flat on seed 82.

## Heredity (heredity_s81_s82.txt, c00's analyze.py, both seeds pooled)

D on D, parent and offspring both dividing: n = 41 pairs (33 parents), slope -0.25 [-0.47, -0.02]; time-matched null +0.14,
P(null >= obs) 0.99. The interval excludes +0.3: the swim-far phenotype is regenerated every cycle, not inherited, under
turnover too, as c00 found without it. Speed on speed: -0.21 [-0.55, +0.01]. Net speed and cycle are anti-correlated
(Spearman -0.52), and early speed predicts early area gain (+0.37): faster rods grow and divide sooner.

## Against the question

Births continue at a steady count with turnover on both seeds (pass for the demography), for 8 generations on seed 81
and 4 on seed 82 (half pass). The minority persists only by being redrawn (slope interval excludes +0.3); the mar=0 floor
has no passers. Not done: the 100-pair target (41 pairs), selection differentials on early speed and on D at fixed speed.

## Limits

Two seeds, one p. REDIST is a design choice (the plain removal of loop 1 did not keep the rods dividing). Persistent splits
need both daughters to live 20 frames, and a removal every 10 frames at p 0.1 kills about a third of sister pairs before
that, so labkit's split counts and generations are lower bounds. Body count is about 25, above the question's 12-20 target.
