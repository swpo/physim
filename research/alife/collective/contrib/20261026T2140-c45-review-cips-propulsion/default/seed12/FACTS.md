# Evidence pack: cips-turnover-divide (seed 12)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1526-c41-cips-propulsion-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 462s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c41-cips-propulsion-negative/world.py --out /tmp/claude-0/cp/default/seed12 --seeds 12 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0211, 0.975], min area 6 px

## Measurements
- components: final 15, mean 10.6, max 15; occupancy final 0.08
- tracks: 23; persistent (alive >= 50% of run): 7; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.09 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00366/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, -0.598, 0.6458]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 51: holes 0, rim-vs-core 0.37, rim-vs-outside 0.61, heterogeneity 0.12; core [0.983, 0.943, 0.044] rim [0.774, 0.701, 0.232]
  - track 7 at frame 68: holes 0, rim-vs-core 0.35, rim-vs-outside 0.60, heterogeneity 0.12; core [0.974, 0.92, 0.061] rim [0.761, 0.703, 0.225]
  - track 8 at frame 68: holes 0, rim-vs-core 0.36, rim-vs-outside 0.60, heterogeneity 0.12; core [0.98, 0.935, 0.056] rim [0.772, 0.705, 0.233]
  - track 19 at frame 89: holes 0, rim-vs-core 0.36, rim-vs-outside 0.64, heterogeneity 0.12; core [0.991, 0.965, 0.073] rim [0.794, 0.725, 0.251]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 25.5 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.833)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 11.8 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.812)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16.5, rim/outside 0.651 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.497)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=5100, R_eq 8.43): none; #7 (t=6800, R_eq 9.01): none; #8 (t=6800, R_eq 8.29): none; #19 (t=8900, R_eq 7.16): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
