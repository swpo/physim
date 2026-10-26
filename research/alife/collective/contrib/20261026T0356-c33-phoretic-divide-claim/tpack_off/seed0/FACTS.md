# Evidence pack: phoretic-colloids (seed 0)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 126s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/tpack_off --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0076], min area 6 px

## Measurements
- components: final 6, mean 14.2, max 29; occupancy final 0.06
- tracks: 202; persistent (alive >= 50% of run): 4; longest 579 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 6, 6], H1 [0, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.35/time; max body lengths 10.2
- replication (lineage window K = 20 frames = time 10, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 26, merge/split ratio 26, nucleations 174
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 316: holes 0, rim-vs-core 0.21, rim-vs-outside 0.26, heterogeneity 0.12; core [0.796, 0.304, 0.418] rim [0.593, 0.344, 0.364]
  - track 2 at frame 289: holes 0, rim-vs-core 0.19, rim-vs-outside 0.27, heterogeneity 0.13; core [0.786, 0.311, 0.471] rim [0.609, 0.327, 0.4]
  - track 188 at frame 598: holes 0, rim-vs-core 0.31, rim-vs-outside 0.32, heterogeneity 0.18; core [0.773, 0.592, 0.728] rim [0.573, 0.426, 0.563]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 16.4 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.713)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 15.6 (aggregate of 80 individuals; 35/80 membrane-like individually; rim level 0.443)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 2.91 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.548)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #49 (t=188, R_eq 1.95): ['B density']; #21 (t=158, R_eq 2.99): ['B density']; #2 (t=144.5, R_eq 3.34): none; #188 (t=299, R_eq 5.5): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
