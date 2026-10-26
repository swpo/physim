# Evidence pack: cgle-gain (seed 3)

- world: `../../../20261026T1610-c43-cgle-gain-bigbox/world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 651s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T2147-c46-review-cgle-bigbox/eps1.43/seed3 --seeds 3 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3447], min area 6 px

## Measurements
- components: final 4, mean 5.6, max 9; occupancy final 0.05
- tracks: 46; persistent (alive >= 50% of run): 2; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.18 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [2, 2, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 1.33/time; max body lengths 16.4
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 15, merge/split ratio 1.25, nucleations 0
- channel total drift (end/start - 1): [-0.9297, -0.6051, -0.1211]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 74: holes 0, rim-vs-core 0.54, rim-vs-outside 0.27, heterogeneity 0.22; core [0.85, 0.153, 0.459] rim [0.356, 0.35, 0.574]
  - track 26 at frame 116: holes 0, rim-vs-core 0.52, rim-vs-outside 0.31, heterogeneity 0.19; core [0.875, 0.156, 0.474] rim [0.381, 0.267, 0.58]
  - track 16 at frame 55: holes 0, rim-vs-core 0.44, rim-vs-outside 0.36, heterogeneity 0.21; core [0.849, 0.38, 0.262] rim [0.439, 0.486, 0.382]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.715, rim/outside 12.2 (aggregate of 31 individuals; 5/31 membrane-like individually; rim level 0.491)
  - radial Re A: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 0.983 (aggregate of 31 individuals; 1/31 membrane-like individually; rim level 0.432)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.81, rim/outside 0.859 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.575)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=370, R_eq 6.7): none; #26 (t=580, R_eq 6.36): none; #30 (t=590, R_eq 21.36): none; #16 (t=275, R_eq 7.14): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
