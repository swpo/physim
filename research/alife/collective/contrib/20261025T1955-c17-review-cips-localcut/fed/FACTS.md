# Evidence pack: cips-fuel (seed 4)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 251 frames x 100 steps x dt 0.1 = time 2500; grid [256, 256]; wall 220s; status ok
- command: `python -m labkit.run world.py --out fed --seeds 4 --frames 250 --spf 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 0.9988], min area 6 px

## Measurements
- components: final 188, mean 209.4, max 307; occupancy final 0.14
- tracks: 431; persistent (alive >= 50% of run): 210; longest 232 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [191, 190, 188], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 113, merge/split ratio n/a, nucleations 318
- channel total drift (end/start - 1): [0.0, -0.2145, 0.1478]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 134: holes 0, rim-vs-core 0.26, rim-vs-outside 0.53, heterogeneity 0.10; core [0.983, 0.878, 0.153] rim [0.815, 0.718, 0.275]
  - track 1 at frame 134: holes 0, rim-vs-core 0.28, rim-vs-outside 0.50, heterogeneity 0.09; core [0.979, 0.868, 0.178] rim [0.795, 0.702, 0.305]
  - track 2 at frame 134: holes 0, rim-vs-core 0.23, rim-vs-outside 0.48, heterogeneity 0.08; core [0.976, 0.84, 0.226] rim [0.821, 0.7, 0.33]
  - track 3 at frame 134: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.09; core [0.983, 0.876, 0.166] rim [0.819, 0.717, 0.29]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1353 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 42.7 (aggregate of 1353 individuals; 0/1353 membrane-like individually; rim level 0.933)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 3.81 (aggregate of 1353 individuals; 0/1353 membrane-like individually; rim level 0.81)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.79, rim/outside 0.681 (aggregate of 1353 individuals; 0/1353 membrane-like individually; rim level 0.45)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1340, R_eq 3.29): none; #1 (t=1340, R_eq 3.24): none; #2 (t=1340, R_eq 2.88): none; #3 (t=1340, R_eq 3.19): none

## Warnings
- radial: 1 of 1353 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
