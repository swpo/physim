# Evidence pack: cips-gene (seed 7)

- world: `../../20261026T2316-c48-cips-gene-selection-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1023s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2316-c48-cips-gene-selection-negative/world.py --out collective/contrib/c53-rev-gneg/pack --seeds 7 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0239, 0.9737], min area 6 px

## Measurements
- components: final 12, mean 9.7, max 13; occupancy final 0.06
- tracks: 28; persistent (alive >= 50% of run): 10; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 12], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 10, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [-0.0165, 0.3538, -0.06, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 56: holes 0, rim-vs-core 0.55, rim-vs-outside 1.11, heterogeneity 0.11; core [0.983, 0.935, 0.054, 0.078, 0.0, 1.0] rim [0.776, 0.697, 0.24, 0.488, 0.0, 0.996]
  - track 8 at frame 75: holes 0, rim-vs-core 0.55, rim-vs-outside 1.13, heterogeneity 0.11; core [0.982, 0.931, 0.042, 0.089, 0.0, 1.0] rim [0.776, 0.69, 0.23, 0.5, 0.0, 0.996]
  - track 3 at frame 46: holes 0, rim-vs-core 0.58, rim-vs-outside 1.13, heterogeneity 0.11; core [0.984, 0.937, 0.05, 0.084, 0.0, 1.0] rim [0.767, 0.687, 0.242, 0.521, 0.0, 0.999]
  - track 11 at frame 78: holes 0, rim-vs-core 0.58, rim-vs-outside 1.15, heterogeneity 0.11; core [0.983, 0.935, 0.051, 0.084, 0.0, 1.0] rim [0.766, 0.685, 0.242, 0.525, 0.0, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 29 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.845)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 11.9 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.818)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22, rim/outside 0.643 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.489)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.97, rim/outside 16.2 (aggregate of 62 individuals; 56/62 membrane-like individually; rim level 0.477)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 20 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.27)
  - radial g2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 45.7 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.598)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #7 (t=5600, R_eq 8.21): ['s']; #8 (t=7500, R_eq 8.41): ['s']; #3 (t=4600, R_eq 8.18): ['s']; #11 (t=7800, R_eq 8.2): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
