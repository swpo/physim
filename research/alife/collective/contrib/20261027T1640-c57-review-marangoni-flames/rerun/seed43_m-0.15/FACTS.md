# Evidence pack: marangoni-flames (seed 43)

- world: `../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c57-w15/m15 --seeds 43 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.37 of robust range [0.0, 0.6811], min area 6 px

## Measurements
- components: final 23, mean 17.4, max 44; occupancy final 0.03
- tracks: 131; persistent (alive >= 50% of run): 16; longest 589 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.86 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.026/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 20, default): splits 38, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.132, nucleations 17
- channel total drift (end/start - 1): [-0.8653, -0.2606, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 308: holes 0, rim-vs-core 0.55, rim-vs-outside 0.68, heterogeneity 0.14; core [0.973, 0.026, 0.534, 1.0] rim [0.678, 0.107, 0.943, 0.802]
  - track 95 at frame 313: holes 0, rim-vs-core 0.57, rim-vs-outside 0.68, heterogeneity 0.16; core [0.952, 0.019, 0.515, 0.959] rim [0.642, 0.112, 0.944, 0.757]
  - track 104 at frame 318: holes 0, rim-vs-core 0.57, rim-vs-outside 0.67, heterogeneity 0.15; core [0.938, 0.021, 0.525, 0.954] rim [0.635, 0.115, 0.953, 0.755]
  - track 117 at frame 484: holes 0, rim-vs-core 0.52, rim-vs-outside 0.67, heterogeneity 0.16; core [0.964, 0.03, 0.557, 0.996] rim [0.674, 0.108, 0.928, 0.784]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 110 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 30.4 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.809)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 14.9, rim/outside 0.636 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.237)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.34, rim/outside 3.29 (aggregate of 110 individuals; 110/110 membrane-like individually; rim level 0.95)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 74.9 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.909)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #60 (t=308, R_eq 2.39): ['|u|']; #95 (t=313, R_eq 2.76): ['|u|']; #104 (t=318, R_eq 2.76): ['|u|']; #117 (t=484, R_eq 2.46): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
