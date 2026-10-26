# Review of 20261025T2238-c22-metabolic-crawler-regrowth (rim uptake gives a size set point; whole-body synthesis does not)

Written before reading other reviews. The author's cutrun.py (30% front cut at t=8, branched undamaged twin) on fresh
seeds, run to t=40 instead of 30; labkit run of the rim world with the cut inside it on seed 3 (rerun/).

Area (cut / twin):

| run | t=8.5 | t=15 | t=20 | t=30 | t=40 | gap t=8.5 -> 40 | speed t>35 cut / twin |
|---|---|---|---|---|---|---|---|
| rim s3 | 1.59 / 2.40 | 1.74 / 2.24 | 1.75 / 2.13 | 1.79 / 2.02 | 1.81 / 1.94 | 0.81 -> 0.13 | 0.39 / 0.40 |
| rim s4 | 1.57 / 2.38 | 1.72 / 2.24 | 1.76 / 2.13 | 1.80 / 2.03 | 1.82 / 1.94 | 0.81 -> 0.13 | 0.39 / 0.40 |
| whole body s3 | 1.67 / 2.57 | 1.64 / 2.47 | 1.57 / 2.39 | 1.49 / 2.24 | 1.42 / 2.11 | 0.90 -> 0.69 | 0.36 / 0.41 |

- Rim uptake: the cut cell re-polarizes within ~3 t (cuts/met3_s3/cut.png), crawls at its twin's speed, and keeps
  growing slowly after the first rebound (1.75 -> 1.81 from t=20 to 40) while the twin keeps shrinking (2.13 -> 1.94).
  The gap closes to 0.13 on both seeds by t=40, so the two converge toward a common size near 1.85-1.9; neither has
  stopped moving at t=40, so the set point is still not pinned down, as the finding says.
- Whole-body synthesis: both arms shrink in parallel, the cut cell never regrows and the gap stays at 0.69, as reported.
- Part of the closing in the rim arm is the twin's own descent (the box's nutrient has not reached steady state), not
  only regrowth of the cut cell; the cut cell's own regrowth is +0.22-0.25 area units (14-16%).

Verdict: Supported. Limits: planted crawler, one parameter set per arm, two seeds for rim and one for whole body;
the nutrient dependence is by construction.
