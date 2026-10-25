# Evidence pack: cips-fuel (seed 4)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 238s; status ok
- command: `python -m labkit.run world.py --out reservoir --seeds 4 --frames 300 --spf 100 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0011, 1.0025], min area 6 px

## Measurements
- components: final 168, mean 221.1, max 399; occupancy final 0.14
- tracks: 632; persistent (alive >= 50% of run): 185; longest 293 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [168, 168, 168], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00166/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 207, merge/split ratio n/a, nucleations 425
- channel total drift (end/start - 1): [0.0, -0.1984, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 154: holes 0, rim-vs-core 0.15, rim-vs-outside 0.50, heterogeneity 0.05; core [0.994, 0.708, 0.0] rim [0.893, 0.592, 0.0]
  - track 1 at frame 154: holes 0, rim-vs-core 0.17, rim-vs-outside 0.55, heterogeneity 0.05; core [0.989, 0.666, 0.0] rim [0.857, 0.551, 0.0]
  - track 2 at frame 156: holes 0, rim-vs-core 0.23, rim-vs-outside 0.62, heterogeneity 0.07; core [0.989, 0.757, 0.0] rim [0.821, 0.607, 0.0]
  - track 3 at frame 156: holes 0, rim-vs-core 0.16, rim-vs-outside 0.50, heterogeneity 0.05; core [0.992, 0.72, 0.0] rim [0.884, 0.6, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1262 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 57.9 (aggregate of 1262 individuals; 0/1262 membrane-like individually; rim level 0.964)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 4.08 (aggregate of 1262 individuals; 0/1262 membrane-like individually; rim level 0.745)
  - radial F: flat profile (no radial structure; level 0; aggregate of 1262 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1540, R_eq 2.65): none; #1 (t=1540, R_eq 2.59): none; #2 (t=1560, R_eq 3.39): none; #3 (t=1560, R_eq 2.76): none

## Warnings
- radial: 1 of 1262 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
