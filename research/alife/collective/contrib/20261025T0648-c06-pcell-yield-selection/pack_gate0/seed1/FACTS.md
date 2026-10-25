# Evidence pack: pcell (seed 1)

- world: `../../world_gate0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 22s; status ok
- command: `python -m labkit.run collective/work/pcell/world_gate0.py --out collective/work/pcell/pack_gate0 --seeds 0 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3248], min area 6 px

## Measurements
- components: final 0, mean 0.6, max 33; occupancy final 0.00
- tracks: 60; persistent (alive >= 50% of run): 0; longest 15 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 1000, default): splits 10, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.4, nucleations 7
- channel total drift (end/start - 1): [0.0, -1.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 9: holes 1, rim-vs-core 0.29, rim-vs-outside 0.76, heterogeneity 0.17; core [0.0, 0.82, 0.506, 0.932] rim [0.01, 0.629, 0.5, 0.72]
  - track 59 at frame 12: holes 1, rim-vs-core 0.30, rim-vs-outside 0.65, heterogeneity 0.17; core [0.0, 0.715, 0.48, 0.939] rim [0.009, 0.57, 0.467, 0.672]
  - track 50 at frame 5: holes 0, rim-vs-core 0.41, rim-vs-outside 0.73, heterogeneity 0.17; core [0.0, 0.725, 0.705, 0.971] rim [0.092, 0.438, 0.576, 0.731]
  - track 40 at frame 3: holes 0, rim-vs-core 0.44, rim-vs-outside 0.35, heterogeneity 0.11; core [0.186, 0.32, 0.778, 0.986] rim [0.248, 0.24, 0.624, 0.588]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
