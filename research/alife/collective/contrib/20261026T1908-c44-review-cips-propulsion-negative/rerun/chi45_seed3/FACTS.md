# Evidence pack: cips-turnover-divide (seed 3)

- world: `../../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 629s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/chi45_seed3 --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0066, 0.9932], min area 6 px

## Measurements
- components: final 30, mean 29.2, max 30; occupancy final 0.11
- tracks: 30; persistent (alive >= 50% of run): 30; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00199/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 30
- channel total drift (end/start - 1): [0.0, -0.4709, 0.5097]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.28, rim-vs-outside 0.78, heterogeneity 0.12; core [0.996, 0.949, 0.054] rim [0.866, 0.749, 0.202]
  - track 1 at frame 51: holes 0, rim-vs-core 0.34, rim-vs-outside 0.73, heterogeneity 0.12; core [0.995, 0.939, 0.047] rim [0.824, 0.698, 0.225]
  - track 2 at frame 51: holes 0, rim-vs-core 0.38, rim-vs-outside 0.45, heterogeneity 0.11; core [0.982, 0.892, 0.126] rim [0.752, 0.639, 0.286]
  - track 3 at frame 51: holes 0, rim-vs-core 0.34, rim-vs-outside 0.71, heterogeneity 0.12; core [0.995, 0.935, 0.05] rim [0.83, 0.695, 0.225]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 180 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 78 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.989)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 11.7 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.881)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.2, rim/outside 0.675 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.48)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 6.38): none; #1 (t=5100, R_eq 6.72): none; #2 (t=5100, R_eq 5.81): none; #3 (t=5100, R_eq 6.63): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
