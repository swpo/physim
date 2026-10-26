# Evidence pack: r-two56-none (seed 8)

- world: `../../../../contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 7s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/work_c35/rv/orig --seeds 7 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 6, mean 5.2, max 12; occupancy final 0.03
- tracks: 92; persistent (alive >= 50% of run): 2; longest 149 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.91 (1 = constant size)
- enclosures: components with a hole mean 4.00, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 10, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [10, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 10, default): splits 37, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 11, merge/split ratio 0.297, nucleations 1
- channel total drift (end/start - 1): [-0.9358, -0.8461]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 126: holes 1, rim-vs-core 0.79, rim-vs-outside 0.47, heterogeneity 0.47; core [0.853, 0.386] rim [0.171, 0.783]
  - track 60 at frame 131: holes 2, rim-vs-core 0.84, rim-vs-outside 0.51, heterogeneity 0.47; core [0.903, 0.371] rim [0.165, 0.771]
  - track 86 at frame 155: holes 1, rim-vs-core 0.67, rim-vs-outside 0.53, heterogeneity 0.47; core [0.644, 0.4] rim [0.139, 0.838]
  - track 89 at frame 173: holes 0, rim-vs-core 0.77, rim-vs-outside 0.45, heterogeneity 0.47; core [0.867, 0.422] rim [0.178, 0.776]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.398, rim/outside 9.13 (aggregate of 35 individuals; 4/35 membrane-like individually; rim level 0.27)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 12.7 (aggregate of 35 individuals; 8/35 membrane-like individually; rim level 0.776)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #43 (t=63, R_eq 8.65): none; #60 (t=65.5, R_eq 8.96): none; #86 (t=77.5, R_eq 8.97): none; #89 (t=86.5, R_eq 7.84): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
