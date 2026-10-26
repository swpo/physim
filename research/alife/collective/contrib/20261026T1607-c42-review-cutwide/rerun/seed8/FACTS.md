# Evidence pack: cips-layered-divide (seed 8)

- world: `../../../20261026T1238-c40-cips-local-cut-wide/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 893s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1238-c40-cips-local-cut-wide/world.py --out collective/contrib/20261026T1607-c42-review-cutwide/rerun/seed8 --seeds 8 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0211, 0.9754], min area 6 px

## Measurements
- components: final 13, mean 8.3, max 13; occupancy final 0.08
- tracks: 22; persistent (alive >= 50% of run): 4; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 13], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00423/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 9, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [0.0, -0.6198, 0.669, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 76: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.17; core [0.984, 0.949, 0.038, 0.083] rim [0.775, 0.708, 0.221, 0.522]
  - track 9 at frame 78: holes 0, rim-vs-core 0.55, rim-vs-outside 0.62, heterogeneity 0.16; core [0.986, 0.953, 0.041, 0.082] rim [0.783, 0.715, 0.222, 0.503]
  - track 11 at frame 79: holes 0, rim-vs-core 0.60, rim-vs-outside 0.60, heterogeneity 0.17; core [0.977, 0.931, 0.036, 0.086] rim [0.76, 0.699, 0.215, 0.558]
  - track 12 at frame 100: holes 0, rim-vs-core 0.61, rim-vs-outside 0.61, heterogeneity 0.17; core [0.981, 0.938, 0.037, 0.085] rim [0.756, 0.694, 0.221, 0.564]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 34.6 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.855)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 12.4 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.832)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 31.9, rim/outside 0.637 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.481)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.46, rim/outside 17.6 (aggregate of 56 individuals; 53/56 membrane-like individually; rim level 0.486)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #5 (t=7600, R_eq 8.16): ['s']; #9 (t=7800, R_eq 7.94): ['s']; #11 (t=7900, R_eq 8.72): ['s']; #12 (t=10000, R_eq 8.48): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
