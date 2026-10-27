# Evidence pack: marangoni-flames (seed 43)

- world: `../../20261027T0319-c51-marangoni-flames-negative/world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py --out collective/contrib/c57-w15/m0 --seeds 43 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.39 of robust range [0.0, 0.6477], min area 6 px

## Measurements
- components: final 19, mean 9.3, max 45; occupancy final 0.02
- tracks: 134; persistent (alive >= 50% of run): 1; longest 330 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.93 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 17], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0369/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 20, default): splits 43, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.116, nucleations 9
- channel total drift (end/start - 1): [-0.908, -0.1687, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 111 at frame 429: holes 0, rim-vs-core 0.21, rim-vs-outside 0.64, heterogeneity 0.06; core [0.953, 0.022, 0.0, 0.967] rim [0.778, 0.1, 0.0, 0.888]
  - track 115 at frame 454: holes 0, rim-vs-core 0.20, rim-vs-outside 0.63, heterogeneity 0.06; core [0.998, 0.019, 0.0, 1.0] rim [0.828, 0.087, 0.0, 0.923]
  - track 110 at frame 403: holes 0, rim-vs-core 0.23, rim-vs-outside 0.58, heterogeneity 0.07; core [0.954, 0.023, 0.0, 0.967] rim [0.767, 0.098, 0.0, 0.859]
  - track 116 at frame 539: holes 0, rim-vs-core 0.23, rim-vs-outside 0.62, heterogeneity 0.07; core [0.988, 0.03, 0.0, 0.995] rim [0.797, 0.103, 0.0, 0.898]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 18 (aggregate of 56 individuals; 1/56 membrane-like individually; rim level 0.873)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.8, rim/outside 0.6 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.221)
  - radial |u|: flat profile (no radial structure; level 0; aggregate of 56 individuals)
  - radial burn r: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 48.5 (aggregate of 56 individuals; 1/56 membrane-like individually; rim level 0.92)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #111 (t=429, R_eq 2.65): none; #115 (t=454, R_eq 2.33): none; #110 (t=403, R_eq 2.65): none; #116 (t=539, R_eq 2.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
