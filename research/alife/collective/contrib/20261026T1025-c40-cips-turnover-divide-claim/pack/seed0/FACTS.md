# Evidence pack: cips-turnover-divide (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 986s; status ok
- command: `python -m labkit.run world.py --out pack --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0215, 0.976], min area 6 px

## Measurements
- components: final 17, mean 12.3, max 17; occupancy final 0.09
- tracks: 28; persistent (alive >= 50% of run): 10; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.36 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00333/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0, -0.5886, 0.6357]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.61, heterogeneity 0.12; core [0.982, 0.935, 0.042] rim [0.801, 0.718, 0.218]
  - track 8 at frame 119: holes 0, rim-vs-core 0.24, rim-vs-outside 0.67, heterogeneity 0.11; core [0.972, 0.909, 0.051] rim [0.83, 0.764, 0.172]
  - track 9 at frame 119: holes 0, rim-vs-core 0.35, rim-vs-outside 0.59, heterogeneity 0.12; core [0.974, 0.916, 0.055] rim [0.758, 0.694, 0.227]
  - track 26 at frame 183: holes 0, rim-vs-core 0.36, rim-vs-outside 0.64, heterogeneity 0.12; core [0.991, 0.961, 0.08] rim [0.79, 0.717, 0.258]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 34.4 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.877)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 12.4 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.84)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.2, rim/outside 0.654 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.498)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 8.37): none; #8 (t=11900, R_eq 8.9): none; #9 (t=11900, R_eq 8.87): none; #26 (t=18300, R_eq 7.02): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
