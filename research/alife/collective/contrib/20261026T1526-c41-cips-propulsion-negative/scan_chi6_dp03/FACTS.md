# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 598s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_chi6_dp03 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0006, 1.0026], min area 6 px

## Measurements
- components: final 118, mean 117.5, max 124; occupancy final 0.10
- tracks: 130; persistent (alive >= 50% of run): 118; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [118, 118, 118], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 128
- channel total drift (end/start - 1): [-0.0, -0.3459, 0.3762]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.24, rim-vs-outside 0.75, heterogeneity 0.10; core [0.993, 0.92, 0.104] rim [0.879, 0.73, 0.188]
  - track 1 at frame 51: holes 0, rim-vs-core 0.34, rim-vs-outside 0.64, heterogeneity 0.11; core [0.99, 0.898, 0.127] rim [0.798, 0.644, 0.236]
  - track 3 at frame 51: holes 0, rim-vs-core 0.26, rim-vs-outside 0.59, heterogeneity 0.07; core [0.996, 0.933, 0.053] rim [0.913, 0.719, 0.167]
  - track 4 at frame 51: holes 0, rim-vs-core 0.23, rim-vs-outside 0.62, heterogeneity 0.07; core [0.994, 0.88, 0.171] rim [0.894, 0.684, 0.246]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 705 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 76.2 (aggregate of 705 individuals; 0/705 membrane-like individually; rim level 0.985)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 8.82 (aggregate of 705 individuals; 0/705 membrane-like individually; rim level 0.849)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.39, rim/outside 0.696 (aggregate of 705 individuals; 0/705 membrane-like individually; rim level 0.355)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 3.43): none; #1 (t=5100, R_eq 3.29): none; #3 (t=5100, R_eq 3.43): none; #4 (t=5100, R_eq 2.59): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
