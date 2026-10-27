# Evidence pack: reacting-thermals (seed 1)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 58s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack_g0 --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.42 of robust range [0.0, 0.6001], min area 6 px

## Measurements
- components: final 22, mean 13.5, max 53; occupancy final 0.02
- tracks: 161; persistent (alive >= 50% of run): 7; longest 347 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.33 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0378/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 20, default): splits 52, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 8, merge/split ratio 0.154, nucleations 12
- channel total drift (end/start - 1): [-0.8745, -0.2308, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 135 at frame 429: holes 0, rim-vs-core 0.19, rim-vs-outside 0.60, heterogeneity 0.06; core [0.955, 0.015, 0.0, 0.945] rim [0.791, 0.091, 0.0, 0.874]
  - track 127 at frame 212: holes 0, rim-vs-core 0.15, rim-vs-outside 0.56, heterogeneity 0.06; core [0.908, 0.012, 0.0, 0.881] rim [0.779, 0.093, 0.0, 0.86]
  - track 128 at frame 212: holes 0, rim-vs-core 0.14, rim-vs-outside 0.53, heterogeneity 0.05; core [0.908, 0.012, 0.0, 0.882] rim [0.791, 0.087, 0.0, 0.875]
  - track 149 at frame 514: holes 0, rim-vs-core 0.20, rim-vs-outside 0.66, heterogeneity 0.06; core [0.987, 0.025, 0.0, 0.988] rim [0.814, 0.096, 0.0, 0.911]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 18.6 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.866)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.6, rim/outside 0.598 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.219)
  - radial vorticity: flat profile (no radial structure; level 0; aggregate of 82 individuals)
  - radial burn r: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 54.6 (aggregate of 82 individuals; 1/82 membrane-like individually; rim level 0.906)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #135 (t=429, R_eq 2.59): none; #127 (t=212, R_eq 2.76): none; #128 (t=212, R_eq 2.71): none; #149 (t=514, R_eq 2.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
