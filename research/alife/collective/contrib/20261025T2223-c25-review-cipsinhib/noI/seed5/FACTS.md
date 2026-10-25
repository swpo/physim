# Evidence pack: cips-inhib (seed 5)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 82s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2223-c25-review-cipsinhib/noI --seeds 5 6 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9988], min area 6 px

## Measurements
- components: final 47, mean 51.4, max 73; occupancy final 0.14
- tracks: 104; persistent (alive >= 50% of run): 50; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 47, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio n/a, nucleations 76
- channel total drift (end/start - 1): [0.0, -0.2158, 0.1484, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 159: holes 0, rim-vs-core 0.28, rim-vs-outside 0.50, heterogeneity 0.07; core [0.976, 0.863, 0.168, 0.0] rim [0.782, 0.697, 0.296, 0.0]
  - track 1 at frame 161: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.07; core [0.974, 0.847, 0.196, 0.0] rim [0.782, 0.691, 0.314, 0.0]
  - track 2 at frame 161: holes 0, rim-vs-core 0.31, rim-vs-outside 0.50, heterogeneity 0.08; core [0.976, 0.872, 0.125, 0.0] rim [0.764, 0.694, 0.265, 0.0]
  - track 5 at frame 161: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.06; core [0.976, 0.852, 0.215, 0.0] rim [0.812, 0.704, 0.327, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 327 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 49.9 (aggregate of 327 individuals; 0/327 membrane-like individually; rim level 0.945)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 4.01 (aggregate of 327 individuals; 0/327 membrane-like individually; rim level 0.824)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.63, rim/outside 0.677 (aggregate of 327 individuals; 0/327 membrane-like individually; rim level 0.454)
  - radial I: flat profile (no radial structure; level 0; aggregate of 327 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1590, R_eq 3.29): none; #1 (t=1610, R_eq 3.09): none; #2 (t=1610, R_eq 3.52): none; #5 (t=1610, R_eq 2.99): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
