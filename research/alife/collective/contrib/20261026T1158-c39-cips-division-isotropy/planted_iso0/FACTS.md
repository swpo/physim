# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world_iso.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [192, 192]; wall 432s; status ok
- command: `python -m labkit.run collective/contrib/c39-cips-iso-wip/world_iso.py --out collective/contrib/c39-cips-iso-wip/planted_iso0 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0221, 0.9748], min area 6 px

## Measurements
- components: final 14, mean 10.0, max 14; occupancy final 0.08
- tracks: 21; persistent (alive >= 50% of run): 9; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 14], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00361/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0185, -0.6215, 0.6669]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 41: holes 0, rim-vs-core 0.38, rim-vs-outside 0.61, heterogeneity 0.13; core [0.981, 0.936, 0.046] rim [0.763, 0.694, 0.233]
  - track 7 at frame 54: holes 0, rim-vs-core 0.37, rim-vs-outside 0.62, heterogeneity 0.13; core [0.988, 0.953, 0.054] rim [0.777, 0.706, 0.24]
  - track 9 at frame 59: holes 0, rim-vs-core 0.38, rim-vs-outside 0.63, heterogeneity 0.13; core [0.989, 0.958, 0.062] rim [0.773, 0.706, 0.251]
  - track 10 at frame 59: holes 0, rim-vs-core 0.36, rim-vs-outside 0.61, heterogeneity 0.12; core [0.985, 0.946, 0.044] rim [0.785, 0.705, 0.229]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 36.4 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.902)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 13.6 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.858)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 25.4, rim/outside 0.653 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.499)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=4100, R_eq 8.48): none; #7 (t=5400, R_eq 7.9): none; #9 (t=5900, R_eq 7.63): none; #10 (t=5900, R_eq 8.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
