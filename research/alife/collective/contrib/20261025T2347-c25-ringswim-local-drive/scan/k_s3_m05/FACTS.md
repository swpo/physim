# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2347-c25-ringswim-local-drive/scan/k_s3_m05 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3576], min area 6 px

## Measurements
- components: final 0, mean 0.5, max 27; occupancy final 0.00
- tracks: 64; persistent (alive >= 50% of run): 0; longest 7 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 1000, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 0.273, nucleations 4
- channel total drift (end/start - 1): [0.0, -1.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 3: holes 0, rim-vs-core 0.69, rim-vs-outside 0.46, heterogeneity 0.16; core [0.0, 0.83, 0.991, 0.997] rim [0.0, 0.321, 0.71, 0.626]
  - track 52 at frame 5: holes 1, rim-vs-core 0.23, rim-vs-outside 0.87, heterogeneity 0.12; core [0.0, 0.699, 0.519, 0.977] rim [0.0, 0.616, 0.632, 0.798]
  - track 25 at frame 3: holes 0, rim-vs-core 0.56, rim-vs-outside 0.84, heterogeneity 0.16; core [0.0, 0.947, 0.933, 1.0] rim [0.0, 0.444, 0.766, 0.804]
  - track 46 at frame 5: holes 0, rim-vs-core 0.29, rim-vs-outside 0.96, heterogeneity 0.11; core [0.0, 0.683, 0.464, 0.95] rim [0.0, 0.595, 0.727, 0.849]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
