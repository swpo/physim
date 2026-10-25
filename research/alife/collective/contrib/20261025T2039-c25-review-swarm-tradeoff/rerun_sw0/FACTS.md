# Evidence pack: swarmalator (seed 5)

- world: `../../20261025T2012-c21-swarmalator-motility-turnover-tradeoff/world.py`, family `swarmalator`
- parent: new class (O'Keeffe-Ha-Strogatz swarmalators, local coupling, phase = heading); mutation: none
- run: 201 frames x 40 steps x dt 0.05 = time 400; grid [128, 128]; wall 275s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2012-c21-swarmalator-motility-turnover-tradeoff/world.py --out collective/contrib/20261025T2039-c25-review-swarm-tradeoff/rerun_sw0 --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 12.5091], min area 6 px

## Measurements
- components: final 4, mean 3.9, max 6; occupancy final 0.01
- tracks: 22; persistent (alive >= 50% of run): 3; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 2], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 1.06/time; max body lengths 93.7
- replication (lineage window K = 20 frames = time 40, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio n/a, nucleations 19
- channel total drift (end/start - 1): [0.0, 26.2567, 30.2671]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 123: holes 0, rim-vs-core 0.00, rim-vs-outside 0.26, heterogeneity 0.00; core [1.0, 1.0, 1.0] rim [1.0, 1.0, 1.0]
  - track 17 at frame 131: holes 0, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.07; core [1.0, 1.0, 1.0] rim [0.988, 0.825, 1.0]
  - track 20 at frame 136: holes 0, rim-vs-core 0.00, rim-vs-outside 0.37, heterogeneity 0.00; core [1.0, 1.0, 0.0] rim [1.0, 1.0, 0.0]
  - track 4 at frame 76: holes 0, rim-vs-core 0.10, rim-vs-outside 0.56, heterogeneity 0.03; core [1.0, 1.0, 1.0] rim [1.0, 0.905, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial particle density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 25.4 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 1)
  - radial density x cos(phase): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 10.3 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.882)
  - radial density x sin(phase): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 7.62 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.699)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=246, R_eq 1.95): none; #17 (t=262, R_eq 2.93): none; #20 (t=272, R_eq 2.26): none; #4 (t=152, R_eq 2.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
