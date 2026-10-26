# Evidence pack: cips-turnover-divide (seed 4)

- world: `../../../../20261026T1025-c40-cips-turnover-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [192, 192]; wall 795s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1025-c40-cips-turnover-divide-claim/world.py --out collective/contrib/wip-c37/c40/rerun/seed4 --seeds 4 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0238, 0.9728], min area 6 px

## Measurements
- components: final 10, mean 5.1, max 10; occupancy final 0.05
- tracks: 17; persistent (alive >= 50% of run): 3; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 10], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.0, -0.6633, 0.7156]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 57: holes 0, rim-vs-core 0.36, rim-vs-outside 0.64, heterogeneity 0.12; core [0.991, 0.969, 0.028] rim [0.789, 0.731, 0.207]
  - track 3 at frame 53: holes 0, rim-vs-core 0.38, rim-vs-outside 0.60, heterogeneity 0.13; core [0.98, 0.946, 0.027] rim [0.75, 0.701, 0.206]
  - track 7 at frame 60: holes 0, rim-vs-core 0.36, rim-vs-outside 0.61, heterogeneity 0.12; core [0.985, 0.954, 0.029] rim [0.772, 0.715, 0.204]
  - track 2 at frame 21: holes 0, rim-vs-core 0.34, rim-vs-outside 0.60, heterogeneity 0.11; core [0.975, 0.927, 0.012] rim [0.778, 0.704, 0.173]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 26.7 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.849)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 11.9 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.838)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 24.9, rim/outside 0.632 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.478)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=5700, R_eq 7.98): none; #3 (t=5300, R_eq 8.94): none; #7 (t=6000, R_eq 8.52): none; #2 (t=2100, R_eq 9.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
