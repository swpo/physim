# Evidence pack: cips-predator-prey (seed 5)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [128, 128]; wall 370s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1815-c43-review-cips-predator/world.py --out collective/contrib/20261026T1815-c43-review-cips-predator/rerun_late/seed5 --seeds 5 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0356, 0.9612], min area 6 px

## Measurements
- components: final 0, mean 1.3, max 4; occupancy final 0.00
- tracks: 4; persistent (alive >= 50% of run): 0; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 4
- channel total drift (end/start - 1): [-0.0693, -0.7889, 0.8499, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 17: holes 0, rim-vs-core 0.21, rim-vs-outside 0.52, heterogeneity 0.03; core [0.999, 0.999, 0.0, 0.0, 0.0] rim [0.841, 0.866, 0.003, 0.0, 0.0]
  - track 1 at frame 17: holes 0, rim-vs-core 0.25, rim-vs-outside 0.55, heterogeneity 0.04; core [1.0, 1.0, 0.0, 0.0, 0.0] rim [0.804, 0.851, 0.019, 0.0, 0.0]
  - track 2 at frame 18: holes 0, rim-vs-core 0.16, rim-vs-outside 0.83, heterogeneity 0.04; core [1.0, 1.0, 0.0, 0.0, 0.0] rim [0.88, 0.897, 0.001, 0.0, 0.0]
  - track 3 at frame 18: holes 0, rim-vs-core 0.24, rim-vs-outside 0.52, heterogeneity 0.04; core [0.999, 0.999, 0.0, 0.0, 0.0] rim [0.809, 0.848, 0.012, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [13, 27]):
  - radial e prey: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 61.7 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.941)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 16.7 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.963)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 30, rim/outside 0.443 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.29)
  - radial q predator: flat profile (no radial structure; level 0; aggregate of 8 individuals)
  - radial r: flat profile (no radial structure; level 0; aggregate of 8 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1700, R_eq 5.64): none; #1 (t=1700, R_eq 4.89): none; #2 (t=1800, R_eq 6.26): none; #3 (t=1800, R_eq 5.56): none
- species `prey` (channels ['e prey'], own threshold): components final 0, mean 1.3, max 4; tracks 4, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['q predator'], own threshold): components final 1, mean 0.6, max 1; tracks 1, persistent 1; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
