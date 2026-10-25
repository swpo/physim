# Evidence pack: cips-inhib (seed 0)

- world: `../world_inh.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 60s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/p_e --seeds 0 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.53 of robust range [0.015, 0.9355], min area 6 px

## Measurements
- components: final 29, mean 8.8, max 29; occupancy final 0.12
- tracks: 29; persistent (alive >= 50% of run): 0; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 29], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 29
- channel total drift (end/start - 1): [0.0, -0.6769, 0.4662, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 242: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.09; core [0.958, 0.918, 0.082, 0.983] rim [0.725, 0.735, 0.235, 0.892]
  - track 1 at frame 242: holes 0, rim-vs-core 0.33, rim-vs-outside 0.32, heterogeneity 0.09; core [0.958, 0.918, 0.082, 0.983] rim [0.74, 0.743, 0.231, 0.897]
  - track 2 at frame 242: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.09; core [0.956, 0.92, 0.082, 0.979] rim [0.724, 0.736, 0.24, 0.885]
  - track 3 at frame 245: holes 0, rim-vs-core 0.36, rim-vs-outside 0.33, heterogeneity 0.10; core [0.952, 0.916, 0.089, 0.975] rim [0.707, 0.727, 0.249, 0.877]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 10.4 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.886)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 3.72 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.844)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.4, rim/outside 0.641 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.439)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 1.64 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.932)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=2420, R_eq 4.51): none; #1 (t=2420, R_eq 4.48): none; #2 (t=2420, R_eq 4.58): none; #3 (t=2450, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
