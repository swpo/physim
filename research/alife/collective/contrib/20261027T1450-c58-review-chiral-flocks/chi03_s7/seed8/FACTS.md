# Evidence pack: chiral-eating-flocks (seed 8)

- world: `../../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/20261027T1450-c58-review-chiral-flocks/chi03_s7 --seeds 7 8 --frames 300 --spf 40 --threshold 0.45 --no-movie`
- segmentation: matter > 0.59 of robust range [0.0, 0.7613], min area 6 px

## Measurements
- components: final 15, mean 18.6, max 25; occupancy final 0.05
- tracks: 1807; persistent (alive >= 50% of run): 0; longest 21 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 14, 5], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.215/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 200, default): splits 338, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 255, merge/split ratio 0.754, nucleations 851
- channel total drift (end/start - 1): [0.3998, -0.4002, -0.4336, 0.8326]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1375 at frame 237: holes 0, rim-vs-core 0.06, rim-vs-outside 0.19, heterogeneity 0.06; core [0.809, 0.117, 0.931, 0.199] rim [0.759, 0.147, 0.911, 0.179]
  - track 270 at frame 55: holes 0, rim-vs-core 0.11, rim-vs-outside 0.24, heterogeneity 0.05; core [0.846, 0.052, 0.955, 0.0] rim [0.766, 0.116, 0.92, 0.013]
  - track 1396 at frame 237: holes 0, rim-vs-core 0.28, rim-vs-outside 0.34, heterogeneity 0.11; core [0.855, 0.054, 0.63, 0.219] rim [0.763, 0.122, 0.88, 0.186]
  - track 601 at frame 113: holes 0, rim-vs-core 0.07, rim-vs-outside 0.17, heterogeneity 0.07; core [0.815, 0.118, 0.927, 0.585] rim [0.766, 0.146, 0.906, 0.619]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 103 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 2.22 (aggregate of 103 individuals; 1/103 membrane-like individually; rim level 0.677)
  - radial food c: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.9, rim/outside 0.71 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.286)
  - radial |p|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 1.87 (aggregate of 103 individuals; 1/103 membrane-like individually; rim level 0.84)
  - radial p_x: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 1.01 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.485)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1375 (t=2370, R_eq 3.29): none; #270 (t=550, R_eq 4.15): none; #1396 (t=2370, R_eq 6.23, ring): ['density rho']; #601 (t=1130, R_eq 2.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 15 of 103 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
