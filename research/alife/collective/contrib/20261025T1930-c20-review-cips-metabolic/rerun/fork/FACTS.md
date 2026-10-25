# Evidence pack: cips-fuel (seed 5)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 201 frames x 100 steps x dt 0.1 = time 2000; grid [256, 256]; wall 313s; status ok
- command: `python -m labkit.run /tmp/c20ci/world.py --out /tmp/c20ci/fork --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0001, 0.998], min area 6 px

## Measurements
- components: final 0, mean 169.1, max 297; occupancy final 0.00
- tracks: 378; persistent (alive >= 50% of run): 201; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 20, 2], H1 [32, 12, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 70, merge/split ratio 70, nucleations 306
- channel total drift (end/start - 1): [0.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 89: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.09; core [0.986, 0.956, 0.615] rim [0.793, 0.781, 0.688]
  - track 1 at frame 87: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.08; core [0.982, 0.92, 0.642] rim [0.799, 0.757, 0.701]
  - track 2 at frame 87: holes 0, rim-vs-core 0.14, rim-vs-outside 0.58, heterogeneity 0.08; core [0.969, 0.881, 0.652] rim [0.851, 0.808, 0.677]
  - track 4 at frame 87: holes 0, rim-vs-core 0.28, rim-vs-outside 0.49, heterogeneity 0.09; core [0.977, 0.909, 0.646] rim [0.758, 0.738, 0.707]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1009 components >= 12 px at frames [34, 67, 101, 133]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 36.5 (aggregate of 1009 individuals; 0/1009 membrane-like individually; rim level 0.929)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 2.88 (aggregate of 1009 individuals; 0/1009 membrane-like individually; rim level 0.841)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.897 (aggregate of 1009 individuals; 0/1009 membrane-like individually; rim level 0.774)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=890, R_eq 3.91): none; #1 (t=870, R_eq 3.34): none; #2 (t=870, R_eq 3.29): none; #4 (t=870, R_eq 3.39): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 1009 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
