# Evidence pack: marangoni-flames (seed 32)

- world: `../../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c53-rev-mf/pack_m0 --seeds 32 33 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.7952], min area 6 px

## Measurements
- components: final 16, mean 8.7, max 44; occupancy final 0.02
- tracks: 127; persistent (alive >= 50% of run): 0; longest 273 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0375/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 20, default): splits 42, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.119, nucleations 9
- channel total drift (end/start - 1): [-0.9351, -0.1676, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 103 at frame 373: holes 0, rim-vs-core 0.22, rim-vs-outside 0.62, heterogeneity 0.06; core [0.907, 0.056, 0.0, 0.968] rim [0.729, 0.134, 0.0, 0.87]
  - track 107 at frame 373: holes 0, rim-vs-core 0.19, rim-vs-outside 0.62, heterogeneity 0.06; core [0.914, 0.053, 0.0, 0.964] rim [0.754, 0.128, 0.0, 0.906]
  - track 86 at frame 131: holes 0, rim-vs-core 0.13, rim-vs-outside 0.54, heterogeneity 0.04; core [0.844, 0.039, 0.0, 0.875] rim [0.753, 0.128, 0.0, 0.91]
  - track 111 at frame 514: holes 0, rim-vs-core 0.26, rim-vs-outside 0.63, heterogeneity 0.07; core [0.964, 0.063, 0.0, 0.997] rim [0.742, 0.138, 0.0, 0.882]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 18.8 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.853)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.44, rim/outside 0.628 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.245)
  - radial |u|: flat profile (no radial structure; level 0; aggregate of 55 individuals)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 55.9 (aggregate of 55 individuals; 1/55 membrane-like individually; rim level 0.941)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #103 (t=373, R_eq 2.71): none; #107 (t=373, R_eq 2.65): none; #86 (t=131, R_eq 2.99): none; #111 (t=514, R_eq 2.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
