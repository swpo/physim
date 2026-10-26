# Evidence pack: phoretic-colloids (seed 4)

- world: `../../20261026T0441-c33-phoretic-no-wall/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 51s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0441-c33-phoretic-no-wall/world.py --out collective/contrib/20261026T0503-c30-review-phoretic-nowall/coat --seeds 4 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6829], min area 6 px

## Measurements
- components: final 23, mean 27.1, max 38; occupancy final 0.08
- tracks: 176; persistent (alive >= 50% of run): 18; longest 376 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 16], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.169/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 10, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 24, merge/split ratio 24, nucleations 151
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 215: holes 0, rim-vs-core 0.34, rim-vs-outside 0.30, heterogeneity 0.17; core [0.851, 0.342, 0.551] rim [0.532, 0.401, 0.456]
  - track 14 at frame 218: holes 0, rim-vs-core 0.30, rim-vs-outside 0.30, heterogeneity 0.11; core [0.821, 0.413, 0.45] rim [0.562, 0.565, 0.397]
  - track 17 at frame 218: holes 0, rim-vs-core 0.33, rim-vs-outside 0.33, heterogeneity 0.14; core [0.829, 0.607, 0.663] rim [0.537, 0.504, 0.537]
  - track 22 at frame 218: holes 0, rim-vs-core 0.31, rim-vs-outside 0.34, heterogeneity 0.14; core [0.84, 0.547, 0.606] rim [0.545, 0.537, 0.505]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 154 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 20.2 (aggregate of 154 individuals; 0/154 membrane-like individually; rim level 0.704)
  - radial B density: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 13.7 (aggregate of 154 individuals; 39/154 membrane-like individually; rim level 0.583)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 2.69 (aggregate of 154 individuals; 0/154 membrane-like individually; rim level 0.597)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=107.5, R_eq 3.19): ['B density']; #14 (t=109, R_eq 2.39): ['B density']; #17 (t=109, R_eq 3.7): none; #22 (t=109, R_eq 3.29): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
