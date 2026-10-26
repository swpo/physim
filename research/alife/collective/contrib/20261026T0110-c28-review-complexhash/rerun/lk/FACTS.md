# Evidence pack: complex-hash-chemistry (seed 7)

- world: `../world.py`, family `hash-chemistry`
- parent: collective/contrib/20261026T0009-c30-hash-chemistry-o-calibration/world.py; mutation: particles bound into explicit complexes that move, contest a neighbour and replicate with type/insert/delete mutations
- run: 51 frames x 100 steps x dt 1.0 = time 5000; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run /tmp/claude-0/c28hc/world.py --out /tmp/claude-0/c28hc/lk --seeds 7 --frames 50 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 4.0], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 0; occupancy final 0.00
- tracks: 0; persistent (alive >= 50% of run): 0; longest 0 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [244, 77, 18], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [3.078, 9.6, 36.1337]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
