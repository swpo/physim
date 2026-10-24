# Evidence pack: phase-protocell-noise (seed 0)

- world: `../../../worlds/phase_protocell_noise/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: same dynamics, unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_protocell_noise/world.py --out threads/autopoiesis/packs/phase_protocell_noise --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5276], min area 6 px

## Measurements
- components: final 42, mean 25.8, max 42; occupancy final 0.36
- tracks: 125; persistent (alive >= 50% of run): 9; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.20 (1 = constant size)
- enclosures: components with a hole mean 2.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 42, 42], H1 [42, 41, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication: splits 45, persistent splits 30, max generation 3, merges 4, nucleations 0
- channel total drift (end/start - 1): [-0.5283, -0.6837, 0.2774, 0.0239]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 98: holes 0, rim-vs-core 0.46, rim-vs-outside 0.98, heterogeneity 0.19; core [0.088, 0.87, 0.743, 0.587] rim [0.289, 0.475, 0.666, 0.697]
  - track 73 at frame 104: holes 0, rim-vs-core 0.45, rim-vs-outside 0.96, heterogeneity 0.19; core [0.083, 0.845, 0.711, 0.599] rim [0.286, 0.456, 0.643, 0.683]
  - track 75 at frame 105: holes 0, rim-vs-core 0.42, rim-vs-outside 0.97, heterogeneity 0.18; core [0.086, 0.841, 0.712, 0.609] rim [0.284, 0.479, 0.675, 0.703]
  - track 89 at frame 125: holes 0, rim-vs-core 0.26, rim-vs-outside 1.02, heterogeneity 0.18; core [0.095, 0.84, 0.72, 0.659] rim [0.204, 0.617, 0.677, 0.615]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
