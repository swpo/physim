# Evidence pack: swarmalator (seed 5)

- world: `../../20261025T2012-c21-swarmalator-motility-turnover-tradeoff/world.py`, family `swarmalator`
- parent: new class (O'Keeffe-Ha-Strogatz swarmalators, local coupling, phase = heading); mutation: none
- run: 201 frames x 40 steps x dt 0.05 = time 400; grid [128, 128]; wall 58s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2012-c21-swarmalator-motility-turnover-tradeoff/world.py --out collective/contrib/20261025T2039-c25-review-swarm-tradeoff/rerun_sw06 --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 3.755], min area 6 px

## Measurements
- components: final 7, mean 6.9, max 11; occupancy final 0.01
- tracks: 85; persistent (alive >= 50% of run): 4; longest 186 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 14, 3], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.118/time; max body lengths 5.8
- replication (lineage window K = 20 frames = time 40, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 85
- channel total drift (end/start - 1): [0.0, 3.3582, -0.4372]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 108: holes 0, rim-vs-core 0.11, rim-vs-outside 0.54, heterogeneity 0.13; core [1.0, 0.236, 1.0] rim [0.917, 0.312, 1.0]
  - track 3 at frame 111: holes 0, rim-vs-core 0.24, rim-vs-outside 0.63, heterogeneity 0.14; core [1.0, 0.119, 1.0] rim [0.803, 0.251, 0.999]
  - track 5 at frame 114: holes 0, rim-vs-core 0.22, rim-vs-outside 0.70, heterogeneity 0.11; core [1.0, 1.0, 0.995] rim [0.916, 0.996, 0.787]
  - track 9 at frame 121: holes 0, rim-vs-core 0.17, rim-vs-outside 0.54, heterogeneity 0.08; core [1.0, 1.0, 0.0] rim [0.945, 0.834, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 23 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particle density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 17.1 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.976)
  - radial density x cos(phase): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 1.4 (aggregate of 23 individuals; 1/23 membrane-like individually; rim level 0.556)
  - radial density x sin(phase): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 1.16 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.434)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=216, R_eq 2.46): none; #3 (t=222, R_eq 3.19): none; #5 (t=228, R_eq 2.93): none; #9 (t=242, R_eq 2.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
