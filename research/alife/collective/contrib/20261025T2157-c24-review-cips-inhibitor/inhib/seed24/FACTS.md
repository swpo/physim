# Evidence pack: cips-inhib (seed 24)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 101s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2157-c24-review-cips-inhibitor/inhib/seed24 --seeds 24 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0018, 0.9844], min area 6 px

## Measurements
- components: final 34, mean 28.7, max 43; occupancy final 0.13
- tracks: 52; persistent (alive >= 50% of run): 34; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 34], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio n/a, nucleations 44
- channel total drift (end/start - 1): [0.0, -0.5729, 0.3947, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 184: holes 0, rim-vs-core 0.35, rim-vs-outside 0.40, heterogeneity 0.09; core [0.941, 0.866, 0.216, 0.87] rim [0.691, 0.682, 0.35, 0.775]
  - track 1 at frame 184: holes 0, rim-vs-core 0.34, rim-vs-outside 0.40, heterogeneity 0.09; core [0.946, 0.877, 0.21, 0.871] rim [0.709, 0.695, 0.345, 0.776]
  - track 2 at frame 184: holes 0, rim-vs-core 0.37, rim-vs-outside 0.41, heterogeneity 0.10; core [0.958, 0.912, 0.157, 0.912] rim [0.719, 0.713, 0.313, 0.8]
  - track 3 at frame 184: holes 0, rim-vs-core 0.36, rim-vs-outside 0.41, heterogeneity 0.10; core [0.955, 0.907, 0.174, 0.895] rim [0.714, 0.71, 0.325, 0.786]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 189 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 23.8 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.893)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 4.16 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.825)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.04, rim/outside 0.694 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.495)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 1.68 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.877)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1840, R_eq 3.95): none; #1 (t=1840, R_eq 3.95): none; #2 (t=1840, R_eq 4.41): none; #3 (t=1840, R_eq 4.3): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
