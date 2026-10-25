# Evidence pack: pcell (seed 0)

- world: `../../world_gate0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 22s; status ok
- command: `python -m labkit.run collective/work/pcell/world_gate0.py --out collective/work/pcell/pack_gate0 --seeds 0 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3607], min area 6 px

## Measurements
- components: final 0, mean 0.8, max 33; occupancy final 0.00
- tracks: 61; persistent (alive >= 50% of run): 0; longest 11 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 1000, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 0.455, nucleations 3
- channel total drift (end/start - 1): [0.0, -1.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 9: holes 1, rim-vs-core 0.21, rim-vs-outside 0.69, heterogeneity 0.18; core [0.0, 0.722, 0.481, 0.81] rim [0.036, 0.568, 0.492, 0.666]
  - track 34 at frame 5: holes 1, rim-vs-core 0.28, rim-vs-outside 0.70, heterogeneity 0.20; core [0.002, 0.745, 0.589, 0.78] rim [0.101, 0.536, 0.533, 0.625]
  - track 46 at frame 7: holes 1, rim-vs-core 0.26, rim-vs-outside 0.77, heterogeneity 0.19; core [0.0, 0.685, 0.46, 0.654] rim [0.09, 0.461, 0.533, 0.693]
  - track 7 at frame 3: holes 0, rim-vs-core 0.52, rim-vs-outside 0.60, heterogeneity 0.20; core [0.046, 0.763, 0.758, 0.767] rim [0.238, 0.32, 0.585, 0.66]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
