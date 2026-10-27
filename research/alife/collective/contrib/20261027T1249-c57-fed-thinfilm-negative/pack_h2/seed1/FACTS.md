# Evidence pack: fed-thinfilm (seed 1)

- world: `../../world.py`, family `thin-film`
- parent: collective/contrib/20261025T1915-c24-thinfilm-sighting; mutation: non-conserved film: condensation from a consumed, regrowing vapour along the film's own chemical potential, and decay of liquid inside drops
- run: 61 frames x 200 steps x dt 0.25 = time 3000; grid [128, 128]; wall 77s; status ok
- command: `python -m labkit.run collective/contrib/c57-w3/world.py --out collective/contrib/c57-w3/pack_h2 --seeds 0 1 --size 128 128 --frames 60 --no-movie`
- segmentation: matter > 0.20 of robust range [0.1158, 2.0737], min area 6 px

## Measurements
- components: final 8, mean 11.2, max 20; occupancy final 0.12
- tracks: 41; persistent (alive >= 50% of run): 8; longest 54 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.43 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.0303/time; max body lengths 4.9
- replication (lineage window K = 20 frames = time 1000, default): splits 11, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 8, merge/split ratio 0.727, nucleations 0
- channel total drift (end/start - 1): [-0.686, 9.071, -488.9543, -1298.7275, -0.0629]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 34: holes 0, rim-vs-core 0.39, rim-vs-outside 0.23, heterogeneity 0.11; core [0.702, 0.934, 0.175, 0.126, 0.155] rim [0.33, 0.865, 0.21, 0.164, 0.231]
  - track 12 at frame 35: holes 0, rim-vs-core 0.42, rim-vs-outside 0.27, heterogeneity 0.12; core [0.727, 0.906, 0.254, 0.931, 0.175] rim [0.331, 0.811, 0.277, 0.861, 0.25]
  - track 18 at frame 35: holes 0, rim-vs-core 0.35, rim-vs-outside 0.22, heterogeneity 0.09; core [0.649, 0.925, 0.035, 0.335, 0.213] rim [0.317, 0.849, 0.081, 0.344, 0.269]
  - track 34 at frame 42: holes 0, rim-vs-core 0.38, rim-vs-outside 0.24, heterogeneity 0.10; core [0.7, 0.922, 0.2, 0.11, 0.199] rim [0.335, 0.838, 0.249, 0.142, 0.251]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.662, rim/outside 7.29 (aggregate of 77 individuals; 1/77 membrane-like individually; rim level 0.543)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 1.66 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.898)
  - radial p_x: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.967 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.407)
  - radial p_y: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 0.938 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.342)
  - radial vapour V: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.06, rim/outside 0.826 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.328)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1700, R_eq 8.27): none; #12 (t=1750, R_eq 8.2): none; #18 (t=1750, R_eq 7.61): none; #34 (t=2100, R_eq 7.74): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
