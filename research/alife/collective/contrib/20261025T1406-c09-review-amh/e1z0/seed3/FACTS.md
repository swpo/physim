# Evidence pack: active-model-h (seed 3)

- world: `../../../20261025T1240-c12-amh-turnover-static/world.py`, family `active-model-h`
- parent: None; mutation: -
- run: 151 frames x 200 steps x dt 0.05 = time 1500; grid [128, 128]; wall 277s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1240-c12-amh-turnover-static/world.py --out collective/contrib/20261025T1406-c09-review-amh/e1z0/seed3 --seeds 3 --frames 150 --spf 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1007, 1.9988], min area 6 px

## Measurements
- components: final 61, mean 46.3, max 93; occupancy final 0.37
- tracks: 188; persistent (alive >= 50% of run): 43; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.52 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 61, 61], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 56, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 27, merge/split ratio 0.482, nucleations 0
- channel total drift (end/start - 1): [-0.0003, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 96: holes 0, rim-vs-core 0.48, rim-vs-outside 0.20, heterogeneity 0.15; core [0.804, 0.215] rim [0.32, 0.199]
  - track 6 at frame 100: holes 0, rim-vs-core 0.47, rim-vs-outside 0.19, heterogeneity 0.15; core [0.78, 0.253] rim [0.307, 0.234]
  - track 7 at frame 100: holes 0, rim-vs-core 0.47, rim-vs-outside 0.21, heterogeneity 0.14; core [0.805, 0.058] rim [0.335, 0.069]
  - track 147 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.18, heterogeneity 0.13; core [0.704, 0.184] rim [0.305, 0.173]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 297 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi + 1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.739, rim/outside 7.46 (aggregate of 297 individuals; 1/297 membrane-like individually; rim level 0.695)
  - radial flow speed |u|: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.06 (aggregate of 297 individuals; 3/297 membrane-like individually; rim level 0.202)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=960, R_eq 5.41): none; #6 (t=1000, R_eq 5.11): none; #7 (t=1000, R_eq 5.2): none; #147 (t=1010, R_eq 3.95): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: for 2 of 297 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
