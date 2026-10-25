# Evidence pack: cips-fuel (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 235s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1845-c23-cips-metabolic-claim/hold --seeds 0 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0011, 1.0026], min area 6 px

## Measurements
- components: final 164, mean 220.0, max 410; occupancy final 0.14
- tracks: 639; persistent (alive >= 50% of run): 183; longest 293 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [164, 164, 164], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00613/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 212, merge/split ratio n/a, nucleations 427
- channel total drift (end/start - 1): [-0.0, -0.1982, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 154: holes 0, rim-vs-core 0.29, rim-vs-outside 0.59, heterogeneity 0.07; core [0.987, 0.759, 0.0] rim [0.757, 0.582, 0.0]
  - track 2 at frame 154: holes 0, rim-vs-core 0.17, rim-vs-outside 0.51, heterogeneity 0.05; core [0.992, 0.72, 0.0] rim [0.878, 0.6, 0.0]
  - track 8 at frame 156: holes 0, rim-vs-core 0.24, rim-vs-outside 0.57, heterogeneity 0.07; core [0.991, 0.768, 0.0] rim [0.816, 0.607, 0.0]
  - track 16 at frame 156: holes 0, rim-vs-core 0.26, rim-vs-outside 0.58, heterogeneity 0.07; core [0.99, 0.784, 0.0] rim [0.799, 0.612, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1256 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 57.8 (aggregate of 1256 individuals; 0/1256 membrane-like individually; rim level 0.964)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 4.14 (aggregate of 1256 individuals; 0/1256 membrane-like individually; rim level 0.759)
  - radial F: flat profile (no radial structure; level 0; aggregate of 1256 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1540, R_eq 3.43): none; #2 (t=1540, R_eq 2.71): none; #8 (t=1560, R_eq 3.29): none; #16 (t=1560, R_eq 3.48): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
