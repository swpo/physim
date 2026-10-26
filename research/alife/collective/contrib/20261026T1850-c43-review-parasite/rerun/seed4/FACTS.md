# Evidence pack: cips-turnover-divide (seed 4)

- world: `../../world_base.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 865s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1850-c43-review-parasite/world_base.py --out collective/contrib/20261026T1850-c43-review-parasite/rerun/seed4 --seeds 4 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0228, 0.9736], min area 6 px

## Measurements
- components: final 11, mean 6.2, max 11; occupancy final 0.07
- tracks: 19; persistent (alive >= 50% of run): 1; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.16 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.0, -0.6416, 0.6924]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 67: holes 0, rim-vs-core 0.39, rim-vs-outside 0.63, heterogeneity 0.13; core [0.988, 0.961, 0.04] rim [0.761, 0.705, 0.231]
  - track 7 at frame 63: holes 0, rim-vs-core 0.36, rim-vs-outside 0.60, heterogeneity 0.12; core [0.981, 0.942, 0.038] rim [0.764, 0.706, 0.211]
  - track 3 at frame 53: holes 0, rim-vs-core 0.38, rim-vs-outside 0.59, heterogeneity 0.13; core [0.979, 0.937, 0.032] rim [0.748, 0.695, 0.214]
  - track 9 at frame 84: holes 0, rim-vs-core 0.37, rim-vs-outside 0.61, heterogeneity 0.12; core [0.983, 0.949, 0.031] rim [0.764, 0.705, 0.211]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 41 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 26.2 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.835)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 11.6 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.822)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.3, rim/outside 0.636 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.482)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=6700, R_eq 8.02): none; #7 (t=6300, R_eq 8.67): none; #3 (t=5300, R_eq 8.94): none; #9 (t=8400, R_eq 8.54): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
