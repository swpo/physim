# Evidence pack: cips-layered-lownoise (seed 6)

- world: `../../../20261026T1626-c44-cips-lownoise-gen4-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 251 frames x 1000 steps x dt 0.1 = time 25000; grid [192, 192]; wall 1323s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1626-c44-cips-lownoise-gen4-claim/world.py --out collective/contrib/20261026T2231-c46-review-cips-lownoise/rerun/seed6 --seeds 6 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [0.022, 0.9747], min area 6 px

## Measurements
- components: final 17, mean 12.0, max 17; occupancy final 0.09
- tracks: 31; persistent (alive >= 50% of run): 13; longest 216 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.53 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00377/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 3
- channel total drift (end/start - 1): [0.0, -0.5893, 0.635, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 143: holes 0, rim-vs-core 0.34, rim-vs-outside 0.79, heterogeneity 0.17; core [0.984, 0.934, 0.073, 0.078] rim [0.856, 0.8, 0.168, 0.349]
  - track 12 at frame 162: holes 0, rim-vs-core 0.58, rim-vs-outside 0.62, heterogeneity 0.17; core [0.984, 0.938, 0.046, 0.083] rim [0.767, 0.691, 0.236, 0.525]
  - track 14 at frame 164: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.987, 0.946, 0.047, 0.081] rim [0.786, 0.704, 0.231, 0.474]
  - track 19 at frame 185: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.952, 0.061, 0.077] rim [0.786, 0.708, 0.245, 0.477]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 48.9 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.939)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 14.6 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.879)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 32.7, rim/outside 0.659 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.501)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.11, rim/outside 29.5 (aggregate of 81 individuals; 77/81 membrane-like individually; rim level 0.665)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=14300, R_eq 7.65): ['s']; #12 (t=16200, R_eq 8.18): ['s']; #14 (t=16400, R_eq 7.86): ['s']; #19 (t=18500, R_eq 7.48): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
