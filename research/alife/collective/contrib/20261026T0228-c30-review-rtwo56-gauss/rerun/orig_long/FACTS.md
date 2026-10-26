# Evidence pack: r-two56-none (seed 5)

- world: `../../../20261026T0205-c32-rtwo56-gauss-twin/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 601 frames x 5 steps x dt 0.1 = time 300; grid [192, 192]; wall 40s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0228-c30-review-rtwo56-gauss/rerun/orig_long --seeds 5 --frames 600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 6, mean 6.5, max 11; occupancy final 0.04
- tracks: 88; persistent (alive >= 50% of run): 6; longest 579 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.14 (1 = constant size)
- enclosures: components with a hole mean 5.17, final 6; holes at thresholds 0.2/0.35/0.5 final [0, 16, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [21, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 10, default): splits 35, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.229, nucleations 1
- channel total drift (end/start - 1): [-0.9181, -0.8098]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 313: holes 5, rim-vs-core 0.84, rim-vs-outside 0.51, heterogeneity 0.47; core [0.98, 0.42] rim [0.214, 0.764]
  - track 21 at frame 313: holes 2, rim-vs-core 0.71, rim-vs-outside 0.48, heterogeneity 0.47; core [0.821, 0.424] rim [0.195, 0.765]
  - track 43 at frame 333: holes 2, rim-vs-core 0.74, rim-vs-outside 0.49, heterogeneity 0.48; core [0.863, 0.417] rim [0.209, 0.752]
  - track 67 at frame 348: holes 2, rim-vs-core 0.74, rim-vs-outside 0.51, heterogeneity 0.47; core [0.904, 0.453] rim [0.22, 0.742]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.165, rim/outside 10.9 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.119)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 23.3 (aggregate of 40 individuals; 2/40 membrane-like individually; rim level 0.918)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=156.5, R_eq 8.59): none; #21 (t=156.5, R_eq 8.76): none; #43 (t=166.5, R_eq 8.72): none; #67 (t=174, R_eq 8.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
