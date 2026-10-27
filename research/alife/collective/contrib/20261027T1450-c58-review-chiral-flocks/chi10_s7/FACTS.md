# Evidence pack: chiral-eating-flocks (seed 7)

- world: `../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/20261027T1450-c58-review-chiral-flocks/chi10_s7 --seeds 7 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.5715], min area 6 px

## Measurements
- components: final 28, mean 22.2, max 29; occupancy final 0.38
- tracks: 1161; persistent (alive >= 50% of run): 3; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.39 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 30, 28], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 401, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 379, merge/split ratio 0.945, nucleations 3
- channel total drift (end/start - 1): [0.7807, -0.4598, -0.2873, 2.8034]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 568 at frame 214: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.12; core [0.669, 0.094, 0.853, 0.044] rim [0.537, 0.276, 0.668, 0.172]
  - track 605 at frame 219: holes 0, rim-vs-core 0.34, rim-vs-outside 0.49, heterogeneity 0.15; core [0.66, 0.099, 0.842, 0.344] rim [0.534, 0.288, 0.651, 0.506]
  - track 634 at frame 224: holes 0, rim-vs-core 0.35, rim-vs-outside 0.52, heterogeneity 0.14; core [0.685, 0.09, 0.854, 0.812] rim [0.549, 0.276, 0.67, 0.63]
  - track 705 at frame 242: holes 0, rim-vs-core 0.31, rim-vs-outside 0.50, heterogeneity 0.14; core [0.683, 0.093, 0.853, 0.455] rim [0.558, 0.276, 0.675, 0.582]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 141 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 2.82 (aggregate of 141 individuals; 2/141 membrane-like individually; rim level 0.611)
  - radial food c: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 4.75, rim/outside 0.981 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.499)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 3.14 (aggregate of 141 individuals; 2/141 membrane-like individually; rim level 0.743)
  - radial p_x: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 0.992 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.487)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #568 (t=2140, R_eq 8.23): none; #605 (t=2190, R_eq 8.48): none; #634 (t=2240, R_eq 7.74): none; #705 (t=2420, R_eq 7.88): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 141 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
