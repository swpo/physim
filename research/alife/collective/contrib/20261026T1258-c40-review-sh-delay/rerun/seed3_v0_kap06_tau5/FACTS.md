# Evidence pack: sh-spots-inhibitor (seed 3)

- world: `../../world_v0.py`, family `swift-hohenberg`
- parent: None; mutation: Swift-Hohenberg (quadratic-cubic) localized states plus a slow linear inhibitor for a drift bifurcation; new class
- run: 101 frames x 50 steps x dt 0.1 = time 500; grid [128, 128]; wall 16s; status ok
- command: `python -m labkit.run world_v0.py --out rerun/seed3_v0_kap06_tau5 --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 138.10 of robust range [-0.0, 0.0028], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 1; occupancy final 0.00
- tracks: 1; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 0: holes 0, rim-vs-core 0.00, rim-vs-outside 0.00, heterogeneity 0.00; core [1.0, 0.187, 0.0] rim [1.0, 0.187, 0.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
