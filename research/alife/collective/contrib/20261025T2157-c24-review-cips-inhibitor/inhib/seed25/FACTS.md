# Evidence pack: cips-inhib (seed 25)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 101s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2157-c24-review-cips-inhibitor/inhib/seed25 --seeds 25 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.002, 0.9841], min area 6 px

## Measurements
- components: final 37, mean 30.0, max 45; occupancy final 0.13
- tracks: 53; persistent (alive >= 50% of run): 36; longest 239 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 36], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio n/a, nucleations 45
- channel total drift (end/start - 1): [0.0, -0.5678, 0.3912, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 182: holes 0, rim-vs-core 0.33, rim-vs-outside 0.40, heterogeneity 0.09; core [0.967, 0.931, 0.123, 0.94] rim [0.767, 0.748, 0.272, 0.834]
  - track 1 at frame 184: holes 0, rim-vs-core 0.34, rim-vs-outside 0.38, heterogeneity 0.09; core [0.94, 0.872, 0.173, 0.914] rim [0.699, 0.694, 0.303, 0.822]
  - track 2 at frame 184: holes 0, rim-vs-core 0.34, rim-vs-outside 0.39, heterogeneity 0.09; core [0.948, 0.892, 0.183, 0.892] rim [0.714, 0.709, 0.32, 0.795]
  - track 3 at frame 187: holes 0, rim-vs-core 0.37, rim-vs-outside 0.40, heterogeneity 0.10; core [0.944, 0.887, 0.161, 0.919] rim [0.686, 0.695, 0.304, 0.817]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 201 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 22.8 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.891)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 4.03 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.828)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.11, rim/outside 0.688 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.481)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 1.64 (aggregate of 201 individuals; 0/201 membrane-like individually; rim level 0.885)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1820, R_eq 4.3): none; #1 (t=1840, R_eq 3.95): none; #2 (t=1840, R_eq 3.99): none; #3 (t=1870, R_eq 4.18): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
