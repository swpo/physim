# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 581s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_chi45 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0065, 0.9933], min area 6 px

## Measurements
- components: final 30, mean 29.3, max 30; occupancy final 0.11
- tracks: 32; persistent (alive >= 50% of run): 30; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.36 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0018/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 31
- channel total drift (end/start - 1): [-0.0, -0.4716, 0.5106]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.34, rim-vs-outside 0.72, heterogeneity 0.12; core [0.996, 0.939, 0.057] rim [0.834, 0.701, 0.229]
  - track 1 at frame 51: holes 0, rim-vs-core 0.34, rim-vs-outside 0.73, heterogeneity 0.12; core [0.994, 0.935, 0.04] rim [0.826, 0.696, 0.215]
  - track 2 at frame 51: holes 0, rim-vs-core 0.21, rim-vs-outside 0.61, heterogeneity 0.12; core [0.98, 0.884, 0.126] rim [0.842, 0.752, 0.208]
  - track 3 at frame 51: holes 0, rim-vs-core 0.33, rim-vs-outside 0.72, heterogeneity 0.12; core [0.996, 0.94, 0.063] rim [0.84, 0.705, 0.23]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 180 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 77.2 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.985)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 11.6 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.878)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.2, rim/outside 0.675 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.476)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 6.43): none; #1 (t=5100, R_eq 6.86): none; #2 (t=5100, R_eq 5.94): none; #3 (t=5100, R_eq 6.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
