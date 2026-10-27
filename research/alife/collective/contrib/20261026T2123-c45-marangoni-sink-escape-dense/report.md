# Q:marangoni-sink-escape, loop 2: four times the disc rate (c45)

Same world and analysis as loop 1 (20261026T2053-c45-marangoni-sink-escape), with discs opening once per 50 t instead of
200 t (disc_dt 50; R 24, 0.08 px/t, phi_in -1.2). Arms: S (discs lower the supply; caught bodies dissolve or escape) and I
(same disc stream, caught bodies removed at opening) at mar 40 on seeds 90 and 91, and S at mar 0 on both seeds. T=1600.
fate.py per run (runs/*/fate.txt); c00's mtips.py for the rear-tip test (runs/*/tips.txt); pooled_sel.py pools the two seeds
(traits standardized within run, relative descendants within run).

| run | bodies caught | escape / dissolve | escape share | persistent splits | dividing tracks (extract.py) | median D | median path speed |
|---|---|---|---|---|---|---|---|
| S mar 40, s90 | 43 | 23 / 20 | 0.53 | 22 | 14 | 2.03 | 0.222 |
| S mar 40, s91 | 41 | 23 / 18 | 0.56 | 23 | 8 | 1.93 | 0.266 |
| S mar 0, s90 | 27 | 4 / 23 | 0.15 | 15 | 8 | 0.53 | 0.042 |
| S mar 0, s91 | 27 | 6 / 21 | 0.22 | 12 | 4 | 0.49 | 0.048 |
| I mar 40, s90 | removed at opening | - | - | 19 | 9 | 1.25 | 0.170 |
| I mar 40, s91 | removed at opening | - | - | 14 | 5 | 1.11 | 0.198 |

Rear tip (mtips.py, its own dividing set): the rear tip advances at least 2/3 of the net displacement in 16 of 22 and 15 of 22
dividing rods in S, against 8 of 14 and 4 of 12 in I; every rod that moves 3 Feret lengths translates (S 2 + 2, I 1 + 1).

Selection, pooled over the two seeds (pooled_sel.txt), gradients of relative descendants two median cycles after birth on
standardized D, path speed and straightness:
S mar 40 (n 22): D +0.015 [-0.133, +0.225], speed -0.141 [-0.332, +0.058], straightness +0.317 [+0.103, +0.491];
I mar 40 (n 14): D -0.322 [-0.684, -0.086], speed +0.175 [-0.158, +0.547], straightness +0.212 [-0.160, +0.488];
S mar 0 (n 12): D -0.030 [-0.537, +0.531].

## Against the question

1. Escape share at mar 40 at least twice that at mar 0 on both seeds: 0.53 vs 0.15 (3.5x), 0.56 vs 0.22 (2.5x). **Pass.**
2. Gradient on D at fixed speed positive in S and larger than in I: larger than in I (+0.02 vs -0.32, the I interval excludes 0)
   but not positive (interval -0.13 to +0.23). **Half pass.** Loop 1 at a quarter of the disc rate gave -0.14 and -0.15 in S.
3. Passers translate as often in S as in I: S 70% of dividing rods translate vs 43% in I; all 3-length movers translate. **Pass.**

## Reading

When discs are frequent enough to catch about 40 bodies per run, swimming rods escape a growing sink 2.5-3.5 times as often
as non-swimming ones, and the escape environment removes the cost that distance per cycle carries in the removal control
(where far-swimming, long-cycle rods leave fewer descendants, gradient -0.32). It does not yet make distance pay outright.
Dividing rods in S swim further per cycle than in I (median D 1.93-2.03 vs 1.11-1.25), by translation, which reflects
which rods survive the discs. The cost: the dense discs lower the division count (persistent splits 22-23 in S and 14-19 in I
against 29-38 at the lower rate), so n per run is small (8-14 dividing tracks).

## Limits

Two seeds; selection rests on 22 (S) and 14 (I) dividing tracks pooled. In S the discs also lower total supply while open,
so S and I differ in supply as well as in escape. The S arm's higher D may partly reflect survivorship (rods that escaped are
the ones that later divide), which is the selection the question is after but is not separated here from plasticity.
