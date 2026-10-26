# Evidence pack: phoretic-colloids (seed 2)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 39s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0315-c32-review-janus/world.py --out collective/contrib/20261026T0315-c32-review-janus/pack_recip --seeds 2 3 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7852], min area 6 px

## Measurements
- components: final 20, mean 24.9, max 39; occupancy final 0.07
- tracks: 145; persistent (alive >= 50% of run): 21; longest 377 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 20, 15], H1 [0, 0, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.321/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio n/a, nucleations 117
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 212: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.11; core [0.671, 0.658, 0.505] rim [0.563, 0.41, 0.44]
  - track 0 at frame 205: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.15; core [0.82, 0.372, 0.582] rim [0.525, 0.459, 0.478]
  - track 8 at frame 218: holes 0, rim-vs-core 0.32, rim-vs-outside 0.29, heterogeneity 0.15; core [0.707, 0.53, 0.508] rim [0.421, 0.646, 0.427]
  - track 72 at frame 235: holes 0, rim-vs-core 0.17, rim-vs-outside 0.26, heterogeneity 0.09; core [0.68, 0.479, 0.442] rim [0.526, 0.445, 0.382]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 137 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 22.2 (aggregate of 137 individuals; 0/137 membrane-like individually; rim level 0.695)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 17.9 (aggregate of 137 individuals; 22/137 membrane-like individually; rim level 0.545)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 2.87 (aggregate of 137 individuals; 0/137 membrane-like individually; rim level 0.609)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=106, R_eq 2.88): none; #0 (t=102.5, R_eq 3.48): ['B density']; #8 (t=109, R_eq 3.04): ['B density']; #72 (t=117.5, R_eq 2.59): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
