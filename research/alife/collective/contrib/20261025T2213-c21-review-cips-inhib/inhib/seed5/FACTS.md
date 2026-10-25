# Evidence pack: cips-inhib (seed 5)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 63s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2213-c21-review-cips-inhib/inhib --seeds 4 5 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0019, 0.9847], min area 6 px

## Measurements
- components: final 37, mean 30.0, max 43; occupancy final 0.13
- tracks: 51; persistent (alive >= 50% of run): 40; longest 235 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 37, 37], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio n/a, nucleations 44
- channel total drift (end/start - 1): [0.0, -0.5664, 0.39, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 184: holes 0, rim-vs-core 0.37, rim-vs-outside 0.40, heterogeneity 0.10; core [0.958, 0.919, 0.129, 0.943] rim [0.72, 0.719, 0.29, 0.827]
  - track 1 at frame 184: holes 0, rim-vs-core 0.38, rim-vs-outside 0.39, heterogeneity 0.10; core [0.95, 0.9, 0.165, 0.914] rim [0.691, 0.697, 0.32, 0.802]
  - track 2 at frame 184: holes 0, rim-vs-core 0.36, rim-vs-outside 0.39, heterogeneity 0.10; core [0.945, 0.893, 0.162, 0.916] rim [0.7, 0.704, 0.304, 0.814]
  - track 3 at frame 184: holes 0, rim-vs-core 0.21, rim-vs-outside 0.54, heterogeneity 0.10; core [0.956, 0.914, 0.145, 0.922] rim [0.817, 0.803, 0.232, 0.86]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 198 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 26.9 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.901)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 4.24 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.83)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.04, rim/outside 0.692 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.49)
  - radial I: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 1.66 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.888)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1840, R_eq 4.51): none; #1 (t=1840, R_eq 4.3): none; #2 (t=1840, R_eq 4.18): none; #3 (t=1840, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
