# Evidence pack: marangoni-flames (seed 33)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c53-rev-mf/pack_m0 --seeds 32 33 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.37 of robust range [0.0, 0.6738], min area 6 px

## Measurements
- components: final 24, mean 14.4, max 38; occupancy final 0.03
- tracks: 120; persistent (alive >= 50% of run): 8; longest 549 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 24, 24], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0329/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 20, default): splits 38, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.079, nucleations 11
- channel total drift (end/start - 1): [-0.8899, -0.2455, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 88 at frame 328: holes 0, rim-vs-core 0.17, rim-vs-outside 0.56, heterogeneity 0.05; core [0.925, 0.04, 0.0, 0.939] rim [0.78, 0.104, 0.0, 0.881]
  - track 89 at frame 333: holes 0, rim-vs-core 0.12, rim-vs-outside 0.67, heterogeneity 0.05; core [0.918, 0.041, 0.0, 0.945] rim [0.816, 0.092, 0.0, 0.9]
  - track 92 at frame 418: holes 0, rim-vs-core 0.25, rim-vs-outside 0.62, heterogeneity 0.07; core [0.966, 0.049, 0.0, 0.995] rim [0.758, 0.119, 0.0, 0.867]
  - track 102 at frame 494: holes 0, rim-vs-core 0.24, rim-vs-outside 0.68, heterogeneity 0.07; core [0.986, 0.037, 0.0, 0.986] rim [0.783, 0.108, 0.0, 0.873]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 18.1 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.851)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.01, rim/outside 0.61 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.228)
  - radial |u|: flat profile (no radial structure; level 0; aggregate of 90 individuals)
  - radial burn r: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 52.1 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.91)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #88 (t=328, R_eq 2.46): none; #89 (t=333, R_eq 2.52): none; #92 (t=418, R_eq 2.39): none; #102 (t=494, R_eq 2.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
