# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0227-c29-kernel-ring-screen/world.py --out collective/contrib/20261026T0227-c29-kernel-ring-screen/screen/chi4kd08dL01 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.112, 1.3316], min area 6 px

## Measurements
- components: final 0, mean 0.1, max 16; occupancy final 0.00
- tracks: 29; persistent (alive >= 50% of run): 0; longest 2 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 1000, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 2, nucleations 6
- channel total drift (end/start - 1): [-0.6347, -0.8547, 0.5779, -0.9814]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 0: holes 0, rim-vs-core 0.24, rim-vs-outside 0.35, heterogeneity 0.09; core [1.0, 0.966, 0.0, 1.0] rim [1.0, 0.731, 0.019, 1.0]
  - track 1 at frame 0: holes 1, rim-vs-core 0.14, rim-vs-outside 0.83, heterogeneity 0.12; core [1.0, 0.582, 0.018, 1.0] rim [1.0, 0.724, 0.013, 0.988]
  - track 2 at frame 0: holes 0, rim-vs-core 0.06, rim-vs-outside 0.82, heterogeneity 0.12; core [1.0, 0.654, 0.011, 1.0] rim [1.0, 0.714, 0.014, 0.986]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
