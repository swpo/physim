# Evidence pack: reacting-thermals (seed 0)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack_g0 --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7534], min area 6 px

## Measurements
- components: final 11, mean 6.0, max 49; occupancy final 0.01
- tracks: 121; persistent (alive >= 50% of run): 0; longest 289 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.0394/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 20, default): splits 34, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.176, nucleations 6
- channel total drift (end/start - 1): [-0.9543, -0.1153, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 109 at frame 459: holes 0, rim-vs-core 0.17, rim-vs-outside 0.59, heterogeneity 0.04; core [0.963, 0.048, 0.0, 1.0] rim [0.81, 0.116, 0.0, 0.973]
  - track 104 at frame 182: holes 0, rim-vs-core 0.12, rim-vs-outside 0.54, heterogeneity 0.04; core [0.823, 0.036, 0.0, 0.893] rim [0.754, 0.119, 0.0, 0.941]
  - track 102 at frame 161: holes 0, rim-vs-core 0.11, rim-vs-outside 0.60, heterogeneity 0.05; core [0.811, 0.04, 0.0, 0.882] rim [0.747, 0.119, 0.0, 0.928]
  - track 111 at frame 529: holes 0, rim-vs-core 0.23, rim-vs-outside 0.67, heterogeneity 0.06; core [0.987, 0.068, 0.0, 1.0] rim [0.775, 0.133, 0.0, 0.953]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 37 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 19.1 (aggregate of 37 individuals; 1/37 membrane-like individually; rim level 0.842)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.84, rim/outside 0.62 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.245)
  - radial vorticity: flat profile (no radial structure; level 0; aggregate of 37 individuals)
  - radial burn r: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 56.9 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.948)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #109 (t=459, R_eq 2.39): none; #104 (t=182, R_eq 3.04): none; #102 (t=161, R_eq 3.19): none; #111 (t=529, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
