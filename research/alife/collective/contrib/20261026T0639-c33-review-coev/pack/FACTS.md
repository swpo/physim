# Evidence pack: coev-matching (seed 5)

- world: `../../20261026T0605-c38-coev-matching-o/world.py`, family `particle`
- parent: 20261026T0125-c30-q-o-needs-moving-target; mutation: individual-based predator-prey particles with heritable 2-D matching traits (capture exp(-|pref-trait|^2/w^2))
- run: 201 frames x 1 steps x dt 100.0 = time 20000; grid [64, 64]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0605-c38-coev-matching-o/world.py --out collective/contrib/wip-c33-coev/pack --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 3.0], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 1; occupancy final 0.00
- tracks: 1; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [75, 32, 4], H1 [24, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 1
- channel total drift (end/start - 1): [-0.31, 7.6333, -0.6462]
- radial profiles: no component with area >= 12 px at the sampled frames
- species `prey` (channels ['prey'], own threshold): components final 0, mean 0.0, max 1; tracks 1, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
