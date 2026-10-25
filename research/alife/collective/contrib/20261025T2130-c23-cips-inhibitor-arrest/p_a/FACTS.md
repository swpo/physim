# Evidence pack: cips-inhib (seed 0)

- world: `../world_inh.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 83s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/p_a --seeds 0 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0005, 0.9934], min area 6 px

## Measurements
- components: final 43, mean 40.3, max 58; occupancy final 0.13
- tracks: 74; persistent (alive >= 50% of run): 42; longest 264 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 43], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 14, merge/split ratio n/a, nucleations 60
- channel total drift (end/start - 1): [0.0, -0.4328, 0.2981, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 169: holes 0, rim-vs-core 0.35, rim-vs-outside 0.44, heterogeneity 0.10; core [0.956, 0.901, 0.086, 0.892] rim [0.746, 0.729, 0.238, 0.739]
  - track 3 at frame 169: holes 0, rim-vs-core 0.28, rim-vs-outside 0.44, heterogeneity 0.08; core [0.956, 0.849, 0.181, 0.809] rim [0.771, 0.706, 0.29, 0.693]
  - track 5 at frame 171: holes 0, rim-vs-core 0.30, rim-vs-outside 0.45, heterogeneity 0.08; core [0.958, 0.857, 0.137, 0.836] rim [0.762, 0.709, 0.25, 0.715]
  - track 6 at frame 171: holes 0, rim-vs-core 0.34, rim-vs-outside 0.46, heterogeneity 0.10; core [0.963, 0.885, 0.136, 0.853] rim [0.751, 0.712, 0.275, 0.708]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 275 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 26.6 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.906)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 3.79 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.816)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.49, rim/outside 0.666 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.438)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 2.71 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.808)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1690, R_eq 4.37): none; #3 (t=1690, R_eq 3.24): none; #5 (t=1710, R_eq 3.39): none; #6 (t=1710, R_eq 3.78): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
