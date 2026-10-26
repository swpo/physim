# Evidence pack: cips-predator-prey (seed 5)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T0704-c35-cips-coop-fork-lsc5; mutation: c35 cooperative CIPS (n=2) with turnover d=0.003 strong enough that the bath is linearly stable, started from a smoothed random field (c40)
- run: 81 frames x 1000 steps x dt 0.1 = time 8000; grid [128, 128]; wall 416s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1815-c43-review-cips-predator/world.py --out collective/contrib/20261026T1815-c43-review-cips-predator/rerun/seed5 --seeds 5 --frames 80 --no-movie`
- segmentation: matter > 3.33 of robust range [0.1515, 0.256], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 0; occupancy final 0.00
- tracks: 0; persistent (alive >= 50% of run): 0; longest 0 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.1893, -0.8348, 0.899, -0.0008, None]
- radial profiles: no component with area >= 12 px at the sampled frames
- species `prey` (channels ['e prey'], own threshold): components final 0, mean 0.1, max 2; tracks 5, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['q predator'], own threshold): components final 0, mean 0.1, max 1; tracks 1, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
