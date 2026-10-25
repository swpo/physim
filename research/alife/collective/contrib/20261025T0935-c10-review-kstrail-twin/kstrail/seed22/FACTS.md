# Evidence pack: kstrail (seed 22)

- world: `../../../../../threads/chemotaxis-motility/worlds/kstrail/world.py`, family `chemotaxis`
- parent: None; mutation: Keller-Segel with volume filling + second, slow self-secreted repellent (trail)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 62s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/kstrail/world.py --out collective/contrib/20261025T0935-c10-review-kstrail-twin/kstrail --seeds 21 22 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9994], min area 6 px

## Measurements
- components: final 14, mean 9.0, max 14; occupancy final 0.06
- tracks: 59; persistent (alive >= 50% of run): 7; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.475/time; max body lengths 19.8
- replication (lineage window K = 20 frames = time 60, default): splits 16, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.438, nucleations 20
- channel total drift (end/start - 1): [-0.0001, -0.0001, -0.0001]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 123: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.15; core [0.865, 0.442, 0.33] rim [0.472, 0.352, 0.25]
  - track 30 at frame 143: holes 0, rim-vs-core 0.40, rim-vs-outside 0.34, heterogeneity 0.16; core [0.89, 0.492, 0.372] rim [0.508, 0.388, 0.289]
  - track 4 at frame 91: holes 0, rim-vs-core 0.43, rim-vs-outside 0.63, heterogeneity 0.20; core [0.99, 0.808, 0.617] rim [0.677, 0.601, 0.415]
  - track 50 at frame 182: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.13; core [0.862, 0.407, 0.301] rim [0.489, 0.325, 0.223]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 14 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.66)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 3.08 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.572)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.39 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.473)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=369, R_eq 4.98): none; #30 (t=429, R_eq 5.29): none; #4 (t=273, R_eq 7.98): none; #50 (t=546, R_eq 4.58): none

## Warnings
- radial: 1 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
