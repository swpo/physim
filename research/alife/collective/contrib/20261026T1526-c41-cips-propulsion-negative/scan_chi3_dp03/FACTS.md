# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 577s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_chi3_dp03 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0103, 0.9913], min area 6 px

## Measurements
- components: final 31, mean 29.9, max 31; occupancy final 0.10
- tracks: 31; persistent (alive >= 50% of run): 31; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00287/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 31
- channel total drift (end/start - 1): [0.0, -0.4866, 0.5267]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.32, rim-vs-outside 0.78, heterogeneity 0.12; core [0.993, 0.953, 0.053] rim [0.823, 0.725, 0.201]
  - track 1 at frame 51: holes 0, rim-vs-core 0.29, rim-vs-outside 0.81, heterogeneity 0.13; core [0.992, 0.944, 0.04] rim [0.832, 0.744, 0.182]
  - track 2 at frame 51: holes 0, rim-vs-core 0.37, rim-vs-outside 0.52, heterogeneity 0.11; core [0.986, 0.942, 0.103] rim [0.779, 0.677, 0.251]
  - track 3 at frame 51: holes 0, rim-vs-core 0.39, rim-vs-outside 0.52, heterogeneity 0.12; core [0.983, 0.932, 0.11] rim [0.754, 0.653, 0.255]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 22.5 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.746)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 12.5 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.734)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 18, rim/outside 0.647 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 6.02): none; #1 (t=5100, R_eq 6.38): none; #2 (t=5100, R_eq 5.2): none; #3 (t=5100, R_eq 5.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
