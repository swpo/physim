# Evidence pack: cips-inhib (seed 0)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 100s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2157-c24-review-cips-inhibitor/inhib_defaults/seed0 --seeds 0 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0006, 0.9951], min area 6 px

## Measurements
- components: final 39, mean 37.6, max 51; occupancy final 0.13
- tracks: 63; persistent (alive >= 50% of run): 44; longest 262 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 38], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio n/a, nucleations 52
- channel total drift (end/start - 1): [0.0, -0.4616, 0.3179, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 171: holes 0, rim-vs-core 0.37, rim-vs-outside 0.46, heterogeneity 0.10; core [0.97, 0.912, 0.094, 0.92] rim [0.734, 0.702, 0.274, 0.865]
  - track 3 at frame 171: holes 0, rim-vs-core 0.37, rim-vs-outside 0.46, heterogeneity 0.09; core [0.968, 0.899, 0.125, 0.916] rim [0.73, 0.691, 0.299, 0.863]
  - track 4 at frame 171: holes 0, rim-vs-core 0.34, rim-vs-outside 0.45, heterogeneity 0.09; core [0.969, 0.884, 0.148, 0.912] rim [0.748, 0.691, 0.304, 0.864]
  - track 5 at frame 171: holes 0, rim-vs-core 0.37, rim-vs-outside 0.47, heterogeneity 0.10; core [0.973, 0.914, 0.102, 0.919] rim [0.74, 0.701, 0.284, 0.863]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 255 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 25.1 (aggregate of 255 individuals; 0/255 membrane-like individually; rim level 0.908)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 4.1 (aggregate of 255 individuals; 0/255 membrane-like individually; rim level 0.794)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.33, rim/outside 0.695 (aggregate of 255 individuals; 0/255 membrane-like individually; rim level 0.486)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 1.19 (aggregate of 255 individuals; 0/255 membrane-like individually; rim level 0.92)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1710, R_eq 4.55): none; #3 (t=1710, R_eq 4.37): none; #4 (t=1710, R_eq 4.07): none; #5 (t=1710, R_eq 4.51): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
