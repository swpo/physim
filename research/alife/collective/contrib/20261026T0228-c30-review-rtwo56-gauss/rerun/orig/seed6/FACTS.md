# Evidence pack: r-two56-none (seed 6)

- world: `../../../../20261026T0205-c32-rtwo56-gauss-twin/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 11s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0228-c30-review-rtwo56-gauss/rerun/orig --seeds 5 6 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 5, mean 5.4, max 13; occupancy final 0.03
- tracks: 66; persistent (alive >= 50% of run): 5; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.61 (1 = constant size)
- enclosures: components with a hole mean 3.95, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 8, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [10, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10, default): splits 25, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.12, nucleations 0
- channel total drift (end/start - 1): [-0.9341, -0.8444]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 34 at frame 124: holes 1, rim-vs-core 0.75, rim-vs-outside 0.46, heterogeneity 0.47; core [0.845, 0.4] rim [0.185, 0.747]
  - track 35 at frame 124: holes 2, rim-vs-core 0.68, rim-vs-outside 0.44, heterogeneity 0.48; core [0.833, 0.455] rim [0.22, 0.743]
  - track 38 at frame 124: holes 2, rim-vs-core 0.69, rim-vs-outside 0.51, heterogeneity 0.47; core [0.73, 0.395] rim [0.164, 0.796]
  - track 17 at frame 50: holes 1, rim-vs-core 0.56, rim-vs-outside 0.39, heterogeneity 0.45; core [0.734, 0.521] rim [0.207, 0.71]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.276, rim/outside 19.7 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.218)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 60.4 (aggregate of 32 individuals; 4/32 membrane-like individually; rim level 0.88)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #34 (t=62, R_eq 8.9): none; #35 (t=62, R_eq 8.41): none; #38 (t=62, R_eq 8.9): none; #17 (t=25, R_eq 8.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
