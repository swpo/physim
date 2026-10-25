# Evidence pack: active-gel-ac-cells (seed 4)

- world: `../../../20261025T1249-c09-ac-gel-cells-bistable/world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 101 frames x 300 steps x dt 0.01 = time 300; grid [128, 128]; wall 312s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1249-c09-ac-gel-cells-bistable/world.py --out collective/contrib/20261025T1440-c16-review-acgel/rerun_ath2/seed4 --seeds 4 --frames 100 --spf 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 0.9941], min area 6 px

## Measurements
- components: final 0, mean 0.4, max 38; occupancy final 0.00
- tracks: 38; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -0.9437, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 0: holes 2, rim-vs-core 0.09, rim-vs-outside 0.27, heterogeneity 0.21; core [0.892, 0.703, 0.666, 1.0] rim [0.908, 0.772, 0.721, 1.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
