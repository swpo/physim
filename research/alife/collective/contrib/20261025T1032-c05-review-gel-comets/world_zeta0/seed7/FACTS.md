# Evidence pack: active-gel-fed-comets (seed 7)

- world: `../../../../contrib/20261025T1016-c09-active-gel-comets-claim/world_zeta0.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world_zeta0.py --out collective/work_c05/rev_gel/world_zeta0/seed7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 1.58 of robust range [0.0664, 0.6564], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 0; occupancy final 0.00
- tracks: 0; persistent (alive >= 50% of run): 0; longest 0 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.7963, -0.6603, -0.5093]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
