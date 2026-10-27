# Evidence pack: marangoni-flames (seed 4)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 53s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/20261027T1500-c58-review-marangoni-flames/pack_m15 --seeds 4 5 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7346], min area 6 px

## Measurements
- components: final 7, mean 5.4, max 44; occupancy final 0.01
- tracks: 105; persistent (alive >= 50% of run): 4; longest 549 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.17 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0268/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 20, default): splits 26, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.154, nucleations 7
- channel total drift (end/start - 1): [-0.9678, -0.0916, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 98 at frame 328: holes 0, rim-vs-core 0.53, rim-vs-outside 0.73, heterogeneity 0.14; core [0.975, 0.057, 0.513, 1.0] rim [0.715, 0.147, 0.952, 0.891]
  - track 96 at frame 237: holes 0, rim-vs-core 0.56, rim-vs-outside 0.69, heterogeneity 0.15; core [0.932, 0.049, 0.461, 0.995] rim [0.687, 0.153, 0.94, 0.892]
  - track 95 at frame 212: holes 0, rim-vs-core 0.55, rim-vs-outside 0.72, heterogeneity 0.15; core [0.976, 0.053, 0.505, 1.0] rim [0.697, 0.152, 0.962, 0.91]
  - track 99 at frame 484: holes 0, rim-vs-core 0.51, rim-vs-outside 0.73, heterogeneity 0.14; core [0.999, 0.067, 0.573, 1.0] rim [0.707, 0.153, 0.973, 0.899]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 38.5 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.873)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.28, rim/outside 0.653 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.281)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.56, rim/outside 3.4 (aggregate of 32 individuals; 32/32 membrane-like individually; rim level 0.974)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 95.6 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.97)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #98 (t=328, R_eq 2.71): ['|u|']; #96 (t=237, R_eq 3.09): ['|u|']; #95 (t=212, R_eq 2.88): ['|u|']; #99 (t=484, R_eq 2.52): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
