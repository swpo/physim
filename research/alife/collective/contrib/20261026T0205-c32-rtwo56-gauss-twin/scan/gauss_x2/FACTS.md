# Evidence pack: r-two56-gauss (seed 0)

- world: `../../world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/scan/gauss_x2 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7713], min area 6 px

## Measurements
- components: final 1, mean 1.2, max 2; occupancy final 1.00
- tracks: 9; persistent (alive >= 50% of run): 1; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.60 (1 = constant size)
- enclosures: components with a hole mean 0.74, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 272]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [321, 91, 2], H1 [335, 119, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 10, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.667, nucleations 0
- channel total drift (end/start - 1): [2.2037, 0.9647]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 74: holes 8, rim-vs-core 0.06, rim-vs-outside 0.64, heterogeneity 0.28; core [0.572, 0.353] rim [0.541, 0.401]
  - track 7 at frame 178: holes 0, rim-vs-core 0.01, rim-vs-outside 0.56, heterogeneity 0.15; core [0.575, 0.354] rim [0.585, 0.35]
  - track 1 at frame 150: holes 0, rim-vs-core 0.02, rim-vs-outside 0.58, heterogeneity 0.16; core [0.574, 0.354] rim [0.594, 0.346]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 7 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.03 (aggregate of 7 individuals; 0/7 membrane-like individually; rim level 0.5)
  - radial A1: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 1.33 (aggregate of 7 individuals; 0/7 membrane-like individually; rim level 0.329)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=37, R_eq 86.69): none; #7 (t=89, R_eq 106.76): none; #8 (t=85.5, R_eq 12.33, ring): none; #1 (t=75, R_eq 103.01): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 7 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 7 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
