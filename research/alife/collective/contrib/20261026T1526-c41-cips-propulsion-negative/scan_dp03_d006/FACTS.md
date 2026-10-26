# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 557s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_dp03_d006 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0144, 0.9884], min area 6 px

## Measurements
- components: final 32, mean 30.0, max 32; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 32; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 32, 32], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00247/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 32
- channel total drift (end/start - 1): [0.0, -0.5102, 0.5519]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.28, rim-vs-outside 0.61, heterogeneity 0.11; core [0.982, 0.932, 0.069] rim [0.828, 0.737, 0.2]
  - track 1 at frame 51: holes 0, rim-vs-core 0.36, rim-vs-outside 0.50, heterogeneity 0.11; core [0.98, 0.92, 0.077] rim [0.764, 0.667, 0.226]
  - track 2 at frame 51: holes 0, rim-vs-core 0.38, rim-vs-outside 0.49, heterogeneity 0.12; core [0.975, 0.911, 0.075] rim [0.734, 0.654, 0.225]
  - track 3 at frame 51: holes 0, rim-vs-core 0.35, rim-vs-outside 0.51, heterogeneity 0.12; core [0.981, 0.918, 0.078] rim [0.77, 0.675, 0.22]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 192 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.711, rim/outside 21.7 (aggregate of 192 individuals; 0/192 membrane-like individually; rim level 0.698)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 11.8 (aggregate of 192 individuals; 0/192 membrane-like individually; rim level 0.716)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 24.7, rim/outside 0.623 (aggregate of 192 individuals; 0/192 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 5.44): none; #1 (t=5100, R_eq 5.67): none; #2 (t=5100, R_eq 5.89): none; #3 (t=5100, R_eq 5.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
