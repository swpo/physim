# Evidence pack: cips-fuel (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 260s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1820-c23-cips-sighting/world.py --out collective/contrib/20261025T1820-c23-cips-sighting/pack --seeds 0 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.999], min area 6 px

## Measurements
- components: final 183, mean 204.9, max 301; occupancy final 0.14
- tracks: 419; persistent (alive >= 50% of run): 198; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [184, 183, 183], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 111, merge/split ratio n/a, nucleations 308
- channel total drift (end/start - 1): [0.0, -0.2179, 0.1502]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 159: holes 0, rim-vs-core 0.34, rim-vs-outside 0.51, heterogeneity 0.10; core [0.97, 0.854, 0.189] rim [0.724, 0.668, 0.332]
  - track 1 at frame 161: holes 0, rim-vs-core 0.24, rim-vs-outside 0.49, heterogeneity 0.08; core [0.981, 0.872, 0.157] rim [0.828, 0.721, 0.274]
  - track 3 at frame 161: holes 0, rim-vs-core 0.28, rim-vs-outside 0.50, heterogeneity 0.09; core [0.984, 0.894, 0.159] rim [0.82, 0.72, 0.298]
  - track 4 at frame 161: holes 0, rim-vs-core 0.32, rim-vs-outside 0.51, heterogeneity 0.11; core [0.975, 0.874, 0.137] rim [0.753, 0.691, 0.282]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1287 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.949, rim/outside 48 (aggregate of 1287 individuals; 0/1287 membrane-like individually; rim level 0.94)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 4.04 (aggregate of 1287 individuals; 0/1287 membrane-like individually; rim level 0.818)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.63, rim/outside 0.675 (aggregate of 1287 individuals; 0/1287 membrane-like individually; rim level 0.451)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1590, R_eq 3.43): none; #1 (t=1610, R_eq 3.19): none; #3 (t=1610, R_eq 3.43): none; #4 (t=1610, R_eq 3.61): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
