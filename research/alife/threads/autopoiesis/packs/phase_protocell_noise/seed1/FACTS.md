# Evidence pack: phase-protocell-noise (seed 1)

- world: `../../../worlds/phase_protocell_noise/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: same dynamics, unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell_noise/world.py --out threads/autopoiesis/packs/phase_protocell_noise --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5262], min area 6 px

## Measurements
- components: final 42, mean 31.3, max 42; occupancy final 0.36
- tracks: 120; persistent (alive >= 50% of run): 32; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.04 (1 = constant size)
- enclosures: components with a hole mean 1.70, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [42, 41, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication: splits 44, persistent splits 28, max generation 3, merges 4, nucleations 0
- channel total drift (end/start - 1): [-0.5318, -0.6835, 0.2861, 0.281]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 83: holes 0, rim-vs-core 0.43, rim-vs-outside 0.96, heterogeneity 0.18; core [0.085, 0.842, 0.726, 0.65] rim [0.274, 0.468, 0.662, 0.697]
  - track 66 at frame 86: holes 0, rim-vs-core 0.37, rim-vs-outside 1.07, heterogeneity 0.18; core [0.074, 0.876, 0.74, 0.53] rim [0.229, 0.598, 0.71, 0.71]
  - track 72 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 1.04, heterogeneity 0.19; core [0.074, 0.861, 0.727, 0.56] rim [0.248, 0.551, 0.688, 0.707]
  - track 94 at frame 114: holes 0, rim-vs-core 0.43, rim-vs-outside 1.00, heterogeneity 0.18; core [0.087, 0.866, 0.754, 0.637] rim [0.268, 0.49, 0.677, 0.719]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
