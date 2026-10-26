# Evidence pack: cips-turnover-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 567s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1505-c41-cips-propulsion-wip/world.py --out collective/contrib/20261026T1505-c41-cips-propulsion-wip/scan_chi6_d006 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0057, 0.9958], min area 6 px

## Measurements
- components: final 49, mean 48.1, max 49; occupancy final 0.11
- tracks: 51; persistent (alive >= 50% of run): 49; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 49], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.00151/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 50
- channel total drift (end/start - 1): [-0.0, -0.4015, 0.4356]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 51: holes 0, rim-vs-core 0.39, rim-vs-outside 0.52, heterogeneity 0.12; core [0.985, 0.887, 0.075] rim [0.742, 0.631, 0.243]
  - track 1 at frame 51: holes 0, rim-vs-core 0.39, rim-vs-outside 0.51, heterogeneity 0.12; core [0.986, 0.889, 0.07] rim [0.749, 0.634, 0.238]
  - track 2 at frame 51: holes 0, rim-vs-core 0.33, rim-vs-outside 0.51, heterogeneity 0.10; core [0.988, 0.875, 0.108] rim [0.8, 0.65, 0.247]
  - track 3 at frame 51: holes 0, rim-vs-core 0.35, rim-vs-outside 0.51, heterogeneity 0.11; core [0.986, 0.874, 0.103] rim [0.776, 0.641, 0.248]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 294 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 83.5 (aggregate of 294 individuals; 0/294 membrane-like individually; rim level 0.992)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 8.22 (aggregate of 294 individuals; 0/294 membrane-like individually; rim level 0.858)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.1, rim/outside 0.674 (aggregate of 294 individuals; 0/294 membrane-like individually; rim level 0.434)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5100, R_eq 5.26): none; #1 (t=5100, R_eq 5.32): none; #2 (t=5100, R_eq 4.55): none; #3 (t=5100, R_eq 4.69): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
