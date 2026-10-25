# Evidence pack: cips-inhib (seed 1)

- world: `../../world_inh.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 50s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/p_noI --seeds 0 1 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9987], min area 6 px

## Measurements
- components: final 49, mean 52.8, max 75; occupancy final 0.13
- tracks: 102; persistent (alive >= 50% of run): 52; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 49], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00207/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 24, merge/split ratio n/a, nucleations 78
- channel total drift (end/start - 1): [-0.0, -0.2101, 0.1452, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 161: holes 0, rim-vs-core 0.31, rim-vs-outside 0.52, heterogeneity 0.08; core [0.979, 0.894, 0.117, 0.0] rim [0.774, 0.71, 0.264, 0.0]
  - track 1 at frame 161: holes 0, rim-vs-core 0.25, rim-vs-outside 0.47, heterogeneity 0.07; core [0.974, 0.843, 0.183, 0.0] rim [0.803, 0.698, 0.291, 0.0]
  - track 2 at frame 161: holes 0, rim-vs-core 0.35, rim-vs-outside 0.51, heterogeneity 0.09; core [0.978, 0.91, 0.068, 0.0] rim [0.746, 0.708, 0.234, 0.0]
  - track 3 at frame 161: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.07; core [0.978, 0.874, 0.16, 0.0] rim [0.809, 0.718, 0.281, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 335 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 48.2 (aggregate of 335 individuals; 0/335 membrane-like individually; rim level 0.941)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 3.91 (aggregate of 335 individuals; 0/335 membrane-like individually; rim level 0.82)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.75, rim/outside 0.674 (aggregate of 335 individuals; 0/335 membrane-like individually; rim level 0.442)
  - radial I: flat profile (no radial structure; level 0; aggregate of 335 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1610, R_eq 3.61): none; #1 (t=1610, R_eq 2.99): none; #2 (t=1610, R_eq 4.03): none; #3 (t=1610, R_eq 3.19): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
