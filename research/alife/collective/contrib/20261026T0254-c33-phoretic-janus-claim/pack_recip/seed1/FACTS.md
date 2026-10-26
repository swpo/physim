# Evidence pack: phoretic-colloids (seed 1)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/pack_recip --seeds 0 1 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9174], min area 6 px

## Measurements
- components: final 20, mean 25.0, max 38; occupancy final 0.07
- tracks: 201; persistent (alive >= 50% of run): 15; longest 377 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 20, 17], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.289/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 25, merge/split ratio n/a, nucleations 176
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 212: holes 0, rim-vs-core 0.35, rim-vs-outside 0.33, heterogeneity 0.13; core [0.704, 0.742, 0.555] rim [0.532, 0.45, 0.462]
  - track 7 at frame 215: holes 0, rim-vs-core 0.25, rim-vs-outside 0.36, heterogeneity 0.15; core [0.888, 0.379, 0.627] rim [0.666, 0.363, 0.523]
  - track 9 at frame 215: holes 0, rim-vs-core 0.20, rim-vs-outside 0.30, heterogeneity 0.13; core [0.789, 0.465, 0.565] rim [0.635, 0.36, 0.481]
  - track 32 at frame 225: holes 0, rim-vs-core 0.27, rim-vs-outside 0.33, heterogeneity 0.16; core [0.788, 0.547, 0.609] rim [0.578, 0.413, 0.504]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 18.4 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.724)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 16.7 (aggregate of 135 individuals; 21/135 membrane-like individually; rim level 0.572)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 2.64 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.622)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=106, R_eq 3.29): none; #7 (t=107.5, R_eq 3.43): ['B density']; #9 (t=107.5, R_eq 3.09): none; #32 (t=112.5, R_eq 3.48): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
