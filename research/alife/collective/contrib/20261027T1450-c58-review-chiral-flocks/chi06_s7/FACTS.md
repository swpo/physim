# Evidence pack: chiral-eating-flocks (seed 7)

- world: `../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/20261027T1450-c58-review-chiral-flocks/chi06_s7 --seeds 7 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6737], min area 6 px

## Measurements
- components: final 13, mean 15.8, max 28; occupancy final 0.26
- tracks: 2464; persistent (alive >= 50% of run): 0; longest 17 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 18, 12], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 200, default): splits 892, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 739, merge/split ratio 0.828, nucleations 38
- channel total drift (end/start - 1): [0.7009, -0.4377, -0.3384, 0.7324]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 137 at frame 30: holes 0, rim-vs-core 0.20, rim-vs-outside 0.47, heterogeneity 0.10; core [0.546, 0.135, 0.798, 0.879] rim [0.506, 0.281, 0.709, 0.777]
  - track 50 at frame 15: holes 0, rim-vs-core 0.32, rim-vs-outside 0.71, heterogeneity 0.17; core [0.819, 0.023, 0.923, 0.701] rim [0.624, 0.226, 0.781, 0.741]
  - track 317 at frame 53: holes 0, rim-vs-core 0.16, rim-vs-outside 0.60, heterogeneity 0.15; core [0.575, 0.092, 0.833, 0.608] rim [0.533, 0.216, 0.749, 0.657]
  - track 942 at frame 118: holes 0, rim-vs-core 0.28, rim-vs-outside 0.77, heterogeneity 0.19; core [0.803, 0.056, 0.913, 0.677] rim [0.635, 0.242, 0.79, 0.705]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 3.01 (aggregate of 84 individuals; 2/84 membrane-like individually; rim level 0.507)
  - radial food c: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 4.12, rim/outside 0.844 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.478)
  - radial |p|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 3.36 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.692)
  - radial p_x: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 0.999 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.493)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #137 (t=300, R_eq 8.41): none; #50 (t=150, R_eq 8.52): none; #317 (t=530, R_eq 10.75, ring): ['density rho']; #942 (t=1180, R_eq 6.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
