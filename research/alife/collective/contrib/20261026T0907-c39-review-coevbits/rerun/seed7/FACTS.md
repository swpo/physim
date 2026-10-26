# Evidence pack: coevbits-matching (seed 7)

- world: `../../world.py`, family `particle`
- parent: 20261026T0125-c30-q-o-needs-moving-target; mutation: individual-based predator-prey particles with heritable 20-bit matching genotypes (capture exp(-h^2/w^2), h = Hamming distance)
- run: 101 frames x 1 steps x dt 100.0 = time 10000; grid [64, 64]; wall 1s; status ok
- command: `python -m labkit.run collective/contrib/c39-rev-coev-wip/world.py --out collective/contrib/c39-rev-coev-wip/rerun/seed7 --seeds 7 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 3.0], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 0; occupancy final 0.00
- tracks: 0; persistent (alive >= 50% of run): 0; longest 0 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [60, 18, 2], H1 [10, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.507, 5.2333, -0.4196]
- radial profiles: no component with area >= 12 px at the sampled frames
- species `prey` (channels ['prey'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
