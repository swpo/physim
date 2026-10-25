# Evidence pack: cips-inhib (seed 4)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 76s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2213-c21-review-cips-inhib/noI --seeds 4 5 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.999], min area 6 px

## Measurements
- components: final 46, mean 52.5, max 80; occupancy final 0.14
- tracks: 115; persistent (alive >= 50% of run): 48; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 46, 46], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00761/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 29, merge/split ratio n/a, nucleations 86
- channel total drift (end/start - 1): [0.0, -0.2209, 0.1519, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 159: holes 0, rim-vs-core 0.28, rim-vs-outside 0.50, heterogeneity 0.07; core [0.978, 0.864, 0.163, 0.0] rim [0.791, 0.7, 0.287, 0.0]
  - track 3 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.07; core [0.974, 0.849, 0.178, 0.0] rim [0.762, 0.678, 0.306, 0.0]
  - track 5 at frame 161: holes 0, rim-vs-core 0.17, rim-vs-outside 0.58, heterogeneity 0.07; core [0.981, 0.9, 0.079, 0.0] rim [0.877, 0.801, 0.164, 0.0]
  - track 7 at frame 161: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.06; core [0.978, 0.849, 0.19, 0.0] rim [0.815, 0.7, 0.3, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 329 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 43.3 (aggregate of 329 individuals; 0/329 membrane-like individually; rim level 0.94)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 3.82 (aggregate of 329 individuals; 0/329 membrane-like individually; rim level 0.807)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.73, rim/outside 0.688 (aggregate of 329 individuals; 0/329 membrane-like individually; rim level 0.449)
  - radial I: flat profile (no radial structure; level 0; aggregate of 329 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1590, R_eq 3.34): none; #3 (t=1610, R_eq 3.34): none; #5 (t=1610, R_eq 3.87): none; #7 (t=1610, R_eq 3.09): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
