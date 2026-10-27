# Evidence pack: chiral-eating-flocks (seed 42)

- world: `../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 80 steps x dt 0.25 = time 6000; grid [128, 128]; wall 52s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/c57-w14/chi0.03_dthalf --seeds 42 --frames 300 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7454], min area 6 px

## Measurements
- components: final 21, mean 14.8, max 29; occupancy final 0.19
- tracks: 2490; persistent (alive >= 50% of run): 0; longest 10 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 21, 10], H1 [7, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 400, default): splits 893, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 855, merge/split ratio 0.957, nucleations 40
- channel total drift (end/start - 1): [0.7572, -0.4452, -0.4097, 1.1571]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 13: holes 0, rim-vs-core 0.30, rim-vs-outside 0.64, heterogeneity 0.17; core [0.733, 0.082, 0.896, 0.776] rim [0.575, 0.266, 0.79, 0.633]
  - track 455 at frame 66: holes 0, rim-vs-core 0.20, rim-vs-outside 0.51, heterogeneity 0.14; core [0.645, 0.133, 0.866, 0.431] rim [0.531, 0.255, 0.774, 0.48]
  - track 48 at frame 10: holes 0, rim-vs-core 0.25, rim-vs-outside 0.28, heterogeneity 0.11; core [0.632, 0.236, 0.816, 0.157] rim [0.474, 0.362, 0.695, 0.25]
  - track 66 at frame 10: holes 0, rim-vs-core 0.11, rim-vs-outside 0.20, heterogeneity 0.06; core [0.531, 0.366, 0.691, 0.543] rim [0.458, 0.406, 0.616, 0.527]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 2.83 (aggregate of 93 individuals; 5/93 membrane-like individually; rim level 0.472)
  - radial food c: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 3.02, rim/outside 0.823 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.45)
  - radial |p|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 3 (aggregate of 93 individuals; 3/93 membrane-like individually; rim level 0.665)
  - radial p_x: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.961 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.466)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #58 (t=260, R_eq 9.77, ring): none; #455 (t=1320, R_eq 8.97): none; #48 (t=200, R_eq 4.03): none; #66 (t=200, R_eq 2.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 93 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
