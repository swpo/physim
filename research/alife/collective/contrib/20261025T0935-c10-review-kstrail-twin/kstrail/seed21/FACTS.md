# Evidence pack: kstrail (seed 21)

- world: `../../../../../threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 77s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out collective/contrib/20261025T0935-c10-review-kstrail-twin/kstrail --seeds 21 22 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9985], min area 6 px

## Measurements
- components: final 12, mean 9.3, max 16; occupancy final 0.05
- tracks: 76; persistent (alive >= 50% of run): 5; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [1, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.582/time; max body lengths 15.5
- replication (lineage window K = 20 frames = time 60, default): splits 18, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 0.889, nucleations 24
- channel total drift (end/start - 1): [-0.0, -0.0, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 121: holes 0, rim-vs-core 0.40, rim-vs-outside 0.56, heterogeneity 0.20; core [0.964, 0.749, 0.611] rim [0.634, 0.578, 0.455]
  - track 20 at frame 129: holes 0, rim-vs-core 0.38, rim-vs-outside 0.34, heterogeneity 0.16; core [0.887, 0.605, 0.403] rim [0.522, 0.511, 0.327]
  - track 26 at frame 138: holes 0, rim-vs-core 0.47, rim-vs-outside 0.54, heterogeneity 0.21; core [0.938, 0.902, 0.792] rim [0.608, 0.686, 0.538]
  - track 2 at frame 87: holes 0, rim-vs-core 0.45, rim-vs-outside 0.30, heterogeneity 0.17; core [0.876, 0.644, 0.501] rim [0.463, 0.519, 0.377]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 15.1 (aggregate of 61 individuals; 1/61 membrane-like individually; rim level 0.712)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 3.08 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.654)
  - radial h: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 4.5 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.539)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=363, R_eq 6.53): none; #20 (t=387, R_eq 4.95): none; #26 (t=414, R_eq 8.43): none; #2 (t=261, R_eq 5.75): none

## Warnings
- radial: 1 of 61 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
