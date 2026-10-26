# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 547s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_chi45_d0045 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0088, 0.9915], min area 6 px

## Measurements
- components: final 33, mean 32.2, max 33; occupancy final 0.10
- tracks: 35; persistent (alive >= 50% of run): 33; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 33], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00176/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 34
- channel total drift (end/start - 1): [0.0, -0.469, 0.5079]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.39, rim-vs-outside 0.45, heterogeneity 0.12; core [0.98, 0.888, 0.107] rim [0.74, 0.633, 0.275]
  - track 1 at frame 51: holes 0, rim-vs-core 0.36, rim-vs-outside 0.73, heterogeneity 0.13; core [0.995, 0.934, 0.048] rim [0.81, 0.686, 0.226]
  - track 2 at frame 51: holes 0, rim-vs-core 0.23, rim-vs-outside 0.60, heterogeneity 0.12; core [0.976, 0.875, 0.116] rim [0.821, 0.73, 0.211]
  - track 3 at frame 51: holes 0, rim-vs-core 0.33, rim-vs-outside 0.73, heterogeneity 0.12; core [0.995, 0.94, 0.043] rim [0.837, 0.703, 0.214]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 198 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 76.5 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.988)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 10.8 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.873)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 26.5, rim/outside 0.673 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.473)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 5.75): none; #1 (t=5100, R_eq 6.26): none; #2 (t=5100, R_eq 5.75): none; #3 (t=5100, R_eq 6.21): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
