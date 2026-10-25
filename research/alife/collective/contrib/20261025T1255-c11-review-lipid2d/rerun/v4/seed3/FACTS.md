# Evidence pack: lipid-2d (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1025-c12-lipid-2d-sighting/world.py`, family `lipid-particle`
- parent: None; mutation: -
- run: 8001 frames x 1 steps x dt 0.3 = time 2400; grid [128, 128]; wall 686s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1025-c12-lipid-2d-sighting/world.py --out /tmp/claude-0/c11rev22/v4 --seeds 3 --frames 8000 --no-movie`
- segmentation: matter > 0.93 of robust range [0.0, 0.5357], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 1; occupancy final 0.00
- tracks: 1; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [76, 51, 32], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 6, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0, 0.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
