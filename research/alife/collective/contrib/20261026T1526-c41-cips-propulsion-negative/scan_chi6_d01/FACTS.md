# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 562s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_chi6_d01 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0089, 0.9938], min area 6 px

## Measurements
- components: final 51, mean 50.1, max 52; occupancy final 0.10
- tracks: 53; persistent (alive >= 50% of run): 51; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 51, 51], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0016/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 52
- channel total drift (end/start - 1): [0.0, -0.4097, 0.4444]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.39, rim-vs-outside 0.52, heterogeneity 0.12; core [0.985, 0.891, 0.065] rim [0.748, 0.637, 0.233]
  - track 1 at frame 51: holes 0, rim-vs-core 0.36, rim-vs-outside 0.51, heterogeneity 0.11; core [0.987, 0.896, 0.065] rim [0.783, 0.653, 0.226]
  - track 2 at frame 51: holes 0, rim-vs-core 0.36, rim-vs-outside 0.50, heterogeneity 0.11; core [0.986, 0.889, 0.074] rim [0.775, 0.647, 0.234]
  - track 5 at frame 51: holes 0, rim-vs-core 0.36, rim-vs-outside 0.52, heterogeneity 0.12; core [0.988, 0.89, 0.074] rim [0.777, 0.648, 0.233]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 306 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 80 (aggregate of 306 individuals; 0/306 membrane-like individually; rim level 0.991)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 8.02 (aggregate of 306 individuals; 0/306 membrane-like individually; rim level 0.857)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 27.1, rim/outside 0.668 (aggregate of 306 individuals; 0/306 membrane-like individually; rim level 0.428)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 5.14): none; #1 (t=5100, R_eq 4.98): none; #2 (t=5100, R_eq 4.85): none; #5 (t=5100, R_eq 4.82): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
