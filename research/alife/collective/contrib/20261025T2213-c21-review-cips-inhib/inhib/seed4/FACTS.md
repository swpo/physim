# Evidence pack: cips-inhib (seed 4)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 77s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2213-c21-review-cips-inhib/inhib --seeds 4 5 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.51 of robust range [0.0017, 0.986], min area 6 px

## Measurements
- components: final 37, mean 28.8, max 43; occupancy final 0.13
- tracks: 51; persistent (alive >= 50% of run): 37; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio n/a, nucleations 45
- channel total drift (end/start - 1): [-0.0, -0.5694, 0.3921, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 184: holes 0, rim-vs-core 0.29, rim-vs-outside 0.45, heterogeneity 0.09; core [0.956, 0.901, 0.177, 0.886] rim [0.763, 0.739, 0.295, 0.797]
  - track 1 at frame 184: holes 0, rim-vs-core 0.37, rim-vs-outside 0.40, heterogeneity 0.10; core [0.951, 0.897, 0.157, 0.909] rim [0.698, 0.698, 0.304, 0.798]
  - track 2 at frame 184: holes 0, rim-vs-core 0.34, rim-vs-outside 0.40, heterogeneity 0.09; core [0.947, 0.879, 0.19, 0.882] rim [0.712, 0.699, 0.319, 0.786]
  - track 3 at frame 184: holes 0, rim-vs-core 0.38, rim-vs-outside 0.40, heterogeneity 0.10; core [0.95, 0.904, 0.132, 0.93] rim [0.693, 0.703, 0.285, 0.815]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 193 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 21.6 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.893)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 3.9 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.82)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.92, rim/outside 0.699 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.472)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 1.65 (aggregate of 193 individuals; 0/193 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1840, R_eq 4.11): none; #1 (t=1840, R_eq 4.37): none; #2 (t=1840, R_eq 4.03): none; #3 (t=1840, R_eq 4.58): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
