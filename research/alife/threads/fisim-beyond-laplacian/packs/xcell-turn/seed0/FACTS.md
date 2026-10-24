# Evidence pack: xcell-turn (seed 0)

- world: `../../../worlds/xcell-turn/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a slow waste channel q (tau=40, D=2) produced by the body, trapped by the same membrane gate (D_q exp(-5m)) and inhibiting the body (K=+0.3). Trapped waste ages cells; division dilutes it; cells die and the freed global resource lets others divide (turnover).
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 215s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-turn/world.py --out threads/fisim-beyond-laplacian/packs/xcell-turn --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8865], min area 6 px

## Measurements
- components: final 20, mean 16.5, max 20; occupancy final 0.18
- tracks: 44; persistent (alive >= 50% of run): 18; longest 180 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.305/time; max body lengths 13.4
- replication: splits 18, persistent splits 18, max generation 5, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.3023, None, 0.3335, -0.1615]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 111: holes 0, rim-vs-core 0.61, rim-vs-outside 0.64, heterogeneity 0.21; core [0.916, 0.635, 0.888, 0.758] rim [0.67, 0.868, 0.587, 0.345]
  - track 17 at frame 111: holes 0, rim-vs-core 0.65, rim-vs-outside 0.56, heterogeneity 0.20; core [0.924, 0.692, 0.852, 0.697] rim [0.579, 0.914, 0.511, 0.33]
  - track 20 at frame 114: holes 0, rim-vs-core 0.66, rim-vs-outside 0.56, heterogeneity 0.22; core [0.919, 0.647, 0.857, 0.677] rim [0.577, 0.909, 0.516, 0.318]
  - track 42 at frame 168: holes 0, rim-vs-core 0.61, rim-vs-outside 0.54, heterogeneity 0.19; core [0.924, 0.701, 0.831, 0.617] rim [0.575, 0.904, 0.495, 0.307]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
