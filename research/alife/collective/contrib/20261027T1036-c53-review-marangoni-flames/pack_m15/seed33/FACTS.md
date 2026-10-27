# Evidence pack: marangoni-flames (seed 33)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c53-rev-mf/pack_m15 --seeds 32 33 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.36 of robust range [0.0, 0.6946], min area 6 px

## Measurements
- components: final 23, mean 19.6, max 39; occupancy final 0.03
- tracks: 101; persistent (alive >= 50% of run): 19; longest 599 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0253/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 20, default): splits 25, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.12, nucleations 15
- channel total drift (end/start - 1): [-0.883, -0.2698, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 303: holes 0, rim-vs-core 0.57, rim-vs-outside 0.67, heterogeneity 0.15; core [0.959, 0.043, 0.554, 0.998] rim [0.641, 0.122, 0.951, 0.76]
  - track 39 at frame 308: holes 0, rim-vs-core 0.61, rim-vs-outside 0.77, heterogeneity 0.15; core [1.0, 0.04, 0.448, 1.0] rim [0.694, 0.116, 0.938, 0.82]
  - track 55 at frame 308: holes 0, rim-vs-core 0.58, rim-vs-outside 0.67, heterogeneity 0.16; core [0.951, 0.041, 0.564, 0.989] rim [0.619, 0.128, 0.959, 0.732]
  - track 99 at frame 580: holes 0, rim-vs-core 0.53, rim-vs-outside 0.73, heterogeneity 0.14; core [0.986, 0.061, 0.502, 1.0] rim [0.69, 0.12, 0.895, 0.821]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 32.6 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.809)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.3, rim/outside 0.64 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.241)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.43, rim/outside 3.34 (aggregate of 123 individuals; 123/123 membrane-like individually; rim level 0.967)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 85.5 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.919)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #13 (t=303, R_eq 2.39): ['|u|']; #39 (t=308, R_eq 2.26): ['|u|']; #55 (t=308, R_eq 2.52): ['|u|']; #99 (t=580, R_eq 2.11): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
