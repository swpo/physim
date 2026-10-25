# Evidence pack: active-gel-fed-comets (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1224-c09-active-gel-regulator-window/world_ks0.03_r2_kb0.1.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 63s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1224-c09-active-gel-regulator-window/world_ks0.03_r2_kb0.1.py --out /tmp/claude-0/c11rev28/k03 --seeds 4 --frames 300 --no-movie`
- segmentation: matter > 1.55 of robust range [0.1258, 0.6896], min area 6 px

## Measurements
- components: final 0, mean 0.0, max 0; occupancy final 0.00
- tracks: 0; persistent (alive >= 50% of run): 0; longest 0 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 6, 1], H1 [10, 6, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.6999, -0.6999, -0.5001]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
