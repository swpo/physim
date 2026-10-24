# Evidence pack: xcell-turn (seed 2)

- world: `../../../worlds/xcell-turn/world.py`, family `fisim-extended-rd`
- parent: xcell-div; mutation: xcell-div + a slow waste channel q (tau=40, D=2) produced by the body, trapped by the same membrane gate (D_q exp(-5m)) and inhibiting the body (K=+0.3). Trapped waste ages cells; division dilutes it; cells die and the freed global resource lets others divide (turnover).
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 204s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-turn/world.py --out threads/fisim-beyond-laplacian/packs/xcell-turn --seeds 0 1 2`
- segmentation: matter > 0.35 of robust range [0.0, 1.8873], min area 6 px

## Measurements
- components: final 20, mean 16.6, max 20; occupancy final 0.18
- tracks: 40; persistent (alive >= 50% of run): 19; longest 178 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.45 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.431/time; max body lengths 14.5
- replication: splits 16, persistent splits 16, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.2946, None, 0.3222, -0.1684]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 113: holes 0, rim-vs-core 0.69, rim-vs-outside 0.55, heterogeneity 0.21; core [0.914, 0.659, 0.869, 0.74] rim [0.57, 0.923, 0.521, 0.327]
  - track 19 at frame 114: holes 0, rim-vs-core 0.63, rim-vs-outside 0.55, heterogeneity 0.21; core [0.924, 0.682, 0.841, 0.635] rim [0.567, 0.908, 0.501, 0.312]
  - track 20 at frame 116: holes 0, rim-vs-core 0.67, rim-vs-outside 0.55, heterogeneity 0.21; core [0.917, 0.697, 0.847, 0.701] rim [0.565, 0.923, 0.499, 0.315]
  - track 38 at frame 185: holes 0, rim-vs-core 0.59, rim-vs-outside 0.55, heterogeneity 0.20; core [0.927, 0.657, 0.842, 0.541] rim [0.575, 0.902, 0.507, 0.303]

## Warnings
- none

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
