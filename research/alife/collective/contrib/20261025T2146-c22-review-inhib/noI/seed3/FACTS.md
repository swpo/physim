# Evidence pack: cips-inhib (seed 3)

- world: `../../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 67s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/wip-c22/rev_inh/noI/seed3 --seeds 3 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9991], min area 6 px

## Measurements
- components: final 47, mean 51.0, max 76; occupancy final 0.14
- tracks: 102; persistent (alive >= 50% of run): 52; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 47, 47], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00307/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 25, merge/split ratio n/a, nucleations 77
- channel total drift (end/start - 1): [0.0, -0.2163, 0.149, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.07; core [0.982, 0.891, 0.133, 0.0] rim [0.796, 0.714, 0.272, 0.0]
  - track 2 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.51, heterogeneity 0.07; core [0.974, 0.852, 0.207, 0.0] rim [0.762, 0.682, 0.334, 0.0]
  - track 5 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.50, heterogeneity 0.07; core [0.975, 0.85, 0.171, 0.0] rim [0.774, 0.685, 0.295, 0.0]
  - track 6 at frame 161: holes 0, rim-vs-core 0.28, rim-vs-outside 0.49, heterogeneity 0.07; core [0.977, 0.859, 0.162, 0.0] rim [0.782, 0.693, 0.288, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 323 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 48 (aggregate of 323 individuals; 0/323 membrane-like individually; rim level 0.939)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 3.92 (aggregate of 323 individuals; 0/323 membrane-like individually; rim level 0.813)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.12, rim/outside 0.68 (aggregate of 323 individuals; 0/323 membrane-like individually; rim level 0.442)
  - radial I: flat profile (no radial structure; level 0; aggregate of 323 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1610, R_eq 3.61): none; #2 (t=1610, R_eq 3.29): none; #5 (t=1610, R_eq 3.29): none; #6 (t=1610, R_eq 3.34): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
