# Evidence pack: r-two56-none (seed 1)

- world: `../../world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/pack_orig --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 5, mean 5.1, max 15; occupancy final 0.04
- tracks: 100; persistent (alive >= 50% of run): 2; longest 151 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.49 (1 = constant size)
- enclosures: components with a hole mean 3.46, final 3; holes at thresholds 0.2/0.35/0.5 final [1, 6, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 5], H1 [11, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 10, default): splits 41, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 8, merge/split ratio 0.195, nucleations 2
- channel total drift (end/start - 1): [-0.9099, -0.8109]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 126: holes 1, rim-vs-core 0.65, rim-vs-outside 0.53, heterogeneity 0.47; core [0.669, 0.429] rim [0.141, 0.811]
  - track 76 at frame 148: holes 2, rim-vs-core 0.88, rim-vs-outside 0.48, heterogeneity 0.48; core [0.871, 0.307] rim [0.15, 0.806]
  - track 11 at frame 50: holes 1, rim-vs-core 0.46, rim-vs-outside 0.46, heterogeneity 0.45; core [0.615, 0.39] rim [0.29, 0.711]
  - track 81 at frame 146: holes 1, rim-vs-core 0.72, rim-vs-outside 0.49, heterogeneity 0.47; core [0.766, 0.368] rim [0.178, 0.78]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.534, rim/outside 13 (aggregate of 30 individuals; 4/30 membrane-like individually; rim level 0.353)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 12.4 (aggregate of 30 individuals; 9/30 membrane-like individually; rim level 0.776)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=63, R_eq 9.03): none; #76 (t=74, R_eq 8.44): none; #11 (t=25, R_eq 8.72): none; #81 (t=73, R_eq 8.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
