# Evidence pack: cips-predator-prey (seed 3)

- world: `../../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 61 frames x 1000 steps x dt 0.1 = time 6000; grid [128, 128]; wall 264s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/g4_seed3 --seeds 3 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0349, 0.9614], min area 6 px

## Measurements
- components: final 0, mean 1.8, max 4; occupancy final 0.00
- tracks: 4; persistent (alive >= 50% of run): 0; longest 30 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [1, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 4
- channel total drift (end/start - 1): [-0.0693, -0.7889, 0.8499, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 17: holes 0, rim-vs-core 0.24, rim-vs-outside 0.76, heterogeneity 0.06; core [0.997, 0.996, 0.0, 0.0, 0.0] rim [0.83, 0.827, 0.024, 0.0, 0.0]
  - track 1 at frame 18: holes 0, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.05; core [1.0, 0.999, 0.0, 0.0, 0.0] rim [0.87, 0.853, 0.009, 0.0, 0.0]
  - track 2 at frame 18: holes 0, rim-vs-core 0.27, rim-vs-outside 0.77, heterogeneity 0.06; core [1.0, 0.999, 0.0, 0.0, 0.0] rim [0.817, 0.799, 0.013, 0.0, 0.0]
  - track 3 at frame 18: holes 0, rim-vs-core 0.37, rim-vs-outside 0.47, heterogeneity 0.06; core [0.979, 0.971, 0.0, 0.0, 0.0] rim [0.71, 0.725, 0.038, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [10, 20, 30]):
  - radial e prey: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 25.4 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.819)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 12.9 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.856)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 34.2, rim/outside 0.491 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.336)
  - radial q predator: flat profile (no radial structure; level 0; aggregate of 12 individuals)
  - radial r: flat profile (no radial structure; level 0; aggregate of 12 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1700, R_eq 6.15): none; #1 (t=1800, R_eq 6.18): none; #2 (t=1800, R_eq 6.23): none; #3 (t=1800, R_eq 5.86): none
- species `prey` (channels ['e prey'], own threshold): components final 0, mean 1.8, max 4; tracks 4, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['q predator'], own threshold): components final 1, mean 0.5, max 1; tracks 1, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
