# Evidence pack: noise-control (seed 0)

- world: `../../noise_control/world.py`, family `control`
- parent: None; mutation: reference
- run: 101 frames x 1 steps x dt 1.0 = time 100; grid [128, 128]; wall 0s; status ok
- command: `python -m labkit.run examples/noise_control/world.py --out examples/packs/noise_control --frames 100`
- segmentation: matter > 0.35 of robust range [-0.0902, 0.1196], min area 6 px

## Measurements
- components: final 3, mean 2.1, max 5; occupancy final 0.64
- tracks: 174; persistent (alive >= 50% of run): 0; longest 4 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.99, final 1; holes at thresholds 0.2/0.35/0.5 final [25, 20, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 6, 1], H1 [36, 12, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 20, default): splits 56, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 55, merge/split ratio 0.982, nucleations 10
- channel total drift (end/start - 1): [None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 19: holes 21, rim-vs-core 0.33, rim-vs-outside 0.36, heterogeneity 0.15; core [0.925] rim [0.592]
  - track 45 at frame 30: holes 20, rim-vs-core 0.07, rim-vs-outside 0.37, heterogeneity 0.14; core [0.539] rim [0.607]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 13 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial noise: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 1.64 (aggregate of 13 individuals; 0/13 membrane-like individually; rim level 0.474)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #34 (t=24, R_eq 59.24): none; #47 (t=34, R_eq 60.01): none; #29 (t=19, R_eq 58.86): none; #45 (t=30, R_eq 62.34, ring): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: for 6 of 13 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
