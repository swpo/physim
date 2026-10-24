# Evidence pack: phase-membrane (seed 2)

- world: `../../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 13s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane --seeds 0 1 2 --frames 160`
- segmentation: matter > 0.35 of robust range [0.0, 1.5463], min area 6 px

## Measurements
- components: final 15, mean 15.9, max 22; occupancy final 0.28
- tracks: 140; persistent (alive >= 50% of run): 7; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.77 (1 = constant size)
- enclosures: components with a hole mean 10.16, final 8; holes at thresholds 0.2/0.35/0.5 final [2, 9, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 15], H1 [13, 12, 6]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00743/time; max body lengths 1.6
- replication: splits 53, persistent splits 9, max generation 2, merges 7, nucleations 0
- channel total drift (end/start - 1): [-0.4558, -0.7234, -0.0327, -0.3153]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 101: holes 1, rim-vs-core 0.26, rim-vs-outside 0.69, heterogeneity 0.19; core [0.103, 0.739, 0.554, 0.689] rim [0.191, 0.535, 0.476, 0.568]
  - track 85 at frame 106: holes 0, rim-vs-core 0.36, rim-vs-outside 0.85, heterogeneity 0.18; core [0.097, 0.764, 0.527, 0.649] rim [0.277, 0.454, 0.572, 0.693]
  - track 73 at frame 87: holes 1, rim-vs-core 0.15, rim-vs-outside 0.76, heterogeneity 0.16; core [0.078, 0.655, 0.431, 0.726] rim [0.149, 0.574, 0.478, 0.627]
  - track 94 at frame 117: holes 1, rim-vs-core 0.17, rim-vs-outside 0.76, heterogeneity 0.18; core [0.098, 0.726, 0.539, 0.685] rim [0.153, 0.595, 0.492, 0.614]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
