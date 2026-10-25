# Evidence pack: active-gel-ac-cells (seed 7)

- world: `../world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 119s; status ok
- command: `python -m labkit.run /tmp/c20ac/world.py --out /tmp/c20ac/p050_s7 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 0.6, max 48; occupancy final 0.00
- tracks: 91; persistent (alive >= 50% of run): 0; longest 6 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 20, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 1, nucleations 1
- channel total drift (end/start - 1): [-1.0, -1.0, -0.8354, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 36 at frame 3: holes 0, rim-vs-core 0.03, rim-vs-outside 0.05, heterogeneity 0.06; core [1.0, 0.937, 0.821, 0.027] rim [1.0, 0.928, 0.849, 0.028]
  - track 88 at frame 3: holes 0, rim-vs-core 0.07, rim-vs-outside 0.10, heterogeneity 0.10; core [1.0, 0.826, 0.838, 0.025] rim [1.0, 0.764, 0.825, 0.046]
  - track 56 at frame 3: holes 0, rim-vs-core 0.05, rim-vs-outside 0.13, heterogeneity 0.04; core [1.0, 1.0, 0.915, 0.0] rim [1.0, 0.957, 0.889, 0.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
