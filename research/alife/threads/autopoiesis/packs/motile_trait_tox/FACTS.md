# Evidence pack: motile-trait-tox (seed 0)

- world: `../../worlds/motile_trait_tox/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/motile_trait; mutation: toxic waste on (kd=0.02): selection environment for the motility trait
- run: 161 frames x 300 steps x dt 1.0 = time 48000; grid [128, 128]; wall 226s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/motile_trait_tox/world.py --out threads/autopoiesis/packs/motile_trait_tox --seeds 0 --frames 160 --spf 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.5343], min area 6 px

## Measurements
- components: final 4, mean 3.8, max 6; occupancy final 0.13
- tracks: 375; persistent (alive >= 50% of run): 0; longest 24 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.33, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [6, 5, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0442/time; max body lengths 15.9
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 371
- channel total drift (end/start - 1): [-0.2296, 4.7921, 14.107, 3.4279, 1.8411, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 59: holes 0, rim-vs-core 0.50, rim-vs-outside 1.08, heterogeneity 0.19; core [0.089, 0.743, 0.553, 0.71, 0.512, 0.776] rim [0.295, 0.451, 0.547, 0.595, 0.761, 0.57]
  - track 131 at frame 82: holes 0, rim-vs-core 0.54, rim-vs-outside 1.14, heterogeneity 0.19; core [0.085, 0.743, 0.552, 0.716, 0.478, 0.831] rim [0.316, 0.446, 0.549, 0.608, 0.757, 0.581]
  - track 318 at frame 152: holes 0, rim-vs-core 0.50, rim-vs-outside 1.02, heterogeneity 0.15; core [0.118, 0.664, 0.4, 0.686, 0.587, 0.979] rim [0.356, 0.368, 0.395, 0.614, 0.699, 0.688]
  - track 7 at frame 15: holes 0, rim-vs-core 0.58, rim-vs-outside 1.00, heterogeneity 0.20; core [0.124, 0.719, 0.556, 0.74, 0.582, 0.885] rim [0.391, 0.363, 0.528, 0.585, 0.682, 0.557]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
