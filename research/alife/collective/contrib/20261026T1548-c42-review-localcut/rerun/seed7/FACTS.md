# Evidence pack: cips-layered-divide (seed 7)

- world: `../../../20261026T1210-c40-cips-local-cut/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 899s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1210-c40-cips-local-cut/world.py --out collective/contrib/20261026T1548-c42-review-localcut/rerun/seed7 --seeds 7 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0214, 0.975], min area 6 px

## Measurements
- components: final 16, mean 12.5, max 16; occupancy final 0.09
- tracks: 25; persistent (alive >= 50% of run): 13; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.84 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0027/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 7
- channel total drift (end/start - 1): [0.0, -0.5889, 0.636, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 74: holes 0, rim-vs-core 0.59, rim-vs-outside 0.60, heterogeneity 0.17; core [0.981, 0.936, 0.059, 0.078] rim [0.763, 0.694, 0.243, 0.533]
  - track 9 at frame 76: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.954, 0.055, 0.08] rim [0.789, 0.711, 0.239, 0.475]
  - track 10 at frame 76: holes 0, rim-vs-core 0.43, rim-vs-outside 0.69, heterogeneity 0.16; core [0.974, 0.918, 0.056, 0.075] rim [0.816, 0.755, 0.2, 0.408]
  - track 21 at frame 96: holes 0, rim-vs-core 0.53, rim-vs-outside 0.63, heterogeneity 0.16; core [0.99, 0.959, 0.07, 0.076] rim [0.791, 0.717, 0.252, 0.464]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 35.2 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.867)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 13 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.834)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 24.1, rim/outside 0.651 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.497)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.4, rim/outside 18.8 (aggregate of 80 individuals; 75/80 membrane-like individually; rim level 0.499)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #7 (t=7400, R_eq 8.23): ['s']; #9 (t=7600, R_eq 7.76): ['s']; #10 (t=7600, R_eq 8.74): ['s']; #21 (t=9600, R_eq 7.36): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
