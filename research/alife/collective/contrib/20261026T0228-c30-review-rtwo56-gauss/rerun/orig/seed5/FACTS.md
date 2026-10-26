# Evidence pack: r-two56-none (seed 5)

- world: `../../../../20261026T0205-c32-rtwo56-gauss-twin/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0228-c30-review-rtwo56-gauss/rerun/orig --seeds 5 6 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 7, mean 7.4, max 11; occupancy final 0.05
- tracks: 86; persistent (alive >= 50% of run): 7; longest 179 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.43 (1 = constant size)
- enclosures: components with a hole mean 4.42, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 11, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [14, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 10, default): splits 34, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.235, nucleations 1
- channel total drift (end/start - 1): [-0.9063, -0.7821]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 111: holes 2, rim-vs-core 0.72, rim-vs-outside 0.53, heterogeneity 0.47; core [0.8, 0.431] rim [0.172, 0.782]
  - track 21 at frame 113: holes 2, rim-vs-core 0.72, rim-vs-outside 0.52, heterogeneity 0.47; core [0.801, 0.423] rim [0.171, 0.774]
  - track 43 at frame 133: holes 0, rim-vs-core 0.60, rim-vs-outside 0.51, heterogeneity 0.48; core [0.709, 0.457] rim [0.197, 0.772]
  - track 40 at frame 121: holes 0, rim-vs-core 0.82, rim-vs-outside 0.50, heterogeneity 0.47; core [0.722, 0.378] rim [0.067, 0.873]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.302, rim/outside 14.8 (aggregate of 48 individuals; 2/48 membrane-like individually; rim level 0.229)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 20.5 (aggregate of 48 individuals; 7/48 membrane-like individually; rim level 0.889)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=55.5, R_eq 8.81): none; #21 (t=56.5, R_eq 8.88): none; #43 (t=66.5, R_eq 8.78): none; #40 (t=60.5, R_eq 8.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
