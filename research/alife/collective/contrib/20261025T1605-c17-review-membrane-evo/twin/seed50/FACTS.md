# Evidence pack: membrane-evo (seed 50)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 100s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed50 --seeds 50 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3033], min area 6 px

## Measurements
- components: final 0, mean 0.1, max 9; occupancy final 0.00
- tracks: 9; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 5000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 0: holes 0, rim-vs-core 0.09, rim-vs-outside 0.68, heterogeneity 0.13; core [0.806, 0.0, 0.827, 1.0] rim [0.9, 0.0, 0.84, 1.0]
  - track 2 at frame 0: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.23; core [0.811, 0.0, 0.801, 0.98] rim [0.811, 0.0, 0.91, 0.75]
  - track 3 at frame 0: holes 0, rim-vs-core 0.24, rim-vs-outside 0.65, heterogeneity 0.23; core [0.771, 0.0, 0.768, 1.0] rim [0.862, 0.0, 0.827, 0.79]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
