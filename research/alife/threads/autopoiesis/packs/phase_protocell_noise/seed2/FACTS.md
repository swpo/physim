# Evidence pack: phase-protocell-noise (seed 2)

- world: `../../../worlds/phase_protocell_noise/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: same dynamics, unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell_noise/world.py --out threads/autopoiesis/packs/phase_protocell_noise --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.529], min area 6 px

## Measurements
- components: final 43, mean 27.4, max 43; occupancy final 0.37
- tracks: 108; persistent (alive >= 50% of run): 15; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.04 (1 = constant size)
- enclosures: components with a hole mean 2.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 43], H1 [45, 37, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication: splits 37, persistent splits 32, max generation 4, merges 1, nucleations 0
- channel total drift (end/start - 1): [-0.535, -0.6822, 0.2975, -0.0278]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 104: holes 0, rim-vs-core 0.43, rim-vs-outside 0.98, heterogeneity 0.18; core [0.094, 0.852, 0.738, 0.657] rim [0.273, 0.479, 0.658, 0.716]
  - track 52 at frame 104: holes 0, rim-vs-core 0.46, rim-vs-outside 0.97, heterogeneity 0.19; core [0.087, 0.859, 0.728, 0.586] rim [0.29, 0.467, 0.659, 0.692]
  - track 55 at frame 105: holes 0, rim-vs-core 0.46, rim-vs-outside 0.96, heterogeneity 0.19; core [0.086, 0.849, 0.716, 0.585] rim [0.291, 0.46, 0.653, 0.685]
  - track 86 at frame 126: holes 0, rim-vs-core 0.46, rim-vs-outside 0.98, heterogeneity 0.19; core [0.101, 0.885, 0.782, 0.637] rim [0.283, 0.478, 0.672, 0.699]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
