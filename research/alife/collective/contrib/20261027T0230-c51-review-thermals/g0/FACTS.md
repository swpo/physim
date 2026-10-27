# Evidence pack: reacting-thermals (seed 7)

- world: `../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 36s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0230-c51-review-thermals/g0 --seeds 7 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.36 of robust range [0.0, 0.7038], min area 6 px

## Measurements
- components: final 19, mean 11.3, max 44; occupancy final 0.02
- tracks: 128; persistent (alive >= 50% of run): 5; longest 505 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.82 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.0367/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 20, default): splits 39, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.231, nucleations 6
- channel total drift (end/start - 1): [-0.9022, -0.1977, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 81 at frame 267: holes 0, rim-vs-core 0.14, rim-vs-outside 0.53, heterogeneity 0.05; core [0.909, 0.011, 0.0, 0.901] rim [0.79, 0.086, 0.0, 0.88]
  - track 103 at frame 292: holes 0, rim-vs-core 0.19, rim-vs-outside 0.58, heterogeneity 0.06; core [0.944, 0.019, 0.0, 0.952] rim [0.783, 0.091, 0.0, 0.879]
  - track 105 at frame 413: holes 0, rim-vs-core 0.21, rim-vs-outside 0.63, heterogeneity 0.06; core [0.959, 0.022, 0.0, 0.972] rim [0.781, 0.096, 0.0, 0.878]
  - track 112 at frame 454: holes 0, rim-vs-core 0.21, rim-vs-outside 0.62, heterogeneity 0.07; core [0.963, 0.018, 0.0, 0.973] rim [0.791, 0.096, 0.0, 0.884]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 17.1 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.849)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.7, rim/outside 0.593 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.217)
  - radial vorticity: flat profile (no radial structure; level 0; aggregate of 70 individuals)
  - radial burn r: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 44.2 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.892)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #81 (t=267, R_eq 2.65): none; #103 (t=292, R_eq 2.59): none; #105 (t=413, R_eq 2.52): none; #112 (t=454, R_eq 2.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
