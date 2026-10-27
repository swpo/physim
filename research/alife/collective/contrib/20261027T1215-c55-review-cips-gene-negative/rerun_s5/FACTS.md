# Evidence pack: cips-gene (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2316-c48-cips-gene-selection-negative/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 791s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2316-c48-cips-gene-selection-negative/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/gene2/pack --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0245, 0.9729], min area 6 px

## Measurements
- components: final 7, mean 7.6, max 11; occupancy final 0.05
- tracks: 16; persistent (alive >= 50% of run): 7; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00274/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0115, 0.2178, -0.04, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 52: holes 0, rim-vs-core 0.59, rim-vs-outside 1.14, heterogeneity 0.11; core [0.985, 0.945, 0.035, 0.09, 0.0, 1.0] rim [0.766, 0.691, 0.224, 0.538, 0.0, 1.0]
  - track 6 at frame 71: holes 0, rim-vs-core 0.47, rim-vs-outside 1.16, heterogeneity 0.11; core [0.989, 0.958, 0.032, 0.086, 0.0, 1.0] rim [0.816, 0.74, 0.201, 0.421, 0.0, 0.995]
  - track 7 at frame 71: holes 0, rim-vs-core 0.58, rim-vs-outside 1.13, heterogeneity 0.11; core [0.987, 0.951, 0.044, 0.087, 0.0, 1.0] rim [0.772, 0.7, 0.233, 0.531, 0.0, 1.0]
  - track 8 at frame 72: holes 0, rim-vs-core 0.61, rim-vs-outside 1.16, heterogeneity 0.12; core [0.985, 0.945, 0.048, 0.083, 0.0, 1.0] rim [0.757, 0.69, 0.236, 0.554, 0.0, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 34.5 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.879)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 13.5 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.846)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 31, rim/outside 0.64 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.49)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.7, rim/outside 20.8 (aggregate of 47 individuals; 45/47 membrane-like individually; rim level 0.567)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 14.2 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.15)
  - radial g2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 59.3 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.752)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #4 (t=5200, R_eq 8.33): ['s']; #6 (t=7100, R_eq 8.02): ['s']; #7 (t=7100, R_eq 7.98): ['s']; #8 (t=7200, R_eq 8): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
