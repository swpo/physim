# Evidence pack: cips-predator-prey (seed 3)

- world: `../../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 61 frames x 1000 steps x dt 0.1 = time 6000; grid [128, 128]; wall 289s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/a_seed3 --seeds 3 --frames 60 --no-movie`
- segmentation: matter > 0.48 of robust range [0.0491, 0.9851], min area 6 px

## Measurements
- components: final 4, mean 3.7, max 4; occupancy final 0.03
- tracks: 4; persistent (alive >= 50% of run): 4; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.46 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 4, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 4
- channel total drift (end/start - 1): [-0.0366, -0.7186, 0.7747, -0.0845, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 31: holes 0, rim-vs-core 0.49, rim-vs-outside 0.50, heterogeneity 0.11; core [0.962, 0.933, 0.029, 0.355, 0.897] rim [0.696, 0.694, 0.177, 0.352, 0.599]
  - track 1 at frame 33: holes 0, rim-vs-core 0.37, rim-vs-outside 0.65, heterogeneity 0.11; core [0.974, 0.948, 0.015, 0.356, 0.94] rim [0.785, 0.757, 0.13, 0.353, 0.705]
  - track 2 at frame 33: holes 0, rim-vs-core 0.53, rim-vs-outside 0.49, heterogeneity 0.11; core [0.961, 0.935, 0.028, 0.355, 0.904] rim [0.676, 0.677, 0.199, 0.351, 0.58]
  - track 3 at frame 35: holes 0, rim-vs-core 0.56, rim-vs-outside 0.49, heterogeneity 0.11; core [0.968, 0.938, 0.018, 0.356, 0.931] rim [0.674, 0.66, 0.189, 0.351, 0.59]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial e prey: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 16.2 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.718)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 9.32 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.757)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 24.6, rim/outside 0.597 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.45)
  - radial q predator: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 1.02 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.353)
  - radial r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 10.2 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.733)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3100, R_eq 5.97): none; #1 (t=3300, R_eq 5.78): none; #2 (t=3300, R_eq 5.81): none; #3 (t=3500, R_eq 5.89): none
- species `prey` (channels ['e prey'], own threshold): components final 4, mean 3.7, max 4; tracks 4, persistent 4; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['q predator'], own threshold): components final 0, mean 0.1, max 1; tracks 1, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
