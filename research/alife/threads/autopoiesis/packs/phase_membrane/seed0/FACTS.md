# Evidence pack: phase-membrane (seed 0)

- world: `../../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5437], min area 6 px

## Measurements
- components: final 17, mean 14.2, max 27; occupancy final 0.31
- tracks: 167; persistent (alive >= 50% of run): 0; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 9.06, final 13; holes at thresholds 0.2/0.35/0.5 final [0, 13, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [16, 16, 12]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00729/time; max body lengths 1.2
- replication: splits 60, persistent splits 12, max generation 3, merges 10, nucleations 0
- channel total drift (end/start - 1): [-0.4641, -0.6925, 0.0228, -0.1844]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 106 at frame 116: holes 1, rim-vs-core 0.26, rim-vs-outside 0.82, heterogeneity 0.21; core [0.116, 0.874, 0.629, 0.528] rim [0.175, 0.65, 0.537, 0.592]
  - track 78 at frame 87: holes 1, rim-vs-core 0.36, rim-vs-outside 0.80, heterogeneity 0.22; core [0.117, 0.872, 0.646, 0.561] rim [0.235, 0.561, 0.512, 0.596]
  - track 67 at frame 44: holes 1, rim-vs-core 0.18, rim-vs-outside 0.76, heterogeneity 0.18; core [0.098, 0.727, 0.535, 0.7] rim [0.155, 0.596, 0.491, 0.607]
  - track 133 at frame 144: holes 1, rim-vs-core 0.18, rim-vs-outside 0.83, heterogeneity 0.19; core [0.095, 0.768, 0.541, 0.628] rim [0.163, 0.606, 0.51, 0.617]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
