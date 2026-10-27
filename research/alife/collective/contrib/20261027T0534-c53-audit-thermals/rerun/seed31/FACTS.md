# Evidence pack: reacting-thermals (seed 31)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 38s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/rerun --seeds 31 32 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.39 of robust range [0.0, 0.6461], min area 6 px

## Measurements
- components: final 0, mean 0.7, max 47; occupancy final 0.00
- tracks: 121; persistent (alive >= 50% of run): 0; longest 20 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 20, default): splits 32, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio 0.344, nucleations 3
- channel total drift (end/start - 1): [-1.0, -0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 15: holes 0, rim-vs-core 0.19, rim-vs-outside 0.79, heterogeneity 0.16; core [0.999, 0.01, 0.356, 1.0] rim [0.84, 0.054, 0.456, 0.982]
  - track 30 at frame 10: holes 0, rim-vs-core 0.14, rim-vs-outside 0.74, heterogeneity 0.16; core [1.0, 0.016, 0.474, 1.0] rim [0.896, 0.101, 0.458, 1.0]
  - track 99 at frame 20: holes 0, rim-vs-core 0.13, rim-vs-outside 0.43, heterogeneity 0.11; core [0.964, 0.007, 0.131, 1.0] rim [0.861, 0.051, 0.192, 0.982]
  - track 0 at frame 5: holes 0, rim-vs-core 0.19, rim-vs-outside 1.19, heterogeneity 0.16; core [1.0, 0.002, 0.536, 1.0] rim [0.937, 0.174, 0.486, 1.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
