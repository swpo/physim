# Evidence pack: phoretic-colloids (seed 3)

- world: `../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 147s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0445-c32-review-phor-dthalf/world.py --out collective/contrib/20261026T0445-c32-review-phor-dthalf/pack_dthalf --seeds 3 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9047], min area 6 px

## Measurements
- components: final 12, mean 12.8, max 22; occupancy final 0.05
- tracks: 221; persistent (alive >= 50% of run): 3; longest 715 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 16, 10], H1 [0, 0, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.505/time; max body lengths 10.8
- replication (lineage window K = 20 frames = time 10, default): splits 16, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 30, merge/split ratio 1.88, nucleations 159
- channel total drift (end/start - 1): [0.5171, 0.265, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 444: holes 0, rim-vs-core 0.24, rim-vs-outside 0.29, heterogeneity 0.13; core [0.854, 0.203, 0.538] rim [0.637, 0.156, 0.446]
  - track 28 at frame 350: holes 0, rim-vs-core 0.19, rim-vs-outside 0.27, heterogeneity 0.05; core [0.839, 0.0, 0.419] rim [0.661, 0.0, 0.362]
  - track 0 at frame 249: holes 0, rim-vs-core 0.28, rim-vs-outside 0.29, heterogeneity 0.14; core [0.84, 0.207, 0.606] rim [0.611, 0.11, 0.486]
  - track 183 at frame 746: holes 0, rim-vs-core 0.30, rim-vs-outside 0.23, heterogeneity 0.15; core [0.812, 0.145, 0.485] rim [0.547, 0.27, 0.415]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 67 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 16.4 (aggregate of 67 individuals; 1/67 membrane-like individually; rim level 0.694)
  - radial B density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 12 (aggregate of 67 individuals; 28/67 membrane-like individually; rim level 0.327)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 2.87 (aggregate of 67 individuals; 0/67 membrane-like individually; rim level 0.553)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=222, R_eq 3.61): ['B density']; #28 (t=175, R_eq 2.88): none; #0 (t=124.5, R_eq 4.15): none; #183 (t=373, R_eq 3.14): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
