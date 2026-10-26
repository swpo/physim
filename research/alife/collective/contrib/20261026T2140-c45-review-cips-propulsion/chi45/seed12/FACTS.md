# Evidence pack: cips-turnover-divide (seed 12)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1526-c41-cips-propulsion-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 470s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c41-cips-propulsion-negative/world.py --out /tmp/claude-0/cp/chi45/seed12 --seeds 12 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0068, 0.9929], min area 6 px

## Measurements
- components: final 29, mean 28.3, max 29; occupancy final 0.11
- tracks: 31; persistent (alive >= 50% of run): 29; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 29], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00258/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 30
- channel total drift (end/start - 1): [0.0, -0.4754, 0.5146]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.22, rim-vs-outside 0.83, heterogeneity 0.12; core [0.996, 0.94, 0.078] rim [0.887, 0.783, 0.187]
  - track 1 at frame 51: holes 0, rim-vs-core 0.32, rim-vs-outside 0.71, heterogeneity 0.11; core [0.997, 0.944, 0.066] rim [0.851, 0.716, 0.228]
  - track 2 at frame 51: holes 0, rim-vs-core 0.32, rim-vs-outside 0.73, heterogeneity 0.12; core [0.996, 0.941, 0.081] rim [0.837, 0.706, 0.239]
  - track 3 at frame 51: holes 0, rim-vs-core 0.29, rim-vs-outside 0.78, heterogeneity 0.12; core [0.997, 0.951, 0.059] rim [0.862, 0.74, 0.213]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 174 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.991, rim/outside 78.2 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.99)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 12.1 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.885)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 25.2, rim/outside 0.675 (aggregate of 174 individuals; 0/174 membrane-like individually; rim level 0.479)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 6.15): none; #1 (t=5100, R_eq 6.21): none; #2 (t=5100, R_eq 6.02): none; #3 (t=5100, R_eq 6.38): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
