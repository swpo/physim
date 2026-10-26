# Evidence pack: cips-layered-divide (seed 4)

- world: `../../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 745s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/c39-rev-cipslay-wip/rerun/seed4 --seeds 4 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0223, 0.9747], min area 6 px

## Measurements
- components: final 14, mean 7.1, max 14; occupancy final 0.07
- tracks: 25; persistent (alive >= 50% of run): 1; longest 87 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.16 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 14], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00308/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [-0.0, -0.6164, 0.6655, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 78: holes 0, rim-vs-core 0.58, rim-vs-outside 0.63, heterogeneity 0.17; core [0.989, 0.962, 0.042, 0.087] rim [0.776, 0.715, 0.228, 0.533]
  - track 10 at frame 94: holes 0, rim-vs-core 0.57, rim-vs-outside 0.60, heterogeneity 0.16; core [0.983, 0.945, 0.036, 0.083] rim [0.778, 0.711, 0.212, 0.525]
  - track 11 at frame 95: holes 0, rim-vs-core 0.60, rim-vs-outside 0.62, heterogeneity 0.17; core [0.987, 0.955, 0.036, 0.087] rim [0.767, 0.705, 0.223, 0.548]
  - track 9 at frame 92: holes 0, rim-vs-core 0.59, rim-vs-outside 0.60, heterogeneity 0.16; core [0.979, 0.933, 0.036, 0.083] rim [0.767, 0.704, 0.209, 0.549]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 31.8 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.851)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 12 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.834)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 28.4, rim/outside 0.639 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.481)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.46, rim/outside 17.9 (aggregate of 50 individuals; 46/50 membrane-like individually; rim level 0.539)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=7800, R_eq 7.84): ['s']; #10 (t=9400, R_eq 8.46): ['s']; #11 (t=9500, R_eq 8.2): ['s']; #9 (t=9200, R_eq 8.83): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
