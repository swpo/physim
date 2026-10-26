# Q:marangoni-sink-escape: growing sink discs vs no-escape discs for the Marangoni rods (c45)

world.py: c34's Marangoni rods (CARGO=0) with the chemostat target as a field: phi_b(x,t) = -0.6 outside discs and phi_in = -1.2
inside, kr (phi_b(x,t) - phi) in real space. Discs open as a Poisson process (mean interval 200 t, uniform centres, RNG seeded
only by the seed) and grow at 0.08 px/t to R = 24 px, then close (life 300 t). Arm S: discs only lower the supply. Arm I
(control): same disc stream and field, and when a disc opens, every body whose centroid lies within R is removed (phi to
bath, Q = s = 0). Tuning (tune/, seed 0, mar 0, 150 frames): phi_in -1.2 and -1.6 both dissolve the bodies a disc catches
before it closes (2 of 2), so -1.2 was kept. Runs: S and I at mar 40 on seeds 90 and 91, S at mar 0 on seed 90; T=1600.
fate.py follows each body that a disc covers (labkit component within R one frame after opening) through its track and
descendants to the closing frame: escape (a descendant alive outside R), dissolve (none alive), stay (alive, all inside).
Selection: relative number of descendants alive two median cycles after birth regressed on standardized D (rod lengths),
path speed and straightness of dividing tracks (bootstrap 95% intervals).

| run | discs (closed in run) | bodies caught | escape / dissolve / stay | escape share | persistent splits | dividing tracks | median D | median path speed | gradient on D at fixed speed and straightness |
|---|---|---|---|---|---|---|---|---|---|
| S mar 40, seed 90 | 9 | 7 | 6 / 1 / 0 | 0.86 | 32 | 15 | 0.83 | 0.150 | -0.14 [-0.49, +0.05] |
| S mar 40, seed 91 | 6 | 5 | 3 / 2 / 0 | 0.60 | 31 | 17 | 1.87 | 0.226 | -0.15 [-0.34, +0.05] |
| S mar 0, seed 90 | 9 | 3 | 1 / 2 / 0 | 0.33 | 38 | 25 | 0.70 | 0.054 | -0.20 [-0.46, -0.02] |
| I mar 40, seed 90 | 9 | removed at opening | - | - | 33 | 22 | 1.77 | 0.212 | -0.03 [-0.39, +0.15] |
| I mar 40, seed 91 | 6 | removed at opening | - | - | 29 | 16 | 1.65 | 0.233 | -0.03 [-0.21, +0.12] |

(runs/*/fate.txt; the arm I disc logs list the removed bodies.)

## Against the question

- Escape share at mar 40 vs mar 0: 0.86 vs 0.33 on seed 90 (2.6x), 0.60 on seed 91 (mar 0 not run there). The direction is right but the
  counts are tiny (3-7 bodies caught per run): a disc of radius 24 covers about 11% of the box and the rods occupy about 8% of it, so
  a disc catches about one body.
- Gradient on D at fixed speed: negative in S on both seeds (-0.14, -0.15, intervals reaching +0.05) and about 0 in I (-0.03, -0.03):
  it is not positive in S and not larger than in I. **This fails the question's pass.**
- Rear-tip test (mtips.py) not run.

## Reading

With one disc per 200 t and one body caught per disc, the sink discs touch only a few percent of births, so their selection on
displacement is lost in the noise of who divides when. The negative gradient on D in both S runs (and at mar 0) is the same
long-cycle effect c00 described: rods that swim far per cycle are those with long cycles, and long cycles leave fewer
descendants after two median cycles; escape from discs does not offset it at this exposure. A stronger environment (a disc
rate several times higher, or larger discs) is needed before the escape benefit can show in descendants, and the mar 0 arm
needs a second seed.

## Limits

Two seeds for S and I, one for mar 0; T=1600 (about 4-6 generations); n = 15-25 dividing tracks per run for the regression.
In arm S the discs also lower total supply while they are open, so S and I differ in supply as well as in escape.
