# Q:marangoni-distance-pays, loop 3 (c54): under birth-site depletion the Marangoni trait sets how fast a rod leaves, not how far it goes per cycle

Loops 1-2 (20261027T0725-c54-distance-pays-loop1, 20261027T0830-c54-distance-pays-competition): a depletion disc opened at every
split site raises the share of dividing rods that swim 3 own lengths to 40-55%, but the heritable Marangoni trait is not selected
and mar 60 lost to mar 40 in competition on the one informative seed. This loop asks what the trait does to each life-history
component when each kind lives alone.

**World**: loop 2's world.py (20261027T0830-c54-distance-pays-competition/world.py), mutation off, founders all mar 40
(FOUNDER 1) or all mar 60 (FOUNDER 2). Arms: **dep** (depletion R 20 px, target -0.7, 200 t, with sink discs) on fresh seeds 620
and 621; **E** (sink discs only) on seed 620. 128^2, T = 2000. Readouts: c00's extract.py and c50's spread_stats.py (unchanged),
single.py (fates from the track table), single_plot.py, merges.py (cross-kind merges in loop 2's competition runs).

## Results (single.txt, single.png)

| seed | arm | bodies (t >= 500) | vanishings per split | path speed of dividing rods | median cycle (t) | median D (own rod lengths) | M passers |
|---|---|---|---|---|---|---|---|
| 620 | mar 40, dep | 5.9 | 0.85 | 0.25 | 338 | **3.69** | 8/10 |
| 620 | mar 60, dep | 6.3 | 0.89 | 0.39 | 305 | **3.17** | 9/15 |
| 621 | mar 40, dep | 11.1 | 1.29 | 0.16 | 470 | **2.92** | 5/11 |
| 621 | mar 60, dep | 9.0 | 1.22 | 0.33 | 322 | **3.07** | 7/14 |
| 620 | mar 40, sink discs only | 8.4 | 0.86 | 0.26 | 140 | 1.59 | 2/16 |
| 620 | mar 60, sink discs only | 10.0 | **1.35** | 0.38 | 175 | **2.42** | 4/13 |

(path speed in the table is the median over dividing rods from spread_stats.py; single.txt's vpath column is over all tracks
of >= 10 frames.)

- **With depletion, distance per cycle is the same for both kinds** (median D 3.69 vs 3.17 and 2.92 vs 3.07): mar-60 rods move
  1.5-2x faster and divide 10-30% sooner, so the extra speed is spent on a shorter cycle and the distance per cycle stays near
  the depletion radius (20 px, about 2-3 rod lengths). Passing shares are alike (8/10 vs 9/15; 5/11 vs 7/14).
- **Without depletion** (seed 620) mar 60 does go farther per cycle (2.42 vs 1.59, passers 4/13 vs 2/16) but loses more bodies
  per split (1.35 vs 0.86 vanishings per split).
- Alone under depletion neither kind pays a survival cost (vanishings per split 0.85-0.89 and 1.22-1.29), and population sizes are
  similar, so loop 2's loss of mar 60 in competition is not an intrinsic cost visible in monoculture; cross-kind merges in loop 2
  (merges.py on seed 610: depletion 4 merges of a mar-40 and a mar-60 body ending mar 40, 3 ending mar 60) do not explain it either.

## Reading

Birth-site depletion makes distance pay by fixing the distance: a daughter grows once it is out of the disc, so every rod that
divides has gone about one disc radius, whatever its trait. That raises the capability (loop 1) but levels the trait's effect on
it (this loop), so there is nothing heritable for selection to pick: the share of passers cannot carry "the heritable trait behind
it". A depletion rule that pays distance in proportion (the farther a rod gets before dividing, the more it grows) would be needed,
for example a supply that increases with distance from the birth site rather than a step at a fixed radius. Without depletion the
trait does change distance per cycle, but there it costs survival.

## Limits

Two seeds with depletion and one without; 6-11 bodies; 2000 t (5-6 cycles). Kinds are pure by construction here (mutation off).
Mar-60 monocultures show strong grid-scale stripes in the rendered fields during nucleation (runs/m60dep_s621/sheet.jpg, t 85-170),
as in loops 1-2 around high-surfactant mar-60 bodies; whether this numerical feature affects mar-60 survival was not tested (a dt/2
or dealiasing check is the obvious next step before trusting any cost of mar 60).
