# Evidence pack: phoretic-colloids (seed 3)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 36s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0315-c32-review-janus/world.py --out collective/contrib/20261026T0315-c32-review-janus/pack_recip --seeds 2 3 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.869], min area 6 px

## Measurements
- components: final 20, mean 24.9, max 36; occupancy final 0.07
- tracks: 201; persistent (alive >= 50% of run): 19; longest 382 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 16], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.274/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 24, merge/split ratio n/a, nucleations 177
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 212: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.15; core [0.737, 0.69, 0.654] rim [0.498, 0.521, 0.531]
  - track 7 at frame 215: holes 0, rim-vs-core 0.34, rim-vs-outside 0.35, heterogeneity 0.14; core [0.869, 0.337, 0.695] rim [0.569, 0.424, 0.559]
  - track 40 at frame 229: holes 0, rim-vs-core 0.24, rim-vs-outside 0.26, heterogeneity 0.13; core [0.532, 0.871, 0.416] rim [0.522, 0.638, 0.383]
  - track 47 at frame 232: holes 0, rim-vs-core 0.39, rim-vs-outside 0.36, heterogeneity 0.17; core [0.908, 0.45, 0.865] rim [0.572, 0.432, 0.669]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 20.3 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.715)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 15.5 (aggregate of 128 individuals; 18/128 membrane-like individually; rim level 0.561)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 2.79 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.64)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=106, R_eq 3.7): none; #7 (t=107.5, R_eq 3.87): ['B density']; #40 (t=114.5, R_eq 1.95): none; #47 (t=116, R_eq 4.62): ['B density']

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
