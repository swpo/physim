# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 586s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_chi6 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0033, 0.9974], min area 6 px

## Measurements
- components: final 40, mean 39.5, max 42; occupancy final 0.11
- tracks: 48; persistent (alive >= 50% of run): 40; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00194/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 44
- channel total drift (end/start - 1): [-0.0, -0.4176, 0.4529]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.32, rim-vs-outside 0.78, heterogeneity 0.12; core [0.997, 0.939, 0.03] rim [0.849, 0.703, 0.194]
  - track 1 at frame 51: holes 0, rim-vs-core 0.33, rim-vs-outside 0.76, heterogeneity 0.12; core [0.997, 0.938, 0.029] rim [0.843, 0.698, 0.196]
  - track 2 at frame 51: holes 0, rim-vs-core 0.39, rim-vs-outside 0.52, heterogeneity 0.12; core [0.985, 0.881, 0.109] rim [0.737, 0.625, 0.267]
  - track 5 at frame 51: holes 0, rim-vs-core 0.38, rim-vs-outside 0.50, heterogeneity 0.12; core [0.986, 0.881, 0.095] rim [0.747, 0.627, 0.256]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 86 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.993)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 9.34 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.87)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16, rim/outside 0.68 (aggregate of 240 individuals; 0/240 membrane-like individually; rim level 0.447)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 6.26): none; #1 (t=5100, R_eq 6.38): none; #2 (t=5100, R_eq 5.47): none; #5 (t=5100, R_eq 5.59): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
