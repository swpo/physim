# Evidence pack: cips-turnover-divide (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 985s; status ok
- command: `python -m labkit.run world.py --out pack/seed1 --seeds 1 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0211, 0.9756], min area 6 px

## Measurements
- components: final 16, mean 13.1, max 16; occupancy final 0.09
- tracks: 25; persistent (alive >= 50% of run): 14; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.32 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.00363/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, -0.5907, 0.6379]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 103: holes 0, rim-vs-core 0.37, rim-vs-outside 0.63, heterogeneity 0.12; core [0.988, 0.949, 0.056] rim [0.779, 0.7, 0.241]
  - track 9 at frame 119: holes 0, rim-vs-core 0.38, rim-vs-outside 0.62, heterogeneity 0.13; core [0.988, 0.948, 0.06] rim [0.77, 0.696, 0.247]
  - track 10 at frame 119: holes 0, rim-vs-core 0.24, rim-vs-outside 0.69, heterogeneity 0.12; core [0.979, 0.921, 0.068] rim [0.83, 0.761, 0.168]
  - track 19 at frame 139: holes 0, rim-vs-core 0.37, rim-vs-outside 0.61, heterogeneity 0.12; core [0.981, 0.93, 0.048] rim [0.764, 0.691, 0.232]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 37.1 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.87)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 12.8 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.835)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 24.9, rim/outside 0.65 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.494)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=10300, R_eq 7.67): none; #9 (t=11900, R_eq 7.65): none; #10 (t=11900, R_eq 8.57): none; #19 (t=13900, R_eq 8.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
