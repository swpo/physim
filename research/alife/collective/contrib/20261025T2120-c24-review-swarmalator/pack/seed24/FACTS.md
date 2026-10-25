# Evidence pack: swarmalator (seed 24)

- world: `../../../20261025T2012-c21-swarmalator-motility-turnover-tradeoff/world.py`, family `swarmalator`
- parent: new class (O'Keeffe-Ha-Strogatz swarmalators, local coupling, phase = heading); mutation: none
- run: 201 frames x 40 steps x dt 0.05 = time 400; grid [128, 128]; wall 163s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2012-c21-swarmalator-motility-turnover-tradeoff/world.py --out collective/contrib/20261025T2120-c24-review-swarmalator/pack/seed24 --seeds 24 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 6.7246], min area 6 px

## Measurements
- components: final 5, mean 3.3, max 6; occupancy final 0.01
- tracks: 15; persistent (alive >= 50% of run): 4; longest 152 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 3, 2], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.778/time; max body lengths 15.5
- replication (lineage window K = 20 frames = time 40, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 14
- channel total drift (end/start - 1): [0.0, 53.5304, 25.6318]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 131: holes 0, rim-vs-core 0.05, rim-vs-outside 0.54, heterogeneity 0.15; core [1.0, 0.37, 1.0] rim [0.972, 0.408, 1.0]
  - track 13 at frame 134: holes 0, rim-vs-core 0.11, rim-vs-outside 0.60, heterogeneity 0.07; core [1.0, 0.0, 0.003] rim [0.931, 0.0, 0.088]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particle density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 11.4 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.988)
  - radial density x cos(phase): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 1.3 (aggregate of 15 individuals; 1/15 membrane-like individually; rim level 0.472)
  - radial density x sin(phase): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 1.6 (aggregate of 15 individuals; 2/15 membrane-like individually; rim level 0.545)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=248, R_eq 1.87): none; #10 (t=258, R_eq 1.6): none; #12 (t=262, R_eq 2.93): ['density x cos(phase)']; #13 (t=268, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
