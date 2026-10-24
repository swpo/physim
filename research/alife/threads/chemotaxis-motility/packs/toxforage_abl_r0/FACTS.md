# Evidence pack: toxforage (seed 0)

- world: `../../worlds/toxforage/world.py`, family `chemotaxis`
- parent: toxtrail; mutation: growth limited by a consumed, regrowing nutrient n (metabolism), with chemotaxis up n
- run: 201 frames x 120 steps x dt 0.05 = time 1200; grid [160, 160]; wall 127s; status ok
- command: `python -m labkit.run threads/chemotaxis-motility/worlds/toxforage/world.py --out threads/chemotaxis-motility/packs/toxforage_abl_r0 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.9744], min area 6 px

## Measurements
- components: final 4, mean 5.7, max 11; occupancy final 0.01
- tracks: 51; persistent (alive >= 50% of run): 4; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.536/time; max body lengths 53.0
- replication: splits 10, persistent splits 1, max generation 1, merges 13, nucleations 19
- channel total drift (end/start - 1): [-0.8617, -0.8613, -0.8606, -0.7715]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 123: holes 0, rim-vs-core 0.26, rim-vs-outside 0.47, heterogeneity 0.14; core [0.89, 0.605, 0.41, 0.046] rim [0.64, 0.548, 0.406, 0.063]
  - track 43 at frame 141: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.11; core [0.884, 0.548, 0.393, 0.02] rim [0.583, 0.466, 0.312, 0.047]
  - track 46 at frame 145: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.15; core [0.903, 0.622, 0.462, 0.077] rim [0.517, 0.505, 0.343, 0.127]
  - track 49 at frame 148: holes 0, rim-vs-core 0.35, rim-vs-outside 0.45, heterogeneity 0.16; core [0.92, 0.692, 0.547, 0.07] rim [0.623, 0.585, 0.404, 0.121]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
