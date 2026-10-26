# Evidence pack: r-two56-none (seed 2)

- world: `../../world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 7s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/pack_orig --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 4, mean 5.4, max 13; occupancy final 0.03
- tracks: 80; persistent (alive >= 50% of run): 4; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.41 (1 = constant size)
- enclosures: components with a hole mean 3.01, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [5, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 10, default): splits 33, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.242, nucleations 1
- channel total drift (end/start - 1): [-0.9461, -0.8748]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 39 at frame 128: holes 0, rim-vs-core 0.53, rim-vs-outside 0.46, heterogeneity 0.47; core [0.692, 0.483] rim [0.228, 0.733]
  - track 59 at frame 138: holes 0, rim-vs-core 0.68, rim-vs-outside 0.51, heterogeneity 0.47; core [0.712, 0.414] rim [0.147, 0.798]
  - track 60 at frame 139: holes 0, rim-vs-core 0.66, rim-vs-outside 0.50, heterogeneity 0.47; core [0.675, 0.421] rim [0.144, 0.804]
  - track 75 at frame 150: holes 1, rim-vs-core 0.70, rim-vs-outside 0.52, heterogeneity 0.47; core [0.747, 0.413] rim [0.153, 0.791]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.297, rim/outside 21.6 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.23)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 63.3 (aggregate of 31 individuals; 6/31 membrane-like individually; rim level 0.888)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #39 (t=64, R_eq 8.67): none; #59 (t=69, R_eq 9.01): none; #60 (t=69.5, R_eq 8.97): none; #75 (t=75, R_eq 8.94): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
