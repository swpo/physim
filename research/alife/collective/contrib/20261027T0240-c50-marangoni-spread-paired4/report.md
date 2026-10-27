# Q:marangoni-swimmer-spread, loop 4 (c50): four paired seeds of the question's design

World and readouts: 20261027T0000-c50-marangoni-spread-loop1 (world.py, spread_stats.py, fate_kind.py; c45's mar 20/40/60
ladder copied by the rods' own majority-feedback surfactant, mutation 2.5e-3 per body per frame that never reads a body's
speed or displacement, all founders mar 40, growing sink discs one per 50 t at 0.08 px/t, no other removal). This loop adds
fresh seeds 502 and 503 (E and identical-event twin) to seeds 500 (loop 1) and 501 (loop 2). pool.py pairs them; pool.txt.

| seed | trait mean late (t >= 1000), E / twin | at T=2000, E / twin | mar-60 share late, E / twin | M passers, E / twin | D gradient in E |
|---|---|---|---|---|---|
| 500 | 42.6 / 35.0 | 45.7 / 36.7 | 0.20 / 0.05 | 1/17 / 2/17 | +0.00 [-0.19, +0.40] |
| 501 | 46.3 / 39.1 | 47.5 / 37.5 | 0.44 / 0.08 | 5/9 / 2/10 | +0.04 [-0.84, +3.0] |
| 502 | 38.7 / 35.4 | 43.1 / 35.7 | 0.10 / 0.03 | 4/19 / 4/17 | -0.11 [-0.34, -0.02] |
| 503 | 46.3 / 45.9 | 40.0 / 40.0 | 0.47 / 0.38 | 1/10 / 1/10 | -0.13 [-0.55, +0.31] |

E above the twin: **trait mean late on 4 of 4 seeds** (mean +4.7; +7.6, +7.2, +3.4, +0.4), at T=2000 on 3 of 4 (one tie);
**M-gate share on 1 of 4** (mean +0.07, carried by seed 501). Dividing rods passing the gate born after t 1000: E 2 of 14,
twin 2 of 17. The selection gradient on distance per cycle in E is never positive (+0.00, +0.04, -0.11, -0.13).

Heredity bookkeeping, seeds 502-503: kind changes on living bodies at logged mutations 20/20, 14/15 (E), 21/21, 15/16 (twin);
off-kind daughters 1/58, 5/36 (E), 3/57, 1/34 (twin). Escape share 0.80 and 0.72 in E vs 0.65 and 0.63 in the twin.
Persistent splits 29 and 18 in E, 29 and 17 in the twin; populations 6-21 bodies.

Food flashes (loop 3, 20261027T0210-c50-marangoni-spread-food) on the same seeds: trait mean at T=2000 60.0 / 36.0 in E
against 43.1 / 40.0 here; M passers 0/10 and 1/13 against 4/19 and 1/10 here. The food raised the trait on one seed and lowered
the passing share on both.

## Against the challenge

C:minority-swimmers-spread asks that the share of dividing rods passing the gate, with the heritable trait behind it, rise
consistently more in the selective environment than in the no-escape control and the twin. Over the four-loop campaign:
- heredity through fission in a self-copied species, mutation blind to the trait, continuing births and deaths from the
  environment, a minority capability in the ancestor: **met by the world** (inherited from c45's ladder and sink discs);
- the heritable trait (Marangoni coefficient) rises more in E than in the twin: **4 of 4 paired seeds**, small (+0.4 to +7.6
  ladder units) with 6-21 bodies per run;
- the passing share rises more in E than in the twin: **1 of 4**; and the no-escape control collapses or shrinks at this
  size (seed 500: 1 body; 501 fast: 4), so it cannot be read late.
So the selective environment selects the trait but not the capability. Loops 1-3 show why: escaping a disc rewards speed while
caught, and in this world a faster rod also divides sooner (speed vs cycle Spearman -0.28 to -0.65 across arms), so distance
per cycle, which the gate counts, is not what gets selected.

## What would

An environment where the payoff of moving cannot be spent on growth until the rod has travelled: for example supply placed at a
distance from a rod's birth site (daughters born into depletion, food a few rod lengths away), or divisions that need matter
from two patches. Or a second heritable axis that lengthens the cycle (a growth throttle such as c34's gated mobility gm) so
that speed and cycle can be selected apart. Larger domains (192^2-256^2, about 30-70 min per run here) would give 40-100
bodies and let a trait-mean shift of this size be read per seed.

## Limits

Four seeds at 128^2 and T=2000 (4-8 generations), 9-19 dividing rods per run; the trait-mean difference rests on a few
lineages per run. The no-escape control was run only on seeds 500 (slow) and 501 (fast). The twin shares the disc and mutation
streams but its bodies diverge after the first frames, so its events act on different bodies.
