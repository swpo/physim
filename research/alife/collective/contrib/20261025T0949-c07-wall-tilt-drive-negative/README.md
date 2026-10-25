# A label-free wall-tilt ("treadmilling") drive does not make ring cells swim

World: `world.py` = ringswim-waste (20261025T0806-c07-ringswim-claim/world_claim.py) with the
per-body phoretic drift off (mu = 0) and a local, label-free drive in the Allen-Cahn tilt:

    tilt += a_s * w * (Sw - Sm),  w = 4 phi (1 - phi)  (the wall)
    Sw = G_3 [w S] / G_3 [w]      (S averaged across the wall thickness)
    Sm = G_8 [w S] / G_8 [w]      (wall-weighted mean over the cell scale)

so the wall should advance where the substrate is above the cell's wall mean (the fresh front)
and retract where it is below (the depleted wake), with zero net growth. 128^2, seed 1, T=10000.

| a_s | cells at end | max BL (labkit) | persistent splits | what the sheet shows |
|---|---|---|---|---|
| 0 | 18 | 1.6 | 16 | static ringed cells (mu=0 control) |
| 3 | 15 | 1.5 | 16 | as a_s=0, slightly fewer cells |
| 5 | 0 | 1.4 | 6 | cells thin out and die by t=10000 |
| 7 | 5 | 1.6 | 13 | a cluster of 4-6 cells drifts together across the domain; individual cells barely move; near extinction (`img/a_s7.png`) |
| 10 | 0 | 1.0 | 1 | all die |

Two earlier versions died at every a_s tried (`data/summary.txt` a2, w3, w10; `img/naive_tilt_a3.png`):
a tilt a_s (S - G[S]) on the whole field drains the interior, which is always depleted; a
wall-only tilt without the cross-wall average punches a hole from the inside, because the inner
face of the wall sits in depleted substrate and the outer face in fresh substrate. The cross-wall
average removes that, but the remaining front-back asymmetry is too weak to translate a cell before
it destabilizes it.

Reading: a growth/retraction (treadmilling) drive in the tilt is not a substitute for the
per-body drift in this cell; individual motility stays <= 1.6 BL at every setting that survives.
Limits: one seed, one sig_s (8) and wall average (3 px), T=10000; no a_s between 3 and 5 or above
7 with other sig_s.
