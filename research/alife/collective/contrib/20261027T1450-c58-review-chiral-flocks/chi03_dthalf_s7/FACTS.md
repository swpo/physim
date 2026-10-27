# Evidence pack: chiral-eating-flocks (seed 7)

- world: `../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 80 steps x dt 0.25 = time 6000; grid [128, 128]; wall 53s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/20261027T1450-c58-review-chiral-flocks/chi03_dthalf_s7 --seeds 7 --frames 300 --spf 80 --threshold 0.45 --no-movie`
- segmentation: matter > 0.60 of robust range [0.0, 0.7462], min area 6 px

## Measurements
- components: final 20, mean 17.0, max 24; occupancy final 0.06
- tracks: 1620; persistent (alive >= 50% of run): 0; longest 21 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 14, 5], H1 [5, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.132/time; max body lengths 7.9
- replication (lineage window K = 20 frames = time 400, default): splits 302, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 212, merge/split ratio 0.702, nucleations 780
- channel total drift (end/start - 1): [0.7969, -0.4457, -0.3281, 1.49]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1195 at frame 227: holes 0, rim-vs-core 0.10, rim-vs-outside 0.22, heterogeneity 0.05; core [0.822, 0.032, 0.963, 0.075] rim [0.752, 0.101, 0.93, 0.076]
  - track 684 at frame 129: holes 0, rim-vs-core 0.13, rim-vs-outside 0.25, heterogeneity 0.09; core [0.868, 0.047, 0.954, 0.213] rim [0.765, 0.105, 0.918, 0.181]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 2.15 (aggregate of 94 individuals; 2/94 membrane-like individually; rim level 0.669)
  - radial food c: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 3.1, rim/outside 0.703 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.276)
  - radial |p|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 1.82 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.83)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.982, rim/outside 1.03 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.506)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #575 (t=2220, R_eq 2.33): none; #1195 (t=4540, R_eq 3.52): none; #637 (t=2320, R_eq 2.19): none; #684 (t=2580, R_eq 4.92): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 94 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
