# Evidence pack: phase-membrane (seed 1)

- world: `../../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 11s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5365], min area 6 px

## Measurements
- components: final 15, mean 16.2, max 27; occupancy final 0.28
- tracks: 163; persistent (alive >= 50% of run): 2; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.61 (1 = constant size)
- enclosures: components with a hole mean 10.82, final 4; holes at thresholds 0.2/0.35/0.5 final [3, 4, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [17, 10, 4]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0248/time; max body lengths 1.2
- replication: splits 62, persistent splits 10, max generation 2, merges 12, nucleations 0
- channel total drift (end/start - 1): [-0.4553, -0.733, -0.045, -0.0397]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 47: holes 1, rim-vs-core 0.18, rim-vs-outside 0.75, heterogeneity 0.18; core [0.097, 0.746, 0.553, 0.684] rim [0.147, 0.602, 0.494, 0.612]
  - track 88 at frame 94: holes 0, rim-vs-core 0.54, rim-vs-outside 0.99, heterogeneity 0.22; core [0.095, 0.869, 0.58, 0.474] rim [0.319, 0.467, 0.593, 0.755]
  - track 77 at frame 62: holes 1, rim-vs-core 0.18, rim-vs-outside 0.82, heterogeneity 0.19; core [0.098, 0.778, 0.558, 0.632] rim [0.164, 0.618, 0.519, 0.609]
  - track 130 at frame 125: holes 1, rim-vs-core 0.25, rim-vs-outside 0.81, heterogeneity 0.19; core [0.104, 0.801, 0.591, 0.628] rim [0.187, 0.584, 0.511, 0.6]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
