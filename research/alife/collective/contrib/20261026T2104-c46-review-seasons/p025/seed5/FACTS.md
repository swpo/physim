# Evidence pack: cips-layered-divide (seed 5)

- world: `../../../20261026T1526-c44-cips-seasons-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [128, 128]; wall 433s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1526-c44-cips-seasons-negative/world.py --out collective/contrib/20261026T2104-c46-review-seasons/p025/seed5 --seeds 5 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0222, 0.9743], min area 6 px

## Measurements
- components: final 6, mean 5.7, max 7; occupancy final 0.01
- tracks: 30; persistent (alive >= 50% of run): 2; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00329/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 2, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 26
- channel total drift (end/start - 1): [0.0, -0.9598, -0.7707, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 141: holes 0, rim-vs-core 0.33, rim-vs-outside 0.75, heterogeneity 0.16; core [0.985, 0.947, 0.312, 0.073] rim [0.85, 0.806, 0.381, 0.324]
  - track 11 at frame 141: holes 0, rim-vs-core 0.41, rim-vs-outside 0.70, heterogeneity 0.15; core [0.991, 0.968, 0.288, 0.076] rim [0.823, 0.766, 0.412, 0.366]
  - track 0 at frame 40: holes 0, rim-vs-core 0.56, rim-vs-outside 0.61, heterogeneity 0.16; core [0.983, 0.94, 0.263, 0.091] rim [0.767, 0.694, 0.418, 0.52]
  - track 5 at frame 69: holes 0, rim-vs-core 0.52, rim-vs-outside 0.61, heterogeneity 0.15; core [0.986, 0.949, 0.282, 0.08] rim [0.788, 0.714, 0.422, 0.47]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 8.18 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.803)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 10.2 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.702)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.39, rim/outside 0.75 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.513)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.19, rim/outside 5.9 (aggregate of 35 individuals; 27/35 membrane-like individually; rim level 0.383)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #10 (t=14100, R_eq 7.55): ['s']; #11 (t=14100, R_eq 7.55): ['s']; #0 (t=4000, R_eq 8.44): ['s']; #5 (t=6900, R_eq 7.86): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
