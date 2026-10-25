# Evidence pack: lipid-2d (seed 3)

- world: `../../world.py`, family `lipid-particle`
- parent: None; mutation: -
- run: 201 frames x 60 steps x dt 0.3 = time 3600; grid [128, 128]; wall 1090s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1310-c13-review-lipid-2d/world.py --out collective/contrib/20261025T1310-c13-review-lipid-2d/rerun/seed3 --seeds 3 --spf 60 --frames 200 --no-movie`
- segmentation: matter > 0.93 of robust range [0.0, 0.5355], min area 6 px

## Measurements
- components: final 1, mean 0.0, max 1; occupancy final 0.00
- tracks: 3; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [73, 37, 15], H1 [4, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 360, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 2
- channel total drift (end/start - 1): [0.0, 0.0]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
