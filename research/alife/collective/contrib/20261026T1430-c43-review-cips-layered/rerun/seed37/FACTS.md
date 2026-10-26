# Evidence pack: cips-layered-divide (seed 37)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1934s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1430-c43-review-cips-layered/world.py --out collective/contrib/20261026T1430-c43-review-cips-layered/rerun/seed37 --seeds 37 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0211, 0.976], min area 6 px

## Measurements
- components: final 17, mean 12.2, max 17; occupancy final 0.09
- tracks: 29; persistent (alive >= 50% of run): 11; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.96 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 17, 17], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.00325/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 5
- channel total drift (end/start - 1): [0.0, -0.5843, 0.6311, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 118: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.989, 0.953, 0.061, 0.077] rim [0.784, 0.707, 0.244, 0.479]
  - track 8 at frame 118: holes 0, rim-vs-core 0.58, rim-vs-outside 0.64, heterogeneity 0.17; core [0.988, 0.952, 0.062, 0.077] rim [0.771, 0.699, 0.25, 0.508]
  - track 13 at frame 136: holes 0, rim-vs-core 0.52, rim-vs-outside 0.63, heterogeneity 0.15; core [0.984, 0.941, 0.045, 0.08] rim [0.793, 0.71, 0.224, 0.464]
  - track 25 at frame 168: holes 0, rim-vs-core 0.54, rim-vs-outside 0.64, heterogeneity 0.16; core [0.989, 0.952, 0.054, 0.076] rim [0.786, 0.707, 0.237, 0.473]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 34.3 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.881)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 12.5 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.839)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.8, rim/outside 0.655 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.497)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.76, rim/outside 21.1 (aggregate of 79 individuals; 72/79 membrane-like individually; rim level 0.572)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #7 (t=11800, R_eq 7.4): ['s']; #8 (t=11800, R_eq 7.51): ['s']; #13 (t=13600, R_eq 7.98): ['s']; #25 (t=16800, R_eq 7.55): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
