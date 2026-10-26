# Evidence pack: hash-chemistry (seed 1)

- world: `../../world.py`, family `hash-chemistry`
- parent: None; mutation: reproduction of Sayama 2019 Hash Chemistry (positive control for O)
- run: 101 frames x 20 steps x dt 1.0 = time 2000; grid [128, 128]; wall 7s; status ok
- command: `python -m labkit.run collective/contrib/WIP-c30-hash/world.py --out collective/contrib/WIP-c30-hash/pack --seeds 0 1 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 7.0], min area 6 px

## Measurements
- components: final 0, mean 1.1, max 5; occupancy final 0.00
- tracks: 110; persistent (alive >= 50% of run): 0; longest 3 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 9, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 400, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 110
- channel total drift (end/start - 1): [272.1, 1939.0, 86.8889]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
