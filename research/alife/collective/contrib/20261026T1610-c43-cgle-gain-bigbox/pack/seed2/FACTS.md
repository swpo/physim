# Evidence pack: cgle-gain (seed 2)

- world: `../../world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 1402s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T1610-c43-cgle-gain-bigbox/pack/seed2 --seeds 2 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3471], min area 6 px

## Measurements
- components: final 6, mean 4.8, max 8; occupancy final 0.08
- tracks: 43; persistent (alive >= 50% of run): 2; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.60 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [3, 3, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.426/time; max body lengths 4.9
- replication (lineage window K = 20 frames = time 100, default): splits 14, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 12, merge/split ratio 0.857, nucleations 0
- channel total drift (end/start - 1): [-0.8911, 1.3446, -0.1893]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 103: holes 0, rim-vs-core 0.48, rim-vs-outside 0.30, heterogeneity 0.22; core [0.836, 0.462, 0.231] rim [0.382, 0.445, 0.4]
  - track 36 at frame 166: holes 0, rim-vs-core 0.49, rim-vs-outside 0.29, heterogeneity 0.22; core [0.823, 0.545, 0.17] rim [0.367, 0.497, 0.333]
  - track 38 at frame 166: holes 0, rim-vs-core 0.48, rim-vs-outside 0.29, heterogeneity 0.22; core [0.829, 0.449, 0.212] rim [0.375, 0.456, 0.37]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 8.96 (aggregate of 29 individuals; 3/29 membrane-like individually; rim level 0.487)
  - radial Re A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 1.01 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.454)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.29, rim/outside 0.827 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.548)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=515, R_eq 7.09): none; #17 (t=360, R_eq 22): none; #36 (t=830, R_eq 8.1): none; #38 (t=830, R_eq 7.09): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
