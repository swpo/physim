# Evidence pack: marangoni-flames (seed 4)

- world: `../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 50 steps x dt 0.04 = time 1200; grid [128, 128]; wall 96s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/20261027T1500-c58-review-marangoni-flames/pack_m15_dthalf --seeds 4 --frames 600 --spf 50 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7346], min area 6 px

## Measurements
- components: final 7, mean 5.5, max 44; occupancy final 0.01
- tracks: 104; persistent (alive >= 50% of run): 4; longest 549 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.17 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.013/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 40, default): splits 26, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.154, nucleations 7
- channel total drift (end/start - 1): [-0.9676, -0.0921, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 97 at frame 328: holes 0, rim-vs-core 0.53, rim-vs-outside 0.73, heterogeneity 0.14; core [0.974, 0.056, 0.513, 1.0] rim [0.716, 0.146, 0.952, 0.891]
  - track 96 at frame 232: holes 0, rim-vs-core 0.56, rim-vs-outside 0.70, heterogeneity 0.15; core [0.935, 0.049, 0.462, 0.996] rim [0.687, 0.154, 0.944, 0.894]
  - track 94 at frame 212: holes 0, rim-vs-core 0.55, rim-vs-outside 0.72, heterogeneity 0.15; core [0.976, 0.053, 0.504, 1.0] rim [0.697, 0.151, 0.962, 0.91]
  - track 98 at frame 484: holes 0, rim-vs-core 0.51, rim-vs-outside 0.73, heterogeneity 0.14; core [0.999, 0.066, 0.57, 1.0] rim [0.71, 0.152, 0.973, 0.898]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 39.3 (aggregate of 32 individuals; 1/32 membrane-like individually; rim level 0.887)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.51, rim/outside 0.659 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.283)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.64, rim/outside 3.41 (aggregate of 32 individuals; 32/32 membrane-like individually; rim level 0.973)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 94.6 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.981)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #97 (t=656, R_eq 2.71): ['|u|']; #96 (t=464, R_eq 3.09): ['|u|']; #94 (t=424, R_eq 2.88): ['|u|']; #98 (t=968, R_eq 2.52): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
