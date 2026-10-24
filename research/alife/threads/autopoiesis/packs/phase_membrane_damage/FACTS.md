# Evidence pack: phase-membrane (seed 0)

- world: `../../worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out threads/autopoiesis/packs/phase_membrane_damage --frames 160 --damage 40:0.3`
- segmentation: matter > 0.35 of robust range [0.0, 1.5447], min area 6 px

## Measurements
- components: final 18, mean 14.2, max 27; occupancy final 0.31
- tracks: 171; persistent (alive >= 50% of run): 1; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.35 (1 = constant size)
- enclosures: components with a hole mean 9.03, final 9; holes at thresholds 0.2/0.35/0.5 final [1, 10, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 18], H1 [17, 15, 6]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0126/time; max body lengths 1.5
- replication: splits 63, persistent splits 12, max generation 3, merges 9, nucleations 0
- channel total drift (end/start - 1): [-0.4732, -0.704, 0.0357, -0.1679]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 77 at frame 106: holes 1, rim-vs-core 0.16, rim-vs-outside 0.78, heterogeneity 0.18; core [0.099, 0.747, 0.553, 0.659] rim [0.149, 0.607, 0.498, 0.616]
  - track 76 at frame 90: holes 0, rim-vs-core 0.29, rim-vs-outside 0.91, heterogeneity 0.22; core [0.123, 0.835, 0.637, 0.626] rim [0.227, 0.587, 0.528, 0.595]
  - track 111 at frame 114: holes 1, rim-vs-core 0.27, rim-vs-outside 0.81, heterogeneity 0.20; core [0.112, 0.834, 0.611, 0.571] rim [0.193, 0.596, 0.524, 0.613]
  - track 134 at frame 140: holes 1, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.20; core [0.105, 0.782, 0.581, 0.633] rim [0.176, 0.632, 0.529, 0.595]
- damage applied at frame 40: erased 12 px of a 597 px component

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
