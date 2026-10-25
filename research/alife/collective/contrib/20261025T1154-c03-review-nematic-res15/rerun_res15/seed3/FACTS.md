# Evidence pack: active-nematic-droplets (seed 3)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1036-c11-active-nematic-res15/world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [192, 192]; wall 681s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1036-c11-active-nematic-res15/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/nemr/res/seed3 --seeds 3 --size 192 192 --no-movie`
- segmentation: matter > 1.10 of robust range [-0.6, -0.0533], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 0; occupancy final 0.00
- tracks: 0; persistent (alive >= 50% of run): 0; longest 0 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 1], H1 [1, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.5027, -1.0, None]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
