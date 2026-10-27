# Evidence pack: reacting-thermals (seed 0)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/20261027T0040-c49-reacting-thermals-claim/pack --seeds 0 1 2 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7549], min area 6 px

## Measurements
- components: final 26, mean 14.8, max 43; occupancy final 0.02
- tracks: 381; persistent (alive >= 50% of run): 0; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 33, 28], H1 [0, 0, 0]
- motion: 144 long-lived tracks moved >= 1 body length; max speed 1.28/time; max body lengths 23.0
- replication (lineage window K = 20 frames = time 20, default): splits 92, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 8, merges 11, merge/split ratio 0.12, nucleations 150
- channel total drift (end/start - 1): [-0.8764, -0.3436, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 194 at frame 449: holes 0, rim-vs-core 0.25, rim-vs-outside 0.59, heterogeneity 0.13; core [0.887, 0.116, 0.345, 0.938] rim [0.694, 0.161, 0.285, 0.793]
  - track 189 at frame 418: holes 0, rim-vs-core 0.25, rim-vs-outside 0.53, heterogeneity 0.14; core [0.896, 0.079, 0.302, 0.915] rim [0.703, 0.127, 0.288, 0.764]
  - track 244 at frame 494: holes 0, rim-vs-core 0.22, rim-vs-outside 0.49, heterogeneity 0.13; core [0.888, 0.093, 0.451, 0.952] rim [0.73, 0.131, 0.458, 0.805]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 5.44 (aggregate of 61 individuals; 1/61 membrane-like individually; rim level 0.652)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.79, rim/outside 0.68 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.255)
  - radial vorticity: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.07 (aggregate of 61 individuals; 12/61 membrane-like individually; rim level 0.497)
  - radial burn r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 6.53 (aggregate of 61 individuals; 2/61 membrane-like individually; rim level 0.676)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #194 (t=449, R_eq 1.95): none; #189 (t=418, R_eq 2.26): none; #244 (t=494, R_eq 2.11): none; #340 (t=575, R_eq 2.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
