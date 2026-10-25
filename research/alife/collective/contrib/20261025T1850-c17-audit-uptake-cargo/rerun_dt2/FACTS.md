# Evidence pack: fch-uptake-micelles (seed 7)

- world: `../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 201 frames x 400 steps x dt 0.01 (--dt; world META dt 0.02) = time 800; grid [128, 128]; wall 481s; status ok
- command: `python -m labkit.run world.py --out rerun_dt2 --seeds 7 --dt 0.01 --spf 400 --no-movie`
- segmentation: matter > 0.13 of robust range [0.121, 2.9942], min area 6 px

## Measurements
- components: final 82, mean 51.5, max 82; occupancy final 0.41
- tracks: 171; persistent (alive >= 50% of run): 42; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [83, 83, 83], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.022/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 80, default): splits 78, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 6, merges 4, merge/split ratio 0.051, nucleations 7
- channel total drift (end/start - 1): [1.3416, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 103: holes 0, rim-vs-core 0.51, rim-vs-outside 0.10, heterogeneity 0.29; core [0.618, 0.23] rim [0.166, 0.001]
  - track 32 at frame 104: holes 0, rim-vs-core 0.50, rim-vs-outside 0.10, heterogeneity 0.29; core [0.606, 0.218] rim [0.154, 0.001]
  - track 34 at frame 104: holes 0, rim-vs-core 0.29, rim-vs-outside 0.30, heterogeneity 0.30; core [0.599, 0.246] rim [0.348, 0.104]
  - track 150 at frame 190: holes 0, rim-vs-core 0.47, rim-vs-outside 0.11, heterogeneity 0.21; core [0.63, 0.102] rim [0.172, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 341 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.517, rim/outside 4.98 (aggregate of 341 individuals; 3/341 membrane-like individually; rim level 0.481)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.039, rim/outside 1.68 (aggregate of 341 individuals; 3/341 membrane-like individually; rim level 0.0148)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=412, R_eq 5.11): none; #32 (t=416, R_eq 5.26): none; #34 (t=416, R_eq 5.14): none; #150 (t=760, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.01 only relabels time (world META dt 0.02): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 1 of 341 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
