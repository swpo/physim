# Evidence pack: cips-inhib (seed 4)

- world: `../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 154s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2213-c21-review-cips-inhib/noI_T6000 --seeds 4 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0001, 0.9995], min area 6 px

## Measurements
- components: final 34, mean 46.2, max 80; occupancy final 0.14
- tracks: 125; persistent (alive >= 50% of run): 45; longest 583 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 34], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00761/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 39, merge/split ratio n/a, nucleations 86
- channel total drift (end/start - 1): [-0.0, -0.2615, 0.1799, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 313: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.07; core [0.978, 0.832, 0.205, 0.0] rim [0.79, 0.674, 0.318, 0.0]
  - track 3 at frame 313: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.06; core [0.977, 0.824, 0.206, 0.0] rim [0.807, 0.679, 0.308, 0.0]
  - track 18 at frame 313: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.08; core [0.976, 0.852, 0.194, 0.0] rim [0.759, 0.677, 0.324, 0.0]
  - track 31 at frame 313: holes 0, rim-vs-core 0.24, rim-vs-outside 0.48, heterogeneity 0.06; core [0.977, 0.813, 0.235, 0.0] rim [0.808, 0.673, 0.332, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 271 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 51.8 (aggregate of 271 individuals; 0/271 membrane-like individually; rim level 0.95)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 4.22 (aggregate of 271 individuals; 0/271 membrane-like individually; rim level 0.813)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.82, rim/outside 0.694 (aggregate of 271 individuals; 0/271 membrane-like individually; rim level 0.47)
  - radial I: flat profile (no radial structure; level 0; aggregate of 271 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3130, R_eq 3.34): none; #3 (t=3130, R_eq 3.19): none; #18 (t=3130, R_eq 3.66): none; #31 (t=3130, R_eq 3.04): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
