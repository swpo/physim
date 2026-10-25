# Evidence pack: cips-fuel (seed 5)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 201 frames x 100 steps x dt 0.1 = time 2000; grid [256, 256]; wall 314s; status ok
- command: `python -m labkit.run /tmp/c20ci/world.py --out /tmp/c20ci/fed --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 0.9987], min area 6 px

## Measurements
- components: final 209, mean 217.4, max 297; occupancy final 0.13
- tracks: 390; persistent (alive >= 50% of run): 229; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [210, 209, 209], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 84, merge/split ratio n/a, nucleations 306
- channel total drift (end/start - 1): [0.0, -0.1981, 0.1365]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 111: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.09; core [0.973, 0.856, 0.163] rim [0.786, 0.699, 0.286]
  - track 1 at frame 111: holes 0, rim-vs-core 0.32, rim-vs-outside 0.50, heterogeneity 0.10; core [0.976, 0.877, 0.126] rim [0.759, 0.693, 0.275]
  - track 2 at frame 111: holes 0, rim-vs-core 0.15, rim-vs-outside 0.61, heterogeneity 0.10; core [0.966, 0.843, 0.141] rim [0.849, 0.767, 0.201]
  - track 3 at frame 111: holes 0, rim-vs-core 0.28, rim-vs-outside 0.48, heterogeneity 0.10; core [0.974, 0.857, 0.14] rim [0.779, 0.695, 0.267]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1437 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 40.7 (aggregate of 1437 individuals; 0/1437 membrane-like individually; rim level 0.933)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 3.77 (aggregate of 1437 individuals; 0/1437 membrane-like individually; rim level 0.814)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.54, rim/outside 0.67 (aggregate of 1437 individuals; 0/1437 membrane-like individually; rim level 0.439)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1110, R_eq 3.09): none; #1 (t=1110, R_eq 3.43): none; #2 (t=1110, R_eq 3.29): none; #3 (t=1110, R_eq 3.14): none

## Warnings
- radial: 1 of 1437 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
