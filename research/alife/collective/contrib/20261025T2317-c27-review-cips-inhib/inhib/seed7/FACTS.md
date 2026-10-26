# Evidence pack: cips-inhib (seed 7)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 124s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27k/world.py --out collective/contrib/wip-c27k/inhib --seeds 7 8 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0017, 0.9866], min area 6 px

## Measurements
- components: final 37, mean 34.4, max 44; occupancy final 0.13
- tracks: 50; persistent (alive >= 50% of run): 39; longest 537 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio n/a, nucleations 44
- channel total drift (end/start - 1): [-0.0, -0.5683, 0.3916, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 333: holes 0, rim-vs-core 0.38, rim-vs-outside 0.40, heterogeneity 0.11; core [0.956, 0.909, 0.155, 0.887] rim [0.716, 0.71, 0.313, 0.744]
  - track 1 at frame 333: holes 0, rim-vs-core 0.35, rim-vs-outside 0.41, heterogeneity 0.10; core [0.947, 0.882, 0.211, 0.825] rim [0.709, 0.698, 0.347, 0.703]
  - track 2 at frame 338: holes 0, rim-vs-core 0.35, rim-vs-outside 0.40, heterogeneity 0.10; core [0.953, 0.895, 0.199, 0.837] rim [0.722, 0.707, 0.34, 0.711]
  - track 3 at frame 338: holes 0, rim-vs-core 0.31, rim-vs-outside 0.39, heterogeneity 0.09; core [0.939, 0.846, 0.241, 0.812] rim [0.72, 0.685, 0.356, 0.71]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 236 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 27.9 (aggregate of 236 individuals; 0/236 membrane-like individually; rim level 0.904)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 4.23 (aggregate of 236 individuals; 0/236 membrane-like individually; rim level 0.821)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.67, rim/outside 0.701 (aggregate of 236 individuals; 0/236 membrane-like individually; rim level 0.502)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 2.11 (aggregate of 236 individuals; 0/236 membrane-like individually; rim level 0.828)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3330, R_eq 4.51): none; #1 (t=3330, R_eq 4.07): none; #2 (t=3380, R_eq 4.15): none; #3 (t=3380, R_eq 3.66): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
