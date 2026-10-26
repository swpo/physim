# Evidence pack: cips-turnover-divide (seed 12)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1526-c41-cips-propulsion-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 476s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c41-cips-propulsion-negative/world.py --out /tmp/claude-0/cp/chi6/seed12 --seeds 12 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0032, 0.9973], min area 6 px

## Measurements
- components: final 40, mean 39.4, max 40; occupancy final 0.11
- tracks: 42; persistent (alive >= 50% of run): 40; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00204/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 41
- channel total drift (end/start - 1): [0.0, -0.4179, 0.4531]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.35, rim-vs-outside 0.48, heterogeneity 0.11; core [0.989, 0.893, 0.084] rim [0.793, 0.651, 0.244]
  - track 1 at frame 51: holes 0, rim-vs-core 0.38, rim-vs-outside 0.51, heterogeneity 0.12; core [0.986, 0.883, 0.092] rim [0.753, 0.633, 0.252]
  - track 2 at frame 51: holes 0, rim-vs-core 0.33, rim-vs-outside 0.78, heterogeneity 0.12; core [0.997, 0.943, 0.031] rim [0.842, 0.704, 0.2]
  - track 3 at frame 51: holes 0, rim-vs-core 0.35, rim-vs-outside 0.50, heterogeneity 0.11; core [0.99, 0.894, 0.094] rim [0.795, 0.652, 0.251]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 85.5 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.993)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 9.41 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.87)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16.8, rim/outside 0.68 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.451)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 5.61): none; #1 (t=5100, R_eq 5.59): none; #2 (t=5100, R_eq 6.33): none; #3 (t=5100, R_eq 5.47): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
