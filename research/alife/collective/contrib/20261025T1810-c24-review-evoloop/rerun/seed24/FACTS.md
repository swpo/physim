# Evidence pack: evoloop (seed 24)

- world: `../../../20261025T1256-c16-evoloop-claim/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 20s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T1810-c24-review-evoloop/rerun/seed24 --seeds 24 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.0], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 1; occupancy final 0.00
- tracks: 1; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 0: holes 0, rim-vs-core 0.58, rim-vs-outside 0.49, heterogeneity 0.27; core [1.0, 0.317, 0.008, 0.0] rim [0.426, 0.234, 0.043, 0.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
