# Q:marangoni-distance-pays, loop 1 (c54): birth-site depletion makes distance per cycle pay, but plastically, not by selection

**World** (world.py): c50's spread world (20261027T0000-c50-marangoni-spread-loop1: c45's self-copied mar 20/40/60 surfactant
ladder, all founders mar 40, trait-blind mutation 2.5e-3 per body per frame, growing sink discs one per 50 t) plus a
**birth-site depletion** (DEP=1): at every frame boundary the bodies are labelled; a body of the previous frame whose pixels
overlap two or more current bodies (area >= 6 px) is a split, and a disc of radius 20 px (about 2 rod lengths) centred on that
parent's last centroid sets the chemostat target to dep_in for 200 t (about one median cycle). Daughters must leave their birth
site to grow. The rule reads where a split happened and nothing about any body's kind, speed, size, age or displacement; it acts
on every body inside the disc alike. The world was run from `collective/contrib/20261027T0540-c54-distance-pays-loop1/` (the
draft name of this directory; metrics.json and FACTS.md carry that path); the code is unchanged.

**Screen** (seed 600): dep_in -1.0 went extinct (no dividing rod after t 300); -0.8 kept only 2-9 bodies (5 of 9 dividing rods
passed the M gate); **-0.7** keeps 6-15 bodies and was used. 128^2, T=2000, unstructured start.

**Arms** on fresh seeds 600, 601, 602: **dep** (depletion, ladder); **twin** (depletion, MARS 40/40/40: identical-event twin);
**glob** (DEP=2: the same split detection, but each split lowers the chemostat target uniformly over the whole domain by the
same integrated amount, so moving cannot change the supply); **E** (c50's sink-disc world, no depletion). Drive-off with
depletion (MARS 0/0/0) on seeds 600 and 601. Readouts: c00's extract.py and c50's spread_stats.py (unchanged), pool.py.

## Results (pool.txt, paired3.png)

| seed | arm | M passers (3 own rod lengths, rear tip >= 2/3) | median D (rod lengths per cycle) | trait mean, t >= 1000 | D gradient | bodies late |
|---|---|---|---|---|---|---|
| 600 | dep | **7/15** | 2.61 | 37.1 | -0.04 | 11 |
| 600 | twin | 3/11 | 2.31 | 42.6 | +0.08 | 12 |
| 600 | glob | 1/11 | 1.60 | 36.5 | -0.04 | 11 |
| 600 | E | 4/17 | 1.71 | 39.6 | +0.23 | 15 |
| 601 | dep | **6/11** | 3.57 | 39.1 | -0.26 | 10 |
| 601 | twin | 2/7 | 2.68 | 35.7 | +0.66 | 10 |
| 601 | glob | 3/12 | 1.88 | 37.3 | +0.19 | 11 |
| 601 | E | 1/10 | 1.55 | 42.4 | -0.07 | 13 |
| 602 | dep | **6/15** | 2.51 | 32.4 | -0.09 | 6 |
| 602 | twin | 7/16 | 2.96 | 43.4 | -0.15 | 8 |
| 602 | glob | 1/16 | 1.96 | 39.6 | -0.12 | 7 |
| 602 | E | 3/20 | 1.62 | 41.3 | -0.17 | 10 |
| 600 | drive-off + dep | 0/6 | 1.21 (k1) | - | - | - |
| 601 | drive-off + dep | 0/3 | 1.0-1.8 | - | - | - |

- **Distance pays, as intended**: with depletion at the birth site, 40-55% of dividing rods swim 3 of their own lengths between
  birth and division (dep 19/41 pooled, twin 12/34) against 5/39 when the same supply loss is spread everywhere (glob) and 8/47
  in the sink-disc world (E). dep > glob and dep > E on 3 of 3 seeds; median D rises from 1.6-2.0 to 2.5-3.6 rod lengths.
- The passers translate (rear-tip test) and need the drive: with the Marangoni drive off and the same depletion, 0 of 9
  dividing rods pass (median D about 1), so depletion does not move rods by dissolving one side.
- **But it is not selection**: the heritable trait does not rise. Trait mean late: dep below E on 3 of 3 seeds, below the
  twin on 2 of 3 (the twin's labels drift with no effect); the selection gradient of descendants on distance per cycle is
  negative in dep on 3 of 3 seeds (-0.04, -0.26, -0.09). dep's passing share is above the twin's on 2 of 3 (+0.19, +0.26,
  -0.04): the twin, with every body at the ancestral trait, passes almost as often, so the rise is the bodies' response to the
  environment, not a heritable change. Nearly all dividing rods are the ancestral mar-40 kind (dep: 14/15, 10/11, all of 602's
  dividing rods k0 or k1); mutants rarely reach division in 2000 t.

## Against the challenge

C:minority-swimmers-spread asks that the share of passers, **with the heritable trait behind it**, rise more in the selective
environment than in the twin. Here the passing share rises in the depletion environment, but just as much in its twin, and the
trait does not follow it. The capability stops being a minority-by-chance and becomes a plastic response to where a rod was born
(40-55% instead of 10-25%). This is negative for the challenge and positive for the question's first half: an environment rule
blind to kind, speed and displacement can make distance per cycle (not speed) what matters for supply.

## Limits

Three paired seeds at 128^2, 6-15 bodies, 2000 t (about 5 median cycles; only 2-6 dividing rods per run born after t 1000, so
the share cannot be read as a time course). Mutants (mar 20 / mar 60) are 0-38% of bodies late and rarely divide, so the trait
has little variance to select on; a competition assay (mar 40 vs mar 60 founders, mutation off) is the next loop. The kind of a
body is read only on rendered frames. Mar-60 bodies at high surfactant show grid-scale ripples in the rendered fields (sheet of
dep seed 601, t 1210-1645), a numerical feature of the parent world that this loop did not test. Split detection for the
depletion uses pixel overlap between frames 5 t apart; it also fires on a few fragmentations and does not wait for persistence.
