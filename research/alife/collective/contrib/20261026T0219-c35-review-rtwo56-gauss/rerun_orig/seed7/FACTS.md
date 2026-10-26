# Evidence pack: r-two56-none (seed 7)

- world: `../../../../contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/work_c35/rv/orig --seeds 7 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 8, mean 7.0, max 10; occupancy final 0.05
- tracks: 68; persistent (alive >= 50% of run): 8; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.96 (1 = constant size)
- enclosures: components with a hole mean 4.96, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 8, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [11, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 10, default): splits 26, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.192, nucleations 0
- channel total drift (end/start - 1): [-0.8914, -0.7492]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 111: holes 2, rim-vs-core 0.66, rim-vs-outside 0.48, heterogeneity 0.47; core [0.702, 0.439] rim [0.141, 0.786]
  - track 21 at frame 111: holes 1, rim-vs-core 0.73, rim-vs-outside 0.54, heterogeneity 0.47; core [0.753, 0.413] rim [0.135, 0.807]
  - track 46 at frame 126: holes 2, rim-vs-core 0.70, rim-vs-outside 0.44, heterogeneity 0.48; core [0.785, 0.408] rim [0.178, 0.757]
  - track 57 at frame 134: holes 2, rim-vs-core 0.74, rim-vs-outside 0.42, heterogeneity 0.47; core [0.726, 0.358] rim [0.14, 0.814]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.27, rim/outside 19.6 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.205)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 29.4 (aggregate of 45 individuals; 8/45 membrane-like individually; rim level 0.884)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=55.5, R_eq 8.96): none; #21 (t=55.5, R_eq 8.92): none; #46 (t=63, R_eq 8.81): none; #57 (t=67, R_eq 8.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 45 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
