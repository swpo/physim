# Evidence pack: marangoni-flames (seed 5)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 40s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/20261027T1500-c58-review-marangoni-flames/pack_m15 --seeds 4 5 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7316], min area 6 px

## Measurements
- components: final 7, mean 4.8, max 40; occupancy final 0.01
- tracks: 106; persistent (alive >= 50% of run): 1; longest 337 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.50 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 7, 6], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0227/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 20, default): splits 29, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.103, nucleations 5
- channel total drift (end/start - 1): [-0.9672, -0.0913, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 71 at frame 182: holes 0, rim-vs-core 0.58, rim-vs-outside 0.73, heterogeneity 0.14; core [0.962, 0.05, 0.449, 0.997] rim [0.721, 0.155, 0.958, 0.948]
  - track 18 at frame 156: holes 0, rim-vs-core 0.55, rim-vs-outside 0.70, heterogeneity 0.13; core [0.983, 0.049, 0.463, 1.0] rim [0.754, 0.147, 0.958, 0.968]
  - track 98 at frame 454: holes 0, rim-vs-core 0.54, rim-vs-outside 0.78, heterogeneity 0.15; core [0.986, 0.066, 0.544, 1.0] rim [0.694, 0.161, 0.98, 0.905]
  - track 99 at frame 454: holes 0, rim-vs-core 0.52, rim-vs-outside 0.79, heterogeneity 0.13; core [0.993, 0.069, 0.571, 1.0] rim [0.695, 0.162, 0.985, 0.928]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 26.5 (aggregate of 28 individuals; 1/28 membrane-like individually; rim level 0.802)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.82, rim/outside 0.652 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.291)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.36, rim/outside 3.14 (aggregate of 28 individuals; 28/28 membrane-like individually; rim level 0.927)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 44.5 (aggregate of 28 individuals; 1/28 membrane-like individually; rim level 0.881)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #71 (t=182, R_eq 3.09): ['|u|']; #18 (t=156, R_eq 2.93): ['|u|']; #98 (t=454, R_eq 2.82): ['|u|']; #99 (t=454, R_eq 2.76): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
