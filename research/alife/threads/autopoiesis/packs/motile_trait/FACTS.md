# Evidence pack: motile-trait (seed 1)

- world: `../../worlds/motile_trait/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/motile_kinds + phase_trait; waste toxicity from chemotaxis-motility/worlds/toxforage; mutation: phoretic mobility is a continuous heritable trait of the catalyst, with a neutral tag as drift control; optional toxic waste
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 228s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/motile_trait/world.py --out threads/autopoiesis/packs/motile_trait --seeds 1 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5294], min area 6 px

## Measurements
- components: final 44, mean 30.0, max 44; occupancy final 0.36
- tracks: 186; persistent (alive >= 50% of run): 34; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.28 (1 = constant size)
- enclosures: components with a hole mean 1.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 44, 44], H1 [44, 44, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.011/time; max body lengths 5.1
- replication: splits 44, persistent splits 29, max generation 4, merges 1, nucleations 94
- channel total drift (end/start - 1): [-0.5308, 14.6053, 23.3109, 9.8351, 9.8919, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 121 at frame 104: holes 0, rim-vs-core 0.55, rim-vs-outside 1.34, heterogeneity 0.16; core [0.084, 0.875, 0.858, 0.821, 0.613, 0.853] rim [0.276, 0.478, 0.845, 0.723, 0.704, 0.55]
  - track 129 at frame 105: holes 0, rim-vs-core 0.58, rim-vs-outside 1.18, heterogeneity 0.17; core [0.084, 0.864, 0.623, 0.805, 0.612, 0.857] rim [0.286, 0.446, 0.606, 0.693, 0.672, 0.54]
  - track 131 at frame 108: holes 0, rim-vs-core 0.33, rim-vs-outside 1.39, heterogeneity 0.17; core [0.099, 0.859, 0.811, 0.825, 0.699, 0.827] rim [0.205, 0.614, 0.803, 0.746, 0.64, 0.663]
  - track 166 at frame 116: holes 0, rim-vs-core 0.26, rim-vs-outside 1.34, heterogeneity 0.15; core [0.116, 0.866, 0.622, 0.859, 0.79, 0.797] rim [0.179, 0.688, 0.616, 0.789, 0.666, 0.701]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
