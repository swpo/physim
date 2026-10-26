# Evidence pack: cips-fuel (seed 5)

- world: `../../../20261026T0146-c25-cips-slowp-negative-fix/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 72s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0146-c25-cips-slowp-negative-fix/world.py --out collective/contrib/20261026T0221-c30-review-cips-slowp/rerun/st_dp1 --seeds 5 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.52 of robust range [0.0009, 0.9531], min area 6 px

## Measurements
- components: final 20, mean 20.4, max 40; occupancy final 0.14
- tracks: 65; persistent (alive >= 50% of run): 13; longest 235 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 20], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00509/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 21, merge/split ratio n/a, nucleations 44
- channel total drift (end/start - 1): [0.0, -0.5317, 0.4421]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 184: holes 0, rim-vs-core 0.23, rim-vs-outside 0.28, heterogeneity 0.07; core [0.896, 0.855, 0.017] rim [0.696, 0.755, 0.081]
  - track 1 at frame 184: holes 0, rim-vs-core 0.25, rim-vs-outside 0.30, heterogeneity 0.07; core [0.918, 0.881, 0.013] rim [0.701, 0.767, 0.081]
  - track 5 at frame 184: holes 0, rim-vs-core 0.24, rim-vs-outside 0.28, heterogeneity 0.07; core [0.928, 0.894, 0.011] rim [0.729, 0.784, 0.07]
  - track 6 at frame 187: holes 0, rim-vs-core 0.22, rim-vs-outside 0.28, heterogeneity 0.07; core [0.907, 0.89, 0.015] rim [0.715, 0.789, 0.074]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 9.32 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.757)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 2.65 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.839)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.4, rim/outside 0.523 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.398)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1840, R_eq 4.26): none; #1 (t=1840, R_eq 4.72): none; #5 (t=1840, R_eq 4.72): none; #6 (t=1870, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 130 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
