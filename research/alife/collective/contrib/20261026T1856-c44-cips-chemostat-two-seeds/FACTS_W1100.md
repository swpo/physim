# Evidence pack: cips-layered-chemostat (seed 0)

- world: `../world_wash.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [192, 192]; wall 2188s; status ok
- command: `python -m labkit.run world_wash.py --out W1100 --seeds 0 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0213, 0.9757], min area 6 px

## Measurements
- components: final 11, mean 11.2, max 15; occupancy final 0.07
- tracks: 50; persistent (alive >= 50% of run): 4; longest 238 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.36 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 11, 11], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.0034/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 22, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0125, -0.6402, 0.6911, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 156: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.985, 0.951, 0.044, 0.084] rim [0.778, 0.708, 0.228, 0.497]
  - track 9 at frame 139: holes 0, rim-vs-core 0.54, rim-vs-outside 0.60, heterogeneity 0.16; core [0.975, 0.921, 0.057, 0.072] rim [0.771, 0.71, 0.211, 0.493]
  - track 10 at frame 113: holes 0, rim-vs-core 0.38, rim-vs-outside 0.75, heterogeneity 0.17; core [0.985, 0.951, 0.04, 0.087] rim [0.842, 0.781, 0.167, 0.372]
  - track 39 at frame 267: holes 0, rim-vs-core 0.57, rim-vs-outside 0.61, heterogeneity 0.16; core [0.983, 0.941, 0.04, 0.086] rim [0.769, 0.696, 0.223, 0.52]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 30.7 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.851)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 11.9 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.824)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21, rim/outside 0.646 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.482)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.88, rim/outside 16 (aggregate of 71 individuals; 66/71 membrane-like individually; rim level 0.459)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #11 (t=15600, R_eq 8.14): ['s']; #9 (t=13900, R_eq 9.06): ['s']; #10 (t=11300, R_eq 8.16): ['s']; #39 (t=26700, R_eq 8.35): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
