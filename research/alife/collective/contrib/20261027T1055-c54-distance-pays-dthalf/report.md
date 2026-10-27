# dt/2 check of loop 3 (20261027T1005-c54-distance-pays-single-kind), seed 620: the result does not hold at half the time step

Same single-kind depletion arms as loop 3 (world 20261027T0830-c54-distance-pays-competition/world.py, DEP 1, dep_in -0.7, mu 0,
FOUNDER 1 or 2, seed 620, 128^2, T = 2000) with the world's own step halved: WORLD_P dt 0.025 and --spf 200, so frames are still 5 t
apart (labkit's FACTS.md and sheet labels read time x2 because META dt stays 0.05; extract.py and spread_stats.py use 5 t per
frame, which is correct). Mutation and split detection run every 200 steps (2.5 t) instead of every 100 steps (5 t).

| arm (seed 620) | dividing rods | M passers | median D (own rod lengths) | median cycle (t) | path speed |
|---|---|---|---|---|---|
| mar 40, dt 0.05 (loop 3) | 10 | 8/10 | 3.69 | 338 | 0.25 |
| mar 60, dt 0.05 (loop 3) | 15 | 9/15 | 3.17 | 305 | 0.39 |
| mar 40, dt 0.025 | 6 | 3/6 | **2.66** | 180 | 0.30 |
| mar 60, dt 0.025 | 9 | 6/9 | **4.36** | 215 | 0.36 |

At dt/2, mar 60 covers more distance per cycle than mar 40 (4.36 vs 2.66) and both kinds' cycles are about 40% shorter, so loop 3's
"same distance per cycle for both kinds under depletion" is **not robust to the time step** on this seed (6-15 dividing rods per run,
so the medians are noisy). Loop 3's conclusion should be read as untested until it is repeated at dt/2 on more seeds. The
grid-scale stripes around mar-60 bodies during nucleation are still there at dt/2 (runs/m60dt2_s620/sheet.jpg, labelled t = 340,
real t = 170), so they are not a time-step artefact; a finer grid or dealiasing check remains open.
